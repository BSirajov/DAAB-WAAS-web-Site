#!/usr/bin/env python3
"""Scale font-size in title/heading CSS rules by --daab-title-scale (default 0.7 = −30%)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

SCALE = 0.7
CSS_DIR = ROOT / "css"

TITLE_SELECTOR = re.compile(
    r"h[1-6]\b|"
    r"panel-title|card-title|section-title|page-title|"
    r"section-head|section-heading|values-title|"
    r"page-hero|forum-hero|story-head|mv-section-head|mv-cta|"
    r"join-banner|photos-gallery-head|"
    r"flyer-brand-block|flyer-hero|flyer-section-title|"
    r"presentation-toc-title|"
    r"footer-brand|intro-card|section-label|success-screen|"
    r"hero-summary-title|activities-summary-title|"
    r"sri-title|\.foot\b|"
    r"\.panel h2|\.value h2|\.cta h2|\.card h3|\.qa-item h3",
    re.I,
)

EXCLUDE_SELECTOR = re.compile(
    r"page-hero-subtitle|hero-text|panel-copy|\.lead\b|card-header|"
    r"search-input|search-icon|search-close|search-hint|search-empty|search-prompt|"
    r"price-box|\.stat\b|card-tag|nav-link|nav-brand|breadcrumb|"
    r"card-desc|card-body p|\.muted|lang-label|section-label span|"
    r"card-title|card-name|card-country|card-role|card-meta|card-email|"
    r"card-bio|card-profile-header|card-tts|scientists-profiles|"
    r"daab-section-nav-title",
    re.I,
)

NUM = re.compile(r"(\d+(?:\.\d+)?)(px|rem|em|vw|vh)")

FONT_SIZE_DECL = re.compile(
    r"(font-size\s*:\s*)([^;}{]+)",
    re.I,
)


def _fmt(n: float, unit: str) -> str:
    if unit in ("px", "vw", "vh"):
        s = f"{n:.2f}".rstrip("0").rstrip(".")
    else:
        s = f"{n:.4f}".rstrip("0").rstrip(".")
    return f"{s}{unit}"


def scale_size_token(token: str) -> str:
    token = token.strip()
    if not token or token.startswith("var(") or token.startswith("calc("):
        return token
    m = NUM.fullmatch(token)
    if not m:
        return token
    value, unit = float(m.group(1)), m.group(2)
    return _fmt(value * SCALE, unit)


def scale_font_size_value(raw: str) -> str:
    value = raw.strip()
    if not value or "var(" in value:
        return value

    if value.lower().startswith("clamp(") and value.endswith(")"):
        inner = value[6:-1]
        parts = [p.strip() for p in inner.split(",")]
        if len(parts) == 3:
            scaled = ", ".join(scale_size_token(p) for p in parts)
            return f"clamp({scaled})"
        return value

    return scale_size_token(value)


def is_title_selector(selector: str) -> bool:
    if EXCLUDE_SELECTOR.search(selector):
        return False
    return bool(TITLE_SELECTOR.search(selector))


def split_rule_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return (prefix, selector, body) for each rule; prefix includes @media wrappers."""
    blocks: list[tuple[str, str, str]] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "@":
            start = i
            depth = 0
            while i < n:
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            at_block = text[start:i]
            inner_start = at_block.find("{") + 1
            inner_end = at_block.rfind("}")
            prefix = at_block[: inner_start]
            suffix = at_block[inner_end:]
            inner = at_block[inner_start:inner_end]
            for sel, body in split_plain_rules(inner):
                blocks.append((prefix, sel, body + suffix))
            continue

        if text[i] == "{":
            i += 1
            continue

        sel_start = i
        while i < n and text[i] != "{":
            i += 1
        if i >= n:
            break
        selector = text[sel_start:i].strip()
        i += 1
        body_start = i
        depth = 1
        while i < n and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[body_start : i - 1]
        blocks.append(("", selector, "}"))
        blocks[-1] = ("", selector, body)
    return blocks


def split_plain_rules(text: str) -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i] in " \t\n\r":
            i += 1
        if i >= n:
            break
        sel_start = i
        while i < n and text[i] != "{":
            i += 1
        if i >= n:
            break
        selector = text[sel_start:i].strip()
        i += 1
        body_start = i
        depth = 1
        while i < n and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[body_start : i - 1]
        if selector:
            rules.append((selector, body))
    return rules


def scale_rule_body(selector: str, body: str) -> str:
    if not is_title_selector(selector):
        return body

    def repl(m: re.Match[str]) -> str:
        prefix, raw = m.group(1), m.group(2)
        return prefix + scale_font_size_value(raw)

    return FONT_SIZE_DECL.sub(repl, body)


def process_css(text: str) -> tuple[str, int]:
    """Scale title font sizes; return (new_text, change_count)."""
    changes = 0
    out: list[str] = []
    pos = 0

    for prefix, selector, body in split_rule_blocks(text):
        # Reconstruct block from split — split_rule_blocks loses structure for top-level.
        pass

    # Simpler line-oriented approach: walk selectors via regex on full file
    result_parts: list[str] = []
    idx = 0
    pattern = re.compile(r"([^{}@]+)\{([^{}]*)\}", re.S)

    def replace_rule(m: re.Match[str]) -> str:
        nonlocal changes
        selector, body = m.group(1).strip(), m.group(2)
        if not selector or selector.startswith("@") or "{" in selector:
            return m.group(0)
        new_body = scale_rule_body(selector, body)
        if new_body != body:
            changes += 1
        return f"{selector}{{{new_body}}}"

    # Handle @media blocks recursively
    def process_segment(segment: str) -> str:
        nonlocal changes
        out_seg = []
        last = 0
        for m in re.finditer(r"(@[^{]+\{)", segment):
            before = segment[last : m.start()]
            out_seg.append(pattern.sub(replace_rule, before))
            at_start = m.start()
            depth = 0
            j = at_start
            while j < len(segment):
                if segment[j] == "{":
                    depth += 1
                elif segment[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            at_block = segment[at_start:j]
            head = at_block[: at_block.index("{") + 1]
            inner = at_block[at_block.index("{") + 1 : -1]
            tail = "}"
            out_seg.append(head + process_segment(inner) + tail)
            last = j
        out_seg.append(pattern.sub(replace_rule, segment[last:]))
        return "".join(out_seg)

    new_text = process_segment(text)
    return new_text, changes


def main() -> None:
    total_files = 0
    total_changes = 0
    for path in sorted(CSS_DIR.glob("*.css")):
        if path.name in ("daab-tokens.css", "daab-site-background.css"):
            continue
        original = path.read_text(encoding="utf-8")
        updated, changes = process_css(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            total_files += 1
            total_changes += changes
            print(f"{path.name}: {changes} rule(s)")
    print(f"Updated {total_files} file(s), {total_changes} rule(s) scaled by {SCALE}")


if __name__ == "__main__":
    main()
