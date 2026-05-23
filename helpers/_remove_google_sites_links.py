"""Remove all hyperlinks to sites.google.com from site data and HTML."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import AZ_SCIENTISTS_LIST, ROOT

GOOGLE_SITES = re.compile(r"https://sites\.google\.com\S*")
CARD_OPEN = re.compile(
    r'<a (class="(?:chair-card|co-card|person-card)") '
    r'href="https://sites\.google\.com[^"]*" '
    r'rel="noopener noreferrer" target="_blank">',
)


def strip_data_files() -> int:
    count = 0
    for name in ("js/scientists-catalog-data.js", AZ_SCIENTISTS_LIST.relative_to(ROOT).as_posix()):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        found = len(GOOGLE_SITES.findall(text))
        text = GOOGLE_SITES.sub("", text)
        text = re.sub(r'"url":\s*"\s*\n', '"url": ""\n', text)
        path.write_text(text, encoding="utf-8", newline="")
        count += found
        print(f"  {name}: cleared {found} URL(s)")
    return count


def strip_executive_board() -> int:
    path = ROOT / "executive_board_az.html"
    text = path.read_text(encoding="utf-8")
    n = len(CARD_OPEN.findall(text))
    text = CARD_OPEN.sub(r"<div \1>", text)
    text = text.replace("</a>", "</div>")
    # Ensure each card wrapper closes before sibling card/grid/section
    # Close each card wrapper after person-body (before next card or section end)
    text = re.sub(
        r'(<div class="person-country">[^<]*</div>\s*</div>)\s*(?=<div class="(?:co-card|person-card)|</section>)',
        r"\1\n</div>\n",
        text,
    )
    path.write_text(text, encoding="utf-8", newline="")
    print(f"  executive_board_az.html: converted {n} card link(s) to divs")
    return n


def verify() -> bool:
    ok = True
    for path in ROOT.rglob("*"):
        if path.suffix not in {".html", ".js"}:
            continue
        if "helpers" in path.parts or "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "sites.google.com" in text:
            print(f"  still found in {path.relative_to(ROOT)}")
            ok = False
    return ok


def main() -> int:
    print("Removing Google Sites links...")
    strip_data_files()
    strip_executive_board()
    print()
    if verify():
        print("OK — no sites.google.com references remain.")
        return 0
    print("Some references may remain — review output above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
