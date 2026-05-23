"""Rebuild flat catalog from card blocks in scientists_card_view_az.html."""
import re

from _paths import AZ_SCIENTISTS_PROFILES, ROOT

CV = AZ_SCIENTISTS_PROFILES
text = CV.read_text(encoding="utf-8")

cards = re.findall(
    r'<div class="card" data-country-name[^>]*>.*?</div>\s*</div>\s*</div>',
    text,
    re.S,
)
print(f"Found {len(cards)} cards")

start = text.find('<section class="catalog-section"')
if start < 0:
    start = text.find('<section class="country-section"')
end = text.find('<div class="no-results"')
if start < 0 or end < 0:
    raise SystemExit("boundaries not found")

catalog = (
    '<section class="catalog-section" id="scientists-catalog">\n'
    '  <div class="cards-grid">\n\n'
    + "\n\n".join(cards)
    + "\n\n  </div>\n</section>\n  "
)
text = text[:start] + catalog + text[end:]
CV.write_text(text, encoding="utf-8")
print("Rebuilt catalog")
