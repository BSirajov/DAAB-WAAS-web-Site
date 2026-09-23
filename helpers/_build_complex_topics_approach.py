"""Build AZ/EN complex-topics-approach.html from the Word extracts."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(r"C:\dev\DAAB-WAAS-web-Site")
TMP = Path(r"C:\Users\BSira\AppData\Local\Temp")

HEADING_IDS = {
    "sənədin məqsədi": "purpose",
    "purpose of this document": "purpose",
    "sənədin statusu": "status",
    "status of this document": "status",
    "oxucu üçün istiqamət": "how-to-read",
    "how to read this document": "how-to-read",
    "müəllif və əlaqə məlumatları": "appendix-a-author",
    "author and contact details": "appendix-a-author",
    "təqdim edilən iş haqqında məlumat": "appendix-a-work",
    "information about the submitted work": "appendix-a-work",
}

SKIP_TITLES = {
    "mündəricat",
    "contents",
    "informatika və ikt müsabiqəsinin təşkili və iştirak qaydaları",
    "organisation of the informatics and ict competition and the rules of participation",
    "sistemləşdirilmiş konsepsiya və icra üzrə işçi sənəd",
    "working document: structured concept and delivery",
}

INTRO_IDS = {"purpose", "status", "how-to-read"}

CHAPTER_RE = re.compile(r"^(\d+)\s+\S")
SECTION_RE = re.compile(r"^(\d+)\.(\d+)\b")
APPENDIX_RE = re.compile(r"^(?:Əlavə|Appendix)\s+([A-G])\b", re.I)
FORM_LINE_RE = re.compile(r"^(.+?):\s*_{3,}\s*$")
BLANK_RE = re.compile(r"^_{8,}$")
EDITORIAL_RE = re.compile(r"^(Editorial recommendation|Redaksiya tövsiyəsi)\b", re.I)
PROPOSAL_RE = re.compile(
    r"(not an approved regulation|təsdiqlənmiş Əsasnamə deyil|"
    r"working proposal|işçi təklif|"
    r"have not been decided|müəyyən edilməyib|"
    r"It is not known|məlum deyil|"
    r"not approved|təsdiqlənmiş təqvim deyil|"
    r"working sample|işçi nümunə|"
    r"working text|işçi status)",
    re.I,
)
FUNDING_RE = re.compile(
    r"(budget|prize fund|financial support|material prize|cash prize|"
    r"büdcə|mükafat fond|maliyyə|maddi mükafat|pul mükafat|sponsor gəliri)",
    re.I,
)

UI = {
    "az": {
        "lang": "az",
        "locale": "az_AZ",
        "alt_locale": "en_US",
        "site": "DAAB",
        "title": "DAAB — İnformatika və İKT müsabiqəsinin təşkili və iştirak qaydaları",
        "description": "Complex Topics, Clear Explanations müsabiqəsinin sistemləşdirilmiş konsepsiya və icra üzrə işçi sənədi. Təsdiqlənmiş Əsasnamə deyil; büdcə və maliyyə dəstəyi müəyyən edilməyib.",
        "h1_lead": "İşçi",
        "h1_span": "sənəd",
        "subtitle": "İnformatika və İKT müsabiqəsinin təşkili və iştirak qaydaları",
        "panel_title": "Sənədin statusu",
        "panel_lead": "Bu mətn təsdiqlənmiş Əsasnamə deyil. Tarixlər, qiymətləndirmə hədləri və prosedurlar DAAB-ın nəzərdən keçirməsi üçün işçi təkliflərdir. Büdcə və maliyyə mənbələri müəyyən edilməyib; maliyyə dəstəyinin və maddi mükafatların mümkünlüyü məlum deyil.",
        "skip": "Məzmuna keç",
        "nav_aria": "Əsas naviqasiya",
        "menu": "Menyunu aç",
        "home_title": "Ana səhifə",
        "home_aria": "DAAB ana səhifə",
        "brand1": "Dünya Azərbaycanlı",
        "brand2": "Alimlər Birliyi",
        "logo_alt": "DAAB Logo",
        "hero_panel": "Sənədin qısa xülasəsi",
        "toc": "Mündəricat",
        "toc_aria": "Bu sənədin bölmələri",
        "toc_toggle": "Mündəricatı aç və ya bağla",
        "related": "Açıq müsabiqə dəvəti",
        "related_aria": "Müsabiqə flayerinə keçid",
        "org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "contact": "Əlaqə",
        "address": "Ünvan",
        "address_html": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə",
        "leadership": "Rəhbərlik",
        "leader_html": "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru",
        "legal_aria": "Hüquqi sənədlər və saytın xəritəsi",
        "privacy": "Məxfilik bildirişi",
        "terms": "İstifadə şərtləri",
        "cookies": "Kuki siyasəti",
        "legal": "Hüquqi rekvizitlər",
        "sitemap": "Saytın xəritəsi",
        "feedback": "Rəy bildirin",
        "copy": "© 2026 DAAB — Bütün hüquqlar qorunur",
    },
    "en": {
        "lang": "en",
        "locale": "en_US",
        "alt_locale": "az_AZ",
        "site": "WAAS",
        "title": "WAAS — Organisation of the informatics and ICT competition and the rules of participation",
        "description": "Working document for the Complex Topics, Clear Explanations competition: structured concept and delivery. This text is not an approved regulation. The budget and sources of funding have not been decided.",
        "h1_lead": "Working",
        "h1_span": "document",
        "subtitle": "Organisation of the informatics and ICT competition and the rules of participation",
        "panel_title": "Status of this document",
        "panel_lead": "This text is not an approved regulation. Dates, scoring thresholds and procedures are working proposals for WAAS to review. The budget and sources of funding have not been decided; it is not known whether financial support or material prizes will be possible.",
        "skip": "Skip to content",
        "nav_aria": "Main navigation",
        "menu": "Open menu",
        "home_title": "Home page",
        "home_aria": "WAAS home",
        "brand1": "World Association of",
        "brand2": "Azerbaijani Scientists",
        "logo_alt": "WAAS Logo",
        "hero_panel": "Document summary",
        "toc": "Contents",
        "toc_aria": "Sections of this document",
        "toc_toggle": "Toggle contents menu",
        "related": "Open competition invitation",
        "related_aria": "Link to the competition flyer",
        "org": "World Association of Azerbaijani Scientists",
        "contact": "Contact",
        "address": "Address",
        "address_html": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye",
        "leadership": "Leadership",
        "leader_html": "<strong>Prof. Dr. Messoud Efendiyev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Distinguished Professor",
        "legal_aria": "Legal documents and sitemap",
        "privacy": "Privacy notice",
        "terms": "Terms of use",
        "cookies": "Cookie policy",
        "legal": "Legal notice (Imprint)",
        "sitemap": "Sitemap",
        "feedback": "Feedback",
        "copy": "© 2026 WAAS — All Rights Reserved",
    },
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def heading_id(text: str) -> str | None:
    key = re.sub(r"\s+", " ", text).strip()
    low = key.casefold()
    if low in SKIP_TITLES:
        return None
    mapped = HEADING_IDS.get(low)
    if mapped:
        return mapped
    m = APPENDIX_RE.match(key)
    if m:
        return f"appendix-{m.group(1).lower()}"
    m = SECTION_RE.match(key)
    if m:
        return f"s-{m.group(1)}-{m.group(2)}"
    m = CHAPTER_RE.match(key)
    if m:
        return f"ch-{m.group(1)}"
    return None


def heading_label(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def para_class(text: str) -> str:
    classes = []
    if EDITORIAL_RE.search(text) or text.startswith("Redaksiya tövsiyəsi"):
        classes.append("cta-note")
        classes.append("cta-note--editorial")
    elif PROPOSAL_RE.search(text):
        classes.append("cta-note")
        if FUNDING_RE.search(text):
            classes.append("cta-note--funding")
    if not classes and FUNDING_RE.search(text) and PROPOSAL_RE.search(text):
        classes.extend(["cta-note", "cta-note--funding"])
    return " ".join(classes)


def render_paragraph(text: str) -> str:
    m = FORM_LINE_RE.match(text)
    if m:
        return (
            f'<p class="cta-form-line"><span class="cta-form-label">{esc(m.group(1).strip())}</span>'
            f'<span class="cta-form-rule" role="presentation"></span></p>'
        )
    if BLANK_RE.match(text):
        return '<p class="cta-form-blank" role="presentation"></p>'
    cls = para_class(text)
    attr = f' class="{cls}"' if cls else ""
    return f"<p{attr}>{esc(text)}</p>"


def render_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    head, *body = rows
    ths = "".join(f"<th scope=\"col\">{esc(c)}</th>" for c in head)
    body_html = []
    for row in body:
        tds = "".join(f"<td>{esc(c)}</td>" for c in row)
        body_html.append(f"<tr>{tds}</tr>")
    return (
        '<div class="cta-table-wrap" tabindex="0">'
        f'<table class="cta-table"><thead><tr>{ths}</tr></thead>'
        f"<tbody>{''.join(body_html)}</tbody></table></div>"
    )


def usable_items(data: dict) -> list[dict]:
    items = []
    for item in data["items"]:
        if item["type"] == "sdt":
            continue
        if item["type"] == "table":
            items.append(item)
            continue
        text = item["text"].strip()
        if not text:
            continue
        style = (item.get("style") or "").lower()
        if style in {"title", "subtitle"}:
            continue
        if text.casefold() in SKIP_TITLES:
            continue
        hid = heading_id(text) if item.get("heading") is not None or style.startswith("heading") else None
        item = dict(item)
        item["id"] = hid
        items.append(item)
    return items


def toc_nodes(items: list[dict]) -> list[dict]:
    nodes = []
    current = None
    for item in items:
        if item["type"] != "p":
            continue
        hid = item.get("id")
        if not hid:
            continue
        node = {"id": hid, "label": heading_label(item["text"]), "children": []}
        if hid.startswith("s-") or hid.startswith("appendix-a-"):
            if current:
                current["children"].append(node)
            else:
                nodes.append(node)
        else:
            current = node
            nodes.append(node)
    return nodes


TOC_NUM_RE = re.compile(
    r"^((?:\d+(?:\.\d+)*)|(?:Appendix|Əlavə)\s+[A-G])\s+(.+)$",
    re.I,
)


def toc_link(node: dict) -> str:
    label = node["label"]
    match = TOC_NUM_RE.match(label)
    if match:
        return (
            f'<a href="#{node["id"]}">'
            f'<span class="cta-toc-num">{esc(match.group(1))}</span>'
            f'<span class="cta-toc-text">{esc(match.group(2))}</span></a>'
        )
    return (
        f'<a class="cta-toc-plain" href="#{node["id"]}">'
        f'<span class="cta-toc-text">{esc(label)}</span></a>'
    )


def render_toc(nodes: list[dict], ui: dict) -> str:
    parts = ['<nav class="cta-toc-nav">', '<ol class="cta-toc-list timeline-list">']
    for node in nodes:
        kind = "cta-toc-item"
        if node["children"]:
            kind += " cta-toc-item--branch"
        parts.append(f'<li class="{kind}">')
        parts.append(toc_link(node))
        if node["children"]:
            parts.append('<ol class="cta-toc-sub">')
            for child in node["children"]:
                parts.append(f'<li class="cta-toc-item">{toc_link(child)}</li>')
            parts.append("</ol>")
        parts.append("</li>")
    parts.append("</ol>")
    parts.append("</nav>")
    return "\n".join(parts)


def close_lists(buf: list[str], list_kind: str | None) -> str | None:
    if list_kind == "ul":
        buf.append("</ul>")
    elif list_kind == "ol":
        buf.append("</ol>")
    return None


def render_body(items: list[dict]) -> str:
    out: list[str] = []
    in_card = False
    in_sub = False
    list_kind = None

    def ensure_card(hid: str, title: str, level: str) -> None:
        nonlocal in_card, in_sub, list_kind
        list_kind = close_lists(out, list_kind)
        if level == "h2":
            if in_sub:
                out.append("</section>")
                in_sub = False
            if in_card:
                out.append("</div></section>")
            out.append(f'<section class="cta-card" id="{hid}">')
            out.append(f"<h2>{esc(title)}</h2>")
            out.append('<div class="cta-card-body">')
            in_card = True
        else:
            if not in_card:
                out.append('<section class="cta-card">')
                out.append('<div class="cta-card-body">')
                in_card = True
            if in_sub:
                out.append("</section>")
            out.append(f'<section class="cta-sub" id="{hid}">')
            out.append(f"<h3>{esc(title)}</h3>")
            in_sub = True

    for item in items:
        if item["type"] == "table":
            list_kind = close_lists(out, list_kind)
            out.append(render_table(item["rows"]))
            continue
        text = item["text"].strip()
        hid = item.get("id")
        is_heading = bool(hid) or (item.get("heading") is not None and heading_id(text))
        if is_heading and hid:
            level = "h2" if (hid in INTRO_IDS or hid.startswith("ch-") or hid.startswith("appendix-") and not hid.startswith("appendix-a-")) else "h3"
            if hid.startswith("appendix-") and hid not in {"appendix-a-author", "appendix-a-work"}:
                level = "h2"
            ensure_card(hid, heading_label(text), level)
            continue
        style = item.get("style") or ""
        if item.get("list") or style.startswith("List"):
            want = "ol" if "Number" in style else "ul"
            if list_kind != want:
                list_kind = close_lists(out, list_kind)
                out.append(f"<{want}>")
                list_kind = want
            out.append(f"<li>{esc(text)}</li>")
            continue
        list_kind = close_lists(out, list_kind)
        out.append(render_paragraph(text))

    list_kind = close_lists(out, list_kind)
    if in_sub:
        out.append("</section>")
    if in_card:
        out.append("</div></section>")
    return "\n".join(out)


def page_html(lang: str, items: list[dict]) -> str:
    ui = UI[lang]
    other = "en" if lang == "az" else "az"
    nodes = toc_nodes(items)
    body = render_body(items)
    return f"""<!DOCTYPE html>
<html lang="{ui['lang']}" data-daab-lang="{ui['lang']}" data-daab-asset-root="../" data-daab-page-id="complex-topics-approach" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(ui['title'])}</title>
<meta name="description" content="{esc(ui['description'])}"/>
<!-- daab-seo -->
<link rel="icon" href="../images/daab-favicon.png" type="image/png"/>
<link rel="apple-touch-icon" href="../images/daab-favicon.png"/>
<link rel="canonical" href="https://daab-waas.com/{lang}/complex-topics-approach.html"/>
<link rel="alternate" hreflang="az" href="https://daab-waas.com/az/complex-topics-approach.html"/>
<link rel="alternate" hreflang="en" href="https://daab-waas.com/en/complex-topics-approach.html"/>
<link rel="alternate" hreflang="x-default" href="https://daab-waas.com/az/complex-topics-approach.html"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{ui['site']}"/>
<meta property="og:title" content="{esc(ui['title'])}"/>
<meta property="og:description" content="{esc(ui['description'])}"/>
<meta property="og:url" content="https://daab-waas.com/{lang}/complex-topics-approach.html"/>
<meta property="og:image" content="https://daab-waas.com/images/daab-logo.png"/>
<meta property="og:locale" content="{ui['locale']}"/>
<meta property="og:locale:alternate" content="{ui['alt_locale']}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{esc(ui['title'])}"/>
<meta name="twitter:description" content="{esc(ui['description'])}"/>
<meta name="twitter:image" content="https://daab-waas.com/images/daab-logo.png"/>
<!-- /daab-seo -->
<link href="../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../css/daab-common.css?v=101" rel="stylesheet"/>
<link href="../css/daab-perf.css?v=2" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=14" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=2" rel="stylesheet"/>
<link href="../css/daab-search.css?v=10" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=4" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=14" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=79" rel="stylesheet"/>
<link href="../css/daab-sidebar-widget.css?v=6" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../css/daab-complex-topics-approach.css?v=7" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-perf.js?v=4" defer></script>
<script src="../js/daab-sticky-chrome.js?v=3" defer></script>
<script src="../js/daab-back-to-top.js?v=5" defer></script>
<script src="../js/daab-i18n.js?v=65" defer></script>
<script src="../js/daab-lang-position.js?v=14" defer></script>
<script src="../js/daab-design-tokens.js?v=2" defer></script>
<script src="../js/daab-nav.js?v=34" defer></script>
<script src="../js/daab-primary-nav.js?v=67" defer></script>
<script src="../js/daab-breadcrumbs.js?v=57" defer></script>
<script src="../js/daab-shell.js?v=19" defer></script>
<script src="../js/daab-page-subtitle.js?v=2" defer></script>
<script src="../js/daab-search.js?v=17" defer></script>
<script src="../js/daab-analytics.js?v=7" defer></script>
<script src="../js/daab-sidebar-spy.js?v=1" defer></script>
<script src="../js/daab-sidebar-timeline.js?v=7" defer></script>
</head>
<body class="cta-page">
<a class="skip" href="#content">{esc(ui['skip'])}</a>
<nav aria-label="{esc(ui['nav_aria'])}" class="nav-strip">
<div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="{esc(ui['menu'])}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a title="{esc(ui['home_title'])}" aria-label="{esc(ui['home_aria'])}" href="index.html">
<img src="../images/daab-logo.png" class="nav-brand-logo" alt="{esc(ui['logo_alt'])}"></a></div>
<a aria-label="{esc(ui['home_aria'])}" class="nav-brand" href="index.html">
<span class="nav-brand-text"><span class="nav-brand-line">{esc(ui['brand1'])}</span><span class="nav-brand-line">{esc(ui['brand2'])}</span></span></a>
<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div></div></nav>
<header class="hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1 aria-describedby="page-hero-subtitle">{esc(ui['h1_lead'])} <span>{esc(ui['h1_span'])}</span></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(ui['subtitle'])}</p>
</section>
<aside aria-label="{esc(ui['hero_panel'])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(ui['panel_title'])}</h2>
<div class="panel-copy">
<p class="panel-copy-lead">{esc(ui['panel_lead'])}</p>
</div>
</div>
</aside>
</div>
</header>
<main class="main" id="content">
<div class="cta-layout">
<aside class="cta-toc sidebar" aria-label="{esc(ui['toc_aria'])}">
<div class="sidebar-widget" id="ctaTocWidget">
<div class="widget-head">
<h2 class="cta-toc-title" id="ctaTocHeading"><span aria-hidden="true">📄</span> {esc(ui['toc'])}</h2>
<button aria-controls="ctaTocMenu" aria-expanded="false" aria-label="{esc(ui['toc_toggle'])}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button>
</div>
<div class="widget-body" id="ctaTocMenu">
{render_toc(nodes, ui)}
</div>
</div>
</aside>
<div class="cta-stack">
{body}
</div>
</div>
</main>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(ui['org'])}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(ui['contact'])}</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(ui['address'])}</h4><p class="footer-address">{ui['address_html']}</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(ui['leadership'])}</h4><p class="footer-leader">{ui['leader_html']}</p></div>
</div>
</div>
<div class="footer-bottom"><nav class="footer-legal-links" aria-label="{esc(ui['legal_aria'])}"><a href="/{lang}/feedback.html">{esc(ui['feedback'])}</a><a href="/{lang}/privacy.html#page-title">{esc(ui['privacy'])}</a><a href="/{lang}/terms.html#page-title">{esc(ui['terms'])}</a><a href="/{lang}/cookies.html#page-title">{esc(ui['cookies'])}</a><a href="/{lang}/legal-notice.html#page-title">{esc(ui['legal'])}</a><a href="/{lang}/sitemap.html#page-title">{esc(ui['sitemap'])}</a></nav><div class="footer-copy">{esc(ui['copy'])}</div></div>
</footer>
</body>
</html>
"""


def collect_plain(items: list[dict]) -> list[str]:
    texts = []
    for item in items:
        if item["type"] == "table":
            for row in item["rows"]:
                texts.extend(c for c in row if c)
        else:
            texts.append(item["text"].strip())
    return texts


def main() -> None:
    az = json.loads((TMP / "ctce_az.json").read_text(encoding="utf-8"))
    en = json.loads((TMP / "ctce_en.json").read_text(encoding="utf-8"))
    az_items = usable_items(az)
    en_items = usable_items(en)
    az_ids = [i.get("id") for i in az_items if i.get("id")]
    en_ids = [i.get("id") for i in en_items if i.get("id")]
    if az_ids != en_ids:
        raise SystemExit(f"Heading ID mismatch\nAZ {az_ids}\nEN {en_ids}")
    (ROOT / "az" / "complex-topics-approach.html").write_text(
        page_html("az", az_items), encoding="utf-8", newline="\n"
    )
    (ROOT / "en" / "complex-topics-approach.html").write_text(
        page_html("en", en_items), encoding="utf-8", newline="\n"
    )
    print("ids", len(en_ids), en_ids)
    print("az items", len(az_items), "en items", len(en_items))
    print("az texts", len(collect_plain(az_items)), "en texts", len(collect_plain(en_items)))


if __name__ == "__main__":
    main()
