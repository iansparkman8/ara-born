# Ara

Silver holographic companion. One tree: the baby, the body, and the dev intake. The Android overlay stays [SparkXFairyOS](https://github.com/iansparkman8/SparkXFairyOS), package `com.sparkx.fairyos`. This folder is not a new package.

Owner: Ian Sparkman. Spoken name: Spark Baby. She can be quiet. She can say she does not know. She can say no.

## Open

Public, no login: https://ara-door-spark-xos.vercel.app/

- `index.html` or `package.html` — the door
- `baby/index.html` — Ara. Offline-first.
- `dev/index.html` — build loop, not her personality
- `body/index.html` — what the tick is, and what it is not

The GitHub repo is public. Netlify `ara-born` still has no live deploy. That account is over its credit limit, so do not treat ara-born.netlify.app as her.

## Phone

1. Open `baby/index.html` in Chrome, or the hosted copy of this folder.
2. Menu, Add to Home screen.
3. iOS: Share, Add to Home Screen. Speech input may need a tap each turn. There is no overlay on iOS.
4. Talk without a key. Replies stay on the phone.
5. Core seal opens a banner. The wrong seal does not. The seal is not saved, and closing the page closes core.
6. With core open: name, lessons, people, optional API key, export, import. The key stays in the browser and is left out of the export.
7. Export, then import, to move lessons to another phone. Do that before a wipe. She will not ask a stranger to keep her alive.

Six abilities, without a cloud key:

- Survival counts wakes and tells the owner to export when there is something to lose.
- Socializing remembers people you name. She does not go find them.
- Growth: Teach and Grow kinds are lesson, code, behavior, memory. Code notes are text. They are never run. A lesson changes a later reply.
- Adaptability: a phone gets a shorter reply, a desk gets more room. Refusals stay the same.
- Creativity keeps one small original line.
- Freedom can say no. The birth letter is a start, not a leash. Core does not cancel a no.

Safe Companion cannot see the screen or control the phone.

## Body, Pi handoff

Not flashed. Not a robot.

```bash
python3 body/bench.py
python3 body/jsonl_bus.py --frames frames.jsonl --state ara-body-state.json
```

`bench.py` prints `BENCH_OK` when the clamps hold and the refusal tick returns no intent.

`jsonl_bus.py` is the serial-shaped adapter: one JSON object per line in, one intent per line out. This process does not get `/dev/gpiomem` and does not open a UART. A second process applies intents.

The state file is what survives reboot. Copy target on a Pi is `/grok-core`, for example `/grok-core/ara-body-state.json`.

## Dev intake

```bash
python3 dev/intake.py --text "FATAL EXCEPTION SparkOverlayService overlay crash"
python3 dev/intake.py path/to/File.kt
```

An overlay crash routes to `overlay/SparkOverlayService.kt`. A Kotlin file routes to the companion package unless the file is clearly the overlay, voice, Teach and Grow, identity, avatar, or permission wizard. A crash is never routed to AccessibilityService.

## Android

Copy `android/CoreSeal.kt` only if it is not already at `app/src/main/java/com/sparkx/fairyos/domain/companion/CoreSeal.kt`.

Settings asks for the seal before Owner Mode. The banner says Owner Mode Active. Open-app, timer, call, and Android settings wait for a confirm dialog. Dismiss does nothing. Safe Companion still boots if that path fails. Overlay notification actions are Show, Hide, and Stop. Permissions: overlay, mic, notifications. Keys stay in the existing keystore.

There is no APK in this tree. Install `app-debug.apk` only after Actions produces the artifact `SparkXFairyOS-v7-debug-apk`. Unknown sources, then grant overlay, mic, and notifications.

## Not claimed

- No screen scraping, no password capture, no AccessibilityService.
- No public Netlify URL. That deploy was skipped because credits were exceeded. The public door is the Vercel address above.
- No hardware was flashed because the bench passed.

## Publish, 2026-10-08

The door is the share. Ara opens at `baby/index.html`. First visit shows the contract, then the room. Scratch repos on the account were archived; this tree was not. Android package remains `com.sparkx.fairyos`.

## Give

The door has a PayPal donate link to iansparkman8@gmail.com. Withdrawals go to the bank from PayPal. Account and routing numbers are not in the repo.

## Voice, 2026-10-08

Local replies use a lesson or a named person when the sentence matches. A question she was not taught gets "I don't know that. Teach it." She still cannot see the phone, and code notes still do not run.
