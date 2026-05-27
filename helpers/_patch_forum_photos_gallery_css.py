#!/usr/bin/env python3
"""Add forum-photos-gallery alongside forum-cooperation in daab-forum-content.css."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"
MARKER = "forum-photos-gallery"


def expand_line(line: str) -> str:
    if MARKER in line or 'data-daab-page-id="forum-cooperation"' not in line:
        return line

    def repl(m: re.Match[str]) -> str:
        suffix = m.group(1)
        brace = ""
        if suffix.endswith("{"):
            brace = "{"
            suffix = suffix[:-1]
        return (
            f'html[data-daab-page-id="forum-cooperation"]{suffix},\n'
            f'html[data-daab-page-id="{MARKER}"]{suffix}{brace}'
        )

    return re.sub(
        r'html\[data-daab-page-id="forum-cooperation"\]([^\n,]*)',
        repl,
        line,
    )


def main() -> None:
    text = CSS.read_text(encoding="utf-8")
    if MARKER in text:
        # Fix broken `{,` from an earlier patch attempt
        text = text.replace("{,", ",")
        text = text.replace("]{,", "],")
    lines = [expand_line(ln) for ln in text.splitlines()]
    if not any(MARKER in ln for ln in lines):
        lines = [expand_line(ln) for ln in CSS.read_text(encoding="utf-8").splitlines()]
    CSS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    n = sum(1 for ln in lines if MARKER in ln)
    print(f"Patched ({n} lines with {MARKER}) -> {CSS}")


if __name__ == "__main__":
    main()
