#!/usr/bin/env python3
"""Ensure Forum 2024 hub index pages link to rector and ANAS leadership speech pages."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

HUB_PAGES = (
    (ROOT / "az" / "forum" / "2024" / "index.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "index.html", "en"),
)

CARDS = {
    "az": """
<a class="page-card" data-title="Rektorlar nitqləri" href="rector_speeches.html">
<div class="card-icon-wrap">🎓</div>
<div class="card-body">
<h3 class="card-title">Rektorlar</h3>
<div class="card-desc">Azərbaycan universitet rektorlarının Forum 2024-dəki nitqləri.</div>
<div class="card-footer"><span class="card-tag">Oxu</span><span class="card-arrow">↗</span></div>
</div>
</a>
<a class="page-card" data-title="AMEA rəhbərliyi nitqləri" href="anas_leadership_speeches.html">
<div class="card-icon-wrap">🔬</div>
<div class="card-body">
<h3 class="card-title">AMEA rəhbərliyi</h3>
<div class="card-desc">Azərbaycan Milli Elmlər Akademiyasının rəhbərliyinin Forum 2024-dəki nitqləri.</div>
<div class="card-footer"><span class="card-tag">Oxu</span><span class="card-arrow">↗</span></div>
</div>
</a>""".strip(),
    "en": """
<a class="page-card" data-title="Rectors speeches" href="rector_speeches.html">
<div class="card-icon-wrap">🎓</div>
<div class="card-body">
<h3 class="card-title">Rectors</h3>
<div class="card-desc">Speeches by rectors of Azerbaijani universities at Forum 2024.</div>
<div class="card-footer"><span class="card-tag">Read</span><span class="card-arrow">↗</span></div>
</div>
</a>
<a class="page-card" data-title="ANAS Leadership speeches" href="anas_leadership_speeches.html">
<div class="card-icon-wrap">🔬</div>
<div class="card-body">
<h3 class="card-title">ANAS Leadership</h3>
<div class="card-desc">Speeches by leaders of the Azerbaijan National Academy of Sciences at Forum 2024.</div>
<div class="card-footer"><span class="card-tag">Read</span><span class="card-arrow">↗</span></div>
</div>
</a>""".strip(),
}

PROGRAM_CARD = {
    "az": '<a class="page-card" data-title="Proqram sentyabr cədvəl',
    "en": '<a class="page-card" data-title="Programme schedule September',
}

INTRO = {
    "az": (
        "Aşağıdakı kartlar vasitəsilə rəsmi müraciətlər, rektorlar, AMEA rəhbərliyi, "
        "proqram, strateji yol xəritəsi, məruzələr, təəssüratlar, hekayələr, "
        "töhfələr və alimlərimizin siyahısına keçid edə bilərsiniz."
    ),
    "en": (
        "Use the cards below to open official addresses, rectors, ANAS leadership, "
        "the programme, the strategic roadmap, presentations, impressions, stories, "
        "contributions, and the scientists directory."
    ),
}

OLD_INTRO = {
    "az": (
        "Aşağıdakı kartlar vasitəsilə rəsmi müraciətlər, proqram, strateji yol xəritəsi, "
        "məruzələr, təəssüratlar, forumla bağlı hekayələr, töhfələr və əməkdaşlıq və "
        "alimlərimizin siyahısına keçid edə bilərsiniz."
    ),
    "en": (
        "Use the cards below to open official addresses, the programme, the strategic roadmap, "
        "presentations, impressions, stories of the forum, contributions and cooperation, and the "
        "scientists directory."
    ),
}


def sync_file(path: Path, lang: str) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    if "rector_speeches.html" not in text:
        needle = "\n" + PROGRAM_CARD[lang]
        idx = text.find(needle)
        if idx < 0:
            raise SystemExit(f"Program card anchor not found in {path.relative_to(ROOT)}")
        text = text[:idx] + "\n" + CARDS[lang] + text[idx:]
        changed = True

    if OLD_INTRO[lang] in text:
        text = text.replace(OLD_INTRO[lang], INTRO[lang])
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    for path, lang in HUB_PAGES:
        if sync_file(path, lang):
            print(f"updated {path.relative_to(ROOT)}")
        else:
            print(f"ok {path.relative_to(ROOT)} (speech cards already present)")


if __name__ == "__main__":
    main()
