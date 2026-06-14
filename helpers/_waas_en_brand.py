#!/usr/bin/env python3
"""Replace DAAB with WAAS in English UI strings (not AZ keys or asset paths)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

ORDER = [
    ("DAAB / WAAS", "WAAS"),
    ("DAAB's", "WAAS's"),
    ("DAAB —", "WAAS —"),
    ("DAAB (", "WAAS ("),
    ("DAAB-", "WAAS-"),
    ("Join DAAB", "Join WAAS"),
    ("join DAAB", "join WAAS"),
    ("DAAB ", "WAAS "),
    ("DAAB.", "WAAS."),
    ("DAAB,", "WAAS,"),
    ("DAAB<", "WAAS<"),
    ("DAAB\n", "WAAS\n"),
    ('DAAB"', 'WAAS"'),
    ("DAAB'", "WAAS'"),
    ("DAAB", "WAAS"),
]


def apply_waas(text: str) -> str:
    for old, new in ORDER:
        text = text.replace(old, new)
    return text


def patch_en_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = apply_waas(text)
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


TUPLE_RE = re.compile(
    r'\(\s*("(?:\\.|[^"\\])*"|"""(?:\\.|[^\\])*""")\s*,\s*("(?:\\.|[^"\\])*"|"""(?:\\.|[^\\])*""")\s*\)',
    re.DOTALL,
)


def patch_i18n_tuple_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    def sub_tuple(m: re.Match[str]) -> str:
        az = m.group(1)
        en = m.group(2)
        return f"({az}, {apply_waas(en)})"

    updated = TUPLE_RE.sub(sub_tuple, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def patch_publish_py(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_mission = False
    changed = False
    for line in lines:
        if line.startswith("MISSION_REPLACEMENTS"):
            in_mission = True
        if in_mission and line.startswith("]") and "MISSION" not in line:
            in_mission = False
        if in_mission and '", "' in line and line.strip().startswith("("):
            idx = line.find('", "')
            if idx != -1:
                new_line = line[: idx + 4] + apply_waas(line[idx + 4 :])
                if new_line != line:
                    changed = True
                    line = new_line
        elif "en_nav_html" in "".join(out[-5:]) or "en_footer_html" in line:
            pass
        if "DAAB home" in line or "DAAB Logo" in line or "DAAB Board of Directors" in line or "DAAB / WAAS" in line:
            new_line = apply_waas(line)
            if new_line != line:
                changed = True
                line = new_line
        out.append(line)
    updated = "".join(out)
    # nav/footer template strings
    updated2 = updated
    for block in ('aria-label="DAAB home"', "alt=\"DAAB Logo\"", "Chair of the DAAB", "© 2026 DAAB / WAAS"):
        if block in updated2:
            updated2 = apply_waas(updated2)
    if updated2 != text:
        path.write_text(updated2, encoding="utf-8", newline="\n")
        return True
    return changed


def patch_ui_json(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    # Only patch en gateway title and nav/footer en keys
    updated = text.replace('"title": "DAAB — Choose language"', '"title": "WAAS — Choose language"')
    updated = updated.replace('"ariaHome": "DAAB home"', '"ariaHome": "WAAS home"')
    updated = updated.replace('"chairRole": "Chair of the DAAB Board of Directors"', '"chairRole": "Chair of the WAAS Executive Board"')
    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        return True
    return False


def patch_search_js(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = 'if (ctx === "en" || ctx === "en-scientists")'
    start = text.find(marker)
    if start == -1:
        return False
    end = text.find("\n    return [", start)
    block = text[start:end]
    new_block = apply_waas(block)
    if new_block == block:
        return False
    updated = text[:start] + new_block + text[end:]
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    changed: list[str] = []
    en_dir = ROOT / "en"
    for html in sorted(en_dir.rglob("*.html")):
        if patch_en_html(html):
            changed.append(str(html.relative_to(ROOT)))

    for name in (
        "i18n_home_en.py",
        "i18n_foundation_en.py",
        "i18n_membership_en.py",
        "i18n_executive_board_en.py",
        "i18n_activities_en.py",
        "i18n_charter_en.py",
        "i18n_scientists_en.py",
    ):
        p = ROOT / "helpers" / name
        if p.is_file() and patch_i18n_tuple_file(p):
            changed.append(str(p.relative_to(ROOT)))

    pub = ROOT / "helpers" / "_publish_en_pages.py"
    text = pub.read_text(encoding="utf-8")
    new_text = apply_waas(text)
    # Restore AZ-side mission keys that must stay DAAB for matching
    az_restores = [
        ('("WAAS-ın məqsədi', '("DAAB-ın məqsədi'),
        ('("WAAS-ın institusional', '("DAAB-ın institusional'),
        ("Dəyərlər WAAS-ın akademik", "Dəyərlər DAAB-ın akademik"),
        ('<title>\n      WAAS — Missiya', '<title>\n      DAAB — Missiya'),
        ('aria-label="WAAS missiya', 'aria-label="DAAB missiya'),
        ("WAAS İdarə Heyətinin Sədri", "DAAB İdarə Heyətinin Sədri"),
        ("World Association of Azerbaijani Scientists \\(WAAS\\)", "World Association of Azerbaijani Scientists \\(DAAB\\)"),
        ("<p><strong>WAAS</strong>", "<p><strong>DAAB</strong>"),
        ("<p>WAAS elm", "<p>DAAB elm"),
    ]
    for old, new in az_restores:
        new_text = new_text.replace(old, new)
    if new_text != text:
        pub.write_text(new_text, encoding="utf-8", newline="\n")
        changed.append(str(pub.relative_to(ROOT)))

    ui = ROOT / "i18n" / "ui.json"
    if ui.is_file() and patch_ui_json(ui):
        changed.append(str(ui.relative_to(ROOT)))

    js = ROOT / "js" / "daab-search.js"
    if js.is_file() and patch_search_js(js):
        changed.append(str(js.relative_to(ROOT)))

    for rel in changed:
        print(f"  updated {rel}")
    print(f"Done ({len(changed)} files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
