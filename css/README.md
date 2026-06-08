# Stylesheets

Shared and page-specific CSS for the DAAB static site.

| File | Purpose |
|------|---------|
| `daab-common.css` | Global design system: layout, navigation, footer, typography, search overlay, shared components. |
| `daab-mobile.css` | Mobile/touch layer: safe areas, scroll lock, sticky offsets, landscape, search overlay on phones. |
| `scientists-catalog-toolbar.css` | Filter toolbar and result count bar on `az/scientists/list.html` and `az/scientists/profiles.html`. |

**HTML reference (pages in site root):**

```html
<link href="css/daab-common.css?v=6" rel="stylesheet"/>
<link href="css/daab-mobile.css?v=1" rel="stylesheet"/>
<link href="css/scientists-catalog-toolbar.css?v=2" rel="stylesheet"/>
```

Image URLs inside `daab-common.css` use `../images/` (relative to this folder).

**Related:** client scripts in `../js/`; maintenance tools in `../helpers/`.
