#!/usr/bin/env python3
"""Ara development intake. Classifies a dropped artifact and routes the next patch.

Not the companion. This is the build loop: logcat, screenshot, voice note,
Kotlin, JSON memory, spec text, or a plain sentence.

Never route a crash to AccessibilityService. Safe Companion stays the boot path.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import re
from pathlib import Path

COMPANION = "domain/companion/SparkCompanionPolicy.kt"
OVERLAY = "overlay/SparkOverlayService.kt"
VOICE = "domain/voice/SparkVoiceController.kt"
TEACH = "domain/memory/TeachGrowRepository.kt"
IDENTITY = "FairyIdentity.kt"
AVATAR = "ui/components/SparkBabyAvatar.kt"
PERMS = "ui/screens/PermissionWizardScreen.kt"
COMMAND = "domain/command/SparkCommandRouter.kt"
BABY = "baby/index.html"

NO_A11Y = "Do not add AccessibilityService."


def _low(text: str) -> str:
    return text.lower()


def _has(blob: str, *words: str) -> bool:
    low = _low(blob)
    return any(word in low for word in words)


def kind_for(path: Path | None, text: str) -> str:
    name = path.name.lower() if path else ""
    mime = mimetypes.guess_type(name)[0] or ""
    # A real source file stays source, even if the body mentions an exception.
    if name.endswith((".kt", ".kts", ".java")) or "package com.sparkx.fairyos" in text:
        return "kotlin"
    if "fatal exception" in _low(text) or "exception" in _low(text) or name.endswith(".log"):
        return "logcat"
    if mime.startswith("image/") or name.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return "screenshot"
    if mime.startswith("audio/") or name.endswith((".m4a", ".mp3", ".wav", ".ogg")):
        return "audio"
    if name.endswith(".json") and _has(text, "turns", "lessons"):
        return "memory"
    if name.endswith((".html", ".webmanifest")):
        return "pwa"
    if name.endswith((".md", ".txt")) and len(text) > 400:
        return "spec"
    return "text"


def module_for(kind: str, text: str, name: str) -> tuple[str, str]:
    blob = f"{name}\n{text}"
    crash = kind == "logcat" or _has(blob, "fatal exception", "crash", "anr")

    if crash and _has(blob, "overlay", "bubble", "windowmanager"):
        return OVERLAY, f"Overlay crash. Patch the overlay service. {NO_A11Y}"
    if crash and _has(blob, "voice", "speech", "tts", "microphone"):
        return VOICE, f"Voice crash. Mic stays user-granted. {NO_A11Y}"
    if crash and _has(blob, "permission"):
        return PERMS, f"Permission failure. Patch the wizard. {NO_A11Y}"
    if crash and _has(blob, "accessibilityservice", "accessibility service"):
        return COMPANION, f"{NO_A11Y} Keep Safe Companion bootable."
    if crash:
        return OVERLAY, f"Crash or permission failure. {NO_A11Y}"

    if kind == "kotlin":
        if _has(blob, "sparkoverlayservice", "overlay service", "class sparkoverlay"):
            return OVERLAY, f"Overlay source. Package stays com.sparkx.fairyos. {NO_A11Y}"
        if _has(blob, "sparkvoicecontroller", "speechrecognizer"):
            return VOICE, "Voice controller. Mic stays user-granted."
        if _has(blob, "teachgrowrepository", "teach & grow", "teach and grow"):
            return TEACH, "Teach and Grow. Text only. Never execute saved code."
        if _has(blob, "fairyidentity"):
            return IDENTITY, "Copy or names. Safe Companion remains the default."
        if _has(blob, "sparkbabyavatar"):
            return AVATAR, "Avatar stays a silver fairy drawn on the Compose canvas."
        if _has(blob, "permissionwizard"):
            return PERMS, "Permissions: overlay, mic, notifications. Nothing else."
        return COMPANION, "Source patch. Package stays com.sparkx.fairyos."

    if kind == "screenshot":
        return AVATAR, "Visual bug. Avatar stays silver fairy, dark glass."
    if kind == "audio":
        return VOICE, "Voice input. Mic stays user-granted."
    if kind == "memory":
        return TEACH, "Teach and Grow. Text only. Never execute saved code."
    if kind == "spec":
        return IDENTITY, "Copy or behavior note. Safe Companion remains the default."
    if kind == "pwa":
        return BABY, "Browser surface. Not a second source of truth."
    return COMMAND, "Plain instruction. Map to one module."


def adapt(text: str, path: Path | None = None) -> dict:
    sample = text[:4000]
    name = path.name if path else "stdin"
    kind = kind_for(path, sample)
    target, rule = module_for(kind, sample, name)
    if "AccessibilityService" in target:
        target = COMPANION
        rule = f"{NO_A11Y} Keep Safe Companion bootable."
    signals = []
    if re.search(r"overlay|bubble|draw over", sample, re.I):
        signals.append("overlay")
    if re.search(r"mic|speech|tts|voice", sample, re.I):
        signals.append("voice")
    if re.search(r"owner|core|seal", sample, re.I):
        signals.append("core")
    if re.search(r"crash|exception|anr", sample, re.I):
        signals.append("failure")
    if re.search(r"accessibility", sample, re.I):
        signals.append("refused-a11y")
    return {
        "input": name,
        "kind": kind,
        "bytes": path.stat().st_size if path and path.exists() else len(sample.encode()),
        "signals": signals,
        "module": target,
        "rule": rule,
        "next": f"Patch {target}. Keep Safe Companion bootable. {rule}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route any Ara dev input to one module.")
    parser.add_argument("paths", nargs="*", help="Files of any type. Text is read. Binary is classified by name.")
    parser.add_argument("--text", default="", help="Inline instruction.")
    args = parser.parse_args()
    reports = []
    if args.text:
        reports.append(adapt(args.text))
    for raw in args.paths:
        path = Path(raw)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        reports.append(adapt(text, path))
    print(json.dumps(reports, indent=2))


if __name__ == "__main__":
    main()
