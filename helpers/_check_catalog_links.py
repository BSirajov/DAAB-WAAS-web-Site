#!/usr/bin/env python3
"""Check encyclopedia catalog hrefs against profile files."""
import re
from pathlib import Path

from _paths import ROOT

text = (ROOT / "js" / "prominent-figures-catalog-data.js").read_text(encoding="utf-8")
hrefs = re.findall(r'"href": "([^"]+)"', text)
missing_az: list[str] = []
missing_en: list[str] = []
for h in hrefs:
    if not (ROOT / "az" / h).exists():
        missing_az.append(h)
    if not (ROOT / "en" / h).exists():
        missing_en.append(h)
print(f"Total hrefs: {len(hrefs)}")
print(f"Missing AZ: {len(missing_az)}")
for x in missing_az[:15]:
    print(f"  AZ missing: {x}")
print(f"Missing EN: {len(missing_en)}")
for x in missing_en[:15]:
    print(f"  EN missing: {x}")
