"""Embed page subtitles in hero HTML from i18n/page-subtitles.json."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBTITLES_PATH = ROOT / "i18n" / "page-subtitles.json"
ROUTES_PATH = ROOT / "i18n" / "routes.json"

HERO_H1_END = re.compile(
    r"(<header\s+class=\"(?:hero|page-hero)\"[^>]*>.*?<h1\b[^>]*>.*?</h1>)",
    re.DOTALL | re.IGNORECASE,
)
MARKER = "page-hero-subtitle"


def subtitle_tag(text: str) -> str:
    safe = html.escape(text, quote=False)
    return (
        f'\n<p class="{MARKER}" id="{MARKER}" role="doc-subtitle">{safe}</p>'
    )


def embed_in_file(path: Path, text: str) -> bool:
    raw = path.read_text(encoding="utf-8")
    if MARKER in raw:
        # Replace existing subtitle paragraph content
        updated = re.sub(
            rf'<p class="{MARKER}"[^>]*>.*?</p>',
            subtitle_tag(text).strip(),
            raw,
            count=1,
            flags=re.DOTALL,
        )
        if updated != raw:
            path.write_text(updated, encoding="utf-8")
            return True
        return False
    m = HERO_H1_END.search(raw)
    if not m:
        print(f"  skip (no hero h1): {path.relative_to(ROOT)}")
        return False
    updated = raw[: m.end()] + subtitle_tag(text) + raw[m.end() :]
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    data = json.loads(SUBTITLES_PATH.read_text(encoding="utf-8"))
    routes = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    pages = data.get("pages") or {}
    done = 0
    skipped = 0
    for page in routes.get("pages") or []:
        pid = page.get("id")
        entry = pages.get(pid)
        if not entry:
            skipped += 1
            continue
        for lang in ("az", "en"):
            rel = page.get(lang)
            if not rel:
                continue
            path = ROOT / rel.replace("/", "\\") if "\\" in str(ROOT) else ROOT / rel
            text = entry.get(lang) or entry.get("en") or ""
            if not text:
                continue
            if embed_in_file(path, text):
                done += 1
                print(f"  ok {path.relative_to(ROOT)}")
    print(f"Embedded/updated {done} subtitles ({skipped} route pages without copy)")


if __name__ == "__main__":
    main()
