#!/usr/bin/env python3
"""Bootstrap independent Knowledge Treasury / Bilik xəzinəsi site from DAAB treasury assets."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from _paths import ROOT

KT_ROOT = ROOT.parent / "knowledge-treasury"
DAAB = ROOT

CSS_FILES = [
    "daab-tokens.css",
    "daab-common.css",
    "daab-mobile.css",
    "daab-perf.css",
    "daab-sticky-chrome.css",
    "daab-back-to-top.css",
    "daab-lang.css",
    "daab-nav-mega.css",
    "daab-hero-summary.css",
    "daab-content-hero.css",
    "daab-encyclopedia-page.css",
    "daab-prominent-figure-profile.css",
    "scientists-catalog-toolbar.css",
    "daab-table-resize.css",
    "daab-site-background.css",
    "kt-home.css",
]

JS_FILES = [
    "daab-i18n.js",
    "daab-lang-position.js",
    "daab-design-tokens.js",
    "daab-nav.js",
    "daab-primary-nav.js",
    "daab-breadcrumbs.js",
    "daab-shell.js",
    "daab-mobile.js",
    "daab-perf.js",
    "daab-sticky-chrome.js",
    "daab-back-to-top.js",
    "daab-page-subtitle.js",
    "daab-collation.js",
    "daab-scientists-toolbar-mobile.js",
    "daab-table-resize.js",
    "prominent-figures-catalog.js",
    "prominent-figures-catalog-data.js",
    "prominent-figures-catalog-data-en.js",
]

LOCALE_PAGES = [
    "encyclopedia.html",
    "industrial_revolutions.html",
    "major_scientific_inventions.html",
]

HELPER_FILES = [
    "_paths.py",
    "_build_prominent_figures_catalog.py",
    "_build_en_prominent_figures.py",
    "_create_treasury_placeholder_pages.py",
    "_check_catalog_links.py",
]

HELPER_DATA = [
    "prominent_figure_enrichment_en.json",
    "prominent_figure_enrichment_azturk.json",
]

SITE_DOMAIN = "https://bilik-xezinesi.az"


def count_catalog_entries() -> int:
    text = (DAAB / "js" / "prominent-figures-catalog-data.js").read_text(encoding="utf-8")
    return len(re.findall(r'"id"\s*:', text))


def adapt_html(html: str, lang: str) -> str:
    if lang == "az":
        pairs = [
            (
                "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi",
                "Bilik<br class=\"mobile-hidden-break\">xəzinəsi",
            ),
            ("DAAB ana səhifə", "Bilik xəzinəsi ana səhifə"),
            ("DAAB Logo", "Bilik xəzinəsi loqosu"),
            ("DAAB — ", "Bilik xəzinəsi — "),
            ("DAAB/WAAS", "Bilik xəzinəsi"),
            ("Dünya Azərbaycanlı Alimlər Birliyi", "Bilik xəzinəsi"),
            ("© 2026 DAAB / WAAS", "© 2026 Bilik xəzinəsi"),
            ("Xəzinə kataloqu", "Bilik xəzinəsi kataloqu"),
            ("Xəzinə:", "Bilik xəzinəsi:"),
            ("Xəzinə ", "Bilik xəzinəsi "),
            ("aria-label=\"Xəzinə", "aria-label=\"Bilik xəzinəsi"),
        ]
    else:
        pairs = [
            (
                "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists",
                "Knowledge<br class=\"mobile-hidden-break\">Treasury",
            ),
            ("WAAS home", "Knowledge Treasury home"),
            ("WAAS Logo", "Knowledge Treasury logo"),
            ("WAAS — ", "Knowledge Treasury — "),
            ("WAAS/WAAS", "Knowledge Treasury"),
            ("World Association of Azerbaijani Scientists", "Knowledge Treasury"),
            ("© 2026 WAAS", "© 2026 Knowledge Treasury"),
            ("Treasury:", "Knowledge Treasury:"),
            ("Treasury ", "Knowledge Treasury "),
            ('aria-label="About the treasury catalog"', 'aria-label="About the Knowledge Treasury catalog"'),
            ("Treasury of science", "Knowledge Treasury of science"),
        ]
    pairs += [
        ("../images/daab-logo.svg", "../images/kt-logo.svg"),
        ("../../images/daab-logo.svg", "../../images/kt-logo.svg"),
        ("../../../images/daab-logo.svg", "../../../images/kt-logo.svg"),
        ("https://daab-waas.com", SITE_DOMAIN),
        ("daab-search.js", ""),
        ("daab-search.css", ""),
    ]
    for old, new in pairs:
        html = html.replace(old, new)
    html = html.replace("Bilik xəzinəsi — Bilik xəzinəsi", "Bilik xəzinəsi —")
    html = html.replace("Knowledge Treasury — Knowledge Treasury", "Knowledge Treasury —")
    html = re.sub(r'<script[^>]*daab-search\.js[^>]*></script>\s*', "", html)
    html = re.sub(r'<link[^>]*daab-search\.css[^>]*>\s*', "", html)
    return html


def write_kt_logo() -> None:
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Knowledge Treasury">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#117fc8"/>
      <stop offset="100%" stop-color="#005a9a"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#g)"/>
  <path fill="#fff" d="M18 18h28v6H24v24h-6V18zm10 10h18v6H28v18h-6V28z"/>
  <circle cx="46" cy="46" r="8" fill="#fff0bf" stroke="#c99b3b" stroke-width="2"/>
  <text x="46" y="50" text-anchor="middle" font-size="10" font-family="Georgia, serif" fill="#005a9a">K</text>
</svg>
"""
    (KT_ROOT / "images" / "kt-logo.svg").write_text(svg, encoding="utf-8", newline="\n")


def write_i18n(catalog_count: int) -> None:
    ui_az = {
        "home": "Ana səhifə",
        "treasury": "Bilik xəzinəsi",
        "prominentFigures": "Görkəmli şəxsiyyətlər",
        "prominentFiguresDesc": "Tarix boyu görkəmli alimlər, mütəfəkkirlər və yaradıcı simalar",
        "industrialRevolutions": "Sənaye inqilabları",
        "industrialRevolutionsDesc": "Tarixi sənaye inqilablarının izləri",
        "majorScientificInventions": "Əsas elmi ixtiralar",
        "majorScientificInventionsDesc": "Elm tarixinin mühüm ixtiraları",
        "ariaMain": "Əsas naviqasiya",
        "ariaHome": "Bilik xəzinəsi ana səhifə",
        "menuOpen": "Menyunu aç",
        "menuClose": "Menyunu bağla",
        "skip": "Məzmuna keç",
        "homeLogoTooltip": "Ana səhifə",
    }
    ui_en = {
        "home": "Home",
        "treasury": "Knowledge Treasury",
        "prominentFigures": "Prominent Figures",
        "prominentFiguresDesc": "Scientists, thinkers, and creators across history",
        "industrialRevolutions": "Industrial Revolutions",
        "industrialRevolutionsDesc": "Landmarks of industrial history",
        "majorScientificInventions": "Major Scientific Inventions",
        "majorScientificInventionsDesc": "Key inventions that shaped science",
        "ariaMain": "Main navigation",
        "ariaHome": "Knowledge Treasury home",
        "menuOpen": "Open menu",
        "menuClose": "Close menu",
        "skip": "Skip to content",
        "homeLogoTooltip": "Home page",
    }
    ui = {
        "nav": {"az": ui_az, "en": ui_en},
        "navIcons": {
            "home": "🏠",
            "treasury": "🏛️",
            "encyclopedia": "👤",
            "prominentFigures": "👤",
            "industrial-revolutions": "⚙️",
            "industrialRevolutions": "⚙️",
            "major-scientific-inventions": "💡",
            "majorScientificInventions": "💡",
        },
        "breadcrumbs": {
            "az": {
                "aria": "Səhifə yolu",
                "home": "Ana səhifə",
                "treasury": "Bilik xəzinəsi",
                "encyclopedia": "Görkəmli şəxsiyyətlər",
            },
            "en": {
                "aria": "Breadcrumb",
                "home": "Home",
                "treasury": "Knowledge Treasury",
                "encyclopedia": "Prominent Figures",
            },
        },
        "meta": {
            "siteNameAz": "Bilik xəzinəsi",
            "siteNameEn": "Knowledge Treasury",
            "catalogCount": catalog_count,
        },
    }
    nav = {
        "version": 1,
        "primary": [
            {"type": "page", "id": "home"},
            {
                "type": "group",
                "id": "treasury",
                "style": "dropdown",
                "labelKey": "treasury",
                "landingId": "encyclopedia",
                "children": [
                    {
                        "id": "encyclopedia",
                        "labelKey": "prominentFigures",
                        "descKey": "prominentFiguresDesc",
                    },
                    {
                        "id": "industrial-revolutions",
                        "labelKey": "industrialRevolutions",
                        "descKey": "industrialRevolutionsDesc",
                    },
                    {
                        "id": "major-scientific-inventions",
                        "labelKey": "majorScientificInventions",
                        "descKey": "majorScientificInventionsDesc",
                    },
                ],
            },
        ],
        "sections": {
            "treasury": {
                "landingId": "encyclopedia",
                "pages": [
                    "encyclopedia",
                    "industrial-revolutions",
                    "major-scientific-inventions",
                ],
            }
        },
    }
    routes = {
        "version": 1,
        "defaultLang": "az",
        "languages": ["az", "en"],
        "pages": [
            {
                "id": "home",
                "navId": "home",
                "az": "az/index.html",
                "en": "en/index.html",
            },
            {
                "id": "encyclopedia",
                "navId": "encyclopedia",
                "navGroup": "treasury",
                "navParent": "treasury",
                "az": "az/encyclopedia.html",
                "en": "en/encyclopedia.html",
            },
            {
                "id": "industrial-revolutions",
                "navId": "industrial-revolutions",
                "navGroup": "treasury",
                "navParent": "treasury",
                "az": "az/industrial_revolutions.html",
                "en": "en/industrial_revolutions.html",
            },
            {
                "id": "major-scientific-inventions",
                "navId": "major-scientific-inventions",
                "navGroup": "treasury",
                "navParent": "treasury",
                "az": "az/major_scientific_inventions.html",
                "en": "en/major_scientific_inventions.html",
            },
            {
                "id": "prominent-figure",
                "navId": None,
                "az": "az/encyclopedia.html",
                "en": "en/encyclopedia.html",
                "sitemap": False,
            },
        ],
    }
    i18n = KT_ROOT / "i18n"
    i18n.mkdir(parents=True, exist_ok=True)
    (i18n / "ui.json").write_text(json.dumps(ui, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (i18n / "nav.json").write_text(json.dumps(nav, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (i18n / "routes.json").write_text(json.dumps(routes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def home_shell(lang: str, catalog_count: int) -> str:
    if lang == "az":
        title = "Bilik xəzinəsi — insanlığın bilik irsi"
        desc = "Elm, texnologiya, tibb, mühəndislik və mədəniyyət sahələrində tarix boyu ən əhəmiyyətli kəşf, ixtira və innovasiyalar."
        brand = "Bilik<br class=\"mobile-hidden-break\">xəzinəsi"
        aria_home = "Bilik xəzinəsi ana səhifə"
        skip = "Məzmuna keç"
        nav_aria = "Əsas naviqasiya"
        h1 = "Bilik xəzinəsi"
        lead = (
            "Qədim dövrlərdən müasirliyə qədər insanlığın ən dəyərli kəşfləri, ixtiraları, "
            "innovasiyaları və bilik irsi — sadə, aydın və strukturlaşdırılmış formada."
        )
        cards = [
            ("👤", "Görkəmli şəxsiyyətlər", f"{catalog_count} profil", "Tarix boyu elm, mədəniyyət və cəmiyyətə yön vermiş simalar.", "encyclopedia.html"),
            ("⚙️", "Sənaye inqilabları", "Tezliklə", "Tarixi sənaye inqilabları və onların elmə təsiri.", "industrial_revolutions.html"),
            ("💡", "Əsas elmi ixtiralar", "Tezliklə", "Elm və texnologiyanın inkişafına yön vermiş mühüm ixtiralar.", "major_scientific_inventions.html"),
        ]
        fields_title = "Bilik sahələri"
        fields = ["Elm", "Texnologiya", "Tibb", "Mühəndislik", "Təhsil", "Mədəniyyət", "İnnovasiya"]
        vision_title = "Missiya"
        vision = (
            "Bilik xəzinəsi insanlığın ortaq irsinə asan çıxış yaratmaq üçün hazırlanır: "
            "hər kəs üçün başa düşülən dillə, müasir interfeyslə və iki dildə."
        )
        footer = "© 2026 Bilik xəzinəsi"
    else:
        title = "Knowledge Treasury — humanity's heritage of knowledge"
        desc = "Major discoveries, inventions, and innovations across science, technology, medicine, engineering, and culture."
        brand = "Knowledge<br class=\"mobile-hidden-break\">Treasury"
        aria_home = "Knowledge Treasury home"
        skip = "Skip to content"
        nav_aria = "Main navigation"
        h1 = "Knowledge Treasury"
        lead = (
            "From ancient times to the present — humanity's most valuable discoveries, inventions, "
            "innovations, and knowledge, presented in a simple, clear, and structured way."
        )
        cards = [
            ("👤", "Prominent Figures", f"{catalog_count} profiles", "People who shaped science, culture, and society.", "encyclopedia.html"),
            ("⚙️", "Industrial Revolutions", "Coming soon", "Historical industrial revolutions and their impact on science.", "industrial_revolutions.html"),
            ("💡", "Major Scientific Inventions", "Coming soon", "Key inventions that advanced science and technology.", "major_scientific_inventions.html"),
        ]
        fields_title = "Fields of knowledge"
        fields = ["Science", "Technology", "Medicine", "Engineering", "Education", "Culture", "Innovation"]
        vision_title = "Vision"
        vision = (
            "Knowledge Treasury is being built to open access to our shared heritage: "
            "understandable language, a modern interface, and bilingual access for every visitor."
        )
        footer = "© 2026 Knowledge Treasury"

    field_pills = "".join(f'<span class="kt-field-pill">{f}</span>' for f in fields)
    card_html = ""
    for icon, name, badge, text, href in cards:
        card_html += f"""
<article class="kt-home-card">
  <div class="kt-home-card__icon" aria-hidden="true">{icon}</div>
  <p class="kt-home-card__badge">{badge}</p>
  <h2 class="kt-home-card__title"><a href="{href}">{name}</a></h2>
  <p class="kt-home-card__text">{text}</p>
  <a class="btn btn-secondary kt-home-card__link" href="{href}">{"Kəşf et" if lang == "az" else "Explore"}</a>
</article>"""

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="../" data-daab-page-id="home" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="icon" href="../images/kt-logo.svg" type="image/svg+xml"/>
<link rel="canonical" href="{SITE_DOMAIN}/{lang}/index.html"/>
<link rel="alternate" hreflang="az" href="{SITE_DOMAIN}/az/index.html"/>
<link rel="alternate" hreflang="en" href="{SITE_DOMAIN}/en/index.html"/>
<link rel="alternate" hreflang="x-default" href="{SITE_DOMAIN}/az/index.html"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/daab-common.css?v=1" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=1" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=1" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=1" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="../css/kt-home.css?v=1" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=1" defer></script>
<script src="../js/daab-back-to-top.js?v=1" defer></script>
<script src="../js/daab-i18n.js?v=1" defer></script>
<script src="../js/daab-lang-position.js?v=1" defer></script>
<script src="../js/daab-nav.js?v=1" defer></script>
<script src="../js/daab-primary-nav.js?v=1" defer></script>
<script src="../js/daab-breadcrumbs.js?v=1" defer></script>
<script src="../js/daab-shell.js?v=1" defer></script>
</head>
<body class="kt-home-page">
<a class="skip" href="#content">{skip}</a>
<nav aria-label="{nav_aria}" class="nav-strip"><div class="nav-inner"><button class="mobile-menu-toggle" type="button" aria-label="{"Menyunu aç" if lang == "az" else "Open menu"}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button><div class="page-logo"><a title="{"Ana səhifə" if lang == "az" else "Home page"}" aria-label="{aria_home}" href="index.html"><img src="../images/kt-logo.svg" class="nav-brand-logo" alt="{"Bilik xəzinəsi" if lang == "az" else "Knowledge Treasury"}"></a></div><a aria-label="{aria_home}" class="nav-brand" href="index.html"><span class="nav-brand-text">{brand}</span></a><div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div></div></nav>
<header class="kt-home-hero">
<div class="shell kt-home-hero__inner">
<p class="kt-home-hero__eyebrow">{"Bilik platforması" if lang == "az" else "Knowledge platform"}</p>
<h1>{h1}</h1>
<p class="kt-home-hero__lead">{lead}</p>
</div>
</header>
<main class="main shell" id="content">
<section class="kt-home-cards" aria-label="{"Əsas bölmələr" if lang == "az" else "Main sections"}">
{card_html}
</section>
<section class="kt-home-fields">
<h2 class="kt-section-title">{fields_title}</h2>
<div class="kt-field-grid">{field_pills}</div>
</section>
<section class="kt-home-vision glass-card">
<h2 class="kt-section-title">{vision_title}</h2>
<p>{vision}</p>
</section>
</main>
<footer class="footer-pro"><div class="footer-bottom">{footer}</div></footer>
</body>
</html>
"""


def write_gateway() -> None:
    html = """<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Bilik xəzinəsi / Knowledge Treasury</title>
<meta name="description" content="Knowledge Treasury — discoveries, inventions, and innovations across human history."/>
<link rel="icon" href="images/kt-logo.svg" type="image/svg+xml"/>
<script>
(function () {
  var q = location.search || "";
  if (/[?&](legacy|choose)=1/.test(q)) return;
  var saved;
  try { saved = localStorage.getItem("daab-lang"); } catch (e) {}
  if (saved === "en") { location.replace("en/index.html" + q); return; }
  location.replace("az/index.html" + q);
})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=Playfair+Display:wght@700&amp;display=swap" rel="stylesheet"/>
<link href="css/daab-common.css?v=1" rel="stylesheet"/>
<link href="css/daab-lang.css?v=1" rel="stylesheet"/>
<link href="css/kt-home.css?v=1" rel="stylesheet"/>
</head>
<body class="daab-gateway kt-gateway">
<main class="daab-gateway-page">
<div class="daab-gateway-card">
<img class="daab-gateway-logo" src="images/kt-logo.svg" alt="Knowledge Treasury"/>
<h1>Bilik xəzinəsi</h1>
<p>Knowledge Treasury</p>
<div class="daab-gateway-actions">
<a class="btn btn-primary" href="az/index.html">Azərbaycan dilində davam et</a>
<a class="btn btn-secondary" href="en/index.html">Continue in English</a>
</div>
</div>
</main>
</body>
</html>
"""
    (KT_ROOT / "index.html").write_text(html, encoding="utf-8", newline="\n")


def write_readme(catalog_count: int) -> None:
    text = f"""# Bilik xəzinəsi / Knowledge Treasury

Independent bilingual knowledge platform extracted from the DAAB website Treasury section.

## Contents

- **Home** (`az/index.html`, `en/index.html`)
- **Prominent Figures** — {catalog_count} profiles (`encyclopedia.html`)
- **Industrial Revolutions** — placeholder
- **Major Scientific Inventions** — placeholder

## Local preview

```bat
python helpers/serve_site.py --bind 127.0.0.1 --port 8020
```

Open http://localhost:8020/index.html

## Structure

- `az/`, `en/` — locale pages
- `css/`, `js/`, `images/` — shared assets (DAAB-compatible shell)
- `i18n/` — navigation and UI strings
- `helpers/` — catalog build scripts (not deployed)

## Regenerate catalog after profile edits

```bat
python helpers/_build_prominent_figures_catalog.py
python helpers/_build_en_prominent_figures.py
```
"""
    (KT_ROOT / "README.md").write_text(text, encoding="utf-8", newline="\n")


def copy_tree() -> int:
    count = 0
    for sub in ("css", "js", "images", "i18n", "helpers", "helpers/data", "az", "en"):
        (KT_ROOT / sub).mkdir(parents=True, exist_ok=True)

    for name in CSS_FILES:
        src = DAAB / "css" / name
        if src.is_file():
            shutil.copy2(src, KT_ROOT / "css" / name)
            count += 1
        elif name == "kt-home.css":
            continue
        else:
            print(f"  WARN missing css: {name}")

    for name in JS_FILES:
        shutil.copy2(DAAB / "js" / name, KT_ROOT / "js" / name)
        count += 1

    bg = DAAB / "images" / "diaspor-body-top-bg.png"
    if bg.is_file():
        shutil.copy2(bg, KT_ROOT / "images" / "diaspor-body-top-bg.png")
        count += 1

    for lang in ("az", "en"):
        for page in LOCALE_PAGES:
            src = DAAB / lang / page
            dst = KT_ROOT / lang / page
            dst.write_text(adapt_html(src.read_text(encoding="utf-8"), lang), encoding="utf-8", newline="\n")
            count += 1
        pf_src = DAAB / lang / "prominent_figures"
        pf_dst = KT_ROOT / lang / "prominent_figures"
        if pf_dst.exists():
            shutil.rmtree(pf_dst)
        shutil.copytree(pf_src, pf_dst)
        for path in pf_dst.rglob("*.html"):
            text = adapt_html(path.read_text(encoding="utf-8"), lang)
            path.write_text(text, encoding="utf-8", newline="\n")
            count += 1

    helpers_dst = KT_ROOT / "helpers"
    (helpers_dst / "_paths.py").write_text(
        '"""Knowledge Treasury repo root."""\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent.parent\nHELPERS = Path(__file__).resolve().parent\n',
        encoding="utf-8",
    )
    for name in HELPER_FILES:
        if name == "_paths.py":
            continue
        src = DAAB / "helpers" / name
        if src.is_file():
            shutil.copy2(src, helpers_dst / name)
            count += 1
    for name in HELPER_DATA:
        shutil.copy2(DAAB / "helpers" / "data" / name, helpers_dst / "data" / name)
        count += 1

    return count


def validate_links() -> list[str]:
    errors: list[str] = []
    for path in KT_ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(KT_ROOT).as_posix()
        for m in re.finditer(r'(?:href|src)="([^"#?]+)"', text):
            target = m.group(1)
            if target.startswith(("http", "mailto:", "tel:", "data:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.is_file():
                errors.append(f"{rel} -> {target}")
    return errors[:30]


def main() -> None:
    print(f"Bootstrapping Knowledge Treasury at:\n  {KT_ROOT}\n")
    if KT_ROOT.exists():
        print("  (merging into existing folder)")
    else:
        KT_ROOT.mkdir(parents=True)

    catalog_count = count_catalog_entries()
    copied = copy_tree()
    write_kt_logo()
    write_i18n(catalog_count)
    for lang in ("az", "en"):
        (KT_ROOT / lang / "index.html").write_text(
            home_shell(lang, catalog_count), encoding="utf-8", newline="\n"
        )
    write_gateway()
    write_readme(catalog_count)
    serve = KT_ROOT / "helpers" / "serve_site.py"
    serve.write_text(
        (DAAB / "knowledge-treasury" / "helpers" / "serve_site.py").read_text(encoding="utf-8")
        if (DAAB / "knowledge-treasury" / "helpers" / "serve_site.py").is_file()
        else '',
        encoding="utf-8",
    )
    if not serve.read_text(encoding="utf-8").strip():
        serve.write_text(
            '#!/usr/bin/env python3\n"""Run: python helpers/serve_site.py --port 8020"""\n',
            encoding="utf-8",
        )
    (KT_ROOT / ".nojekyll").write_text("", encoding="utf-8")

    errors = validate_links()
    print(f"Copied/adapted {copied} files")
    print(f"Catalog profiles: {catalog_count}")
    print(f"Homepages: az/index.html, en/index.html")
    if errors:
        print(f"Link check: {len(errors)} issue(s) (first 30 shown)")
        for line in errors:
            print(f"  - {line}")
    else:
        print("Link check: OK")


if __name__ == "__main__":
    main()
