#!/usr/bin/env python3
"""Mark decorative forum TOC/partner photos for accessibility (aria-hidden on redundant thumbs)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

TOC_PHOTO_RE = re.compile(
    r'(<img\b(?=[^>]*\bclass="[^"]*(?:presentation-toc-photo|rector-toc-photo|impression-toc-photo)[^"]*")'
    r'(?![^>]*\baria-hidden=)[^>]*\balt="")',
    re.I,
)

PARTNER_LOGO_RE = re.compile(
    r'(<div class="forum-partner-logo[^"]*">\s*<img\b(?![^>]*\baria-hidden=)[^>]*\balt="")',
    re.I,
)

LIGHTBOX_PLACEHOLDER_RE = re.compile(
    r'(<img\b(?=[^>]*\bid="photosGalleryLightboxImg")(?![^>]*\baria-hidden=)[^>]*\balt="")',
    re.I,
)

PAGES = (
    ROOT / "az" / "forum" / "2024" / "index.html",
    ROOT / "en" / "forum" / "2024" / "index.html",
    ROOT / "az" / "forum" / "2024" / "photos_gallery.html",
    ROOT / "en" / "forum" / "2024" / "photos_gallery.html",
    ROOT / "az" / "forum" / "2024" / "official.html",
    ROOT / "en" / "forum" / "2024" / "official.html",
    ROOT / "az" / "forum" / "2024" / "presentations.html",
    ROOT / "en" / "forum" / "2024" / "presentations.html",
    ROOT / "az" / "forum" / "2024" / "rector_speeches.html",
    ROOT / "en" / "forum" / "2024" / "rector_speeches.html",
    ROOT / "az" / "forum" / "2024" / "anas_leadership_speeches.html",
    ROOT / "en" / "forum" / "2024" / "anas_leadership_speeches.html",
    ROOT / "az" / "forum" / "2024" / "impressions.html",
    ROOT / "en" / "forum" / "2024" / "impressions.html",
)


def patch_html(text: str) -> tuple[str, int]:
    count = 0

    def add_hidden(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return match.group(1) + ' aria-hidden="true"'

    text = TOC_PHOTO_RE.sub(add_hidden, text)
    text = PARTNER_LOGO_RE.sub(add_hidden, text)
    text = LIGHTBOX_PLACEHOLDER_RE.sub(add_hidden, text)
    return text, count


def main() -> None:
    total = 0
    for path in PAGES:
        if not path.is_file():
            print(f"  skip (missing): {path.relative_to(ROOT)}")
            continue
        original = path.read_text(encoding="utf-8")
        updated, n = patch_html(original)
        if n:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"  {path.relative_to(ROOT)}: {n} img(s)")
            total += n
    print(f"Done — {total} decorative forum images marked aria-hidden.")


if __name__ == "__main__":
    main()
