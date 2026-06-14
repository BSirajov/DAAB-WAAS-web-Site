#!/usr/bin/env python3
"""Migrate prominent figure profiles to the shared DAAB site shell."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from _embed_static_nav import NAV_AZ, prominent_nav, prominent_nav_strip
from _paths import ROOT
from _prominent_figure_hero import transform_hero_inner

FIGURES = ROOT / "az" / "prominent_figures"
ASSET = "../../../"
CSS_V = {
    "daab-common.css": 63,
    "daab-mobile.css": 12,
    "daab-sticky-chrome.css": 1,
    "daab-search.css": 4,
    "daab-back-to-top.css": 2,
    "daab-lang.css": 12,
    "daab-nav-mega.css": 27,
    "daab-hero-summary.css": 11,
    "daab-prominent-figure-profile.css": 2,
}
JS_V = {
    "daab-mobile.js": 6,
    "daab-sticky-chrome.js": 1,
    "daab-back-to-top.js": 3,
    "daab-i18n.js": 18,
    "daab-lang-position.js": 7,
    "daab-design-tokens.js": 1,
    "daab-nav.js": 23,
    "daab-primary-nav.js": 25,
    "daab-breadcrumbs.js": 18,
    "daab-shell.js": 12,
    "daab-search.js": 7,
}

FOOTER = """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Əlaqə</div><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <span>+90 555 147 46 74</span></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" target="_blank" rel="noopener">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Ünvan</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><div class="footer-title">Rəhbərlik</div><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>
</footer>"""

RE_TITLE = re.compile(r"<title>([^<]+)</title>", re.I)
RE_DESC = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
RE_HERO = re.compile(r'<section class="(?:profile-hero|hero)">(.*)</section>', re.I | re.DOTALL)
RE_BODY = re.compile(r'<div class="container">(.*)<footer', re.I | re.DOTALL)
RE_NAME = re.compile(r'<h1 class="hero-name">([^<]+)</h1>', re.I)
RE_PLACEHOLDER = re.compile(r"Profil hazırlanır", re.I)


def css_links() -> str:
    lines = []
    for name, ver in CSS_V.items():
        lines.append(f'<link href="{ASSET}css/{name}?v={ver}" rel="stylesheet"/>')
    return "\n".join(lines)


def js_scripts() -> str:
    lines = []
    for name, ver in JS_V.items():
        lines.append(f'<script src="{ASSET}js/{name}?v={ver}" defer></script>')
    return "\n".join(lines)


def extract(text: str) -> dict:
    title_m = RE_TITLE.search(text)
    desc_m = RE_DESC.search(text)
    hero_m = RE_HERO.search(text)
    body_m = RE_BODY.search(text)
    name_m = RE_NAME.search(text)
    placeholder = bool(RE_PLACEHOLDER.search(text))
    body = body_m.group(1).strip() if body_m else ""
    if placeholder and not body:
        stub_m = re.search(r'<main class="container">(.*)</main>', text, re.I | re.DOTALL)
        if stub_m:
            body = stub_m.group(1).strip()
    return {
        "title": html.unescape(title_m.group(1).strip()) if title_m else "DAAB",
        "description": html.unescape(desc_m.group(1).strip()) if desc_m else "",
        "hero": hero_m.group(1).strip() if hero_m else "",
        "body": body,
        "name": html.unescape(name_m.group(1).strip()) if name_m else "",
        "placeholder": placeholder,
    }


def render_placeholder(data: dict, nav_menu: str) -> str:
    main = data["body"] or (
        '<div class="pf-placeholder-card"><p>Hazırda qədim və orta əsrlərdən başlayaraq '
        "birinci profil qrupu tam səhifə formatında təqdim edilmişdir.</p>"
        '<a class="btn" href="../../encyclopedia.html">Kataloqa qayıt</a></div>'
    )
    return render_page(
        data,
        nav_menu,
        hero=transform_hero_inner(
            '<section class="pf-placeholder-hero"><h1>Profil hazırlanır</h1>'
            "<p>Bu şəxsiyyət haqqında material mərhələli şəkildə hazırlanacaq "
            "və mənbələrlə birlikdə ayrıca profil səhifəsinə əlavə ediləcək.</p></section>"
        ),
        main=f'<main class="pf-main" id="content">{main}</main>',
    )


def render_page(data: dict, nav_menu: str, *, hero: str, main: str) -> str:
    profile_name = html.escape(data["name"], quote=True)
    title = html.escape(data["title"], quote=True)
    desc = html.escape(data["description"], quote=True)
    nav = prominent_nav_strip(nav_menu)
    return f"""<!DOCTYPE html>
<html lang="az" data-daab-lang="az" data-daab-asset-root="{ASSET}" data-daab-page-id="prominent-figure" data-daab-profile-name="{profile_name}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
{css_links()}
{js_scripts()}
</head>
<body class="daab-prominent-figure-page">
<a class="skip" href="#content">Məzmuna keç</a>
{nav}
{hero}
{main}
{FOOTER}
</body>
</html>
"""


def render_full(data: dict, nav_menu: str) -> str:
    main = f'<main class="pf-main" id="content">{data["body"]}</main>'
    return render_page(data, nav_menu, hero=transform_hero_inner(data["hero"]), main=main)


def migrate_file(path: Path, nav_menu: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if "pf-profile-hero" in text and "daab-hero-summary.css" in text:
        return False
    data = extract(text)
    if data["placeholder"]:
        out = render_placeholder(data, nav_menu)
    elif not data["hero"] and not data["body"]:
        print(f"skip empty: {path.relative_to(ROOT)}", file=sys.stderr)
        return False
    else:
        out = render_full(data, nav_menu)
    path.write_text(out, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    nav_menu = prominent_nav(NAV_AZ)
    n = 0
    for group in ("azturk", "world"):
        folder = FIGURES / group
        for path in sorted(folder.glob("*.html")):
            if migrate_file(path, nav_menu):
                n += 1
                print(path.relative_to(ROOT))
    print(f"Migrated {n} profile pages to DAAB shell")


if __name__ == "__main__":
    main()
