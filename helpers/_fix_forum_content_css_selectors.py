#!/usr/bin/env python3
"""Repair forum-anas-leadership-speeches selectors missing descendant suffixes in
css/daab-forum-content.css (same bug class as daab-activities-layout.css).

When forum-anas was added to comma-separated selector lists, many lines were
inserted as bare page-id selectors while siblings kept suffixes like
`.news-card:hover` — rules then targeted `<html>` instead of page content.
"""
from __future__ import annotations

import re
import sys

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"

PAGE_SEL = re.compile(r'^(\s*)html\[data-daab-page-id="([^"]+)"\](.*)$')
ANAS = "forum-anas-leadership-speeches"

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


def is_bare_anas_line(line: str) -> bool:
    m = PAGE_SEL.match(line.rstrip())
    return bool(m and m.group(2) == ANAS and selector_suffix(line) is None)


def fix_line_suffixes(lines: list[str]) -> int:
    fixed = 0
    for i, line in enumerate(lines):
        if not is_bare_anas_line(line):
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
        lines[i] = f'{indent}html[data-daab-page-id="{ANAS}"]{suffix}{trailing}'
        fixed += 1
    return fixed


def audit(text: str) -> list[str]:
    """Bare anas selectors in lists where a neighbour carries a suffix."""
    issues: list[str] = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not is_bare_anas_line(line):
            continue
        prev_suf = selector_suffix(lines[i - 1]) if i > 0 else None
        next_suf = selector_suffix(lines[i + 1]) if i + 1 < len(lines) else None
        if prev_suf or next_suf:
            issues.append(f"line {i + 1}: bare anas beside suffixed neighbour")
    for m in re.finditer(
        r'html\[data-daab-page-id="forum-anas-leadership-speeches"\]([^\s,\{])',
        text,
    ):
        issues.append(f"missing combinator space before {m.group(1)!r}")
    return issues


def repair_anas_combinator_spacing(text: str) -> tuple[str, int]:
    """Insert missing descendant combinator space after anas page-id selectors."""
    fixed, count = re.subn(
        r'(html\[data-daab-page-id="forum-anas-leadership-speeches"\])([^\s,\{])',
        r"\1 \2",
        text,
    )
    return fixed, count


def main() -> int:
    text = CSS.read_text(encoding="utf-8")
    issues = audit(text)
    if "--audit-only" in sys.argv:
        if issues:
            print(f"ERROR: {len(issues)} bare anas selector(s):", file=sys.stderr)
            for msg in issues[:10]:
                print(f"  {msg}", file=sys.stderr)
            return 1
        print(f"OK — forum-anas selectors in {CSS.relative_to(ROOT)}")
        return 0

    block_fixed = 0
    if _JUSTIFY_BLOCK_OLD in text:
        text = text.replace(_JUSTIFY_BLOCK_OLD, _JUSTIFY_BLOCK_NEW, 1)
        block_fixed = 1

    lines = text.splitlines()
    line_fixed = fix_line_suffixes(lines)
    new_text = "\n".join(lines) + "\n"

    issues = audit(new_text)
    if issues:
        print(f"ERROR: {len(issues)} bare anas selector(s) remain:", file=sys.stderr)
        for msg in issues[:10]:
            print(f"  {msg}", file=sys.stderr)
        return 1

    if block_fixed or line_fixed:
        CSS.write_text(new_text, encoding="utf-8", newline="\n")

    spacing_text, spacing_fixed = repair_anas_combinator_spacing(CSS.read_text(encoding="utf-8"))
    if spacing_fixed:
        CSS.write_text(spacing_text, encoding="utf-8", newline="\n")
        new_text = spacing_text

    print(
        f"Fixed {line_fixed} anas selector line(s)"
        f"{f' + {block_fixed} justify block' if block_fixed else ''}"
        f"{f' + {spacing_fixed} combinator space(s)' if spacing_fixed else ''}"
        f" in {CSS.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
