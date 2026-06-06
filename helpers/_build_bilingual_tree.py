#!/usr/bin/env python3
"""Build /az/ and /en/ page trees from legacy *_az.html sources.

Usage (from repo root):
    python helpers/_build_bilingual_tree.py
    python helpers/_build_bilingual_tree.py --patch-legacy
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _paths import ROOT

ROUTES_PATH = ROOT / "i18n" / "routes.json"
I18N_HEAD = """
<link href="{prefix}css/daab-lang.css?v=1" rel="stylesheet"/>
<link href="{prefix}css/daab-nav-mega.css?v=1" rel="stylesheet"/>
<script src="{prefix}js/daab-i18n.js?v=3" defer></script>
<script src="{prefix}js/daab-nav.js?v=6" defer></script>
<script src="{prefix}js/daab-primary-nav.js?v=2" defer></script>
<script src="{prefix}js/daab-breadcrumbs.js?v=1" defer></script>
<script src="{prefix}js/daab-section-nav.js?v=1" defer></script>
<script src="{prefix}js/daab-shell.js?v=2" defer></script>
"""

LEGACY_LINK_MAP = {
    "index.html": "index.html",
    "foundation_az.html": "foundation.html",
    "mission_vision_values_az.html": "mission.html",
    "activities_az.html": "activities.html",
    "scientists_list_view_az.html": "scientists/list.html",
    "scientists_card_view_az.html": "scientists/profiles.html",
    "executive_board_az.html": "executive-board.html",
    "charter_az.html": "charter.html",
    "membership_terms_az.html": "membership_value.html",
}

REVERSE_LEGACY = {v: k for k, v in LEGACY_LINK_MAP.items()}

SEARCH_SCRIPT_RE = re.compile(
    r'<script id="daab-shared-search-script">.*?</script>',
    re.DOTALL | re.IGNORECASE,
)

HOME_AZ_SOURCE = "sources/home_az.html"

INLINE_LIST_DATA_RE = re.compile(
    r"<script>\s*const DATA = \[.*?\];\s*",
    re.DOTALL,
)

EN_COMPLETE_MARKER = "<!-- daab-en-complete -->"

LOCALE_HINT_RE = re.compile(
    r'<div id="daab-locale-hint"[^>]*>.*?</div>\s*',
    re.DOTALL | re.IGNORECASE,
)

GATEWAY_INDEX = """<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>DAAB — Dünya Azərbaycanlı Alimlər Birliyi</title>
<meta name="description" content="Dünya Azərbaycanlı Alimlər Birliyi — rəsmi veb sayt."/>
<link rel="canonical" href="az/index.html"/>
<script>
(function () {
  var q = location.search || "";
  if (/[?&](legacy|choose)=1/.test(q)) return;
  var saved;
  try { saved = localStorage.getItem("daab-lang"); } catch (e) {}
  if (saved === "en") {
    location.replace("en/index.html" + q);
    return;
  }
  location.replace("az/index.html" + q);
})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=Playfair+Display:wght@700&amp;display=swap" rel="stylesheet"/>
<link href="css/daab-common.css?v=8" rel="stylesheet"/>
<link href="css/daab-lang.css?v=1" rel="stylesheet"/>
</head>
<body class="daab-gateway">
<main class="daab-gateway-page">
<div class="daab-gateway-card">
<img class="daab-gateway-logo" src="images/daab-logo.svg" alt="DAAB"/>
<h1>Dünya Azərbaycanlı Alimlər Birliyi</h1>
<p>World Association of Azerbaijani Scientists</p>
<div class="daab-gateway-actions">
<a class="btn btn-primary" href="az/index.html">Azərbaycan dilində davam et</a>
<a class="btn btn-secondary" href="en/index.html">Continue in English</a>
</div>
<p class="daab-gateway-note">
<a href="az/index.html">/az/</a> · <a href="en/index.html">/en/</a> ·
<a href="index.html?choose=1">Choose language / Dil seçin</a>
</p>
</div>
</main>
</body>
</html>
"""

STUB_EN_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{asset_root}" data-daab-page-id="{page_id}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>DAAB — {title}</title>
<meta name="description" content="World Association of Azerbaijani Scientists — {title}."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="{asset_root}css/daab-common.css?v=8" rel="stylesheet"/>
<link href="{asset_root}css/daab-mobile.css?v=3" rel="stylesheet"/>
<link href="{asset_root}css/daab-lang.css?v=1" rel="stylesheet"/>
{extra_css}
<script src="{asset_root}js/daab-nav.js?v=5" defer></script>
<script src="{asset_root}js/daab-mobile.js?v=1" defer></script>
<script src="{asset_root}js/daab-i18n.js?v=1" defer></script>
<script src="{asset_root}js/daab-shell.js?v=1" defer></script>
</head>
<body>
<a class="skip" href="#content">{skip}</a>
<nav aria-label="Main navigation" class="nav-strip"><div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a aria-label="DAAB home" href="{home}"><img src="{asset_root}images/daab-logo.svg" class="nav-brand-logo" alt="DAAB Logo"/></a></div>
<a class="nav-brand" href="{home}"><span class="nav-brand-text">World Association of<br class="mobile-hidden-break">Azerbaijani Scientists</span></a>
<div class="nav-menu" id="primaryNavMenu"><div class="nav-divider"></div>
{nav_links}
</div></div></nav>
<main class="main shell" id="content" style="padding-top:40px;padding-bottom:60px;">
<section class="daab-stub-banner">
<p style="margin:0 0 6px;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#7a5a00;">English version</p>
<h2>{stub_title}</h2>
<p>{stub_body}</p>
<div class="daab-stub-actions">
<a class="btn btn-primary" href="{az_url}">View Azerbaijani page</a>
<a class="btn btn-secondary" href="{en_home}">English home</a>
</div>
</section>
</main>
<footer class="footer-pro"><div class="footer-inner"><div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div></div>
<div class="footer-bottom">© 2026 DAAB / WAAS — All Rights Reserved</div></footer>
</body>
</html>
"""

EN_NAV = [
    ("home", "index.html", "🏠 Home"),
    ("foundation", "foundation.html", "🏛️ Foundation"),
    ("mission", "mission.html", "💎 Mission"),
    ("activities", "activities.html", "📰 Activities"),
    ("scientists-list", "scientists/list.html", "📋 Directory"),
    ("scientists-profiles", "scientists/profiles.html", "👤 Profiles"),
    ("executive-board", "executive-board.html", "🎓 Board of Directors"),
    ("charter", "charter.html", "📜 Charter"),
    ("membership", "membership.html", "✒️ Membership"),
]


def load_routes() -> dict:
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def asset_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def rewrite_asset_paths(html: str, depth: int) -> str:
    prefix = asset_prefix(depth)
    if not prefix:
        return html

    def repl_attr(m: re.Match) -> str:
        attr, path = m.group(1), m.group(2)
        if path.startswith(("http://", "https://", "//", "data:", "mailto:", "tel:", "#")):
            return m.group(0)
        if path.startswith(prefix):
            return m.group(0)
        if re.match(r"^(css|js|images|cv|i18n)/", path, re.I):
            return f'{attr}="{prefix}{path}"'
        return m.group(0)

    html = re.sub(r'(href|src)=["\']([^"\']+)["\']', repl_attr, html, flags=re.I)
    html = re.sub(
        r'url\(["\']?(css|images|js)/',
        lambda m: f'url("{prefix}{m.group(1)}/',
        html,
        flags=re.I,
    )
    return html


AZ_ROOT_PAGES = [
    "index.html",
    "foundation.html",
    "mission.html",
    "activities.html",
    "executive-board.html",
    "charter.html",
    "membership.html",
]


def rewrite_internal_links(html: str, depth: int) -> str:
    for legacy, target in LEGACY_LINK_MAP.items():
        html = html.replace(f'href="{legacy}"', f'href="{target}"')
        html = html.replace(f"href='{legacy}'", f"href='{target}'")
    if depth >= 2:
        up = "../" * (depth - 1)
        for page in AZ_ROOT_PAGES:
            html = html.replace(f'href="{page}"', f'href="{up}{page}"')
            html = html.replace(f"href='{page}'", f"href='{up}{page}'")
        html = html.replace('href="scientists/list.html"', 'href="list.html"')
        html = html.replace('href="scientists/profiles.html"', 'href="profiles.html"')
    return html


def inject_i18n_head(html: str, depth: int, page_id: str, lang: str) -> str:
    prefix = asset_prefix(depth)
    block = I18N_HEAD.format(prefix=prefix).strip()
    html = re.sub(r'\s*lang="[^"]*"', "", html, count=1)
    html = re.sub(r'\s*data-daab-lang="[^"]*"', "", html)
    html = re.sub(r'\s*data-daab-asset-root="[^"]*"', "", html)
    html = re.sub(r'\s*data-daab-page-id="[^"]*"', "", html)
    html = re.sub(
        r"<html([^>]*)>",
        f'<html\\1 lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{prefix}" data-daab-page-id="{page_id}" data-daab-nav-mount="1">',
        html,
        count=1,
        flags=re.I,
    )
    if "daab-i18n.js" not in html:
        html = html.replace("</head>", block + "\n</head>", 1)
    return html


def externalize_scientists_list_data(html: str, depth: int) -> str:
    prefix = asset_prefix(depth)
    if "const DATA = [" not in html:
        return html
    block = (
        f'<script src="{prefix}js/scientists-catalog-data.js?v=1"></script>\n'
        "<script>\nconst DATA = window.SCIENTISTS_CATALOG_DATA || [];\n"
    )
    return INLINE_LIST_DATA_RE.sub(block, html, count=1)


LEGACY_REDIRECT_RE = re.compile(
    r'<meta\s+http-equiv=["\']refresh["\'][^>]*>\s*',
    re.IGNORECASE,
)


def strip_legacy_redirect_meta(html: str) -> str:
    """Remove meta-refresh tags copied from root *_az.html legacy files."""
    html = LEGACY_REDIRECT_RE.sub("", html)
    html = re.sub(r"<!-- data-daab-legacy-redirect -->\s*", "", html)
    html = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']az/[^"\']*["\']\s*/>\s*',
        "",
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    return html


def replace_inline_search(html: str, depth: int) -> str:
    prefix = asset_prefix(depth)
    tag = f'<script src="{prefix}js/daab-search.js?v=1" defer></script>'
    if SEARCH_SCRIPT_RE.search(html):
        return SEARCH_SCRIPT_RE.sub(tag, html, count=1)
    if 'id="search-overlay"' in html and "daab-search.js" not in html:
        return html.replace("</body>", tag + "\n</body>", 1)
    return html


def bump_nav_script(html: str) -> str:
    return html.replace("daab-nav.js?v=4", "daab-nav.js?v=5")


def strip_locale_hint(html: str) -> str:
    return LOCALE_HINT_RE.sub("", html)


def add_nav_data_attrs(html: str) -> str:
    pairs = [
        ("index.html", "home"),
        ("foundation.html", "foundation"),
        ("mission.html", "mission"),
        ("activities.html", "activities"),
        ("executive-board.html", "executive-board"),
        ("charter.html", "charter"),
        ("membership.html", "membership"),
        ("scientists/list.html", "scientists-list"),
        ("scientists/profiles.html", "scientists-profiles"),
        ("foundation_az.html", "foundation"),
        ("mission_vision_values_az.html", "mission"),
        ("activities_az.html", "activities"),
        ("executive_board_az.html", "executive-board"),
        ("charter_az.html", "charter"),
        ("membership_terms_az.html", "membership"),
        ("scientists_list_view_az.html", "scientists-list"),
        ("scientists_card_view_az.html", "scientists-profiles"),
    ]
    for href, nav_id in pairs:
        html = re.sub(
            rf'(<a[^>]*href=["\']){re.escape(href)}(["\'][^>]*class=["\'][^"\']*nav-link)',
            rf'\1{href}\2" data-nav-id="{nav_id}"',
            html,
            count=0,
        )
        html = re.sub(
            rf'(<a[^>]*href=["\']){re.escape(href)}(["\'][^>]*class=["\'][^"\']*nav-dropdown-link)',
            rf'\1{href}\2" data-nav-id="{nav_id}"',
            html,
            count=0,
        )
    return html


def build_az_page(legacy_name: str, dest: Path, page_id: str) -> None:
    src = ROOT / legacy_name
    if not src.is_file():
        print(f"  skip missing source: {legacy_name}")
        return
    depth = len(dest.relative_to(ROOT).parts) - 1  # az/x.html -> 2, az/scientists/x.html -> 3
    html = src.read_text(encoding="utf-8")
    html = strip_legacy_redirect_meta(html)
    html = rewrite_asset_paths(html, depth)
    html = rewrite_internal_links(html, depth)
    html = inject_i18n_head(html, depth, page_id, "az")
    html = add_nav_data_attrs(html)
    html = replace_inline_search(html, depth)
    html = externalize_scientists_list_data(html, depth)
    html = bump_nav_script(html)
    html = strip_locale_hint(html)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8", newline="\n")
    print(f"  az: {dest.relative_to(ROOT)}")


def en_nav_links(active_id: str, depth: int) -> str:
    """depth = number of path segments under en/ (1 = en/page, 2 = en/scientists/page)."""
    nav_prefix = "../" if depth >= 2 else ""
    lines = []
    for nav_id, href, label in EN_NAV[:4]:
        cur = " active" if nav_id == active_id else ""
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="nav-link{cur}" data-nav-id="{nav_id}" href="{nav_prefix}{href}"{ac}>{label}</a>'
        )
    lines.append(
        '<div class="nav-dropdown" data-nav-dropdown>'
        '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
        '🌐 Scientists <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        '<div class="nav-dropdown-panel" role="menu">'
    )
    for nav_id, href, label in EN_NAV[4:6]:
        cur = " active" if nav_id == active_id else ""
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="nav-dropdown-link{cur}" data-nav-id="{nav_id}" role="menuitem" '
            f'href="{nav_prefix}{href}"{ac}>{label}</a>'
        )
    lines.append("</div></div>")
    for nav_id, href, label in EN_NAV[6:]:
        cur = " active" if nav_id == active_id else ""
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="nav-link{cur}" data-nav-id="{nav_id}" href="{nav_prefix}{href}"{ac}>{label}</a>'
        )
    return "\n".join(lines)


def en_page_is_complete(path: Path) -> bool:
    if not path.is_file():
        return False
    html = path.read_text(encoding="utf-8", errors="replace")
    if LEGACY_REDIRECT_RE.search(html):
        return False
    return EN_COMPLETE_MARKER in html


def build_en_stub(page: dict) -> None:
    dest = ROOT / page["en"]
    if en_page_is_complete(dest):
        print(f"  en: {dest.relative_to(ROOT)} (published — skipped)")
        return
    parts = dest.relative_to(ROOT).parts
    depth = len(parts) - 1  # en/foo.html -> 2, en/scientists/list.html -> 3
    asset_root = asset_prefix(depth)
    az_url = asset_root + page["az"]
    en_home = asset_root + "index.html" if depth else "index.html"
    title = page["id"].replace("-", " ").title()
    extra = ""
    if page["id"] in ("scientists-list", "scientists-profiles"):
        extra = f'<link href="{asset_root}css/scientists-catalog-toolbar.css?v=4" rel="stylesheet"/>'
    html = STUB_EN_TEMPLATE.format(
        asset_root=asset_root,
        page_id=page["id"],
        title=title,
        extra_css=extra,
        skip="Skip to content",
        home=en_home if depth == 0 else asset_root + "index.html",
        nav_links=en_nav_links(page["id"], depth),
        stub_title="Translation in progress",
        stub_body=(
            "This page is part of the new bilingual site structure. "
            "Full English content will be published here. "
            "You can read the Azerbaijani version in the meantime."
        ),
        az_url=az_url,
        en_home=asset_root + "index.html",
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8", newline="\n")
    print(f"  en: {dest.relative_to(ROOT)}")


def build_en_home() -> None:
    dest = ROOT / "en" / "index.html"
    az_home = ROOT / "az" / "index.html"
    if dest.is_file() and en_page_is_complete(dest):
        if "hero-panel" in dest.read_text(encoding="utf-8"):
            print(f"  en: {dest.relative_to(ROOT)} (published home — skipped)")
            return
    if az_home.is_file():
        try:
            from _publish_en_pages import publish_home

            publish_home()
            return
        except Exception as exc:
            print(f"  en: home publish failed ({exc}), using stub")
    cards = [
        ("mission.html", "💎", "Mission, Vision & Values", "Available in English — mission, vision and academic values."),
        ("activities.html", "📰", "Activities", "Events, conferences, and institutional initiatives."),
        ("foundation.html", "🏛️", "Foundation", "Available in English — Shusha Congress to Istanbul founding meeting."),
        ("scientists/list.html", "📋", "Scientists directory", "Searchable list of member scientists."),
        ("scientists/profiles.html", "👤", "Academic profiles", "Detailed scholar profiles and CV links."),
        ("executive-board.html", "🎓", "Board of Directors", "Leadership and governance."),
        ("charter.html", "📜", "Charter", "Statutes and governing documents."),
        ("membership.html", "✒️", "Membership", "How to join WAAS."),
    ]
    card_html = []
    for href, icon, title, desc in cards:
        card_html.append(
            f'<a class="page-card" href="{href}" style="min-height:200px;text-decoration:none;">'
            f'<div class="card-icon-wrap">{icon}</div>'
            f'<div class="card-body"><h3 class="card-title">{title}</h3>'
            f'<div class="card-desc">{desc}</div></div></a>'
        )
    stub = build_en_stub  # noqa — use template pieces
    page = {"id": "home", "en": "en/index.html", "az": "az/index.html"}
    nav = en_nav_links("home", 1)
    asset_root = "../"
    html = f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="../" data-daab-page-id="home">
<head>
{EN_COMPLETE_MARKER}
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>WAAS — World Association of Azerbaijani Scientists</title>
<meta name="description" content="International scientific network of Azerbaijani scholars worldwide."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/daab-common.css?v=8" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=3" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=1" rel="stylesheet"/>
<style>
.hero {{ position:relative; overflow:hidden; color:var(--ink)!important;
  background:#fff var(--site-bg-image) top center/100% auto no-repeat!important; }}
.hero-wrap {{ display:grid; grid-template-columns:1fr; gap:20px; padding:28px 24px 36px; }}
.hero h1 {{ margin:0; font-family:"Playfair Display",Georgia,serif; font-size:clamp(28px,4vw,48px); color:#08263b; }}
.cards-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:18px; }}
</style>
<script src="../js/daab-nav.js?v=5" defer></script>
<script src="../js/daab-mobile.js?v=1" defer></script>
<script src="../js/daab-i18n.js?v=1" defer></script>
<script src="../js/daab-shell.js?v=1" defer></script>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<nav aria-label="Main navigation" class="nav-strip"><div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a href="index.html"><img src="../images/daab-logo.svg" class="nav-brand-logo" alt="DAAB"/></a></div>
<a class="nav-brand" href="index.html"><span class="nav-brand-text">World Association of<br class="mobile-hidden-break">Azerbaijani Scientists</span></a>
<div class="nav-menu" id="primaryNavMenu"><div class="nav-divider"></div>
{nav}
</div></div></nav>
<header class="hero"><div class="hero-wrap shell">
<h1>World Association of <span style="color:var(--blue-700)">Azerbaijani Scientists</span></h1>
<p style="color:#345d76;max-width:52ch;">WAAS connects Azerbaijani scholars abroad with universities, research centres, and international partners.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;">
<a class="btn btn-primary" href="scientists/list.html">Meet our scientists</a>
<a class="btn btn-secondary" href="membership.html">Membership</a>
</div>
</div></header>
<main class="main shell" id="content" style="padding-bottom:60px;">
<section class="cards-grid">{''.join(card_html)}</section>
</main>
<footer class="footer-pro"><div class="footer-bottom">© 2026 WAAS — All Rights Reserved</div></footer>
</body>
</html>"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8", newline="\n")
    print(f"  en: {dest.relative_to(ROOT)}")


def patch_legacy(pages: list) -> None:
    for page in pages:
        legacy = page.get("legacy")
        if not legacy or legacy == "index.html":
            continue
        path = ROOT / legacy
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        html = inject_i18n_head(html, 0, page["id"], "az")
        html = add_nav_data_attrs(html)
        html = replace_inline_search(html, 0)
        html = bump_nav_script(html)
        html = strip_locale_hint(html)
        path.write_text(html, encoding="utf-8", newline="\n")
        print(f"  legacy patch: {legacy}")


def write_gateway_index() -> None:
    (ROOT / "index.html").write_text(GATEWAY_INDEX, encoding="utf-8", newline="\n")
    print("  gateway: index.html -> az/index.html")


SITE_ORIGIN = "https://daab-waas.com"


def write_sitemap(routes: dict) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in routes["pages"]:
        if page.get("sitemap") is False:
            continue
        az = page["az"].replace("\\", "/")
        en = page["en"].replace("\\", "/")
        az_url = f"{SITE_ORIGIN}/{az}"
        en_url = f"{SITE_ORIGIN}/{en}"
        for loc, lang in ((az_url, "az"), (en_url, "en")):
            lines.append("  <url>")
            lines.append(f"    <loc>{loc}</loc>")
            lines.append(f'    <xhtml:link rel="alternate" hreflang="az" href="{az_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{az_url}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  sitemap: sitemap.xml (with hreflang alternates)")


def write_robots_txt() -> None:
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE_ORIGIN}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(body, encoding="utf-8", newline="\n")
    print("  robots: robots.txt")


def write_legacy_redirects(routes: dict) -> None:
    redirects = routes.get("legacyRedirects", {})
    for legacy, target in redirects.items():
        if legacy == "index.html":
            continue
        src = ROOT / legacy
        if not src.is_file():
            continue
        html = src.read_text(encoding="utf-8")
        if "data-daab-legacy-redirect" in html:
            continue
        meta = f'<meta http-equiv="refresh" content="0; url={target}"/>\n<link rel="canonical" href="{target}"/>'
        if "<head>" in html:
            html = html.replace("<head>", f'<head>\n{meta}\n<!-- data-daab-legacy-redirect -->', 1)
        src.write_text(html, encoding="utf-8", newline="\n")
        print(f"  redirect hint: {legacy} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-legacy", action="store_true", default=True, help="Add i18n scripts to root *_az.html files (default: on)")
    parser.add_argument("--no-patch-legacy", action="store_false", dest="patch_legacy", help="Skip legacy root patches")
    parser.add_argument("--gateway", action="store_true", default=True, help="Replace root index.html with gateway (default: on)")
    parser.add_argument("--no-gateway", action="store_false", dest="gateway", help="Keep existing root index.html")
    parser.add_argument("--sitemap", action="store_true", default=True, help="Write sitemap.xml (default: on)")
    parser.add_argument("--no-sitemap", action="store_false", dest="sitemap", help="Skip sitemap generation")
    parser.add_argument(
        "--redirects",
        action="store_true",
        default=True,
        help="Add meta refresh from legacy pages to /az/ (default: on)",
    )
    parser.add_argument(
        "--no-redirects",
        action="store_false",
        dest="redirects",
        help="Skip legacy meta-refresh hints",
    )
    parser.add_argument(
        "--seo-only",
        action="store_true",
        help="Only regenerate sitemap.xml, robots.txt, and legacy redirect hints",
    )
    args = parser.parse_args()

    routes = load_routes()
    pages = routes["pages"]

    if args.seo_only:
        if args.sitemap:
            write_sitemap(routes)
            write_robots_txt()
        if args.redirects:
            print("Adding legacy redirect hints...")
            write_legacy_redirects(routes)
        print("Done. Run: python helpers/_validate_bilingual.py")
        return 0

    print("Building Azerbaijani tree (/az/)...")
    for page in pages:
        legacy = page.get("legacy")
        if page["id"] == "home":
            build_az_page(HOME_AZ_SOURCE, ROOT / page["az"], page["id"])
        elif legacy:
            build_az_page(legacy, ROOT / page["az"], page["id"])

    print("Building English stubs (/en/)...")
    build_en_home()
    for page in pages:
        if page["id"] == "home":
            continue
        build_en_stub(page)

    if args.patch_legacy:
        print("Patching legacy root pages...")
        patch_legacy(pages)

    if args.gateway:
        print("Writing root gateway...")
        write_gateway_index()

    if args.sitemap:
        write_sitemap(routes)
        write_robots_txt()

    if not (ROOT / ".nojekyll").exists():
        (ROOT / ".nojekyll").write_text("", encoding="utf-8")
        print("  created: .nojekyll")

    if args.redirects:
        print("Adding legacy redirect hints...")
        write_legacy_redirects(routes)

    print("Done. Run: python helpers/_validate_bilingual.py")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
