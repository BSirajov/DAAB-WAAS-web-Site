#!/usr/bin/env python3
"""Publish English Forum 2024 pages from Azerbaijani sources."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _embed_static_nav import forum_nav_strip  # noqa: E402
from forum_en_common import FORUM_FOOTER_EN, apply_shell  # noqa: E402
from forum_en_official import OFFICIAL_EN_SECTIONS  # noqa: E402
from forum_en_impressions_phrases import apply_impressions_phrases  # noqa: E402
from forum_en_presentations_phrases import (  # noqa: E402
    PRESENTATIONS_UI,
    apply_presentations_phrases,
)
from forum_en_program_map import apply_program_phrases  # noqa: E402

ASSET = "../../../"

from _build_official_from_docx import SIDEBAR_SCRIPT  # noqa: E402

EN_DIR = ROOT / "en" / "forum" / "2024"
AZ_DIR = ROOT / "az" / "forum" / "2024"

FORUM_EN_BREADCRUMB = (
    '<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Breadcrumb">'
    '<a href="../../index.html">Home</a><span aria-hidden="true">›</span>'
    '<a href="../../activities.html">Activities</a><span aria-hidden="true">›</span>'
    '<a href="index.html">Forum 2024</a><span aria-hidden="true">›</span>'
    '<span class="forum-breadcrumbs-current" aria-current="page">{current}</span></div>'
)


def _forum_en_breadcrumbs(text: str, *, current: str) -> str:
    return re.sub(
        r'<div[^>]*class="[^"]*breadcrumbs[^"]*"[^>]*>.*?</div>',
        FORUM_EN_BREADCRUMB.format(current=current),
        text,
        count=1,
        flags=re.S,
    )


def _collapse_ws(html: str) -> str:
    """Normalize whitespace so phrase keys match HTML (NBSP, double spaces)."""
    html = html.replace("\u00a0", " ")
    return re.sub(r"[ \t]{2,}", " ", html)


def _inject_en_nav(text: str) -> str:
    return re.sub(
        r'<nav aria-label="[^"]*" class="nav-strip">.*?</nav>',
        forum_nav_strip("en"),
        text,
        count=1,
        flags=re.S,
    )


def _inject_en_footer(text: str) -> str:
    return re.sub(
        r'<footer class="footer-pro">.*?</footer>',
        FORUM_FOOTER_EN,
        text,
        count=1,
        flags=re.S,
    )


def _ensure_forum_en_scripts(text: str) -> str:
    if "daab-search.css" not in text:
        text = text.replace(
            '<link href="../../../css/daab-lang.css?v=10" rel="stylesheet"/>',
            '<link href="../../../css/daab-lang.css?v=10" rel="stylesheet"/>\n'
            '<link href="../../../css/daab-search.css?v=1" rel="stylesheet"/>',
        )
    if "daab-primary-nav.js" not in text:
        text = text.replace(
            '<script src="../../../js/daab-nav.js?v=10" defer></script>',
            '<script src="../../../js/daab-nav.js?v=10" defer></script>\n'
            '<script src="../../../js/daab-primary-nav.js?v=10" defer></script>',
        )
    if "daab-section-nav.js" not in text:
        text = text.replace(
            '<script src="../../../js/daab-search.js?v=4" defer></script>',
            '<script src="../../../js/daab-search.js?v=4" defer></script>\n'
            '<script src="../../../js/daab-section-nav.js?v=6" defer></script>',
        )
    text = text.replace("daab-activities-layout.css?v=7", "daab-activities-layout.css?v=10")
    text = text.replace("daab-forum-content.css?v=12", "daab-forum-content.css?v=15")
    text = text.replace("daab-nav.js?v=9", "daab-nav.js?v=10")
    text = text.replace("daab-primary-nav.js?v=9", "daab-primary-nav.js?v=10")
    text = text.replace("daab-section-nav.js?v=5", "daab-section-nav.js?v=6")
    return text


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def paras_to_html(paras: list[str], *, quote: str = "") -> str:
    parts: list[str] = []
    if quote:
        parts.append(f'<p class="card-quote">{esc(quote)}</p>')
    for text in paras:
        if text in ("Respectfully,", "Hörmətlə,"):
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        elif len(text) < 80 and text.endswith(("2024", "Palace", "Khankendi,")):
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        elif "," in text and text.isupper() and len(text) < 120:
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        else:
            parts.append(f'<p class="card-text">{esc(text)}</p>')
    return "\n".join(parts)


def official_card(section: dict) -> str:
    lead = f'<p class="card-lead">{esc(section["subtitle"])}</p>' if section.get("subtitle") else ""
    image = ""
    if section.get("image") == "president":
        image = (
            f'<div class="card-gallery single"><img src="{ASSET}images/forum/Prezidentin_müraciəti.jpg" '
            'alt="President of the Republic of Azerbaijan Ilham Aliyev" width="900" height="520" '
            'loading="lazy" decoding="async"/></div>'
        )
    elif section.get("image") == "scientists":
        image = (
            f'<div class="card-gallery double">'
            f'<img src="{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_1.jpg" '
            'alt="Scientists\' appeal — Khankendi" loading="lazy" decoding="async"/>'
            f'<img src="{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_2.jpg" '
            'alt="Scientists\' appeal — Khankendi" loading="lazy" decoding="async"/>'
            "</div>"
        )
    body = section.get("body", [])
    signoff = section.get("signoff", [])
    quote = section.get("quote", "")
    return f"""
<article class="news-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(section["title"])}</h2>
</div>
<div class="card-body">
{image}
{lead}
{paras_to_html(body, quote=quote)}
{paras_to_html(signoff)}
</div>
</article>"""


def build_official() -> None:
    toc = "".join(f'<li><a href="#{esc(s["id"])}">{esc(s["title"])}</a></li>' for s in OFFICIAL_EN_SECTIONS)
    cards = "\n".join(official_card(s) for s in OFFICIAL_EN_SECTIONS)
    nav = forum_nav_strip("en", active_nav_id="forum-2024")
    out = f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{ASSET}" data-daab-page-id="forum-official" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Official addresses — WAAS</title>
<meta name="description" content="Forum 2024 — addresses by the President, Nobel laureates and scientists."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v=7" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v=12" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=5" defer></script>
<script src="{ASSET}js/daab-shell.js?v=11" defer></script>
<script src="{ASSET}js/daab-search.js?v=4" defer></script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Breadcrumb">
<a href="../../index.html">Home</a><span aria-hidden="true">›</span><a href="../../activities.html">Activities</a><span aria-hidden="true">›</span><a href="index.html">Forum 2024</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">Official addresses</span>
</div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>Official <span>addresses</span></h1>
</section>
<aside aria-label="Official addresses summary" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">Official addresses</h2>
<div class="panel-copy">President Ilham Aliyev's message, letters from Nobel laureates Aziz Sancar and Arye Varshavsky, and our scientists' appeal to the President.</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head"><span>📋 Addresses</span><button aria-controls="officialTOC" aria-expanded="false" aria-label="Open addresses menu" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="officialTOC">
{toc}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cards}
</main>
</div>
{FORUM_FOOTER_EN}
{SIDEBAR_SCRIPT}
</body>
</html>
"""
    path = EN_DIR / "official.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def build_program() -> None:
    src = (AZ_DIR / "program.html").read_text(encoding="utf-8")
    text = apply_shell(src)
    text = text.replace('data-daab-page-id="forum-program"', 'data-daab-page-id="forum-program"', 1)
    text = text.replace("<title>Forumun proqramı — DAAB</title>", "<title>Forum programme — WAAS</title>")
    text = text.replace(
        'aria-label="Forumun proqramı haqqında qısa məlumat"',
        'aria-label="Forum programme summary"',
    )
    text = text.replace(
        '<span class="forum-breadcrumbs-current" aria-current="page">Forumun proqramı</span>',
        '<span class="forum-breadcrumbs-current" aria-current="page">Forum programme</span>',
    )
    text = apply_program_phrases(text)
    # Ensure EN lang attrs after phrase map (some AZ fragments may remain in edge cells)
    text = re.sub(r'lang="az"', 'lang="en"', text, count=1)
    text = text.replace('data-daab-lang="az"', 'data-daab-lang="en"')
    path = EN_DIR / "program.html"
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


IMPRESSIONS_UI: dict[str, str] = {
    "Forumla bağlı <span>təəssüratlar</span>": "Forum <span>impressions</span>",
    "Forumla bağlı təəssüratlar — DAAB": "Forum impressions — WAAS",
    "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu ilə bağlı iştirakçı təəssüratları və ibrət nəticələri.": (
        "Participant impressions and reflections from the First Forum of Azerbaijani Scientists Living Abroad."
    ),
    "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu ilə bağlı alimlərimizin şəxsi düşüncələri, müşahidələri və mənəvi nəticələri.": (
        "Personal reflections, observations and lessons from our scientists on the First Forum of Azerbaijani Scientists Living Abroad."
    ),
    "Elm, vətən və həmrəylik": "Science, homeland and solidarity",
    "Bu səhifə forum iştirakçılarının elmi əməkdaşlıq, diaspor həmrəyliyi və Qarabağ səfəri ilə bağlı təəssüratlarını vahid, oxunaqlı formatda təqdim edir.": (
        "This page presents participants' impressions of scientific cooperation, diaspora solidarity and the Karabakh visit in a unified, readable academic format."
    ),
    "Bu səhifə forum iştirakçılarının elmi əməkdaşlıq, diaspora həmrəyliyi və Qarabağ səfəri ilə bağlı təəssüratlarını vahid, oxunaqlı və akademik formatda təqdim edir.": (
        "This page presents participants' impressions of scientific cooperation, diaspora solidarity and the Karabakh visit in a unified, readable academic format."
    ),
    "💬 Təəssüratlar": "💬 Impressions",
    'aria-label="Təəssüratlar menyusunu aç"': 'aria-label="Open impressions menu"',
    'aria-label="Səhifə üzrə naviqasiya"': 'aria-label="On-page navigation"',
    "Mündəricat": "Contents",
    "İştirakçı təəssüratları": "Participant impressions",
    "Mətnlər müəlliflər üzrə strukturlaşdırılıb; hər bölmənin sonunda əsas ideyanı ifadə edən qısa “İbrət nəticəsi” verilib.": (
        "Texts are structured by author; each section ends with a brief “Reflection” summarising the main idea."
    ),
    "Ümumi nəticə": "Overall summary",
    "İbrət nəticəsi": "Reflection",
    "Ümumi ibrət nəticəsi": "Overall reflection",
    "Forumla bağlı ümumi düşüncələr": "Overall reflections on the forum",
    "Afina Məmmədli Barmanbay – əlavə yekun düşüncələr": "Afina Məmmədli Barmanbay — additional closing thoughts",
    '<span id="forum-bc-tail"></span>': '<span class="forum-breadcrumbs-current" aria-current="page">Impressions</span>',
    "data-daab-page-id=\"forum-impressions\"": "data-daab-page-id=\"forum-impressions\"",
}


def build_impressions() -> None:
    src = _collapse_ws((AZ_DIR / "impressions.html").read_text(encoding="utf-8"))
    for az, en in sorted(IMPRESSIONS_UI.items(), key=lambda kv: -len(kv[0])):
        src = src.replace(az, en)
    text = apply_impressions_phrases(src)
    text = apply_shell(text)
    text = re.sub(r"<title>[^<]*</title>", "<title>Forum impressions — WAAS</title>", text, count=1)
    text = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        '<meta content="Participant impressions from the First Forum of Azerbaijani Scientists Living Abroad." name="description"/>',
        text,
        count=1,
    )
    text = _forum_en_breadcrumbs(text, current="Impressions")
    text = _inject_en_nav(text)
    text = _inject_en_footer(text)
    text = _ensure_forum_en_scripts(text)
    path = EN_DIR / "impressions.html"
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def build_presentations() -> None:
    src = _collapse_ws((AZ_DIR / "presentations.html").read_text(encoding="utf-8"))
    for az, en in sorted(PRESENTATIONS_UI.items(), key=lambda kv: -len(kv[0])):
        src = src.replace(az, en)
    text = apply_presentations_phrases(src)
    text = apply_shell(text)
    text = text.replace("<th>Azərbaycan</th>", "<th>Azerbaijan</th>")
    text = re.sub(r"<title>[^<]*</title>", "<title>Presentations — WAAS</title>", text, count=1)
    text = _forum_en_breadcrumbs(text, current="Presentations")
    text = _inject_en_nav(text)
    text = _inject_en_footer(text)
    text = _ensure_forum_en_scripts(text)
    path = EN_DIR / "presentations.html"
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")


def sync_en_index() -> None:
    """Align EN hub with current AZ hub structure and copy."""
    az = (AZ_DIR / "index.html").read_text(encoding="utf-8")
    en = (EN_DIR / "index.html").read_text(encoding="utf-8")
    # Update EN-only strings to match AZ card set without book page refs
    replacements = [
        ("Forum programme", "Forum programme"),
        (
            '<div class="panel-copy">9–11 September 2024, Baku – Khankendi – Shusha. Official addresses, programme, speeches and presentations (pp. 24–115) and participant impressions (pp. 176–203) are published in this section.</div>',
            '<div class="panel-copy">9–11 September 2024, Baku – Khankendi – Shusha. Official addresses, programme, speeches, presentations and participant impressions are published in this section.</div>',
        ),
        (
            "<p>Use the cards below to open official texts, the programme, speeches, presentations and participant impressions from the forum book.</p>",
            "<p>Use the cards below to open official addresses, the programme, speeches, presentations, impressions and the scientists directory.</p>",
        ),
        (
            '<div class="card-desc">President, Nobel laureates and scientists\' appeal (book pp. 24–28).</div>',
            '<div class="card-desc">President, Nobel laureates and scientists\' appeal.</div>',
        ),
        (
            '<div class="card-desc">9–11 September 2024 schedule (book pp. 31–35).</div>',
            '<div class="card-desc">9–11 September 2024 event schedule.</div>',
        ),
        (
            '<div class="card-desc">State, university and diaspora addresses (book pp. 36–69).</div>',
            '<div class="card-desc">State, university and diaspora addresses.</div>',
        ),
        (
            '<div class="card-desc">Scientific presentations at the forum (book pp. 70–114).</div>',
            '<div class="card-desc">Scientific presentations delivered at the forum.</div>',
        ),
        (
            '<div class="card-desc">Participants\' personal impressions (book pp. 176–203).</div>',
            '<div class="card-desc">Participants\' personal impressions.</div>',
        ),
        ("<h2 class=\"panel-title\">First Forum — book archive</h2>", "<h2 class=\"panel-title\">Forum 2024 information</h2>"),
        ('data-title="Forum programme schedule"', 'data-title="Forum programme schedule September"'),
    ]
    for old, new in replacements:
        en = en.replace(old, new)
    (EN_DIR / "index.html").write_text(en, encoding="utf-8", newline="\n")
    print("updated en/forum/2024/index.html")


def main() -> None:
    build_official()
    build_program()
    build_impressions()
    build_presentations()
    sync_en_index()
    print("Done. Run: python helpers/_embed_static_nav.py && python helpers/_build_search_index.py && python helpers/_validate_site.py")


if __name__ == "__main__":
    main()
