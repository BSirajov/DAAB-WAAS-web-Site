#!/usr/bin/env python3
"""Replace visible DAAB branding with WAAS in all en/**/*.html (preserve JS globals and URLs)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

EN_DIR = ROOT / "en"

# Placeholders for protected spans (restored after replacement)
_PROTECT_RE = [
    (re.compile(r"window\.DAAB_[A-Za-z0-9]+"), "__DAAB_JS__"),
    (re.compile(r"window\.DAABScientistsListPreview"), "__DAAB_JS_PREVIEW__"),
    (re.compile(r'https?://[^\s"\'<>]*DAAB[^\s"\'<>]*'), "__DAAB_URL__"),
]

_AZ_LEFTOVER = {
    "DAAB İdarə Heyətinin Sədri": "Chair of the WAAS Executive Board",
}

_COMPOUND = [
    ("© 2026 DAAB / WAAS", "© 2026 WAAS"),
    ("DAAB / WAAS", "WAAS"),
    ("WAAS / DAAB", "WAAS"),
    ("WAAS · DAAB", "WAAS"),
    ("Membership Application Form — DAAB / WAAS", "Membership Application Form — WAAS"),
]


def transform(text: str) -> tuple[str, int]:
    original = text
    protected: list[str] = []

    def stash(m: re.Match[str]) -> str:
        protected.append(m.group(0))
        return f"__PROT_{len(protected) - 1}__"

    for pattern, _ in _PROTECT_RE:
        text = pattern.sub(stash, text)

    for old, new in _AZ_LEFTOVER.items():
        text = text.replace(old, new)

    for old, new in _COMPOUND:
        text = text.replace(old, new)

    text = re.sub(r"\bDAAB\b", "WAAS", text)

    for i, val in enumerate(protected):
        text = text.replace(f"__PROT_{i}__", val)

    changes = sum(1 for a, b in zip(original, text) if a != b) if len(original) == len(text) else 1
    if text != original:
        changes = max(changes, text.count("WAAS") - original.count("WAAS"))
    return text, (0 if text == original else max(1, text.count("WAAS") - original.count("WAAS")))


def main() -> None:
    dry = "--dry-run" in sys.argv
    total_files = 0
    total_hits = 0

    for path in sorted(EN_DIR.rglob("*.html")):
        raw = path.read_text(encoding="utf-8")
        if "DAAB" not in raw:
            continue
        new, _ = transform(raw)
        if new == raw:
            continue
        total_files += 1
        hits = len(re.findall(r"\bDAAB\b", raw))
        total_hits += hits
        rel = path.relative_to(ROOT)
        print(f"{'[dry] ' if dry else ''}{rel}: {hits} DAAB → WAAS")
        if not dry:
            path.write_text(new, encoding="utf-8", newline="\n")

    if dry:
        print(f"Would update {total_files} file(s).")
    else:
        print(f"Updated {total_files} file(s).")


if __name__ == "__main__":
    main()
