# Android drop-in

Package stays `com.sparkx.fairyos`. Canon repo: `iansparkman8/SparkXFairyOS`.
Do not fork Fairy, FairyOS-v7-Voice, or Spark as the source of truth.

`CoreSeal.kt` belongs at:

`app/src/main/java/com/sparkx/fairyos/domain/companion/CoreSeal.kt`

The public file keeps the SHA-256 only. Do not put the seal, an API key, or a password in git.

Wiring, on the SparkXFairyOS tree, not in this folder:

- Settings calls `CoreSeal.matches` before Owner Mode can open.
- The seal is not written to preferences. Process death returns to Safe Companion.
- A visible banner reads Owner Mode Active while core is open.
- Open-app, timer, call, and Android settings intents wait for a confirm dialog. Dismiss runs nothing.
- Safe Companion still boots if that path throws.
- Overlay is the existing foreground service. Notification actions are Show, Hide, and Stop. The bubble stays draggable.
- Permissions stay overlay, mic, and notifications. No AccessibilityService. No screen scraping. Keys stay in `AIKeyStore`.

Wiring is pull request [iansparkman8/SparkXFairyOS#1](https://github.com/iansparkman8/SparkXFairyOS/pull/1). Merge it before expecting a debug APK. This folder is not an APK.
