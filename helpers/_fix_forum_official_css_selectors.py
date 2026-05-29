#!/usr/bin/env python3
"""Copy selector suffix from next forum-* line onto bare forum-official entries."""
from __future__ import annotations

import re

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"

PATTERN = re.compile(
    r'html\[data-daab-page-id="forum-official"\],\n'
    r'(html\[data-daab-page-id="forum-[^"]+"\])([^\n]+)',
    re.MULTILINE,
)


def repl(match: re.Match[str]) -> str:
    suffix = match.group(2).rstrip()
    if not suffix or suffix == ",":
        return match.group(0)
    trailing_comma = "," if suffix.endswith(",") else ""
    core = suffix.rstrip(",").rstrip()
    return (
        f'html[data-daab-page-id="forum-official"]{core}{trailing_comma}\n'
        f"{match.group(1)}{suffix}"
    )


def main() -> None:
    text = CSS.read_text(encoding="utf-8")
    fixed, count = PATTERN.subn(repl, text)
    if count:
        CSS.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"Fixed {count} forum-official selector(s) in {CSS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
