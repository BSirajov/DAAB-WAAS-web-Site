#!/usr/bin/env python3
"""Build az/en forum/2024/roadmap.html from forum_2024/Strateji_yol_xəritəsi.docx."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _embed_static_nav import forum_nav_strip  # noqa: E402
from forum_en_roadmap import ROADMAP_EN  # noqa: E402

DOCX = ROOT / "forum_2024" / "Strateji_yol_xəritəsi.docx"
OUT_AZ = ROOT / "az" / "forum" / "2024" / "roadmap.html"
OUT_EN = ROOT / "en" / "forum" / "2024" / "roadmap.html"
ASSET = "../../../"
PAGE_ID = "forum-roadmap"

AZ_CATEGORIES = [
    "Təhsil və akademik inkişaf",
    "Elmi tədqiqat və nəşrlər",
    "Rəqəmsal platformalar və virtual infrastruktur",
    "Beynəlxalq əməkdaşlıq və diaspor inteqrasiyası",
    "Gənclər və ictimai maarifləndirmə",
    "Səhiyyə və biotexnologiyalar",
    "İncəsənət, dil və mədəni irs",
    "İdarəçilik, siyasət və hüquqi mexanizmlər",
    "Enerji, ətraf mühit və regionların inkişafı",
]

CATEGORY_IDS = {
    "Təhsil və akademik inkişaf": "education",
    "Elmi tədqiqat və nəşrlər": "research",
    "Rəqəmsal platformalar və virtual infrastruktur": "digital",
    "Beynəlxalq əməkdaşlıq və diaspor inteqrasiyası": "international",
    "Gənclər və ictimai maarifləndirmə": "youth",
    "Səhiyyə və biotexnologiyalar": "health",
    "İncəsənət, dil və mədəni irs": "culture",
    "İdarəçilik, siyasət və hüquqi mexanizmlər": "governance",
    "Enerji, ətraf mühit və regionların inkişafı": "energy",
}

SIDEBAR_SCRIPT = f'<script src="{ASSET}js/daab-sidebar-timeline.js?v=1" defer></script>'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def norm(text: str) -> str:
    return text.replace("\r", "").replace("\xa0", " ").strip()


def slugify(title: str) -> str:
    return CATEGORY_IDS.get(title, re.sub(r"[^a-z0-9]+", "-", title.lower())[:40].strip("-"))


def parse_docx(doc: Document) -> dict:
    lines = [norm(p.text) for p in doc.paragraphs if norm(p.text)]
    title = lines[0] if lines else ""
    subtitle = lines[1] if len(lines) > 1 else ""
    intro: list[str] = []
    closing = ""
    sections: list[dict] = []
    current: dict | None = None
    cat_set = set(AZ_CATEGORIES)

    i = 2
    while i < len(lines):
        line = lines[i]
        if line.startswith("Təqdim edilmiş"):
            closing = line
            break
        if line in cat_set:
            if current:
                sections.append(current)
            current = {"title": line, "id": slugify(line), "items": []}
            i += 1
            continue
        if current is None:
            intro.append(line)
        else:
            current["items"].append(line)
        i += 1

    if current:
        sections.append(current)

    return {
        "title": title,
        "subtitle": subtitle,
        "intro": intro,
        "closing": closing,
        "sections": sections,
    }


def list_html(items: list[str]) -> str:
    lis = "".join(f"<li>{esc(t)}</li>" for t in items)
    return f'<ul class="content-list">{lis}</ul>'


def overview_card(data: dict, *, lang: str) -> str:
    if lang == "en":
        title = ROADMAP_EN["title"]
        subtitle = ROADMAP_EN["subtitle"]
        intro = ROADMAP_EN["intro"]
        closing = ROADMAP_EN["closing"]
    else:
        title = data["title"]
        subtitle = data["subtitle"]
        intro = data["intro"]
        closing = data["closing"]

    intro_html = "".join(f'<p class="card-text">{esc(p)}</p>' for p in intro)
    closing_html = f'<p class="card-text card-text--closing">{esc(closing)}</p>' if closing else ""
    return f"""
<article class="news-card roadmap-overview-card" id="overview">
<div class="card-header">
<h2 class="card-title">{esc(title)}</h2>
</div>
<div class="card-body">
<p class="card-lead">{esc(subtitle)}</p>
{intro_html}
{closing_html}
</div>
</article>"""


def section_card(section: dict, *, lang: str) -> str:
    if lang == "en":
        en_sec = next(s for s in ROADMAP_EN["sections"] if s["id"] == section["id"])
        title = en_sec["title"]
        items = en_sec["items"]
    else:
        title = section["title"]
        items = section["items"]

    return f"""
<article class="news-card roadmap-section-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(title)}</h2>
</div>
<div class="card-body">
{list_html(items)}
</div>
</article>"""


def toc_items(sections: list[dict], *, lang: str) -> str:
    if lang == "en":
        overview_label = "Overview"
    else:
        overview_label = "Ümumi baxış"
    parts = [f'<li><a href="#overview">{esc(overview_label)}</a></li>']
    for sec in sections:
        if lang == "en":
            title = next(s["title"] for s in ROADMAP_EN["sections"] if s["id"] == sec["id"])
        else:
            title = sec["title"]
        parts.append(f'<li><a href="#{esc(sec["id"])}">{esc(title)}</a></li>')
    return "\n".join(parts)


def page_html(data: dict, *, lang: str) -> str:
    if lang == "en":
        meta = ROADMAP_EN
        hero_h1 = meta["hero_h1"]
        panel_title = meta["panel_title"]
        panel_copy = meta["panel_copy"]
        breadcrumb = meta["breadcrumb"]
        sidebar_label = meta["sidebar_label"]
        sidebar_aria = meta["sidebar_aria"]
        page_title = meta["page_title"]
        meta_desc = meta["meta_description"]
        skip = "Skip to content"
        bc_home = "Home"
        bc_activities = "Activities"
        bc_forum = "Forum 2024"
        footer_brand = "World Association of Azerbaijani Scientists"
        footer_contact = "Contact"
        footer_address_title = "Address"
        footer_leadership = "Leadership"
        footer_rights = "© 2026 DAAB / WAAS — All Rights Reserved"
        bc_aria = "Breadcrumb"
        panel_aria = "Strategic roadmap summary"
    else:
        hero_h1 = "Strateji <span>yol xəritəsi</span>"
        panel_title = "Strateji yol xəritəsi"
        panel_copy = (
            "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu iştirakçılarının təklifləri "
            "əsasında Azərbaycan elmi və təhsilinin inkişafı üçün strateji hədəflər."
        )
        breadcrumb = "Strateji yol xəritəsi"
        sidebar_label = "🗺️ Yol xəritəsi"
        sidebar_aria = "Yol xəritəsi menyusunu aç"
        page_title = "Strateji yol xəritəsi — DAAB"
        meta_desc = (
            "Azərbaycan elmi və təhsilinin inkişafına dair yol xəritəsi — "
            "Forum 2024 iştirakçılarının strateji təklifləri."
        )
        skip = "Məzmuna keç"
        bc_home = "Ana səhifə"
        bc_activities = "Fəaliyyətimiz"
        bc_forum = "Forum 2024"
        footer_brand = "Dünya Azərbaycanlı Alimlər Birliyi"
        footer_contact = "Əlaqə"
        footer_address_title = "Ünvan"
        footer_leadership = "Rəhbərlik"
        footer_rights = "© 2026 DAAB — Bütün hüquqlar qorunur"
        bc_aria = "Səhifə yolu"
        panel_aria = "Strateji yol xəritəsi haqqında qısa məlumat"

    cards = overview_card(data, lang=lang) + "".join(
        section_card(s, lang=lang) for s in data["sections"]
    )
    toc = toc_items(data["sections"], lang=lang)
    nav = forum_nav_strip(lang, active_nav_id="forum-2024")

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{ASSET}" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(meta_desc)}"/>
<link href="{ASSET}css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=23" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v=9" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v=14" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-shell.js?v=11" defer></script>
<script src="{ASSET}js/daab-search.js?v=4" defer></script>
</head>
<body>
<a class="skip" href="#content">{esc(skip)}</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="{esc(bc_aria)}">
<a href="../../index.html">{esc(bc_home)}</a><span aria-hidden="true">›</span><a href="../../activities.html">{esc(bc_activities)}</a><span aria-hidden="true">›</span><a href="index.html">{esc(bc_forum)}</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">{esc(breadcrumb)}</span>
</div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>{hero_h1}</h1>
</section>
<aside aria-label="{esc(panel_aria)}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(panel_title)}</h2>
<div class="panel-copy">{esc(panel_copy)}</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head"><span>{sidebar_label}</span><button aria-controls="roadmapTOC" aria-expanded="false" aria-label="{esc(sidebar_aria)}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="roadmapTOC">
{toc}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cards}
</main>
</div>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(footer_brand)}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(footer_contact)}</h4><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(footer_address_title)}</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(footer_leadership)}</h4><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Germany — James D. Murray Distinguished Professor</p></div>
</div>
</div>
<div class="footer-bottom">{esc(footer_rights)}</div>
</footer>
{SIDEBAR_SCRIPT}
</body>
</html>
"""


def patch_routes() -> None:
    path = ROOT / "i18n" / "routes.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if any(p["id"] == PAGE_ID for p in data["pages"]):
        return
    entry = {
        "id": PAGE_ID,
        "navId": PAGE_ID,
        "navGroup": "forum",
        "navParent": "forum",
        "navOrder": 7,
        "legacy": None,
        "az": "az/forum/2024/roadmap.html",
        "en": "en/forum/2024/roadmap.html",
    }
    data["pages"].append(entry)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")


def patch_nav() -> None:
    path = ROOT / "i18n" / "nav.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    pages = data["sections"]["forum"]["pages"]
    if PAGE_ID not in pages:
        pages.append(PAGE_ID)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")


def patch_ui() -> None:
    path = ROOT / "i18n" / "ui.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    az = data["nav"]["az"]
    en = data["nav"]["en"]
    icons = data.setdefault("navIcons", {})
    if "forumRoadmap" not in az:
        az["forumRoadmap"] = "Strateji yol xəritəsi"
        en["forumRoadmap"] = "Strategic roadmap"
        icons[PAGE_ID] = "🗺️"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")


def patch_forum_css() -> None:
    """forum-roadmap must appear in daab-activities-layout.css (do not patch via string replace)."""
    layout = ROOT / "css" / "daab-activities-layout.css"
    if PAGE_ID not in layout.read_text(encoding="utf-8"):
        print(f"warn: add {PAGE_ID} to daab-activities-layout.css")


def patch_search_index_loader() -> None:
    path = ROOT / "helpers" / "_build_search_index.py"
    text = path.read_text(encoding="utf-8")
    key = f'"{PAGE_ID}":'
    if key in text:
        return
    needle = '"forum-2024-presentations": lambda raw, lang: extract_forum_sections(raw, lang, "forum-2024-presentations"),'
    repl = (
        needle + "\n"
        f'        "{PAGE_ID}": lambda raw, lang: extract_forum_sections(raw, lang, "{PAGE_ID}"),'
    )
    text = text.replace(needle, repl)
    icon_needle = '"forum-impressions": "forumImpressions",'
    if icon_needle in text and '"forumRoadmap"' not in text:
        text = text.replace(
            icon_needle,
            icon_needle + '\n    "forum-roadmap": "forumRoadmap",',
        )
    path.write_text(text, encoding="utf-8", newline="\n")
    print("updated _build_search_index.py")


def patch_hub_cards() -> None:
    for lang, href, title, desc, icon, tags in (
        (
            "az",
            "roadmap.html",
            "Strateji yol xəritəsi",
            "Forum iştirakçılarının elmi və təhsil inkişafı üçün strateji təklifləri.",
            "🗺️",
            "strateji yol xəritəsi elm təhsil",
        ),
        (
            "en",
            "roadmap.html",
            "Strategic roadmap",
            "Strategic proposals for science and education from Forum 2024 participants.",
            "🗺️",
            "strategic roadmap science education",
        ),
    ):
        path = ROOT / lang / "forum" / "2024" / "index.html"
        text = path.read_text(encoding="utf-8")
        if href in text and "page-card" in text:
            continue
        card = f"""
<a class="page-card" data-title="{esc(tags)}" href="{href}">
<div class="card-icon-wrap" aria-hidden="true">{icon}</div>
<div class="card-body">
<h3 class="card-title">{esc(title)}</h3>
<div class="card-desc">{esc(desc)}</div>
<div class="card-footer"><span class="card-tag">{"Oxu" if lang == "az" else "Read"}</span></div>
</div>
</a>
"""
        marker = '<a class="page-card" data-title="Alimlər kataloqu profillər"'
        en_marker = '<a class="page-card" data-title="Scientists directory profiles"'
        insert_before = marker if lang == "az" else en_marker
        if insert_before not in text:
            insert_before = "</section>"
            text = text.replace(
                "</section>\n<p class=\"search-empty\"",
                card + "</section>\n<p class=\"search-empty\"",
                1,
            )
        else:
            text = text.replace(insert_before, card + insert_before, 1)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"updated {path.relative_to(ROOT)}")


def build() -> None:
    doc = Document(str(DOCX))
    data = parse_docx(doc)
    OUT_AZ.parent.mkdir(parents=True, exist_ok=True)
    OUT_AZ.write_text(page_html(data, lang="az"), encoding="utf-8", newline="\n")
    OUT_EN.write_text(page_html(data, lang="en"), encoding="utf-8", newline="\n")
    print(f"wrote {OUT_AZ.relative_to(ROOT)} ({len(data['sections'])} sections)")
    print(f"wrote {OUT_EN.relative_to(ROOT)}")
    patch_routes()
    patch_nav()
    patch_ui()
    patch_forum_css()
    patch_search_index_loader()
    patch_hub_cards()


if __name__ == "__main__":
    build()
