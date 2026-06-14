#!/usr/bin/env python3
"""Repair forum-program selectors broken by naive _sync_sessions_page_css.py replace."""
from __future__ import annotations

import re

from _paths import ROOT

BROKEN = re.compile(
    r'html\[data-daab-page-id="forum-program"\],\n'
    r'html\[data-daab-page-id="forum-sessions-organization"\]([^\n{]+)'
)


def repair_css(text: str) -> tuple[str, int]:
    return BROKEN.subn(
        r'html[data-daab-page-id="forum-program"]\1,\n'
        r'html[data-daab-page-id="forum-sessions-organization"]\1',
        text,
    )


def main() -> None:
    total = 0
    for rel in ("css/daab-forum-content.css", "css/daab-activities-layout.css"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        fixed, n = repair_css(text)
        if n:
            path.write_text(fixed, encoding="utf-8", newline="\n")
        print(f"{rel}: repaired {n} broken selector pair(s)")
        total += n
    if not total:
        print("No repairs needed")


if __name__ == "__main__":
    main()
