#!/usr/bin/env python3
"""Sort scientific-field checkboxes alphabetically within each category."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

AZ_LOWER = str.maketrans(
    "ABCÇDEƏFGĞHXIİJKLMNOÖPQRSŞTUÜVYZ",
    "abcçdeəfgğhxıijklmnoöpqrsştuüvyz",
)
AZ_INDEX = {ch: i for i, ch in enumerate("abcçdeəfgğhxıijklmnoöpqrsştuüvyz")}

ITEM_RE = re.compile(
    r'(\s*)(<div class="sci-item">.*?</div>)(\s*)',
    re.S,
)
BODY_OPEN = '<div class="sci-cat-body">'
LABEL_RE = re.compile(r"<label[^>]*>(.*?)</label>", re.S)


def visible_label(item_html: str) -> str:
    match = LABEL_RE.search(item_html)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return re.sub(r"\s+", " ", text).strip()


def az_sort_key(text: str) -> tuple:
    lowered = text.translate(AZ_LOWER)
    ranks: list[int] = []
    for ch in lowered:
        if ch in AZ_INDEX:
            ranks.append(AZ_INDEX[ch])
        elif ch.isdigit():
            ranks.append(1000 + ord(ch))
        elif ch == " ":
            ranks.append(2000)
        else:
            ranks.append(3000 + ord(ch))
    return tuple(ranks)


def en_sort_key(text: str) -> str:
    return text.casefold()


def sort_body(body: str, lang: str) -> str:
    items = [m.group(2) for m in ITEM_RE.finditer(body)]
    if not items:
        return body
    key_fn = az_sort_key if lang == "az" else en_sort_key
    items.sort(key=lambda html: key_fn(visible_label(html)))
    indent = "            "
    return "\n" + "\n".join(indent + item for item in items) + "\n          "


def replace_bodies(html: str, lang: str) -> tuple[str, int]:
    count = 0
    out: list[str] = []
    i = 0
    while True:
        start = html.find(BODY_OPEN, i)
        if start == -1:
            out.append(html[i:])
            break
        out.append(html[i:start])
        inner_start = start + len(BODY_OPEN)
        pos = inner_start
        depth = 1
        close_at = -1
        while pos < len(html) and depth:
            nxt_open = html.find("<div", pos)
            nxt_close = html.find("</div>", pos)
            if nxt_close == -1:
                raise SystemExit(f"Unclosed sci-cat-body starting at {start}")
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                pos = nxt_open + 4
            else:
                depth -= 1
                if depth == 0:
                    close_at = nxt_close
                    break
                pos = nxt_close + 6
        inner = html[inner_start:close_at]
        out.append(BODY_OPEN + sort_body(inner, lang) + "</div>")
        count += 1
        i = close_at + len("</div>")
    return "".join(out), count


def sort_file(path: Path) -> int:
    lang = "az" if "/az/" in path.as_posix() or "\\az\\" in str(path) else "en"
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8").replace("\r\n", "\n")
    updated, count = replace_bodies(text, lang)
    if updated != text:
        path.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    return count


def main() -> None:
    files = [
        ROOT / "az" / "application.html",
        ROOT / "en" / "application.html",
        ROOT / "az" / "forum" / "2026" / "register.html",
        ROOT / "en" / "forum" / "2026" / "register.html",
        ROOT / "Deployment" / "az" / "application.html",
        ROOT / "Deployment" / "en" / "application.html",
        ROOT / "Deployment" / "az" / "forum" / "2026" / "register.html",
        ROOT / "Deployment" / "en" / "forum" / "2026" / "register.html",
    ]
    for path in files:
        n = sort_file(path)
        print(f"{path.relative_to(ROOT)}: {n} groups")


if __name__ == "__main__":
    main()
