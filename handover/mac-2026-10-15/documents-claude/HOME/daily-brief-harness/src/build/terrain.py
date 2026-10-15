"""Deterministic terrain SVG — no model draws anything.

Spec (reference/render.md): one unbroken #2E2C27 stroke edge to edge,
840×170, x mapped 6 AM → 10 PM at 52.5 px/hour, elevation = load. Meeting
dots on the line, r 6–13 by weight; optional/unanswered grey and weightless;
overlaps hollow. Clay #C6613F rationed to ONE accent, always at least one.
A calm day flattens to still water — the elevation term is proportional to
real load, so an empty calendar yields a nearly flat line by construction.
"""
from datetime import datetime

W, H, BASE_Y = 840, 170, 128
X0_HOUR, PX_PER_HOUR = 6.0, 52.5
INK, GREY, BG = "#2E2C27", "#B4B3A8", "#FCFCFB"
CLAY = "#C6613F"

def _hour(dt_iso):
    t = datetime.fromisoformat(dt_iso)
    return t.hour + t.minute / 60

def _x(hour):
    return max(0, min(W, (hour - X0_HOUR) * PX_PER_HOUR))

def build(today_events, motif: str | None = None):
    timed = [e for e in today_events if not e["all_day"]]
    loads = []          # (x_center, weight, grey?, hours)
    for e in timed:
        try:
            s, en = _hour(e["start"]), _hour(e["end"])
        except ValueError:
            continue
        grey = e.get("self_response") in ("needsAction", "tentative", "declined")
        loads.append((( _x(s) + _x(en)) / 2, min(en - s, 4.0), grey, (s, en)))

    # Elevation profile: sum of gaussian bumps, height ∝ event length.
    def elev(x):
        y = 0.0
        for cx, w, grey, _ in loads:
            if grey:
                continue
            y += (w * 22) * pow(2.71828, -((x - cx) ** 2) / (2 * 90 ** 2))
        return min(y, 95)

    pts = [(x, BASE_Y - elev(x)) for x in range(0, W + 1, 12)]
    path = "M " + " L ".join(f"{x:.0f} {y:.1f}" for x, y in pts)

    # Dots at event start positions, sitting ON the line.
    dots, spans = [], []
    for cx, w, grey, (s, en) in sorted(loads, key=lambda l: l[0]):
        r = 6 + min(7, w * 2.2)
        y = BASE_Y - elev(cx)
        overlap = any(s < b and en > a for a, b in spans)
        spans.append((s, en))
        if overlap:
            dots.append(f'<circle cx="{cx:.0f}" cy="{y:.0f}" r="{r:.0f}" '
                        f'fill="{BG}" stroke="{INK}" stroke-width="2"/>')
        elif grey:
            dots.append(f'<circle cx="{cx:.0f}" cy="{BASE_Y - elev(cx):.0f}" r="6" fill="{GREY}"/>')
        else:
            dots.append(f'<circle cx="{cx:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{INK}"/>')

    # Exactly one clay accent: the sun disc (open day) or first dot's halo.
    if motif == "sun" or not loads:
        accent = f'<circle cx="120" cy="42" r="14" fill="none" stroke="{CLAY}" stroke-width="2.5"/>'
    elif motif == "moon":
        accent = (f'<path d="M 790 40 a 13 13 0 1 0 10 21 a 10 10 0 1 1 -10 -21" '
                  f'fill="{CLAY}"/>')
    else:
        accent = f'<line x1="20" y1="{BASE_Y+18}" x2="60" y2="{BASE_Y+18}" stroke="{CLAY}" stroke-width="2.5"/>'

    return (f'<svg class="drawing" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="the drawn day">'
            f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="2.5" '
            f'stroke-linecap="round"/>{"".join(dots)}{accent}</svg>')
