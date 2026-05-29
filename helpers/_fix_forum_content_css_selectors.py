#!/usr/bin/env python3
"""Fix forum-rector / forum-anas CSS selector pairs broken by naive replace_all."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"

PATTERN = re.compile(
    r'html\[data-daab-page-id="forum-rector-speeches"\],\n'
    r'html\[data-daab-page-id="forum-anas-leadership-speeches"\]([^\n]+)',
    re.MULTILINE,
)


def repl(match: re.Match[str]) -> str:
    suffix = match.group(1)
    if suffix.strip() in ("", ","):
        return match.group(0)
    return (
        f'html[data-daab-page-id="forum-rector-speeches"]{suffix}\n'
        f'html[data-daab-page-id="forum-anas-leadership-speeches"]{suffix}'
    )


def main() -> None:
    text = CSS.read_text(encoding="utf-8")
    fixed, count = PATTERN.subn(repl, text)
    if count:
        CSS.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"Fixed {count} broken selector pair(s) in {CSS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
