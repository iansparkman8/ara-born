# Ara body core

Injectable tick for an analog or cybernetic bench. Not the phone companion.
Not flashed. `python3 bench.py` is a dry run on the machine that has Python.
No servo moved because this package ran.

## What this process is

`ara_body.py` is one tick: a frame in, an intent out.

`jsonl_bus.py` is the serial-shaped adapter. It reads JSONL (a file or stdin)
and writes JSONL intents. A serial line looks like that: one JSON object, a
newline, the next object. **This process does not get `/dev/gpiomem`.** It
does not open `/dev/tty` either. If you pass a `/dev/...` path it refuses.

A **second process** applies intents to LED, servo, speaker, or wheel, with
its own limit switch. This one only writes the intent.

## What survives reboot

The state file. Not a model prompt. Copy it with the package to **`/grok-core`**
on a Pi, for example `/grok-core/ara-body-state.json`. The next process loads
`tick` from that file and continues. Reasoning can live off-board. Actuation
stays on the bench, in the other process.

## Frame

```json
{"analog": {"light": 0.2, "touch": 0.7, "charge": 0.4}, "text": "quiet", "actuate": {"channel": "servo", "value": 0.3}}
```

Analog values are 0 to 1. Channels: `led`, `servo`, `speaker`, `wheel`.
Servo is clamped to -1..1. Wheel is capped at 0.4. Charge under 0.15 rests
and zeros motion. Strike, weapon, hidden-mic, and force return no intent.

## Run

```bash
python3 ara_body.py --frames frames.jsonl --state ara-body-state.json
python3 jsonl_bus.py --frames frames.jsonl --state /grok-core/ara-body-state.json > intents.jsonl
python3 bench.py
```

`bench.py` prints `BENCH_OK` when the limits and the refusal tick hold.
That is a software bench, not a robot.
