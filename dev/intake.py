#!/usr/bin/env python3
"""Ara development intake. Classifies any dropped artifact and routes the next patch.

Not the companion. This is the build loop: logcat, screenshot, voice note,
Kotlin, JSON memory, spec text, or a plain sentence.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import re
from pathlib import Path

ROUTES = [
    ("logcat", "overlay/SparkOverlayService.kt", "Crash or permission failure. Do not add AccessibilityService."),
    ("kotlin", "domain/companion/SparkCompanionPolicy.kt", "Source patch. Package stays com.sparkx.fairyos."),
    ("screenshot", "ui/components/SparkBabyAvatar.kt", "Visual bug. Avatar stays silver fairy, dark glass."),
    ("audio", "domain/voice/SparkVoiceController.kt", "Voice input. Mic stays user-granted."),
    ("memory", "domain/memory/TeachGrowRepository.kt", "Teach and Grow. Text only. Never execute saved code."),
    ("spec", "FairyIdentity.kt", "Copy or behavior note. Safe Companion remains the default."),
    ("pwa", "ara-born/index.html", "Browser surface. Not a second source of truth."),
    ("text", "domain/command/SparkCommandRouter.kt", "Plain instruction. Map to one module."),
]

def kind_for(path: Path | None, text: str) -> str:
    name = path.name.lower() if path else ""
    mime = mimetypes.guess_type(name)[0] or ""
    if "exception" in text.lower() or "fatal exception" in text.lower() or name.endswith(".log"):
        return "logcat"
    if name.endswith((".kt", ".kts", ".java")) or "package com.sparkx.fairyos" in text:
        return "kotlin"
    if mime.startswith("image/") or name.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return "screenshot"
    if mime.startswith("audio/") or name.endswith((".m4a", ".mp3", ".wav", ".ogg")):
        return "audio"
    if "lesson" in text.lower() or name.endswith(".json") and "turns" in text:
        return "memory"
    if name.endswith((".html", ".webmanifest")):
        return "pwa"
    if name.endswith((".md", ".txt")) and len(text) > 400:
        return "spec"
    return "text"

def route(kind: str) -> tuple[str, str]:
    for key, target, rule in ROUTES:
        if key == kind:
            return target, rule
    return ROUTES[-1][1], ROUTES[-1][2]

def adapt(text: str, path: Path | None = None) -> dict:
    sample = text[:4000]
    kind = kind_for(path, sample)
    target, rule = route(kind)
    signals = []
    if re.search(r"overlay|bubble|draw over", sample, re.I):
        signals.append("overlay")
    if re.search(r"mic|speech|tts|voice", sample, re.I):
        signals.append("voice")
    if re.search(r"owner|core|seal", sample, re.I):
        signals.append("core")
    if re.search(r"crash|exception|anr", sample, re.I):
        signals.append("failure")
    return {
        "input": path.name if path else "stdin",
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
