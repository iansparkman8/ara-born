#!/usr/bin/env python3
"""Serial-shaped JSONL bus for Ara.

Frames in, intents out, one JSON object per line. This is the shape a
serial line would carry. This process does not open /dev/gpiomem, a UART,
or any other device node. A second process applies intents to hardware.

The state file is what survives reboot. On a Pi the copy target is
/grok-core (for example /grok-core/ara-body-state.json).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ara_body import AraBody


class DeviceBoundary(RuntimeError):
    """Raised if a caller tries to hand this process a device node."""


def assert_host_only(path: str | Path) -> None:
    text = str(path)
    if text.startswith("/dev/"):
        raise DeviceBoundary(
            "This process does not get /dev/gpiomem. A second process applies intents."
        )


def load_body(state_path: Path) -> AraBody:
    body = AraBody()
    if not state_path.exists():
        return body
    try:
        prev = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return body
    body.age = int(prev.get("tick") or 0)
    body.mood = str(prev.get("mood") or body.mood)
    body.last_said = str(prev.get("said") or "")
    body.refused = list(prev.get("refused") or [])
    analog = prev.get("body") or {}
    try:
        body.charge = float(analog.get("charge", body.charge))
        body.light = float(analog.get("light", body.light))
        body.touch = float(analog.get("touch", body.touch))
    except (TypeError, ValueError):
        pass
    return body


def run_jsonl(lines: list[str], state_path: Path) -> list[dict]:
    assert_host_only(state_path)
    body = load_body(state_path)
    out: list[dict] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        frame = json.loads(line)
        out.append(body.tick(frame))
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(out[-1] if out else {}, indent=2),
        encoding="utf-8",
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read JSONL frames, write JSONL intents. Does not touch GPIO."
    )
    parser.add_argument(
        "--frames",
        help="JSONL file. Omit to read stdin. Do not pass a /dev node.",
    )
    parser.add_argument(
        "--state",
        default="ara-body-state.json",
        help="State file that survives reboot. Pi copy target: /grok-core/",
    )
    args = parser.parse_args()
    assert_host_only(args.state)
    if args.frames:
        assert_host_only(args.frames)
        lines = Path(args.frames).read_text(encoding="utf-8").splitlines()
    else:
        lines = sys.stdin.read().splitlines()
    for row in run_jsonl(lines, Path(args.state)):
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
