# AI image prompts (tool-agnostic) and provenance

Use AI images only for atmosphere: Insight backgrounds, generic care scenes behind a `--bg` scrim. Never for named people, customers, team news or product UI. Never present an AI person as a real client, staff member or deployment.

## The look (put this in every prompt)
Candid documentary photograph, shot on a 35mm or 50mm cinema lens at f/1.8, shallow depth of field, soft natural window light, warm muted colour grade with gentle teal shadows, fine film grain, slightly imperfect framing, real lived-in Hong Kong interior. Natural skin with visible texture, real wrinkles, unposed expression.

## Prompt template
```
[SCENE], [WHO: age, role, clothing], [ACTION in progress, not looking at camera],
candid documentary photograph, 35mm cinema lens, f/1.8 shallow depth of field,
soft natural window light, warm muted palette with teal accents, film grain,
negative space on the [left/top] for headline text, square 1:1 composition
```
Negative / avoid: text, letters, logos, watermarks, plastic or airbrushed skin, perfect symmetry, staring at the camera with a stock smile, studio lighting, hospital-blue sterility, neon, 3D render, illustration, extra or fused fingers.

## Scenes that fit the brand (edit, do not copy blindly)
1. Home visit: a care worker and an older adult at a small dining table in a compact Hong Kong flat, checking a schedule on a phone, afternoon light through a window.
2. Coordinator at work: a woman at a desk with a phone and a notebook, mid-call, a care home corridor blurred behind her.
3. Evening handover: a nurse reading a phone in a quiet corridor, warm lamp light, city lights outside.
4. Hands only: an older adult's hand holding a phone with a voice message waveform glowing on the screen (no readable UI).
5. Skyline day and night: reuse `inputs/05-media/from-ezzy-site/morning-bg.webp` and `night-bg2.webp` (already on the site).

## Quality check before use (reject on any fail)
Hands and fingers correct · eyes and teeth natural · ears and jewellery symmetrical only by chance · no garbled text on clothes, signs or screens · uniform and setting consistent with Hong Kong care work · no resemblance to a real, identifiable person · looks fine at 360 px wide.

## Provenance (required)
Save to `inputs/05-media/photos/ai/ai-<scene>-<yyyymmdd>-<tool>.jpg` and add a row to `inputs/05-media/photos/ai/MANIFEST.md`: file, tool and model, full prompt, date, where used. Some tools embed AI metadata and LinkedIn may label such images; that is fine, hiding it is not.

## Export
At least 2400 px on the long side, crop to 1:1, keep a clean area where the headline sits, JPEG quality 90.
