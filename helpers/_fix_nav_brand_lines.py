#!/usr/bin/env python3
"""Rewrite nav brand labels into two locked .nav-brand-line spans (no soft-wrap)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

BRAND_RES = [
    (
        re.compile(
            r'(<span class="nav-brand-text">)\s*'
            r"World Association of\s*"
            r'(?:<br\s+class="mobile-hidden-break"\s*/?>)\s*'
            r"Azerbaijani Scientists\s*"
            r"(</span>)",
            re.IGNORECASE,
        ),
        r'\1<span class="nav-brand-line">World Association of</span>'
        r'<span class="nav-brand-line">Azerbaijani Scientists</span>\2',
    ),
    (
        re.compile(
            r'(<span class="nav-brand-text">)\s*'
            r"Dünya Azərbaycanlı\s*"
            r'(?:<br\s+class="mobile-hidden-break"\s*/?>)\s*'
            r"Alimlər Birliyi\s*"
            r"(</span>)",
            re.IGNORECASE,
        ),
        r'\1<span class="nav-brand-line">Dünya Azərbaycanlı</span>'
        r'<span class="nav-brand-line">Alimlər Birliyi</span>\2',
    ),
]


def iter_html() -> list[Path]:
    out: list[Path] = []
    for base in (ROOT / "az", ROOT / "en", ROOT / "templates"):
        if not base.exists():
            continue
        out.extend(p for p in base.rglob("*.html") if p.is_file())
    for name in ("index.html", "404.html"):
        p = ROOT / name
        if p.is_file():
            out.append(p)
    return sorted(out)


def patch_text(text: str) -> str:
    for pattern, repl in BRAND_RES:
        text = pattern.sub(repl, text)
    return text


def main() -> int:
    updated = 0
    for path in iter_html():
        original = path.read_text(encoding="utf-8")
        text = patch_text(original)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            updated += 1
            print(f"  updated {path.relative_to(ROOT)}")
    print(f"Done — {updated} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
