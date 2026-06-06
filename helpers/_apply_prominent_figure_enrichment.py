#!/usr/bin/env python3
"""Apply researched enrichment to AZ prominent-figure profile sections."""
from __future__ import annotations

import sys

from _paths import ROOT
from _prominent_figure_enrichment import (
    apply_enrichment,
    derive_enrichment,
    merge_enrichment,
    needs_enrichment,
)

try:
    from _prominent_figure_enrichment_overrides import OVERRIDES
except ImportError:
    OVERRIDES = {}

FIGURES = ROOT / "az" / "prominent_figures"
SKIP = {"hazirlanir.html"}


def main() -> int:
    dry = "--dry-run" in sys.argv
    updated = 0
    skipped = 0
    missing = []

    for group in ("azturk", "world"):
        for path in sorted((FIGURES / group).glob("*.html")):
            if path.name in SKIP:
                continue
            slug = path.stem
            text = path.read_text(encoding="utf-8")
            if not needs_enrichment(text):
                skipped += 1
                continue

            derived = derive_enrichment(text, group)
            override = OVERRIDES.get(slug)
            enrichment = merge_enrichment(derived, override)
            if not enrichment:
                missing.append(slug)
                continue

            new_text, changed = apply_enrichment(text, enrichment)
            if changed:
                updated += 1
                if not dry:
                    path.write_text(new_text, encoding="utf-8", newline="\n")
            else:
                missing.append(slug)

    print(f"Updated {updated} profiles (dry_run={dry})")
    print(f"Skipped (already enriched): {skipped}")
    if missing:
        print(f"Missing enrichment for {len(missing)} profiles:")
        for s in missing[:20]:
            print(f"  - {s}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
