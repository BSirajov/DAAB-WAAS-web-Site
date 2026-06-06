#!/usr/bin/env python3
"""Embed static fallback nav inside #primaryNavMenu so menu is visible before JS runs."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

def _top_link(href: str, nav_id: str, title: str) -> str:
    return f'<a class="nav-link" href="{href}" data-nav-id="{nav_id}">{title}</a>'


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


def _treasury_drop(label: str, items: list[tuple[str, str, str, str]]) -> str:
    return (
        '<div class="nav-dropdown" data-nav-dropdown>'
        + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
        + label
        + ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        + '<div class="nav-dropdown-panel" role="menu">'
        + _drop(items)
        + "</div></div>"
    )


TREASURY_AZ = _treasury_drop("Xəzinə", [
    ("encyclopedia.html", "encyclopedia", "Görkəmli şəxsiyyətlər", "Görkəmli şəxsiyyətlər kataloqu"),
    ("industrial_revolutions.html", "industrial-revolutions", "Sənaye inqilabları", "Tarixi sənaye inqilablarının izləri"),
    ("major_scientific_inventions.html", "major-scientific-inventions", "Əsas elmi ixtiralar", "Elm tarixinin mühüm ixtiraları"),
])

TREASURY_EN = _treasury_drop("Treasury", [
    ("encyclopedia.html", "encyclopedia", "Prominent Figures", "Directory of prominent figures"),
    ("industrial_revolutions.html", "industrial-revolutions", "Industrial Revolutions", "Landmarks of industrial history"),
    ("major_scientific_inventions.html", "major-scientific-inventions", "Major Scientific Inventions", "Key inventions that shaped science"),
])


NAV_AZ = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">Ana səhifə</a>'
    + _top_link("activities.html", "activities", "Fəaliyyətimiz")
    + _top_link("forum/2024/index.html", "forum-2024", "Forum 2024")
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + 'Haqqımızda <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "Birliyin təsisi", "Yaradılma tarixi və təsis prosesi"),
        ("mission.html", "mission", "Missiya və dəyərlər", "Missiya, vizyon və akademik dəyərlər"),
        ("executive-board.html", "executive-board", "İdarə heyəti", "İdarə heyəti və rəhbərlik"),
        ("charter.html", "charter", "Nizamnamə", "Nizamnamə və idarəetmə qaydaları"),
    ])
    + "</div></div>"
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + 'Üzvlük <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "Niyə DAAB-a qoşulmalı", "Üzvlüyün dəyəri və əsas faydalar"),
        ("application.html", "membership-application", "Bizə qoşulun", "Onlayn üzvlük müraciət forması"),
        ("membership_flyer.html", "membership-flyer", "Dəvət məktubu", "Potensial üzvlər üçün çap oluna bilən flyer"),
    ])
    + "</div></div>"
    '<a class="nav-link" href="sponsors.html" data-nav-id="sponsors">Bizi dəstəkləyin</a>'
    + TREASURY_AZ
)

NAV_EN = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">Home</a>'
    + _top_link("activities.html", "activities", "Activities")
    + _top_link("forum/2024/index.html", "forum-2024", "Forum 2024")
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + 'About us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "Foundation", "History and founding process"),
        ("mission.html", "mission", "Mission &amp; values", "Mission, vision and academic values"),
        ("executive-board.html", "executive-board", "Executive board", "Leadership and governance structure"),
        ("charter.html", "charter", "Charter", "Charter and governance rules"),
    ])
    + "</div></div>"
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + 'Membership <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "Why join WAAS", "Membership value, benefits, and opportunities"),
        ("application.html", "membership-application", "Join us", "Online membership application form"),
        ("membership_flyer.html", "membership-flyer", "Send invitation", "Printable flyer to share with potential members"),
    ])
    + "</div></div>"
    '<a class="nav-link" href="sponsors.html" data-nav-id="sponsors">Support us</a>'
    + TREASURY_EN
)

NAV_SCI_AZ = NAV_AZ.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace('href="forum/2024/', 'href="../forum/2024/').replace('href="encyclopedia.html"', 'href="../encyclopedia.html"').replace('href="industrial_revolutions.html"', 'href="../industrial_revolutions.html"').replace('href="major_scientific_inventions.html"', 'href="../major_scientific_inventions.html"').replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
).replace(
    'href="sponsors.html"', 'href="../sponsors.html"'
)

PROMINENT_PREFIX_REPLACES = [
    ('href="index.html"', 'href="../../index.html"'),
    ('href="activities.html"', 'href="../../activities.html"'),
    ('href="forum/2024/', 'href="../../forum/2024/'),
    ('href="encyclopedia.html"', 'href="../../encyclopedia.html"'),
    ('href="industrial_revolutions.html"', 'href="../../industrial_revolutions.html"'),
    ('href="major_scientific_inventions.html"', 'href="../../major_scientific_inventions.html"'),
    ('href="foundation.html"', 'href="../../foundation.html"'),
    ('href="mission.html"', 'href="../../mission.html"'),
    ('href="executive-board.html"', 'href="../../executive-board.html"'),
    ('href="charter.html"', 'href="../../charter.html"'),
    ('href="membership_value.html"', 'href="../../membership_value.html"'),
    ('href="application.html"', 'href="../../application.html"'),
    ('href="membership_flyer.html"', 'href="../../membership_flyer.html"'),
    ('href="sponsors.html"', 'href="../../sponsors.html"'),
]


def prominent_nav(nav: str) -> str:
    for old, new in PROMINENT_PREFIX_REPLACES:
        nav = nav.replace(old, new)
    return nav


def prominent_nav_strip_en(menu_html: str) -> str:
    """Full nav-strip for pages under en/prominent_figures/{group}/."""
    return (
        '<nav aria-label="Main navigation" class="nav-strip"><div class="nav-inner">'
        '<button class="mobile-menu-toggle" type="button" aria-label="Open menu" '
        'aria-expanded="false" aria-controls="primaryNavMenu">'
        "<span></span><span></span><span></span></button>"
        '<div class="page-logo"><a title="Home page" aria-label="WAAS home" href="../../index.html">'
        '<img src="../../../images/daab-logo.svg" class="nav-brand-logo" alt="WAAS Logo"></a></div>'
        '<a aria-label="WAAS home" class="nav-brand" href="../../index.html">'
        '<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">'
        "Azerbaijani Scientists</span></a>"
        f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu_html}</div>'
        '<div class="nav-actions" role="group"></div>'
        "</div></nav>"
    )


def prominent_nav_strip(menu_html: str) -> str:
    """Full nav-strip for pages under az/prominent_figures/{group}/."""
    return (
        '<nav aria-label="Əsas naviqasiya" class="nav-strip"><div class="nav-inner">'
        '<button class="mobile-menu-toggle" type="button" aria-label="Menyunu aç" '
        'aria-expanded="false" aria-controls="primaryNavMenu">'
        "<span></span><span></span><span></span></button>"
        '<div class="page-logo"><a title="Ana səhifə" aria-label="DAAB ana səhifə" href="../../index.html">'
        '<img src="../../../images/daab-logo.svg" class="nav-brand-logo" alt="DAAB Logo"></a></div>'
        '<a aria-label="DAAB ana səhifə" class="nav-brand" href="../../index.html">'
        '<span class="nav-brand-text">Dünya Azərbaycanlı<br class="mobile-hidden-break">'
        "Alimlər Birliyi</span></a>"
        f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu_html}</div>'
        '<div class="nav-actions" role="group"></div>'
        "</div></nav>"
    )


FORUM_PREFIX_REPLACES = [
    ('href="index.html"', 'href="../../index.html"'),
    ('href="activities.html"', 'href="../../activities.html"'),
    ('href="forum/2024/', 'href="'),
    ('href="encyclopedia.html"', 'href="../../encyclopedia.html"'),
    ('href="industrial_revolutions.html"', 'href="../../industrial_revolutions.html"'),
    ('href="major_scientific_inventions.html"', 'href="../../major_scientific_inventions.html"'),
    ('href="scientists/', 'href="../../scientists/'),
    ('href="foundation.html"', 'href="../../foundation.html"'),
    ('href="mission.html"', 'href="../../mission.html"'),
    ('href="executive-board.html"', 'href="../../executive-board.html"'),
    ('href="charter.html"', 'href="../../charter.html"'),
    ('href="membership.html"', 'href="../../membership.html"'),
    ('href="membership_value.html"', 'href="../../membership_value.html"'),
    ('href="application.html"', 'href="../../application.html"'),
    ('href="membership_flyer.html"', 'href="../../membership_flyer.html"'),
    ('href="sponsors.html"', 'href="../../sponsors.html"'),
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
            f'<div class="page-logo"><a aria-label="WAAS home" title="Home page" href="../../index.html">'
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
        f'<div class="page-logo"><a aria-label="DAAB ana səhifə" title="Ana səhifə" href="../../index.html">'
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
).replace('href="forum/2024/', 'href="../forum/2024/').replace('href="encyclopedia.html"', 'href="../encyclopedia.html"').replace('href="industrial_revolutions.html"', 'href="../industrial_revolutions.html"').replace('href="major_scientific_inventions.html"', 'href="../major_scientific_inventions.html"').replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
).replace(
    'href="sponsors.html"', 'href="../sponsors.html"'
)

PLACEHOLDER_RE = re.compile(
    r'(<div[^>]*class="nav-menu"[^>]*id="primaryNavMenu"[^>]*>)(.*?)(</div>\s*</div>\s*</nav>)',
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
    if "/prominent_figures/" in rel and rel.startswith("az/"):
        return prominent_nav(NAV_AZ)
    if "/prominent_figures/" in rel and rel.startswith("en/"):
        return prominent_nav(NAV_EN)
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
