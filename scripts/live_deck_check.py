#!/usr/bin/env python3
"""Check a LIVE Google Slides deck against the shipping standard.

`deck_lint` reads the built `.pptx` files. It has never read a live deck, so
it cannot see anything done in Google Slides - by Katherine, by a Gemini
enhancement, or by an API edit. This does that job.

What it is for: the feedback pipeline finds slides by matching literal
strings. Rewrite a heading and that slide stops being detected as its type,
and the grading prompts stop reading its boxes - silently, and not until
grading. Run this after any session of editing in Slides.

Input is the JSON body of a Slides `presentations.get`, one file per deck,
named `<key>.json` (for example `Cycle 09.json`). Fetch it with:

    GOOGLESLIDES_PRESENTATIONS_GET
      presentationId = <doc_id from docs/decks_live_ids.csv>
      fields = pageSize,slides(objectId,pageElements(objectId,shape(text(
               textElements(textRun(content,style(fontFamily,fontSize)))))))

Usage:  python3 live_deck_check.py <dir-of-json> [--csv docs/decks_live_ids.csv]
"""
import argparse
import csv
import glob
import json
import os
import re

# Section 7 of vt-skill. The feedback prompts and the type detector both
# match on these literally. A rewritten heading is a broken slide.
TYPE_STRINGS = {
    "3-Tier Question": ["Getting Started", "Working On It", "Mastery"],
    "Pattern Break": ["Pattern break"],
    "Build a Rule": ["Finish this sentence as a rule"],
    "What if": ["What if?"],
    "Continuity question": ["Keep going"],
    "Compensatory pair": ["Compensatory pair"],
    "Conflict case": ["Conflict case"],
}

# Slide types Katherine removed on 29 August. None should come back.
RETIRED = ["Then and Now", "Think → Write → Submit",
           "Turn your answer into a draft"]

GRADING = ["MARKER-INVENTORY", "NOTES:", "DRAFT:", "OPTIONAL:", "BANK:"]

# Calibrated against the built files, not against a reading of section 13.4.
# The builds set Arial on every run they style; Google resolves the unstyled
# runs to Calibri on import, on all 24 decks, so Calibri is the import's doing
# and not damage. The builds also carry 24pt and 26pt title runs, which are the
# aspect-opening slides and are correct. The first version of this script
# flagged both and returned 24 failures, every one of them false - which is how
# a check teaches its reader to ignore it.
FONT_OK = {"Arial", "Calibri"}
SIZE_CEILING_PT = 26.0
CHECKLIST_MARK = "Reopen this deck"


def runs(page):
    """Every text run on a page as (text, fontFamily, fontSize_pt)."""
    for el in page.get("pageElements", []):
        text = el.get("shape", {}).get("text")
        if not text:
            continue
        for te in text.get("textElements", []):
            tr = te.get("textRun")
            if not tr:
                continue
            style = tr.get("style", {})
            size = style.get("fontSize", {}).get("magnitude")
            yield tr.get("content", ""), style.get("fontFamily"), size


def page_text(page):
    return "".join(t for t, _, _ in runs(page))


def check(key, doc, expected_slides):
    slides = doc.get("slides", [])
    all_text = [page_text(s) for s in slides]
    joined = "\n".join(all_text)
    problems, notes = [], []

    if expected_slides and len(slides) != expected_slides:
        problems.append("slide count %d, expected %d" % (len(slides), expected_slides))

    size = doc.get("pageSize", {})
    w = size.get("width", {}).get("magnitude")
    h = size.get("height", {}).get("magnitude")
    if w and h and abs(w / h - 4 / 3) > 0.01:
        problems.append("page is not 4:3 (%.3f)" % (w / h))

    # Slide types still detectable
    found = {}
    for name, needles in TYPE_STRINGS.items():
        n = sum(1 for t in all_text if all(x in t for x in needles))
        if n:
            found[name] = n
    if "3-Tier Question" not in found:
        problems.append("no 3-Tier Question slide detected")

    for r in RETIRED:
        if r in joined:
            problems.append("retired slide type present: %s" % r)

    aspects = re.findall(r"Critical aspect[^:]*:\s*([^\n]+)", joined)
    aspects = [a.strip() for a in aspects if a.strip()]
    uniq = []
    for a in aspects:
        if a not in uniq:
            uniq.append(a)
    if len(uniq) != 2:
        problems.append("%d distinct 'Critical aspect:' labels, expected 2" % len(uniq))

    s1 = all_text[0] if all_text else ""
    n_block = s1.count("CRITICAL ASPECTS")
    if n_block == 0:
        problems.append("slide 1 has no CRITICAL ASPECTS block")
    elif n_block > 1:
        problems.append("slide 1 has %d CRITICAL ASPECTS blocks" % n_block)
    else:
        for a in uniq:
            if a not in s1:
                problems.append("slide 1 block does not carry the aspect %r" % a[:40])

    div = [i for i, t in enumerate(all_text) if "Day 3" in t]
    if not div:
        problems.append("no Day 3 divider found")
    else:
        if CHECKLIST_MARK in all_text[div[0]]:
            problems.append("Day 3 divider still carries the old checklist")

    grading = {g: joined.count("[[" + g) for g in GRADING}
    if grading["MARKER-INVENTORY"] == 0:
        notes.append("no grading markers yet (expected until that job runs)")

    bad_fonts, big = set(), []
    for i, s in enumerate(slides, 1):
        for text, font, sz in runs(s):
            if font and font not in FONT_OK:
                bad_fonts.add(font)
            if sz and sz > SIZE_CEILING_PT and text.strip():
                big.append((i, sz, text.strip()[:40]))
    if bad_fonts:
        problems.append("fonts other than Arial: %s" % ", ".join(sorted(bad_fonts)))
    if big:
        problems.append("%d run(s) above %gpt, first on slide %d at %gpt (%r)"
                        % (len(big), SIZE_CEILING_PT, big[0][0], big[0][1], big[0][2]))

    return problems, notes, found, grading


def fingerprint(doc):
    """What the deck looks like now, for comparison with a later run.

    The fixed rules above catch the breaks they were written for. This catches
    the ones they were not: an enhancement that swaps a font, resizes a
    heading, or rewrites a slide so its type string stops matching shows up as
    a difference from the last fingerprint, whatever the change was.
    """
    fonts, sizes, typed = {}, {}, {}
    texts = [page_text(s) for s in doc.get("slides", [])]
    for name, needles in TYPE_STRINGS.items():
        n = sum(1 for t in texts if all(x in t for x in needles))
        if n:
            typed[name] = n
    for s in doc.get("slides", []):
        for text, font, size in runs(s):
            if font:
                fonts[font] = fonts.get(font, 0) + 1
            if size:
                sizes[str(size)] = sizes.get(str(size), 0) + 1
    return {"slides": len(texts), "fonts": fonts, "sizes": sizes, "types": typed}


def compare(old, new):
    out = []
    if old["slides"] != new["slides"]:
        out.append("slide count %d -> %d" % (old["slides"], new["slides"]))
    for f in sorted(set(new["fonts"]) - set(old["fonts"])):
        out.append("new font appeared: %s" % f)
    for s in sorted(set(new["sizes"]) - set(old["sizes"]), key=float):
        out.append("new font size appeared: %spt" % s)
    for t in sorted(set(old["types"]) | set(new["types"])):
        a, b = old["types"].get(t, 0), new["types"].get(t, 0)
        if a != b:
            out.append("%s slides detected %d -> %d" % (t, a, b))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="directory of <key>.json files")
    ap.add_argument("--csv", default="docs/decks_live_ids.csv")
    ap.add_argument("--baseline", default="docs/live_baseline.json")
    ap.add_argument("--save-baseline", action="store_true")
    args = ap.parse_args()

    base = {}
    if os.path.exists(args.baseline):
        base = json.load(open(args.baseline))

    expected = {}
    if os.path.exists(args.csv):
        for row in csv.DictReader(open(args.csv)):
            try:
                expected[row["key"]] = int(row["new_slides"])
            except (KeyError, ValueError):
                pass

    clean = 0
    for f in sorted(glob.glob(os.path.join(args.path, "*.json"))):
        key = os.path.basename(f)[:-5]
        doc = json.load(open(f))
        doc = doc.get("data", doc)
        problems, notes, found, grading = check(key, doc, expected.get(key))
        fp = fingerprint(doc)
        if args.save_baseline:
            base[key] = fp
        elif key in base:
            problems += compare(base[key], fp)
        types = " ".join("%s×%d" % (k.split()[0], v) for k, v in sorted(found.items()))
        mark = "OK  " if not problems else "FAIL"
        print("%s %-10s %s" % (mark, key, types))
        for p in problems:
            print("       ! %s" % p)
        for n in notes:
            print("       - %s" % n)
        if not problems:
            clean += 1

    if args.save_baseline:
        json.dump(base, open(args.baseline, "w"), indent=1, sort_keys=True)
        print("\nbaseline written to %s" % args.baseline)

    print("\n%d clean, %d with findings" % (clean, len(glob.glob(
        os.path.join(args.path, "*.json"))) - clean))


if __name__ == "__main__":
    main()
