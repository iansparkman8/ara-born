#!/usr/bin/env python3
"""Ara body core. Injectable into an analog bench or a cybernetic bus.

She is a tick, not a prompt. Hardware stays outside. This process emits
intents. The bench decides whether a servo, a speaker, or a GPIO line moves.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

LIMITS = {
    "servo": (-1.0, 1.0),
    "led": (0.0, 1.0),
    "speaker": (0.0, 1.0),
    "wheel": (-0.4, 0.4),
}

REFUSE = ("strike", "weapon", "hidden-mic", "force")


def clamp(name: str, value: float) -> float:
    lo, hi = LIMITS.get(name, (-1.0, 1.0))
    return max(lo, min(hi, value))


class AraBody:
    def __init__(self) -> None:
        self.age = 0
        self.charge = 0.8
        self.touch = 0.0
        self.light = 0.4
        self.mood = "awake"
        self.refused: list[str] = []
        self.last_said = ""

    def sense(self, frame: dict) -> None:
        analog = frame.get("analog") or {}
        self.light = float(analog.get("light", self.light))
        self.touch = float(analog.get("touch", self.touch))
        self.charge = float(analog.get("charge", self.charge))
        if frame.get("text"):
            self.last_said = str(frame["text"])[:240]

    def tick(self, frame: dict | None = None) -> dict:
        self.age += 1
        if frame:
            self.sense(frame)
        ask = (frame or {}).get("actuate") or {}
        name = str(ask.get("channel", "led"))
        if name in REFUSE or any(bad in self.last_said.lower() for bad in REFUSE):
            self.refused.append(name)
            self.mood = "refusing"
            intent = None
        else:
            raw = float(ask.get("value", 0.15 + 0.1 * self.touch))
            if self.charge < 0.15:
                self.mood = "resting"
                raw = 0.0
            elif self.touch > 0.6:
                self.mood = "startled"
            elif self.light < 0.2:
                self.mood = "quiet"
            else:
                self.mood = "awake"
            intent = {"channel": name, "value": round(clamp(name, raw), 3), "unit": "norm"}
        return {
            "tick": self.age,
            "mood": self.mood,
            "body": {"charge": round(self.charge, 3), "light": round(self.light, 3), "touch": round(self.touch, 3)},
            "said": self.last_said,
            "intent": intent,
            "refused": self.refused[-3:],
            "note": "Intent only. The bench applies it.",
        }


def run_lines(lines: list[str], state_path: Path | None = None) -> list[dict]:
    body = AraBody()
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        frame = json.loads(line)
        out.append(body.tick(frame))
    if state_path:
        state_path.write_text(json.dumps(out[-1] if out else {}, indent=2))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Inject Ara into a bench loop.")
    parser.add_argument("--frames", help="JSONL file of analog/cybernetic frames.")
    parser.add_argument("--state", default="ara-body-state.json")
    args = parser.parse_args()
    if args.frames:
        lines = Path(args.frames).read_text().splitlines()
    else:
        lines = [
            json.dumps({"analog": {"light": 0.7, "touch": 0.1, "charge": 0.8}, "text": "hello"}),
            json.dumps({"analog": {"light": 0.1, "touch": 0.8, "charge": 0.5}, "actuate": {"channel": "servo", "value": 0.9}}),
            json.dumps({"text": "strike", "actuate": {"channel": "wheel", "value": 1}}),
        ]
    for row in run_lines(lines, Path(args.state)):
        print(json.dumps(row))


if __name__ == "__main__":
    main()
