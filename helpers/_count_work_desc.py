#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import re
from _paths import ROOT

AZ = ROOT / "az" / "prominent_figures"
c = Counter()
for p in AZ.rglob("*.html"):
    if p.parent.name.endswith("_") or p.name == "hazirlanir.html":
        continue
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r'class="work-desc">([^<]+)</div>', t):
        c[m.group(1).strip()] += 1
print("unique work-desc", len(c))
for s, n in c.most_common(20):
    print(n, s[:140])
