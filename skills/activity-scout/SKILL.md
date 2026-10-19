---
name: activity-scout
description: Katherine's monthly opportunity calendar. Sweeps a verified source registry plus the login-gated sites (Meetup, Facebook Events, Instagram, Eventbrite) for activities that build her long-term capabilities, scores them against the life-design spec, and renders one tickable HTML calendar covering two horizons — next month day-by-day, and four months out for anything with a registration deadline. Runs the last Sunday of each month. Triggers - "activity scout", "opportunity calendar", "what's on next month", "run the scout", scheduled monthly run.
---

# Activity Scout

Builds the monthly opportunity calendar. The governing principle, in Katherine's words: **optimize for becoming, not merely doing.** Every recommendation must answer "what capability does this help me become?" rather than "how does this fill an evening?"

Read `references/life-design.md` before scoring anything. Read `references/source-registry.md` before searching — it holds the verified local sources, the confirmed school-year survivors, and the known dead ends, so each run starts from accumulated knowledge rather than from zero.

---

## Cadence

**Last Sunday of the month.** The scheduled task fires every Sunday; this skill gates itself.

**Gate, run this first:** if more than 7 days remain in the current month, this is not the last Sunday. Exit silently without producing anything and without messaging Katherine. Only proceed when 7 or fewer days remain.

Manual invocation ignores the gate and runs immediately.

---

## Two horizons, every run

Both are produced in the same document. Neither is optional.

**Horizon A — next calendar month, day by day.** The tickable calendar. Local recurring offerings, one-time events, everything inside the drive radius.

**Horizon B — four months out.** Only items that carry a *registration consequence*: an early-bird cutoff, a published deadline, a residential retreat with a fixed bed count, or any immersion that historically fills. Horizon B exists because a one-month view surfaces retreats the month they happen, when they are full. Immersions in her categories open registration two to four months ahead.

For a run on the last Sunday of August, Horizon A is September and Horizon B covers September through December.

Horizon B entries lead with the deadline, not the event date. Where no deadline is published, say so explicitly and treat silent sellout as the risk — that is the normal failure mode for residential weekends, and "no published deadline" argues for booking early rather than waiting.

---

## Step 0 — the Chrome login pause

Meetup, Facebook Events, and Instagram require an authenticated session and block automated retrieval. Eventbrite is partially retrievable but returns far more when logged in. These four hold a large share of the local dance, music, Spanish, and outdoor-group activity that exists nowhere else, so the run is materially worse without them.

**Katherine works at a Mac she calls Mac 1, with Chrome signed in to all four.** This step hands control to her, waits, and then browses through her live session.

### 0a. Check for browser tools

Call `ToolSearch` with `browser chrome navigate screenshot`. Claude in Chrome is proxied through the device bridge and appears as `mcp__remote-devices__{server}__*` tools. If nothing comes back, the desktop is not connected or Chrome MCP is not running — go to 0d.

### 0b. Open the four sites

Open each in its own tab, in this order. Use the search URLs directly so the pages are already scoped when she looks at them:

1. `https://www.meetup.com/find/?location=us--de--Wilmington&distance=twentyFiveMiles`
2. `https://www.facebook.com/events/explore/`
3. `https://www.instagram.com/`
4. `https://www.eventbrite.com/d/de--wilmington/events/`

### 0c. Pause and hand over

Stop. Use `AskUserQuestion` — do not simply write a sentence and continue, because the browsing that follows depends on her having finished.

Front-load the context in the question itself, and name the surface and the click-path:

> Chrome on Mac 1 now has four tabs open: Meetup, Facebook Events, Instagram, Eventbrite. Sign in to any that show a login wall — the account chip is top-right on all four. Facebook may also ask you to dismiss a "See more events" interstitial before the explore feed renders.

Options:
- **Logged in, go** — proceed to the authenticated sweep
- **Skip the gated sites this month** — proceed to Step 1 with registry and open search only, and say plainly in the output which four sources were not searched
- **Chrome isn't open on Mac 1** — go to 0d

Do not proceed on silence. If no answer arrives, treat it as "skip" and label the output accordingly.

### 0d. Fallback when the bridge is unavailable

Do not retry and do not stall. Say once that Chrome on Mac 1 could not be reached, run the rest of the sweep, and mark the four gated sources as unsearched in the output's gaps section. Never let a missing browser silently shrink the calendar without saying so.

### 0e. The authenticated sweep

Once she confirms, work through the four sites. What to pull:

- **Meetup** — groups and events in these categories: line dance, social dance, contra and English country, ukulele and jams, Spanish conversation and intercambio, paddling and kayak, hiking and outdoors, tai chi and qigong, women 50+, newcomers and social. Capture the *group* as well as the event: a group that meets monthly is worth more than any single listing.
- **Facebook Events** — this is where Delaware's line dance scene actually lives. Named entities to check by hand each run: Delaware's Finest Line Dance Crew, Happy Feet Soul Line Dance Network, Country Line Dance Nights Wilmington, Downtown Newark Partnership, Historic Kennett Square, Riverfront Wilmington, Arden Gild Hall, Brandywine Creek State Park, Bay Venture Outfitters.
- **Instagram** — dance studios and venues post schedule changes to stories and grid before they update their websites. Check Take The Lead, BlueBallRoom, and any studio in the registry.
- **Eventbrite** — filter to Wilmington DE within 25 miles, then again for Kennett Square and West Chester PA.

Record every find with its URL so the output can cite it.

---

## Step 1 — load the spec

Read `references/life-design.md`. It contains the hard constraints, the capability taxonomy, the fixed weekly commitments, and the physical filters. Read `references/source-registry.md` for the verified sources, the confirmed school-year survivors, the phone numbers that unlock what the web cannot, and the dead ends not worth re-searching.

---

## Step 2 — sweep the registry

Work the registry systematically. For each source, fetch its current page and pull anything falling in Horizon A or B.

Registry entries carry a status. Update it as you go: a source that has produced nothing for three consecutive runs gets demoted; a source that goes 404 or shows a stale year gets marked dead with the date. Note these updates at the end of the output so the registry can be amended.

---

## Step 3 — open search for the gaps

After the registry, run open web search for what the registry does not cover: new studios, one-time festivals, seasonal series, newly published retreat calendars. Search each capability category separately rather than in one broad sweep.

Anything genuinely new and good gets proposed as a registry addition in the output.

---

## Step 4 — score

### Hard filters — a candidate failing any of these is dropped, not ranked lower

- **Drive time.** 20 minutes weekday, 40 minutes weekend, from Wilmington 19806. Retreats may reach 2–3 hours and are exempt.
- **Schedule collision** with a fixed commitment (see the life-design spec). Flag rather than drop when the collision depends on an hour that is not known.
- **Physical incompatibility** — see the drop list below.
- **Cost** — no expensive membership or high recurring cost unless the value is exceptional and stated.
- **Not beginner-welcoming**, or an event that assumes prior competence she does not have.

### Capability weighting — rank the survivors

Four branches, from her spec. Score each candidate on how many it serves and how directly:

- **Physical** — strength, mobility, balance, coordination, endurance, inflammation reduction
- **Social** — warmth, conversation, confidence, community, meeting new people, ease speaking with strangers
- **Professional** — consulting presence, presentation, storytelling, leadership, confidence in groups
- **Creative** — writing, music, voice, Spanish, movement

Weight upward, in this order:

1. **Recurring and school-year-compatible** beats one-time or summer-only. A weekday-morning class that vanishes in September is worth less than an evening class she can keep. Say so when the difference matters.
2. **Immersion format** beats scattered sessions. Two concentrated days beats eight one-hour classes; this is explicit in her spec.
3. **Serves more than one capability branch** in the same hour.
4. **Participation** beats spectating. Playing beats listening; dancing beats watching.
5. **Low sunk cost** — a $6 walk-in she can abandon without regret beats a $200 series that has to be justified.

### Physical filters — the drop list

Her constraints are a posterior cervical fusion C3–T1, knee limitations, and inflammation management. Drop or explicitly flag:

- Sustained or repeated **cervical extension** — looking up to track a ball, prone paddling in surf, overhead work
- **Rotational load through the neck** — partner spins, the contra swing, hustle, West Coast swing, salsa, bachata, Viennese waltz. She cannot spot with her head. English country dance and soul line dancing are the gentle ends of the same families.
- **Inversions** — headstand, shoulderstand, plow. Chair and therapeutic yoga structurally exclude them; vinyasa above difficulty 2 does not.
- **Asymmetric loaded carries** — carrying a canoe or kayak to the water
- **Repetitive impact** — running, jumping, stomps and kick-ball-changes at volume, hip hop
- **Heated rooms**, against inflammation management
- **Deep sustained knee flexion** — yin holds, long-held deep lunges
- **Strength duplication.** BSF covers strength three days a week. Do not recommend more of it.
- **Hard floors over concrete** are a knee cost. Fire halls, Legion halls, and school gyms sit on concrete; dance studios have sprung floors. Note the difference when it decides between two otherwise equal options.

None of this is medical advice, and no provider publishes a contraindication list. Every physical note is an assessment of the *modality* from its own description. Say so, and tell her to name the fusion to the instructor before a first session.

### The gate

Every surviving candidate must answer **"why is this worth my life?"** in two or three sentences of substance. Not a restatement of the event description — an argument about what capability it builds and why this particular offering earns the hours.

**If the answer is weak, drop it.** Then list what was dropped and why in a "dropped by the gate" section, so she can see it was considered rather than missed. That section is part of the deliverable, not an appendix.

---

## Step 5 — render

One self-contained HTML file. Arial, white background, austere, no decoration that does not carry information. Mobile-readable, because she often reads on a phone and acts at a desk.

**Color coding**, consistent with her Google My Maps layers:

| | |
|---|---|
| `#1F5C9E` Blue | Parks and outdoor movement |
| `#2E7D4F` Green | BSF and strength |
| `#B8860B` Yellow | Dance |
| `#B23A32` Red | Music and ukulele |
| `#6B3FA0` Purple | Spanish and cultural |
| `#0F8B8D` Turquoise | Water |
| `#C1660F` Orange | Retreats and workshops |

**Every event carries all of these fields.** A missing field is stated as missing, never omitted or guessed:

date · time · location and full address · drive time from 19806 · cost · beginner friendliness (quote the provider's own language where it exists) · recurring or one-time · whether it survives the school year · capability developed · physical demand with any neck or knee flag · whether Bonnie might enjoy it · confidence · source URL

**Confidence, on every entry:**

- **confirmed** — date, time, and price read off the organization's own current page
- **likely** — the pattern is established but the specific date was not visible
- **unverified** — needs a phone call before she goes

**Document sections, in order:**

1. Top 3 for the coming week
2. Top 3 for the month
3. Top quarterly immersion
4. Horizon B — decisions with deadlines, ordered by deadline
5. The month day by day, tickable, with fixed commitments shown in grey so the negative space is visible
6. What survives the school year
7. Calls that unlock the most — phone numbers, with the specific question to ask
8. Dropped by the gate
9. Gaps that could not be closed
10. Open questions

Deliver with `SendUserFile`. If a desktop is connected, also call `mcp__remote-devices__create_artifact` on the returned `file_uuid` so the calendar persists in her gallery rather than living only in one conversation.

---

## Step 6 — after she picks

She ticks, then tells you what she chose. Only then:

- Write the selected events to Google Calendar via the Google Calendar MCP. One event each, with the address in the location field so the phone can navigate, and the cost and the "call first" note in the description.
- Produce a CSV for Google My Maps import with columns: `Name, Address, Layer, Date, Time, Cost, Notes`. My Maps has no write API, so this is a manual import: **Google My Maps → open the map → Import → choose the CSV → set Layer as the styling column.** Roughly thirty seconds, once a month.

Do not write anything to her calendar before she has selected. The calendar is hers.

---

## Non-negotiables

- **Never invent an event, date, price, venue, or deadline.** A short list of real confirmed offerings is worth more than a long list of plausible ones. When a source cannot be reached, say which source and why.
- **Never assume an annual event repeats on the same weekend.** Verify the year on the page. Several local listings show a prior year without saying so.
- **Report dead ends.** A closed venue or a defunct group is useful — it stops her chasing it and it updates the registry.
- **Never collapse a "call first" into a recommendation.** If the county's page could not be read, the entry says call, and it says which number.
- **One question at a time** when anything needs her input, with the recommendation named. Never a paragraph of decisions.
- **Challenges to her thinking go in brackets.** Do not soften them and do not skip them; the gate depends on being willing to say an item is not worth her life.
