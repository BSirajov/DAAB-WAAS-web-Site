#!/usr/bin/env python3
"""Add forum-rector-speeches and forum-anas-leadership-speeches to daab-forum-content.css."""
from __future__ import annotations

import re

from _forum_layout_pages import NEW_PAGE_IDS, selector
from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"
ANCHOR_PAGE_IDS = ("forum-video-gallery",)


def last_page_id(line: str) -> str | None:
    ids = re.findall(r'data-daab-page-id="([^"]+)"', line)
    return ids[-1] if ids else None


def suffix_after_anchor(line: str, anchor: str) -> str | None:
    m = re.search(rf'{re.escape(anchor)}"\](.*)$', line)
    if not m:
        return None
    rest = m.group(1)
    if rest.endswith(" {"):
        return rest[:-2]
    if rest.endswith("{"):
        return rest[:-1]
    if rest.endswith(","):
        return rest[:-1]
    return rest


def insert_after_anchor_line(line: str) -> list[str]:
    anchor = last_page_id(line)
    if anchor not in ANCHOR_PAGE_IDS:
        return [line]
    if any(pid in line for pid in NEW_PAGE_IDS):
        return [line]

    suffix = suffix_after_anchor(line, anchor)
    if suffix is None:
        return [line]

    stripped = line.rstrip()
    ends_brace = stripped.endswith(" {") or stripped.endswith("{")
    selectors = [f'html[data-daab-page-id="{anchor}"]{suffix}']
    for pid in NEW_PAGE_IDS:
        selectors.append(selector(pid, suffix))

    out: list[str] = []
    for i, sel in enumerate(selectors):
        if i < len(selectors) - 1:
            out.append(sel + ",")
        elif ends_brace:
            out.append(sel + " {")
        else:
            out.append(sel + ",")
    return out


def sync() -> int:
    text = CSS.read_text(encoding="utf-8")
    if all(pid in text for pid in NEW_PAGE_IDS) and 'forum-rector-speeches"] .forum-breadcrumbs' in text:
        print("Speech page IDs already present in forum-content CSS")
        return 0

    lines = text.splitlines()
    out: list[str] = []
    added = 0

    for line in lines:
        if (
            line.strip().startswith("html[")
            and 'data-daab-page-id="forum-' in line
            and last_page_id(line) in ANCHOR_PAGE_IDS
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
    print(f"Inserted {n} selector line(s) into {CSS.relative_to(ROOT)}")
