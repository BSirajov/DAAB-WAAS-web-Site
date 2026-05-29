# DAAB site — pre-release status (May 2026)

## Automated checks (pass)

| Check | Result |
|-------|--------|
| `python helpers/_validate_site.py` | OK — 47 pages, 3626 references |
| `python helpers/_validate_cv_cards.py` | OK — 83 cards, 0 issues |
| `python helpers/_check_name_order.py` | OK — 0 mismatches |
| Deploy pages on `daab-common.css?v=35` | OK (only `sources/` reference is non-deploy) |

## Completed since cleanup audit

- Site-wide diaspora background (`daab-site-background.css`)
- Forum card headers, roadmap sidebar/card icons, justified long-form forum prose
- Forum section-nav pill icons (`navIcons`)
- EN/AZ membership CTA alignment (“Join us” / “Bizə qoşulun”)
- Stories, presentations, official, impressions, cooperation, roadmap text justify (shared rule in `daab-forum-content.css`)

## Manual QA still recommended (Phase 7)

- [ ] Keyboard: nav dropdown, section pills, search (Ctrl/Cmd+K), application form steps
- [ ] Tablet width (~768–1024px): forum sidebar + scientists profile sticky panel
- [ ] Hard-refresh after deploy (`Ctrl+F5`) so `?v=` caches clear

## Deferred (not blocking deploy)

- Full unused CSS/JS audit (Phase 5 — use `helpers/_audit_css_usage.py`)
- `_archive/` / `sources/` pruning

## Deploy bundle

Ship: `index.html`, `az/`, `en/`, `css/`, `js/`, `images/`, `i18n/`, `forum_2024/` (PDF if linked).  
Omit: `helpers/`, `documents/`, `_archive/`, `sources/`, `node_modules/`.

## When ready

Create a git commit locally; push when satisfied with manual QA.
