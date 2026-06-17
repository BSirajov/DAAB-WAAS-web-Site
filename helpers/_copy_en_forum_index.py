#!/usr/bin/env python3
"""Create en/forum/2024/index.html from the Azerbaijani hub page."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

SRC = ROOT / "az" / "forum" / "2024" / "index.html"
DST = ROOT / "en" / "forum" / "2024" / "index.html"


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace('lang="az"', 'lang="en"', 1)
    text = text.replace('data-daab-lang="az"', 'data-daab-lang="en"')
    text = text.replace("Forumun mənzərəsi — DAAB", "I Forum – Highlights — WAAS")
    text = text.replace("<h1><span>Forumun mənzərəsi</span></h1>", "<h1><span>I Forum – Highlights</span></h1>")
    text = text.replace("<h2>Forumun mənzərəsi</h2>", "<h2>Highlights</h2>")
    text = text.replace(
        "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu — kitab məzmunu və arxiv.",
        "First Forum of Azerbaijani Scientists Living Abroad — book content and archive.",
    )
    text = text.replace("Məzmuna keç", "Skip to content")
    text = text.replace('aria-label="Səhifə yolu"', 'aria-label="Breadcrumb"')
    text = text.replace(
        '<a href="../../index.html">Ana səhifə</a><span aria-hidden="true">›</span><a href="index.html">I Forum</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">Ümumi Mənzərə</span>',
        '<a href="../../index.html">Home</a><span aria-hidden="true">›</span><a href="index.html">I Forum</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">Highlights</span>',
    )
    text = text.replace(
        "Kitabdan seçilmiş rəsmi mətnlər, proqram, məruzələr və iştirakçı təəssüratları.",
        "Selected official texts, programme, presentations and participant impressions from the book.",
    )
    text = text.replace(
        "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu",
        "First Forum of Azerbaijani Scientists Living Abroad",
    )
    text = text.replace(
        "9–11 sentyabr 2024, Bakı – Xankəndi – Şuşa. Bu bölmədə forum kitabından seçilmiş məzmun —",
        "9–11 September 2024, Baku – Khankendi – Shusha. This section publishes selected content from the forum book —",
    )
    text = text.replace(
        "<strong>səhifə 24–115</strong> (rəsmi çıxışlar, proqram, nitqlər, məruzələr) və",
        "<strong>pages 24–115</strong> (official addresses, programme, speeches, presentations) and",
    )
    text = text.replace(
        "<strong>səhifə 176–203</strong> (iştirakçı təəssüratları) — DAAB saytında strukturlaşdırılıb.",
        "<strong>pages 176–203</strong> (participant impressions) — structured on the WAAS website.",
    )
    text = text.replace("Kitabı PDF yüklə", "Download book")
    text = text.replace("Kitabı yüklə", "Download book")
    text = text.replace("Rəsmi müraciətlər", "Official addresses")
    text = text.replace("Rektorların nitqləri", "Rectors")
    text = text.replace(
        "Azərbaycan universitet rektorlarının Forum 2024-dəki nitqləri.",
        "Speeches by rectors of Azerbaijani universities at Forum 2024.",
    )
    text = text.replace("AMEA rəhbərliyinin nitqləri", "ANAS Leadership")
    text = text.replace(
        "Azərbaycan Milli Elmlər Akademiyası rəhbərlərinin Forumla bağlı görüşləri.",
        "Speeches by leaders of the Azerbaijan National Academy of Sciences at Forum 2024.",
    )
    text = text.replace(
        "Aşağıdakı kartlar vasitəsilə rəsmi müraciətlər, universitetlər, elm akademiyası, proqram, strateji yol xəritəsi, məruzələr, təəssüratlar, hekayələr, töhfələr və alimlərimizin siyahısına keçid edə bilərsiniz.",
        "Use the cards below to open official addresses, universities, academy of sciences, the programme, the strategic roadmap, presentations, impressions, stories, contributions, and the scientists directory.",
    )
    text = text.replace(
        "Prezident, Nobel laureatları və alimlərin müraciəti (kitab səh. 24–28).",
        "President, Nobel laureates and scientists' appeal (book pp. 24–28).",
    )
    text = text.replace("Forumun proqramı", "Programme")
    text = text.replace("Forumla bağlı hekayələr", "Stories")
    text = text.replace("Töhfələr və əməkdaşlıq", "Contributions")
    text = text.replace(
        "9–11 sentyabr 2024 tədbir cədvəli (kitab səh. 31–35).",
        "9–11 September 2024 schedule (book pp. 31–35).",
    )
    text = text.replace("Nitqlər və müzakirələr", "Speeches and discussions")
    text = text.replace(
        "Dövlət, universitet və diaspora çıxışları (kitab səh. 36–69).",
        "State, university and diaspora addresses (book pp. 36–69).",
    )
    text = text.replace("Məruzələr", "Presentations")
    text = text.replace(
        "Foruma təqdim olunmuş elmi məruzələr (kitab səh. 70–114).",
        "Scientific presentations at the forum (book pp. 70–114).",
    )
    text = text.replace(
        "Foruma təqdim olunmuş elmi məruzələr.",
        "Scientific presentations at the forum (book pp. 70–114).",
    )
    text = text.replace("Təəssüratlar", "Impressions")
    text = text.replace(
        "İştirakçıların şəxsi təəssüratları (kitab səh. 176–203).",
        "Participants' personal impressions (book pp. 176–203).",
    )
    text = text.replace("Alimlər kataloqu", "Scientists directory")
    text = text.replace(
        "Tam akademik profillər (sayt kataloqu).",
        "Full academic profiles (site directory).",
    )
    text = text.replace("Kataloq", "Directory")
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
