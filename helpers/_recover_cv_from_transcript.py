"""Recover az/scientists/profiles.html card catalog from agent transcript."""
import json
import re
from pathlib import Path

from _paths import AZ_SCIENTISTS_PROFILES, ROOT

TRANSCRIPT = Path(
    r"C:\Users\BSira\.cursor\projects\c-Users-BSira-Documents-GitHub-DAAB-WAAS-web-site"
    r"\agent-transcripts\2d0cb383-2b26-4ef8-b10c-07f813cba3d4"
    r"\2d0cb383-2b26-4ef8-b10c-07f813cba3d4.jsonl"
)

CV = AZ_SCIENTISTS_PROFILES

best_cards = ""
best_count = 0

for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
    if "data-country-name" not in line:
        continue
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    text = json.dumps(obj, ensure_ascii=False)
    count = text.count("data-country-name")
    if count <= best_count:
        continue
    # try to extract cards-grid section
    for m in re.finditer(
        r'<div class="cards-grid">.*?</div>\s*</section>',
        text,
        re.S,
    ):
        block = m.group(0)
        c = block.count("data-country-name")
        if c > best_count:
            best_count = c
            best_cards = block

print("best card count in snippet:", best_count)
if best_count < 80:
    # fallback: collect all unique card blocks from entire transcript text
    full = TRANSCRIPT.read_text(encoding="utf-8")
    cards = re.findall(
        r'<div class="card" data-country-name[^>]*>.*?</div>\s*</div>\s*</div>',
        full,
        re.S,
    )
    print("regex cards in full transcript:", len(cards))
    if len(cards) >= 80:
        best_cards = (
            '<div class="cards-grid">\n\n'
            + "\n\n".join(cards)
            + "\n\n  </div>\n</section>"
        )
        best_count = len(cards)

if best_count < 80:
    raise SystemExit("Could not recover enough cards")

cv = CV.read_text(encoding="utf-8")
start = cv.find('<section class="catalog-section" id="scientists-catalog">')
end = cv.find('<div class="no-results"')
if start < 0 or end < 0:
    raise SystemExit("CV shell boundaries missing")

if best_cards.startswith("<div class=\"cards-grid\">"):
    catalog = (
        '<section class="catalog-section" id="scientists-catalog">\n  '
        + best_cards
    )
    if not catalog.rstrip().endswith("</section>"):
        catalog = catalog.rstrip() + "\n</section>\n  "
else:
    catalog = (
        '<section class="catalog-section" id="scientists-catalog">\n  '
        + best_cards
        + "\n  "
    )

CV.write_text(cv[:start] + catalog + cv[end:], encoding="utf-8")
print(f"Restored {best_count} cards into {CV}")
