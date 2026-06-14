#!/usr/bin/env python3
"""Set descriptive alt text on executive board QR images."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

QR_LABEL = {"az": "profil QR kodu", "en": "profile QR code"}


def fix_file(path: Path, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    label = QR_LABEL[lang]
    out: list[str] = []
    last = 0
    changed = False
    for m in re.finditer(r'<img class="board-card-qr[^"]*"[^>]*alt=""', text):
        before = text[last : m.start()]
        names = re.findall(r'class="person-name-link"[^>]*>([^<]+)<', before)
        chunk = text[m.start() : m.end()]
        if names:
            name = re.sub(r",?\s*(Prof\.?\s*Dr\.?|Dr\.?)\s*$", "", names[-1].strip(), flags=re.I)
            alt = f'{name} — {label}'
            chunk = chunk.replace('alt=""', f'alt="{alt}"', 1)
            changed = True
        out.append(before)
        out.append(chunk)
        last = m.end()
    out.append(text[last:])
    if changed:
        path.write_text("".join(out), encoding="utf-8")
    return changed


def main() -> None:
    for lang in ("az", "en"):
        path = ROOT / lang / "executive-board.html"
        if fix_file(path, lang):
            print(f"Updated {path.relative_to(ROOT)}")
        else:
            print(f"No change {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
