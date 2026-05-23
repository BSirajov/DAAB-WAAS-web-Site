"""Apply Latin personal-name forms to all existing en/*.html pages."""
from __future__ import annotations

from pathlib import Path

try:
    from _paths import ROOT
    from i18n_person_names_en import apply_person_name_latin, write_cache
except ImportError:
    from helpers._paths import ROOT  # type: ignore
    from helpers.i18n_person_names_en import apply_person_name_latin, write_cache  # type: ignore


def main() -> None:
    write_cache()
    count = 0
    for path in sorted(ROOT.joinpath("en").rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        updated = apply_person_name_latin(html)
        if updated != html:
            path.write_text(updated, encoding="utf-8", newline="\n")
            count += 1
            print(f"Updated {path.relative_to(ROOT)}")
    print(f"Latinized names on {count} page(s)")


if __name__ == "__main__":
    main()
