#!/usr/bin/env python3
"""Rebuild prev/next sidebar links on prominent figure profiles (slug-based, per group)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _build_prominent_figures_catalog import parse_profile
from _paths import ROOT
from _prominent_figure_names_en import english_name

SKIP = {"hazirlanir.html"}

RELATED_RE_AZ = re.compile(
    r'<div class="info-card"><div class="info-title">Həmçinin Baxın</div>.*?</div>(?=</aside>)',
    re.DOTALL,
)
RELATED_RE_EN = re.compile(
    r'<div class="info-card"><div class="info-title">See also</div>.*?</div>(?=</aside>)',
    re.DOTALL,
)


def load_group(group: str, figures_root: Path) -> list[dict]:
    folder = figures_root / group
    rows: list[dict] = []
    for path in sorted(folder.glob("*.html")):
        if path.name in SKIP:
            continue
        row = parse_profile(path, group)
        if not row:
            print(f"skip (no metadata): {path.relative_to(ROOT)}", file=sys.stderr)
            continue
        row["file"] = path.name
        rows.append(row)
    rows.sort(key=lambda r: r["name"].casefold())
    return rows


def person_link(person: dict, lang: str = "az") -> str:
    display = (
        english_name(person["id"], person["name"])
        if lang == "en"
        else person["name"]
    )
    return (
        f'<a href="{person["file"]}" class="nav-person-link">'
        f'<div class="avatar">{person["emoji"]}</div><div>'
        f'<div class="nav-person-name">{display}</div>'
        f'<div class="nav-person-dates">{person["dates"]}</div></div></a>'
    )


def related_html(prev: dict, nxt: dict, *, lang: str) -> str:
    if lang == "en":
        return (
            '<div class="info-card"><div class="info-title">See also</div>'
            '<div class="nav-dir">Previous profile</div>'
            + person_link(prev, lang)
            + '<div class="nav-dir">Next profile</div>'
            + person_link(nxt, lang)
            + "</div>"
        )
    return (
        '<div class="info-card"><div class="info-title">Həmçinin Baxın</div>'
        '<div class="nav-dir">Əvvəlki profil</div>'
        + person_link(prev, lang)
        + '<div class="nav-dir">Növbəti profil</div>'
        + person_link(nxt, lang)
        + "</div>"
    )


def patch_group(group: str, figures_root: Path, related_re: re.Pattern[str], lang: str) -> int:
    rows = load_group(group, figures_root)
    if len(rows) < 2:
        return 0
    by_file = {r["file"]: r for r in rows}
    n = 0
    for i, row in enumerate(rows):
        prev = rows[(i - 1) % len(rows)]
        nxt = rows[(i + 1) % len(rows)]
        path = figures_root / group / row["file"]
        text = path.read_text(encoding="utf-8")
        marker = "See also" if lang == "en" else "Həmçinin Baxın"
        if marker not in text:
            continue
        new_section = related_html(prev, nxt, lang=lang)
        new_text, count = related_re.subn(new_section, text, count=1)
        if count != 1:
            print(f"warn: could not patch related nav in {path.relative_to(ROOT)}", file=sys.stderr)
            continue
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            n += 1
    return n


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=("az", "en", "both"), default="both")
    args = parser.parse_args()
    langs = ("az", "en") if args.lang == "both" else (args.lang,)
    total = 0
    for lang in langs:
        root = ROOT / lang / "prominent_figures"
        rel_re = RELATED_RE_EN if lang == "en" else RELATED_RE_AZ
        az = patch_group("azturk", root, rel_re, lang)
        world = patch_group("world", root, rel_re, lang)
        total += az + world
        print(f"[{lang}] Updated {az} azturk + {world} world (circular A→Z per group)")
    print(f"Total: {total} profile pages")


if __name__ == "__main__":
    main()
