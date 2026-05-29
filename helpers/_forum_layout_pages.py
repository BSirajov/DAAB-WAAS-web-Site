#!/usr/bin/env python3
"""Page IDs that share Activities-style sidebar + news-feed layout (daab-activities-layout.css)."""
from __future__ import annotations

import re

# Keep in sync with css/daab-activities-layout.css selector lists.
FORUM_SIDEBAR_LAYOUT_PAGE_IDS: tuple[str, ...] = (
    "activities",
    "forum-official",
    "forum-rector-speeches",
    "forum-anas-leadership-speeches",
    "forum-program",
    "forum-2024-presentations",
    "forum-impressions",
    "forum-roadmap",
    "forum-bagli-hekayeler",
    "forum-cooperation",
    "forum-photos-gallery",
)

ANCHOR_PAGE_ID = "forum-cooperation"
NEW_PAGE_IDS = ("forum-rector-speeches", "forum-anas-leadership-speeches")


def selector(page_id: str, suffix: str = "") -> str:
    return f'html[data-daab-page-id="{page_id}"]{suffix}'


def sync_activities_layout_css() -> int:
    """Append missing page selectors to comma lists (before the opening brace)."""
    from _paths import ROOT

    path = ROOT / "css" / "daab-activities-layout.css"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    added = 0
    anchor = f'html[data-daab-page-id="{ANCHOR_PAGE_ID}"]'

    for i, line in enumerate(lines):
        out.append(line)
        if anchor not in line or not line.strip().startswith("html["):
            continue
        if any(pid in line for pid in NEW_PAGE_IDS):
            continue
        # Only extend lists that end on this line (comma or opening brace)
        stripped = line.rstrip()
        if not (stripped.endswith(",") or stripped.endswith(" {")):
            continue
        m = re.search(rf'{re.escape(ANCHOR_PAGE_ID)}"\](.*)$', line)
        if not m:
            continue
        suffix = m.group(1).removesuffix(" {").rstrip()
        insert_at = len(out)
        for pid in NEW_PAGE_IDS:
            sel = selector(pid, suffix)
            if sel in text:
                continue
            out.insert(insert_at, sel)
            insert_at += 1
            added += 1
            text += "\n" + sel
        # Comma-terminate anchor line when brace was on same line
        if stripped.endswith(" {"):
            out[-1] = stripped[:-2] + ","

    if added:
        path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return added


if __name__ == "__main__":
    n = sync_activities_layout_css()
    print(f"Added {n} selector line(s) to css/daab-activities-layout.css")
