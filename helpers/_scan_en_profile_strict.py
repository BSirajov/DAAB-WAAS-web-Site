#!/usr/bin/env python3
"""Strict scan: AZ text in EN profiles excluding proper names in titles."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Distinctive Azerbaijani letters (excludes ü/ö/ş/ç/ğ shared with Turkish prose).
AZ_CHAR = re.compile(r"[əı]")
EN_ROOT = ROOT / "en" / "prominent_figures"
TAG = re.compile(r"<[^>]+>")


def strip(s: str) -> str:
    return " ".join(TAG.sub(" ", s).split())


def main() -> None:
    issues: list[tuple[str, str]] = []
    for path in sorted(EN_ROOT.rglob("*.html")):
        if path.name == "hazirlanir.html" or path.parent.name.endswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        name = ""
        m = re.search(r'data-daab-profile-name="([^"]*)"', text)
        if m:
            name = m.group(1)

        for cls in ("work-desc", "event-text", "contribution-item", "quote-text", "info-val", "hero-tag gold"):
            for block in re.findall(rf'class="{cls}">([^<]+)</', text):
                frag = strip(block)
                if not frag or not AZ_CHAR.search(frag):
                    continue
                if name and frag == name:
                    continue
                issues.append((str(path.relative_to(ROOT)), frag[:160]))

        pm = re.search(r'class="prose pf-profile-article">(.*?)</div>', text, re.DOTALL)
        if pm:
            raw = pm.group(1)
            for sent in re.split(r"(?<=[.!?])\s+", strip(raw)):
                if not sent or not AZ_CHAR.search(sent):
                    continue
                # skip if sentence is only the person's name
                if name and sent.strip() == name:
                    continue
                issues.append((str(path.relative_to(ROOT)), sent[:200]))

    print(f"Issues found: {len(issues)}")
    for rel, frag in issues[:60]:
        print(f"{rel}: {frag}")


if __name__ == "__main__":
    main()
