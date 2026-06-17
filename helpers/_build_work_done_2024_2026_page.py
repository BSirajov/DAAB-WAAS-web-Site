#!/usr/bin/env python3
"""Build az/work_done_2024_2026.html from the DİDK report source document."""
from __future__ import annotations

import base64
import html
import re
import subprocess
import sys
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS
from work_done_2024_2026_en_content import (
    HERO_SUBTITLE_EN,
    LAYOUT_EN,
    SUMMARY_ARIA_EN,
    SUMMARY_LEAD_EN,
    SUMMARY_TITLE_EN,
    remap_en_anchors,
)
from _footer_leader_snippets import FOOTER_AZ_LEADER_HTML, FOOTER_EN_LEADER_HTML

ASSET = "../"
PAGE_ID = "work-done-2024-2026"
SRC = ROOT / "documents/report_2024-2026/2.DAAB-DİDK Arayış 2024-2026 (1.8).html"
OUT = ROOT / "az/work_done_2024_2026.html"
EN_OUT = ROOT / "en/work_done_2024_2026.html"
IMG_DIR = ROOT / "images/work_done_2024_2026"
REPORT_CSS = ROOT / "css/daab-work-done-report.css"
REPORT_JS = ROOT / "js/daab-work-done-report.js"

DATA_URI_RE = re.compile(
    r"data:image/(?P<fmt>png|jpe?g|gif|webp);base64,(?P<data>[A-Za-z0-9+/=\s]+)",
    re.I,
)

HERO_SUBTITLE = (
    "Azərbaycan Diasporla İş üzrə Dövlət Komitəsinə təqdim olunur: "
    "2024–2026-cı illər ərzindəki fəaliyyətlər, əməkdaşlıq memorandumları, "
    "məşvərət şuraları və universitetlər ilə tərəfdaşlıq."
)

SUMMARY_ARIA_AZ = "Hesabatın icmalı"
SUMMARY_TITLE_AZ = "Hesabatın icmalı"
SUMMARY_LEAD_AZ = (
    "DİDK-ya təqdim olunan bu arayış 2024–2026-cı illər ərzindəki fəaliyyəti, o cümlədən "
    "onlayn görüşləri, universitet koordinatorlarının təyin edilməsini, əməkdaşlıq "
    "memorandumlarını, UNEC–DAAB Məşvərət Şurasını və Azərbaycan universitetlərində "
    "üzvlərin seminar, tədris və layihə fəaliyyətini üç əsas bölmədə ümumiləşdirir."
)

SECTION_I_TITLE_AZ_OLD = "DAAB-nin 1-ci Forumundan keçən vaxt ərzində görülmüş işlər"
SECTION_I_TITLE_AZ = "2024–2026-cı illər ərzində görülmüş işlər"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def hero_summary_aside(aria_label: str, title: str, lead: str) -> str:
    return (
        f'<aside class="hero-panel" aria-label="{esc(aria_label)}">\n'
        f'<div class="panel-card">\n'
        f'<h2 class="panel-title">{esc(title)}</h2>\n'
        f'<div class="panel-copy">\n'
        f'<p class="panel-copy-lead">{esc(lead)}</p>\n'
        f"</div>\n"
        f"</div>\n"
        f"</aside>"
    )


def extract_hero_subtitle(source: str) -> str:
    m = re.search(r'<div class="subtitle">(.*?)</div>', source, re.S)
    if not m:
        return HERO_SUBTITLE
    text = re.sub(r"\s+", " ", m.group(1)).strip()
    return text or HERO_SUBTITLE


def extract_layout_html(source: str) -> str:
    body = re.search(r"<body>(.*)</body>", source, re.S)
    if not body:
        raise SystemExit("Source body not found")
    m = re.search(r'(<div class="layout">.*?</div>\s*)(?=<button class="print-btn")', body.group(1), re.S)
    if not m:
        raise SystemExit("Source layout block not found")
    return m.group(1).strip()


def externalize_images(fragment: str) -> str:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        fmt = match.group("fmt").lower()
        ext = "jpg" if fmt in {"jpeg", "jpg"} else fmt
        raw = match.group("data").replace("\n", "").replace("\r", "").replace(" ", "")
        out_name = f"img-{counter:02d}.{ext}"
        (IMG_DIR / out_name).write_bytes(base64.b64decode(raw))
        return f"{ASSET}images/work_done_2024_2026/{out_name}"

    return DATA_URI_RE.sub(repl, fragment)


def normalize_content_links(fragment: str) -> str:
    fragment = fragment.replace("www.daab-waas.org", "daab-waas.com")
    fragment = re.sub(
        r"https?://daab-waas\.org(?=[/\s\"'])",
        "https://daab-waas.com",
        fragment,
        flags=re.I,
    )
    return fragment


def report_css() -> str:
    return """/**
 * DAAB–DİDK work-done report (2024–2026) — scoped content styles.
 * Source: documents/report_2024-2026/
 */
html[data-daab-page-id="work-done-2024-2026"] {
  scroll-behavior: smooth;
}

html[data-daab-page-id="work-done-2024-2026"] [id] {
  scroll-margin-top: calc(var(--daab-nav-height, 64px) + var(--daab-breadcrumbs-height, 0px) + 18px);
}

.work-done-report .report-layout {
  display: grid;
  grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.work-done-report .report-toc {
  position: sticky;
  top: calc(var(--daab-nav-height, 64px) + var(--daab-breadcrumbs-height, 0px) + 12px);
  align-self: start;
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 16px;
  max-height: calc(100vh - var(--daab-nav-height, 64px) - var(--daab-breadcrumbs-height, 0px) - 28px);
  overflow: auto;
}

.work-done-report .report-toc strong {
  display: block;
  color: var(--blue-700);
  margin-bottom: 10px;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.work-done-report .report-toc .toc-link {
  display: block;
  width: 100%;
  border: 0;
  background: transparent;
  text-align: left;
  font: inherit;
  color: var(--ink);
  padding: 7px 9px;
  border-radius: 10px;
  font-size: 0.94rem;
  cursor: pointer;
  line-height: 1.35;
}

.work-done-report .report-toc .toc-link:hover,
.work-done-report .report-toc .toc-link:focus {
  background: var(--blue-50, #eef4fb);
  color: var(--blue-700);
  outline: none;
}

.work-done-report .report-toc .toc-link.sub {
  padding-left: 22px;
  color: var(--muted);
  font-size: 0.88rem;
}

.work-done-report .report-toc .toc-link.active {
  background: var(--blue-50, #e6f0fb);
  color: var(--blue-700);
  font-weight: 700;
}

.work-done-report .report-content {
  min-width: 0;
}

.work-done-report .report-section {
  background: var(--white);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 28px 26px;
  margin-bottom: 22px;
  box-shadow: var(--shadow);
}

.work-done-report .report-section h2 {
  margin: 0 0 16px;
  font-family: var(--font-display, "Playfair Display", Georgia, serif);
  color: var(--blue-700);
  font-size: clamp(1.25rem, 2.2vw, 1.55rem);
  line-height: 1.25;
  border-left: 5px solid var(--gold-soft, #c8a24a);
  padding-left: 14px;
}

.work-done-report .report-section h3 {
  margin: 26px 0 10px;
  color: var(--blue-400, #1f4e79);
  font-size: 1.12rem;
}

.work-done-report .report-section p,
.work-done-report .report-section li {
  text-align: justify;
  text-justify: inter-word;
}

.work-done-report .report-section p {
  margin: 0 0 14px;
}

.work-done-report .doc-list {
  margin: 0 0 16px 22px;
  padding: 0;
}

.work-done-report .doc-list li {
  margin: 4px 0;
}

.work-done-report .table-wrap {
  overflow-x: auto;
  margin: 18px 0 20px;
  border: 1px solid var(--line);
  border-radius: 14px;
}

.work-done-report table {
  width: 100%;
  border-collapse: collapse;
  background: var(--white);
  min-width: 520px;
}

.work-done-report th,
.work-done-report td {
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
  text-align: left;
}

.work-done-report th {
  background: var(--blue-50, #eef4fb);
  color: var(--blue-700);
  font-weight: 700;
}

.work-done-report tr:last-child td {
  border-bottom: none;
}

.work-done-report .doc-figure {
  margin: 18px 0 8px;
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
  background: var(--white);
}

.work-done-report .doc-figure img {
  width: 100%;
  display: block;
  max-height: 560px;
  object-fit: contain;
  background: var(--white);
}

.work-done-report .caption {
  color: var(--muted);
  font-size: 0.92rem;
  margin: 8px 0 18px;
  font-style: italic;
}

.work-done-report .report-print-btn {
  position: fixed;
  right: 22px;
  bottom: calc(22px + env(safe-area-inset-bottom, 0px));
  z-index: 40;
  border: none;
  border-radius: 999px;
  background: var(--gold-soft, #c8a24a);
  color: var(--blue-900, #102a43);
  padding: 12px 18px;
  font-weight: 700;
  box-shadow: 0 8px 18px rgba(16, 42, 67, 0.2);
  cursor: pointer;
}

.work-done-report .report-print-btn:hover {
  filter: brightness(1.03);
}

@media (max-width: 960px) {
  .work-done-report .report-layout {
    grid-template-columns: 1fr;
  }

  .work-done-report .report-toc {
    position: relative;
    top: auto;
    max-height: none;
  }

  .work-done-report .report-section {
    padding: 20px 18px;
  }
}

@media print {
  .work-done-report .report-toc,
  .work-done-report .report-print-btn,
  .nav-strip,
  .daab-breadcrumbs,
  .daab-lang-switch,
  .footer-pro {
    display: none !important;
  }

  .work-done-report .report-layout {
    display: block;
    padding: 0;
  }

  .work-done-report .report-section {
    box-shadow: none;
    border: none;
    page-break-inside: auto;
  }
}
"""


def report_js() -> str:
    return """/**
 * Work-done report — sidebar TOC scroll + active section highlight.
 */
(function () {
  "use strict";

  var root = document.querySelector(".work-done-report");
  if (!root) return;

  function scrollOffset() {
    var nav = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue("--daab-nav-height") || "64",
      10
    );
    var crumbs = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue("--daab-breadcrumbs-height") || "0",
      10
    );
    return nav + crumbs + 16;
  }

  function scrollToTarget(id) {
    var el = document.getElementById(id);
    if (!el) return;
    var top = el.getBoundingClientRect().top + window.pageYOffset - scrollOffset();
    window.scrollTo({ top: top, behavior: "smooth" });
    try {
      if (history && history.replaceState) {
        history.replaceState(null, "", "#" + encodeURIComponent(id));
      }
    } catch (e) {}
  }

  var buttons = Array.prototype.slice.call(root.querySelectorAll(".toc-link[data-target]"));
  buttons.forEach(function (btn) {
    btn.addEventListener("click", function (ev) {
      ev.preventDefault();
      scrollToTarget(btn.getAttribute("data-target"));
    });
  });

  var targets = buttons
    .map(function (btn) {
      return document.getElementById(btn.getAttribute("data-target"));
    })
    .filter(Boolean);

  if ("IntersectionObserver" in window && targets.length) {
    var byId = {};
    buttons.forEach(function (btn) {
      byId[btn.getAttribute("data-target")] = btn;
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            buttons.forEach(function (btn) {
              btn.classList.remove("active");
            });
            var active = byId[entry.target.id];
            if (active) active.classList.add("active");
          }
        });
      },
      { root: null, rootMargin: "-12% 0px -68% 0px", threshold: 0.01 }
    );
    targets.forEach(function (el) {
      observer.observe(el);
    });
  }

  window.addEventListener("load", function () {
    var id = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (id) {
      setTimeout(function () {
        scrollToTarget(id);
      }, 180);
    }
  });
})();
"""


def remap_layout_classes(fragment: str) -> str:
    fragment = fragment.replace('class="toc" aria-label="Mündəricat"', 'class="report-toc" aria-label="Mündəricat"')
    fragment = fragment.replace('class="layout"', 'class="report-layout"')
    fragment = fragment.replace('class="toc"', 'class="report-toc" aria-label="Mündəricat"')
    fragment = fragment.replace('class="content"', 'class="report-content"')
    fragment = fragment.replace('class="section"', 'class="report-section"')
    fragment = fragment.replace("<main class=\"report-content\">", "<div class=\"report-content\">")
    fragment = re.sub(r"</main>(\s*</div>\s*)$", r"</div>\1", fragment)
    return fragment


def shell_head() -> str:
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    report_css_v = st.get("daab-work-done-report.css", 1)
    return f"""<!DOCTYPE html>
<html lang="az" data-daab-lang="az" data-daab-asset-root="{ASSET}" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>DAAB — Görülən işlər, 2024-2026</title>
<meta content="2024-2026-cu illərdə Dünya Azərbaycanlı Alimlər Birliyi (DAAB) fəaliyyətinin DİDK-ya təqdim olunan arayışı." name="description"/>
<link href="{ASSET}css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-perf.css?v={st.get("daab-perf.css", 1)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st.get("daab-sticky-chrome.css", 1)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-content-hero.css?v={st.get("daab-content-hero.css", 5)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v={st.get("daab-sidebar-widget.css", 6)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-work-done-report.css?v={report_css_v}" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-perf.js?v={sv.get("daab-perf.js", 1)}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv.get("daab-sticky-chrome.js", 3)}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v={sv.get("daab-design-tokens.js", 1)}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v={sv.get("daab-page-subtitle.js", 2)}" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
<script src="{ASSET}js/daab-work-done-report.js?v={sv.get("daab-work-done-report.js", 1)}" defer></script>
</head>
<body class="work-done-page">
<a class="skip" href="#content">Məzmuna keç</a>
"""


def footer_block() -> str:
    return f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Əlaqə</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Ünvan</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><div class="footer-title">Rəhbərlik</div><p class="footer-leader">{FOOTER_AZ_LEADER_HTML}</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>
</footer>
"""


def nav_strip_az() -> str:
    return """<nav aria-label="Əsas naviqasiya" class="nav-strip">
<div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="Menyunu aç" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a title="Ana səhifə" aria-label="DAAB ana səhifə" href="index.html">
<img src="../images/daab-logo.png" class="nav-brand-logo" alt="DAAB Logo"></a></div>
<a aria-label="DAAB ana səhifə" class="nav-brand" href="index.html">
<span class="nav-brand-text">Dünya Azərbaycanlı<br class="mobile-hidden-break">Alimlər Birliyi</span></a>
<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"></div>
</div></nav>"""


def build_az_page(source: str, layout_html: str, hero_subtitle: str) -> str:
    return (
        shell_head()
        + nav_strip_az()
        + """
<header class="hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>Görülən işlər, <span>2024-2026</span></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">"""
        + esc(hero_subtitle)
        + """</p>
</section>
"""
        + hero_summary_aside(SUMMARY_ARIA_AZ, SUMMARY_TITLE_AZ, SUMMARY_LEAD_AZ)
        + """
</div>
</header>
<main class="main shell work-done-report" id="content">
"""
        + layout_html
        + """
<button type="button" class="report-print-btn" onclick="window.print()">Çap et / PDF</button>
</main>
"""
        + footer_block()
        + """
</body>
</html>
"""
    )


def footer_block_en() -> str:
    return f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Contact</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Address</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p></div>
<div class="footer-col"><div class="footer-title">Leadership</div><p class="footer-leader">{FOOTER_EN_LEADER_HTML}</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 WAAS — All rights reserved</div>
</footer>
"""


def shell_head_en() -> str:
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    report_css_v = st.get("daab-work-done-report.css", 1)
    return f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{ASSET}" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<!-- daab-en-complete -->
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0, viewport-fit=cover" name="viewport"/>
<title>WAAS — Work Done 2024-2026</title>
<meta content="Report on World Association of Azerbaijani Scientists (WAAS) activities for 2024–2026, submitted to the State Committee on Work with Diaspora." name="description"/>
<link href="{ASSET}css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-perf.css?v={st.get("daab-perf.css", 1)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st.get("daab-sticky-chrome.css", 1)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-content-hero.css?v={st.get("daab-content-hero.css", 5)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v={st.get("daab-sidebar-widget.css", 6)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-work-done-report.css?v={report_css_v}" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-perf.js?v={sv.get("daab-perf.js", 1)}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv.get("daab-sticky-chrome.js", 3)}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v={sv.get("daab-design-tokens.js", 1)}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v={sv.get("daab-page-subtitle.js", 2)}" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
<script src="{ASSET}js/daab-work-done-report.js?v={sv.get("daab-work-done-report.js", 1)}" defer></script>
</head>
<body class="work-done-page">
<a class="skip" href="#content">Skip to content</a>
"""


def nav_strip_en() -> str:
    return """<nav aria-label="Main navigation" class="nav-strip">
<div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a title="Home page" aria-label="WAAS home" href="index.html">
<img src="../images/daab-logo.png" class="nav-brand-logo" alt="WAAS Logo"></a></div>
<a aria-label="WAAS home" class="nav-brand" href="index.html">
<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">Azerbaijani Scientists</span></a>
<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"></div>
</div></nav>"""


def build_en_page() -> str:
    return (
        shell_head_en()
        + nav_strip_en()
        + """
<header class="hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>Work Done, <span>2024-2026</span></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">"""
        + esc(HERO_SUBTITLE_EN)
        + """</p>
</section>
"""
        + hero_summary_aside(SUMMARY_ARIA_EN, SUMMARY_TITLE_EN, SUMMARY_LEAD_EN)
        + """
</div>
</header>
<main class="main shell work-done-report" id="content">
"""
        + remap_en_anchors(LAYOUT_EN)
        + """
<button type="button" class="report-print-btn" onclick="window.print()">Print / PDF</button>
</main>
"""
        + footer_block_en()
        + """
</body>
</html>
"""
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source: {SRC}")

    source = SRC.read_text(encoding="utf-8")
    hero_subtitle = extract_hero_subtitle(source)
    layout = extract_layout_html(source)
    layout = externalize_images(layout)
    layout = normalize_content_links(layout)
    layout = layout.replace(SECTION_I_TITLE_AZ_OLD, SECTION_I_TITLE_AZ)
    layout = remap_layout_classes(layout)

    REPORT_CSS.write_text(report_css(), encoding="utf-8")
    REPORT_JS.write_text(report_js(), encoding="utf-8")

    OUT.write_text(build_az_page(source, layout, hero_subtitle), encoding="utf-8")
    EN_OUT.write_text(build_en_page(), encoding="utf-8")

    embed = ROOT / "helpers/_embed_static_nav.py"
    subprocess.run([sys.executable, str(embed)], check=True, cwd=ROOT)

    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote {EN_OUT.relative_to(ROOT)}")
    print(f"Images in {IMG_DIR.relative_to(ROOT)} ({len(list(IMG_DIR.glob('*')))} files)")


if __name__ == "__main__":
    main()
