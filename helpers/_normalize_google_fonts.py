#!/usr/bin/env python3
"""Replace heavy Google Fonts URLs with a trimmed weight set across deploy HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

STANDARD_FONT_LINK = '<link href="{root}css/daab-fonts.css?v=1" rel="stylesheet"/>'

PATTERNS = (
    re.compile(
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/?>',
        re.I,
    ),
    re.compile(
        r'<link href="https://fonts\.googleapis\.com" rel="preconnect"\s*/>\s*'
        r'<link crossorigin="" href="https://fonts\.gstatic\.com" rel="preconnect"\s*/>\s*'
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/?>',
        re.I,
    ),
)


def normalize_html(text: str, *, css_root: str = "../") -> tuple[str, int]:
    count = 0
    local = STANDARD_FONT_LINK.format(root=css_root)

    def repl(_: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return local

    new_text = text
    for pattern in PATTERNS:
        new_text, n = pattern.subn(repl, new_text)
        count += n
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
        if "fonts.googleapis.com/css2" not in text and "daab-fonts.css" in text:
            continue
        depth = len(path.relative_to(ROOT).parts) - 1
        css_root = "../" * depth if depth else ""
        new_text, n = normalize_html(text, css_root=css_root)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            total += n
            files += 1
            print(f"  {path.relative_to(ROOT)} ({n})")

    print(f"\nNormalized Google Fonts in {files} file(s), {total} link(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
