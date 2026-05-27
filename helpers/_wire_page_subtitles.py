"""Add daab-page-subtitle.js after daab-shell.js; bump daab-hero-summary.css version."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUB = "daab-page-subtitle.js"
SHELL_PAT = re.compile(
    r'(<script(?:\s+defer(?:="")?)?\s+src="([^"]*?)js/daab-shell\.js\?v=\d+"(?:\s+defer(?:="")?)?\s*></script>)'
)
HERO_CSS_PAT = re.compile(r"daab-hero-summary\.css\?v=1")


def main() -> None:
    wired = 0
    bumped = 0
    for path in sorted((ROOT / "az").rglob("*.html")) + sorted((ROOT / "en").rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        changed = False
        if SUB not in text and "daab-shell.js" in text:

            def repl(m: re.Match[str]) -> str:
                prefix = m.group(2)
                return (
                    m.group(1)
                    + f'\n<script src="{prefix}js/{SUB}?v=1" defer></script>'
                )

            new_text, n = SHELL_PAT.subn(repl, text, count=1)
            if n:
                text = new_text
                wired += 1
                changed = True
        if "daab-hero-summary.css?v=1" in text:
            text = HERO_CSS_PAT.sub("daab-hero-summary.css?v=2", text)
            bumped += 1
            changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
    print(f"subtitle script added: {wired}")
    print(f"hero-summary css bumped: {bumped}")


if __name__ == "__main__":
    main()
