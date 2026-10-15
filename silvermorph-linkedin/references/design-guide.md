# Silvermorph LinkedIn: poster design guide (v2)

Renderer: `python3 scripts/render_poster.py --list` shows the 10 layouts and their slots. Output: 1200 x 1200 PNG (1:1, locked as default by the owner; a 4:5 variant is optional later). Filename: `silvermorph-<category>-<slug>.png`.

## Brand tokens (v3, owner-set 2026-10-14 from the SenseAI x Silvermorph partnership image)
Cool, clean, tech-forward. Values sampled from the reference image.

| Token | Hex | Use |
|---|---|---|
| White | `#FFFFFF` | default background |
| Pale cyan | `#F6FCFC` | secondary background, cards |
| Tint | `#EAF8FB` | tinted background, soft curves |
| Navy (headings, light bg) | `#0C305A` | headings, body emphasis |
| Deep navy (dark bg) | `#06244E` | inverted backgrounds, corner stripe |
| Teal deep | `#0096A8` | accent lines, key phrases on light |
| Teal bright | `#24CCD2` | highlights, big numerals on dark |
| Teal light | `#50DFDD` | gradient start, accents on dark |
| Line | `#DCE8EC` | dividers, borders |
| Text | `#20242A` | body text |

Logo stays as is (SILVER `#489690`, MORPH `#3C4E6C`), `assets/logo.png`. Font Inter, monospace for small labels. The earlier warm cream and muted teal (`#FAF9F6`, `#4F9A98`, `#33415F`) are retired.

### Reference motif (partnership lockup, from the attached image)
White field, pale curves, a teal-gradient corner with a deep-navy stripe and a thin teal line at two opposite corners, both logos side by side with a thin vertical divider and a teal x between them. All ecosystem-partner posters follow this. Layout 5A implements it in the square frame (the owner first asked for the reference's 16:9, then chose square): partner logo left, Silvermorph logo right; slot `partner_logo`, optional `own_logo`, optional one-line `headline` caption. The header logo and bottom strip are hidden because the lockup already carries the logo; the category tag stays. The corner stripes may be reused on other categories later; they are not required.

## Design direction: the voice-first "line"
Ezzy turns one voice message into one schedule across many handoffs, so the visual language is a line: waveform (voice), tangled thread (handoffs), straight line (Ezzy). Bold through scale and asymmetry (oversized type and numerals, arch crop, tilted cards, inverted backgrounds), never through new colours.

## Frame invariants (never break)
Logo top-left · category tag top-right · wordmark strip at the bottom · one idea per poster · headline readable at 360 px wide · English only · brand tokens only.

## Layout pool (rotate within a category, never the same layout twice in a row)
| ID | Category | Look |
|---|---|---|
| 1A | Team News | photo, date chip, deep-blue lower-third panel |
| 1B | Team News | huge name, arch-cropped portrait |
| 2A | Product Update | tinted waveform ribbon, tilted phone with chat |
| 2B | Product Update | dark, giant percentage, ranked match card |
| 2C | Product Update | same as 2A but the phone shows a REAL English screenshot or recording frame (slot `screenshot`). Preferred whenever a real capture exists |
| 3A | Insight | dark, giant headline, teal key-phrase block, concentric arcs |
| 3B | Insight | tangled thread vs straight line diagram |
| 4A | Customer Story | giant quote mark, quote, attribution |
| 4B | Customer Story | dark, old value struck through, new value giant |
| 5A | Partnership | reference lockup, square: partner logo, divider and ×, Silvermorph logo, corner stripes, category tag kept top-right. No header logo or bottom strip |
| 5B | Partnership | orbit diagram around Ezzy, one corner stripe |
New layouts may be added if they keep the tokens and invariants. Record the last layout used per category in `published/publish-log.csv`.

## Image policy (owner decision)
- AI-generated images are allowed when they match the look: warm natural light, muted palette, negative space, no neon, no glossy 3D, no busy collage.
- People images: photographic, cinema-lens look (shallow depth of field, natural skin, real Hong Kong care settings, candid). Must read as a real person in a real scene.
- No readable text, logos or UI inside generated images.
- Real photos or real captures are mandatory for: named people, named customers, product UI. AI never stands in for a specific real person or deployment.
- Product UI is cropped to one key screen, English, legible at phone width.
- Insight posters are typography or diagram only.
- The Ezzy logo asset on the site contains Chinese characters (易仔). Posters are English-only: use an English-only Ezzy logo, or none.

## Stamps
`--stamp` is an optional internal marker and is off in all showcase renders. Safety does not rely on it: the gates in `categories.md`, the rubric and the approval card decide what may be published. A stamped poster is never published.
