# DAAB–WAAS deep QA report

**Date:** 2026-10-21  
**Scope:** Static analysis of source (`az/`, `en/`) + spot-check `Deployment/`. Browser/runtime UI not fully exercised in this pass.  
**Method:** Followed `helpers/QA_DEEP_PROMPT.md`.

## Summary

**Ship-ready on M1–M3.** Locale twin coverage and critical assets look solid; home poster/CTA wiring and scientists photo pipeline check out. Forum dates aligned to **9–10 December**, registration is **Cognito-only** (`register.html` redirects), DIDK on register matches complex-topics. Rebuild `Deployment/` still recommended so stamps match recent home/CSS work.

## Blockers

*(none found in static scope)*

## Majors

### M1 — Forum dates conflict (home alt vs Forum 2026 hub) — **FIXED**

- Home poster `alt` now **9–10** December/dekabr 2026 (EN/AZ + Deployment), matching Forum hub.

### M2 — Dual Forum 2026 registration paths — **FIXED**

- Product path is **Cognito Forms**. `en|az/forum/2026/register.html` (and Deployment) are Cognito bridges (`meta refresh` + `location.replace` + CTA). Legacy `mail.php` form removed from register pages. Hub participant pill already Cognito.

### M3 — Forum register DIDK logo inconsistent with complex-topics — **FIXED**

- Register sponsors now use `images/didk-logo.jpg` (same as complex-topics).

## Minors

### m1 — EN vs AZ ANAS caption layout on complex-topics

- AZ uses two `forum-register-sponsors__line` spans; EN is single-line.
- **Fix hint:** Optional EN two-line split for visual parity.

### m2 — Home CTA is one hop from Cognito

- Pill links to `forum/2026/index.html` (intentional in HTML); registration needs a second click.
- **Fix hint:** Only change if product wants direct Cognito from home.

### m3 — Deployment HTML size drift without full rebuild stamp refresh

- Spot-checked HTML: same mtime family but Deployment files ~340–485 bytes larger (typical stamp/path diffs). Footer still `Build 20261016 - 0703` while home/CSS were edited 2026-10-21.
- **Fix hint:** Run `python helpers/_build_deployment_folder.py` with UTF-8 env before ship.

### m4 — `images/Archive/` posters are 1536×1024 while live posters are 1536×978

- Live files had bottom cropped (~46px) for QR gap; Archive is older full-height backup.
- **Fix hint:** Refresh Archive after intentional poster edits, or document Archive as pre-crop backup.

## Nits

### n1 — Home still loads page-content-search CSS/JS though `home` is in `SKIP_PAGE_IDS`

- `js/daab-page-content-search.js` correctly skips mount; assets still linked from `index.html`.
- **Fix hint:** Optional remove of those tags on home only.

### n2 — Unused PLACEHOLDERS.home strings remain in page-content-search.js

### n3 — Source vs Deployment `?v=` inconsistency on some assets

- e.g. complex-topics DIDK: source often unversioned; Deployment uses `?v=20261016-0703`.

## Locale parity gaps

| Area | Status |
|------|--------|
| Top-level HTML basenames (24↔24) | **Parity OK** — no missing twins |
| Home poster EN/AZ files | **OK** — `_EN.png` / `_AZ.png` |
| Complex-topics DIDK | **OK** both locales |
| Complex-topics ANAS caption lines | **AZ two-line / EN one-line** |
| Forum 2026 Cognito CTA | **OK** both locales |
| Forum register DIDK asset | **OK** — `didk-logo.jpg` both locales |

## Deployment drift

| Asset | Sync |
|-------|------|
| `css/daab-hub-cards.css` | Match size/mtime |
| `js/daab-page-content-search.js` | Match |
| Home / complex-topics / forum HTML | Present; size diffs likely stamps |
| Footer build stamp | `20261016 - 0703` (stale vs recent home work) |
| Cognito participant pill lock in `_build_deployment_folder.py` | **Present** |

**Recommendation:** Full Deployment rebuild before production cut.

## Checks passed (highlights)

- Critical assets present (DIDK, posters, sponsors, Bakhtiyar photo + thumb).
- Home: Support us hidden (`hidden` + CSS); CTA pill + copy; posters wired; `home` in `SKIP_PAGE_IDS`; no `#cardSearch`; poster CSS rounded, no aspect-ratio squeeze.
- Scientists: profiles loader + chunks; 15/15 sampled photos + thumbs exist; 102/102 full/thumb folder counts match.
- Relative href scan (cache-bust stripped): no missing same-tree targets in sample methodology used by explorer.
- `mail.php` files exist where referenced (not a missing-file bug; product path question is M2).

## Test matrix covered

| Area | AZ | EN | Mobile | Notes |
|------|----|----|--------|-------|
| Top-level HTML inventory | ✓ | ✓ | — | Static |
| Home hero/poster/CTA | ✓ | ✓ | — | Static + CSS |
| Forum 2026 index/register | ✓ | ✓ | — | Static |
| Complex-topics partners | ✓ | ✓ | — | Static |
| Scientists list/profiles/photos | ✓* | ✓ | — | *parity assumed via shared i18n |
| Deployment spot-check | ✓ | ✓ | — | Partial |
| Live browser / a11y keyboard | — | — | — | **Not run** this pass |
| Full nav click-through | — | — | — | **Not run** |

## Open questions for product

1. ~~Is the official Forum date **9–10** or **8–10** December 2026?~~ → **9–10** (confirmed).
2. ~~Should public nav expose only Cognito, or keep legacy `register.html`?~~ → **Cognito**; `register.html` redirects.
3. ~~Should Forum register sponsors match complex-topics (`didk-logo`) immediately?~~ → **Yes** (done).
4. Should the home pill deep-link to Cognito or stay on the Forum hub?

## Agents used

- [QA locale inventory parity](c3277441-1c94-40db-9812-a250f8743ee7)
- [QA home forum complex-topics](c0f24b0c-43a7-489d-839e-63ae2fa5ed62)
- [QA scientists broken links](dcb45b26-22c0-4b31-8e82-ef62d2219f2c)
