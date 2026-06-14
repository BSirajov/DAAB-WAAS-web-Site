"""DEPRECATED: superseded by _harmonize_governance_terminology.py (Executive Board)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# User requested "Board of director"; standard EN governing-body term:
BOARD_EN = "Board of Directors"  # legacy; do not run — use _harmonize_governance_terminology.py

EN_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "Chair of the Executive Board of the World Association of Azerbaijani Scientists",
        f"Chair of the {BOARD_EN} of the World Association of Azerbaijani Scientists",
    ),
    (
        "member of the Executive Board of the World Association of Azerbaijani Scientists",
        f"member of the {BOARD_EN} of the World Association of Azerbaijani Scientists",
    ),
    (f"Co-Chair of the WAAS Executive Board", f"Co-Chair of the WAAS {BOARD_EN}"),
    ("Chair of the WAAS Executive Board", f"Chair of the WAAS {BOARD_EN}"),
    ("Chair of the Executive Board", "Chair"),
    ("Executive Board Members", "Board Members"),
    ("Executive Board Member", "Board Member"),
    (f"WAAS Executive Board Co-Chair", f"WAAS {BOARD_EN} Co-Chair"),
    (f"WAAS Executive Board Chair", f"WAAS {BOARD_EN} Chair"),
    (f"WAAS Executive Board member", f"WAAS {BOARD_EN} member"),
    (f"WAAS Executive Board sends", f"WAAS {BOARD_EN} sends"),
    ("members of the WAAS Executive Board", f"members of the WAAS {BOARD_EN}"),
    ("Executive Board and leadership", f"{BOARD_EN} and leadership"),
    ('aria-label="Executive Board summary"', f'aria-label="{BOARD_EN} summary"'),
    ('aria-label="Executive Board members"', f'aria-label="{BOARD_EN} members"'),
    ("Executive Board Co-Chair", f"{BOARD_EN} Co-Chair"),
    ("Executive Board Chair", f"{BOARD_EN} Chair"),
    ("Executive Board member", f"{BOARD_EN} member"),
    ("Scientists Executive Board", f"Scientists {BOARD_EN}"),
    ("Executive Board leadership", f"{BOARD_EN} leadership"),
    ("executive board members", f"{BOARD_EN} members"),
    ("executive board,", f"{BOARD_EN.lower()},"),
    ("executive board ", f"{BOARD_EN.lower()} "),
    ("The executive board ", f"The {BOARD_EN.lower()} "),
    ("Initial WAAS executive board", f"Initial WAAS {BOARD_EN.lower()}"),
    ("Executive Board", BOARD_EN),
    ("Executive Board", BOARD_EN),
]

EN_HELPER_FILES_EXTRA = (
    "helpers/forum_en_common.py",
    "helpers/forum_en_cooperation.py",
    "helpers/forum_en_official.py",
    "helpers/forum_en_program_map.py",
    "helpers/forum_en_presentations_phrases.py",
    "helpers/forum_en_impressions_phrases.py",
    "helpers/_presentations_en_map.json",
    "helpers/_waas_en_brand.py",
)

EN_HELPER_FILES = (
    "helpers/i18n_executive_board_en.py",
    "helpers/i18n_home_en.py",
    "helpers/i18n_membership_en.py",
    "helpers/i18n_activities_en.py",
    "helpers/i18n_foundation_en.py",
    "helpers/i18n_charter_en.py",
    "helpers/i18n_scientists_en.py",
    "helpers/_complete_activities_en_translations.py",
    "helpers/_build_bilingual_tree.py",
    "helpers/_publish_en_pages.py",
)

AZ_EXECUTIVE_BOARD_REPLACEMENTS: list[tuple[str, str]] = [
    ("İdarə Heyətinin Sədri", "Sədr"),
    ("İdarə Heyəti Üzvləri", "Üzvlər"),
    ("İdarə Heyəti Üzvü", "Üzv"),
    ("DAAB İdarə Heyətinin Sədri", "DAAB Sədri"),
]

def apply_replacements(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


def update_en_files() -> int:
    count = 0
    for path in sorted(ROOT.glob("en/**/*.html")):
        original = path.read_text(encoding="utf-8")
        updated = apply_replacements(original, EN_REPLACEMENTS)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            count += 1
            print(f"  {path.relative_to(ROOT)}")
    return count


def update_en_helpers_and_i18n() -> None:
    helper_files = EN_HELPER_FILES + EN_HELPER_FILES_EXTRA
    for rel in helper_files:
        path = ROOT / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        updated = apply_replacements(text, EN_REPLACEMENTS)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"  {path.relative_to(ROOT)}")

    ui = ROOT / "i18n" / "ui.json"
    ui.write_text(apply_replacements(ui.read_text(encoding="utf-8"), EN_REPLACEMENTS), encoding="utf-8", newline="\n")
    print("  i18n/ui.json")

    search = ROOT / "i18n" / "search-index.json"
    if search.is_file():
        search.write_text(
            apply_replacements(search.read_text(encoding="utf-8"), EN_REPLACEMENTS),
            encoding="utf-8",
            newline="\n",
        )
        print("  i18n/search-index.json")


def update_az_executive_board() -> None:
    path = ROOT / "az" / "executive-board.html"
    text = path.read_text(encoding="utf-8")
    path.write_text(apply_replacements(text, AZ_EXECUTIVE_BOARD_REPLACEMENTS), encoding="utf-8", newline="\n")
    print(f"  {path.relative_to(ROOT)}")


def main() -> None:
    print("EN HTML:")
    n = update_en_files()
    print(f"  ({n} files)\nEN helpers / i18n:")
    update_en_helpers_and_i18n()
    print("\nAZ executive-board.html:")
    update_az_executive_board()


if __name__ == "__main__":
    main()
