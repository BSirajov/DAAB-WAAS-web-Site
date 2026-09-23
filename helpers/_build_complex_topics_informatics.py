"""Build AZ/EN topic-selection guide pages for the competition section."""
from __future__ import annotations

from html import escape as esc
from pathlib import Path

from _informatics_guide_content import TOC, render_body

ROOT = Path(__file__).resolve().parents[1]
PAGE_ID = "complex-topics-informatics"
FILE = "complex-topics-informatics.html"

UI = {
    "en": {
        "lang": "en",
        "site": "WAAS",
        "title": "WAAS — Guide to topic selection",
        "description": "A working guide to popular and difficult informatics topics for Complex Topics, Clear Explanations. It combines curriculum priorities, current interest, teaching research and examples, and it marks where the sources differ.",
        "locale": "en_US",
        "alt_locale": "az_AZ",
        "skip": "Skip to content",
        "nav_aria": "Main navigation",
        "menu": "Open menu",
        "home_title": "Home page",
        "home_aria": "WAAS home",
        "logo_alt": "WAAS Logo",
        "brand1": "World Association of",
        "brand2": "Azerbaijani Scientists",
        "h1": "Guide to <span>topic selection</span>",
        "subtitle": "A working guide for “Complex Topics, Clear Explanations”",
        "panel_aria": "Page summary",
        "panel_title": "What this guide is",
        "panel_lead": "This page is a working guide: it gathers curriculum priorities, learner interest, documented teaching difficulties and examples, and it marks places where the source documents differ.",
        "toc_aria": "Sections of this page",
        "toc_title": "Contents",
        "toc_toggle": "Toggle contents menu",
        "toc_open": "Open contents",
        "toc_label": "Contents",
        "footer_brand": "World Association of Azerbaijani Scientists",
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
        "related_flyer": "Open competition invitation",
        "related_approach": "Organisation of competition",
    },
    "az": {
        "lang": "az",
        "site": "DAAB",
        "title": "DAAB — Mövzu seçimi üzrə bələdçi",
        "description": "“Çətin mövzu, aydın izah” müsabiqəsi üçün informatikanın populyar və çətin mövzuları üzrə işçi bələdçi. Səhifə tədris prioritetlərini, mövcud marağı, tədris tədqiqatlarını və nümunələri birləşdirir, mənbələr fərqlənəndə isə fərqi göstərir.",
        "locale": "az_AZ",
        "alt_locale": "en_US",
        "skip": "Məzmuna keç",
        "nav_aria": "Əsas naviqasiya",
        "menu": "Menyunu aç",
        "home_title": "Ana səhifə",
        "home_aria": "DAAB ana səhifə",
        "logo_alt": "DAAB loqosu",
        "brand1": "Dünya Azərbaycanlı",
        "brand2": "Alimlər Birliyi",
        "h1": "Mövzu seçimi üzrə <span>bələdçi</span>",
        "subtitle": "“Çətin mövzu, aydın izah” müsabiqəsi üçün işçi bələdçi",
        "panel_aria": "Səhifənin qısa xülasəsi",
        "panel_title": "Bu bələdçi nədir",
        "panel_lead": "Bu səhifə işçi bələdçidir: tədris prioritetlərini, öyrənənlərin marağını, sənədləşdirilmiş çətinlikləri və nümunələri bir yerə toplayır, mənbələr fərqlənəndə isə fərqi gizlətmir.",
        "toc_aria": "Bu səhifənin bölmələri",
        "toc_title": "Mündəricat",
        "toc_toggle": "Mündəricat menyusunu aç",
        "toc_open": "Mündəricatı aç",
        "toc_label": "Mündəricat",
        "footer_brand": "Dünya Azərbaycanlı Alimlər Birliyi",
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
        "related_flyer": "Açıq müsabiqə dəvəti",
        "related_approach": "Müsabiqənin təşkili",
    },
}

def body(lang: str) -> str:
    return render_body(lang)


def toc_html(lang: str) -> str:
    items = []
    for sid, title, children in TOC:
        label = esc(title[lang])
        if children:
            subs = "".join(
                f'<li class="cta-toc-item"><a href="#{cid}"><span class="cta-toc-text">{esc(ct[lang])}</span></a></li>'
                for cid, ct in children
            )
            items.append(
                f'<li class="cta-toc-item cta-toc-item--branch"><a href="#{sid}"><span class="cta-toc-text">{label}</span></a>'
                f'<ol class="cta-toc-sub">{subs}</ol></li>'
            )
        else:
            items.append(
                f'<li class="cta-toc-item"><a class="cta-toc-plain" href="#{sid}"><span class="cta-toc-text">{label}</span></a></li>'
            )
    return "\n".join(items)


def page_html(lang: str) -> str:
    ui = UI[lang]
    return f"""<!DOCTYPE html>
<html data-daab-print="1" lang="{ui['lang']}" data-daab-lang="{ui['lang']}" data-daab-asset-root="../" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(ui['title'])}</title>
<meta name="description" content="{esc(ui['description'])}"/>
<!-- daab-seo -->
<link rel="icon" href="../images/daab-favicon.png" type="image/png"/>
<link rel="apple-touch-icon" href="../images/daab-favicon.png"/>
<link rel="canonical" href="https://daab-waas.com/{lang}/{FILE}"/>
<link rel="alternate" hreflang="az" href="https://daab-waas.com/az/{FILE}"/>
<link rel="alternate" hreflang="en" href="https://daab-waas.com/en/{FILE}"/>
<link rel="alternate" hreflang="x-default" href="https://daab-waas.com/az/{FILE}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{ui['site']}"/>
<meta property="og:title" content="{esc(ui['title'])}"/>
<meta property="og:description" content="{esc(ui['description'])}"/>
<meta property="og:url" content="https://daab-waas.com/{lang}/{FILE}"/>
<meta property="og:image" content="https://daab-waas.com/images/daab-logo.png"/>
<meta property="og:locale" content="{ui['locale']}"/>
<meta property="og:locale:alternate" content="{ui['alt_locale']}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{esc(ui['title'])}"/>
<meta name="twitter:description" content="{esc(ui['description'])}"/>
<meta name="twitter:image" content="https://daab-waas.com/images/daab-logo.png"/>
<!-- /daab-seo -->
<link href="../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../css/daab-common.css?v=115" rel="stylesheet"/>
<link href="../css/daab-perf.css?v=2" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=14" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=11" rel="stylesheet"/>
<link href="../css/daab-search.css?v=10" rel="stylesheet"/>
<link href="../css/daab-page-content-search.css?v=9" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=4" rel="stylesheet"/>
<link href="../css/daab-print-pdf.css?v=11" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=15" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=86" rel="stylesheet"/>
<link href="../css/daab-sidebar-widget.css?v=6" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../css/daab-complex-topics-approach.css?v=8" rel="stylesheet"/>
<link href="../css/daab-complex-topics-informatics.css?v=6" rel="stylesheet"/>
<link href="../css/daab-table-resize.css?v=3" rel="stylesheet"/>
<link href="../css/daab-toc-drawer.css?v=1" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-perf.js?v=4" defer></script>
<script src="../js/daab-sticky-chrome.js?v=7" defer></script>
<script src="../js/daab-page-content-search.js?v=10" defer></script>
<script src="../js/daab-back-to-top.js?v=5" defer></script>
<script src="../js/daab-print-pdf.js?v=3" defer></script>
<script src="../js/daab-i18n.js?v=74" defer></script>
<script src="../js/daab-lang-position.js?v=16" defer></script>
<script src="../js/daab-design-tokens.js?v=2" defer></script>
<script src="../js/daab-nav.js?v=35" defer></script>
<script src="../js/daab-primary-nav.js?v=67" defer></script>
<script src="../js/daab-breadcrumbs.js?v=61" defer></script>
<script src="../js/daab-shell.js?v=19" defer></script>
<script src="../js/daab-page-subtitle.js?v=3" defer></script>
<script src="../js/daab-search.js?v=17" defer></script>
<script src="../js/daab-analytics.js?v=7" defer></script>
<script src="../js/daab-sidebar-spy.js?v=1" defer></script>
<script src="../js/daab-sidebar-timeline.js?v=7" defer></script>
<script src="../js/daab-toc-drawer.js?v=1" defer></script>
<script src="../js/daab-table-resize.js?v=5" defer></script>
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
<h1 aria-describedby="page-hero-subtitle">{ui['h1']}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(ui['subtitle'])}</p>
</section>
<aside aria-label="{esc(ui['panel_aria'])}" class="hero-panel">
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
<div class="cta-toc-backdrop" id="ctaTocBackdrop" hidden></div>
<div class="cta-layout">
<aside class="cta-toc sidebar" id="ctaTocPanel" aria-label="{esc(ui['toc_aria'])}">
<div class="sidebar-widget" id="ctaTocWidget">
<div class="widget-head">
<h2 class="cta-toc-title" id="ctaTocHeading"><span aria-hidden="true">📗</span> {esc(ui['toc_title'])}</h2>
<button aria-controls="ctaTocMenu" aria-expanded="false" aria-label="{esc(ui['toc_toggle'])}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button>
</div>
<div class="widget-body" id="ctaTocMenu">
<nav class="cta-toc-nav">
<ol class="cta-toc-list timeline-list">
{toc_html(lang)}
</ol>
</nav>
</div>
</div>
</aside>
<div class="cta-stack">
{body(lang)}
</div>
</div>
</main>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(ui['footer_brand'])}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(ui['contact'])}</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(ui['address'])}</h4><p class="footer-address">{ui['address_html']}</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(ui['leadership'])}</h4><p class="footer-leader">{ui['leader_html']}</p></div>
</div>
</div>
<div class="footer-bottom"><nav class="footer-legal-links" aria-label="{esc(ui['legal_aria'])}"><a href="/{lang}/feedback.html">{esc(ui['feedback'])}</a><a href="/{lang}/privacy.html#page-title">{esc(ui['privacy'])}</a><a href="/{lang}/terms.html#page-title">{esc(ui['terms'])}</a><a href="/{lang}/cookies.html#page-title">{esc(ui['cookies'])}</a><a href="/{lang}/legal-notice.html#page-title">{esc(ui['legal'])}</a><a href="/{lang}/sitemap.html#page-title">{esc(ui['sitemap'])}</a></nav><div class="footer-copy">{esc(ui['copy'])}</div></div>
</footer>
<button type="button" class="cta-toc-launch" id="ctaTocLaunch" aria-controls="ctaTocPanel" aria-expanded="false" aria-label="{esc(ui['toc_open'])}">
<span class="cta-toc-launch-icon" aria-hidden="true">📗</span>
<span class="cta-toc-launch-label">{esc(ui['toc_label'])}</span>
</button>
</body>
</html>
"""


def main() -> None:
    for lang in ("az", "en"):
        html = page_html(lang)
        path = ROOT / lang / FILE
        path.write_text(html, encoding="utf-8", newline="\n")
        dest = ROOT / "Deployment" / lang / FILE
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8", newline="\n")
        print("wrote", path)


if __name__ == "__main__":
    main()
