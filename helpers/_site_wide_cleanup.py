#!/usr/bin/env python3
"""One-shot site cleanup: foundation image paths, asset cache bumps, membership section nav."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Canonical ?v= for deploy HTML — keep in sync with latest page builds (May 2026).
SCRIPT_VERSIONS = {
    "daab-i18n.js": 18,
    "daab-lang-position.js": 7,
    "daab-design-tokens.js": 1,
    "daab-nav.js": 23,
    "daab-primary-nav.js": 17,
    "daab-breadcrumbs.js": 14,
    "daab-section-nav.js": 18,
    "daab-shell.js": 12,
    "daab-search.js": 7,
    "daab-mobile.js": 6,
    "daab-sticky-chrome.js": 1,
    "daab-back-to-top.js": 3,
    "daab-page-subtitle.js": 2,
    "daab-sidebar-timeline.js": 2,
    "daab-photos-gallery.js": 3,
    "daab-profile-tts.js": 3,
    "daab-profile-deep-link.js": 2,
    "daab-membership-application.js": 1,
    "daab-membership-flyer-email.js": 27,
    "daab-collation.js": 1,
    "daab-table-resize.js": 1,
    "daab-scientists-toolbar-mobile.js": 1,
    "daab-profiles-sticky.js": 1,
    "scientists-cv-filters.js": 2,
    "scientists-list-preview.js": 2,
    "scientists-catalog-data.js": 2,
    "scientists-catalog-data-en.js": 2,
}

STYLE_VERSIONS = {
    "daab-common.css": 55,
    "daab-mobile.css": 12,
    "daab-sticky-chrome.css": 1,
    "daab-lang.css": 12,
    "daab-nav-mega.css": 25,
    "daab-search.css": 4,
    "daab-back-to-top.css": 2,
    "daab-hero-summary.css": 11,
    "daab-forum-content.css": 29,
    "daab-forum-section-nav.css": 8,
    "daab-video-gallery.css": 8,
    "daab-hub-cards.css": 26,
    "daab-presentations-toc.css": 10,
    "daab-speech-photos.css": 3,
    "daab-impressions-photos.css": 2,
    "daab-activities-layout.css": 14,
    "daab-activities-page.css": 6,
    "daab-executive-board.css": 6,
    "daab-membership-page.css": 8,
    "daab-membership-value.css": 14,
    "daab-scientists-profiles-page.css": 13,
    "daab-content-hero.css": 4,
    "daab-charter-page.css": 5,
    "daab-foundation-page.css": 4,
    "daab-mission-page.css": 4,
    "daab-membership-application.css": 5,
    "daab-application-membership-value-embed.css": 2,
    "daab-application-embed-az.css": 2,
    "daab-application-embed-en.css": 2,
    "daab-scientists-list-page.css": 5,
    "daab-photos-gallery.css": 8,
    "daab-forum-book.css": 5,
    "daab-membership-flyer.css": 26,
    "daab-sidebar-widget.css": 4,
    "daab-table-resize.css": 2,
    "scientists-catalog-toolbar.css": 2,
    "scientists-list-preview.css": 2,
    "scientists-profiles-sticky.css": 2,
    "scientists-profile-tts.css": 5,
    "scientists-profile-deep-link.css": 4,
    "scientists-profile-qr.css": 18,
}

DEPLOY_HTML_DIRS = (ROOT / "az", ROOT / "en")

SECTION_NAV_EN = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="In this section">
<p class="daab-section-nav-title">Membership</p>
<ul class="daab-section-nav-list">
<li><a href="membership_value.html">Why become a member</a></li>
<li><a class="active" href="membership.html" aria-current="page">Membership terms</a></li>
<li><a href="application.html">Join us</a></li>
<li><a href="membership_flyer.html">Send invite</a></li>
</ul>
</nav>
"""

SECTION_NAV_EN_VALUE = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="In this section">
<p class="daab-section-nav-title">Membership</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page">Why become a member</a></li>
<li><a href="membership.html">Membership terms</a></li>
<li><a href="application.html">Join us</a></li>
<li><a href="membership_flyer.html">Send invite</a></li>
</ul>
</nav>
"""

SECTION_NAV_AZ = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="Bu bölmədə">
<p class="daab-section-nav-title">Üzvlük</p>
<ul class="daab-section-nav-list">
<li><a href="membership_value.html">Niyə üzv olmalı</a></li>
<li><a class="active" href="membership.html" aria-current="page">Üzvlük şərtləri</a></li>
<li><a href="application.html">Bizə qoşulun</a></li>
<li><a href="membership_flyer.html">Dəvət göndərin</a></li>
</ul>
</nav>
"""

SECTION_NAV_AZ_VALUE = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="Bu bölmədə">
<p class="daab-section-nav-title">Üzvlük</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page">Niyə üzv olmalı</a></li>
<li><a href="membership.html">Üzvlük şərtləri</a></li>
<li><a href="application.html">Bizə qoşulun</a></li>
<li><a href="membership_flyer.html">Dəvət göndərin</a></li>
</ul>
</nav>
"""


def iter_deploy_html() -> list[Path]:
    out: list[Path] = []
    for base in DEPLOY_HTML_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if not path.is_file():
                continue
            # Skip prototype sources: az/application/foo.html, en/application/foo.html
            if path.parent.name == "application" and path.parent.parent.name in ("az", "en"):
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


def inject_membership_section_nav(path: Path, html: str) -> str:
    if "membership-value-page" not in html:
        return html
    if 'class="daab-section-nav"' in html:
        return html
    marker = "</header>\n<main"
    if marker not in html:
        marker = "</header>\r\n<main"
    if marker not in html:
        return html
    if path.name == "membership_value.html":
        block = SECTION_NAV_AZ_VALUE if path.parts[-2] == "az" else SECTION_NAV_EN_VALUE
    else:
        return html
    return html.replace(marker, f"</header>\n{block}<main", 1)


def process_file(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    original = text
    if path.name == "foundation.html":
        text = fix_foundation_images(text)
    text = bump_asset_versions(text)
    text = inject_membership_section_nav(path, text)
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
