#!/usr/bin/env python3
"""Add forum-logistics selectors mirroring forum-program lines in shared CSS files."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PROGRAM_LINE = re.compile(r'^(\s*)html\[data-daab-page-id="forum-program"\](.*)$')

TARGETS = (
    ROOT / "css" / "daab-forum-content.css",
    ROOT / "css" / "daab-activities-layout.css",
)


def patch_file(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        match = PROGRAM_LINE.match(line)
        if not match:
            out.append(line)
            continue
        if i + 1 < len(lines) and "forum-logistics" in lines[i + 1]:
            out.append(line)
            continue
        indent, rest = match.group(1), match.group(2)
        if rest.endswith("{"):
            suffix = rest[:-1]
            out.append(f'{indent}html[data-daab-page-id="forum-program"]{suffix},')
            out.append(f'{indent}html[data-daab-page-id="forum-logistics"]{suffix}{{')
        else:
            out.append(line)
            out.append(f'{indent}html[data-daab-page-id="forum-logistics"]{rest}')
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return path.read_text(encoding="utf-8").count("forum-logistics")


def main() -> None:
    for path in TARGETS:
        count = patch_file(path)
        print(f"{path.relative_to(ROOT)}: forum-logistics selector lines = {count}")


if __name__ == "__main__":
    main()
