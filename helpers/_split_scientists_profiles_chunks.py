#!/usr/bin/env python3
"""Split i18n/scientists-profiles.json into parallel-loadable chunks."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _paths import ROOT

SOURCE = ROOT / "i18n" / "scientists-profiles.json"
CHUNK_DIR = ROOT / "i18n" / "scientists-profiles"
MANIFEST = CHUNK_DIR / "manifest.json"
DEFAULT_CHUNK_SIZE = 21


def split_profiles(*, chunk_size: int = DEFAULT_CHUNK_SIZE) -> dict:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    profiles = list(data.get("profiles") or [])
    profiles.sort(key=lambda p: int(p.get("say") or 0))
    version = data.get("version", 1)

    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old in CHUNK_DIR.glob("chunk-*.json"):
        old.unlink()

    chunk_names: list[str] = []
    for index in range(0, len(profiles), chunk_size):
        chunk_profiles = profiles[index : index + chunk_size]
        name = f"chunk-{index // chunk_size + 1:02d}.json"
        (CHUNK_DIR / name).write_text(
            json.dumps({"profiles": chunk_profiles}, ensure_ascii=False, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )
        chunk_names.append(name)

    manifest = {
        "version": version,
        "profile_count": len(profiles),
        "chunk_size": chunk_size,
        "chunks": chunk_names,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    args = parser.parse_args()
    manifest = split_profiles(chunk_size=max(1, args.chunk_size))
    print(
        f"Wrote {manifest['profile_count']} profiles in {len(manifest['chunks'])} chunk(s) "
        f"under {CHUNK_DIR.relative_to(ROOT).as_posix()}/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
