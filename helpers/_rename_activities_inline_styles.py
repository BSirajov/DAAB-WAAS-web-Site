#!/usr/bin/env python3
"""Rename activities page inline-style-* classes to semantic act-* names."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Old → semantic (scoped under activities page CSS)
RENAME: dict[str, str] = {
    "inline-style-001": "act-card-lead",
    "inline-style-002": "act-row-thumb",
    "inline-style-004": "act-pullquote",
    "inline-style-005": "act-thumb-row",
    "inline-style-006": "act-gallery-spaced",
    "inline-style-007": "act-gallery-compact",
    "inline-style-008": "act-float-photo",
    "inline-style-009": "act-info-panel",
    "inline-style-010": "act-info-panel-title",
    "inline-style-011": "act-info-link",
    "inline-style-012": "act-contact-panel",
    "inline-style-013": "act-contact-title",
    "inline-style-014": "act-contact-line",
    "inline-style-015": "act-contact-link",
    "inline-style-016": "act-contact-muted",
    "inline-style-017": "act-centered-wrap",
    "inline-style-018": "act-feature-img",
    "inline-style-019": "act-photo-grid",
    "inline-style-020": "act-photo-grid-cell",
    "inline-style-021": "act-photo-grid-img-lg",
    "inline-style-022": "act-photo-grid-img",
    "inline-style-023": "act-narrow-img",
    "inline-style-024": "act-video-row",
    "inline-style-025": "act-video-col",
    "inline-style-026": "act-video-thumb",
    "inline-style-027": "act-video-caption",
    "inline-style-028": "act-video-row-wrap",
    "inline-style-029": "act-portrait-img",
    "inline-style-030": "act-half-img",
    "inline-style-031": "act-inline-row",
}

CSS_PATH = ROOT / "css" / "daab-activities-page.css"
HTML_PATHS = [ROOT / "az" / "activities.html", ROOT / "en" / "activities.html"]
BUMP_PAGES = HTML_PATHS + [
    ROOT / "az" / "forum" / "2024" / "photos_gallery.html",
    ROOT / "en" / "forum" / "2024" / "photos_gallery.html",
]
NEW_CSS_VERSION = 3


def apply_renames(text: str) -> str:
    for old, new in sorted(RENAME.items(), key=lambda x: -len(x[0])):
        text = text.replace(old, new)
    return text


def remove_dead_rules(text: str) -> str:
    """Drop unused inline-style-003 (never referenced in HTML)."""
    text = re.sub(
        r"\.inline-style-003\{[^}]+\}\n?",
        "",
        text,
    )
    text = text.replace("  .inline-style-003,\n", "")
    return text


def bump_css_version(html: str) -> str:
    return re.sub(
        r"daab-activities-page\.css\?v=\d+",
        f"daab-activities-page.css?v={NEW_CSS_VERSION}",
        html,
    )


def main() -> None:
    css = CSS_PATH.read_text(encoding="utf-8")
    css_new = remove_dead_rules(apply_renames(css))
    if css_new != css:
        CSS_PATH.write_text(css_new, encoding="utf-8", newline="\n")
        print(f"Updated {CSS_PATH.relative_to(ROOT)}")

    for path in HTML_PATHS:
        text = path.read_text(encoding="utf-8")
        updated = apply_renames(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"Updated {path.relative_to(ROOT)}")

    for path in BUMP_PAGES:
        text = path.read_text(encoding="utf-8")
        bumped = bump_css_version(text)
        if bumped != text:
            path.write_text(bumped, encoding="utf-8", newline="\n")
            print(f"Bumped CSS v on {path.relative_to(ROOT)}")

    leftover = re.findall(r"inline-style-\d+", css_new)
    for path in HTML_PATHS:
        leftover.extend(re.findall(r"inline-style-\d+", path.read_text(encoding="utf-8")))
    if leftover:
        raise SystemExit(f"Leftover inline-style classes: {sorted(set(leftover))}")
    print("Done — all inline-style-* renamed to act-*.")


if __name__ == "__main__":
    main()
