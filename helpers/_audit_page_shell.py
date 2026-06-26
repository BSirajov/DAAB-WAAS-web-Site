#!/usr/bin/env python3
"""Audit (and optionally fix) standard head script bundles on nav-mounted pages."""
from __future__ import annotations

import argparse
import sys

from _page_shell_assets import audit_shell_scripts, fix_shell_scripts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Insert missing standard shell scripts into HTML pages",
    )
    args = parser.parse_args()

    if args.fix:
        changed = fix_shell_scripts()
        if not changed:
            print("Page shell audit — all nav pages have standard scripts.")
            return 0
        print(f"Page shell fix — updated {len(changed)} page(s):")
        for rel, inserted in changed:
            print(f"  {rel}: +{', '.join(inserted)}")
        remaining = audit_shell_scripts()
        if remaining:
            print(f"\nWARN — {len(remaining)} page(s) still missing scripts after fix")
            return 1
        print("\nOK — standard shell scripts present on all nav pages.")
        return 0

    issues = audit_shell_scripts()
    if not issues:
        print("Page shell audit OK — standard scripts present on all nav pages.")
        return 0

    print(f"Page shell audit — {len(issues)} page(s) missing standard scripts:\n")
    for rel, missing in sorted(issues.items()):
        print(f"  {rel}")
        print(f"    missing: {', '.join(missing)}")
    print("\nRun with --fix to insert missing scripts.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
