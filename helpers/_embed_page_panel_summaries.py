"""Embed hero panel summary prose from i18n/page-panel-summaries.json."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARIES_PATH = ROOT / "i18n" / "page-panel-summaries.json"
ROUTES_PATH = ROOT / "i18n" / "routes.json"

PANEL_COPY_DIV = re.compile(
    r'(<div class="panel-copy">)(.*?)(</div>)',
    re.DOTALL | re.IGNORECASE,
)
PANEL_COPY_P = re.compile(
    r'(<p class="panel-copy">)(.*?)(</p>)',
    re.DOTALL | re.IGNORECASE,
)
HERO_TEXT_P = re.compile(
    r'(<p class="hero-text(?: panel-copy-lead)?">)(.*?)(</p>)',
    re.DOTALL | re.IGNORECASE,
)
PANEL_TITLE = re.compile(
    r'(<h2 class="panel-title">)(.*?)(</h2>)',
    re.DOTALL | re.IGNORECASE,
)
HERO_PANEL = re.compile(
    r'(<aside\b[^>]*class="hero-panel"[^>]*\b)(aria-label=")[^"]*(")',
    re.DOTALL | re.IGNORECASE,
)


def summary_text(entry: dict, lang: str) -> str:
    raw = entry.get(lang) or entry.get("en") or ""
    if isinstance(raw, list):
        return " ".join(str(part).strip() for part in raw if str(part).strip())
    return str(raw).strip()


def prose_html(text: str) -> str:
    return f'<p class="panel-copy-lead">{html.escape(text, quote=False)}</p>'


def embed_summary(raw: str, text: str, entry: dict | None, lang: str) -> tuple[str, bool]:
    block = prose_html(text)
    updated = raw

    titles = (entry or {}).get("panelTitle") or {}
    arias = (entry or {}).get("panelAria") or {}
    title = titles.get(lang) or titles.get("en")
    aria = arias.get(lang) or arias.get("en")
    if title:
        updated = PANEL_TITLE.sub(
            lambda m: m.group(1) + html.escape(title, quote=False) + m.group(3),
            updated,
            count=1,
        )
    if aria:
        updated = HERO_PANEL.sub(
            lambda m: m.group(1) + m.group(2) + html.escape(aria, quote=True) + m.group(3),
            updated,
            count=1,
        )

    m = PANEL_COPY_DIV.search(updated)
    if m:
        updated = updated[: m.start(2)] + "\n" + block + "\n" + updated[m.end(2) :]
        return updated, updated != raw

    m = PANEL_COPY_P.search(updated)
    if m:
        updated = updated[: m.start()] + f'<div class="panel-copy">\n{block}\n</div>' + updated[m.end() :]
        return updated, updated != raw

    m = HERO_TEXT_P.search(updated)
    if m:
        updated = (
            updated[: m.start()]
            + f'<p class="hero-text panel-copy-lead">{html.escape(text, quote=False)}</p>'
            + updated[m.end() :]
        )
        return updated, updated != raw

    return raw, False


def main() -> None:
    data = json.loads(SUMMARIES_PATH.read_text(encoding="utf-8"))
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
            path = ROOT / rel.replace("/", "\\")
            text = summary_text(entry, lang)
            if not text:
                print(f"  skip (empty): {pid} {lang}")
                continue
            raw = path.read_text(encoding="utf-8")
            updated, changed = embed_summary(raw, text, entry, lang)
            if changed:
                path.write_text(updated, encoding="utf-8")
                done += 1
                print(f"  ok {path.relative_to(ROOT)}")
            else:
                print(f"  no panel target: {path.relative_to(ROOT)}")
    print(f"Updated {done} files ({skipped} route pages without copy)")


if __name__ == "__main__":
    main()
