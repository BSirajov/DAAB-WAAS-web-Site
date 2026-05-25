#!/usr/bin/env python3
"""Fix broken forum-roadmap / forum-bagli-hekayeler CSS selector triples and pairs."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# roadmap"], bagli"], cooperation"] .suffix  →  all three get .suffix
TRIPLE_FIX = re.compile(
    r'html\[data-daab-page-id="forum-roadmap"\],\s*\n'
    r'html\[data-daab-page-id="forum-bagli-hekayeler"\],\s*\n'
    r'html\[data-daab-page-id="forum-cooperation"\]([^\{]*)\{',
    re.MULTILINE,
)

# impressions"], roadmap"] .suffix  →  both get .suffix
IMPRESSIONS_ROADMAP_FIX = re.compile(
    r'(html\[data-daab-page-id="forum-impressions"\]),\s*\n'
    r'(html\[data-daab-page-id="forum-roadmap"\])([^,\n{]+)',
    re.MULTILINE,
)

# bagli"], cooperation"] .suffix  →  both get .suffix (when roadmap not in triple)
BAGLI_PAIR_FIX = re.compile(
    r'html\[data-daab-page-id="forum-bagli-hekayeler"\],\s*\n'
    r'html\[data-daab-page-id="forum-cooperation"\]([^\{]*)\{',
    re.MULTILINE,
)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    count = 0

    def triple_repl(m: re.Match[str]) -> str:
        suffix = m.group(1)
        return (
            f'html[data-daab-page-id="forum-roadmap"]{suffix},\n'
            f'html[data-daab-page-id="forum-bagli-hekayeler"]{suffix},\n'
            f'html[data-daab-page-id="forum-cooperation"]{suffix}{{'
        )

    text, n = TRIPLE_FIX.subn(triple_repl, text)
    count += n

    def ir_repl(m: re.Match[str]) -> str:
        suffix = m.group(3)
        return f"{m.group(1)}{suffix},\n{m.group(2)}{suffix}"

    text, n = IMPRESSIONS_ROADMAP_FIX.subn(ir_repl, text)
    count += n

    def bagli_repl(m: re.Match[str]) -> str:
        suffix = m.group(1)
        return (
            f'html[data-daab-page-id="forum-bagli-hekayeler"]{suffix},\n'
            f'html[data-daab-page-id="forum-cooperation"]{suffix}{{'
        )

    text, n = BAGLI_PAIR_FIX.subn(bagli_repl, text)
    count += n

    if count:
        path.write_text(text, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    for rel in ("css/daab-forum-content.css", "css/daab-activities-layout.css"):
        n = fix_file(ROOT / rel)
        print(f"{rel}: fixed {n} replacement(s)")


if __name__ == "__main__":
    main()
