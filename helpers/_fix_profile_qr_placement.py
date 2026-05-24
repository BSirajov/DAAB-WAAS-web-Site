"""Move card-qr-link out of card-body for cards where QR was left nested after card-bio."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES

# Cards known to have QR inside .card-body (not a direct child of .card).
NESTED_QR_CARD_IDS = (
    "bakhtiyar-sirajov",
    "sevinj-mammadova",
    "vehid-geruslu",
    "seymur-nasirov",
    "arzu-qurbanova",
)


def fix_card(html: str, card_id: str) -> tuple[str, bool]:
    start = html.find(f'<div class="card" id="{card_id}"')
    if start == -1:
        return html, False
    end = html.find('<div class="card"', start + 10)
    chunk = html[start : end if end != -1 else len(html)]
    m = re.search(
        r"(    <div class=\"card-bio\">.*?</div>)\s*"
        r"(<a class=\"card-qr-link\"[^>]*>.*?</a>)\s*"
        r"\n  </div>\n</div>",
        chunk,
        re.DOTALL,
    )
    if not m:
        return html, False
    fixed = f"{m.group(1)}\n  </div>\n  {m.group(2)}\n</div>"
    new_chunk = chunk[: m.start()] + fixed + chunk[m.end() :]
    return html[:start] + new_chunk + html[start + len(chunk) :], True


def main() -> None:
    for path in (AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES):
        text = path.read_text(encoding="utf-8")
        fixed_ids: list[str] = []
        for cid in NESTED_QR_CARD_IDS:
            text, ok = fix_card(text, cid)
            if ok:
                fixed_ids.append(cid)
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{path.relative_to(ROOT)}: {fixed_ids}")


if __name__ == "__main__":
    main()
