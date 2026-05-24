"""Inject profile deep-link bootstrap + script on az/en scientists/profiles.html."""
from __future__ import annotations

import re

from _paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT

CSS_MARK = "scientists-profile-deep-link.css"
CSS_SNIPPET = '<link href="{prefix}css/scientists-profile-deep-link.css?v=2" rel="stylesheet"/>'
QR_CSS_MARK = "scientists-profile-qr.css"
QR_CSS_SNIPPET = '<link href="{prefix}css/scientists-profile-qr.css?v=1" rel="stylesheet"/>'
DEEPLINK_MARK = "daab-profile-deep-link.js"
DEEPLINK_SNIPPET = '<script src="{prefix}js/daab-profile-deep-link.js?v=1"></script>'
BOOT_MARK = "daab-profile-hash-boot"
BOOT_SNIPPET = (
    '<script id="daab-profile-hash-boot">\n'
    "(function(){if(!location.hash)return;"
    'if("scrollRestoration"in history)history.scrollRestoration="manual";'
    'document.documentElement.style.scrollBehavior="auto";})();\n'
    "</script>"
)
FILTERS_V = "15"


def inject(path, prefix: str) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")

    if BOOT_MARK not in text:
        idx = text.lower().find("<head>")
        if idx >= 0:
            insert_at = idx + len("<head>")
            text = text[:insert_at] + "\n" + BOOT_SNIPPET + text[insert_at:]
            changes.append("hash-boot")

    if CSS_MARK not in text:
        needle = "scientists-profile-tts.css"
        idx = text.find(needle)
        if idx >= 0:
            line_end = text.find("\n", idx)
            if line_end >= 0:
                insert = CSS_SNIPPET.format(prefix=prefix)
                text = text[: line_end + 1] + insert + "\n" + text[line_end + 1 :]
                changes.append("css")

    if QR_CSS_MARK not in text:
        needle = "scientists-profile-deep-link.css"
        idx = text.find(needle)
        if idx >= 0:
            line_end = text.find("\n", idx)
            if line_end >= 0:
                insert = QR_CSS_SNIPPET.format(prefix=prefix)
                text = text[: line_end + 1] + insert + "\n" + text[line_end + 1 :]
                changes.append("qr-css")

    if DEEPLINK_MARK not in text:
        anchor = "daab-lang-position.js"
        pos = text.find(anchor)
        if pos >= 0:
            line_end = text.find("\n", pos)
            if line_end >= 0:
                insert = DEEPLINK_SNIPPET.format(prefix=prefix) + "\n"
                text = text[: line_end + 1] + insert + text[line_end + 1 :]
                changes.append("deeplink-js")

    new_text, n = re.subn(
        r"scientists-cv-filters\.js\?v=\d+",
        f"scientists-cv-filters.js?v={FILTERS_V}",
        text,
    )
    if n:
        text = new_text
        changes.append("filters-js")

    if changes:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> int:
    for path, prefix in (
        (AZ_SCIENTISTS_PROFILES, "../../"),
        (EN_SCIENTISTS_PROFILES, "../../"),
    ):
        changes = inject(path, prefix)
        if changes:
            print(f"{path.relative_to(ROOT)}: {', '.join(changes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
