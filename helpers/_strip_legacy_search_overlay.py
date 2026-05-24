"""Remove legacy inline search overlay markup and duplicate CSS from live pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

LIVE_DIRS = ("az", "en")

OVERLAY_HTML_RE = re.compile(
    r'<div aria-label="(?:Axtarış|Search)" aria-modal="true" id="search-overlay" role="dialog">\s*'
    r'<div class="search-modal">\s*'
    r'<div class="search-input-row">.*?</div>\s*'
    r'<div class="search-results" id="search-results">.*?</div>\s*'
    r'<div class="search-hint">.*?</div>\s*'
    r"</div>\s*"
    r"</div>\s*",
    re.DOTALL | re.IGNORECASE,
)

CHARTER_CSS_RE = re.compile(
    r"/\* ══ SEARCH OVERLAY ══ \*/\s*"
    r"#search-overlay\{display:none;.*?"
    r"\.search-hint kbd\{[^\}]+\}\s*\n?",
    re.DOTALL,
)

MEMBERSHIP_CSS_RE = re.compile(
    r"#search-overlay\{display:none;.*?\}\s*"
    r"(?:@media\(max-width:720px\)\{[^}]+\}\s*)?",
    re.DOTALL,
)

SEARCH_COMMENT_RE = re.compile(r"<!-- ══ SEARCH OVERLAY ══ -->\s*", re.I)
BODY_SEARCH_SCRIPT_RE = re.compile(
    r'\n?<script[^>]+daab-search\.js[^>]*></script>(?=\s*</body>)',
    re.I,
)


def strip(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    new_text, n = OVERLAY_HTML_RE.subn("", text)
    if n:
        changes.append("overlay-html")
        text = new_text

    new_text, n = CHARTER_CSS_RE.subn("", text)
    if n:
        changes.append("charter-css")
        text = new_text

    new_text, n = MEMBERSHIP_CSS_RE.subn("", text)
    if n:
        changes.append("membership-css")
        text = new_text

    new_text, n = SEARCH_COMMENT_RE.subn("", text)
    if n:
        changes.append("comment")
        text = new_text

    new_text, n = BODY_SEARCH_SCRIPT_RE.subn("", text)
    if n:
        changes.append("body-script")
        text = new_text

    # Normalize glued body tags after overlay removal.
    text = re.sub(
        r"(<body[^>]*>)\s*(<a class=\"skip\")",
        r"\1\n\2",
        text,
        count=1,
    )
    return text, changes


def main() -> None:
    updated: list[str] = []
    for locale in LIVE_DIRS:
        base = ROOT / locale
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            new_text, changes = strip(text)
            if changes:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                rel = path.relative_to(ROOT).as_posix()
                updated.append(f"{rel} ({', '.join(changes)})")
    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
