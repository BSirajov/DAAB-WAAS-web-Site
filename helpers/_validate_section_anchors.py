"""Validate synchronized section anchors across AZ/EN page pairs."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

ROUTES_PATH = ROOT / "i18n" / "routes.json"

# Page-specific selectors for lang-switch anchors (must stay aligned AZ ↔ EN).
PAGE_ANCHOR_RULES: dict[str, list[str]] = {
    "activities": [
        r'<article[^>]*class="[^"]*news-card[^"]*"[^>]*id="([^"]+)"',
        r'href="#([^"]+)"',
    ],
    "charter": [r'<section[^>]*class="[^"]*charter-card[^"]*"[^>]*id="([^"]+)"'],
    "foundation": [r'<section[^>]*id="([^"]+)"'],
    "mission": [r'<section[^>]*id="([^"]+)"'],
}


def extract_ids(html: str, patterns: list[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for pat in patterns:
        out[pat] = re.findall(pat, html, flags=re.I)
    return out


def compare_pair(page_id: str, az_path: Path, en_path: Path) -> list[str]:
    issues: list[str] = []
    patterns = PAGE_ANCHOR_RULES.get(page_id)
    if not patterns:
        return issues
    az_html = az_path.read_text(encoding="utf-8")
    en_html = en_path.read_text(encoding="utf-8")
    az_ids = extract_ids(az_html, patterns)
    en_ids = extract_ids(en_html, patterns)
    for pat in patterns:
        a, e = az_ids[pat], en_ids[pat]
        if a != e:
            label = "articles" if "news-card" in pat else "anchors"
            issues.append(
                f"{page_id}: {label} mismatch between {az_path.name} and {en_path.name}"
            )
            az_set, en_set = set(a), set(e)
            only_az = sorted(az_set - en_set)
            only_en = sorted(en_set - az_set)
            if only_az:
                issues.append(f"  only AZ: {only_az[:8]}{'…' if len(only_az) > 8 else ''}")
            if only_en:
                issues.append(f"  only EN: {only_en[:8]}{'…' if len(only_en) > 8 else ''}")
            for i, (ai, ei) in enumerate(zip(a, e)):
                if ai != ei:
                    issues.append(f"  order[{i}]: az={ai!r} en={ei!r}")
                    if i >= 4:
                        issues.append("  …")
                        break
    return issues


def check_lang_position_script(az_path: Path, en_path: Path) -> list[str]:
    issues: list[str] = []
    for path in (az_path, en_path):
        if path.is_file():
            html = path.read_text(encoding="utf-8")
            if "daab-lang-position.js" not in html:
                issues.append(f"{path.relative_to(ROOT)}: missing daab-lang-position.js")
            if "daab-shell.js" not in html:
                issues.append(f"{path.relative_to(ROOT)}: missing daab-shell.js")
    return issues


def collect_issues() -> list[str]:
    routes = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    issues: list[str] = []
    for page in routes["pages"]:
        az_path = ROOT / page["az"]
        en_path = ROOT / page["en"]
        issues.extend(check_lang_position_script(az_path, en_path))
        issues.extend(compare_pair(page["id"], az_path, en_path))
    return issues


def main() -> int:
    issues = collect_issues()
    if issues:
        print("Section anchor validation FAILED:")
        for item in issues:
            print(f"  - {item}")
        return 1
    print("Section anchor validation OK")
    routes = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    print(f"  {len(routes['pages'])} page pairs checked")
    print(f"  anchor rules: {', '.join(PAGE_ANCHOR_RULES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
