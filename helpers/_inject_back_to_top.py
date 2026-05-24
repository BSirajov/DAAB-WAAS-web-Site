"""Inject back-to-top CSS/JS on live az/, en/, and gateway pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_MARKER = "daab-back-to-top.css"
JS_MARKER = "daab-back-to-top.js"
CSS_V = "1"
JS_V = "2"
I18N_V = "12"

LIVE_DIRS = ("az", "en")
GATEWAY = ROOT / "index.html"


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
    for pattern in (
        r"(<link[^>]+daab-search\.css[^>]*>)",
        r"(<link[^>]+daab-mobile\.css[^>]*>)",
    ):
        m = re.search(pattern, text, re.I)
        if m:
            return text[: m.end()] + "\n" + link + text[m.end() :], True
    return text, False


def inject_js(text: str, prefix: str) -> tuple[str, bool]:
    if JS_MARKER in text:
        new_text, n = re.subn(
            rf'src="{re.escape(prefix)}js/{JS_MARKER}\?v=\d+"',
            f'src="{prefix}js/{JS_MARKER}?v={JS_V}"',
            text,
            count=1,
        )
        return (new_text, n > 0) if n else (text, False)
    tag = f'<script src="{prefix}js/{JS_MARKER}?v={JS_V}" defer></script>'
    m = re.search(r"(<script[^>]+daab-mobile\.js[^>]*></script>)", text, re.I)
    if m:
        return text[: m.end()] + "\n" + tag + text[m.end() :], True
    m = re.search(r"(<script[^>]+daab-shell\.js[^>]*></script>)", text, re.I)
    if m:
        return text[: m.end()] + "\n" + tag + text[m.end() :], True
    if "</body>" in text:
        return text.replace("</body>", tag + "\n</body>", 1), True
    return text, False


def bump_i18n(text: str) -> tuple[str, bool]:
    new_text, n = re.subn(r"daab-i18n\.js\?v=\d+", f"daab-i18n.js?v={I18N_V}", text)
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


def main() -> None:
    updated: list[str] = []
    for locale in LIVE_DIRS:
        base = ROOT / locale
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            changes = process(path)
            if changes:
                updated.append(f"{path.relative_to(ROOT).as_posix()} ({', '.join(changes)})")

    if GATEWAY.is_file():
        changes = process(GATEWAY)
        if changes:
            updated.append(f"index.html ({', '.join(changes)})")

    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
