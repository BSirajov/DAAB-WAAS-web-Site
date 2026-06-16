#!/usr/bin/env python3
"""One-off audit runner for comprehensive review report."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from _paths import ROOT


def deploy_html() -> list[Path]:
    out: list[Path] = []
    for base in (ROOT / "az", ROOT / "en"):
        for p in base.rglob("*.html"):
            if p.parent.name == "application" and p.parent.parent.name in ("az", "en"):
                continue
            out.append(p)
    return sorted(out)


def main() -> None:
    paths = deploy_html()

    imgs: list[tuple[int, str]] = []
    for p in (ROOT / "images").rglob("*"):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            try:
                sz = p.stat().st_size
                if sz > 500_000:
                    imgs.append((sz, str(p.relative_to(ROOT)).replace("\\", "/")))
            except OSError:
                pass
    imgs.sort(reverse=True)
    print(f"LARGE_IMAGES>{500_000}B count={len(imgs)}")
    for sz, rel in imgs[:25]:
        print(f"  {sz / 1024 / 1024:.2f} MB  {rel}")

    inline: list[tuple[int, str]] = []
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="replace")
        n = len(re.findall(r"\sstyle=", t, re.I))
        if n:
            inline.append((n, str(p.relative_to(ROOT)).replace("\\", "/")))
    inline.sort(reverse=True)
    print(f"INLINE_STYLE_PAGES count={len(inline)} total_attrs={sum(n for n,_ in inline)}")
    for n, rel in inline[:15]:
        print(f"  {n:3d}  {rel}")

    refs: dict[str, set[int]] = defaultdict(set)
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"(daab-[a-z0-9-]+\.(?:css|js))\?v=(\d+)", t):
            refs[m.group(1)].add(int(m.group(2)))
    drift = {k: sorted(v) for k, v in refs.items() if len(v) > 1}
    print(f"ASSET_V_DRIFT count={len(drift)}")
    for k, v in sorted(drift.items()):
        print(f"  {k}: {v}")

    # Deployment staleness (sponsorship sample)
    pairs = [
        "az/sponsorship_partnership.html",
        "en/sponsorship_partnership.html",
        "css/daab-sponsors-page.css",
    ]
    print("DEPLOYMENT_STALE")
    for rel in pairs:
        src = ROOT / rel
        dep = ROOT / "Deployment" / rel
        if not dep.exists():
            print(f"  MISSING Deployment/{rel}")
            continue
        if src.read_bytes() != dep.read_bytes():
            print(f"  STALE Deployment/{rel}")

    # Old URL references
    old_url = "forum_2027_sponsorship"
    hits = []
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="replace")
        if old_url in t:
            hits.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    print(f"OLD_URL_forum_2027_sponsorship pages={len(hits)}")
    for h in hits[:10]:
        print(f"  {h}")

    # KSM/CSR in source (not Deployment)
    for term in ("KSM", "CSR"):
        thits = []
        for p in paths:
            t = p.read_text(encoding="utf-8", errors="replace")
            if term in t:
                thits.append(str(p.relative_to(ROOT)).replace("\\", "/"))
        print(f"TERM_{term} in source pages={len(thits)}")

    # Google fonts heavy URLs
    heavy = []
    for p in paths:
        t = p.read_text(encoding="utf-8", errors="replace")
        if "opsz,wght" in t or "Inter:ital" in t:
            heavy.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    print(f"HEAVY_GOOGLE_FONTS pages={len(heavy)}")

    # Uncommitted sponsorship CSS version in HTML
    for rel in ("az/sponsorship_partnership.html", "en/sponsorship_partnership.html"):
        t = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        m = re.search(r"daab-sponsors-page\.css\?v=(\d+)", t)
        if m:
            print(f"SPONSORSHIP_CSS_V {rel} v={m.group(1)}")


if __name__ == "__main__":
    main()
