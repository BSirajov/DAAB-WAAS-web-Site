#!/usr/bin/env python3
"""Add sidebar layout page IDs to daab-activities-layout.css selector groups."""
from __future__ import annotations

import re

from _forum_layout_pages import ANCHOR_PAGE_ID, NEW_PAGE_IDS, selector
from _paths import ROOT

CSS = ROOT / "css" / "daab-activities-layout.css"
ANCHOR = f'html[data-daab-page-id="{ANCHOR_PAGE_ID}"]'


def insert_after_anchor_line(line: str) -> list[str]:
    """Turn anchor selector line into comma list including NEW_PAGE_IDS."""
    stripped = line.rstrip()
    ends_brace = stripped.endswith(" {")
    if ends_brace:
        base = stripped[:-2].rstrip()
    elif stripped.endswith(","):
        base = stripped.rstrip(",").rstrip()
        ends_brace = False
    else:
        return [line]

    m = re.search(rf'{re.escape(ANCHOR_PAGE_ID)}"\](.*)$', base)
    if not m:
        return [line]

    suffix = m.group(1)
    selectors = [f'{ANCHOR}{suffix}']
    for pid in NEW_PAGE_IDS:
        selectors.append(selector(pid, suffix))

    out: list[str] = []
    for i, sel in enumerate(selectors):
        if i < len(selectors) - 1:
            out.append(sel + ",")
        else:
            out.append(sel + (" {" if ends_brace else ","))
    return out


def sync() -> int:
    text = CSS.read_text(encoding="utf-8")
    if all(pid in text for pid in NEW_PAGE_IDS):
        print("Page IDs already present")
        return 0

    lines = text.splitlines()
    out: list[str] = []
    added = 0

    for line in lines:
        if ANCHOR in line and line.strip().startswith("html[") and any(
            pid not in line for pid in NEW_PAGE_IDS
        ):
            new_lines = insert_after_anchor_line(line)
            if len(new_lines) > 1:
                added += len(new_lines) - 1
            out.extend(new_lines)
            continue
        out.append(line)

    if added:
        CSS.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return added


if __name__ == "__main__":
    n = sync()
    print(f"Inserted {n} selector line(s) into {CSS.name}")
