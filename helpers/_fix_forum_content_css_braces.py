#!/usr/bin/env python3
"""Fix broken `{,` selector lines left by _sync_forum_content_speech_pages.py."""
from __future__ import annotations

import re

from _paths import ROOT

CSS = ROOT / "css" / "daab-forum-content.css"
BROKEN = re.compile(r'^(\s*html\[data-daab-page-id="[^"]+"\][^{]+)\{,\s*$')


def fix(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    removed = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        m = BROKEN.match(line)
        if m:
            removed += 1
            i += 1
            continue

        out.append(line)
        # If next lines were broken duplicates, we already skipped them.
        # Ensure the last selector before a property block opens with " {".
        if (
            i + 1 < len(lines)
            and line.strip().startswith("html[")
            and line.rstrip().endswith(",")
            and not lines[i + 1].strip().startswith("html[")
        ):
            # peek: find last consecutive html[ selector
            j = i
            while j + 1 < len(lines) and lines[j + 1].strip().startswith("html["):
                j += 1
            if j > i and not lines[j + 1].strip().startswith("html["):
                last = out[-1 - (j - i) :]
                # last line in out at index len(out)-1 is lines[j] which we haven't added yet
                pass
        i += 1

    # Second pass: last html selector before non-html line should end with " {"
    result: list[str] = []
    n = len(out)
    for idx, line in enumerate(out):
        if (
            line.strip().startswith("html[")
            and line.rstrip().endswith(",")
            and idx + 1 < n
            and not out[idx + 1].strip().startswith("html[")
        ):
            result.append(line.rstrip().rstrip(",") + " {")
        else:
            result.append(line)

    return "\n".join(result) + "\n", removed


if __name__ == "__main__":
    raw = CSS.read_text(encoding="utf-8")
    # Drop corrupted `{,` lines entirely.
    lines = [ln for ln in raw.splitlines() if not ln.rstrip().endswith("{,")]
    removed = len(raw.splitlines()) - len(lines)
    text = "\n".join(lines) + "\n"

    # Open blocks: trailing comma on last selector -> " {"
    fixed_lines: list[str] = []
    for idx, line in enumerate(text.splitlines()):
        if (
            line.strip().startswith("html[")
            and line.rstrip().endswith(",")
            and idx + 1 < len(text.splitlines())
            and not text.splitlines()[idx + 1].strip().startswith("html[")
        ):
            fixed_lines.append(line.rstrip().rstrip(",") + " {")
        else:
            fixed_lines.append(line)
    fixed = "\n".join(fixed_lines) + "\n"

    # Root vars: cooperation should be last before "{"
    fixed = fixed.replace(
        'html[data-daab-page-id="forum-cooperation"] {',
        'html[data-daab-page-id="forum-cooperation"] {',
        1,
    )

    CSS.write_text(fixed, encoding="utf-8", newline="\n")
    print(f"Removed {removed} broken lines; fixed trailing commas before rule bodies")
