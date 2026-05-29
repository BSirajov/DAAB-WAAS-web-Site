# DAAB site — recommended work order (May 2026)

This is the **agent-chosen sequence** after the scoped cleanup pass. Work top to bottom; do not skip validation between phases.

---

## Phase 0 — Baseline (repeat before/after each phase)

```bash
python helpers/_validate_site.py
python helpers/_validate_cv_cards.py
python helpers/_check_name_order.py
```

**Status (May 2026):** All three pass (0 broken paths, 83 CV cards in sync, 0 name-order mismatches).

---

## Phase 1 — Manual smoke test (~30 min)

**Status:** Done (May 2026 — site owner confirmed “looks good”).

---

## Phase 2 — Copy and nav polish (low risk)

**Status:** Done (May 2026).

| Task | Status |
|------|--------|
| EN membership CTA → “Join us” | Done |
| AZ membership CTA → “Bizə qoşulun” | Done |
| Forum section pills + hub card icons | Done (`navIcons` + `daab-section-nav.js`) |
| Search index | Re-run only when routes/titles change |

---

## Phase 3 — Maintenance script alignment

**Status:** Done — `_site_wide_cleanup.py` matches live `?v=` (e.g. `daab-common.css` v35, `daab-section-nav.js` v10).

**Gate:** Diff review only — run `_site_wide_cleanup.py` only when intentionally bumping versions site-wide.

---

## Phase 4 — CSS consolidation

**Status:** Done (May 2026).

| Task | Status |
|------|--------|
| Forum justified prose in `daab-forum-content.css` | Done |
| No `<style>` blocks in deployable AZ/EN HTML | Done |
| Activities `.inline-style-*` → semantic `act-*` classes | Done (`helpers/_rename_activities_inline_styles.py`) |
| Forum `daab-activities-layout.css` `?v=13` harmonized | Done (`_site_wide_cleanup.py`) |
| Duplicate sidebar timeline inline JS | Removed from 9 pages; uses `daab-sidebar-timeline.js` |

**Gate:** Spot-check activities + one forum page; `_validate_site.py` — pass.

---

## Phase 5 — Dead code audit

**Status:** Done (May 2026).

Do **not** delete classes site-wide in one pass. `daab-forum-content.css` is clean (all classes used or JS-toggled). Build-only sheets marked in `css/` headers.

| Subsystem | Result |
|-----------|--------|
| Forum | `daab-forum-content.css` — all classes used on live forum pages |
| Build-only CSS | `daab-forum-book.css`, `daab-application-embed-*.css` — BUILD-ONLY headers; omitted via `.deployignore` |
| Scientists profiles | Removed legacy `.card-org`, `.hero-actions`, `.awards-label`; Eldar photo crop via `#eldar-ehedov`; kept `.card-email--empty` for TTS |
| Scientists toolbar | `.org` / `.w3` are false positives (URL fragments in `data:image` CSS) |
| Application | Removed unused hero `.eyebrow`, `.dot`, `.hero-text`, `.hero-actions` from `daab-membership-application.css` |

**Gate:** `python helpers/_deploy_preflight.py` — pass.

---

## Phase 6 — Repo hygiene

**Status:** Done (May 2026).

- `_archive/`, `sources/`, `helpers/`, `documents/` excluded from deploy (`.deployignore`).
- `node_modules/` added to `.gitignore` (Playwright for PDF export).
- `_archive` prune deferred — no live site links found in routine checks; remove only after external-link audit.

---

## Phase 7 — Pre-release — **NEXT (manual)**

Automated gate: see `documents/DAAB-Pre-Release-Status-2026-05.md`.

- Keyboard-only: nav dropdown, section pills, application steps, gallery lightbox if present.
- Tablet width 768–1024px on forum + scientists profiles.
- Git commit when you want a snapshot.

---

## Quick reference

| Need | Command / doc |
|------|----------------|
| Pre-deploy (all checks) | `python helpers/_deploy_preflight.py` |
| Broken links | `python helpers/_validate_site.py` |
| Forum CSS pairs | `python helpers/_fix_forum_css_pairs.py` |
| Full audit history | `documents/DAAB-Site-Cleanup-Audit-2026-05.md` |
| User manual regen | `python helpers/_export_user_manual_formats.py` |
