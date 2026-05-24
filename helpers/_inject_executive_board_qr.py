"""Add profile QR codes to executive-board member cards (AZ + EN)."""
from __future__ import annotations

import re

from _paths import ROOT

QR_CSS = '<link href="../css/scientists-profile-qr.css?v=1" rel="stylesheet"/>'
PHOTO_SLUG_RE = re.compile(r"board-members-photos/(?P<slug>[\w-]+)\.png")

STRINGS = {
    "az": {
        "title": "Bu alimin profil səhifəsinə keçid",
        "aria": "Profil linkinin QR kodu",
    },
    "en": {
        "title": "Link to this scientist's profile page",
        "aria": "QR code for profile link",
    },
}

PAGES = (
    (ROOT / "az" / "executive-board.html", "az"),
    (ROOT / "en" / "executive-board.html", "en"),
)


def qr_markup(slug: str, lang: str) -> str:
    s = STRINGS[lang]
    return (
        f'<a class="board-card-qr-link card-qr-link" href="scientists/profiles.html#{slug}" '
        f'title="{s["title"]}" aria-label="{s["aria"]}">\n'
        f'<img class="board-card-qr card-qr" src="../images/qr/{lang}/{slug}.png?v=1" '
        f'width="64" height="64" alt="" decoding="async" loading="lazy"/>\n'
        f"</a>\n"
    )


def find_person_body_close(html: str, body_start: int) -> int:
    """Return index of closing </div> for person-body opened at body_start."""
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


def inject_page(path, lang: str) -> int:
    text = path.read_text(encoding="utf-8")
    if QR_CSS not in text:
        text = text.replace(
            '<link href="../css/daab-executive-board.css',
            QR_CSS + "\n" + '<link href="../css/daab-executive-board.css',
            1,
        )
        if QR_CSS not in text and "<style>" in text:
            text = text.replace(
                '<link href="../css/daab-mobile.css',
                QR_CSS + "\n" + '<link href="../css/daab-mobile.css',
                1,
            )

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
        body_inner = text[body_start + len('<div class="person-body">'):close_idx]
        if "board-card-qr-link" not in body_inner:
            qr = qr_markup(slug, lang)
            text = text[:close_idx] + qr + text[close_idx:]
            count += 1
            search_from = close_idx + len(qr) + len("</div>")
        else:
            search_from = close_idx + len("</div>")
    if count:
        path.write_text(text, encoding="utf-8", newline="\n")
    return count


def main() -> None:
    total = 0
    for path, lang in PAGES:
        n = inject_page(path, lang)
        print(f"  {path.relative_to(ROOT)}: {n} QR code(s)")
        total += n
    if not total:
        print("  (all cards already have QR codes)")


if __name__ == "__main__":
    main()
