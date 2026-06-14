#!/usr/bin/env python3
"""Run all automated pre-deploy checks. Exit 1 if any fail."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _paths import ROOT, HELPERS

CHECKS = [
    ("Site links and assets", ["python", str(HELPERS / "_validate_site.py")]),
    ("Bilingual routes and sitemap", ["python", str(HELPERS / "_validate_bilingual.py")]),
    ("Scientists list catalog wiring", ["python", str(HELPERS / "_validate_scientists_list.py")]),
    ("Scientist CV cards", ["python", str(HELPERS / "_validate_cv_cards.py")]),
    ("Scientist name order", ["python", str(HELPERS / "_check_name_order.py")]),
    ("Forum content CSS selectors", ["python", str(HELPERS / "_fix_forum_content_css_selectors.py"), "--audit-only"]),
    ("Artifact consistency (nav/i18n)", ["python", str(HELPERS / "_artifact_audit_temp.py")]),
]


def main() -> int:
    print("DAAB deploy preflight\n")
    failed = False
    for label, cmd in CHECKS:
        print(f"→ {label}")
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (result.stdout or "") + (result.stderr or "")
        for line in out.strip().splitlines():
            print(f"  {line}")
        if result.returncode != 0:
            failed = True
            print(f"  FAILED (exit {result.returncode})")
        print()
    if failed:
        print("Preflight FAILED — fix errors before deploy.")
        return 1
    print("Preflight OK — ready for manual smoke test and upload.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
