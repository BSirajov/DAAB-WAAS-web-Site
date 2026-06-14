#!/usr/bin/env python3
"""Page IDs that share Activities-style sidebar + news-feed layout (daab-activities-layout.css)."""
from __future__ import annotations

import re

# Keep in sync with css/daab-activities-layout.css selector lists.
FORUM_SIDEBAR_LAYOUT_PAGE_IDS: tuple[str, ...] = (
    "activities",
    "activities-news",
    "forum-official",
    "forum-rector-speeches",
    "forum-anas-leadership-speeches",
    "forum-program",
    "forum-logistics",
    "forum-sessions-organization",
    "forum-2024-presentations",
    "forum-impressions",
    "forum-roadmap",
    "forum-bagli-hekayeler",
    "forum-cooperation",
    "forum-photos-gallery",
)

ANCHOR_PAGE_ID = "forum-cooperation"
NEW_PAGE_IDS = ("forum-rector-speeches", "forum-anas-leadership-speeches")

# Canonical page-id set/order used inside every `html:is(...)` selector group of
# css/daab-activities-layout.css. To add a page to the shared sidebar layout,
# append its id here and run this module.
LAYOUT_IS_PAGE_IDS: tuple[str, ...] = (
    "activities-news",
    "forum-official",
    "forum-program",
    "forum-logistics",
    "forum-sessions-organization",
    "forum-2024-presentations",
    "forum-impressions",
    "forum-roadmap",
    "forum-bagli-hekayeler",
    "forum-cooperation",
    "forum-rector-speeches",
    "forum-anas-leadership-speeches",
    "forum-2026",
)

# Matches the `html:is([data-daab-page-id="..."], ...)` selector head (no suffix).
_IS_GROUP_RE = re.compile(
    r'html:is\(\[data-daab-page-id="[^"]+"\]'
    r'(?:\s*,\s*\[data-daab-page-id="[^"]+"\])*\)'
)


def selector(page_id: str, suffix: str = "") -> str:
    return f'html[data-daab-page-id="{page_id}"]{suffix}'


def canonical_is_head() -> str:
    inner = ", ".join(f'[data-daab-page-id="{pid}"]' for pid in LAYOUT_IS_PAGE_IDS)
    return f"html:is({inner})"


def sync_activities_layout_css() -> int:
    """Normalize every `html:is(...)` page-id group in daab-activities-layout.css
    to the canonical LAYOUT_IS_PAGE_IDS set/order. Returns groups changed."""
    from _paths import ROOT

    path = ROOT / "css" / "daab-activities-layout.css"
    text = path.read_text(encoding="utf-8")
    canonical = canonical_is_head()
    changed = 0

    def repl(m: "re.Match[str]") -> str:
        nonlocal changed
        if m.group(0) != canonical:
            changed += 1
        return canonical

    new = _IS_GROUP_RE.sub(repl, text)
    if new != text:
        path.write_text(new, encoding="utf-8", newline="\n")
    return changed


if __name__ == "__main__":
    n = sync_activities_layout_css()
    print(f"Normalized {n} :is() selector group(s) in css/daab-activities-layout.css")
