#!/usr/bin/env python3
"""Shared renderer for scientist "media / internet resources" index pages.

Both `_build_sirajov_media.py` and `_build_teymur_media.py` provide a small
config (strings + resource list + thumbnails) and call `write_pages(cfg)`.
The HTML shell, cards, hero summary panel and footer are produced here so the
two pages stay pixel-identical and share `css/daab-media-resources.css`
(scoped via `data-daab-page-kind="scientist-media"`).
"""
from __future__ import annotations

import html
from pathlib import Path

from _paths import ROOT

MEDIA_CSS_VER = 4  # bump when css/daab-media-resources.css content changes

PLAY_SVG = (
    '<span class="media-card__play" aria-hidden="true">'
    '<svg viewBox="0 0 68 48" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M66.5 7.7c-.8-2.9-2.5-5.2-5.5-6C55.6.5 34 .5 34 .5S12.4.5 6.9 1.7C4 2.5 2.2 4.8 1.5 7.7.4 13.2.4 24 .4 24s0 10.8 1.1 16.3c.8 2.9 2.5 5.2 5.5 6C12.4 47.5 34 47.5 34 47.5s21.6 0 27.1-1.2c3-.8 4.7-3.1 5.5-6C67.6 34.8 67.6 24 67.6 24s0-10.8-1.1-16.3z" fill="#f00"/>'
    '<path d="M27 34.5l18-10.5L27 13.5z" fill="#fff"/></svg></span>'
)
EXT_SVG = (
    '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" '
    'stroke-linecap="round" stroke-linejoin="round"></path></svg>'
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def favicon(domain: str) -> str:
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=128"


def card_html(item: dict, lang: str, strings: dict, thumb_prefix: str) -> str:
    s = strings[lang]
    title = esc(item[lang])
    date = esc(item.get(f"{lang}_date", item.get("date", "")))
    source = esc(item["source"])
    is_video = item["kind"] == "video"

    if is_video:
        url = f"https://www.youtube.com/watch?v={item['yt']}"
        tag, go, overlay = s["tag_video"], f'{s["go_video"]}{EXT_SVG}', PLAY_SVG
    else:
        url = item["url"]
        tag, go, overlay = s["tag_article"], f'{s["go_article"]}{EXT_SVG}', ""

    # Prefer the original site thumbnail; fall back gracefully if missing.
    if item.get("thumb"):
        img = f'<img src="{esc(thumb_prefix + item["thumb"])}" alt="" loading="lazy"/>'
    elif is_video:
        img = f'<img src="https://i.ytimg.com/vi/{item["yt"]}/hqdefault.jpg" alt="" loading="lazy"/>'
    else:
        img = f'<img src="{favicon(item["source"])}" alt="" loading="lazy" width="46" height="46"/>'

    thumb = (
        '<figure class="media-card__thumb">'
        f'{img}<span class="media-type-tag">{tag}</span>{overlay}'
        '</figure>'
    )
    fav_badge = favicon(item["source"])
    return (
        f'<a class="media-card media-card--{item["kind"]}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">'
        f'{thumb}'
        '<div class="media-card__body">'
        f'<span class="media-card__source"><img src="{fav_badge}" alt="" loading="lazy" width="16" height="16"/>{source}</span>'
        f'<h3 class="media-card__title">{title}</h3>'
        '<div class="media-card__meta">'
        f'<span class="media-card__date">{date}</span>'
        f'<span class="media-card__go">{go}</span>'
        '</div></div></a>'
    )


def section_html(section_no: int, lang: str, strings: dict, resources: list, thumb_prefix: str) -> str:
    s = strings[lang]
    items = [it for it in resources if it["section"] == section_no]
    heading = s[f"sec{section_no}"]
    cards = "\n".join(card_html(it, lang, strings, thumb_prefix) for it in items)
    return (
        '<section class="media-section">'
        '<div class="media-section-head">'
        f'<h2>{esc(heading)}</h2>'
        f'<span class="media-section-count">{len(items)} {esc(s["count_one"])}</span>'
        '</div>'
        f'<div class="media-grid">\n{cards}\n</div>'
        '</section>'
    )


def build_html(cfg: dict, lang: str) -> str:
    strings = cfg["strings"]
    s = strings[lang]
    slug = cfg["slug"]
    page_id = cfg["page_id"]
    thumb_dirname = cfg["thumb_dirname"]
    resources = cfg["resources"]

    canonical = f"https://daab-waas.com/{lang}/scientists/{slug}.html"
    az_url = f"https://daab-waas.com/az/scientists/{slug}.html"
    en_url = f"https://daab-waas.com/en/scientists/{slug}.html"
    # Thumbnails live under az/scientists/; EN pages reach them cross-locale.
    thumb_prefix = f"{thumb_dirname}/" if lang == "az" else f"../../az/scientists/{thumb_dirname}/"

    section_nos = sorted({it["section"] for it in resources})
    sections = "\n".join(section_html(n, lang, strings, resources, thumb_prefix) for n in section_nos)

    # Mark EN as a finished translation so _build_bilingual_tree.py never
    # replaces this page with a "Translation in progress" stub.
    en_marker = "\n<!-- daab-en-complete -->" if lang == "en" else ""

    return f"""<!DOCTYPE html>
<html lang="{s['lang']}" data-daab-lang="{s['lang']}" data-daab-asset-root="../../" data-daab-page-id="{page_id}" data-daab-page-kind="scientist-media" data-daab-nav-mount="1">
<head>{en_marker}
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(s['title'])}</title>
<meta content="{esc(s['meta_desc'])}" name="description"/>
<link rel="icon" href="../../images/daab-logo.png" type="image/png"/>
<link rel="canonical" href="{canonical}"/>
<link rel="alternate" hreflang="az" href="{az_url}"/>
<link rel="alternate" hreflang="en" href="{en_url}"/>
<link rel="alternate" hreflang="x-default" href="{az_url}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="DAAB"/>
<meta property="og:title" content="{esc(s['title'])}"/>
<meta property="og:description" content="{esc(s['meta_desc'])}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:image" content="https://daab-waas.com/images/daab-logo.png"/>
<meta property="og:locale" content="{s['locale']}"/>
<meta name="twitter:card" content="summary_large_image"/>
<link href="../../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../../css/daab-common.css?v=81" rel="stylesheet"/>
<link href="../../css/daab-perf.css?v=2" rel="stylesheet"/>
<link href="../../css/daab-mobile.css?v=14" rel="stylesheet"/>
<link href="../../css/daab-sticky-chrome.css?v=2" rel="stylesheet"/>
<link href="../../css/daab-search.css?v=7" rel="stylesheet"/>
<link href="../../css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../../css/daab-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../../css/daab-lang.css?v=13" rel="stylesheet"/>
<link href="../../css/daab-nav-mega.css?v=69" rel="stylesheet"/>
<link href="../../css/daab-media-resources.css?v={MEDIA_CSS_VER}" rel="stylesheet"/>
<script src="../../js/daab-mobile.js?v=6" defer></script>
<script src="../../js/daab-perf.js?v=4" defer></script>
<script src="../../js/daab-sticky-chrome.js?v=3" defer></script>
<script src="../../js/daab-back-to-top.js?v=3" defer></script>
<script src="../../js/daab-i18n.js?v=39" defer></script>
<script src="../../js/daab-lang-position.js?v=8" defer></script>
<script src="../../js/daab-design-tokens.js?v=2" defer></script>
<script src="../../js/daab-nav.js?v=31" defer></script>
<script src="../../js/daab-primary-nav.js?v=60" defer></script>
<script src="../../js/daab-breadcrumbs.js?v=49" defer></script>
<script src="../../js/daab-shell.js?v=13" defer></script>
<script src="../../js/daab-page-subtitle.js?v=2" defer></script>
<script src="../../js/daab-search.js?v=14" defer></script>
<script src="../../js/daab-analytics.js?v=1" defer></script>
</head>
<body>
<a class="skip" href="#content">{esc(s['skip'])}</a>
<nav aria-label="{esc(s['brand_menu_aria'])}" class="nav-strip"><div class="nav-inner"><button class="mobile-menu-toggle" type="button" aria-label="{esc(s['menu_open'])}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button><div class="page-logo"><a title="{esc(s['nav_home_title'])}" aria-label="{esc(s['nav_home_aria'])}" href="../index.html"><img src="../../images/daab-logo.png" class="nav-brand-logo" alt="DAAB Logo"></a></div><a aria-label="{esc(s['nav_home_aria'])}" class="nav-brand" href="../index.html"><span class="nav-brand-text">{s['brand']}</span></a><div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div></div></nav>
<nav class="daab-breadcrumbs" id="daab-breadcrumbs" aria-label="{esc(s['crumb_aria'])}">
<ol class="daab-breadcrumbs-list">
<li class="daab-breadcrumbs-item"><a href="../index.html">{esc(s['crumb_home'])}</a></li>
<li class="daab-breadcrumbs-item"><span class="daab-breadcrumbs-sep" aria-hidden="true">›</span><a href="list.html">{esc(s['crumb_scientists'])}</a></li>
<li class="daab-breadcrumbs-item"><span class="daab-breadcrumbs-sep" aria-hidden="true">›</span><span class="daab-breadcrumbs-current" aria-current="page">{esc(s['crumb_current'])}</span></li>
</ol>
</nav>
<header class="page-hero">
<div class="hero-inner shell">
<section>
<h1>{esc(s['h1'])}<br><em>{esc(s['h1_em'])}</em></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(s['subtitle'])}</p>
</section>
<aside aria-label="{esc(s['panel_title'])}" class="hero-summary-panel">
<div class="hero-summary-card">
<h2 class="panel-title">{esc(s['panel_title'])}</h2>
<p class="hero-text panel-copy-lead">{esc(s['panel_copy'])}</p>
</div>
</aside>
</div>
</header>
<main class="main media-main" id="content">
{sections}
</main>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(s['footer_org'])}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_contact'])}</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a rel="noopener noreferrer" href="https://daab-waas.com" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_addr'])}</h4><p class="footer-address">{s['footer_addr_body']}</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_lead_h'])}</h4><p class="footer-leader">{s['footer_lead_body']}</p></div>
</div>
</div>
<div class="footer-bottom">{esc(s['footer_rights'])}</div>
</footer>
</body>
</html>
"""


def write_pages(cfg: dict) -> int:
    # Attach the downloaded thumbnail filename to each resource (1:1 by order).
    for i, item in enumerate(cfg["resources"]):
        item["thumb"] = cfg["thumbs"][i] if i < len(cfg["thumbs"]) else None

    slug = cfg["slug"]
    targets = {
        "az": ROOT / "az" / "scientists" / f"{slug}.html",
        "en": ROOT / "en" / "scientists" / f"{slug}.html",
    }
    for lang, path in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(build_html(cfg, lang), encoding="utf-8", newline="\n")
        print(f"Wrote {path.relative_to(ROOT)} ({len(cfg['resources'])} resources)")
    return 0
