#!/usr/bin/env python3
"""Build references/design-reference.html: the live design reference.

Every poster in it is the real HTML from render_poster.py (in an iframe), not a screenshot.
Rebuild after changing a layout or the tokens:  python3 scripts/build_reference.py
Sample content is generic and fictional; it is not company fact.
"""
import base64
import html
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_poster as rp  # noqa: E402

ROOT = rp.ROOT
rp.LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "logo.png").read_bytes()).decode()

PARTNER_SVG = ("<svg xmlns='http://www.w3.org/2000/svg' width='480' height='160'><rect width='480' height='160' fill='white'/>"
               "<text x='240' y='95' text-anchor='middle' font-family='Arial' font-size='56' font-weight='700' fill='#0C305A'>Partner</text></svg>")
tmp = Path(tempfile.mkdtemp())
(tmp / "partner.svg").write_text(PARTNER_SVG)

# id: (title, when to use, slot values)
SAMPLES = {
    "1A": ("Team · event recap", "One strong event photo.",
           {"date": "20 OCT", "headline": "Care technology|expo day", "sub": "Sample sub line"}),
    "1B": ("Team · person", "One teammate: name, role, portrait.",
           {"role": "CO-FOUNDER", "name": "Alex|Wong", "line": "on AI in home-based elderly care", "event": "TECH TALK 2026"}),
    "1C": ("Team · event recap, 3 photos", "Two or more event photos: wide main photo plus two details.",
           {"date": "20 OCT", "headline": "Community care|expo day", "sub": "Booth exhibitor, practical exchange area"}),
    "2A": ("Product · chat on phone", "A feature that starts from a voice note or chat.",
           {"headline": "Voice note in.|Schedule|updated.", "sub": "Ezzy · Cantonese on WhatsApp", "voice_label": "Care worker · voice note",
            "voice_text": "Can we move Tuesday's visit to Thursday?", "reply_label": "Ezzy · confirmed", "reply_text": "Moved to Thu 10:00. Family notified."}),
    "2C": ("Product · real screenshot", "Same as 2A with a real English screenshot in the phone. Preferred when a capture exists.",
           {"headline": "Voice note in.|Schedule|updated.", "sub": "Ezzy · Cantonese on WhatsApp"}),
    "2B": ("Product · match card", "A result with one headline number.",
           {"label": "TOP MATCH · SAMPLE", "pct": "98", "name": "Sample Nurse", "detail": "Wound care · nearby · free Thu", "headline": "Many attributes.|One best match."}),
    "3A": ("Insight · thesis type", "A one-line thesis, typography only.",
           {"lines": "Every handoff|in home care|costs", "emphasis": "a wait."}),
    "3B": ("Insight · diagram", "Tangled handoffs versus one straight line.",
           {"heading": "Five handoffs,|or one.", "nodes": "Client|Coordinator|Nurse|Family|Record", "action": "Voice note", "done": "Done"}),
    "4A": ("Customer · quote", "One approved quote with attribution.",
           {"quote": "Sample quote about how the team saves time on coordination.", "name": "Sample Name", "role": "Care Manager, Sample Home"}),
    "4B": ("Customer · number", "An old value struck through, a new value large.",
           {"label": "DAILY ADMIN TIME", "old": "3 hours", "new": "45", "unit": "min", "caption": "Sample figure, not a claim"}),
    "5A": ("Partner · lockup", "Partnership announcement: both logos, divider and ×.",
           {"partner_logo": str(tmp / "partner.svg")}),
    "5B": ("Partner · ecosystem", "Ezzy in the centre, specialists around it.",
           {"partners": "Partner A:Vitals;Partner B:Sleep;Partner C:Cognitive;Partner D:Mobility", "headline": "One schedule.|Four specialists."}),
}

TOKENS = [("White", "#FFFFFF", "background"), ("Pale cyan", "#F6FCFC", "cards"), ("Tint", "#EAF8FB", "soft shapes"),
          ("Navy", "#0C305A", "headings"), ("Deep navy", "#06244E", "dark bg, stripe"), ("Teal deep", "#0096A8", "accent lines"),
          ("Teal bright", "#24CCD2", "highlights"), ("Teal light", "#50DFDD", "on dark"), ("Logo teal", "#489690", "wordmark, fixed"),
          ("Logo slate", "#3C4E6C", "wordmark, fixed")]


def poster(layout, slots):
    page = rp.build_html(layout, slots)
    return f'<div class="pw"><iframe loading="lazy" title="{layout}" srcdoc="{html.escape(page, quote=True)}"></iframe></div>'


def main():
    figs = ""
    for k, (title, use, slots) in SAMPLES.items():
        cmd = f"--layout {k} " + " ".join(f'--set "{a}={b}"' for a, b in slots.items() if a != "partner_logo")
        figs += (f'<figure><div class="card">{poster(k, slots)}</div><figcaption><b>{k}</b> {html.escape(title)}'
                 f'<span>{html.escape(use)}</span><code>{html.escape(rp.LAYOUTS[k][0])} · slots: {html.escape(", ".join(rp.LAYOUTS[k][3]))}</code>'
                 f'<code class="cmd">{html.escape(cmd)}</code></figcaption></figure>')
    sw = "".join(f'<div class="sw" style="background:{h};color:{"#fff" if i in (3, 4, 5, 8, 9) else "#0C305A"}"><b>{n}</b><code>{h}</code><span>{u}</span></div>'
                 for i, (n, h, u) in enumerate(TOKENS))
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Silvermorph LinkedIn design reference</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0C305A;--deep:#06244E;--teal:#0096A8;--tint:#EAF8FB;--line:#DCE8EC}}
*{{box-sizing:border-box;margin:0}}body{{font:16px/1.55 Inter,-apple-system,Arial,sans-serif;color:#20242A;background:#fff}}
header{{background:var(--deep);color:#fff;padding:64px 6vw}}header small{{font:600 13px ui-monospace,Menlo,monospace;letter-spacing:3px;color:#50DFDD}}
h1{{font-size:clamp(34px,6vw,64px);line-height:1.05;margin:12px 0;letter-spacing:-1.5px}}h1 em{{font-style:normal;color:#24CCD2}}
header p{{max-width:640px;opacity:.85}}main{{max-width:1180px;margin:0 auto;padding:0 6vw 80px}}
h2{{font-size:30px;color:var(--navy);margin:56px 0 8px;padding-bottom:10px;border-bottom:2px solid var(--navy)}}
.lead{{margin:12px 0 20px;max-width:760px}}.sws{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}}
.sw{{border:1px solid var(--line);padding:12px;display:flex;flex-direction:column;gap:2px;font-size:13px}}.sw code{{font-size:12px}}
.cols{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;margin-top:20px}}
.cols h3{{font:700 12px ui-monospace,Menlo,monospace;letter-spacing:2px;color:var(--teal);margin-bottom:6px}}
.pool{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:28px;margin-top:20px}}
figure .card{{box-shadow:0 6px 24px rgba(6,36,78,.15);overflow:hidden}}
.pw{{position:relative;width:100%;aspect-ratio:1/1;overflow:hidden}}.pw iframe{{position:absolute;left:0;top:0;width:1200px;height:1200px;border:0;transform-origin:0 0}}
figcaption{{margin-top:10px;font-size:14px;display:flex;flex-direction:column;gap:3px}}figcaption span{{color:#5b6670}}
figcaption code{{font:12px ui-monospace,Menlo,monospace;color:var(--teal)}}figcaption .cmd{{color:#5b6670;word-break:break-all}}
</style></head><body>
<header><small>SILVERMORPH TECH · LINKEDIN SYSTEM</small><h1>Every post image is <em>HTML</em>.</h1>
<p>These are the live layouts, rendered by the same code that makes the real posters, then screenshotted to PNG. Sample content is fictional.</p></header>
<main>
<h2>Design standard</h2><p class="lead">Cool, clean, tech-forward. Square 1200 × 1200. Inter. Brand colours only.</p><div class="sws">{sw}</div>
<div class="cols"><div><h3>FRAME, NEVER BROKEN</h3>Two small corner marks: category tag top-right, wordmark bottom-left. No header logo or footer strip, since LinkedIn already shows the company name. 64 px margins. One idea per poster. Headline readable at 360 px wide. English only.</div>
<div><h3>IMAGES</h3>No AI-generated images. Photos, logos and screenshots come from the team and are placed into the HTML as supplied. Atmosphere is CSS and SVG only.</div>
<div><h3>HOW TO MAKE ONE</h3>Pick a layout below, run <code>render_poster.py --layout ID --set key=value --out poster.png</code>. No layout fits? Write HTML and use <code>--html</code>.</div></div>
<h2>Layout pool</h2><p class="lead">Rotate within a category; never the same layout twice in a row.</p><div class="pool">{figs}</div>
</main>
<script>
function fit(){{document.querySelectorAll('.pw').forEach(function(w){{w.firstElementChild.style.transform='scale('+(w.clientWidth/1200)+')'}})}}
addEventListener('resize',fit);addEventListener('load',fit);fit();
</script></body></html>"""
    out = ROOT / "references" / "design-reference.html"
    out.write_text(page, encoding="utf-8")
    print(f"written: {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
