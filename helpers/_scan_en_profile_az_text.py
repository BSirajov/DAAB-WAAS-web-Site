#!/usr/bin/env python3
"""Scan EN prominent-figure profiles for remaining Azerbaijani text."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from _paths import ROOT

AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")
EN_ROOT = ROOT / "en" / "prominent_figures"
PROSE_RE = re.compile(r'class="prose pf-profile-article">(.*?)</div>', re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")

# Skip proper names / accepted Latin forms in tags, URLs, etc.
SKIP_IN = ("data-daab", "mailto:", "http", "google.com", "worldcat", "britannica")


def strip_html(s: str) -> str:
    return " ".join(TAG_RE.sub(" ", s).split())


def main() -> None:
    sentences: Counter[str] = Counter()
    labels: Counter[str] = Counter()
    files_with_az: list[str] = []
    n_files = 0

    for path in sorted(EN_ROOT.rglob("*.html")):
        if path.name == "hazirlanir.html" or path.stem.endswith("_EN"):
            continue
        if "_/" in str(path) or path.parent.name.endswith("_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        n_files += 1
        if not AZ_CHAR.search(text):
            continue
        files_with_az.append(str(path.relative_to(ROOT)))

        for m in re.finditer(r'info-label">([^<]+)</span>', text):
            lab = m.group(1).strip()
            if AZ_CHAR.search(lab):
                labels[lab] += 1

        for m in re.finditer(r'class="(?:work-name|work-desc|event-text|event-title|quote-text|quote-source|contribution-item|info-val|hero-tag gold|section-title)[^"]*">([^<]{3,200})', text):
            frag = strip_html(m.group(1))
            if AZ_CHAR.search(frag) and not any(x in frag.lower() for x in SKIP_IN):
                sentences[frag[:180]] += 1

        pm = PROSE_RE.search(text)
        if pm:
            raw = strip_html(pm.group(1))
            for sent in re.split(r"(?<=[.!?])\s+", raw):
                sent = sent.strip()
                if sent and AZ_CHAR.search(sent) and len(sent) > 15:
                    sentences[sent[:200]] += 1

    print(f"EN profile files scanned: {n_files}")
    print(f"Files with AZ chars: {len(files_with_az)}")
    print("\n--- Top labels ---")
    for s, c in labels.most_common(30):
        print(f"{c:4d}  {s}")
    print("\n--- Top fragments/sentences (by count) ---")
    for s, c in sentences.most_common(80):
        print(f"{c:4d}  {s}")

if __name__ == "__main__":
    main()
