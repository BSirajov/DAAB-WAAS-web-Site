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

## Phase 4 — CSS consolidation (partial)

**Done:** unified justified forum prose in `daab-forum-content.css`; no `<style>` blocks in deployable AZ/EN HTML.

**Deferred:** activities `.inline-style-*` rename (large, non-blocking).

**Gate:** Spot-check + `_validate_site.py` — pass (May 2026).

---

## Phase 5 — Dead code audit (high effort, subsystem-scoped)

Do **not** delete classes site-wide in one pass.

| Subsystem | Start with | Method |
|-----------|------------|--------|
| Forum | `css/daab-forum-content.css` | Grep class names against `az/forum/`, `en/forum/` HTML |
| Scientists | `css/scientists-*.css`, `js/scientists-*.js` | Run CV validators after any data/CSS change |
| Application | `css/daab-membership-application.css` | Match embed + `application.html` only |

**Gate:** Phase 1 + scientists validators.

---

## Phase 6 — Repo hygiene (optional)

- Keep `_archive/`, `sources/`, `helpers/`, `documents/` out of deploy.
- Remove `_archive` entries only after confirming no external links.
- Do not commit `node_modules/` (Playwright for PDF export).

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
| Broken links | `python helpers/_validate_site.py` |
| Forum CSS pairs | `python helpers/_fix_forum_css_pairs.py` |
| Full audit history | `documents/DAAB-Site-Cleanup-Audit-2026-05.md` |
| User manual regen | `python helpers/_export_user_manual_formats.py` |
