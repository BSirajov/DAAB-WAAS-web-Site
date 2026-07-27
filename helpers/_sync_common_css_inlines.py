#!/usr/bin/env python3
"""Re-inline css/daab-tokens.css and css/daab-site-background.css into daab-common.css."""
from __future__ import annotations

from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    from helpers._paths import ROOT  # type: ignore

COMMON = ROOT / "css" / "daab-common.css"
TOKENS = ROOT / "css" / "daab-tokens.css"
BG = ROOT / "css" / "daab-site-background.css"

HEADER = "/* === DAAB SHARED DESIGN SYSTEM === */"
TOKENS_MARK = "/* --- daab-tokens.css (inlined) --- */"
BG_MARK = "/* --- daab-site-background.css (inlined) --- */"


def sync() -> bool:
    tokens = TOKENS.read_text(encoding="utf-8").strip()
    bg = BG.read_text(encoding="utf-8").strip()
    common = COMMON.read_text(encoding="utf-8")

    if TOKENS_MARK not in common or BG_MARK not in common:
        raise SystemExit("Missing inlined markers in daab-common.css")

    i_tokens = common.index(TOKENS_MARK)
    i_bg = common.index(BG_MARK)
    if i_bg <= i_tokens:
        raise SystemExit("Invalid marker order in daab-common.css")

    # Everything after the inlined background block is the rest of common.css.
    # Background file ends with the prefers-reduced-transparency media block.
    bg_tail = bg[-120:].strip()
    after_bg_start = common.find(bg_tail, i_bg)
    if after_bg_start == -1:
        raise SystemExit("Could not locate end of inlined site-background block")
    after_bg_start += len(bg_tail)
    # Skip trailing whitespace/newlines after the bg file content
    while after_bg_start < len(common) and common[after_bg_start] in "\r\n":
        after_bg_start += 1

    prefix = common[:i_tokens]
    if not prefix.rstrip().endswith(HEADER):
        # Keep any bytes before tokens mark, but ensure header exists once.
        header_at = common.find(HEADER)
        prefix = common[:header_at] + HEADER + "\n" if header_at != -1 else HEADER + "\n"

    new = (
        prefix.rstrip()
        + "\n"
        + TOKENS_MARK
        + "\n"
        + tokens
        + "\n\n"
        + BG_MARK
        + "\n"
        + bg
        + "\n\n"
        + common[after_bg_start:]
    )
    if new == common:
        print("daab-common.css already in sync")
        return False
    COMMON.write_text(new, encoding="utf-8", newline="\n")
    print(f"Updated css/daab-common.css ({len(common.splitlines())} -> {len(new.splitlines())} lines)")
    return True


if __name__ == "__main__":
    sync()
