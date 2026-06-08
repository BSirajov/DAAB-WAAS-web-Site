#!/usr/bin/env python3
"""Inject speaker photos into Forum 2024 ANAS leadership speeches pages."""
from __future__ import annotations

from _paths import ROOT
from _speech_photos_lib import refresh_page

ANAS_PAGES = (
    (ROOT / "az" / "forum" / "2024" / "anas_leadership_speeches.html", "anasTOC"),
    (ROOT / "en" / "forum" / "2024" / "anas_leadership_speeches.html", "anasTOC"),
    (ROOT / "Deployment" / "az" / "forum" / "2024" / "anas_leadership_speeches.html", "anasTOC"),
    (ROOT / "Deployment" / "en" / "forum" / "2024" / "anas_leadership_speeches.html", "anasTOC"),
)


def main() -> None:
    for path, toc_id in ANAS_PAGES:
        refresh_page(path, toc_id)


if __name__ == "__main__":
    main()
