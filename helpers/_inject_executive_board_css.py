"""Replace inline <style> on executive-board pages with daab-executive-board.css."""
from __future__ import annotations

import re

from _paths import ROOT

LINK = '<link href="../css/daab-executive-board.css?v=3" rel="stylesheet"/>'

PAGES = (
    ROOT / "az" / "executive-board.html",
    ROOT / "en" / "executive-board.html",
)


def main() -> None:
    for path in PAGES:
        text = path.read_text(encoding="utf-8")
        new, n = re.subn(r"<style>.*?</style>", LINK, text, count=1, flags=re.DOTALL)
        if n != 1:
            raise SystemExit(f"{path.name}: expected 1 style block, got {n}")
        path.write_text(new, encoding="utf-8", newline="\n")
        print(f"  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
