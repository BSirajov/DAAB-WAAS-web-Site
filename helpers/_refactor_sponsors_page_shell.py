#!/usr/bin/env python3
"""Scope sponsors page CSS to .sponsors-page and align AZ/EN HTML shell with donate.html."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_PATH = ROOT / "css" / "daab-sponsors-page.css"
JS_PATH = ROOT / "js" / "daab-sponsors-page.js"
PAGES = [ROOT / "az" / "sponsors.html", ROOT / "en" / "sponsors.html"]

HEAD_EN = """<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Support WAAS — World Association of Azerbaijani Scientists</title>
<meta name="description" content="Partner with WAAS through corporate sponsorship — scholarships, forums, and research collaboration."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/daab-common.css?v=64" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=13" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=1" rel="stylesheet"/>
<link href="../css/daab-search.css?v=4" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=12" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=28" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=11" rel="stylesheet"/>
<link href="../css/daab-sponsors-page.css?v=3" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-sticky-chrome.js?v=1" defer></script>
<script src="../js/daab-back-to-top.js?v=3" defer></script>
<script src="../js/daab-i18n.js?v=21" defer></script>
<script src="../js/daab-lang-position.js?v=7" defer></script>
<script src="../js/daab-nav.js?v=23" defer></script>
<script src="../js/daab-primary-nav.js?v=28" defer></script>
<script src="../js/daab-breadcrumbs.js?v=20" defer></script>
<script src="../js/daab-page-subtitle.js?v=2" defer></script>
<script src="../js/daab-shell.js?v=12" defer></script>
<script src="../js/daab-search.js?v=8" defer></script>
<script src="../js/daab-sponsors-page.js?v=1" defer></script>"""

HEAD_AZ = """<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>DAAB-a Dəstək — Dünya Azərbaycanlı Alimlər Birliyi</title>
<meta name="description" content="DAAB ilə korporativ sponsorluq — təqaüdlər, forumlar və elmi əməkdaşlıq."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="../css/daab-common.css?v=64" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=13" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=1" rel="stylesheet"/>
<link href="../css/daab-search.css?v=4" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=12" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=28" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=11" rel="stylesheet"/>
<link href="../css/daab-sponsors-page.css?v=3" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-sticky-chrome.js?v=1" defer></script>
<script src="../js/daab-back-to-top.js?v=3" defer></script>
<script src="../js/daab-i18n.js?v=21" defer></script>
<script src="../js/daab-lang-position.js?v=7" defer></script>
<script src="../js/daab-nav.js?v=23" defer></script>
<script src="../js/daab-primary-nav.js?v=28" defer></script>
<script src="../js/daab-breadcrumbs.js?v=20" defer></script>
<script src="../js/daab-page-subtitle.js?v=2" defer></script>
<script src="../js/daab-shell.js?v=12" defer></script>
<script src="../js/daab-search.js?v=8" defer></script>
<script src="../js/daab-sponsors-page.js?v=1" defer></script>"""

INLINE_SCRIPT_RE = re.compile(r"\n<script>.*?</script>\s*(?=</body>)", re.DOTALL)
HEAD_BLOCK_RE = re.compile(
    r"<meta charset=\"UTF-8\">.*?</head>",
    re.DOTALL | re.IGNORECASE,
)


def strip_global_blocks(css: str) -> str:
    css = re.sub(r"/\*\*[\s\S]*?\*/\s*", "", css, count=1)
    css = re.sub(r":root\s*\{[\s\S]*?\}\s*", "", css, count=1)
    css = re.sub(r"\*,\s*\*::before,\s*\*::after\s*\{[\s\S]*?\}\s*", "", css)
    css = re.sub(r"html\s*\{[\s\S]*?\}\s*", "", css)
    css = re.sub(r"body\s*\{[\s\S]*?\}\s*", "", css, count=1)
    return css


def prefix_selectors(css: str, scope: str) -> str:
    out: list[str] = []
    i = 0
    n = len(css)
    while i < n:
        if css.startswith("@keyframes", i) or css.startswith("@-webkit-keyframes", i):
            j = css.find("}", i)
            while j != -1 and css.count("{", i, j + 1) != css.count("}", i, j + 1):
                j = css.find("}", j + 1)
            out.append(css[i : j + 1])
            i = j + 1
            continue
        if css.startswith("@media", i):
            j = css.find("{", i)
            out.append(css[i:j + 1])
            i = j + 1
            inner, i = _extract_block(css, i)
            out.append(prefix_selectors(inner, scope))
            continue
        if css[i] in " \t\n\r":
            out.append(css[i])
            i += 1
            continue
        if css.startswith("/*", i):
            j = css.find("*/", i)
            out.append(css[i : j + 2])
            i = j + 2
            continue
        j = css.find("{", i)
        if j == -1:
            out.append(css[i:])
            break
        selectors = css[i:j].strip()
        if not selectors:
            i = j + 1
            continue
        prefixed = ", ".join(
            f"{scope} {s.strip()}" if not s.strip().startswith(scope) else s.strip()
            for s in selectors.split(",")
        )
        out.append(prefixed)
        block, i = _extract_block(css, j + 1)
        out.append("{" + block + "}")
    return "".join(out)


def _extract_block(css: str, start: int) -> tuple[str, int]:
    depth = 1
    i = start
    while i < len(css) and depth:
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return css[start:i], i + 1
        i += 1
    return css[start:], len(css)


def normalize_tokens(css: str) -> str:
    css = css.replace("'Playfair Display', serif", "var(--font-serif)")
    css = css.replace("'DM Sans', sans-serif", "var(--font-sans)")
    css = css.replace("var(--page-bg-pattern)", "var(--site-bg-image)")
    css = css.replace("var(--gold-pale)", "var(--gold-soft)")
    css = css.replace("var(--card-bg)", "var(--color-surface-toolbar, rgba(245,251,255,.96))")
    css = css.replace("var(--bg)", "var(--color-page-bg, #f0f6fb)")
    return css


def build_scoped_css(raw: str) -> str:
    body = strip_global_blocks(raw)
    body = normalize_tokens(body)
    scoped = prefix_selectors(body, ".sponsors-page")
    header = """/**
 * Sponsors page — scoped to .sponsors-page (shared AZ/EN).
 * Uses design tokens from css/daab-common.css; do not redefine :root here.
 */

.sponsors-page {
  --sp-hero-accent: var(--blue-700);
}

.sponsors-page .skip {
  position: absolute;
  left: -999px;
  top: 8px;
  background: white;
  color: var(--blue-700);
  padding: 10px 14px;
  border-radius: 10px;
  z-index: 999;
}
.sponsors-page .skip:focus {
  left: 8px;
}

.sponsors-page .hero {
  position: relative;
  overflow: hidden;
  color: var(--ink) !important;
  background: var(--white) var(--site-bg-image) top center / 100% auto no-repeat !important;
}
.sponsors-page .hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--color-hero-scrim);
}
.sponsors-page .hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(255, 255, 255, 0.18), rgba(255, 255, 255, 0));
  opacity: 0.72;
  mask-image: linear-gradient(to bottom, #000 0%, transparent 82%);
}
.sponsors-page .hero-wrap {
  position: relative;
  z-index: 1;
}

"""
    return header + scoped


def patch_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    head = HEAD_AZ if path.parent.name == "az" else HEAD_EN
    text = HEAD_BLOCK_RE.sub(head + "\n</head>", text, count=1)
    text = text.replace("<body>", '<body class="sponsors-page">', 1)
    text = INLINE_SCRIPT_RE.sub("\n", text)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    en = (ROOT / "en" / "sponsors.html").read_text(encoding="utf-8")
    m = re.search(r"<script>\s*(.*?)\s*</script>\s*</body>", en, re.DOTALL)
    if m:
        js_body = m.group(1).strip()
        JS_PATH.write_text(
            "/** Sponsors page interactions (scroll reveal, form validation). */\n"
            "(function () {\n"
            + "\n".join("  " + line if line else "" for line in js_body.splitlines())
            + "\n})();\n",
            encoding="utf-8",
            newline="\n",
        )
        print("wrote", JS_PATH.relative_to(ROOT))

    raw = CSS_PATH.read_text(encoding="utf-8")
    CSS_PATH.write_text(build_scoped_css(raw), encoding="utf-8", newline="\n")
    print("wrote", CSS_PATH.relative_to(ROOT))

    for page in PAGES:
        patch_html(page)
        print("patched", page.relative_to(ROOT))


if __name__ == "__main__":
    main()
