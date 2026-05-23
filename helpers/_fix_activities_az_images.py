#!/usr/bin/env python3
"""Ensure activities image src paths work from az/ and en/ pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

AZ = ROOT / "az" / "activities.html"
LEGACY = ROOT / "activities_az.html"

ABS_ACTIVITIES = re.compile(r'src="/images/activities/')
REL_ACTIVITIES = '../images/activities/'
ROOT_ACTIVITIES = 'images/activities/'


def fix_az_page() -> bool:
    text = AZ.read_text(encoding="utf-8")
    updated = text.replace('src="/images/activities/', f'src="{REL_ACTIVITIES}')
    if updated != text:
        AZ.write_text(updated, encoding="utf-8")
        return True
    return False


def fix_legacy_page() -> bool:
    if not LEGACY.exists():
        return False
    text = LEGACY.read_text(encoding="utf-8")
    updated = ABS_ACTIVITIES.sub(f'src="{ROOT_ACTIVITIES}', text)
    if updated != text:
        LEGACY.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    az_changed = fix_az_page()
    legacy_changed = fix_legacy_page()
    print(f"az/activities.html: {'updated' if az_changed else 'ok'}")
    print(f"activities_az.html: {'updated' if legacy_changed else 'ok'}")


if __name__ == "__main__":
    main()
