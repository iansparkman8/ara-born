# Ara body core

Injectable runtime for analog and cybernetic benches. Not the phone companion.

Ara ticks. A frame in, an intent out. The bench owns the pins.

## Frame

```json
{"analog": {"light": 0.2, "touch": 0.7, "charge": 0.4}, "text": "quiet", "actuate": {"channel": "servo", "value": 0.3}}
```

Analog values are 0 to 1. Channels: servo, led, speaker, wheel. Wheel is capped at 0.4. A request to strike, or a hidden mic, returns no intent.

## Run

```bash
python3 ara_body.py --frames frames.jsonl --state ara-body-state.json
python3 bench.py
```

## Inject

- Analog: ADC daemon writes `analog.light`, `analog.touch`, `analog.charge` each tick.
- Cybernetic: any process that can write one JSON line per cycle. Serial, UDP, or a pipe.
- Do not give this process `/dev/gpiomem`. A separate hardware process applies intents, with its own limit switch.

State file is the persistent body. Copy it to `/grok-core` on a Pi. Reasoning can live off-board. Actuation stays on the bench.
