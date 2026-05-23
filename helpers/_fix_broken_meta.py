#!/usr/bin/env python3
"""Repair `<meta c\\n<link .../>ontent="..." name="..."/>` produced by a bad past insertion."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Matches the broken sequence:
#   <meta c\n<link ... />ontent="..." name="..."/>
BROKEN_RE = re.compile(
    r'<meta\s+c\s*\n\s*(?P<link><link[^>]+?/?>)ontent="(?P<desc>[^"]+)"\s+name="(?P<name>[^"]+)"\s*/?>',
    re.IGNORECASE,
)


def fix(text: str) -> tuple[str, int]:
    def repl(m: re.Match) -> str:
        return (
            f'<meta content="{m.group("desc")}" name="{m.group("name")}"/>\n'
            f'{m.group("link")}'
        )

    return BROKEN_RE.subn(repl, text)


def main() -> None:
    updated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in {"node_modules", ".git"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = fix(text)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(f"{path.relative_to(ROOT)}  ({n} occurrence)")
    print(f"Repaired {len(updated)} file(s)")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
