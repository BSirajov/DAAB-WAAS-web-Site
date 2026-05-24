"""Align az/en membership.html backgrounds with daab-common (remove legacy overrides)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

LEGACY_ROOT = re.compile(
    r":root\{--ink:[^}]+\}\s*"
    r"\*\{box-sizing:border-box\}html\{scroll-behavior:smooth\}\s*"
    r"\.membership-page\{margin:0;font-family:[^}]+\}\s*",
    re.DOTALL,
)

LEGACY_FOOTER = re.compile(
    r"\.footer-pro\{background:linear-gradient\(135deg,#102033,#1a6fa8\)[^}]+\}"
    r"\.footer-pro:before\{[^}]+\}"
    r"\.footer-inner\{[^}]+\}"
    r"\.footer-brand\{[^}]+\}"
    r"\.footer-brand h3\{[^}]+\}"
    r"\.footer-grid\{[^}]+\}"
    r"\.footer-col\{[^}]+\}"
    r"\.footer-title\{[^}]+\}"
    r"\.footer-item,\.footer-address,\.footer-leader\{[^}]+\}"
    r"\.footer-item a,\.footer-address a\{[^}]+\}"
    r"\.footer-bottom\{[^}]+\}",
    re.DOTALL,
)


def fix(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = LEGACY_ROOT.sub("", text)
    text = LEGACY_FOOTER.sub("", text)
    text = text.replace(
        "background:rgba(255,255,255,.88);border:1px solid rgba(255,255,255,.72)",
        "background:rgba(245,251,255,.96);border:1px solid #9ed6f5",
    )
    text = text.replace(
        "background:rgba(255,255,255,.9);border:1px solid rgba(26,111,168,.12)",
        "background:rgba(245,251,255,.96);border:1px solid #9ed6f5",
    )

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for rel in ("az/membership.html", "en/membership.html"):
        path = ROOT / rel
        if fix(path):
            updated.append(rel)
    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
