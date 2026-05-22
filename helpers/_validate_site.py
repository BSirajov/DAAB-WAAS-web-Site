#!/usr/bin/env python3
"""Validate DAAB static site links, assets, and common breakage patterns.

Run from repository root:
    python helpers/_validate_site.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

# Pages that must include shared assets (site root HTML only)
MAIN_PAGES = [
    "index.html",
    "activities_az.html",
    "charter_az.html",
    "executive_board_az.html",
    "foundation_az.html",
    "membership_terms_az.html",
    "mission_vision_values_az.html",
    "scientists_list_view_az.html",
    "scientists_card_view_az.html",
]

REQUIRED_SNIPPETS = {
    "daab-common.css": "css/daab-common.css",
    "daab-mobile.css": "css/daab-mobile.css",
    "daab-nav.js": "js/daab-nav.js",
    "daab-mobile.js": "js/daab-mobile.js",
}

# Obsolete targets that often survive refactors
OBSOLETE_TARGETS = {
    "Scientists_AZ.html",
    "Scientists_CV_AZ.html",
    "scientists_az.html",
    "scientists_cv_az.html",
    "Foundation_AZ.html",
    "Activities_AZ.html",
    "Charter_AZ.html",
    "Executive_Board_AZ.html",
    "Membership_Terms_AZ.html",
    "Mission_Vision_Values_AZ.html",
    "daab-common.css",  # root duplicate
    "daab-nav.js",
    "css/daab-common.css",  # if only at root — warn if href without css/
}

# Case-sensitive: only flag uppercase JS/ or CV/ (Linux hosting breaks)
RISKY_PATH_SEGMENTS = re.compile(r"(^|/)(JS|CV)(/|$)|Scientists_Photos")

HREF_SRC_RE = re.compile(
    r"""(?:href|src)=["']([^"']+)["']""",
    re.I,
)

SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "data:", "#", "javascript:")


def site_html_files() -> list[Path]:
    return sorted(ROOT.glob("*.html"))


def resolve_ref(page: Path, ref: str) -> Path | None:
    ref = ref.split("#")[0].split("?")[0].strip()
    if not ref or ref.startswith(SKIP_PREFIXES):
        return None
    if ref.startswith("/"):
        return ROOT / ref.lstrip("/")
    return (page.parent / ref).resolve()


def check_case_collision(path: Path) -> list[str]:
    """On case-sensitive hosts, only one casing can exist; flag ambiguous dirs."""
    issues = []
    parts = path.relative_to(ROOT).parts if path.is_relative_to(ROOT) else path.parts
    cur = ROOT
    for part in parts:
        if not cur.is_dir():
            break
        entries = {p.name.lower(): p.name for p in cur.iterdir()}
        key = part.lower()
        if key in entries and entries[key] != part:
            issues.append(f"case mismatch: {cur / part} vs {cur / entries[key]}")
        cur = cur / part
    return issues


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # Duplicate risky top-level folders (Windows may hide JS==js)
    for name in ("JS", "CV"):
        p = ROOT / name
        lower = ROOT / name.lower()
        if p.exists() and lower.exists() and p.resolve() != lower.resolve():
            errors.append(f"Duplicate folders {name}/ and {name.lower()}/ — Linux deploy will break")

    pages = site_html_files()
    if not pages:
        errors.append("No *.html files at repository root")

    all_refs: list[tuple[Path, str]] = []

    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")

        if page.name in MAIN_PAGES:
            for label, snippet in REQUIRED_SNIPPETS.items():
                if snippet not in text:
                    warnings.append(f"{page.name}: missing {label} ({snippet})")

        for m in HREF_SRC_RE.finditer(text):
            ref = m.group(1)
            if any(x in ref for x in ("${", "%", "{{", "esc(", "`")):
                continue
            all_refs.append((page, ref))

            if ref in OBSOLETE_TARGETS or ref.split("/")[-1] in OBSOLETE_TARGETS:
                warnings.append(f"{page.name}: obsolete reference → {ref}")

            if RISKY_PATH_SEGMENTS.search(ref):
                warnings.append(f"{page.name}: risky path casing → {ref}")

            target = resolve_ref(page, ref)
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{page.name}: missing → {ref} ({target.relative_to(ROOT)})")
            else:
                for issue in check_case_collision(target):
                    warnings.append(f"{page.name}: {issue}")

    # Nav targets: every *.html at root should be reachable naming
    html_names = {p.name for p in pages}
    for page, ref in all_refs:
        if ref.endswith(".html") and "/" not in ref and ref not in html_names:
            if not ref.startswith(SKIP_PREFIXES):
                errors.append(f"{page.name}: links to missing page {ref}")

    # Root stray assets
    for stray in ("daab-common.css", "daab-nav.js"):
        if (ROOT / stray).exists():
            warnings.append(f"stray file at repo root: {stray} (should be under css/ or js/)")

    print("DAAB site validation")
    print(f"  Root HTML pages: {len(pages)}")
    print(f"  References checked: {len(all_refs)}")
    print()

    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings[:40]:
            print(f"  ⚠ {w}")
        if len(warnings) > 40:
            print(f"  … and {len(warnings) - 40} more")
        print()

    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nFix errors before deploy. See documents/DAAB-Site-Stability-and-Deployment-Guide.md")
        return 1

    print("OK — no broken local paths detected.")
    if warnings:
        print("Review warnings above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
