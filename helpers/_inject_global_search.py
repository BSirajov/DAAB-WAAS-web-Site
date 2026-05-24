"""Inject global search CSS/JS on all live az/ and en/ pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_MARKER = "daab-search.css"
JS_MARKER = "daab-search.js"
CSS_V = "1"
JS_V = "3"
I18N_V = "12"

LIVE_DIRS = ("az", "en")
GATEWAY = ROOT / "index.html"

BODY_SEARCH_SCRIPT_RE = re.compile(
    r'\n?<script[^>]+daab-search\.js[^>]*></script>(?=\s*</body>)',
    re.I,
)
SEARCH_SCRIPT_RE = re.compile(
    rf'<script[^>]+{re.escape(JS_MARKER)}[^>]*></script>\s*',
    re.I,
)


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(("az/scientists/", "en/scientists/")):
        return "../../"
    if rel.startswith(("az/", "en/")):
        return "../"
    return ""


def inject_css(text: str, prefix: str) -> tuple[str, bool]:
    if CSS_MARKER in text:
        new_text, n = re.subn(
            rf'href="{re.escape(prefix)}css/{CSS_MARKER}\?v=\d+"',
            f'href="{prefix}css/{CSS_MARKER}?v={CSS_V}"',
            text,
            count=1,
        )
        return (new_text, n > 0) if n else (text, False)
    link = f'<link href="{prefix}css/{CSS_MARKER}?v={CSS_V}" rel="stylesheet"/>'
    m = re.search(r'(<link[^>]+daab-mobile\.css[^>]*>)', text, re.I)
    if m:
        insert_at = m.end()
        return text[:insert_at] + "\n" + link + text[insert_at:], True
    m = re.search(r'(<link[^>]+daab-lang\.css[^>]*>)', text, re.I)
    if m:
        insert_at = m.end()
        return text[:insert_at] + "\n" + link + text[insert_at:], True
    m = re.search(r'(<link[^>]+daab-nav-mega\.css[^>]*>)', text, re.I)
    if m:
        insert_at = m.end()
        return text[:insert_at] + "\n" + link + text[insert_at:], True
    return text, False


def inject_js(text: str, prefix: str) -> tuple[str, bool]:
    tag = f'<script src="{prefix}js/{JS_MARKER}?v={JS_V}" defer></script>'
    original = text

    text = BODY_SEARCH_SCRIPT_RE.sub("", text)
    text = SEARCH_SCRIPT_RE.sub("", text)

    shell = re.search(r'(<script[^>]+daab-shell\.js[^>]*></script>)', text, re.I)
    if shell:
        insert_at = shell.end()
        text = text[:insert_at] + "\n" + tag + text[insert_at:]
    elif "</body>" in text and "daab-gateway" in text:
        text = text.replace("</body>", tag + "\n</body>", 1)

    return text, text != original


def bump_i18n(text: str) -> tuple[str, bool]:
    new_text, n = re.subn(
        r"daab-i18n\.js\?v=\d+",
        f"daab-i18n.js?v={I18N_V}",
        text,
    )
    return new_text, n > 0


def process(path: Path) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")
    prefix = asset_prefix(path)

    text, css_ok = inject_css(text, prefix)
    if css_ok:
        changes.append("css")

    text, js_ok = inject_js(text, prefix)
    if js_ok:
        changes.append("js")

    text, i18n_ok = bump_i18n(text)
    if i18n_ok:
        changes.append("i18n")

    if changes:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def process_gateway() -> list[str]:
    if not GATEWAY.is_file():
        return []
    text = GATEWAY.read_text(encoding="utf-8")
    changes: list[str] = []
    original = text

    text, css_ok = inject_css(text, "")
    if css_ok:
        changes.append("css")

    i18n_tag = f'<script src="js/daab-i18n.js?v={I18N_V}" defer></script>'
    if "daab-i18n.js" not in text:
        text = text.replace("</head>", i18n_tag + "\n</head>", 1)
        changes.append("i18n")

    text, js_ok = inject_js(text, "")
    if js_ok:
        changes.append("js")

    if changes and text != original:
        GATEWAY.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> None:
    updated: list[str] = []
    for locale in LIVE_DIRS:
        base = ROOT / locale
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            changes = process(path)
            if changes:
                rel = path.relative_to(ROOT).as_posix()
                updated.append(f"{rel} ({', '.join(changes)})")

    gateway_changes = process_gateway()
    if gateway_changes:
        updated.append(f"index.html ({', '.join(gateway_changes)})")

    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
