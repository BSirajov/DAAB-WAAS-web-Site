#!/usr/bin/env python3
"""Repair forum page-id selectors missing descendant suffixes in
css/daab-forum-content.css (same bug class as daab-activities-layout.css).

When forum-anas or forum-sessions-organization were added to comma-separated
selector lists, many lines were inserted as bare page-id selectors while
siblings kept suffixes like `.news-card:hover` — rules then targeted `<html>`
instead of page content.
"""
from __future__ import annotations

import re
import sys

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"

PAGE_SEL = re.compile(r'^(\s*)html\[data-daab-page-id="([^"]+)"\](.*)$')
REPAIR_PAGE_IDS = (
    "forum-anas-leadership-speeches",
    "forum-sessions-organization",
)
ANAS = REPAIR_PAGE_IDS[0]

# Corrupted multi-suffix block (justify text on speech card bodies).
_JUSTIFY_BLOCK_OLD = """html[data-daab-page-id="forum-rector-speeches"] .card-body .card-text,
html[data-daab-page-id="forum-rector-speeches"] .card-body .card-quote,
html[data-daab-page-id="forum-rector-speeches"] .card-body .content-list,
html[data-daab-page-id="forum-anas-leadership-speeches"],
html[data-daab-page-id="forum-2026"] .card-body .card-text,
html[data-daab-page-id="forum-anas-leadership-speeches"],
html[data-daab-page-id="forum-2026"] .card-body .card-quote,
html[data-daab-page-id="forum-anas-leadership-speeches"]{
  text-align: justify;
  text-justify: inter-word;
}"""

_JUSTIFY_BLOCK_NEW = """html[data-daab-page-id="forum-rector-speeches"] .card-body .card-text,
html[data-daab-page-id="forum-anas-leadership-speeches"] .card-body .card-text,
html[data-daab-page-id="forum-2026"] .card-body .card-text,
html[data-daab-page-id="forum-rector-speeches"] .card-body .card-quote,
html[data-daab-page-id="forum-anas-leadership-speeches"] .card-body .card-quote,
html[data-daab-page-id="forum-2026"] .card-body .card-quote,
html[data-daab-page-id="forum-rector-speeches"] .card-body .content-list,
html[data-daab-page-id="forum-anas-leadership-speeches"] .card-body .content-list,
html[data-daab-page-id="forum-2026"] .card-body .content-list{
  text-align: justify;
  text-justify: inter-word;
}"""


def normalize_suffix(suffix: str) -> str:
    suffix = suffix.strip()
    if not suffix:
        return ""
    if suffix[0] not in (" ", ">", "+", "~", "#", ".", ":", "["):
        suffix = " " + suffix
    return suffix


def selector_suffix(line: str) -> str | None:
    """Return descendant suffix (e.g. ' .news-card:hover') or None if bare page-id only."""
    m = PAGE_SEL.match(line.rstrip())
    if not m:
        return None
    rest = m.group(3).strip()
    if not rest or rest in (",", "{"):
        return None
    if rest.endswith(","):
        rest = rest[:-1].rstrip()
    if rest.endswith(" {"):
        rest = rest[:-2].rstrip()
    elif rest.endswith("{"):
        rest = rest[:-1].rstrip()
    return rest if rest else None


def is_bare_page_line(line: str, page_id: str) -> bool:
    m = PAGE_SEL.match(line.rstrip())
    return bool(m and m.group(2) == page_id and selector_suffix(line) is None)


def fix_line_suffixes(lines: list[str], page_id: str) -> int:
    fixed = 0
    for i, line in enumerate(lines):
        if not is_bare_page_line(line, page_id):
            continue
        prev_suf = selector_suffix(lines[i - 1]) if i > 0 else None
        next_suf = selector_suffix(lines[i + 1]) if i + 1 < len(lines) else None
        suffix = normalize_suffix(prev_suf or next_suf or "")
        if not suffix:
            continue
        m = PAGE_SEL.match(line.rstrip())
        assert m
        indent = m.group(1)
        trailing = "," if line.rstrip().endswith(",") else ""
        if line.rstrip().endswith("{"):
            trailing = " {"
        lines[i] = f'{indent}html[data-daab-page-id="{page_id}"]{suffix}{trailing}'
        fixed += 1
    return fixed


def audit(text: str) -> list[str]:
    """Bare page-id selectors in lists where a neighbour carries a suffix."""
    issues: list[str] = []
    lines = text.splitlines()
    for page_id in REPAIR_PAGE_IDS:
        for i, line in enumerate(lines):
            if not is_bare_page_line(line, page_id):
                continue
            prev_suf = selector_suffix(lines[i - 1]) if i > 0 else None
            next_suf = selector_suffix(lines[i + 1]) if i + 1 < len(lines) else None
            if prev_suf or next_suf:
                issues.append(
                    f"line {i + 1}: bare {page_id} beside suffixed neighbour"
                )
        for m in re.finditer(
            rf'html\[data-daab-page-id="{re.escape(page_id)}"\]([^\s,\{{])',
            text,
        ):
            issues.append(
                f"missing combinator space on {page_id} before {m.group(1)!r}"
            )
    return issues


def repair_combinator_spacing(text: str, page_id: str) -> tuple[str, int]:
    """Insert missing descendant combinator space after page-id selectors."""
    fixed, count = re.subn(
        rf'(html\[data-daab-page-id="{re.escape(page_id)}"\])([^\s,\{{])',
        r"\1 \2",
        text,
    )
    return fixed, count


def main() -> int:
    text = CSS.read_text(encoding="utf-8")
    issues = audit(text)
    if "--audit-only" in sys.argv:
        if issues:
            print(f"ERROR: {len(issues)} bare forum selector(s):", file=sys.stderr)
            for msg in issues[:15]:
                print(f"  {msg}", file=sys.stderr)
            return 1
        print(f"OK — forum page selectors in {CSS.relative_to(ROOT)}")
        return 0

    block_fixed = 0
    if _JUSTIFY_BLOCK_OLD in text:
        text = text.replace(_JUSTIFY_BLOCK_OLD, _JUSTIFY_BLOCK_NEW, 1)
        block_fixed = 1

    lines = text.splitlines()
    line_fixed = sum(fix_line_suffixes(lines, page_id) for page_id in REPAIR_PAGE_IDS)
    new_text = "\n".join(lines) + "\n"

    issues = audit(new_text)
    if issues:
        print(f"ERROR: {len(issues)} bare forum selector(s) remain:", file=sys.stderr)
        for msg in issues[:15]:
            print(f"  {msg}", file=sys.stderr)
        return 1

    if block_fixed or line_fixed:
        CSS.write_text(new_text, encoding="utf-8", newline="\n")

    spacing_fixed = 0
    spacing_text = CSS.read_text(encoding="utf-8")
    for page_id in REPAIR_PAGE_IDS:
        spacing_text, n = repair_combinator_spacing(spacing_text, page_id)
        spacing_fixed += n
    if spacing_fixed:
        CSS.write_text(spacing_text, encoding="utf-8", newline="\n")

    print(
        f"Fixed {line_fixed} bare selector line(s)"
        f"{f' + {block_fixed} justify block' if block_fixed else ''}"
        f"{f' + {spacing_fixed} combinator space(s)' if spacing_fixed else ''}"
        f" in {CSS.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
