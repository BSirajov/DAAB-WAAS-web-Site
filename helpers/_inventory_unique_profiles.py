#!/usr/bin/env python3
"""Print AZ profiles whose article content is not pure template."""
import re
from pathlib import Path
from _paths import ROOT

AZ = ROOT / "az" / "prominent_figures"
PROSE_RE = re.compile(r'class="prose pf-profile-article">(.*?)</div>', re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
TEMPLATE_MARKERS = ("irsinə mənsub", "elmi və intellektual ənənəsini dünya miqyasında")

for p in sorted(AZ.rglob("*.html")):
    if p.stem.endswith("_EN") or p.name == "hazirlanir.html":
        continue
    txt = p.read_text(encoding="utf-8", errors="replace")
    m = PROSE_RE.search(txt)
    if not m:
        continue
    raw = " ".join(TAG_RE.sub(" ", m.group(1)).split())
    if not re.search(r"[əğıöüşçƏĞİÖÜŞÇ]", raw):
        continue
    # skip pure template profiles
    if any(x in raw for x in TEMPLATE_MARKERS):
        continue
    print(f"=== {p.name}")
    print(raw[:1200])
    print()
