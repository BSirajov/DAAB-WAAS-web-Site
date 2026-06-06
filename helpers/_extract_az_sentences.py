#!/usr/bin/env python3
"""Inventory all unique Azerbaijani sentences across az/prominent_figures profiles."""
import re
from collections import Counter
from pathlib import Path
from _paths import ROOT

AZ = ROOT / "az" / "prominent_figures"
PROSE_RE = re.compile(r'class="prose pf-profile-article">(.*?)</div>', re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
sentences: Counter = Counter()
for p in sorted(AZ.rglob("*.html")):
    if p.stem.endswith("_EN") or p.name == "hazirlanir.html":
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    m = PROSE_RE.search(text)
    if not m:
        continue
    raw = TAG_RE.sub(" ", m.group(1)).replace("\n", " ")
    for sent in re.split(r"(?<=[.!?])\s+", raw):
        sent = " ".join(sent.split())
        if sent and re.search(r"[əğıöüşçƏĞİÖÜŞÇ]", sent):
            sentences[sent] += 1

for s, n in sorted(sentences.items(), key=lambda x: -x[1])[:100]:
    print(f"{n:4d}  {s}")
if __name__ == "__main__":
    pass
