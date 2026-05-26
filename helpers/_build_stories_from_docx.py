#!/usr/bin/env python3
"""Build az/en forum/2024/stories.html from forum_2024/Hekayələr.docx."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _embed_static_nav import forum_nav_strip  # noqa: E402
from forum_en_common import FORUM_FOOTER_EN  # noqa: E402
from forum_en_stories import STORIES_EN  # noqa: E402

DOCX = ROOT / "forum_2024" / "Hekayələr.docx"
OUT_AZ = ROOT / "az" / "forum" / "2024" / "stories.html"
OUT_EN = ROOT / "en" / "forum" / "2024" / "stories.html"
ASSET = "../../../"
PAGE_ID = "forum-bagli-hekayeler"

SECTION_HEADERS = ("NUR", "VƏTƏN HİSSLƏRİ", "CIDIR DÜZÜ", "XƏDİCƏ")
SECTION_IDS = {
    "NUR": "nur",
    "VƏTƏN HİSSLƏRİ": "veten-hissleri",
    "CIDIR DÜZÜ": "cidir-duzu",
    "XƏDİCƏ": "xedice",
}
SECTION_IMAGES = {
    "nur": "NUR.jpg",
    "veten-hissleri": "VƏTƏN HİSSLƏRİ.jpg",
    "cidir-duzu": "CIDIR DÜZÜ.jpg",
    "xedice": "XƏDİCƏ.jpg",
}

SIDEBAR_SCRIPT = f'<script src="{ASSET}js/daab-sidebar-timeline.js?v=1" defer></script>'


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def norm(text: str) -> str:
    return text.replace("\r", "").replace("\xa0", " ").strip()


def parse_docx(doc: Document) -> dict:
    lines = [norm(p.text) for p in doc.paragraphs if norm(p.text)]
    title = lines[0] if lines else ""
    sections: list[dict] = []
    current: dict | None = None

    for line in lines[1:]:
        if line in SECTION_HEADERS:
            if current:
                sections.append(current)
            current = {
                "title": line,
                "id": SECTION_IDS[line],
                "paragraphs": [],
            }
            continue
        if current is not None:
            current["paragraphs"].append(line)

    if current:
        sections.append(current)

    return {"title": title, "sections": sections}


def is_pull_quote(line: str, next_line: str | None) -> bool:
    """Blockquote only for a quoted passage with a separate — attribution line."""
    if not line.startswith('"'):
        return False
    if re.search(r'["\u201d],\s*[-–]\s*dey', line, re.I):
        return False
    if " – deyə" in line or " - deyə" in line.lower():
        return False
    return bool(next_line and next_line.startswith("— "))


def paras_to_html(paragraphs: list[str]) -> str:
    parts: list[str] = []
    i = 0
    while i < len(paragraphs):
        line = paragraphs[i]
        nxt = paragraphs[i + 1] if i + 1 < len(paragraphs) else None
        if is_pull_quote(line, nxt):
            quote_text = line.strip().strip('"').strip()
            cite = nxt or ""
            i += 2
            block = f'<blockquote class="card-quote"><p>{esc(quote_text)}</p>'
            if cite:
                block += f"<footer>{esc(cite)}</footer>"
            block += "</blockquote>"
            parts.append(block)
            continue
        parts.append(f'<p class="card-text">{esc(line)}</p>')
        i += 1
    return "\n".join(parts)


def en_paras_to_html(paragraphs: list[dict]) -> str:
    parts: list[str] = []
    for item in paragraphs:
        if item["type"] == "quote":
            block = f'<blockquote class="card-quote"><p>{esc(item["text"])}</p>'
            if item.get("cite"):
                block += f'<footer>{esc(item["cite"])}</footer>'
            block += "</blockquote>"
            parts.append(block)
        else:
            parts.append(f'<p class="card-text">{esc(item["text"])}</p>')
    return "\n".join(parts)


def figure_html(section_id: str, alt: str) -> str:
    img = SECTION_IMAGES.get(section_id)
    if not img:
        return ""
    compact = " forum-story-figure--half" if section_id == "veten-hissleri" else ""
    return (
        f'<figure class="card-gallery single forum-story-figure{compact}">'
        f'<img src="{ASSET}images/forum/{esc(img)}" alt="{esc(alt)}" width="900" height="520" '
        f'loading="lazy" decoding="async"/>'
        f'<figcaption class="forum-story-caption">{esc(alt)}</figcaption>'
        f"</figure>"
    )


def story_card(section: dict, *, lang: str) -> str:
    if lang == "en":
        en_sec = next(s for s in STORIES_EN["sections"] if s["id"] == section["id"])
        title = en_sec["title"]
        body = en_paras_to_html(en_sec["paragraphs"])
    else:
        title = section["title"]
        body = paras_to_html(section["paragraphs"])

    fig = figure_html(section["id"], title)
    return f"""
<article class="news-card forum-story-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(title)}</h2>
</div>
<div class="card-body">
{fig}
{body}
</div>
</article>"""


def toc_items(sections: list[dict], *, lang: str) -> str:
    parts: list[str] = []
    for sec in sections:
        if lang == "en":
            title = next(s["title"] for s in STORIES_EN["sections"] if s["id"] == sec["id"])
        else:
            title = sec["title"]
        parts.append(f'<li><a href="#{esc(sec["id"])}">{esc(title)}</a></li>')
    return "\n".join(parts)


def page_html(data: dict, *, lang: str) -> str:
    if lang == "en":
        meta = STORIES_EN
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
        panel_aria = "Forum-related stories summary"
        doc_lead = meta["doc_title"]
    else:
        hero_h1 = "Forumla <span>bağlı hekayələr</span>"
        panel_title = "Nur, vətən və yaddaş"
        panel_copy = (
            "Eldar Əhədovun şəxsi ədəbi yazıları — forum təəssüratları, Qarabağ səfəri və "
            "ömürlük xatirəyə çevrilən görüşlər."
        )
        breadcrumb = "Forumla bağlı hekayələr"
        sidebar_label = "📖 Forumla bağlı hekayələr"
        sidebar_aria = "Forumla bağlı hekayələr menyusunu aç"
        page_title = "Forumla bağlı hekayələr — DAAB"
        meta_desc = (
            "Eldar Əhədovun Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu haqqında ədəbi yazıları."
        )
        skip = "Məzmuna keç"
        bc_home = "Ana səhifə"
        bc_activities = "Fəaliyyətimiz"
        bc_forum = "Forum 2024"
        footer_brand = "Dünya Azərbaycanlı Alimlər Birliyi"
        footer_contact = "Əlaqə"
        footer_address_title = "Ünvan"
        footer_leadership = "Rəhbərlik"
        footer_rights = "© 2026 DAAB / WAAS — All Rights Reserved"
        bc_aria = "Səhifə yolu"
        panel_aria = "Forumla bağlı hekayələr haqqında qısa məlumat"
        doc_lead = data["title"]

    cards = "".join(story_card(s, lang=lang) for s in data["sections"])
    toc = toc_items(data["sections"], lang=lang)
    nav = forum_nav_strip(lang, active_nav_id="forum-2024")

    if lang == "en":
        footer_html = FORUM_FOOTER_EN
    else:
        footer_html = f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(footer_brand)}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(footer_contact)}</h4><div class="footer-item">✉ <a href="mailto:bilik.birlik@gmail.com">bilik.birlik@gmail.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(footer_address_title)}</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(footer_leadership)}</h4><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Germany — James D. Murray Distinguished Professor</p></div>
</div>
</div>
<div class="footer-bottom">{esc(footer_rights)}</div>
</footer>"""

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{ASSET}" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(meta_desc)}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v=18" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=10" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=10" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=6" defer></script>
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
<p class="hero-doc-lead">{esc(doc_lead)}</p>
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
<div class="widget-head"><span>{sidebar_label}</span><button aria-controls="hekayelerTOC" aria-expanded="false" aria-label="{esc(sidebar_aria)}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="hekayelerTOC">
{toc}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cards}
</main>
</div>
{footer_html}
{SIDEBAR_SCRIPT}
</body>
</html>
"""


def main() -> None:
    data = parse_docx(Document(DOCX))
    OUT_AZ.parent.mkdir(parents=True, exist_ok=True)
    OUT_AZ.write_text(page_html(data, lang="az"), encoding="utf-8", newline="\n")
    OUT_EN.write_text(page_html(data, lang="en"), encoding="utf-8", newline="\n")
    print(f"wrote {OUT_AZ.relative_to(ROOT)}")
    print(f"wrote {OUT_EN.relative_to(ROOT)} ({len(data['sections'])} stories)")


if __name__ == "__main__":
    main()
