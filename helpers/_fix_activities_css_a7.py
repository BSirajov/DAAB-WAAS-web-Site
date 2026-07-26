#!/usr/bin/env python3
"""A7: tokenize fonts, scope activities CSS, trim non-layout !important."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_PATH = ROOT / "css" / "daab-activities-page.css"
PAGE = 'html[data-daab-page-id="activities-news"]'

KEEP_IMPORTANT_PROPS = {
    "display",
    "position",
    "top",
    "right",
    "bottom",
    "left",
    "inset",
    "width",
    "height",
    "min-width",
    "max-width",
    "min-height",
    "max-height",
    "flex",
    "flex-direction",
    "flex-wrap",
    "flex-grow",
    "flex-shrink",
    "flex-basis",
    "align-items",
    "align-self",
    "justify-content",
    "justify-self",
    "place-items",
    "place-content",
    "gap",
    "row-gap",
    "column-gap",
    "grid",
    "grid-template",
    "grid-template-columns",
    "grid-template-rows",
    "grid-template-areas",
    "grid-area",
    "grid-column",
    "grid-row",
    "grid-auto-flow",
    "float",
    "clear",
    "z-index",
    "overflow",
    "overflow-x",
    "overflow-y",
    "visibility",
    "opacity",
    "transform",
    "content",
    "pointer-events",
    "mask-image",
    "mix-blend-mode",
    "aspect-ratio",
    "object-fit",
    "object-position",
}

FONT_INTER_RE = re.compile(
    r"font-family\s*:\s*Inter\s*,\s*system-ui\s*,\s*-apple-system\s*,\s*"
    r"(?:\"Segoe UI\"|Segoe UI)\s*,\s*sans-serif\s*(!important)?",
    re.I,
)
FONT_PLAYFAIR_RE = re.compile(
    r"font-family\s*:\s*['\"]Playfair Display['\"]\s*,\s*serif\s*(!important)?",
    re.I,
)

TYPO_BLOCK_RE = re.compile(
    r"/\* ===== Global typography normalization \(activities page only\) ===== \*/"
    r".*?"
    r"(?=/\* Egypt medal gallery \*/)",
    re.S,
)

NEW_TYPO_BLOCK = f"""\
/* ===== Global typography normalization (activities page only) ===== */
{PAGE}{{
    font-family: var(--font-sans);
    font-size: 15px;
    line-height: 1.45;
    letter-spacing: 0;
}}
{PAGE} .news-feed,
{PAGE} .sidebar,
{PAGE} .card-text,
{PAGE} .timeline-list,
{PAGE} .card-source,
{PAGE} .widget-body,
{PAGE} .widget-head{{
    font-family: var(--font-sans);
}}
{PAGE} h1,
{PAGE} h2,
{PAGE} h3,
{PAGE} h4,
{PAGE} h5,
{PAGE} h6,
{PAGE} .page-hero h1{{
    font-family: var(--font-serif);
    line-height: 1.25;
}}
{PAGE} .news-card .card-header .card-title{{
    line-height: 1.38;
}}
{PAGE} .card-body p,
{PAGE} .card-text{{
    margin-bottom: 10px;
}}
{PAGE} li{{
    margin-bottom: 2px;
    padding-top: 2px;
    padding-bottom: 2px;
}}
{PAGE} .timeline-list li{{
    line-height: 1.3;
}}
{PAGE} .card-body{{
    line-height: 1.45;
}}
{PAGE} .news-feed .card-body p,
{PAGE} .news-feed .card-text,
{PAGE} .news-feed .card-body li{{
    text-align: justify;
    text-justify: inter-word;
    hyphens: auto;
}}
"""


def protect_comments(css: str) -> tuple[str, list[str]]:
    comments: list[str] = []

    def repl(match: re.Match[str]) -> str:
        comments.append(match.group(0))
        return f"___COMMENT_{len(comments) - 1}___"

    return re.sub(r"/\*.*?\*/", repl, css, flags=re.S), comments


def restore_comments(css: str, comments: list[str]) -> str:
    for i, comment in enumerate(comments):
        css = css.replace(f"___COMMENT_{i}___", comment)
    return css


def strip_non_layout_important(css: str) -> tuple[str, int]:
    removed = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal removed
        prop = match.group(1).lower()
        value = match.group(2)
        if prop in KEEP_IMPORTANT_PROPS:
            return match.group(0)
        removed += 1
        return f"{prop}:{value}"

    out = re.sub(
        r"([a-zA-Z-]+)\s*:\s*([^;{}]+?)\s*!important",
        repl,
        css,
    )
    return out, removed


def split_selectors(selector_group: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in selector_group:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            part = "".join(buf).strip()
            if part:
                parts.append(part)
            buf = []
            continue
        buf.append(ch)
    part = "".join(buf).strip()
    if part:
        parts.append(part)
    return parts


def prefix_selector(sel: str) -> str:
    s = sel.strip()
    if not s:
        return s
    if s.startswith("___COMMENT_"):
        return s
    if s.startswith("@") or s in {"from", "to"}:
        return s
    if re.fullmatch(r"\d+%", s):
        return s
    if s.startswith(":root"):
        return s
    if 'data-daab-page-id="activities-news"' in s:
        return s
    if s.startswith("html[") or s.startswith("html:"):
        return s
    return f"{PAGE} {s}"


def prefix_rule_selectors(css: str) -> str:
    def transform_block(block: str) -> str:
        def at_repl(m: re.Match[str]) -> str:
            head, inner = m.group(1), m.group(2)
            return f"{head}{{{transform_block(inner)}}}"

        block = re.sub(
            r"(@(?:media|supports|layer)[^{]*)\{((?:[^{}]|\{[^{}]*\})*)\}",
            at_repl,
            block,
            flags=re.S,
        )

        def rule_repl(m: re.Match[str]) -> str:
            selectors, body = m.group(1), m.group(2)
            raw = selectors.strip()
            if not raw or raw.startswith("@"):
                return m.group(0)
            # Comments may sit in the selector chunk (e.g. COMMENT\\n  .foo).
            leading_comments = "".join(re.findall(r"___COMMENT_\d+___", selectors))
            parts = split_selectors(selectors)
            cleaned_parts: list[str] = []
            for part in parts:
                cleaned = re.sub(r"___COMMENT_\d+___", "", part).strip()
                if cleaned:
                    cleaned_parts.append(cleaned)
            if not cleaned_parts:
                return m.group(0)
            if all(re.fullmatch(r"\d+%|from|to", p) for p in cleaned_parts):
                return m.group(0)
            prefixed = ",".join(prefix_selector(p) for p in cleaned_parts)
            return f"{leading_comments}{prefixed}{{{body}}}"

        return re.sub(r"([^{}]+)\{([^{}]*)\}", rule_repl, block)

    return transform_block(css)


def main() -> int:
    original = CSS_PATH.read_text(encoding="utf-8")
    if original.lstrip().startswith(PAGE):
        raise SystemExit("CSS already looks transformed — aborting to avoid double-prefix")

    css = original
    if not TYPO_BLOCK_RE.search(css):
        raise SystemExit("Typography block marker not found — aborting")
    css = TYPO_BLOCK_RE.sub(NEW_TYPO_BLOCK, css, count=1)

    css = FONT_INTER_RE.sub("font-family: var(--font-sans)", css)
    css = FONT_PLAYFAIR_RE.sub("font-family: var(--font-serif)", css)

    css, comments = protect_comments(css)
    css = prefix_rule_selectors(css)
    css = restore_comments(css, comments)

    css, _removed = strip_non_layout_important(css)
    css = re.sub(r"\n{3,}", "\n\n", css)

    if css.count("{") != css.count("}"):
        raise SystemExit("Brace imbalance after transform — aborting write")

    # First .content-wrap rule (layout) must be scoped — not only a later override.
    first_cw = re.search(r"\.content-wrap\s*\{", css)
    if not first_cw:
        raise SystemExit("No .content-wrap rule found — aborting write")
    window_start = max(0, first_cw.start() - len(PAGE) - 2)
    window = css[window_start : first_cw.start()]
    if PAGE not in window:
        raise SystemExit("Failed to scope first .content-wrap — aborting write")

    CSS_PATH.write_text(css, encoding="utf-8", newline="\n")

    marker = 'data-daab-page-id="activities-news"'
    print(f"Wrote {CSS_PATH.relative_to(ROOT)}")
    print(f"!important: {original.count('!important')} -> {css.count('!important')}")
    print(f"Inter leftovers: {len(re.findall(r'Inter', css))}")
    print(f"Playfair leftovers: {len(re.findall(r'Playfair', css))}")
    print(f"var(--font-sans): {css.count('var(--font-sans)')}")
    print(f"page-id markers: {css.count(marker)}")
    print(f"starts with comment: {css.lstrip().startswith('/*')}")
    print("first content-wrap scoped: True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
