#!/usr/bin/env python3
"""Remove duplicate html[data-daab-page-id=...] lines within the same CSS rule block."""
from __future__ import annotations

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"


def norm_selector(line: str) -> str | None:
    s = line.strip()
    if not s.startswith("html[data-daab-page-id="):
        return None
    if s.endswith(" {"):
        s = s[:-2].strip()
    return s.rstrip(",").strip()


def dedupe(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    seen: set[str] = set()
    removed = 0

    for line in lines:
        key = norm_selector(line)
        if key:
            if key in seen:
                removed += 1
                continue
            seen.add(key)
        if line.strip().endswith("{"):
            seen = set()
        out.append(line)

    return "\n".join(out) + "\n", removed


if __name__ == "__main__":
    raw = CSS.read_text(encoding="utf-8")
    fixed, n = dedupe(raw)
    if n:
        CSS.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"Removed {n} duplicate selector line(s) from {CSS.name}")
