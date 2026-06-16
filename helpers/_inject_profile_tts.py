"""Inject profile TTS stylesheet on az/en scientists/profiles.html.

TTS script loads on idle via js/daab-perf.js (deferProfileTts) — do not inject a blocking tag.
"""
from __future__ import annotations

from _paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT

CSS_MARK = "scientists-profile-tts.css"
CSS_SNIPPET = '<link href="{prefix}css/scientists-profile-tts.css?v=3" rel="stylesheet"/>'


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
