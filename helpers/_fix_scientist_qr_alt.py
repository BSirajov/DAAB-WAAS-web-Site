#!/usr/bin/env python3
"""Set descriptive alt text on scientist profile QR code images."""
from __future__ import annotations

import re

from _paths import ROOT

CARD_RE = re.compile(
    r'(<div class="card"[^>]*>.*?<img class="card-qr"[^>]*alt=")(")',
    re.DOTALL,
)
NAME_RE = re.compile(r'<span class="card-name">([^<]+)')


def fix_file(path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        block = m.group(0)
        nm = NAME_RE.search(block)
        if not nm:
            return m.group(0)
        name = re.sub(r"\s+", " ", nm.group(1)).strip()
        prefix = "QR kodu:" if "/az/" in path.as_posix() else "QR code:"
        changed = True
        return block.replace('alt=""', f'alt="{prefix} {name}"', 1)

    new_text = CARD_RE.sub(repl, text)
    if changed:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    n = 0
    for rel in ("az/scientists/profiles.html", "en/scientists/profiles.html"):
        path = ROOT / rel
        if path.is_file() and fix_file(path):
            n += 1
            print(f"Updated {rel}")
    print(f"Done ({n} file(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
