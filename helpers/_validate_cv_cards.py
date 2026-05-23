"""Validate CV card HTML structure."""
import re

from _paths import ROOT, AZ_SCIENTISTS_PROFILES

text = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")
starts = [m.start() for m in re.finditer(r'<div class="card" data-country-name', text)]
issues = []
for i, pos in enumerate(starts):
    end = starts[i + 1] if i + 1 < len(starts) else text.find('<div class="no-results"')
    chunk = text[pos:end]
    if chunk.count('class="card-meta"') != 1:
        issues.append((i + 1, "meta"))
    email_row = chunk.count('card-meta-row')
    if email_row not in (1, 2):
        issues.append((i + 1, "meta-rows"))
    if '</span>\n      <p class="card-country">' not in chunk and '</span>\r\n      <p class="card-country">' not in chunk:
        if '<p class="card-country">' in chunk and '</span>' not in chunk.split("card-country")[0][-30:]:
            issues.append((i + 1, "header-span"))
    tail = chunk.strip()[-400:]
    if 'class="card-body"' not in chunk or tail.count("</div>") < 2:
        issues.append((i + 1, "closing"))

print("cards", len(starts))
print("issues", len(issues), issues[:15])
