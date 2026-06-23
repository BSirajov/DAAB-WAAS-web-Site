#!/usr/bin/env python3
"""Find words/phrases starting with 'kart' in AZ site content."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

WORD_RE = re.compile(r"(?i)(?<![\wəğıöüşçƏĞİÖÜŞÇ])(kart[\wəğıöüşçƏĞİÖÜŞÇ'-]*)")

SCAN = [
    ROOT / "az",
    ROOT / "i18n",
    ROOT / "js" / "scientists-list-catalog.js",
]


def scan_file(path: Path, hits: dict[str, list[tuple[str, str, str]]]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return
    rel = path.relative_to(ROOT).as_posix()
    for m in WORD_RE.finditer(text):
        token = m.group(1)
        start = max(0, m.start() - 50)
        end = min(len(text), m.end() + 50)
        ctx = re.sub(r"\s+", " ", text[start:end]).strip()
        hits.setdefault(token.lower(), []).append((rel, token, ctx))


def main() -> None:
    hits: dict[str, list[tuple[str, str, str]]] = {}
    for base in SCAN:
        if base.is_file():
            scan_file(base, hits)
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() in {".html", ".json", ".js", ".xml", ".txt"}:
                scan_file(path, hits)

    print("AZ site — tokens/phrases starting with 'kart' (case-insensitive)\n")
    for key in sorted(hits):
        entries = hits[key]
        # dedupe by file+token
        seen = set()
        unique = []
        for item in entries:
            if item[:2] not in seen:
                seen.add(item[:2])
                unique.append(item)
        print(f"**{unique[0][1]}** ({len(unique)} occurrence(s))")
        for rel, token, ctx in unique:
            print(f"  - `{rel}`")
            print(f"    …{ctx}…")
        print()


if __name__ == "__main__":
    main()
