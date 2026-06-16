#!/usr/bin/env python3
"""One-shot site cleanup: foundation image paths, asset cache bumps, legacy nav strip."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Canonical ?v= for deploy HTML — keep in sync with latest page builds (May 2026).
SCRIPT_VERSIONS = {
    "daab-i18n.js": 37,
    "daab-lang-position.js": 7,
    "daab-design-tokens.js": 2,
    "daab-nav.js": 31,
    "daab-primary-nav.js": 58,
    "daab-breadcrumbs.js": 39,
    "prominent-figures-catalog-data.js": 4,
    "prominent-figures-catalog-data-en.js": 4,
    "prominent-figures-catalog.js": 19,
    "daab-shell.js": 13,
    "daab-search.js": 13,
    "daab-mobile.js": 6,
    "daab-perf.js": 1,
    "daab-sticky-chrome.js": 3,
    "daab-back-to-top.js": 3,
    "daab-work-done-report.js": 1,
    "daab-page-subtitle.js": 2,
    "daab-sidebar-timeline.js": 3,
    "daab-forum-2026-toc.js": 2,
    "daab-photos-gallery.js": 4,
    "daab-profile-tts.js": 3,
    "daab-profile-deep-link.js": 2,
    "daab-membership-application.js": 9,
    "daab-application-config.js": 1,
    "daab-country-codes.js": 1,
    "daab-membership-flyer-email.js": 28,
    "daab-collation.js": 1,
    "daab-table-resize.js": 3,
    "daab-scientists-toolbar-mobile.js": 4,
    "daab-profiles-sticky.js": 4,
    "scientists-cv-filters.js": 3,
    "scientists-list-preview.js": 7,
    "scientists-catalog-data.js": 2,
    "scientists-catalog-data-en.js": 2,
    "daab-sponsors-page.js": 3,
}

STYLE_VERSIONS = {
    "daab-common.css": 69,
    "daab-perf.css": 1,
    "daab-mobile.css": 13,
    "daab-sticky-chrome.css": 1,
    "daab-lang.css": 13,
    "daab-nav-mega.css": 69,
    "daab-search.css": 6,
    "daab-back-to-top.css": 2,
    "daab-hero-summary.css": 13,
    "daab-forum-content.css": 46,
    "daab-forum-logistics.css": 1,
    "daab-forum-sessions.css": 13,
    "daab-video-gallery.css": 8,
    "daab-hub-cards.css": 32,
    "daab-donate-page.css": 2,
    "daab-sponsors-page.css": 7,
    "daab-forum-sponsorship-page.css": 18,
    "daab-presentations-toc.css": 10,
    "daab-speech-photos.css": 3,
    "daab-impressions-photos.css": 2,
    "daab-activities-layout.css": 23,
    "daab-activities-page.css": 11,
    "daab-executive-board.css": 6,
    "daab-membership-page.css": 13,
    "daab-membership-value.css": 17,
    "daab-scientists-profiles-page.css": 13,
    "daab-encyclopedia-page.css": 14,
    "daab-prominent-figure-profile.css": 3,
    "daab-content-hero.css": 7,
    "daab-charter-page.css": 10,
    "daab-work-done-report.css": 2,
    "daab-foundation-page.css": 6,
    "daab-mission-page.css": 5,
    "daab-membership-application.css": 17,
    "daab-scientists-list-page.css": 10,
    "scientists-list-catalog.js": 8,
    "daab-photos-gallery.css": 8,
    "daab-forum-book.css": 5,
    "daab-membership-flyer.css": 30,
    "daab-forum-2026-page.css": 12,
    "daab-sidebar-widget.css": 6,
    "daab-table-resize.css": 2,
    "scientists-catalog-toolbar.css": 5,
    "scientists-list-preview.css": 3,
    "scientists-profiles-sticky.css": 2,
    "scientists-profile-tts.css": 6,
    "scientists-profile-deep-link.css": 4,
    "scientists-profile-qr.css": 18,
}

DEPLOY_HTML_DIRS = (ROOT / "az", ROOT / "en")

SECTION_NAV_RE = re.compile(
    r'\n<nav class="daab-section-nav"[^>]*>.*?</nav>',
    re.DOTALL,
)
SECTION_NAV_SCRIPT_RE = re.compile(
    r'\n<script[^>]*daab-section-nav\.js[^>]*>\s*</script>',
    re.IGNORECASE,
)
FORUM_SECTION_NAV_CSS_RE = re.compile(
    r'\n<link[^>]*daab-forum-section-nav\.css[^>]*>',
    re.IGNORECASE,
)


def strip_legacy_section_nav_assets(html: str) -> str:
    """Remove unused section-nav JS/CSS (primary nav mega-menu replaced in-page pills)."""
    html = SECTION_NAV_SCRIPT_RE.sub("", html)
    html = FORUM_SECTION_NAV_CSS_RE.sub("", html)
    return html


def strip_duplicate_section_nav(html: str) -> str:
    """Remove static in-page section nav; primary mega-menu already lists siblings."""
    return SECTION_NAV_RE.sub("", html)


def iter_deploy_html() -> list[Path]:
    out: list[Path] = []
    for gateway_name in ("index.html", "404.html"):
        gateway = ROOT / gateway_name
        if gateway.is_file():
            out.append(gateway)
    for base in DEPLOY_HTML_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if not path.is_file():
                continue
            out.append(path)
    return sorted(out)


def fix_foundation_images(html: str) -> str:
    if "foundation.html" not in html and "Şuşa qurultayı" not in html and "DAAD, İstanbul" not in html:
        return html
    html = html.replace("../images/Şuşa", "../images/activities/Şuşa")
    html = html.replace("../images/DAAD,", "../images/activities/DAAD,")
    return html


def bump_asset_versions(html: str) -> str:
    for name, ver in {**SCRIPT_VERSIONS, **STYLE_VERSIONS}.items():
        html = re.sub(
            re.escape(name) + r"\?v=\d+",
            f"{name}?v={ver}",
            html,
        )
    return html


def process_file(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    original = text
    if path.name == "foundation.html":
        text = fix_foundation_images(text)
    text = strip_duplicate_section_nav(text)
    text = strip_legacy_section_nav_assets(text)
    text = bump_asset_versions(text)
    if text == original:
        return None
    path.write_text(text, encoding="utf-8", newline="\n")
    return str(path.relative_to(ROOT))


def main() -> None:
    updated: list[str] = []
    for path in iter_deploy_html():
        rel = process_file(path)
        if rel:
            updated.append(rel)
    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  - {line}")
    if not updated:
        print("  (no changes needed)")


if __name__ == "__main__":
    main()
