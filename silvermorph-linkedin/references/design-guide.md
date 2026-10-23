# Silvermorph LinkedIn: poster design guide (v2)

Renderer: `python3 scripts/render_poster.py --list` shows the layouts (live reference: `design-reference.html`, rebuilt by `scripts/build_reference.py`) and their slots. Output: 1200 x 1200 PNG (1:1, locked as default by the owner; a 4:5 variant is optional later). Filename: `silvermorph-<category>-<slug>.png`.

## Brand tokens (v3, owner-set 2026-10-14 from the SenseAI x Silvermorph partnership image)
Cool, clean, tech-forward, editorial. Sharp corners everywhere (no border-radius, no pills, no soft shadows); labels are mono caps with a short teal rule; panels are flush with their photos. Values sampled from the reference image.

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
White field, pale curves, a teal-gradient corner with a deep-navy stripe and a thin teal line at two opposite corners, both logos side by side with a thin vertical divider and a teal x between them. All ecosystem-partner posters follow this. Layout 5A implements it in the square frame: partner logo left, Silvermorph logo right; slot `partner_logo`, optional `own_logo`, optional one-line `headline` caption. The corner stripes may be reused on other categories later; they are not required.

## Design direction: the voice-first "line"
Ezzy turns one voice message into one schedule across many handoffs, so the visual language is a line: waveform (voice), tangled thread (handoffs), straight line (Ezzy). Bold through scale and asymmetry (oversized type and numerals, arch crop, tilted cards, inverted backgrounds), never through new colours.

## Frame invariants (never break)
No header logo, no category tag, no wordmark strip: LinkedIn already shows the company avatar and name above every post, so repeating them on the image is noise. Brand comes from the tokens, Inter and the layout language. The logo appears only where it carries meaning (the 5A partnership lockup). One idea per poster · generous 64 px margins · headline readable at 360 px wide · English only · brand tokens only.

## Layout pool (rotate within a category, never the same layout twice in a row)
| ID | Category | Look |
|---|---|---|
| 1A | Team News | photo, date chip, deep-blue lower-third panel |
| 1B | Team News | huge name, arch-cropped portrait |
| 1C | Team News | event recap with 3 photos: wide main photo, two smaller below, navy panel under the collage. Use when 2 or more event photos exist |
| 2A | Product Update | tinted waveform ribbon, tilted phone with chat |
| 2B | Product Update | dark, giant percentage, ranked match card |
| 2C | Product Update | same as 2A but the phone shows a REAL English screenshot or recording frame (slot `screenshot`). Preferred whenever a real capture exists |
| 3A | Insight | dark, giant headline, teal key-phrase block, concentric arcs |
| 3B | Insight | tangled thread vs straight line diagram |
| 4A | Customer Story | giant quote mark, quote, attribution |
| 4B | Customer Story | dark, old value struck through, new value giant |
| 5A | Partnership | reference lockup, square: partner logo, divider and ×, Silvermorph logo, corner stripes, no tag, no header or footer |
| 5B | Partnership | orbit diagram around Ezzy, one corner stripe |
New layouts may be added if they keep the tokens and invariants. Record the last layout used per category in `published/publish-log.csv`.

## Image policy (owner decision, 2026-10-23)
- **Never generate images with AI.** No image-generation tools, no AI people, no AI scenes or backgrounds. Generated images distort faces, hands, logos and UI, so every poster is built from the owner's real materials.
- Posters are made in **HTML and screenshotted** with `scripts/render_poster.py` (built-in layouts, or `--html` for a custom page; see `html-composition.md`). Photos, logos and screenshots are placed into the HTML as supplied: crop, scale, grade with CSS, never redraw.
- Allowed sources: files the user sent (`materials/`), the website assets in `inputs/05-media/`, brand logos, real product captures, and shapes, type, diagrams and icons drawn in HTML/SVG/CSS.
- If a slot needs a photo and none was supplied, ask for it. Never fill it with a generated or stock-looking stand-in. Insight posters are typography or diagram only.
- Product UI is cropped to one key screen, English, legible at phone width.
- The Ezzy logo asset on the site contains Chinese characters (易仔). Posters are English-only: use an English-only Ezzy logo, or none.

## Stamps
`--stamp` is an optional internal marker and is off in all showcase renders. Safety does not rely on it: the gates in `categories.md`, the rubric and the approval card decide what may be published. A stamped poster is never published.
