"""Replace inline footers with canonical FOOTER_AZ_HTML / FOOTER_EN_HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _footer_leader_snippets import FOOTER_AZ_HTML, FOOTER_EN_HTML
from _paths import ROOT

FOOTER_RE = re.compile(r"<footer class=\"footer-pro\">.*?</footer>", re.DOTALL)

TARGETS: tuple[tuple[Path, str], ...] = (
    (ROOT / "az" / "application.html", "az"),
    (ROOT / "en" / "application.html", "en"),
    (ROOT / "az" / "mission.html", "az"),
    (ROOT / "en" / "mission.html", "en"),
)


def footer_for(lang: str) -> str:
    return FOOTER_AZ_HTML if lang == "az" else FOOTER_EN_HTML


def inject_footer(path: Path, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = FOOTER_RE.subn(footer_for(lang), text, count=1)
    if n != 1:
        raise SystemExit(f"Footer not found in {path.relative_to(ROOT)}")
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    updated = 0
    for path, lang in TARGETS:
        if inject_footer(path, lang):
            print(f"Updated {path.relative_to(ROOT)}")
            updated += 1
        else:
            print(f"Unchanged {path.relative_to(ROOT)}")
    print(f"Done — {updated} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
