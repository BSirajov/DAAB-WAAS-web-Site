"""Remove duplicate nav CSS from az/en membership.html; use shared daab-common shell."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

SHELL_CSS = """<link href="../css/daab-common.css?v=21" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=4" rel="stylesheet"/>
<link href="../css/daab-search.css?v=3" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=1" rel="stylesheet"/>
"""

LEGACY_NAV_INLINE = re.compile(
    r"\.nav-strip\{[^}]+\}\s*"
    r"\.nav-inner\{[^}]+\}\.nav-inner::-webkit-scrollbar\{[^}]+\}\s*"
    r"\.nav-brand\{[^}]+\}\.brand-mark\{[^}]+\}\s*"
    r"\.nav-brand-text\{[^}]+\}\.nav-divider\{[^}]+\}\.nav-link\{[^}]+\}\.nav-link:hover,\.nav-link\.active\{[^}]+\}\s*",
    re.DOTALL,
)

RESPONSIVE_NAV_BLOCK = re.compile(
    r'<style id="daab-responsive-nav-final">.*?</style>\s*',
    re.DOTALL,
)

DUPLICATE_SHELL_LINKS = re.compile(
    r'<link href="\.\./css/daab-common\.css\?v=21" rel="stylesheet"/>\s*'
    r'<link href="\.\./css/daab-mobile\.css\?v=4" rel="stylesheet"/>\s*'
    r'<link href="\.\./css/daab-search\.css\?v=1" rel="stylesheet"/>\s*'
    r'<link href="\.\./css/daab-back-to-top\.css\?v=1" rel="stylesheet"/>\s*',
)

MEDIA_760_NAV = re.compile(
    r"@media\(max-width:760px\)\{\.nav-inner\{height:62px;padding:0 14px\}"
)

MEDIA_760_NAV_BRAND = re.compile(r"\.nav-brand-text\{font-size:12px\}")


def fix(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if 'id="daab-responsive-nav-final"' not in text and "daab-common.css?v=21" in text.split("<style>")[0]:
        return False

    marker = 'rel="stylesheet"/>\n<style>'
    if marker in text and "daab-common.css?v=21" not in text.split("<style>", 1)[0]:
        text = text.replace(marker, 'rel="stylesheet"/>\n' + SHELL_CSS + "<style>", 1)

    text = LEGACY_NAV_INLINE.sub("", text)
    text = RESPONSIVE_NAV_BLOCK.sub("", text)
    # After page <style>, drop duplicate shell links (keep hero-summary).
    text = text.replace(
        "</style>\n<link href=\"../css/daab-hero-summary.css?v=1\" rel=\"stylesheet\"/>\n"
        + SHELL_CSS,
        "</style>\n<link href=\"../css/daab-hero-summary.css?v=1\" rel=\"stylesheet\"/>\n",
        1,
    )
    text = MEDIA_760_NAV.sub("@media(max-width:760px){", text)
    text = MEDIA_760_NAV_BRAND.sub("", text)
    text = re.sub(r"  <script src=", "<script src=", text, count=1)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for rel in ("az/membership.html", "en/membership.html"):
        path = ROOT / rel
        if not path.is_file():
            print(f"skip missing {rel}")
            continue
        if fix(path):
            updated.append(rel)
    print(f"Fixed {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
