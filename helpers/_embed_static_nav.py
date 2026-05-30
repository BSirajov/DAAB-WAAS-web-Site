#!/usr/bin/env python3
"""Embed static fallback nav inside #primaryNavMenu so menu is visible before JS runs."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

def _drop(items: list[tuple[str, str, str, str]]) -> str:
    parts = []
    for href, nav_id, title, desc in items:
        link = (
            f'<a class="nav-dropdown-link" role="menuitem" href="{href}" data-nav-id="{nav_id}">'
            f'<span class="nav-dropdown-link-title">{title}</span>'
        )
        if desc:
            link += f'<span class="nav-dropdown-link-desc">{desc}</span>'
        link += "</a>"
        parts.append(link)
    return "".join(parts)


NAV_AZ = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">Ana səhifə</a>'
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Fəaliyyətimiz <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("activities.html", "activities", "Yeniliklər", "Əsas fəaliyyət və yeniliklər"),
        ("forum/2024/index.html", "forum-2024", "Forum 2024", "Forum 2024 haqqında"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Alimlərimiz <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("scientists/list.html", "scientists-list", "Siyahı", "Bütün alimlərin siyahısı"),
        ("scientists/profiles.html", "scientists-profiles", "Profillər", "Alimlərin akademik profilləri"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Haqqımızda <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "Birliyin təsisi", "Yaradılma tarixi və təsis prosesi"),
        ("mission.html", "mission", "Missiya və dəyərlər", "Missiya, vizyon və akademik dəyərlər"),
        ("executive-board.html", "executive-board", "İdarə heyəti", "İdarə heyəti və rəhbərlik"),
        ("charter.html", "charter", "Nizamnamə", "Nizamnamə və idarəetmə qaydaları"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Üzvlük <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "Niyə üzv olmalı", "Üzvlüyün faydaları və dəyər təklifi"),
        ("membership.html", "membership", "Üzvlük şərtləri", "Üzvlük qaydaları, ödəniş və müraciət məlumatları"),
        ("application.html", "membership-application", "Bizə qoşulun", "Onlayn üzvlük müraciət forması"),
        ("membership_flyer.html", "membership-flyer", "Dəvət göndərin", "Potensial üzvlər üçün çap oluna bilən flyer"),
    ])
    + "</div></div>"
)

NAV_EN = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">Home</a>'
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Activities <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("activities.html", "activities", "News", "News and updates"),
        ("forum/2024/index.html", "forum-2024", "Forum 2024", "Explore Forum 2024"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Scientists <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("scientists/list.html", "scientists-list", "Directory", "Directory of all scientists"),
        ("scientists/profiles.html", "scientists-profiles", "Profiles", "Academic profiles of scientists"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'About us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "Foundation", "History and founding process"),
        ("mission.html", "mission", "Mission &amp; values", "Mission, vision and academic values"),
        ("executive-board.html", "executive-board", "Executive board", "Leadership and governance structure"),
        ("charter.html", "charter", "Charter", "Charter and governance rules"),
    ])
    + "</div></div>"
    '<div class="nav-dropdown" data-nav-dropdown>'
    '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    'Membership <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "Why become a member", "Benefits and value of WAAS membership"),
        ("membership.html", "membership", "Membership terms", "Membership rules, fees and application information"),
        ("application.html", "membership-application", "Join us", "Online membership application form"),
        ("membership_flyer.html", "membership-flyer", "Send invite", "Printable flyer to share with potential members"),
    ])
    + "</div></div>"
)

NAV_SCI_AZ = NAV_AZ.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace(
    'href="forum/2024/index.html"', 'href="../forum/2024/index.html"'
).replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
)

FORUM_PREFIX_REPLACES = [
    ('href="index.html"', 'href="../../index.html"'),
    ('href="activities.html"', 'href="../../activities.html"'),
    ('href="forum/2024/index.html"', 'href="index.html"'),
    ('href="scientists/', 'href="../../scientists/'),
    ('href="foundation.html"', 'href="../../foundation.html"'),
    ('href="mission.html"', 'href="../../mission.html"'),
    ('href="executive-board.html"', 'href="../../executive-board.html"'),
    ('href="charter.html"', 'href="../../charter.html"'),
    ('href="membership.html"', 'href="../../membership.html"'),
    ('href="membership_value.html"', 'href="../../membership_value.html"'),
    ('href="application.html"', 'href="../../application.html"'),
    ('href="membership_flyer.html"', 'href="../../membership_flyer.html"'),
]


def forum_nav(nav: str) -> str:
    for old, new in FORUM_PREFIX_REPLACES:
        nav = nav.replace(old, new)
    return nav


def forum_nav_strip(lang: str = "az", *, active_nav_id: str | None = None) -> str:
    """Full nav-strip HTML for pages under az|en/forum/2024/ (three levels below locale root)."""
    asset = "../../../"
    menu = forum_nav(NAV_EN if lang == "en" else NAV_AZ)
    if active_nav_id:
        menu = menu.replace(
            f'data-nav-id="{active_nav_id}"',
            f'data-nav-id="{active_nav_id}" class="active" aria-current="page"',
            1,
        )
    if lang == "en":
        return (
            f'<nav aria-label="Main navigation" class="nav-strip"><div class="nav-inner">'
            f'<button class="mobile-menu-toggle" type="button" aria-label="Open menu" '
            f'aria-expanded="false" aria-controls="primaryNavMenu">'
            f"<span></span><span></span><span></span></button>"
            f'<div class="page-logo"><a aria-label="WAAS home" href="../../index.html">'
            f'<img src="{asset}images/daab-logo.svg" class="nav-brand-logo" alt="WAAS Logo"></a></div>'
            f'<a aria-label="WAAS home" class="nav-brand" href="../../index.html">'
            f'<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">'
            f"Azerbaijani Scientists</span></a>"
            f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu}</div>'
            f'<div class="nav-actions" role="group"></div>'
            f"</div></nav>"
        )
    return (
        f'<nav aria-label="Əsas naviqasiya" class="nav-strip"><div class="nav-inner">'
        f'<button class="mobile-menu-toggle" type="button" aria-label="Menyunu aç" '
        f'aria-expanded="false" aria-controls="primaryNavMenu">'
        f"<span></span><span></span><span></span></button>"
        f'<div class="page-logo"><a aria-label="DAAB ana səhifə" href="../../index.html">'
        f'<img src="{asset}images/daab-logo.svg" class="nav-brand-logo" alt="DAAB Logo"></a></div>'
        f'<a aria-label="DAAB ana səhifə" class="nav-brand" href="../../index.html">'
        f'<span class="nav-brand-text">Dünya Azərbaycanlı<br class="mobile-hidden-break">'
        f"Alimlər Birliyi</span></a>"
        f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu}</div>'
        f'<div class="nav-actions" role="group"></div>'
        f"</div></nav>"
    )


NAV_SCI_EN = NAV_EN.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace(
    'href="forum/2024/index.html"', 'href="../forum/2024/index.html"'
).replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
)

PLACEHOLDER_RE = re.compile(
    r'(<div class="nav-menu" id="primaryNavMenu"[^>]*>)(.*?)(</div>\s*</div>\s*</nav>)',
    re.DOTALL | re.IGNORECASE,
)


def is_live_page(path: Path) -> bool:
    """Only the bilingual pages under /az and /en are live; legacy root *_az.html
    files are sources used by the build pipeline and should not be patched."""
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith("az/") or rel.startswith("en/")


def nav_html(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/scientists/"):
        return NAV_SCI_EN
    if rel.startswith("az/scientists/"):
        return NAV_SCI_AZ
    if "forum/2024/" in rel:
        if rel.startswith("en/"):
            return forum_nav(NAV_EN)
        return forum_nav(NAV_AZ)
    if rel.startswith("en/"):
        return NAV_EN
    return NAV_AZ


def patch(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "primaryNavMenu" not in text:
        return False
    if not is_live_page(path):
        return False
    html = nav_html(path)
    new_text, _ = PLACEHOLDER_RE.subn(lambda m: m.group(1) + html + m.group(3), text, count=1)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    n = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if patch(path):
            n += 1
            print(path.relative_to(ROOT))
    print(f"Updated {n} files")


if __name__ == "__main__":
    main()
