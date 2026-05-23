"""Inject daab-lang-position.js on all live AZ/EN pages (after daab-i18n.js)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

SNIPPET = '<script src="{prefix}js/daab-lang-position.js?v=3" defer></script>'
MARKER = "daab-lang-position.js"


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    m = re.search(
        r'(<script src="[^"]*daab-i18n\.js[^"]*" defer></script>)',
        text,
        re.I,
    )
    if not m:
        return False
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(("az/scientists/", "en/scientists/")):
        prefix = "../../"
    elif rel.startswith(("az/", "en/")):
        prefix = "../"
    else:
        prefix = ""
    insert = SNIPPET.format(prefix=prefix)
    text = text[: m.end()] + "\n" + insert + text[m.end() :]
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    updated = 0
    for pattern in ("az/**/*.html", "en/**/*.html"):
        for path in sorted(ROOT.glob(pattern)):
            if inject(path):
                updated += 1
                print(path.relative_to(ROOT))
    print(f"Injected on {updated} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
