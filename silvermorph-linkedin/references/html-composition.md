# HTML composition: how posters are made

All poster visuals come from HTML screenshotted to PNG. No AI image generation, ever (see `design-guide.md` image policy).

## Pick a path
1. **Built-in layout** (default): `python3 scripts/render_poster.py --layout <id> --set key=value ... --out poster.png`. Real photos go in photo slots; `--bg <real photo>` puts a real environment photo under any layout.
2. **Custom HTML** when no layout fits: write `poster.html` in the draft folder, then `python3 scripts/render_poster.py --html poster.html --out poster.png [--size 1200x1200]`.

## Custom HTML rules
- Start from `assets/posters.css` (link it with a relative or `file://` path) and use only the brand tokens from `design-guide.md`. Font Inter.
- Keep the frame rules: no header logo, no category tag, no wordmark strip (LinkedIn already shows the company name); 64 px margins; one idea; readable at 360 px wide.
- Place supplied materials with `<img>` or CSS `background` using absolute `file://` paths to `materials/`. Use `object-fit: cover` or `contain`; never stretch, never redraw or "enhance" a logo, face or screenshot.
- Atmosphere comes from CSS only: gradients, tint panels, arcs, waveform or line SVG, big type. Photos come from the user.
- Default canvas 1200x1200. Screenshot, view the PNG, fix overlaps and clipping, re-render.
- Save the HTML next to `poster.png` so edits are cheap.

## Check before the approval card
Text not clipped · logos sharp and undistorted · every photo is a supplied file · no placeholder box left · looks fine at 360 px wide.
