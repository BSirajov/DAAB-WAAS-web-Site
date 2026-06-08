# Scientist profile filtering — UX/UI proposal (DAAB CV catalogue)

**Project:** DAAB-WAAS website  
**Page:** `az/scientists/profiles.html` (aligned with `az/scientists/list.html`)  
**Date:** May 2026  
**Status:** Proposal — not yet implemented (Phase B/C optional)

This document defines how filtering should behave on the CV catalogue page, using the existing DAAB design language: institutional blue (`--blue-700`), soft panels (`rgba(245, 251, 255, .96)`), rounded toolbar (`var(--radius)`), gold accent dots on active selects, and card styling (white panels, light borders, subtle elevation).

---

## 1. Design principles

| Principle | Application |
|-----------|-------------|
| **Clarity over cleverness** | Users are browsing 83 long-form CV cards, not a social feed. The goal is to narrow the set quickly without damaging trust in the content. |
| **Preserve card integrity** | Matching cards always show the full profile (photo, title, İxtisas, E-poçt, bio). Never squash, truncate, or grey out full cards in place. |
| **Instant feedback** | Filter changes should feel immediate; motion supports understanding, not decoration. |
| **AND logic, predictable** | All active filters combine with **AND** (narrowing), same as today — familiar for catalogue/search UIs. |
| **Respect `prefers-reduced-motion`** | Animations are subtle and optional; core behavior works with `display` toggling only. |

---

## 2. Recommended approach (executive summary)

**Use “hide non-matches + smooth grid reflow”** — the pattern already used with `.is-filtered-out { display: none }`, refined with light transitions and stronger filter feedback.

**Do not use:** in-place faded cards, collapsed “stubs,” or draggable reordering of hidden items. Those approaches were tried in this project and felt broken or unprofessional for long CV content.

### Filter flow (conceptual)

```
User inputs: Search, Ölkə, İxtisas, Elmi dərəcə
        ↓
Filter logic (AND): all criteria must match
        ↓
    ┌───┴───┐
    │       │
  Match   No match
    │       │
Visible   Hidden (removed from layout)
full card
```

---

## 3. Matching vs non-matching cards

### Matching cards (visible)

- **State:** Default card appearance — no “selected” border unless optional subtle emphasis is added (see §8).
- **Content:** Unchanged: avatar, name, country, title, meta rows, full bio.
- **Layout:** Participate normally in the CSS grid (1 column mobile, 2 columns ≥960px).
- **Height:** Row pairs can share height via `align-items: stretch` on the grid; cards grow with bio length (no forced equal bio height).

### Non-matching cards (hidden)

- **State:** Removed from layout flow — `display: none` via class `.is-filtered-out`.
- **DOM:** Cards may remain in the DOM but hidden for simplicity and recovery; no visual ghosting.

**Why not fade/collapse in place?**

- **Fade (opacity):** Leaves empty gaps or odd partial rows; 83 tall cards make the page feel broken.
- **Collapse to strip:** Previously felt like profiles were “destroyed” and broke flex/grid layout.
- **Move to bottom:** Adds cognitive load (“where did everyone go?”) and hurts scanability on an institutional site.

---

## 4. Transitions and animation

### Goal

Communicate “the catalogue narrowed” without layout glitches (vertical strips, jumping avatars).

### Recommended motion stack

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Card exit | Opacity `1 → 0` + slight `scale(0.98)` | 180–220ms | `ease-out` |
| Card enter | Opacity `0 → 1` + `scale(0.98 → 1)` | 220–280ms | `ease-out` |
| Grid reflow | Stable `gap`; browser grid reflow after `display` change, or FLIP technique | 250–350ms | `cubic-bezier(0.2, 0.8, 0.2, 1)` |
| Toolbar / count | Count cross-fade or short slide | 150ms | `ease` |

### Implementation phases

1. **Phase 1 (minimal, robust):** Only animate **result count** and **no-results panel**; cards snap in/out via `display: none`. Lowest risk, still modern if count + chips update smoothly.
2. **Phase 2 (polished):** Before hiding, add `.is-leaving` (opacity/scale), then apply `.is-filtered-out`. On show, reverse with `.is-entering`.
3. **`prefers-reduced-motion: reduce`:** Skip scale/opacity; instant `display` toggle only.

### What to avoid

- Animating `height`, `max-height`, or `flex-basis` on cards (causes reflow bugs with long bios).
- Staggered cascade across 83 cards (feels slow on mobile).
- Blur filters on non-matches (GPU cost + readability issues).

---

## 5. Dynamic grid / layout reorganization

### Desktop (≥960px)

- **Grid:** `repeat(2, minmax(0, 1fr))`, `gap: 20px`, `align-items: stretch`.
- **On filter:** Hidden cards leave the flow; remaining cards **reflow in DOM order** (catalogue order unless relevance sorting is added later).
- **Single result:** One card in one column cell — same width as a normal grid cell, not a full-bleed hero unless explicitly designed.

### Tablet (760–959px)

- Single column; same hide/show behavior; reduced padding per existing breakpoints.

### Mobile (&lt;640px)

- Stacked card (avatar centered above body); 1-column grid.
- **Sticky toolbar** under nav; filter row wraps; `scroll-margin-top` on `.catalog-section` prevents overlap with first card.

### Layout stability rules (critical)

- Avatar: fixed `min-width` / `flex: 0 0` (prevents “vertical strip” regression).
- Cards: `height: 100%` only inside stretch grid rows, not fixed pixel heights.
- Avoid `auto-fill` with tiny minimum track sizes; use explicit 1/2 column breakpoints.

---

## 6. Multiple filters — interaction model

### Logic (recommended — current behavior)

```
visible = search_match AND country_match AND ixtisas_match AND degree_match
```

- Empty filter = “any” for that dimension.
- Search: substring match on normalized `data-search` (name, title, email, ixtisas, country, degree).

### UI feedback for combined filters

1. **Active filter chips** (below toolbar or above grid), e.g. `ABŞ ×` `Fizika ×` `Ph.D. ×` `berkeley ×` — chip remove clears that control; style like DAAB pills (`.cred`).
2. **Per-control “active” state** — `.sel-wrap.active` with gold dot (already implemented).
3. **“Hamısını sıfırla”** — visible when any filter is active; primary escape hatch.

### Search + dropdown coordination

- Typing in search does **not** auto-clear dropdowns (AND stays intuitive).
- Changing country may smooth-scroll to first visible card in that country (desktop); on mobile prefer `block: 'nearest'` or disable auto-scroll when it fights the keyboard/toolbar.

### Future enhancement (optional)

- Disable dropdown options when count would be 0 (faceted search). Higher effort; only if users report confusion.

---

## 7. Desktop vs mobile behavior

| Aspect | Desktop | Mobile |
|--------|---------|--------|
| **Toolbar** | Sticky under nav; search + 3 selects + clear | Sticky; filters stack; search full width first |
| **Filter application** | Immediate on `input` / `change` | Same; optional 150ms debounce on search |
| **Card hiding** | `display: none` + grid reflow | Same |
| **Scroll** | Optional scroll-to-first on country change | Avoid forced scroll on every keystroke |
| **Result count** | `12 uyğun profil (83 ümumi)` | Same copy; slightly smaller type |
| **Touch targets** | min 44px | Maintain; chip dismiss ≥44px |

---

## 8. Result feedback (while filtering)

### Result count

- **No filters:** `83 profil`
- **With filters:** `12 uyğun profil` with secondary `(83 ümumi)` in muted text.

### Optional subtle match emphasis (Phase 2)

- Light border or background tint on matching cards only: e.g. `border-color: rgba(0, 105, 180, .28)`.
- Do **not** dim non-matches in place.

### Loading state

- Not required for 83 client-side cards; optional 100ms opacity pulse on count if search is debounced.

---

## 9. Empty / no-results state

When `visible === 0`:

### Placement

- Show **in place of the grid** (inside `.catalog-section`), not below a long list of hidden cards.

### Content (Azerbaijani)

**Heading:** Heç bir profil tapılmadı  

**Body:** Seçilmiş filtrlərə uyğun nəticə yoxdur. Filtrləri dəyişin və ya sıfırlayın.

**Actions:**

- Primary: **Hamısını sıfırla**
- Secondary (optional): **Yalnız axtarışı sil** — when search is the only active filter

### Visual design (DAAB-consistent)

- Centered panel: `#f5fbff` / white background, `border: 1px solid rgba(0, 105, 180, .14)`, `border-radius: var(--radius)`, soft shadow like cards.
- Simple outline icon (search/filter), `--blue-700`.
- Animate: fade + 8px upward slide, 200ms; respect `prefers-reduced-motion`.

### Accessibility

- `aria-live="polite"` on result region when count hits 0.
- Optional: move focus to empty-state heading when zero results after filter apply (not on every keystroke).

---

## 10. Comparison of approaches

| Approach | Pros | Cons | Fit for DAAB CV |
|----------|------|------|-----------------|
| **Hide non-matches (recommended)** | Clean grid, full cards, fast, accessible | Cards not visible for cross-filter comparison | **Best** |
| Fade non-matches in place | Shows what was filtered | Gaps, clutter with 83 long cards | Poor |
| Collapse to mini rows | Compact | Felt broken; not institutional | **Reject** |
| Move non-matches to bottom | Still in DOM | Long scroll of irrelevant content | Poor |
| Paginate filtered set | Less DOM work | Extra control; CV is scroll catalogue | Optional later |
| Server-side filter | Scales huge catalogues | Overkill for 83 static cards | Not needed now |

---

## 11. Alignment with az/scientists/list.html (list page)

Keep a **consistent mental model** between list and profile views:

| az/scientists/list.html (table) | az/scientists/profiles.html (cards) |
|------------------------|---------------------------|
| Rows removed from table | Cards removed from grid |
| Same AND filters | Same AND filters |
| Same toolbar styling | Same toolbar styling |
| Pagination on list | Full scroll on CV (acceptable difference) |

Users switching between **Siyahı** and **Profil** should not learn two different filter philosophies.

---

## 12. Accessibility checklist

- Filter controls: `aria-label` / associated labels on search and selects.
- Result count: `aria-live="polite"` when count changes.
- No-results: announced when shown.
- Focus visible on selects, clear buttons, chips (`:focus-visible` ring matching toolbar).
- `prefers-reduced-motion`: disable card scale/opacity transitions.
- Active filters: not conveyed by color alone — use chips, gold dot, and border state.

---

## 13. Implementation phases

### Phase A — Baseline (current + polish)

- Non-matches: `.is-filtered-out` with `display: none`
- Result count + empty state panel
- Active select styling + “Hamısını sıfırla”
- Stable card/grid CSS (avatar min-width, 1/2 column grid)

**Related files:** `az/scientists/profiles.html`, `js/scientists-cv-filters.js`, `css/scientists-catalog-toolbar.css`

### Phase B — UX polish

- Active filter chips + per-chip dismiss
- Empty state centered in catalogue area with CTA
- `aria-live` on results
- Debounced search on mobile (150ms)

### Phase C — Motion (optional)

- Card enter/leave opacity + scale (with reduced-motion fallback)
- FLIP or CSS transition on grid reflow
- Animated count transition

---

## 14. Final recommendation

For a **professional institutional** DAAB site, the cleanest experience is:

1. **Hide** non-matching cards completely.
2. **Reflow** the grid so visible cards form a tight 1- or 2-column catalogue.
3. **Never deform** hidden or visible card content.
4. **Combine filters with AND**, surfaced through chips + count + active select states.
5. **Use a dedicated, well-designed empty state** when nothing matches.
6. **Keep motion subtle** (count + empty state + optional card fade), with a reduced-motion path.

This matches modern catalogue UX on government, university, and research association sites, avoids layout failures from collapse/dim modes, and stays visually consistent with the existing DAAB toolbar and card system.

---

## Appendix: Current implementation snapshot

| Item | Current behavior |
|------|------------------|
| Filter logic | AND across search, country, ixtisas, degree |
| Non-matches | `.is-filtered-out` → `display: none !important` |
| Result text | `N uyğun profil (83 ümumi)` when filtering |
| Empty state | `#no-results` toggles `.visible` |
| Country change | Smooth scroll to first visible card in country |
| Clear all | `#clearFilters` resets inputs and shows all cards |

---

*Document prepared for DAAB-WAAS web site maintainers. Implementation should follow Phase A before B/C unless product owner approves otherwise.*
