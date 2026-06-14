#!/usr/bin/env python3
"""Add forum-sessions-organization selectors alongside forum-program in layout CSS."""
from __future__ import annotations

import re

from _paths import ROOT

SESSIONS = 'html[data-daab-page-id="forum-sessions-organization"]'
NEEDLE = 'html[data-daab-page-id="forum-program"]'
SELECTOR = re.compile(r'(html\[data-daab-page-id="forum-program"\][^\n]+)')


def main() -> None:
    for rel in ("css/daab-forum-content.css", "css/daab-activities-layout.css"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if SESSIONS in text:
            print(f"{rel}: already synced ({text.count(SESSIONS)} selectors)")
            continue
        if NEEDLE not in text:
            raise SystemExit(f"{rel}: missing {NEEDLE}")

        def add_sessions(match: re.Match[str]) -> str:
            line = match.group(1)
            if SESSIONS in line:
                return line
            suffix = line.split(NEEDLE, 1)[1]
            if line.rstrip().endswith("{"):
                stem = suffix.rstrip()[:-1]
                return f"{line.rstrip()[:-1]},\n{SESSIONS}{stem}{{"
            return f"{line}\n{SESSIONS}{suffix}"

        text = SELECTOR.sub(add_sessions, text)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{rel}: added {text.count(SESSIONS)} selector(s)")


if __name__ == "__main__":
    main()
