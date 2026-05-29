#!/usr/bin/env python3
"""Repair daab-activities-layout.css: merge stray selector lines into comma lists."""
from __future__ import annotations

import re
from _paths import ROOT


def fix_selector_lists(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    fixes = 0
    i = 0
    sel_re = re.compile(r'^(\s*)html\[data-daab-page-id=')

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        if (
            stripped.endswith(" {")
            and i + 1 < len(lines)
            and lines[i + 1].strip().endswith(" {")
            and sel_re.match(lines[i + 1])
        ):
            out.append(stripped[:-2] + ",")
            fixes += 1
            i += 1
            continue
        out.append(line)
        i += 1

    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), fixes


def main() -> None:
    path = ROOT / "css" / "daab-activities-layout.css"
    text = path.read_text(encoding="utf-8")
    fixed, n = fix_selector_lists(text)
    if n:
        # v14 — rector + ANAS leadership speeches sidebar layout (News parity)
        fixed = re.sub(
            r"^\s*\* v13 —",
            " * v14 —",
            fixed,
            count=1,
            flags=re.MULTILINE,
        )
        path.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"Merged {n} broken selector brace(s) in {path.name}")


if __name__ == "__main__":
    main()
