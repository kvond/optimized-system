# daily-brief reference — HTML rendering

One self-contained file. No network at open: fonts embedded, CSS and JS inline, images as data
URIs. It must render correctly on first open — Katherine reads it once, on a phone, and never
sees a retry.

## Page shape, top to bottom

Two full-bleed bands. Content max-width 860px inside each, generous padding. The bands meet at a
hard edge with a 1px line; no card border, no rounded corners.

**Top band** (wash `#F9F9F7`):

1. **Day-date** — small, ink-soft, above the headline: `Sunday · August 2 2026`
2. **Headline** — one serif line, spoken like a friend handing over the day. If one thing makes
   today distinct (she is running something, a decision gets made, a rare open stretch), name
   that. Otherwise name the shape of the day. Never both.
3. **The drawing** — one SVG about 840×170. One unbroken terrain stroke edge to edge, elevation =
   load. A calm day flattens to still water; never invent mountains. No card, no fill, no border.
4. **Three acts** — left-aligned text columns under the drawing with faint hairline dividers.
   Each stacks a bold time range over one sentence earned from the calendar. Uppercase AM/PM on
   the trailing time, and on the leading time when the range crosses noon: `9:30 AM – 1 PM`,
   `1 – 3:30 PM`, `3:30 PM onward`. Focal points sit above column centres (x ≈ 140 / 420 / 700).

**Bottom band** (bg `#FCFCFB`), in this order, each with a system-sans heading:

5. **Needs attention** — numbered items: bold linked title ≤10 words, then one sentence carrying
   the ask and why today. The source phrase inside the sentence is the link ("on your calendar",
   "in the doc"), underlined ink-soft, no colour change. That is the only link in the sentence.
6. **Resolved** — same layout. What closed, who closed it, when, outcome in a phrase.
7. **Triggers** — label column (fixed width) + state column. One line each, `emit_order` order.
   Introduce with one plain sentence: emitting writes nothing, running the skill does the work.
8. **Carry forward** — prose.
9. **Look ahead** — bold date column + what. One date per line.
10. **Pull forward** — prose. Only when a block is open today.

Nothing in either mail list → one calm line in place of both: "Nothing needs you this morning."
A section with nothing found is dropped, heading and all.

## Terrain

One `#2E2C27` stroke. Meeting dots filled `#2E2C27`, sitting on the line, r 6–13 by weight.
Optional or unanswered = grey `#B4B3A8`, weightless. Genuine overlap = two hollow circles
intersecting, filled `#FCFCFB` (the only hollow dots).

At most one supporting motif per act: sun = open creative time · half-risen sun on a horizon =
pre-7:30 start · crescent moon = late finish · birds = room to breathe · fireworks = holiday eve ·
flag = deadline · a distant second ridge through a saddle = depth on heavy days.

Clay `#C6613F` is rationed to ONE accent across the whole drawing. Always include at least one.

Map the day to x by hours: x = 0 is 6 AM, x = 840 is 10 PM, 52.5px per hour.

## Colour and type

- bg `#FCFCFB` · wash `#F9F9F7` · ink `#2E2C27` · ink-soft `#6B6A63` · ink-grey `#B4B3A8` ·
  hairline `#E4E3DC` · line `#E1E1DF` · clay `#C6613F`
- Ink: headline, section headings, item titles, terrain stroke, meeting dots.
  Ink-soft: body, act sentences, item sentences, day-date. Ink-grey: numerals, grey dots.
- Fraunces 600 for the headline only, 40px (30px below 640px). Everything else the system stack,
  `-apple-system, "Segoe UI", sans-serif`. Never italic.
- Nothing on the page is a button, badge, chip, or filled label. No footer, no timestamp.

## Fonts

`assets/fonts/fraunces-latin-600-normal.woff2` ships with this skill. Base64 it straight into the
`@font-face` data URI. No network call.

Do **not** fetch from Google Fonts: `fonts.googleapis.com` (the CSS) is reachable in the sandbox
but `fonts.gstatic.com` (the binaries) is blocked by the egress proxy. The failure only appears
after the CSS step has seemingly succeeded — urllib dies with "Tunnel connection failed: 403",
curl with exit 56. If the asset is somehow missing, `npm pack @fontsource/fraunces` and extract
`files/fraunces-latin-600-normal.woff2`; if that also fails, fall back to `Georgia, serif` and
skip the `@font-face`. A system-font page that opens cleanly beats a broken data URI.

Fraunces covers Latin script only. For a headline in another script use a high-quality system
serif and skip the `@font-face`.

## Build recipe

Write a small Python script that reads the base64 and substitutes it into the HTML template — do
not paste 24KB of base64 into a tool call.

```
base64 -w0 assets/fonts/fraunces-latin-600-normal.woff2 > font.b64
```

Then screenshot and actually look at the image before delivering:

```
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:960,height:1600}});await p.goto('file://<abs path>');await p.waitForTimeout(600);await p.screenshot({path:'brief.png',fullPage:true});await b.close();})();"
```

`executablePath` matters: a bare `chromium.launch()` looks for a browser revision that is not
installed and suggests `playwright install`, which must not be run — the download is blocked and
wastes minutes. If playwright is not in `node_modules`, `npm install playwright` first; the
package installs fine, only browser downloads are blocked.

## Verify on the screenshot

Day-date above headline · one unbroken stroke with every dot on it · three acts · serif on the
headline only · clay in at most one drawing accent · both mail lists share one style · every item
title linked where a URL exists · every quote verbatim · every href https · sections in the order
above with empty ones dropped · no chips, cards, badges, footer, or timestamp · no act restates a
list item · no sentence commands, apologizes, pads, reviews, or narrates process · below 640px the
acts stack and nothing clips.

## Stylesheet

Paste this verbatim; it is the validated version.

```css
@font-face {
  font-family: 'Fraunces';
  font-style: normal;
  font-weight: 600;
  font-display: block;
  src: url(data:font/woff2;base64,<BASE64 FROM assets/fonts/fraunces-latin-600-normal.woff2>) format('woff2');
}
:root {
  --bg: #FCFCFB;
  --wash: #F9F9F7;
  --ink: #2E2C27;
  --ink-soft: #6B6A63;
  --ink-grey: #B4B3A8;
  --hairline: #E4E3DC;
  --line: #E1E1DF;
  --clay: #C6613F;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: -apple-system, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
}
.band-top { background: var(--wash); border-bottom: 1px solid var(--line); }
.band-bottom { background: var(--bg); }
.inner { max-width: 860px; margin: 0 auto; padding: 56px 32px 44px; }
.band-bottom .inner { padding-top: 46px; padding-bottom: 76px; }

.daydate {
  font-size: 13px;
  letter-spacing: 0.06em;
  color: var(--ink-soft);
  margin: 0 0 14px;
}
h1 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 40px;
  line-height: 1.22;
  letter-spacing: -0.01em;
  margin: 0 0 30px;
  color: var(--ink);
}
.drawing { width: 100%; height: auto; display: block; margin: 4px 0 6px; }

.acts { display: flex; margin-top: 10px; }
.act { flex: 1 1 0; padding: 0 22px; }
.act:first-child { padding-left: 0; }
.act:last-child { padding-right: 0; }
.act + .act { border-left: 1px solid var(--hairline); }
.act-time {
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--ink);
  margin: 0 0 7px;
}
.act-note {
  font-size: 14px;
  line-height: 1.55;
  color: var(--ink-soft);
  margin: 0;
}

h2 {
  font-family: -apple-system, "Segoe UI", sans-serif;
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--ink);
  margin: 0 0 20px;
}
.list { margin: 0 0 46px; }
.list:last-child { margin-bottom: 0; }
.item { display: flex; gap: 18px; padding: 0 0 22px; }
.num {
  font-size: 13px;
  color: var(--ink-grey);
  min-width: 16px;
  padding-top: 2px;
  font-variant-numeric: tabular-nums;
}
.item-body { flex: 1; }
.item-title {
  font-size: 15.5px;
  font-weight: 700;
  line-height: 1.4;
  color: var(--ink);
  margin: 0 0 5px;
}
.item-title a { color: inherit; text-decoration: none; }
.item-title a:hover { text-decoration: underline; }
.item-note {
  font-size: 14.5px;
  line-height: 1.6;
  color: var(--ink-soft);
  margin: 0;
}
.item-note a {
  color: inherit;
  text-decoration: underline;
  text-decoration-color: var(--ink-grey);
  text-underline-offset: 2px;
}
.trigger { display: flex; gap: 18px; padding: 0 0 15px; }
.trigger-label {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--ink);
  min-width: 178px;
}
.trigger-state {
  font-size: 14.5px;
  line-height: 1.55;
  color: var(--ink-soft);
  flex: 1;
}
.trigger-state code {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: 13px;
}
.ahead { display: flex; gap: 18px; padding: 0 0 13px; }
.ahead-date {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--ink);
  min-width: 96px;
}
.ahead-what { font-size: 14.5px; line-height: 1.55; color: var(--ink-soft); flex: 1; }
.plain-note { font-size: 14.5px; line-height: 1.6; color: var(--ink-soft); margin: 0 0 22px; }
@media (max-width: 640px) {
  .trigger, .ahead { display: block; }
  .trigger-label, .ahead-date { min-width: 0; margin-bottom: 3px; }
}
@media (max-width: 640px) {
  .inner { padding: 40px 22px 34px; }
  h1 { font-size: 30px; }
  .acts { display: block; }
  .act { padding: 0; }
  .act + .act {
    border-left: none;
    border-top: 1px solid var(--hairline);
    margin-top: 18px;
    padding-top: 18px;
  }
}
```
