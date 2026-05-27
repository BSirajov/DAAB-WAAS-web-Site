Here's a practical breakdown by category:

## System Fonts (zero load time, native feel)

The system font stack is the best default for UI-heavy apps where performance matters most:

`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica Neue, sans-serif`

This renders **San Francisco** on Apple devices, **Segoe UI** on Windows, and **Roboto** on Android — each looking perfectly native on its platform.

## Google Fonts — Best for UI / Body Text

These are reliable, well-hinted, and fast from the CDN:

- **Inter** — the de facto standard for dashboards and SaaS apps. Exceptionally legible at small sizes. Designed specifically for screens.
- **DM Sans** — slightly warmer than Inter, great for modern product UIs.
- **Nunito Sans** — friendly and rounded, works well for consumer apps.
- **IBM Plex Sans** — technical, neutral, very good for data-heavy interfaces.
- **Source Sans 3** — Adobe's workhorse, excellent readability across sizes.

## Display / Heading Fonts (pairing with body fonts)

- **Playfair Display** — editorial, authoritative. Pairs beautifully with Inter or DM Sans (as used in DAAB).
- **Fraunces** — optical, characterful. Good for landing pages.
- **Syne** — geometric, modern, strong personality for headers.
- **Outfit** — clean geometric, works as both heading and body.
- **Plus Jakarta Sans** — geometric grotesque, versatile for both roles.

## Variable Fonts (best for performance)

Variable fonts ship a single file covering the entire weight/width range. The best ones:

- **Inter Variable** — all weights in one file, ~200KB
- **Recursive** — also covers monospace in the same variable file, good for dev tools
- **Fraunces** — optical size axis built in

## Mobile-Specific Considerations

- Minimum **16px body size** on mobile — anything smaller triggers iOS zoom on inputs
- **Line height 1.5–1.6** for body, **1.2–1.3** for headings on small screens
- Avoid very thin weights (100–200) on Android — rendering can be poor
- **font-display: swap** is essential to prevent invisible text during load

## Practical Pairing Recommendations

| Use case | Heading | Body |
|---|---|---|
| SaaS / dashboard | Syne or Outfit | Inter |
| Professional / institutional | Playfair Display | Inter or DM Sans |
| Consumer / mobile app | Plus Jakarta Sans | Nunito Sans |
| Developer tool | IBM Plex Mono | IBM Plex Sans |
| Editorial / content-heavy | Fraunces | Source Sans 3 |

## Loading Best Practice

```html
<!-- Preconnect first -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Load only the weights you use -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

Requesting only the weights you actually use (typically 400, 500, 600) can cut font payload by 60–70% versus loading the full family.