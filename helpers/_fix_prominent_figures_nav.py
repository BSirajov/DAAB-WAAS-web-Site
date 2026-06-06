#!/usr/bin/env python3
"""Point prominent figure profiles back to az/encyclopedia.html instead of missing catalog."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

FIGURES = ROOT / "az" / "prominent_figures"
OLD_HREFS = (
    "../gorkemli_shexsiyyetler_200_AZ.html",
    "../gorkemli_shexsiyyetler_AZ.html",
    "../../../encyclopedia.html",
)
NEW = "../../encyclopedia.html"
OLD_LABEL = "Görkəmli şəxsiyyətlər"
NEW_LABEL = "Ensiklopediya"


def main() -> None:
    n = 0
    for path in FIGURES.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if not any(h in text for h in OLD_HREFS) and OLD_LABEL not in text:
            continue
        for old in OLD_HREFS:
            text = text.replace(old, NEW)
        text = text.replace(OLD_LABEL, NEW_LABEL)
        path.write_text(text, encoding="utf-8", newline="\n")
        n += 1
        print(path.relative_to(ROOT))
    print(f"Updated {n} profile pages")


if __name__ == "__main__":
    main()
