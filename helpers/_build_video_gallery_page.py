"""Build az/en forum video gallery pages from js/video-gallery-data.json."""
from __future__ import annotations

import html
import json
from pathlib import Path

from _paths import ROOT
from _footer_leader_snippets import FOOTER_AZ_CREDENTIAL, FOOTER_EN_CREDENTIAL
from forum_breadcrumbs import forum_breadcrumb_inner
from _inject_seo_head import build_seo_block
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS
from forum_en_video_gallery import translate_description
from _embed_static_nav import forum_nav_strip

DATA_JS = ROOT / "js" / "video-gallery-data.json"
ASSET = "../../../"
VIDEO_ROUTE_PAIR = {
    "az": "az/forum/2024/video_gallery.html",
    "en": "en/forum/2024/video_gallery.html",
}

COPY = {
    "az": {
        "lang": "az",
        "skip": "Məzmuna keç",
        "nav_aria": "Əsas naviqasiya",
        "title": "Video qalereya — DAAB",
        "description": "Forum 2024 (Bakı, sentyabr) haqqında 60-dan çox televiziya və internet media reportajı və müsahibəsi — Diaspor TV, AzTV, İctimai və digər kanallar.",
        "h1_main": "Video",
        "h1_span": "qalereya",
        "subtitle": "Forum 2024-lə bağlı mediada yayımlanan video reportajlar və müsahibələr",
        "panel_title": "Media arxivi",
        "panel_copy": (
            "Bu bölmədə Forum 2024-lə bağlı video materiallar təqdim olunur. Süjetlər Forumun "
            "açılış mərasimini, rəsmi görüşləri, plenar sessiyaları və iştirakçılarla müsahibələri "
            "əhatə edir. Hər kartda materialın mövzusu və yayımlandığı mənbə göstərilir. Diaspor TV, "
            "AzTV, İctimai TV, APA TV, Real TV və digər platformalarda yayımlanmış videoları "
            "YouTube-da izləyə bilərsiniz."
        ),
        "section": "Mediada yayımlanan video reportajlar və müsahibələr",
        "watch": "Videoya keç",
        "footer_org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "footer_contact": "Əlaqə",
        "footer_address": "Ünvan",
        "footer_leadership": "Rəhbərlik",
        "footer_leader": (
            "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>"
            "DAAB İdarə Heyətinin sədri<br/>"
            f"{FOOTER_AZ_CREDENTIAL}"
        ),
        "footer_rights": "© 2026 DAAB — Bütün hüquqlar qorunur",
    },
    "en": {
        "lang": "en",
        "skip": "Skip to content",
        "nav_aria": "Main navigation",
        "title": "Video gallery — WAAS",
        "description": "60+ TV and online reports on Forum 2024 (Baku, September)—coverage from Diaspor TV, AzTV, Public TV, APA and other outlets.",
        "h1_main": "Video",
        "h1_span": "gallery",
        "subtitle": "Video reports and interviews published in the media on Forum 2024",
        "panel_title": "Media archive",
        "panel_copy": (
            "This section presents video materials related to Forum 2024. The clips "
            "cover the opening ceremony, official meetings, plenary sessions and interviews with "
            "participants. Each card shows the topic of the item and the outlet where it was published. "
            "You can watch videos from Diaspor TV, AzTV, Public TV, APA TV, Real TV and other "
            "platforms on YouTube."
        ),
        "section": "Video reports and interviews in the media",
        "watch": "Watch video",
        "footer_org": "World Association of Azerbaijani Scientists",
        "footer_contact": "Contact",
        "footer_address": "Address",
        "footer_leadership": "Leadership",
        "footer_leader": (
            "<strong>Prof. Dr. Messoud Efendiyev</strong><br/>"
            "Chair of the WAAS Executive Board<br/>"
            f"{FOOTER_EN_CREDENTIAL}"
        ),
        "footer_rights": "© 2026 WAAS — All rights reserved",
    },
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def image_src(item: dict) -> str:
    """Resolve site-relative or absolute image path for HTML."""
    raw = item["image"]
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    return f"{ASSET}{raw}"


def grid_html_for(lang: str, items: list[dict]) -> str:
    c = COPY[lang]
    cards: list[str] = []
    for item in items:
        img = esc(image_src(item))
        link = esc(item["link"])
        caption = esc(item["caption"])
        desc_raw = (item.get("description") or "").strip()
        if lang == "en" and desc_raw:
            desc_raw = translate_description(desc_raw)
        desc_html = (
            f'\n<p class="video-gallery-description">{esc(desc_raw)}</p>'
            if desc_raw
            else ""
        )
        cards.append(
            f"""<article class="video-gallery-item" role="listitem">
<figure class="video-gallery-figure">
<a class="video-gallery-thumb" href="{link}" target="_blank" rel="noopener noreferrer" aria-label="{caption} — {esc(c["watch"])}">
<img src="{img}" alt="{caption}" loading="lazy" decoding="async"/>
</a>
<figcaption class="video-gallery-caption">
<a href="{link}" target="_blank" rel="noopener noreferrer">{caption}</a>{desc_html}
</figcaption>
</figure>
</article>"""
        )
    return f"""<div class="video-gallery-intro">
<h2 class="video-gallery-section-title">{esc(c["section"])}</h2>
</div>
<div class="video-gallery-grid" role="list">
{chr(10).join(cards)}
</div>"""


def shell_head(lang: str) -> str:
    c = COPY[lang]
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    seo = build_seo_block(
        rel_path=VIDEO_ROUTE_PAIR[lang],
        lang=lang,
        title=c["title"],
        description=c["description"],
        asset=ASSET,
        pair=VIDEO_ROUTE_PAIR,
    )
    return f"""<!DOCTYPE html>
<html lang="{c["lang"]}" data-daab-lang="{c["lang"]}" data-daab-asset-root="{ASSET}" data-daab-page-id="forum-video-gallery" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(c["title"])}</title>
<meta name="description" content="{esc(c["description"])}"/>
{seo}
<link href="{ASSET}css/daab-fonts.css?v={st["daab-fonts.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-perf.css?v={st["daab-perf.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st["daab-sticky-chrome.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v={st["daab-back-to-top.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v={st["daab-activities-layout.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v={st["daab-forum-content.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-video-gallery.css?v={st["daab-video-gallery.css"]}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-perf.js?v={sv["daab-perf.js"]}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv["daab-sticky-chrome.js"]}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
</head>
"""


def page_html(lang: str, items: list[dict]) -> str:
    c = COPY[lang]
    grid = grid_html_for(lang, items)
    nav = forum_nav_strip(lang, active_nav_id="forum-2024")
    if lang == "az":
        crumbs = (
            '<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Səhifə yolu">\n'
            + forum_breadcrumb_inner("az", "Video qalereya")
            + "\n</div>"
        )
        menu_aria = "Menyunu aç"
    else:
        crumbs = (
            '<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Breadcrumb">\n'
            + forum_breadcrumb_inner("en", "Video gallery")
            + "\n</div>"
        )
        menu_aria = "Open menu"
    return f"""{shell_head(lang)}
<body>
<a class="skip" href="#content">{esc(c["skip"])}</a>
{nav.replace('aria-label="Open menu"', f'aria-label="{menu_aria}"').replace('aria-label="Menyunu aç"', f'aria-label="{menu_aria}"')}
{crumbs}
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1 aria-describedby="page-hero-subtitle">{esc(c["h1_main"])} <span>{esc(c["h1_span"])}</span></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(c["subtitle"])}</p>
</section>
<aside aria-label="{esc(c["panel_title"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(c["panel_title"])}</h2>
<div class="panel-copy">{esc(c["panel_copy"])}</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap content-wrap--single">
<main class="news-feed main video-gallery-main" id="content">
{grid}
</main>
</div>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(c["footer_org"])}</h3></div>
<div class="footer-grid">
<div class="footer-col">
<h4 class="footer-title">{esc(c["footer_contact"])}</h4>
<div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div>
<div class="footer-item">☎ <span>+90 555 147 46 74</span></div>
<div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div>
</div>
<div class="footer-col">
<h4 class="footer-title">{esc(c["footer_address"])}</h4>
<p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p>
</div>
<div class="footer-col">
<h4 class="footer-title">{esc(c["footer_leadership"])}</h4>
<p class="footer-leader">{c["footer_leader"]}</p>
</div>
</div>
</div>
<div class="footer-bottom">{esc(c["footer_rights"])}</div>
</footer>
</body>
</html>
"""


def main() -> None:
    if not DATA_JS.is_file():
        raise SystemExit(f"Missing {DATA_JS}")

    items = json.loads(DATA_JS.read_text(encoding="utf-8"))
    for item in items:
        if item.get("image", "").startswith("http"):
            raise SystemExit(
                "Remote image URLs in video-gallery-data.json; use local images/ paths"
            )

    for lang in ("az", "en"):
        out = ROOT / lang / "forum" / "2024" / "video_gallery.html"
        out.write_text(page_html(lang, items), encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
