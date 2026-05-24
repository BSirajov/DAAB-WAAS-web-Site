"""Move QR out of .card-portrait so grid layout works without display:contents."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES

PORTRAIT_RE = re.compile(
    r'<div class="card-portrait">\s*'
    r'(<div class="card-avatar card-photo">.*?</div>)\s*'
    r'(<a class="card-qr-link"[^>]*>.*?</a>)\s*'
    r'</div>\s*'
    r'(<div class="card-body">.*?<div class="card-bio">.*?</div>\s*</div>)',
    re.DOTALL,
)


def unwrap_cards(html: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return m.group(1) + "\n  " + m.group(3) + "\n  " + m.group(2)

    return PORTRAIT_RE.sub(repl, html), count


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "card-portrait" not in text:
        print(f"skip (no portrait): {path.relative_to(ROOT)}")
        return
    new_text, n = unwrap_cards(text)
    if n == 0:
        print(f"warn: no cards updated in {path.relative_to(ROOT)}")
        return
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"updated {n} cards in {path.relative_to(ROOT)}")


def main() -> None:
    for p in (AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES):
        process(p)


if __name__ == "__main__":
    main()
