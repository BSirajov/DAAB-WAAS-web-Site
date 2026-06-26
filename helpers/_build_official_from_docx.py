"""Build az/forum/2024/official.html from forum_2024/Rəsmi_müraciətlər.docx (Yeniliklər UI)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from _embed_static_nav import forum_nav_strip  # noqa: E402
from _forum_page_shell import forum_inner_shell_scripts, forum_inner_stylesheets  # noqa: E402
from _official_content import (  # noqa: E402
    ASSET,
    META_AZ,
    PANEL_COPY_AZ,
    cards_html_az,
    parse_sections_az,
    toc_html,
)

OUT = ROOT / "az" / "forum" / "2024" / "official.html"

SIDEBAR_SCRIPT = """
<script src="../../../js/daab-sidebar-timeline.js?v=2" defer></script>"""


def build() -> None:
    sections = parse_sections_az()
    toc_items = toc_html(sections)
    cards = cards_html_az(sections)
    nav = forum_nav_strip("az", active_nav_id="forum-2024")

    html = f"""<!DOCTYPE html>
<html lang="az" data-daab-lang="az" data-daab-asset-root="{ASSET}" data-daab-page-id="forum-official" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Rəsmi müraciətlər — DAAB</title>
<meta name="description" content="{META_AZ}"/>
{forum_inner_stylesheets(ASSET, extra=("daab-presentations-toc.css", "daab-speech-photos.css"))}
{forum_inner_shell_scripts(ASSET)}
</head>
<body>
<a class="skip" href="#content">Məzmuna keç</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Səhifə yolu">
<a href="../../index.html">Ana səhifə</a><span aria-hidden="true">›</span><a href="index.html">Forum 2024</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">Rəsmi müraciətlər</span>
</div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>Rəsmi <span>müraciətlər</span></h1>
</section>
<aside aria-label="Rəsmi müraciətlər haqqında qısa məlumat" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">Rəsmi müraciətlər</h2>
<div class="panel-copy">{PANEL_COPY_AZ}</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head"><span>📋 Müraciətlər</span><button aria-controls="officialTOC" aria-expanded="false" aria-label="Müraciətlər menyusunu aç" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="officialTOC">
{toc_items}
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
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">Əlaqə</h4><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">Ünvan</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">Rəhbərlik</h4><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>
</footer>
{SIDEBAR_SCRIPT}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(sections)} sections)")


if __name__ == "__main__":
    build()
