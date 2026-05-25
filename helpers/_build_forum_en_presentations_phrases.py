#!/usr/bin/env python3
"""Generate helpers/forum_en_presentations_phrases.py from AZ strings + EN map."""
from __future__ import annotations

import json
from pathlib import Path

from _paths import ROOT

AZ_PATH = ROOT / "helpers" / "_presentations_az_strings.json"
MAP_PATH = ROOT / "helpers" / "_presentations_en_map.json"
OUT_PATH = ROOT / "helpers" / "forum_en_presentations_phrases.py"

# Standalone country name must not be mapped (corrupts «Azərbaycanlı» in longer phrases).
SKIP_AZ: frozenset[str] = frozenset({"Azərbaycan"})

PRESENTATIONS_UI: dict[str, str] = {
    "Foruma təqdim olunmuş <span>məruzələr</span>": "Presentations at the <span>forum</span>",
    "Məruzələr — DAAB": "Presentations — WAAS",
    "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumuna təqdim olunmuş elmi və akademik məruzələr.": (
        "Scientific and academic presentations delivered at the First Forum of Azerbaijani Scientists Living Abroad."
    ),
    'aria-label="Elm, strategiya və gələcək baxışı"': 'aria-label="Science, strategy and future outlook"',
    "Elm, strategiya və gələcək baxışı": "Science, strategy and future outlook",
    "Bu səhifədə forum iştirakçılarının bioinformatika, süni intellekt, təhsil, ekologiya, mədəniyyət, beynəlxalq əməkdaşlıq və digər sahələr üzrə məruzələri vahid strukturda təqdim olunur.": (
        "This page presents forum participants' presentations on bioinformatics, artificial intelligence, education, ecology, culture, international cooperation and other fields in a unified structure."
    ),
    "📊 Məruzələr": "📊 Presentations",
    'aria-label="Məruzələr menyusunu aç"': 'aria-label="Open presentations menu"',
    '<span class="forum-breadcrumbs-current" aria-current="page">Məruzələr</span>': (
        '<span class="forum-breadcrumbs-current" aria-current="page">Presentations</span>'
    ),
}


def py_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def emit_dict(name: str, d: dict[str, str]) -> str:
    lines = [f"{name}: dict[str, str] = {{"]
    for k in sorted(d, key=lambda x: (-len(x), x)):
        v = d[k]
        if "\n" in v or len(v) > 72:
            lines.append(f"    {py_str(k)}: (")
            lines.append(f"        {py_str(v)}")
            lines.append("    ),")
        else:
            lines.append(f"    {py_str(k)}: {py_str(v)},")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    az_list: list[str] = json.loads(AZ_PATH.read_text(encoding="utf-8"))
    en_map: dict[str, str] = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    required = [s for s in az_list if s not in SKIP_AZ]
    missing = [s for s in required if s not in en_map]
    if missing:
        raise SystemExit(f"Missing {len(missing)} translations; first: {missing[0][:80]!r}")

    phrases = {k: en_map[k] for k in required}
    body = f'''"""Azerbaijani → English phrase map for Forum 2024 presentations page body."""

from __future__ import annotations

# Presentation cards, table cells, TOC speaker links, subtitles.
# Shell/nav/footer strings: PRESENTATIONS_UI (applied before or with apply_shell).
{emit_dict("PRESENTATIONS_UI", PRESENTATIONS_UI)}

{emit_dict("PRESENTATIONS_PHRASES", phrases)}


def apply_presentations_phrases(html: str) -> str:
    """Replace Azerbaijani fragments with English; longest keys first."""
    for az, en in sorted(PRESENTATIONS_PHRASES.items(), key=lambda kv: -len(kv[0])):
        html = html.replace(az, en)
    return html
'''
    OUT_PATH.write_text(body, encoding="utf-8", newline="\n")
    print(f"wrote {OUT_PATH.relative_to(ROOT)} ({len(phrases)} phrases, {len(PRESENTATIONS_UI)} UI)")


if __name__ == "__main__":
    main()
