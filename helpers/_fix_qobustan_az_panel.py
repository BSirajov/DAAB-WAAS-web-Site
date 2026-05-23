"""Remove English column from QOBUSTAN Nobel panel on AZ activities page."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PATH = ROOT / "az" / "activities.html"


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text

    text, n = re.subn(
        r'(<div class="open-letter-bilingual">)\s*'
        r'<div class="open-letter-column"><h3>English</h3>.*?</div>\s*',
        r"\1",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        raise SystemExit(f"Expected 1 English column removal, got {n}")

    text = text.replace("<h3>Azərbaycanca</h3>", "", 1)
    text = text.replace(
        '<div class="open-letter-bilingual"><div class="open-letter-column">',
        '<div class="open-letter-bilingual open-letter-single"><div class="open-letter-column">',
        1,
    )

    if text == original:
        raise SystemExit("No changes made")

    PATH.write_text(text, encoding="utf-8", newline="\n")
    print(f"Updated {PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
