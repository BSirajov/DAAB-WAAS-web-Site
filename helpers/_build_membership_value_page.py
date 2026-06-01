#!/usr/bin/env python3
"""Build az|en/membership_value.html from application/membership_value.html with DAAB shell."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

ASSET = "../"
CSS_V = "13"

LOCALES = {
    "az": {
        "src": ROOT / "az" / "application" / "membership_value.html",
        "membership": ROOT / "az" / "membership.html",
        "out": ROOT / "az" / "membership_value.html",
        "lang": "az",
        "brand": "DAAB",
        "page_id": "membership-value",
        "title": "DAAB — Üzvlük sizə nə qazandırır?",
        "description": "DAAB üzvlüyünün faydaları, əməkdaşlıq imkanları və qlobal elmi şəbəkəyə qoşulma dəyəri.",
        "skip": "Məzmuna keç",
        "nav_aria": "Əsas naviqasiya",
        "hero_h1": "DAAB mənə nə verəcək? <span>Niyə üzv olmalıyam?</span>",
        "hero_subtitle": "Üzvlüyün tanınma, əməkdaşlıq və Azərbaycan elminə xidmət baxımından verdiyi dəyəri kəşf edin",
        "panel_title": "Üzvlük şəxsi fayda ilə ictimai missiyanın kəsişməsidir",
        "panel_copy": (
            "DAAB üzvlüyü sadəcə bir təşkilata qoşulmaq deyil; bu, peşəkar nüfuzunuzu artıran, "
            "beynəlxalq əlaqələrinizi genişləndirən, akademik əməkdaşlıq imkanları yaradan və "
            "Azərbaycanın elmi-intellektual gələcəyinə mənalı töhfə verməyə imkan verən qlobal "
            "Azərbaycan elmi ekosisteminin bir hissəsinə çevrilmək deməkdir."
        ),
        "cta_btn": "Bizə qoşulun",
        "cta_href": "application.html",
    },
    "en": {
        "src": ROOT / "en" / "application" / "membership_value.html",
        "membership": ROOT / "en" / "membership.html",
        "out": ROOT / "en" / "membership_value.html",
        "lang": "en",
        "brand": "WAAS",
        "page_id": "membership-value",
        "title": "WAAS — Why become a member?",
        "description": (
            "Benefits of WAAS membership, collaboration opportunities, and the value of "
            "joining the global Azerbaijani scientific network."
        ),
        "skip": "Skip to content",
        "nav_aria": "Main navigation",
        "hero_h1": "What does WAAS offer me? <span>Why should I join?</span>",
        "hero_subtitle": "See how membership connects visibility, collaboration, and service to Azerbaijani science",
        "panel_title": "Membership connects personal benefit with public mission",
        "panel_copy": (
            "WAAS membership is not simply joining an association; it means becoming part of a "
            "global Azerbaijani scientific ecosystem that enhances your professional visibility, "
            "expands international connections, creates opportunities for academic cooperation, "
            "and enables you to contribute meaningfully to Azerbaijan’s scientific and "
            "intellectual future."
        ),
        "cta_btn": "Join us",
        "cta_href": "application.html",
    },
}


def extract_nav(html: str, nav_aria: str) -> str:
    m = re.search(
        rf'(<nav aria-label="{re.escape(nav_aria)}" class="nav-strip">.*?</nav>)',
        html,
        re.DOTALL,
    )
    return m.group(1) if m else ""


def extract_footer(html: str) -> str:
    m = re.search(r'(<footer class="footer-pro">.*?</footer>)', html, re.DOTALL)
    return m.group(1) if m else ""


def extract_main(src: str) -> str:
    start = src.find('<main id="content">')
    if start < 0:
        raise SystemExit("Could not find <main id=\"content\"> in source")
    start = src.find(">", start) + 1
    end = src.find("</main>", start)
    if end < 0:
        raise SystemExit("Could not find </main> in source")
    block = src[start:end].strip()
    replacements = [
        ('class="value"', 'class="mv-value"'),
        ('class="section"', 'class="mv-section"'),
        ('class="section-head"', 'class="mv-section-head"'),
        ('class="grid grid3"', 'class="mv-grid mv-grid-3"'),
        ('class="grid grid2"', 'class="mv-grid mv-grid-2"'),
        ('class="card"', 'class="mv-card"'),
        ('class="icon icon--flag"', 'class="mv-icon mv-icon--flag"'),
        ('class="icon"', 'class="mv-icon"'),
        ('class="clean"', 'class="mv-clean"'),
        ('class="qa"', 'class="mv-qa"'),
        ('class="qa-item"', 'class="mv-qa-item"'),
        ('class="cta"', 'class="mv-cta"'),
        ('class="stats"', 'class="mv-stats"'),
        ('class="stat"', 'class="mv-stat"'),
        ('class="value-grid"', 'class="mv-value-grid"'),
        ('class="mini"', 'class="mv-mini"'),
    ]
    for old, new in replacements:
        block = block.replace(old, new)
    block = re.sub(
        r'<a class="btn" href="mailto:[^"]+">[^<]+</a>',
        '<a class="btn" href="__CTA_HREF__">__CTA_TEXT__</a>',
        block,
        count=1,
    )
    return block


def shell_head(cfg: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="{cfg["lang"]}" data-daab-lang="{cfg["lang"]}" data-daab-asset-root="{ASSET}" data-daab-page-id="{cfg["page_id"]}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{cfg["title"]}</title>
<meta name="description" content="{cfg["description"]}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=26" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=7" rel="stylesheet"/>
<link href="{ASSET}css/daab-membership-value.css?v={CSS_V}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=16" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=14" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v=6" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=7" defer></script>
<script src="{ASSET}js/daab-shell.js?v=11" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v=2" defer></script>
<script src="{ASSET}js/daab-search.js?v=4" defer></script>
</head>
"""


def hero_block(cfg: dict) -> str:
    return f"""<body class="membership-value-page membership-page">
<a class="skip" href="#content">{cfg["skip"]}</a>
NAV_PLACEHOLDER
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1 aria-describedby="page-hero-subtitle">{cfg["hero_h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{cfg["hero_subtitle"]}</p>
</section>
<aside aria-label="{cfg["panel_title"]}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{cfg["panel_title"]}</h2>
<p class="panel-copy">{cfg["panel_copy"]}</p>
</div>
</aside>
</div>
</header>
MEMBERSHIP_SECTION_NAV
<main class="main membership-value-main" id="content">
"""

SECTION_NAV_AZ = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="Bu bölmədə" data-daab-section-nav-enhanced="1">
<p class="daab-section-nav-title">Üzvlük</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page"><span class="daab-section-nav-icon" aria-hidden="true">💡</span><span class="daab-section-nav-label">Niyə DAAB-a qoşulmalı</span></a></li>
<li><a href="application.html"><span class="daab-section-nav-icon" aria-hidden="true">📝</span><span class="daab-section-nav-label">Bizə qoşulun</span></a></li>
<li><a href="membership_flyer.html"><span class="daab-section-nav-icon" aria-hidden="true">📤</span><span class="daab-section-nav-label">Dəvət göndərin</span></a></li>
</ul>
</nav>
"""

SECTION_NAV_EN = """<nav class="daab-section-nav" id="daab-section-nav" aria-label="In this section" data-daab-section-nav-enhanced="1">
<p class="daab-section-nav-title">Membership</p>
<ul class="daab-section-nav-list">
<li><a class="active" href="membership_value.html" aria-current="page"><span class="daab-section-nav-icon" aria-hidden="true">💡</span><span class="daab-section-nav-label">Why join WAAS</span></a></li>
<li><a href="application.html"><span class="daab-section-nav-icon" aria-hidden="true">📝</span><span class="daab-section-nav-label">Join us</span></a></li>
<li><a href="membership_flyer.html"><span class="daab-section-nav-icon" aria-hidden="true">📤</span><span class="daab-section-nav-label">Send invitation</span></a></li>
</ul>
</nav>
"""


def build_locale(key: str) -> None:
    cfg = LOCALES[key]
    if not cfg["src"].is_file():
        raise SystemExit(f"Missing source: {cfg['src']}")
    membership = cfg["membership"].read_text(encoding="utf-8")
    src = cfg["src"].read_text(encoding="utf-8")
    nav = extract_nav(membership, cfg["nav_aria"])
    if not nav:
        raise SystemExit(f"Could not extract nav from {cfg['membership']}")
    footer = extract_footer(membership)
    if not footer:
        raise SystemExit(f"Could not extract footer from {cfg['membership']}")
    main = extract_main(src)
    main = main.replace("__CTA_HREF__", cfg["cta_href"]).replace("__CTA_TEXT__", cfg["cta_btn"])
    section_nav = SECTION_NAV_AZ if cfg["lang"] == "az" else SECTION_NAV_EN
    html = shell_head(cfg)
    html += (
        hero_block(cfg)
        .replace("NAV_PLACEHOLDER", nav)
        .replace("MEMBERSHIP_SECTION_NAV", section_nav)
    )
    html += main + "\n</main>\n"
    html += footer + "\n</body>\n</html>\n"
    cfg["out"].write_text(html, encoding="utf-8", newline="\n")
    print(f"Wrote {cfg['out'].relative_to(ROOT)}")


def main() -> None:
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(LOCALES.keys())
    for key in targets:
        if key not in LOCALES:
            raise SystemExit(f"Unknown locale: {key}")
        build_locale(key)


if __name__ == "__main__":
    main()
