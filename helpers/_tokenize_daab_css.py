#!/usr/bin/env python3
"""Replace repeated brand literals with var(--*) from daab-tokens.css in DAAB CSS modules."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_DIR = ROOT / "css"

# Order: longest / most specific first. Spacing in rgba normalized by regex where noted.
REPLACEMENTS: list[tuple[str, str]] = [
    # Typography stacks
    (
        '"Playfair Display", Georgia, serif',
        "var(--font-serif)",
    ),
    (
        'Inter, system-ui, -apple-system, "Segoe UI", sans-serif',
        "var(--font-sans)",
    ),
    (
        'Inter, system-ui, "Segoe UI", sans-serif',
        "var(--font-sans)",
    ),
    # Shadows
    ("0 18px 50px rgba(0, 45, 82, .22)", "var(--shadow-hero-panel)"),
    ("0 18px 50px rgba(0, 45, 82, 0.22)", "var(--shadow-hero-panel)"),
    # rgba brand / surfaces
    ("rgba(245, 251, 255, .96)", "var(--color-surface-toolbar)"),
    ("rgba(245, 251, 255, 0.96)", "var(--color-surface-toolbar)"),
    ("rgba(255, 255, 255, .92)", "var(--color-panel-card-bg)"),
    ("rgba(255, 255, 255, 0.92)", "var(--color-panel-card-bg)"),
    ("rgba(255, 255, 255, .62)", "var(--color-panel-card-border)"),
    ("rgba(255, 255, 255, 0.62)", "var(--color-panel-card-border)"),
    ("rgba(255, 255, 255, .36)", "var(--color-hero-scrim)"),
    ("rgba(255, 255, 255, 0.36)", "var(--color-hero-scrim)"),
    ("rgba(255, 255, 255, .24)", "var(--color-hero-panel-border)"),
    ("rgba(255, 255, 255, 0.24)", "var(--color-hero-panel-border)"),
    ("rgba(255, 255, 255, .12)", "var(--color-hero-panel-bg)"),
    ("rgba(255, 255, 255, 0.12)", "var(--color-hero-panel-bg)"),
    ("rgba(0, 105, 180, .26)", "var(--line)"),
    ("rgba(0, 105, 180, 0.26)", "var(--line)"),
    ("rgba(0, 105, 180, .24)", "var(--color-border-blue-light)"),
    ("rgba(0, 105, 180, 0.24)", "var(--color-border-blue-light)"),
    ("rgba(0, 105, 180, .22)", "var(--color-border-blue-subtle)"),
    ("rgba(0, 105, 180, 0.22)", "var(--color-border-blue-subtle)"),
    ("rgba(0, 105, 180, .18)", "var(--color-border-blue-faint)"),
    ("rgba(0, 105, 180, 0.18)", "var(--color-border-blue-faint)"),
    ("rgba(0, 105, 180, .14)", "var(--color-border-blue-muted)"),
    ("rgba(0, 105, 180, 0.14)", "var(--color-border-blue-muted)"),
    ("rgba(0, 105, 180, .12)", "var(--color-border-blue-12)"),
    ("rgba(0, 105, 180, 0.12)", "var(--color-border-blue-12)"),
    ("rgba(0, 105, 180, .08)", "var(--color-surface-filter-chip)"),
    ("rgba(0, 105, 180, 0.08)", "var(--color-surface-filter-chip)"),
    ("rgba(0, 105, 180, .16)", "var(--color-border-blue-16)"),
    ("rgba(0, 105, 180, 0.16)", "var(--color-border-blue-16)"),
    ("rgba(0, 105, 180, .10)", "var(--color-border-blue-10)"),
    ("rgba(0, 105, 180, 0.10)", "var(--color-border-blue-10)"),
    ("rgba(0, 105, 180, .1)", "var(--color-border-blue-10)"),
    ("rgba(0, 105, 180, 0.1)", "var(--color-border-blue-10)"),
    # Hex brand palette (lowercase normalized in pass)
    ("#08263b", "var(--ink)"),
    ("#0069b4", "var(--blue-700)"),
    ("#005a9a", "var(--blue-dark)"),
    ("#9ed6f5", "var(--blue-soft)"),
    ("#094d78", "var(--color-heading-blue)"),
    ("#345d76", "var(--muted-hero)"),
    ("#345f86", "var(--muted)"),
    ("#4eb4ee", "var(--blue-400)"),
    ("#117fc8", "var(--blue-600)"),
    ("#06314e", "var(--blue-900)"),
    ("#eef7fc", "var(--soft)"),
    ("#eef8ff", "var(--soft-alt)"),
    ("#dff2ff", "var(--color-tint-blue)"),
    ("#e5f4fb", "var(--color-panel-blue)"),
    ("#f5fbff", "var(--color-surface-news)"),
    # Radii
    ("border-radius: 999px", "border-radius: var(--radius-pill)"),
    ("border-radius:24px", "border-radius: var(--radius)"),
    ("border-radius: 24px", "border-radius: var(--radius)"),
    ("border-radius:18px", "border-radius: var(--radius2)"),
    ("border-radius: 18px", "border-radius: var(--radius2)"),
]

TARGET_GLOBS = [
    "daab-*-page.css",
    "daab-content-hero.css",
    "daab-hub-cards.css",
    "daab-application-embed-*.css",
    "daab-application-membership-value-embed.css",
    "daab-membership-value.css",
    "daab-executive-board.css",
    "daab-nav-mega.css",
    "daab-sidebar-widget.css",
    "daab-forum-content.css",
    "daab-forum-book.css",
    "daab-common.css",
    "scientists-catalog-toolbar.css",
]


def tokenize_text(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
        low = old.lower()
        if low != old and low in text.lower():
            text, n = re.subn(re.escape(old), new, text, flags=re.IGNORECASE)
            count += n
    # #fff only as standalone color (not #ffffff)
    text2, n = re.subn(
        r"(?<![\w#])#fff(?![\da-fA-F])",
        "var(--white)",
        text,
    )
    if n:
        count += n
        text = text2
    # background: #fff -> var(--white) when not in url()
    text2, n = re.subn(
        r"background:\s*#fff\b",
        "background: var(--white)",
        text,
        flags=re.I,
    )
    if n:
        count += n
        text = text2
    return text, count


def main() -> None:
    total = 0
    files_touched: list[str] = []
    for pattern in TARGET_GLOBS:
        for path in sorted(CSS_DIR.glob(pattern)):
            original = path.read_text(encoding="utf-8")
            updated, n = tokenize_text(original)
            if n and updated != original:
                path.write_text(updated, encoding="utf-8")
                files_touched.append(f"{path.name} ({n})")
                total += n
    print(f"Replacements: {total} across {len(files_touched)} files")
    for line in files_touched:
        print(" ", line)


if __name__ == "__main__":
    main()
