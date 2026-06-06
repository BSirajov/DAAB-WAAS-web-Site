#!/usr/bin/env python3
"""Find EN profile fragments with untranslated Azerbaijani prose (not proper names)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")
# Common AZ function words — presence suggests untranslated prose
AZ_WORD = re.compile(
    r"\b(?:və|ilə|üçün|haqqında|mənsub|olmuşdur|etmişdir|"
    r"sahəsində|irsine|tərəfindən|kimi|olan|edirdi|"
    r"doğulmuş|müəllif|əsərlər|türk|azərbaycan)\b",
    re.I,
)
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
        for cls in ("work-desc", "event-text", "contribution-item", "quote-text"):
            for block in re.findall(rf'class="{cls}">([^<]+)</', text):
                frag = strip(block)
                if AZ_WORD.search(frag):
                    issues.append((str(path.relative_to(ROOT)), frag[:180]))
        pm = re.search(r'class="prose pf-profile-article">(.*?)</div>', text, re.DOTALL)
        if pm:
            for sent in re.split(r"(?<=[.!?])\s+", strip(pm.group(1))):
                if AZ_WORD.search(sent):
                    issues.append((str(path.relative_to(ROOT)), sent[:220]))
    print(f"Prose issues (AZ word heuristic): {len(issues)}")
    for rel, frag in issues[:50]:
        print(f"{rel}: {frag}")


if __name__ == "__main__":
    main()
