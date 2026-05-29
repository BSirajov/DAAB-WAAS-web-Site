#!/usr/bin/env python3
"""Wrap executive-board member names with links to scientist profile cards."""
from __future__ import annotations

import re

from _paths import ROOT

PHOTO_SLUG_RE = re.compile(r"board-members-photos/(?P<slug>[\w-]+)\.png")
NAME_RE = re.compile(r'<h2 class="person-name">([^<]*)</h2>')

PAGES = (
    ROOT / "az" / "executive-board.html",
    ROOT / "en" / "executive-board.html",
)


def find_person_body_close(html: str, body_start: int) -> int:
    open_tag = '<div class="person-body">'
    if not html.startswith(open_tag, body_start):
        raise ValueError("expected person-body at body_start")
    i = body_start + len(open_tag)
    depth = 1
    while i < len(html):
        next_open = html.find("<div", i)
        next_close = html.find("</div>", i)
        if next_close == -1:
            raise ValueError("unclosed person-body")
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
            continue
        depth -= 1
        if depth == 0:
            return next_close
        i = next_close + len("</div>")
    raise ValueError("unclosed person-body")


def link_names(text: str) -> tuple[str, int]:
    count = 0
    search_from = 0
    while True:
        photo = PHOTO_SLUG_RE.search(text, search_from)
        if not photo:
            break
        slug = photo.group("slug")
        body_start = text.find('<div class="person-body">', photo.end())
        if body_start == -1:
            break
        close_idx = find_person_body_close(text, body_start)
        body_open = body_start + len('<div class="person-body">')
        body_inner = text[body_open:close_idx]
        if "person-name-link" in body_inner:
            search_from = close_idx + len("</div>")
            continue
        match = NAME_RE.search(body_inner)
        if not match:
            search_from = close_idx + len("</div>")
            continue
        name = match.group(1)
        linked = (
            f'<h2 class="person-name"><a class="person-name-link" '
            f'href="scientists/profiles.html#{slug}">{name}</a></h2>'
        )
        new_body_inner = NAME_RE.sub(linked, body_inner, count=1)
        text = text[:body_open] + new_body_inner + text[close_idx:]
        count += 1
        search_from = body_open + len(new_body_inner)
    return text, count


def main() -> None:
    for path in PAGES:
        original = path.read_text(encoding="utf-8")
        updated, n = link_names(original)
        if n:
            path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"  {path.relative_to(ROOT)}: {n} name link(s)")


if __name__ == "__main__":
    main()
