# DAAB design system architecture

This document describes how UI/UX tokens and shared styles are organized on the DAAB static site, what was centralized in the May 2026 pass, and what remains for incremental cleanup.

## Goals

- One source of truth for colors, typography, spacing, radii, shadows, motion, z-index, and sticky chrome.
- Azerbaijani and English pages stay visually identical (same CSS; copy in `i18n/ui.json`).
- JavaScript layout logic (nav compact mode, sidebar stack) reads the same breakpoints as documented CSS.
- Page-specific CSS and inline styles are minimized over time, not removed in one risky sweep.

## Layer model

```
i18n/ui.json              → user-visible strings (nav, breadcrumbs, search, mega-menu labels)
i18n/nav.json             → nav tree structure
i18n/routes.json          → page IDs and locale paths
i18n/design-system.json   → breakpoints, layout numbers, z-index (JS + docs mirror)

css/daab-tokens.css       → :root CSS custom properties (authoritative for paint/layout tokens)
css/daab-common.css       → @import tokens; global reset, nav shell, buttons, footer, search overlay
css/daab-mobile.css       → touch, safe-area, compact nav height override
css/daab-*.css            → feature modules (forum, hub, membership, scientists toolbar, …)

js/daab-design-tokens.js  → DAAB_DESIGN API (matchMedia helpers)
js/daab-i18n.js           → routes + ui.json
js/daab-primary-nav.js    → navIcons from ui.json
js/daab-nav.js            → dropdown / mobile menu (uses DAAB_DESIGN)
```

**Do not** link `daab-tokens.css` directly in HTML. It is pulled in by `daab-common.css`.

## Centralized in this pass

| Concern | Location | Notes |
|--------|----------|--------|
| Brand colors, semantic surfaces/borders | `css/daab-tokens.css` | `--blue-700`, `--soft`, `--color-surface-toolbar`, etc. |
| Typography stacks | `--font-sans`, `--font-serif` | Used in `daab-common.css` |
| Spacing scale | `--space-1` … `--space-8`, `--shell-padding-x` | Shell padding wired in common |
| Radii | `--radius`, `--radius2`, `--radius-pill` | Buttons use `--radius-pill` |
| Shadows | `--shadow`, `--shadow-btn-primary`, `--shadow-focus` | Buttons and focus rings |
| Motion | `--transition-fast`, `--transition-btn` | Toolbar + buttons |
| Z-index | `--z-nav`, `--z-search-overlay`, `--z-breadcrumbs` | Nav strip uses `--z-nav` |
| Sticky stack | `--daab-nav-height`, `--daab-sticky-top-stack` | Mobile height override in `daab-mobile.css` |
| Safe area / touch | `--daab-safe-*`, `--daab-touch-min` | Moved out of duplicate `:root` in mobile |
| Breakpoints (JS) | `i18n/design-system.json` | `navCompact: 1180`, `sidebarStack: 1060` |
| Nav compact MQ | `js/daab-nav.js`, `js/daab-shell.js` | `DAAB_DESIGN.navCompactMq()` |
| Sidebar stack MQ | `js/daab-sidebar-timeline.js` | `DAAB_DESIGN.sidebarStackMq()` |
| Scientists toolbar | `css/scientists-catalog-toolbar.css` | Top toolbar/filter chip tokens |
| Shared buttons (partial) | `css/daab-common.css` | `.btn`, focus ring, search overlay |

Cache bust: `daab-common.css?v=28` (imports tokens), `daab-*-page.css?v=2`, `daab-hub-cards.css?v=12`, `daab-membership-value.css?v=3`. Re-run `python helpers/_tokenize_daab_css.py` after adding literals to page CSS.

**Token pass (May 2026):** 380+ brand literals in page/modules replaced with `var(--*)` via `helpers/_tokenize_daab_css.py`; extended `daab-tokens.css` with heading, panel, and border semantic tokens.

**Follow-up (May 2026):** `daab-content-hero.css` consolidates foundation/mission/membership heroes; tokenized `daab-common.css`, forum CSS, scientists toolbar; AZ nav copy fixes in `i18n/ui.json` (`Forum 2024 haqqında`, `Niyə üzv olmalısınız`).

## UI text and icons (already centralized)

- **Navigation labels, breadcrumbs, section nav, search UI:** `i18n/ui.json` (`nav`, `breadcrumbs`, `sectionNav`, `search`, …).
- **Nav icon SVG paths:** `i18n/ui.json` → `navIcons` (consumed by `js/daab-primary-nav.js`).
- **Do not** duplicate strings in `design-system.json`.

## Pages / areas still using local hardcoding

### Inline `<style>` blocks

Run `python helpers/_audit_design_hardcoding.py` — as of the May 2026 cleanup, **no `<style>` blocks remain** under `az/` or `en/`.

| Page(s) | Stylesheet |
|---------|------------|
| Hub home + forum index | `daab-hub-cards.css` |
| `charter.html` | `daab-charter-page.css` |
| `foundation.html` | `daab-foundation-page.css` |
| `mission.html` | `daab-mission-page.css` |
| `membership.html` | `daab-membership-page.css` |
| `activities.html` | `daab-activities-page.css` + `daab-activities-layout.css` |
| `scientists/list.html` | `daab-scientists-list-page.css` |
| `scientists/profiles.html` | `daab-scientists-profiles-page.css` |
| `application.html` | `daab-membership-application.css` |
| `membership_value.html` | `daab-membership-page.css` |

Extracted via `helpers/_migrate_inline_styles.py` (re-run only when adding new inline blocks to migrate).

### Page-specific CSS files with literal hex / rgba

These modules are intentional for now but should prefer `var(--*)` when touched:

- `daab-*-page.css` — per-page rules extracted from former inline blocks; prefer `var(--*)` when editing
- `daab-forum-content.css`, `daab-forum-book.css` — long-form forum typography palette
- `daab-hub-cards.css` — hero gradients and card accents
- `daab-membership-application.css`, `daab-membership-value.css`
- `daab-executive-board.css`, `daab-nav-mega.css`, `daab-search.css`
- `scientists-catalog-toolbar.css`

### CSS `@media` breakpoints

`@media (max-width: 1180px)` and `1060px` remain literal in CSS files (CSS variables are not reliable in media queries in all target browsers). **Single numeric source:** `i18n/design-system.json`; keep CSS comments in sync when changing breakpoints.

## Long-term structure (recommended)

```
css/
  daab-tokens.css          # tokens only
  daab-components.css      # optional: .btn, .card, .panel, .breadcrumb-bar (extract from common)
  daab-common.css          # layout shell + imports
  daab-layout.css          # optional: .shell, .main, grid utilities
  daab-<feature>.css       # forum, membership, scientists, …

i18n/
  design-system.json       # machine-readable non-copy tokens
  ui.json                  # all human-readable UI strings + navIcons

helpers/
  _build_<page>.py         # regenerate HTML from sources; no inline styles in output
  _audit_design_hardcoding.py
```

**Rules for new work**

1. Add tokens to `daab-tokens.css` first; alias legacy names if needed.
2. Use `var(--token)` in feature CSS; avoid new raw `#0069b4` unless defining a token.
3. Add breakpoints/layout numbers to `design-system.json` and use `DAAB_DESIGN` in JS.
4. Put AZ/EN copy only in `i18n/ui.json`.
5. Bump `?v=` on `daab-common.css` (or affected JS) after shared asset changes.
6. Run `python helpers/_validate_site.py` before commit.

## Visual identity

No brand colors or layout proportions were intentionally changed. Tokens preserve previous values (`#0069b4`, `#08263b`, `1220px` max width, `86px` / `72px` nav height, `24px` card radius). AZ and EN pages share the same stylesheets; only text direction and `ui.json` strings differ.

## Verification

```bash
python helpers/_validate_site.py
python helpers/_audit_design_hardcoding.py
```

Preview: `START-SITE.bat` or `python -m http.server 8010 --bind 127.0.0.1`, then check AZ and EN home, membership, scientists list, and one forum page. Hard-refresh after CSS/JS bumps.
