#!/usr/bin/env python3
"""Build en/prominent_figures/*.html from az/prominent_figures/*.html.

Strategy: read the AZ source HTML, run it through the phrase/pattern translator
(_az_profile_translator.py), then replace the nav strip with the EN nav strip
and fix path-relative asset references.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from _az_profile_translator import translate_profile_html
from _prominent_figure_enrichment import apply_en_profile_enrichment
from _build_prominent_figures_catalog import parse_profile
from _embed_static_nav import NAV_EN, prominent_nav, prominent_nav_strip_en
from _paths import ROOT
from _prominent_figure_names_en import apply_english_names, english_name
from _prominent_figure_pronouns_en import apply_singular_pronouns
from _prominent_figure_en_strings import (
    FOOTER_EN,
    CATEGORY_LABEL_EN,
    translate_country,
    translate_field,
    translate_category_tag,
    translate_period,
    translate_region,
)
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

AZ_ROOT = ROOT / "az" / "prominent_figures"
EN_ROOT = ROOT / "en" / "prominent_figures"
ASSET = "../../../"
SKIP = {"hazirlanir.html"}

RE_HERO_INNER = re.compile(
    r"<header class=\"hero pf-profile-hero[^\"]*\">(.*?)</header>",
    re.DOTALL,
)
RE_PLACEHOLDER = re.compile(r"pf-profile-hero--placeholder|Profil hazırlanır", re.I)
RE_META_DESC = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
RE_RELATED = re.compile(
    r'<div class="info-card"><div class="info-title">Həmçinin Baxın</div>.*?</div>(?=</aside>)',
    re.DOTALL,
)


def css_links() -> str:
    return "\n".join(
        f'<link href="{ASSET}css/{name}?v={ver}" rel="stylesheet"/>'
        for name, ver in STYLE_VERSIONS.items()
        if name.startswith("daab-") and name in (
            "daab-common.css",
            "daab-mobile.css",
            "daab-sticky-chrome.css",
            "daab-search.css",
            "daab-back-to-top.css",
            "daab-lang.css",
            "daab-nav-mega.css",
            "daab-hero-summary.css",
            "daab-prominent-figure-profile.css",
        )
    )


def js_scripts() -> str:
    names = [
        "daab-mobile.js",
        "daab-sticky-chrome.js",
        "daab-back-to-top.js",
        "daab-i18n.js",
        "daab-lang-position.js",
        "daab-design-tokens.js",
        "daab-nav.js",
        "daab-primary-nav.js",
        "daab-breadcrumbs.js",
        "daab-shell.js",
        "daab-search.js",
    ]
    return "\n".join(
        f'<script src="{ASSET}js/{name}?v={SCRIPT_VERSIONS[name]}" defer></script>'
        for name in names
        if name in SCRIPT_VERSIONS
    )


def en_summary(row: dict) -> str:
    desc = row.get("summary") or ""
    if desc and not re.search(r"[əğıöüşçƏĞİÖÜŞÇ]", desc):
        return desc
    name = row["name"]
    country = translate_country(row.get("country") or row.get("region") or "")
    field = translate_field(row.get("field") or "")
    if row["category"] == "world":
        return (
            f"{name} is recognized as a major figure in {field or 'this field'}, "
            "with a legacy that contributed to the development of world science and thought."
        )
    return (
        f"{name} was a prominent representative of {country or 'the Turkic world'} "
        f"whose work in {field or 'science, culture, and public life'} occupies an important "
        "place in the shared intellectual and cultural heritage of the Turkic world."
    )


def hero_block(row: dict) -> str:
    emoji = html.escape(row.get("emoji") or "⭐")
    name = html.escape(row["name"])
    dates = html.escape(row.get("dates") or "")
    country = html.escape(translate_country(row.get("country") or ""))
    category_tag = html.escape(translate_category_tag(row.get("categoryLabel") or ""))
    tags = ""
    if country:
        tags += f'<span class="hero-tag gold">{country}</span>\n'
    if category_tag:
        tags += f'<span class="hero-tag">{category_tag}</span>'
    return (
        '<header class="hero pf-profile-hero"><div class="hero-inner shell pf-profile-hero__inner">'
        '<section class="hero-copy"><div class="pf-profile-hero__title-row">'
        f'<aside class="pf-hero-symbol" aria-hidden="true">'
        f'<span class="pf-hero-symbol__icon">{emoji}</span></aside>'
        f"<h1>{name}</h1></div>"
        f'<p class="pf-hero-dates">{dates}</p>'
        f'<div class="hero-tags">{tags}</div>'
        "</section></div></header>"
    )


def main_col_world(row: dict) -> str:
    name = row["name"]
    esc = html.escape
    dates = row.get("dates") or ""
    country = translate_country(row.get("country") or "")
    field = translate_field(row.get("field") or "")
    summary = en_summary(row)
    lead = (
        f"{name} ({dates}) is one of the notable figures associated with "
        f"{country or 'world science'}. This work is closely connected with "
        f"{field or 'scientific and intellectual inquiry'} and reflects the broader "
        "search for knowledge, evidence, and new methods of understanding."
    )
    return f"""<div class="main-col">
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>About {esc(name)}</div>
  <div class="prose pf-profile-article"><h3>Life journey</h3><p>{esc(lead)}</p><h3>Scholarly and creative work</h3><p>{esc(summary)} The importance of this legacy lies not only in individual works or discoveries, but also in the questions, methods, and intellectual standards it helped transmit to later generations.</p><h3>Impact on society</h3><p>{esc(name)} influenced the intellectual climate of the period and remains part of a wider tradition of inquiry, creativity, and public service.</p></div>
</div>
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>Key works and activity</div><ul class="works-list"><li class="work-item"><div class="work-num">1</div><div><div class="work-name"><em>Contributions in {esc(country or "the region")}</em></div><div class="work-desc">{esc(summary)}</div></div></li>
<li class="work-item"><div class="work-num">2</div><div><div class="work-name"><em>Scientific and intellectual legacy</em></div><div class="work-desc">{esc(name)} made a lasting contribution to the growth and spread of knowledge.</div></div></li>
<li class="work-item"><div class="work-num">3</div><div><div class="work-name"><em>Impact on humanity</em></div><div class="work-desc">This work left a memorable mark in the story of human progress.</div></div></li></ul></div>
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>Notable aspects of the life and work</div><div class="event-item"><div class="event-title"><span>🔎</span> A symbol of inquiry</div><div class="event-text">{esc(name)} is remembered for ideas and research that expanded the boundaries of knowledge.</div></div>
<div class="event-item"><div class="event-title"><span>🌍</span> Impact beyond borders</div><div class="event-text">This legacy influenced research and education in many countries.</div></div></div>
<div class="quote-block"><div class="quote-text">Science, culture, and thought are among the greatest forces shaping humanity's future.</div><div class="quote-source">— A guiding idea associated with {esc(name)}'s legacy</div></div>
{sources_block(name)}
</div>"""


def main_col_azturk(row: dict) -> str:
    name = row["name"]
    esc = html.escape
    country = translate_country(row.get("country") or row.get("region") or "")
    field = translate_field(row.get("field") or "")
    summary = en_summary(row)
    return f"""<div class="main-col">
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>About {esc(name)}</div>
  <div class="prose pf-profile-article"><h3>Life journey</h3><p>{esc(summary)} This figure's life and work are presented as part of the wider historical memory of the Turkic world, where scholarship, leadership, literature, and culture often developed in close relationship with one another.</p><h3>Scholarly and creative work</h3><p>{esc(name)} contributed to the traditions associated with {esc(field or "this field")} and helped shape the cultural and intellectual environment of the period. The profile highlights this work, the contribution to public and cultural life, and the place in the shared heritage of Turkic communities.</p><h3>Impact on society</h3><p>{esc(name)} influenced the intellectual climate of the period and remains an example of learning, inquiry, and creative service for later generations.</p></div>
</div>
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>Key works and activity</div><ul class="works-list"><li class="work-item"><div class="work-num">1</div><div><div class="work-name"><em>Contributions in {esc(country or "the region")}</em></div><div class="work-desc">{esc(summary)}</div></div></li>
<li class="work-item"><div class="work-num">2</div><div><div class="work-name"><em>Scientific and intellectual legacy</em></div><div class="work-desc">{esc(name)} made a lasting contribution to the growth and spread of knowledge.</div></div></li>
<li class="work-item"><div class="work-num">3</div><div><div class="work-name"><em>Impact on humanity</em></div><div class="work-desc">This work left a memorable mark in the story of human progress.</div></div></li></ul></div>
<div class="section-card"><div class="section-title"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>Notable aspects of the life and work</div><div class="event-item"><div class="event-title"><span>🔎</span> Inquiry and creativity</div><div class="event-text">{esc(name)} strengthened new directions of thought and research in this field.</div></div>
<div class="event-item"><div class="event-title"><span>🌍</span> Remembered widely</div><div class="event-text">This legacy is recalled across many scientific and cultural settings.</div></div></div>
<div class="quote-block"><div class="quote-text">Science, culture, and thought are among the greatest forces shaping humanity's future.</div><div class="quote-source">— A guiding idea associated with {esc(name)}'s legacy</div></div>
{sources_block(name)}
</div>"""


def sources_block(name: str) -> str:
    q = html.escape(name)
    return f"""<div class="section-card" id="qaynaqlar"><h2 class="section-title">📚 Sources</h2><div class="prose"><p>This profile is based on open, reliable reference works. When portraits or photographs are added to the site, copyright and licensing should be verified separately.</p><ul class="source-links"><li><a href="https://www.google.com/search?q=Encyclopaedia+Britannica+%E2%80%94+{q}" target="_blank" rel="noopener">Encyclopaedia Britannica — {q}</a></li>
<li><a href="https://www.google.com/search?q=WorldCat+and+scholarly+publications+%E2%80%94+{q}" target="_blank" rel="noopener">WorldCat and scholarly publications — {q}</a></li>
<li><a href="https://www.google.com/search?q=Oxford+Reference+%E2%80%94+{q}" target="_blank" rel="noopener">Oxford Reference — {q}</a></li></ul></div></div>"""


def sidebar_block(row: dict) -> str:
    name = html.escape(row["name"])
    country = html.escape(translate_country(row.get("country") or row.get("region") or ""))
    field_raw = row.get("field") or ""
    country_val = translate_country(row.get("country") or "")
    field_display = html.escape(
        f"{country_val}, {translate_field(field_raw)}"
        if country_val and field_raw
        else translate_field(field_raw) or country_val or ""
    )
    category_period = html.escape(
        translate_category_tag(row.get("categoryLabel") or "")
        if row.get("category") == "azturk"
        else translate_category_tag(CATEGORY_LABEL_EN.get("world", ""))
    )
    birth = death = ""
    if row.get("dates"):
        parts = re.split(r"[–—\-]", row["dates"])
        if parts:
            birth = html.escape(parts[0].strip())
        if len(parts) > 1:
            death = html.escape(parts[-1].strip())
    people = html.escape(
        country if row["category"] == "azturk" else translate_region(row.get("region") or "World science")
    )
    return f"""<aside class="sidebar"><div class="info-card"><div class="info-title">Personal information</div><div class="info-row"><span class="info-label">Full name</span><span class="info-val">{name}</span></div><div class="info-row"><span class="info-label">Date of birth</span><span class="info-val">{birth}</span></div><div class="info-row"><span class="info-label">Date of death</span><span class="info-val">{death}</span></div><div class="info-row"><span class="info-label">People / origin</span><span class="info-val">{people}</span></div><div class="info-row"><span class="info-label">Period / context</span><span class="info-val">{category_period}</span></div><div class="info-row"><span class="info-label">Field</span><span class="info-val">{field_display}</span></div><div class="info-divider"></div><div class="info-title">Contributions to society</div><ul class="contribution-list"><li class="contribution-item">Made an important contribution in {html.escape(country_val or 'this field')}</li>
<li class="contribution-item">Enriched the scientific and intellectual heritage</li>
<li class="contribution-item">Shaped ideas that influenced human progress</li></ul></div>
<div class="info-card"><div class="info-title">See also</div>RELATED_PLACEHOLDER</div></aside>"""


def placeholder_page(nav_menu: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{ASSET}" data-daab-page-id="prominent-figure" data-daab-profile-name="" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Profile in preparation — WAAS</title>
<meta name="description" content="This encyclopedia profile is being prepared."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
{css_links()}
{js_scripts()}
</head>
<body class="daab-prominent-figure-page">
<a class="skip" href="#content">Skip to content</a>
{prominent_nav_strip_en(nav_menu)}
<header class="hero pf-profile-hero pf-profile-hero--placeholder"><div class="hero-inner shell"><section class="hero-copy"><h1>Profile in preparation</h1><p>Material for this figure is being prepared in stages and will be published on a dedicated profile page with sources.</p></section></div></header>
<main class="pf-main" id="content"><div class="card"><p>The first profile group — from antiquity and the Middle Ages through the modern era — is already available in full page format in the catalog.</p><a class="btn" href="../../encyclopedia.html">Back to catalog</a></div></main>
{FOOTER_EN}
</body>
</html>
"""


def render_profile(row: dict, nav_menu: str) -> str:
    name = row["name"]
    esc_name = html.escape(name, quote=True)
    title = html.escape(f"{name} — Prominent Figures | WAAS")
    desc = html.escape(en_summary(row), quote=True)
    main_inner = main_col_azturk(row) if row["category"] == "azturk" else main_col_world(row)
    sidebar = sidebar_block(row).replace("RELATED_PLACEHOLDER", "RELATED_PLACEHOLDER")
    body = (
        f'<main class="pf-main" id="content"><div class="content-grid">{main_inner}{sidebar}</div></div></main>'
    )
    return f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{ASSET}" data-daab-page-id="prominent-figure" data-daab-profile-name="{esc_name}" data-daab-nav-mount="1">
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
<a class="skip" href="#content">Skip to content</a>
{prominent_nav_strip_en(nav_menu)}
{hero_block(row)}
{body}
{FOOTER_EN}
</body>
</html>
"""


def build_file(az_path: Path, group: str, nav_menu: str) -> bool:
    """Translate az_path to EN, save under en/prominent_figures/{group}/."""
    if az_path.stem.endswith("_EN"):
        return False

    en_path = EN_ROOT / group / az_path.name
    en_path.parent.mkdir(parents=True, exist_ok=True)

    az_text = az_path.read_text(encoding="utf-8")

    # Placeholder pages
    if az_path.name in SKIP or RE_PLACEHOLDER.search(az_text):
        en_path.write_text(placeholder_page(nav_menu), encoding="utf-8", newline="\n")
        return True

    # Parse metadata for fallback / meta tag generation
    row = parse_profile(az_path, group)
    if row:
        row["categoryLabel"] = CATEGORY_LABEL_EN[group]
    slug = az_path.stem
    az_name = row["name"] if row else slug.replace("_", " ").title()
    en_name = english_name(slug, az_name)

    # --- Run the comprehensive translator on the AZ HTML ---
    translated = translate_profile_html(az_text, name=en_name, az_source=az_text)
    translated = apply_en_profile_enrichment(translated, slug)

    # --- Replace the AZ nav strip with the EN nav strip ---
    # The AZ nav is wrapped in <nav ...> ... </nav> near the top of <body>
    NAV_START_MARKERS = [
        '<nav class="primary-nav',
        '<nav aria-label="Əsas naviqasiya"',
        '<nav aria-label="Ana',
    ]
    nav_start = -1
    for marker in NAV_START_MARKERS:
        nav_start = translated.find(marker)
        if nav_start != -1:
            break
    if nav_start == -1:
        # fallback: find first <nav
        nav_start = translated.find("<nav")
    if nav_start != -1:
        nav_end = translated.find("</nav>", nav_start)
        if nav_end != -1:
            translated = (
                translated[:nav_start]
                + prominent_nav_strip_en(nav_menu)
                + translated[nav_end + len("</nav>"):]
            )

    # --- English display names throughout page text ---
    translated = apply_english_names(translated, slug)
    translated = apply_singular_pronouns(translated)
    translated = re.sub(
        r"(<h1>)(.*?)(</h1>)",
        lambda m: f"{m.group(1)}{html.escape(en_name)}{m.group(3)}",
        translated,
        count=1,
    )
    translated = re.sub(
        r'data-daab-profile-name="[^"]*"',
        f'data-daab-profile-name="{html.escape(en_name, quote=True)}"',
        translated,
        count=1,
    )
    translated = re.sub(
        r'(info-label">Full name</span><span class="info-val">)([^<]*)(</span>)',
        lambda m: f"{m.group(1)}{html.escape(en_name)}{m.group(3)}",
        translated,
        count=1,
    )

    # --- Fix title tag: translate remaining AZ page title ---
    translated = _fix_title_tag(translated, en_name, group)

    # --- Fix meta description ---
    translated = _fix_meta_description(translated, en_name, row)

    en_path.write_text(translated, encoding="utf-8", newline="\n")
    return True


# Patterns to fix title and meta tags
_RE_TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.I)
_RE_META_DESC = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
_GROUP_LABEL_TITLE = {
    "azturk": "Azerbaijani & Turkic Heritage",
    "world": "World Scientists",
}


def _fix_title_tag(html_text: str, name: str, group: str) -> str:
    """Replace AZ title tag with a clean English title."""
    label = _GROUP_LABEL_TITLE.get(group, "Prominent Figures")
    new_title = f"<title>{name} — {label} | WAAS</title>"
    return _RE_TITLE.sub(new_title, html_text, count=1)


def _fix_meta_description(html_text: str, name: str, row: dict | None) -> str:
    """Replace AZ meta description with an English one derived from row data."""
    if not row:
        return html_text
    country = translate_country(row.get("country") or row.get("region") or "")
    field = translate_field(row.get("field") or "")
    period = translate_period(row.get("period") or "")
    if row.get("category") == "world":
        desc = (
            f"{name} ({period}) — {field}. "
            "Compiled profile on the WAAS Encyclopedia of Prominent Figures."
        )
    else:
        desc = (
            f"{name} — {country}. {field}. "
            "Compiled profile on the WAAS Encyclopedia of Prominent Figures."
        )
    new_tag = f'<meta name="description" content="{html.escape(desc[:200])}"'
    return _RE_META_DESC.sub(new_tag, html_text, count=1)


def main() -> int:
    nav_menu = prominent_nav(NAV_EN)
    n = 0
    for group in ("azturk", "world"):
        folder = AZ_ROOT / group
        if not folder.is_dir():
            continue
        for az_path in sorted(folder.glob("*.html")):
            if build_file(az_path, group, nav_menu):
                n += 1
    print(f"Built {n} English profile pages under {EN_ROOT.relative_to(ROOT)}")
    print("Next: python helpers/_fix_prominent_figures_related.py --lang en")
    print("      python helpers/_build_prominent_figures_catalog.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
