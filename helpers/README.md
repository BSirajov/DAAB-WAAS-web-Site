# DAAB site maintenance helpers

Run all commands from the **repository root**: `python helpers/<script>.py`

## Validate before deploy

| Command | Purpose |
|---------|---------|
| `_validate_site.py` | Broken local `href`/`src` paths |
| `_deploy_preflight.py` | Routes, sitemap, nav/i18n consistency, scientists wiring |
| `_audit_az_en_parity.py` | AZ/EN page pair structure |

## Build / regenerate pages

| Command | Output |
|---------|--------|
| `_build_scientists_profiles.py` | `az/en/scientists/profiles.html` cards from `i18n/scientists-profiles.json` |
| `_build_search_index.py` | `i18n/search-index.json` |
| `_embed_static_nav.py` | Slim nav placeholders → full static nav in HTML |
| `_build_membership_flyer.py` | `az/en/membership_flyer.html` |
| `_build_sponsors_flyer.py` | `az/en/sponsors_flyer.html` |
| `_build_work_done_2024_2026_page.py` | `az/en/work_done_2024_2026.html` |
| `_build_donate_pages.py` | `az/en/donate.html` |
| `_build_video_gallery_page.py` | `az/en/forum/2024/video_gallery.html` |
| `_build_membership_redirect.py` | `az/en/membership.html` legacy redirect stubs |
| `_build_deployment_folder.py --include-images` | `Deployment/` upload package |

## One-shot harmonisation

| Command | Purpose |
|---------|---------|
| `_harmonize_footer_credentials.py` | Footer credential lines + `div.footer-title` → `h4` |
| `_harmonize_forum_breadcrumbs.py` | Forum 2024 crumbs: `I Forum` hub, remove static flag |
| `_inject_site_footer.py` | Canonical footer on application + mission pages |
| `_site_wide_cleanup.py` | Propagate shared asset `?v=` versions |

## Paths

Import repo root via `from _paths import ROOT` in new helpers. Do not add `.py` files at repository root.
