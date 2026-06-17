#!/usr/bin/env python3
"""Harmonize visible locale branding: DAAB on az pages, WAAS on en pages."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from _paths import ROOT
    from _replace_daab_en import transform as en_transform
except ImportError:
    from helpers._paths import ROOT  # type: ignore
    from helpers._replace_daab_en import transform as en_transform  # type: ignore

AZ_COMPOUND = [
    ("DAAB / WAAS", "DAAB"),
    ("DAAB/WAAS", "DAAB"),
    ("WAAS / DAAB", "DAAB"),
    ("WAAS · DAAB", "DAAB"),
]

EN_OG_RE = re.compile(
    r'(<meta\s+(?:property="og:site_name"\s+content="|content=")DAAB/WAAS("\s+property="og:site_name"|"/>))',
    re.I,
)


def patch_az(text: str) -> str:
    protected: list[str] = []

    def stash(m: re.Match[str]) -> str:
        protected.append(m.group(0))
        return f"__PROT_{len(protected) - 1}__"

    for pattern in (
        re.compile(r"https?://[^\s\"'<>]+"),
        re.compile(r"window\.DAAB_[A-Za-z0-9]+"),
        re.compile(r"data-daab-[a-z-]+"),
    ):
        text = pattern.sub(stash, text)

    for old, new in AZ_COMPOUND:
        text = text.replace(old, new)

    text = re.sub(r"\bWAAS\b", "DAAB", text)

    for i, val in enumerate(protected):
        text = text.replace(f"__PROT_{i}__", val)
    return text


def patch_en(text: str) -> str:
    new, _ = en_transform(text)
    new = EN_OG_RE.sub(lambda m: m.group(0).replace("DAAB/WAAS", "WAAS"), new)
    new = new.replace('content="DAAB/WAAS"', 'content="WAAS"')
    return new


def iter_locale_html() -> list[Path]:
    paths: list[Path] = []
    for lang in ("az", "en"):
        root = ROOT / lang
        if root.is_dir():
            paths.extend(sorted(root.rglob("*.html")))
    paths.append(ROOT / "404.html")
    return paths


def main() -> int:
    dry = "--dry-run" in sys.argv
    changed: list[str] = []
    for path in iter_locale_html():
        rel = path.relative_to(ROOT)
        lang = rel.parts[0] if rel.parts and rel.parts[0] in ("az", "en") else "az"
        raw = path.read_text(encoding="utf-8")
        updated = patch_az(raw) if lang == "az" else patch_en(raw)
        if updated != raw:
            changed.append(str(rel))
            if not dry:
                path.write_text(updated, encoding="utf-8", newline="\n")

    for rel in changed:
        print(f"  {'[dry] ' if dry else ''}updated {rel}")
    print(f"{'Would update' if dry else 'Updated'} {len(changed)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
