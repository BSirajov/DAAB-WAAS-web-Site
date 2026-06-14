#!/usr/bin/env python3
"""Create AZ/EN placeholder pages for Treasury submenu items (non-catalog sections)."""
from __future__ import annotations

from _paths import ROOT

FOOTER_AZ = """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Əlaqə</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" target="_blank" rel="noopener">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Ünvan</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p></div>
<div class="footer-col"><div class="footer-title">Rəhbərlik</div><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB / WAAS — All Rights Reserved</div>
</footer>"""

FOOTER_EN = """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Contact</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" target="_blank" rel="noopener">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Address</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p></div>
<div class="footer-col"><div class="footer-title">Leadership</div><p class="footer-leader"><strong>Prof. Dr. Masud Afandiyev</strong><br/>Chair of the WAAS Executive Board</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 WAAS — All rights reserved</div>
</footer>"""

PAGES = [
    {
        "file": "industrial_revolutions.html",
        "page_id": "industrial-revolutions",
        "az": {
            "title": "DAAB — Sənaye inqilabları",
            "description": "Xəzinə: tarixi sənaye inqilabları haqqında materiallar hazırlanır.",
            "h1": "Sənaye inqilabları",
            "subtitle": "Tarixi sənaye inqilablarının izləri",
            "body": "Bu bölmə hazırlanır. Tezliklə sənaye inqilablarının tarixi konteksti və elmə təsirini əks etdirən materiallar burada dərc olunacaq.",
        },
        "en": {
            "title": "WAAS — Industrial Revolutions",
            "description": "Treasury: materials on industrial revolutions are being prepared.",
            "h1": "Industrial Revolutions",
            "subtitle": "Landmarks of industrial history",
            "body": "This section is being prepared. Materials on the historical context of industrial revolutions and their impact on science will be published here soon.",
        },
    },
    {
        "file": "major_scientific_inventions.html",
        "page_id": "major-scientific-inventions",
        "az": {
            "title": "DAAB — Əsas elmi ixtiralar",
            "description": "Xəzinə: elm tarixinin mühüm ixtiraları haqqında materiallar hazırlanır.",
            "h1": "Əsas elmi ixtiralar",
            "subtitle": "Elm tarixinin mühüm ixtiraları",
            "body": "Bu bölmə hazırlanır. Tezliklə elm və texnologiyanın inkişafına yön vermiş əsas ixtiralar haqqında materiallar burada dərc olunacaq.",
        },
        "en": {
            "title": "WAAS — Major Scientific Inventions",
            "description": "Treasury: materials on major scientific inventions are being prepared.",
            "h1": "Major Scientific Inventions",
            "subtitle": "Key inventions that shaped science",
            "body": "This section is being prepared. Materials on major inventions that shaped science and technology will be published here soon.",
        },
    },
]


def render(lang: str, spec: dict, copy: dict) -> str:
    brand_line = (
        "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi"
        if lang == "az"
        else "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists"
    )
    nav_label = "Əsas naviqasiya" if lang == "az" else "Main navigation"
    home_label = "DAAB ana səhifə" if lang == "az" else "WAAS home"
    home_title = "Ana səhifə" if lang == "az" else "Home page"
    skip = "Məzmuna keç" if lang == "az" else "Skip to content"
    menu_open = "Menyunu aç" if lang == "az" else "Open menu"
    footer = FOOTER_AZ if lang == "az" else FOOTER_EN
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="../" data-daab-page-id="{spec["page_id"]}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{copy["title"]}</title>
<meta name="description" content="{copy["description"]}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/daab-common.css?v=64" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=13" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=1" rel="stylesheet"/>
<link href="../css/daab-search.css?v=4" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=12" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=28" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=11" rel="stylesheet"/>
<link href="../css/daab-content-hero.css?v=4" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-sticky-chrome.js?v=1" defer></script>
<script src="../js/daab-back-to-top.js?v=3" defer></script>
<script src="../js/daab-i18n.js?v=20" defer></script>
<script src="../js/daab-lang-position.js?v=7" defer></script>
<script src="../js/daab-design-tokens.js?v=1" defer></script>
<script src="../js/daab-nav.js?v=23" defer></script>
<script src="../js/daab-primary-nav.js?v=28" defer></script>
<script src="../js/daab-breadcrumbs.js?v=20" defer></script>
<script src="../js/daab-shell.js?v=12" defer></script>
<script src="../js/daab-page-subtitle.js?v=2" defer></script>
<script src="../js/daab-search.js?v=7" defer></script>
</head>
<body>
<a class="skip" href="#content">{skip}</a>
<nav aria-label="{nav_label}" class="nav-strip"><div class="nav-inner"><button class="mobile-menu-toggle" type="button" aria-label="{menu_open}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button><div class="page-logo"><a title="{home_title}" aria-label="{home_label}" href="index.html"><img src="../images/daab-logo.svg" class="nav-brand-logo" alt="DAAB Logo"></a></div><a aria-label="{home_label}" class="nav-brand" href="index.html"><span class="nav-brand-text">{brand_line}</span></a><div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div><div class="nav-actions" role="group"></div></div></nav>
<header class="hero page-hero"><div class="hero-wrap shell"><section><h1 aria-describedby="page-hero-subtitle">{copy["h1"]}</h1><p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{copy["subtitle"]}</p></section></div></header>
<main class="main" id="content"><section class="intro-card glass-card treasury-coming-soon" role="status"><p class="treasury-coming-soon__badge">{"Tezliklə" if lang == "az" else "Coming soon"}</p><p>{copy["body"]}</p><p class="treasury-coming-soon__links"><a class="btn btn-secondary" href="encyclopedia.html">{"Görkəmli şəxsiyyətlər kataloqu" if lang == "az" else "Prominent Figures catalog"}</a></p></section></main>
{footer}
</body>
</html>
"""


def main() -> None:
    for spec in PAGES:
        for lang in ("az", "en"):
            path = ROOT / lang / spec["file"]
            path.write_text(render(lang, spec, spec[lang]), encoding="utf-8", newline="\n")
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
