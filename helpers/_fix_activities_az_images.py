#!/usr/bin/env python3
"""Ensure activities image src paths work from az/ and en/ pages."""
from __future__ import annotations

from _paths import ROOT

AZ = ROOT / "az" / "activities.html"


def fix_az_page() -> bool:
    text = AZ.read_text(encoding="utf-8")
    updated = text.replace('src="/images/activities/', 'src="../images/activities/')
    if updated != text:
        AZ.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    az_changed = fix_az_page()
    print(f"az/activities.html: {'updated' if az_changed else 'ok'}")


if __name__ == "__main__":
    main()
