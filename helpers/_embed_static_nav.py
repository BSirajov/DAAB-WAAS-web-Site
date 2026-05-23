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
    '<a class="nav-link" href="activities.html" data-nav-id="activities">Fəaliyyətimiz</a>'
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
    '<a class="nav-link" href="membership.html" data-nav-id="membership">Üzvlük</a>'
)

NAV_EN = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">Home</a>'
    '<a class="nav-link" href="activities.html" data-nav-id="activities">Activities</a>'
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
    'About <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "Foundation", "History and founding process"),
        ("mission.html", "mission", "Mission &amp; values", "Mission, vision and academic values"),
        ("executive-board.html", "executive-board", "Executive board", "Leadership and governance structure"),
        ("charter.html", "charter", "Charter", "Charter and governance rules"),
    ])
    + "</div></div>"
    '<a class="nav-link" href="membership.html" data-nav-id="membership">Membership</a>'
)

NAV_SCI_AZ = NAV_AZ.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace('href="membership.html"', 'href="../membership.html"')

NAV_SCI_EN = NAV_EN.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace('href="membership.html"', 'href="../membership.html"')

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
