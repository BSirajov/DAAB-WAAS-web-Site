#!/usr/bin/env python3
"""Replace heavy Google Fonts URLs with a trimmed weight set across deploy HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

STANDARD_FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600;700;800&amp;'
    'family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>'
)

PATTERNS = (
    re.compile(
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/?>',
        re.I,
    ),
)


def normalize_html(text: str) -> tuple[str, int]:
    count = 0

    def repl(_: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return STANDARD_FONT_LINK

    new_text = PATTERNS[0].sub(repl, text)
    return new_text, count


def main() -> int:
    targets: list[Path] = [
        ROOT / "index.html",
        ROOT / "404.html",
    ]
    for base in (ROOT / "az", ROOT / "en"):
        if base.is_dir():
            targets.extend(sorted(base.rglob("*.html")))

    total = 0
    files = 0
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "fonts.googleapis.com/css2" not in text:
            continue
        new_text, n = normalize_html(text)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            total += n
            files += 1
            print(f"  {path.relative_to(ROOT)} ({n})")

    print(f"\nNormalized Google Fonts in {files} file(s), {total} link(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
