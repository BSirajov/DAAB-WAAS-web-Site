"""Validate CV card HTML structure (embedded or client-render mode)."""
from __future__ import annotations

import re

try:
    from _paths import AZ_SCIENTISTS_PROFILES, ROOT
    from scientists_profiles_core import load_profiles, render_card
except ImportError:
    from helpers._paths import AZ_SCIENTISTS_PROFILES, ROOT  # type: ignore
    from helpers.scientists_profiles_core import load_profiles, render_card  # type: ignore

text = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")

if 'data-daab-profiles-client="1"' in text:
    profiles = load_profiles()
    issues: list[tuple[int, str]] = []
    for i, profile in enumerate(profiles, start=1):
        for lang in ("az", "en"):
            chunk = render_card(profile, lang, asset_prefix="../../")
            if chunk.count('class="card-meta"') != 1:
                issues.append((i, f"{lang}-meta"))
            email_row = chunk.count("card-meta-row")
            if email_row not in (1, 2):
                issues.append((i, f"{lang}-meta-rows"))
            if 'class="card-body"' not in chunk:
                issues.append((i, f"{lang}-body"))
    print("mode: client-render")
    print("profiles", len(profiles))
    print("issues", len(issues), issues[:15])
    raise SystemExit(1 if issues else 0)

starts = [m.start() for m in re.finditer(r'<div class="card" data-country-name', text)]
issues = []
for i, pos in enumerate(starts):
    end = starts[i + 1] if i + 1 < len(starts) else text.find('<div class="no-results"')
    chunk = text[pos:end]
    if chunk.count('class="card-meta"') != 1:
        issues.append((i + 1, "meta"))
    email_row = chunk.count("card-meta-row")
    if email_row not in (1, 2):
        issues.append((i + 1, "meta-rows"))
    if "</span>\n      <p class=\"card-country\">" not in chunk and "</span>\r\n      <p class=\"card-country\">" not in chunk:
        if "<p class=\"card-country\">" in chunk and "</span>" not in chunk.split("card-country")[0][-30:]:
            issues.append((i + 1, "header-span"))
    tail = chunk.strip()[-400:]
    if 'class="card-body"' not in chunk or tail.count("</div>") < 2:
        issues.append((i + 1, "closing"))

print("mode: embedded")
print("cards", len(starts))
print("issues", len(issues), issues[:15])
raise SystemExit(1 if issues else 0)
