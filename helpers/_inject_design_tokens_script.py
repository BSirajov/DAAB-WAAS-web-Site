#!/usr/bin/env python3
"""Insert daab-design-tokens.js before daab-nav.js on locale HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

SCRIPT_TAG = '<script src="{root}js/daab-design-tokens.js?v=1" defer></script>'
PATTERN = re.compile(
    r'(<script\s+src="[^"]*daab-nav\.js[^"]*"\s+defer></script>)',
    re.IGNORECASE,
)


def asset_root_for(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def main() -> None:
    updated = 0
    for lang in ("az", "en"):
        base = ROOT / lang
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            if "daab-design-tokens.js" in text:
                continue
            if "daab-nav.js" not in text:
                continue
            root = asset_root_for(path)
            tag = SCRIPT_TAG.format(root=root)

            def repl(m: re.Match[str]) -> str:
                return tag + "\n" + m.group(1)

            new_text, n = PATTERN.subn(repl, text, count=1)
            if n:
                path.write_text(new_text, encoding="utf-8")
                updated += 1
                print("updated", path.relative_to(ROOT))
    print(f"done: {updated} files")


if __name__ == "__main__":
    main()
