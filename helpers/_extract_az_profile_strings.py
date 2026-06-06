#!/usr/bin/env python3
"""Extract unique Azerbaijani strings from AZ profile pages for translation inventory."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from _paths import ROOT

AZ = ROOT / "az" / "prominent_figures"
AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")
TAG = re.compile(r"<[^>]+>")


def strip(s: str) -> str:
    return " ".join(TAG.sub(" ", s).split())


def main() -> None:
    sentences: Counter[str] = Counter()
    for p in sorted(AZ.rglob("*.html")):
        if p.parent.name.endswith("_") or p.name == "hazirlanir.html":
            continue
        t = p.read_text(encoding="utf-8")
        for block in re.findall(
            r'class="(?:prose pf-profile-article|work-desc|event-text|contribution-item)">(.*?)</(?:div|li)>',
            t,
            re.DOTALL,
        ):
            raw = strip(block)
            for sent in re.split(r"(?<=[.!?])\s+", raw):
                sent = sent.strip()
                if len(sent) > 20 and AZ_CHAR.search(sent):
                    sentences[sent] += 1
    print(f"Unique AZ sentences: {len(sentences)}")
    for s, n in sentences.most_common(120):
        print(f"{n:4d}|{s[:220]}")


if __name__ == "__main__":
    main()
