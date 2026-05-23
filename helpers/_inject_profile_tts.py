"""Inject profile TTS assets on az/en scientists/profiles.html."""
from __future__ import annotations

from _paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT

CSS_MARK = "scientists-profile-tts.css"
CSS_SNIPPET = '<link href="{prefix}css/scientists-profile-tts.css?v=2" rel="stylesheet"/>'
JS_MARK = "daab-profile-tts.js"
JS_SNIPPET = '<script src="{prefix}js/daab-profile-tts.js?v=8" defer></script>'


def inject(path, prefix: str) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")

    if CSS_MARK not in text:
        needle = "scientists-catalog-toolbar.css"
        idx = text.find(needle)
        if idx >= 0:
            line_end = text.find("\n", idx)
            if line_end >= 0:
                insert = CSS_SNIPPET.format(prefix=prefix)
                text = text[: line_end + 1] + insert + "\n" + text[line_end + 1 :]
                changes.append("css")

    if JS_MARK not in text:
        anchor = "scientists-cv-filters.js"
        pos = text.find(anchor)
        if pos >= 0:
            line_end = text.find("\n", pos)
            if line_end >= 0:
                insert = JS_SNIPPET.format(prefix=prefix)
                text = text[: line_end + 1] + insert + "\n" + text[line_end + 1 :]
                changes.append("js")

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
