#!/usr/bin/env python3
"""Smoke-check bilingual site before deploy.

Usage:
    python helpers/_validate_bilingual.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _paths import ROOT

ROUTES_PATH = ROOT / "i18n" / "routes.json"
REQUIRED_SCRIPTS = ("daab-i18n.js", "daab-lang-position.js", "daab-shell.js")


def load_routes() -> dict:
    return json.loads(ROUTES_PATH.read_text(encoding="utf-8"))


def check_page(path: Path, lang: str) -> list[str]:
    issues: list[str] = []
    if not path.is_file():
        issues.append(f"missing file: {path.relative_to(ROOT)}")
        return issues
    html = path.read_text(encoding="utf-8")
    if f'data-daab-lang="{lang}"' not in html and f'lang="{lang}"' not in html:
        issues.append(f"{path.relative_to(ROOT)}: expected lang={lang}")
    for script in REQUIRED_SCRIPTS:
        if script not in html:
            issues.append(f"{path.relative_to(ROOT)}: missing {script}")
    if "routes.json" not in html and "daab-i18n" in html:
        pass
    return issues


def check_sitemap(routes: dict) -> list[str]:
    issues: list[str] = []
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        return ["missing sitemap.xml — run _build_bilingual_tree.py"]
    text = sitemap.read_text(encoding="utf-8")
    if "xmlns:xhtml" not in text:
        issues.append("sitemap.xml: missing xhtml namespace (hreflang alternates)")
    for page in routes["pages"]:
        for lang in ("az", "en"):
            rel = page[lang].replace("\\", "/")
            if rel not in text:
                issues.append(f"sitemap.xml: missing {rel}")
    return issues


def check_legacy_redirects(routes: dict) -> list[str]:
    issues: list[str] = []
    for legacy in routes.get("legacyRedirects", {}):
        if legacy == "index.html":
            continue
        path = ROOT / legacy
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        if "data-daab-legacy-redirect" not in html:
            issues.append(
                f"{legacy}: no redirect to /az/ — run _build_bilingual_tree.py (redirects on)"
            )
    return issues


def main() -> int:
    routes = load_routes()
    issues: list[str] = []

    for page in routes["pages"]:
        issues.extend(check_page(ROOT / page["az"], "az"))
        en_path = ROOT / page["en"]
        issues.extend(check_page(en_path, "en"))
        if en_path.is_file():
            en_html = en_path.read_text(encoding="utf-8")
            if "Translation in progress" in en_html and "daab-en-complete" not in en_html:
                issues.append(f"{en_path.relative_to(ROOT)}: still a stub (run _publish_en_pages.py)")

    issues.extend(check_sitemap(routes))
    issues.extend(check_legacy_redirects(routes))

    try:
        from _validate_section_anchors import collect_issues as anchor_issues

        issues.extend(anchor_issues())
    except Exception as exc:
        issues.append(f"section anchor check error: {exc}")

    if not (ROOT / "robots.txt").is_file():
        issues.append("missing robots.txt — run _build_bilingual_tree.py")

    gateway = ROOT / "index.html"
    if gateway.is_file():
        g = gateway.read_text(encoding="utf-8")
        if "location.replace" not in g and "daab-gateway" not in g:
            issues.append("index.html: expected language gateway redirect")

    if issues:
        print("Bilingual validation FAILED:\n")
        for item in issues:
            print(f"  - {item}")
        return 1

    print("Bilingual validation OK")
    print(f"  {len(routes['pages'])} page pairs (az + en)")
    print(f"  sitemap: {ROOT / 'sitemap.xml'}")
    print(f"  robots:  {ROOT / 'robots.txt'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
