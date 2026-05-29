#!/usr/bin/env python3
"""One-shot site cleanup: foundation image paths, asset cache bumps, membership section nav."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Canonical versions from en/application.html (May 2026) — update when bumping ?v= on deploy pages.
SCRIPT_VERSIONS = {
    "daab-i18n.js": 17,
    "daab-lang-position.js": 7,
    "daab-nav.js": 18,
    "daab-primary-nav.js": 16,
    "daab-breadcrumbs.js": 12,
    "daab-section-nav.js": 10,
    "daab-shell.js": 12,
    "daab-search.js": 6,
    "daab-mobile.js": 3,
    "daab-back-to-top.js": 3,
    "daab-sidebar-timeline.js": 2,
}

STYLE_VERSIONS = {
    "daab-common.css": 37,
    "daab-mobile.css": 8,
    "daab-lang.css": 10,
    "daab-nav-mega.css": 17,
    "daab-search.css": 4,
    "daab-back-to-top.css": 2,
    "daab-hero-summary.css": 7,
    "daab-forum-content.css": 17,
    "daab-hub-cards.css": 14,
    "daab-presentations-toc.css": 7,
    "daab-activities-layout.css": 13,
    "daab-activities-page.css": 3,
    "daab-executive-board.css": 2,
    "daab-scientists-profiles-page.css": 4,
    "scientists-catalog-toolbar.css": 2,
    "scientists-profile-tts.css": 3,
    "scientists-profile-deep-link.css": 4,
    "scientists-profile-qr.css": 13,
}

DEPLOY_HTML_DIRS = (ROOT / "az", ROOT / "en")

SECTION_NAV_EN = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="In this section">
<p class="daab-section-nav-title">Membership</p>
<ul class="daab-section-nav-list">
<li><a href="membership_value.html">Why become a member</a></li>
<li><a class="active" href="membership.html" aria-current="page">Membership terms</a></li>
<li><a href="application.html">Join us</a></li>
<li><a href="membership_flyer.html">Share Flyer</a></li>
</ul>
</nav>
"""

SECTION_NAV_EN_VALUE = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="In this section">
<p class="daab-section-nav-title">Membership</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page">Why become a member</a></li>
<li><a href="membership.html">Membership terms</a></li>
<li><a href="application.html">Join us</a></li>
<li><a href="membership_flyer.html">Share Flyer</a></li>
</ul>
</nav>
"""

SECTION_NAV_AZ = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="Bu bölmədə">
<p class="daab-section-nav-title">Üzvlük</p>
<ul class="daab-section-nav-list">
<li><a href="membership_value.html">Niyə üzv olmalı</a></li>
<li><a class="active" href="membership.html" aria-current="page">Üzvlük şərtləri</a></li>
<li><a href="application.html">Bizə qoşulun</a></li>
<li><a href="membership_flyer.html">Flyer paylaş</a></li>
</ul>
</nav>
"""

SECTION_NAV_AZ_VALUE = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="Bu bölmədə">
<p class="daab-section-nav-title">Üzvlük</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page">Niyə üzv olmalı</a></li>
<li><a href="membership.html">Üzvlük şərtləri</a></li>
<li><a href="application.html">Bizə qoşulun</a></li>
<li><a href="membership_flyer.html">Flyer paylaş</a></li>
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
