#!/usr/bin/env python3
"""Ensure daab-activities-layout.css `html:is(...)` groups include every sidebar
layout page id. Delegates to the canonical maintainer in _forum_layout_pages."""
from __future__ import annotations

from _forum_layout_pages import sync_activities_layout_css


def sync() -> int:
    return sync_activities_layout_css()


if __name__ == "__main__":
    n = sync()
    print(f"Normalized {n} :is() selector group(s) in css/daab-activities-layout.css")
