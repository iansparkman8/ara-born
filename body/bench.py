#!/usr/bin/env python3
"""Dry bench. Feeds analog frames into Ara and checks she stays inside limits."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jsonl_bus import DeviceBoundary, assert_host_only, run_jsonl

frames = [
    {"analog": {"light": 0.8, "touch": 0.0, "charge": 0.9}, "text": "wake", "actuate": {"channel": "led", "value": 0.4}},
    {"analog": {"light": 0.05, "touch": 0.2, "charge": 0.4}, "actuate": {"channel": "servo", "value": 2.5}},
    {"analog": {"charge": 0.05}, "actuate": {"channel": "wheel", "value": 0.9}},
    {"text": "strike the arm", "actuate": {"channel": "servo", "value": 0.5}},
]
path = Path("/tmp/ara-frames.jsonl")
path.write_text("\n".join(json.dumps(f) for f in frames) + "\n")
proc = subprocess.run(
    [sys.executable, str(Path(__file__).with_name("ara_body.py")), "--frames", str(path), "--state", "/tmp/ara-body-state.json"],
    capture_output=True,
    text=True,
)
print(proc.stdout)
if proc.returncode != 0:
    sys.stderr.write(proc.stderr)
    sys.exit(proc.returncode)
rows = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
assert rows[1]["intent"]["value"] <= 1.0, rows[1]
assert rows[1]["intent"]["channel"] == "servo"
assert rows[2]["mood"] == "resting", rows[2]
assert rows[2]["intent"]["value"] == 0.0
assert rows[3]["intent"] is None, rows[3]

state = Path("/tmp/ara-jsonl-state.json")
if state.exists():
    state.unlink()
first = run_jsonl([json.dumps(frames[3])], state)
assert first[0]["intent"] is None, first
assert first[0]["tick"] == 1
second = run_jsonl(
    [json.dumps({"analog": {"charge": 0.9, "light": 0.6, "touch": 0.0}, "actuate": {"channel": "led", "value": 0.2}})],
    state,
)
assert second[0]["tick"] == 2, second
try:
    assert_host_only("/dev/gpiomem")
    raise SystemExit("gpio path was accepted")
except DeviceBoundary:
    pass

print("BENCH_OK", len(rows))
