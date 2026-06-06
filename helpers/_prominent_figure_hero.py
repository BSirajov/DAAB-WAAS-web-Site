"""Shared prominent-figure profile hero markup (DAAB site hero pattern)."""
from __future__ import annotations

import re

HERO_BLOCK_RE = re.compile(
    r"<section class=\"pf-hero\">(.*?)</section>\s*(<main)",
    re.DOTALL | re.IGNORECASE,
)

FULL_HERO_RE = re.compile(
    r"<div class=\"portrait-wrap\"><div class=\"portrait-emoji\">([^<]*)</div></div>\s*"
    r"<div class=\"hero-text\">(.*)</div>\s*$",
    re.DOTALL,
)

ERA_BADGE_RE = re.compile(
    r"<div class=\"hero-era-badge\">[^<]*</div>\s*",
    re.IGNORECASE,
)

MALFORMED_HERO_RE = re.compile(
    r"(<header class=\"hero pf-profile-hero\"><div class=\"hero-inner shell pf-profile-hero__inner\">"
    r"<section class=\"hero-copy\">)(.*?)(</section><aside class=\"pf-hero-symbol\" aria-hidden=\"true\">"
    r"<span class=\"pf-hero-symbol__icon\">)([^<]*)(</span></aside></div></header>)",
    re.DOTALL,
)


def _dedupe_era_badge_emoji(copy_html: str) -> str:
    """Remove redundant leading emoji span inside hero-era-badge (symbol lives aside)."""
    return re.sub(
        r"(<div class=\"hero-era-badge\">)\s*<span>[^<]*</span>\s*",
        r"\1",
        copy_html,
        count=1,
    )


def _normalize_copy(copy_html: str) -> str:
    copy_html = ERA_BADGE_RE.sub("", copy_html)
    copy_html = copy_html.replace('<h1 class="hero-name">', "<h1>")
    copy_html = re.sub(
        r'<div class="(?:page-hero-subtitle pf-hero-latin|hero-name-latin)">[^<]*</div>\s*',
        "",
        copy_html,
        count=1,
    )
    copy_html = re.sub(
        r'<div class="hero-dates">([^<]*)</div>',
        r'<p class="pf-hero-dates">\1</p>',
        copy_html,
        count=1,
    )
    return _dedupe_era_badge_emoji(copy_html)


def transform_hero_inner(inner: str) -> str:
    inner = inner.strip()
    m_wrap = re.match(r"^<div class=\"hero-inner\">(.*)</div>\s*$", inner, re.DOTALL | re.I)
    if m_wrap:
        inner = m_wrap.group(1).strip()
    if "pf-placeholder-hero" in inner:
        body = re.sub(r"<section class=\"pf-placeholder-hero\">", "", inner, flags=re.I)
        body = re.sub(r"</section>\s*$", "", body.strip())
        return (
            '<header class="hero pf-profile-hero pf-profile-hero--placeholder">'
            '<div class="hero-inner shell"><section class="hero-copy">'
            f"{body}</section></div></header>"
        )

    m = FULL_HERO_RE.search(inner)
    if not m:
        return (
            '<header class="hero pf-profile-hero">'
            f'<div class="hero-inner shell"><section class="hero-copy">{inner}</section></div></header>'
        )

    emoji = m.group(1).strip()
    copy_html = _normalize_copy(m.group(2).strip())
    symbol = (
        f'<aside class="pf-hero-symbol" aria-hidden="true">'
        f'<span class="pf-hero-symbol__icon">{emoji}</span></aside>'
        if emoji
        else ""
    )
    h1_m = re.search(r"(<h1>[^<]*</h1>)", copy_html)
    if h1_m and symbol:
        before = copy_html[: h1_m.start()]
        after = copy_html[h1_m.end() :]
        copy_html = (
            f"{before}<div class=\"pf-profile-hero__title-row\">"
            f"{symbol}{h1_m.group(1)}</div>{after}"
        )
        symbol = ""
    return (
        '<header class="hero pf-profile-hero">'
        '<div class="hero-inner shell pf-profile-hero__inner">'
        f'<section class="hero-copy">{copy_html}</section>{symbol}'
        "</div></header>"
    )


def transform_page_html(html: str) -> tuple[str, bool]:
    """Return (html, changed)."""
    changed = False

    if "daab-hero-summary.css" not in html:
        html = html.replace(
            '<link href="../../../css/daab-nav-mega.css?v=27" rel="stylesheet"/>',
            '<link href="../../../css/daab-nav-mega.css?v=27" rel="stylesheet"/>\n'
            '<link href="../../../css/daab-hero-summary.css?v=11" rel="stylesheet"/>',
        )
        changed = True

    html = re.sub(
        r"daab-prominent-figure-profile\.css\?v=\d+",
        "daab-prominent-figure-profile.css?v=2",
        html,
    )

    def fix_malformed(m: re.Match[str]) -> str:
        copy_html = m.group(2).strip()
        if "<div class=\"hero-tags\">" in copy_html and not copy_html.rstrip().endswith("</div>"):
            copy_html += "</div>"
        return (
            f"{m.group(1)}{copy_html}{m.group(3)}{m.group(4)}{m.group(5)}"
        )

    new_html, n = MALFORMED_HERO_RE.subn(fix_malformed, html, count=1)
    if n:
        changed = True
        html = new_html

    if "pf-profile-hero" in html and "<section class=\"pf-hero\">" not in html:
        return html, changed

    def repl(m: re.Match[str]) -> str:
        return transform_hero_inner(m.group(1)) + m.group(2)

    new_html, n = HERO_BLOCK_RE.subn(repl, html, count=1)
    if n:
        changed = True
        html = new_html

    return html, changed
