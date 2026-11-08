# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **static bilingual website** (Azerbaijani + English) for DAAB / WAAS.
There is no build step required to run it — the HTML/CSS/JS under the repo root and the
`az/` and `en/` trees are served as-is. Tooling is pure Python 3 standard library (no
`requirements.txt`, no `pip` dependencies needed for the core run/lint/test flow).

### Run (dev server)

Start the local preview server (serves the repo root at http://127.0.0.1:8010/ with gzip
+ cache headers):

```bash
python3 helpers/serve_site.py --bind 127.0.0.1 --port 8010
```

- Entry points: `/index.html` (language gateway, auto-redirects to `az/` or `en/`),
  `/az/index.html`, `/en/index.html`.
- A plain `python3 -m http.server 8010 --bind 127.0.0.1` also works (this is what the
  VS Code task "Start DAAB static server" uses); `serve_site.py` additionally adds gzip
  and cache-control headers.

### Lint / test (site validators)

CI (`.github/workflows/validate-site.yml`) runs these three checks; run them the same way
locally from the repo root:

```bash
python3 helpers/_validate_site.py
python3 helpers/_validate_cv_cards.py
python3 helpers/_check_name_order.py
```

- Gotcha: `_validate_site.py` currently exits non-zero because it flags
  `images/activities/Messoud_Efendiyev_Zaqatala_video.mp4` as a missing reference. That
  large video is **intentionally gitignored** (see `.gitignore` — "keep locally + on the
  web host; do not commit"), so this error is expected on any fresh checkout and CI on
  `main` has been red for this reason. It is a content/asset issue, not an environment
  problem. Do not "fix" it by committing the video.

### Maintenance / build helpers

The many `helpers/_build_*.py`, `helpers/_export_*.py`, etc. scripts are one-off content
maintenance tools (some need extra libs like `python-docx`, `Pillow`, `reportlab`, or
Playwright). They are **not** part of the run/lint/test loop and are not required to
develop or preview the site. Install their dependencies ad hoc only if you specifically
need to run one. Optional Playwright-based UI test helpers
(`helpers/_test_page_content_search.py`, `helpers/_test_scientists_multiselect.py`) need
browsers installed first via `npx playwright install chromium`.
