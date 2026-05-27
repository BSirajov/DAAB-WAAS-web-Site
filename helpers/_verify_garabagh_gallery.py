#!/usr/bin/env python3
"""Verify Garabagh gallery copies."""
from __future__ import annotations

import json
from pathlib import Path

from _paths import ROOT

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Install: pip install Pillow")

LOCAL = Path(
    r"C:\Users\BSira\Documents\Azərbaycanlı Alimlərin Istanbul görüşü, 8-10 Dekabr 2022"
    r"\1-ci Bakı forumu, 8-12 Sentyabr 2024\Forumdan foto və videolar\Fotolar"
)
OUT = ROOT / "images" / "photos-gallery" / "Garabagh"
MANIFEST = OUT / "_match-manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sources = [e["source"] for e in manifest if e.get("matched")]
    print(f"Matched: {len(sources)}/{len(manifest)}")
    print(f"Unique sources: {len(set(sources))} (dupes: {len(sources) - len(set(sources))})")
    print(f"Dest files: {len(list(OUT.glob('garabagh-*.jpg')))}")
    dists = [e["distance"] for e in manifest if e.get("matched")]
    print(f"dHash distance: min={min(dists)} max={max(dists)} avg={sum(dists)/len(dists):.1f}")

    for e in manifest:
        if not e.get("matched"):
            continue
        src = LOCAL / e["source"]
        dst = OUT / e["dest"]
        si = Image.open(src)
        di = Image.open(dst)
        if si.size != di.size:
            raise SystemExit(f"Size mismatch {e['dest']}: {si.size} vs {di.size}")
        if dst.stat().st_size != src.stat().st_size:
            raise SystemExit(f"Bytes mismatch {e['dest']}")

    expected = [f"garabagh-{i:02d}.jpg" for i in range(1, len(manifest) + 1)]
    actual = sorted(p.name for p in OUT.glob("garabagh-*.jpg"))
    if actual != expected:
        raise SystemExit(f"Naming gap: expected {len(expected)}, got {actual[:3]}…{actual[-3:]}")

    print("OK: resolution, bytes, sequential naming")


if __name__ == "__main__":
    main()
