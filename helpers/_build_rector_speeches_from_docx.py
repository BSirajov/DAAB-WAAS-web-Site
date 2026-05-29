#!/usr/bin/env python3
"""Build forum speech pages from forum_2024 rectors docx.

- az|en/forum/2024/rector_speeches.html — university rectors (excludes ANAS leadership)
- az|en/forum/2024/anas_leadership_speeches.html — İsa Həbibbəyli & Rasim Əliquliyev
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DOCX = ROOT / "forum_2024" / "AZƏRBAYCAN UNİVERSİTETLƏRİNİN REKTORLARININ NİTQLƏRİ.docx"
ASSET = "../../../"
SIDEBAR_SCRIPT = f'<script src="{ASSET}js/daab-sidebar-timeline.js?v=2" defer></script>'

ANAS_SECTION_IDS = frozenset({"isa-hebibbeyli", "rasim-eliquliyev"})

from _embed_static_nav import forum_nav_strip  # noqa: E402
from forum_en_common import FORUM_FOOTER_EN  # noqa: E402

AZ_SLUG = str.maketrans(
    {
        "Ə": "e",
        "ə": "e",
        "İ": "i",
        "I": "i",
        "Ö": "o",
        "ö": "o",
        "Ü": "u",
        "ü": "u",
        "Ş": "s",
        "ş": "s",
        "Ç": "c",
        "ç": "c",
        "Ğ": "g",
        "ğ": "g",
    }
)

SIGNOFF_RE = re.compile(
    r"^(Təşəkkür edirəm!|Hörmətlə,?$|Gələn forumda görüşənədək!|P\.S\.)",
    re.I,
)

# Stray roadmap heading sometimes appended after the last rector speech in the docx.
ROADMAP_LEAK_RE = re.compile(
    r"^DİASPOR HƏRƏKATINDA MÜHÜM İSTİQAMƏT",
    re.I,
)

PAGE_SPECS = {
    "rector": {
        "out_az": ROOT / "az" / "forum" / "2024" / "rector_speeches.html",
        "out_en": ROOT / "en" / "forum" / "2024" / "rector_speeches.html",
        "page_id": "forum-rector-speeches",
        "filter": lambda sid: sid not in ANAS_SECTION_IDS,
        "toc_id": "rectorTOC",
        "copy": {
            "az": {
                "title": "Rektorların nitqləri — DAAB",
                "description": (
                    "Forum 2024 — Azərbaycan universitet rektorlarının nitqləri."
                ),
                "breadcrumb": "Rektorların nitqləri",
                "hero_h1": "Rektorların <span>nitqləri</span>",
                "hero_subtitle": "Azərbaycan universitet rektorlarının Forum 2024-dəki nitqləri",
                "panel_aria": "Rektor nitqləri haqqında qısa məlumat",
                "panel_title": "Rektorların nitqləri",
                "panel_copy": (
                    "Bu səhifədə Forum 2024 çərçivəsində Azərbaycan universitet "
                    "rektorlarının və Rəssamlıq Akademiyası rəhbərinin nitqləri "
                    "toplanmışdır."
                ),
                "sidebar_label": "Rektorlar",
                "sidebar_toggle": "Rektorlar siyahısını aç",
            },
            "en": {
                "title": "Rectors' speeches — WAAS",
                "description": (
                    "Forum 2024 — speeches by rectors of Azerbaijani universities."
                ),
                "breadcrumb": "Rectors' speeches",
                "hero_h1": "Rectors' <span>speeches</span>",
                "hero_subtitle": "Speeches by rectors of Azerbaijani universities at Forum 2024",
                "panel_aria": "Rectors' speeches summary",
                "panel_title": "Rectors' speeches",
                "panel_copy": (
                    "This page collects speeches delivered at Forum 2024 by rectors of "
                    "Azerbaijani universities and the Rector of the Academy of Arts."
                ),
                "sidebar_label": "Rectors",
                "sidebar_toggle": "Open rectors list",
            },
        },
    },
    "anas": {
        "out_az": ROOT / "az" / "forum" / "2024" / "anas_leadership_speeches.html",
        "out_en": ROOT / "en" / "forum" / "2024" / "anas_leadership_speeches.html",
        "page_id": "forum-anas-leadership-speeches",
        "filter": lambda sid: sid in ANAS_SECTION_IDS,
        "toc_id": "anasTOC",
        "copy": {
            "az": {
                "title": "AMEA rəhbərliyinin nitqləri — DAAB",
                "description": (
                    "Forum 2024 — Azərbaycan Milli Elmlər Akademiyasının rəhbərliyinin nitqləri."
                ),
                "breadcrumb": "AMEA rəhbərliyinin nitqləri",
                "hero_h1": "AMEA rəhbərliyinin <span>nitqləri</span>",
                "hero_subtitle": (
                    "Azərbaycan Milli Elmlər Akademiyasının rəhbərliyinin Forum 2024-dəki nitqləri"
                ),
                "panel_aria": "AMEA rəhbərliyinin nitqləri haqqında qısa məlumat",
                "panel_title": "AMEA rəhbərliyinin nitqləri",
                "panel_copy": (
                    "Bu səhifədə Forum 2024 çərçivəsində Azərbaycan Milli Elmlər "
                    "Akademiyasının prezidenti və vitse-prezidentinin nitqləri toplanmışdır."
                ),
                "sidebar_label": "📋 Nitqlər",
                "sidebar_toggle": "Nitqlər menyusunu aç",
            },
            "en": {
                "title": "Speeches by the ANAS Leadership — WAAS",
                "description": (
                    "Forum 2024 — speeches by leaders of the Azerbaijan National Academy of Sciences."
                ),
                "breadcrumb": "Speeches by the ANAS Leadership",
                "hero_h1": "Speeches by the <span>ANAS Leadership</span>",
                "hero_subtitle": (
                    "Speeches by leaders of the Azerbaijan National Academy of Sciences at Forum 2024"
                ),
                "panel_aria": "ANAS leadership speeches summary",
                "panel_title": "Speeches by the ANAS Leadership",
                "panel_copy": (
                    "This page collects speeches delivered at Forum 2024 by the President "
                    "and Vice-President of the Azerbaijan National Academy of Sciences."
                ),
                "sidebar_label": "📋 Speeches",
                "sidebar_toggle": "Open speeches menu",
            },
        },
    },
}

FOOTER_AZ = {
    "footer_brand": "Dünya Azərbaycanlı Alimlər Birliyi",
    "footer_contact": "Əlaqə",
    "footer_address": "Ünvan",
    "footer_leadership": "Rəhbərlik",
    "footer_chair": "DAAB İdarə Heyətinin Sədri",
    "footer_chair_name": "Prof. Dr. Məsud Əfəndiyev",
    "footer_bottom": "© 2026 DAAB / WAAS — All Rights Reserved",
}

FOOTER_EN = {
    "footer_brand": "World Association of Azerbaijani Scientists",
    "footer_contact": "Contact",
    "footer_address": "Address",
    "footer_leadership": "Leadership",
    "footer_chair": "Chair of the WAAS Board of Directors",
    "footer_chair_name": "Prof. Dr. Mesud Afandiyev",
    "footer_bottom": "© 2026 WAAS — All Rights Reserved",
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def norm(text: str) -> str:
    return text.replace("\r", "").replace("\xa0", " ").strip()


def name_slug(name: str) -> str:
    s = name.translate(AZ_SLUG).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def parse_speeches() -> list[dict]:
    doc = Document(str(DOCX))
    sections: list[dict] = []
    cur: dict | None = None

    for para in doc.paragraphs:
        text = norm(para.text)
        if not text:
            continue
        style = para.style.name if para.style else ""

        if style == "Heading 1" and "YOL XƏRİTƏSİ" in text.upper():
            break

        if style.startswith("Heading 2"):
            if cur:
                sections.append(cur)
            cur = {
                "id": name_slug(text),
                "name": text,
                "role": "",
                "blocks": [],
            }
            continue

        if not cur:
            continue

        if style.startswith("Heading 3") and not cur["role"]:
            cur["role"] = text
            continue

        if ROADMAP_LEAK_RE.match(text):
            continue

        is_list = style.startswith("List")
        cur["blocks"].append({"list": is_list, "text": text})

    if cur:
        sections.append(cur)
    return sections


def toc_item_html(section: dict, page_key: str) -> str:
    sid = esc(section["id"])
    name = esc(section["name"])
    if page_key != "rector":
        return f'<li><a href="#{sid}">{name}</a></li>'
    titles = (section.get("role") or "").strip()
    titles_html = (
        f'<span class="rector-toc-titles">{esc(titles)}</span>' if titles else ""
    )
    return (
        f'<li><a class="rector-toc-link" href="#{sid}">'
        f'<span class="rector-toc-name">{name}</span>{titles_html}</a></li>'
    )


def strip_duplicate_role_blocks(section: dict) -> None:
    """Drop a leading body paragraph that repeats the Heading 3 academic title."""
    role = (section.get("role") or "").strip()
    if not role or not section.get("blocks"):
        return
    first = section["blocks"][0]
    if first.get("list"):
        return
    if norm(first["text"]) == role:
        section["blocks"].pop(0)


def blocks_to_html(blocks: list[dict]) -> str:
    parts: list[str] = []
    list_buf: list[str] = []

    def flush_list() -> None:
        nonlocal list_buf
        if not list_buf:
            return
        items = "".join(f"<li>{esc(t)}</li>" for t in list_buf)
        parts.append(f'<ul class="content-list">{items}</ul>')
        list_buf = []

    for block in blocks:
        text = block["text"]
        if block["list"]:
            list_buf.append(text)
            continue
        flush_list()
        if SIGNOFF_RE.match(text):
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        elif text.startswith("Belə bir aforizm var:") or text.startswith('"') or text.startswith("“"):
            parts.append(f'<p class="card-quote">{esc(text)}</p>')
        else:
            parts.append(f'<p class="card-text">{esc(text)}</p>')

    flush_list()
    return "\n".join(parts)


def speech_card(section: dict) -> str:
    role_html = ""
    if section["role"]:
        role_html = (
            f'<p class="card-subtitle" role="doc-subtitle">{esc(section["role"])}</p>'
        )
    return f"""
<article class="news-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(section["name"])}</h2>
{role_html}
</div>
<div class="card-body">
{blocks_to_html(section["blocks"])}
</div>
</article>"""


def footer_html(lang: str) -> str:
    if lang == "en":
        return FORUM_FOOTER_EN
    c = FOOTER_AZ
    return f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{c["footer_brand"]}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{c["footer_contact"]}</h4><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{c["footer_address"]}</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">{c["footer_leadership"]}</h4><p class="footer-leader"><strong>{c["footer_chair_name"]}</strong><br/>{c["footer_chair"]}<br/>Germany — James D. Murray Distinguished Professor</p></div>
</div>
</div>
<div class="footer-bottom">{c["footer_bottom"]}</div>
</footer>"""


def build_html(lang: str, sections: list[dict], spec: dict, page_key: str) -> str:
    c = {**spec["copy"][lang], **(FOOTER_EN if lang == "en" else FOOTER_AZ)}
    page_id = spec["page_id"]
    toc_id = spec["toc_id"]
    nav = forum_nav_strip(lang, active_nav_id="forum-2024")
    toc_items = "".join(toc_item_html(s, page_key) for s in sections)
    cards = "\n".join(speech_card(s) for s in sections)

    if lang == "az":
        crumbs = (
            '<a href="../../index.html">Ana səhifə</a><span aria-hidden="true">›</span>'
            '<a href="../../activities.html">Fəaliyyətimiz</a><span aria-hidden="true">›</span>'
            '<a href="index.html">Forum 2024</a><span aria-hidden="true">›</span>'
            f'<span class="forum-breadcrumbs-current" aria-current="page">{c["breadcrumb"]}</span>'
        )
        skip = "Məzmuna keç"
        crumb_aria = "Səhifə yolu"
    else:
        crumbs = (
            '<a href="../../index.html">Home</a><span aria-hidden="true">›</span>'
            '<a href="../../activities.html">Activities</a><span aria-hidden="true">›</span>'
            '<a href="index.html">Forum 2024</a><span aria-hidden="true">›</span>'
            f'<span class="forum-breadcrumbs-current" aria-current="page">{c["breadcrumb"]}</span>'
        )
        skip = "Skip to content"
        crumb_aria = "Breadcrumb"

    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{ASSET}" data-daab-page-id="{page_id}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(c["title"])}</title>
<meta name="description" content="{esc(c["description"])}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=40" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=4" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=19" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=7" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v=4" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v=14" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-page.css?v=3" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=7" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=3" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=17" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v=1" defer></script>
<script src="{ASSET}js/daab-nav.js?v=19" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=16" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=10" defer></script>
<script src="{ASSET}js/daab-shell.js?v=12" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v=2" defer></script>
<script src="{ASSET}js/daab-search.js?v=7" defer></script>
</head>
<body>
<a class="skip" href="#content">{skip}</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" data-daab-breadcrumbs-static="1" role="navigation" aria-label="{crumb_aria}">
{crumbs}
</div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1 aria-describedby="page-hero-subtitle">{c["hero_h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(c["hero_subtitle"])}</p>
</section>
<aside aria-label="{esc(c["panel_aria"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(c["panel_title"])}</h2>
<div class="panel-copy">{esc(c["panel_copy"])}</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head"><span>{c["sidebar_label"]}</span><button aria-controls="{toc_id}" aria-expanded="false" aria-label="{esc(c["sidebar_toggle"])}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="{toc_id}">
{toc_items}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cards}
</main>
</div>
{footer_html(lang)}
{SIDEBAR_SCRIPT}
</body>
</html>
"""


def build() -> None:
    if not DOCX.is_file():
        raise SystemExit(f"Missing source: {DOCX}")
    all_sections = parse_speeches()
    if not all_sections:
        raise SystemExit("No speech sections parsed from docx")

    for key, spec in PAGE_SPECS.items():
        sections = [s for s in all_sections if spec["filter"](s["id"])]
        if not sections:
            raise SystemExit(f"No sections for page {key}")
        for section in sections:
            strip_duplicate_role_blocks(section)

        spec["out_az"].parent.mkdir(parents=True, exist_ok=True)
        spec["out_az"].write_text(
            build_html("az", sections, spec, key), encoding="utf-8", newline="\n"
        )
        print(f"wrote {spec['out_az'].relative_to(ROOT)} ({len(sections)} speeches)")

        spec["out_en"].write_text(
            build_html("en", sections, spec, key), encoding="utf-8", newline="\n"
        )
        print(f"wrote {spec['out_en'].relative_to(ROOT)} ({len(sections)} speeches)")


if __name__ == "__main__":
    build()
