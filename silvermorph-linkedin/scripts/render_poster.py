#!/usr/bin/env python3
"""Render a Silvermorph LinkedIn poster (1200x1200 PNG) from a layout id and slot values.

  python3 scripts/render_poster.py --list
  python3 scripts/render_poster.py --layout 2A \
      --set "headline=Voice note in.|Schedule|updated." --set "sub=Ezzy · Cantonese on WhatsApp" \
      --set "voice_label=Madam Chan · voice note" --set "voice_text=..." --set "reply_label=Ezzy · confirmed" \
      --set "reply_text=..." --out out.png

"|" inside a value is a line break. Photo slots take a file path.
--bg PHOTO [--bg-strength 0.88] puts an environment photo under any layout (brand grade, scrim, light grain).
Layouts are a pool per category; the skill rotates them (see references/design-guide.md).
A missing required slot is an error. A missing photo is an error unless --allow-placeholder.
--html FILE --out out.png [--size 1200x1200] screenshots a hand-written HTML poster (use when no layout fits; see references/html-composition.md).
Chrome path: set CHROME_PATH if Chrome is not at the macOS default.
--stamp "DRAFT · NEEDS SIGN-OFF" overlays a warning chip. A stamped poster must never be published.
"""
import argparse
import html
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "assets" / "posters.css").read_text(encoding="utf-8")
LOGO = (ROOT / "assets" / "logo.png").as_uri()
CHROME = os.environ.get("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
e = html.escape


def br(s):
    return e(s).replace("|", "<br>")


def img_uri(p):
    return Path(p).expanduser().resolve().as_uri()


def photo_div(slots, key, cls="fill"):
    p = slots.get(key)
    if p:
        return f'<div class="photo {cls}" style="background:url(\'{img_uri(p)}\') center/cover"></div>'
    return f'<div class="photo {cls}"><span>REAL PHOTO NEEDED<br><b>{e(slots.get("photo_label", key))}</b></span></div>'


def bars(n=14):
    hs = [30, 62, 40, 82, 55, 95, 48, 72, 36, 64, 52, 30, 58, 42]
    return '<span class="wv">' + "".join(f'<i style="height:{h}%;background:#0096A8"></i>' for h in hs[:n]) + "</span>"


def ribbon():
    ps = ""
    for i, (a, ph, op) in enumerate([(60, 0, .55), (90, 1.2, .35), (130, 2.1, .22), (45, 3.3, .5)]):
        pts = " ".join(f"{x},{600 + i * 70 - 120 + a * math.sin(x / 95 + ph) * math.sin(x / 430 + ph):.1f}" for x in range(-20, 1240, 20))
        ps += f'<polyline points="{pts}" fill="none" stroke="#0096A8" stroke-width="{6 if i % 2 == 0 else 3}" stroke-linecap="round" opacity="{op}"/>'
    return f'<svg class="ribbon" viewBox="0 0 1200 1200" preserveAspectRatio="none">{ps}</svg>'


# ---- layouts: id -> (category tag, dark, tint, required slots, builder) -------------------------

def l1a(s):
    return ('<div class="st">' + photo_div(s, "photo") + f'<div class="lt"><span class="chip">{e(s["date"])}</span>'
            f'<h4>{br(s["headline"])}</h4><p>{e(s["sub"])}</p></div></div>')


def l1b(s):
    return (f'<div class="st"><div class="nm"><small>{e(s["role"])}</small><h4>{br(s["name"])}</h4><p>{e(s["line"])}</p></div>'
            f'<span class="chip chipb">{e(s["event"])}</span><div class="arch">{photo_div(s, "photo")}</div></div>')


def l2a(s):
    return (ribbon() + f'<div class="h2a">{br(s["headline"])}<small>{e(s["sub"])}</small></div>'
            f'<div class="phone"><div class="ph-h"><b>Ezzy</b><span>Online</span></div><div class="ph-b">'
            f'<div class="bb l"><small>{e(s["voice_label"])}</small>{bars()}<p>{e(s["voice_text"])}</p></div>'
            f'<div class="bb r"><small>{e(s["reply_label"])}</small><p>{e(s["reply_text"])}</p></div></div></div>')


def l2c(s):
    shot = f"url('{img_uri(s['screenshot'])}') top center/cover" if s.get("screenshot") else "repeating-linear-gradient(135deg,#E2ECEF 0 22px,#EDF4F6 22px 44px)"
    return (ribbon() + f'<div class="h2a">{br(s["headline"])}<small>{e(s["sub"])}</small></div>'
            f'<div class="phone"><div class="shot" style="background:{shot}"></div></div>')


def l2b(s):
    return (f'<div class="mono">{e(s["label"])}</div><div class="giant">{e(s["pct"])}<span>%</span></div>'
            '<div class="gh gh2"></div><div class="gh gh1"></div>'
            f'<div class="mcard"><b>{e(s["name"])}</b><span>{e(s["detail"])}</span></div><div class="h2b">{br(s["headline"])}</div>')


def l3a(s):
    arcs = ('<svg class="arcs" viewBox="0 0 700 700"><g fill="none" stroke="#0096A8" stroke-width="3"><circle cx="350" cy="350" r="120" opacity=".9"/>'
            '<circle cx="350" cy="350" r="200" opacity=".6"/><circle cx="350" cy="350" r="280" opacity=".4"/><circle cx="350" cy="350" r="340" opacity=".25"/></g></svg>')
    return arcs + f'<div class="h3a">{br(s["lines"])}<br><em>{e(s["emphasis"])}</em></div>'


def l3b(s):
    nodes = [n.strip() for n in s["nodes"].split("|")]
    xs = [70 + i * (720 / max(len(nodes) - 1, 1)) for i in range(len(nodes))]
    nd = "".join(f'<circle cx="{x:.0f}" cy="150" r="16" fill="#fff" stroke="#0C305A" stroke-width="5"/>'
                 f'<text x="{x:.0f}" y="238" text-anchor="middle" font-size="26" font-weight="600" fill="#0C305A">{e(n)}</text>' for x, n in zip(xs, nodes))
    d = f"M{xs[0]:.0f} 150 " + " ".join(f"C{x0 + 70:.0f} {10 if i % 2 == 0 else 290} {x1 - 70:.0f} {290 if i % 2 == 0 else 10} {x1:.0f} 150"
                                       for i, (x0, x1) in enumerate(zip(xs, xs[1:])))
    return (f'<div class="h3b">{br(s["heading"])}</div><div class="pan p1"><small>TODAY</small><svg viewBox="0 0 860 260">'
            f'<path d="{d}" fill="none" stroke="#0096A8" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
            f'<path d="M{xs[0]:.0f} 150 C250 300 600 -40 {xs[-1]:.0f} 150" fill="none" stroke="#0C305A" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>{nd}</svg></div>'
            '<div class="pan p2"><small>WITH EZZY</small><svg viewBox="0 0 860 200"><line x1="70" y1="100" x2="640" y2="100" stroke="#50DFDD" stroke-width="8" stroke-linecap="round"/>'
            '<polygon points="640,76 690,100 640,124" fill="#50DFDD"/><rect x="70" y="52" width="260" height="96" rx="48" fill="#fff"/>'
            f'<text x="200" y="112" text-anchor="middle" font-size="34" font-weight="800" fill="#0C305A">{e(s["action"])}</text>'
            f'<rect x="700" y="52" width="150" height="96" rx="48" fill="#0096A8"/><text x="775" y="112" text-anchor="middle" font-size="34" font-weight="800" fill="#fff">{e(s["done"])}</text></svg></div>')


def l4a(s):
    return (f'<div class="qm">“</div><div class="qt">{e(s["quote"])}</div><div class="who"><i>{e(s["name"][:1].upper() if "initial" not in s else s["initial"])}</i>'
            f'<div><b>{e(s["name"])}</b><span>{e(s["role"])}</span></div></div>')


def l4b(s):
    return (f'<div class="mono">{e(s["label"])}</div><div class="old">{e(s["old"])}</div>'
            f'<div class="new">{e(s["new"])}<span>{e(s["unit"])}</span></div><div class="cap">{e(s["caption"])}</div>')


def corners(top_left=True, w=1200, h=1200, k=1.0):
    """Reference lockup style: bright teal gradient corner, navy stripe, thin line, plus pale curves."""
    g = ('<defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#50DFDD"/><stop offset="1" stop-color="#0096A8"/></linearGradient></defs>')
    a, b, c = 320 * k, 385 * k, 425 * k
    tl = (f'<polygon points="0,0 {a:.0f},0 0,{a:.0f}" fill="url(#cg)"/><polygon points="{a:.0f},0 {b:.0f},0 0,{b:.0f} 0,{a:.0f}" fill="#06244E"/>'
          f'<line x1="{c:.0f}" y1="0" x2="0" y2="{c:.0f}" stroke="#50DFDD" stroke-width="3" opacity=".85"/>')
    top = f'<g>{tl}</g>' if top_left else ''
    return (f'<svg class="cn" viewBox="0 0 {w} {h}">{g}<circle cx="{w * .87:.0f}" cy="{h * .12:.0f}" r="{h * .28:.0f}" fill="#EAF8FB" opacity=".8"/>'
            f'<circle cx="{w * .10:.0f}" cy="{h * .94:.0f}" r="{h * .39:.0f}" fill="#F3FBFD" stroke="#BDEFF2" stroke-width="2" opacity=".9"/>'
            + top + f'<g transform="rotate(180 {w / 2:.0f} {h / 2:.0f})">{tl}</g></svg>')


def l5a(s):
    own = img_uri(s["own_logo"]) if s.get("own_logo") else LOGO
    cap = f'<div class="lk-h lk-cap">{br(s["headline"])}</div>' if s.get("headline") else ""
    return (corners() + f'<div class="lock"><div class="lg"><img src="{img_uri(s["partner_logo"])}" alt=""></div>'
            f'<div class="mid"><i></i><b>×</b><i></i></div><div class="lg"><img src="{own}" alt=""></div></div>' + cap)


def l5b(s):
    sat = [p.split(":", 1) for p in s["partners"].split(";") if p.strip()]
    cx, cy, r = 600, 390, 290
    lines = pills = ""
    for i, (n, role) in enumerate(sat):
        a = math.radians(-90 + 360 / len(sat) * i)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        lines += f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="#0096A8" stroke-width="3" opacity=".5"/>'
        pills += (f'<rect x="{x - 110:.0f}" y="{y - 44:.0f}" width="220" height="88" rx="44" fill="#fff" stroke="#DCE8EC" stroke-width="2"/>'
                  f'<text x="{x:.0f}" y="{y - 4:.0f}" text-anchor="middle" font-size="27" font-weight="800" fill="#0C305A">{e(n.strip())}</text>'
                  f'<text x="{x:.0f}" y="{y + 26:.0f}" text-anchor="middle" font-size="21" fill="#0096A8" font-weight="600">{e(role.strip())}</text>')
    svg = (f'<svg class="orbit" viewBox="0 0 1200 780"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#0096A8" stroke-width="2" stroke-dasharray="3 12" opacity=".7"/>'
           f'{lines}<circle cx="{cx}" cy="{cy}" r="120" fill="#0C305A"/><text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="68" font-weight="800" fill="#fff">{e(s.get("center", "Ezzy"))}</text>'
           f'<text x="{cx}" y="{cy + 44}" text-anchor="middle" font-size="22" fill="#50DFDD" font-weight="600">{e(s.get("center_sub", "schedule · matching"))}</text>{pills}</svg>')
    return corners(top_left=False) + svg + f'<div class="h5b">{br(s["headline"])}</div>'


SIZES = {}  # all layouts are square 1200 x 1200 (owner decision 2026-10-14)

LAYOUTS = {
    "1A": ("TEAM NEWS", False, False, ["date", "headline", "sub", "photo"], l1a),
    "1B": ("TEAM NEWS", False, False, ["role", "name", "line", "event", "photo"], l1b),
    "2A": ("PRODUCT UPDATE", False, True, ["headline", "sub", "voice_label", "voice_text", "reply_label", "reply_text"], l2a),
    "2C": ("PRODUCT UPDATE", False, True, ["headline", "sub", "screenshot"], l2c),
    "2B": ("PRODUCT UPDATE", True, False, ["label", "pct", "name", "detail", "headline"], l2b),
    "3A": ("INSIGHT", True, False, ["lines", "emphasis"], l3a),
    "3B": ("INSIGHT", False, False, ["heading", "nodes", "action", "done"], l3b),
    "4A": ("CUSTOMER STORY", False, False, ["quote", "name", "role"], l4a),
    "4B": ("CUSTOMER STORY", True, False, ["label", "old", "new", "unit", "caption"], l4b),
    "5A": ("PARTNERSHIP", False, False, ["partner_logo"], l5a),
    "5B": ("PARTNERSHIP", False, False, ["partners", "headline"], l5b),
}


GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' "
         "baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='200' height='200' filter='url(%23n)' opacity='.5'/></svg>")


def backdrop(path, dark, tint, strength):
    """Environment photo under the layout: brand grade + brand-colour scrim keeps type legible."""
    rgb = "6,36,78" if dark else ("234,248,251" if tint else "255,255,255")
    a0, a1 = strength, max(strength - 0.38, 0.35)
    return (f'<div style="position:absolute;inset:0;background:url(\'{img_uri(path)}\') center/cover;filter:saturate(.8) sepia(.14) contrast(1.02)"></div>'
            f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba({rgb},{a0}) 0%,rgba({rgb},{a1}) 100%)"></div>'
            f'<div style="position:absolute;inset:0;background:url(&quot;{GRAIN}&quot;);opacity:.07;mix-blend-mode:multiply"></div>')


def build_html(layout, slots, stamp="", bg=None, bg_strength=0.88):
    tag, dark, tint, _, fn = LAYOUTS[layout]
    W, H = SIZES.get(layout, (1200, 1200))
    cls = ("dark " if dark else "") + ("tint " if tint else "") + ("bare" if layout == "5A" else "")
    body = (backdrop(bg, dark, tint, bg_strength) if bg else "") + fn(slots) + (f'<div class="demo">{e(stamp)}</div>' if stamp else "")
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            f"<style>{CSS}body,.poster{{width:{W}px;height:{H}px}}</style></head><body><div class=\"poster\"><div class=\"pin {cls}\">{body}"
            f'<div class="pt"><img src="{LOGO}" alt=""><span class="tag">{tag}</span></div><div class="pb">silvermorph tech</div></div></div></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--layout", choices=sorted(LAYOUTS))
    ap.add_argument("--set", action="append", default=[], metavar="key=value")
    ap.add_argument("--stamp", default="")
    ap.add_argument("--bg", help="environment photo placed under the layout (graded, with brand-colour scrim)")
    ap.add_argument("--bg-strength", type=float, default=0.88, help="scrim opacity at the text side, 0.6 to 0.95")
    ap.add_argument("--allow-placeholder", action="store_true")
    ap.add_argument("--html", help="screenshot this HTML file instead of a built-in layout")
    ap.add_argument("--size", default="1200x1200")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.list:
        for k, (tag, dark, tint, req, _) in LAYOUTS.items():
            print(f"{k}  {tag:15} slots: {', '.join(req)}")
        return 0
    if a.html:
        if not a.out:
            ap.error("--out is required")
        w, h = (int(x) for x in a.size.lower().split("x"))
        out = Path(a.out).resolve()
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                        "--virtual-time-budget=4000", f"--screenshot={out}", f"--window-size={w},{h}", Path(a.html).resolve().as_uri()],
                       check=True, capture_output=True)
        print(f"poster written: {out}  [custom html {w}x{h}]")
        return 0
    if not a.layout or not a.out:
        ap.error("--layout and --out are required")
    slots = dict(kv.split("=", 1) for kv in a.set)
    missing = [k for k in LAYOUTS[a.layout][3] if k not in slots and not (k == "photo" and a.allow_placeholder)]
    if missing:
        print(f"error: layout {a.layout} missing slots: {', '.join(missing)}", file=sys.stderr)
        return 2
    page = build_html(a.layout, slots, a.stamp, a.bg, a.bg_strength)
    out = Path(a.out).resolve()
    if a.html_only:
        out.write_text(page, encoding="utf-8")
        return 0
    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "p.html"
        h.write_text(page, encoding="utf-8")
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                        "--virtual-time-budget=4000", f"--screenshot={out}", f"--window-size={SIZES.get(a.layout, (1200, 1200))[0]},{SIZES.get(a.layout, (1200, 1200))[1]}", h.as_uri()],
                       check=True, capture_output=True)
    print(f"poster written: {out}  [{a.layout} {LAYOUTS[a.layout][0]}]" + ("  STAMPED, NOT PUBLISHABLE" if a.stamp else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
