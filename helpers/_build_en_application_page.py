#!/usr/bin/env python3
"""Build en/application.html from en/application/application.html with DAAB site shell."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

SRC = ROOT / "en" / "application" / "application.html"
MEMBERSHIP = ROOT / "en" / "membership.html"
OUT = ROOT / "en" / "application.html"
ASSET = "../"


def extract_nav(html: str) -> str:
    m = re.search(
        r'(<nav aria-label="Main navigation" class="nav-strip">.*?</nav>)',
        html,
        re.DOTALL,
    )
    return m.group(1) if m else ""


def extract_footer(html: str) -> str:
    m = re.search(r'(<footer class="footer-pro">.*?</footer>)', html, re.DOTALL)
    return m.group(1) if m else ""


def extract_form_block(src: str) -> str:
    start = src.find('<div class="progress-bar"')
    end = src.find("</div>\n\n<!-- FOOTER -->")
    if start < 0 or end < 0:
        raise SystemExit("Could not locate form block in source application.html")
    block = src[start:end].strip()
    block = block.replace(
        'class="progress-bar"',
        'class="app-progress-bar" role="navigation" aria-label="Form steps"',
    )
    block = block.replace('onclick="goTo(', 'onclick="daabApplicationGoTo(')
    block = block.replace('onclick="next(', 'onclick="daabApplicationNext(')
    block = block.replace('onclick="prev(', 'onclick="daabApplicationPrev(')
    block = block.replace('onclick="submitForm()"', 'onclick="daabApplicationSubmit()"')
    block = block.replace('class="btn-row"', 'class="app-btn-row"')
    block = block.replace('class="btn btn-primary"', 'class="app-btn app-btn-primary"')
    block = block.replace('class="btn btn-secondary"', 'class="app-btn app-btn-secondary"')
    block = block.replace('class="btn btn-submit"', 'class="app-btn app-btn-submit"')
    block = block.replace('<a href="#">Charter</a>', '<a href="charter.html">Charter</a>')
    block = block.replace("mailto:info@daab.az", "mailto:bilik.birlik@gmail.com")
    block = block.replace(">info@daab.az</a>", ">bilik.birlik@gmail.com</a>")
    return block


def shell_head() -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-daab-lang="en" data-daab-asset-root="{ASSET}" data-daab-page-id="membership-application" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>WAAS — Membership Application Form</title>
<meta name="description" content="Online membership application form for the World Association of Azerbaijani Scientists (WAAS)."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=26" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-membership-application.css?v=2" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=13" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=13" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v=6" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=7" defer></script>
<script src="{ASSET}js/daab-shell.js?v=11" defer></script>
<script src="{ASSET}js/daab-search.js?v=4" defer></script>
<script src="{ASSET}js/daab-membership-application.js?v=1" defer></script>
</head>
"""


def hero_block() -> str:
    return """<body class="application-page membership-page">
<a class="skip" href="#content">Skip to content</a>
NAV_PLACEHOLDER
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1>Membership <span>Application</span></h1>
<p class="hero-text">Complete the step-by-step form below to apply for WAAS membership. We will contact you after your application is received.</p>
</section>
<aside aria-label="Application overview" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">Membership application form</h2>
<p class="panel-copy">Complete the introduction, personal information, scientific fields, and additional information sections in order. Our email address is shown for CV and photo submissions.</p>
</div>
</aside>
</div>
</header>
<main class="main application-main" id="content">
"""


def success_extra() -> str:
    return """      <p>
        <a class="app-btn app-btn-primary" href="membership.html">Return to membership page</a>
      </p>"""


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing source: {SRC}")
    membership = MEMBERSHIP.read_text(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    nav = extract_nav(membership)
    if not nav:
        raise SystemExit("Could not extract nav from en/membership.html")
    footer = extract_footer(membership)
    if not footer:
        raise SystemExit("Could not extract footer from en/membership.html")
    form = extract_form_block(src)
    form = form.replace(
        "</p>\n    </div>\n\n  </form>",
        "</p>\n" + success_extra().strip() + "\n    </div>\n\n  </form>",
        1,
    )
    html = shell_head()
    html += hero_block().replace("NAV_PLACEHOLDER", nav)
    html += form + "\n</div>\n</main>\n"
    html += footer + "\n</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
