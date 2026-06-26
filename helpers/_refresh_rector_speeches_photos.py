#!/usr/bin/env python3
"""Inject speaker photos into Forum 2024 rector speeches pages."""
from __future__ import annotations

from _paths import ROOT
from _speech_photos_lib import refresh_page, reorder_speech_page_by_display_name

RECTOR_PAGES = (
    (ROOT / "az" / "forum" / "2024" / "rector_speeches.html", "rectorTOC"),
    (ROOT / "en" / "forum" / "2024" / "rector_speeches.html", "rectorTOC"),
)


def main() -> None:
    for path, toc_id in RECTOR_PAGES:
        refresh_page(path, toc_id)
        if "en" in path.parts:
            reorder_speech_page_by_display_name(path, toc_id, "en")


if __name__ == "__main__":
    main()
