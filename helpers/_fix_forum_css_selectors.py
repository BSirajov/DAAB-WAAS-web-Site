#!/usr/bin/env python3
"""Fix broken forum-impressions / forum-roadmap CSS selector pairs."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PAIR_FIX = re.compile(
    r'(html\[data-daab-page-id="forum-impressions"\]),\s*\n'
    r'(html\[data-daab-page-id="forum-roadmap"\])([^,\n{]+)',
    re.MULTILINE,
)


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")

    def repl(m: re.Match[str]) -> str:
        suffix = m.group(3)
        return f"{m.group(1)}{suffix},\n{m.group(2)}{suffix}"

    new_text, count = PAIR_FIX.subn(repl, text)
    if count:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    for rel in ("css/daab-forum-content.css", "css/daab-activities-layout.css"):
        n = fix_file(ROOT / rel)
        print(f"{rel}: fixed {n} selector pair(s)")


if __name__ == "__main__":
    main()
