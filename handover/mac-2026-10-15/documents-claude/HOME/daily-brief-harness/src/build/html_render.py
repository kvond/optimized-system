"""Assemble the self-contained HTML page. Structure is fixed here; the model
never writes markup. Sections with nothing in them are dropped, heading and
all. Fonts embedded from assets/ — no network at open.
"""
import base64, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def _css():
    css = (ROOT / "templates" / "brief.css").read_text()
    woff = (ROOT / "assets" / "fonts" / "fraunces-latin-600-normal.woff2").read_bytes()
    return css.replace(
        "<BASE64 FROM assets/fonts/fraunces-latin-600-normal.woff2>",
        base64.b64encode(woff).decode())

def _esc(s):
    return html.escape(s or "", quote=False)

def _items(items):
    out = []
    for i, it in enumerate(items, 1):
        title = _esc(it["title"])
        if it.get("link"):
            title = f'<a href="{html.escape(it["link"])}">{title}</a>'
        out.append(
            f'<div class="item"><div class="num">{i}</div><div class="item-body">'
            f'<p class="item-title">{title}</p>'
            f'<p class="item-note">{_esc(it["sentence"])}</p></div></div>')
    return "".join(out)

def render(day_label, headline, terrain_svg, acts, needs, resolved,
           triggers_lines, carry, ahead, pull):
    b = []
    b.append(f'<div class="band-top"><div class="inner">'
             f'<p class="daydate">{_esc(day_label)}</p>'
             f'<h1>{_esc(headline)}</h1>{terrain_svg}<div class="acts">')
    for a in acts:
        b.append(f'<div class="act"><p class="act-time">{_esc(a["time"])}</p>'
                 f'<p class="act-note">{_esc(a["sentence"])}</p></div>')
    b.append('</div></div></div><div class="band-bottom"><div class="inner">')

    if not needs and not resolved:
        b.append('<p class="plain-note">Nothing needs you this morning.</p>')
    if needs:
        b.append(f'<div class="list"><h2>Needs attention</h2>{_items(needs)}</div>')
    if resolved:
        b.append(f'<div class="list"><h2>Resolved</h2>{_items(resolved)}</div>')

    if triggers_lines:
        b.append('<div class="list"><h2>Triggers</h2>'
                 '<p class="plain-note">Emitting a line writes nothing; '
                 'running the named skill does the work.</p>')
        for label, state in triggers_lines:
            b.append(f'<div class="trigger"><div class="trigger-label">{_esc(label)}</div>'
                     f'<div class="trigger-state">{_esc(state)}</div></div>')
        b.append('</div>')

    if carry:
        b.append(f'<div class="list"><h2>Carry forward</h2>'
                 f'<p class="plain-note">{_esc(carry)}</p></div>')
    if ahead:
        b.append('<div class="list"><h2>Look ahead</h2>')
        for d, what in ahead:
            b.append(f'<div class="ahead"><div class="ahead-date">{_esc(d)}</div>'
                     f'<div class="ahead-what">{_esc(what)}</div></div>')
        b.append('</div>')
    if pull:
        b.append(f'<div class="list"><h2>Pull forward</h2>'
                 f'<p class="plain-note">{_esc(pull)}</p></div>')
    b.append('</div></div>')

    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="noindex">'
            f'<title>{_esc(day_label)}</title><style>{_css()}</style></head>'
            f'<body>{"".join(b)}</body></html>')
