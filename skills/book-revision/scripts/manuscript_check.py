#!/usr/bin/env python3
"""manuscript_check.py — the mechanical pass over a manuscript snapshot.

Standard library only. It never edits anything. It reads one markdown snapshot of the
manuscript (the Working Copy exported to markdown) and writes one report that the revision
lanes and the integrator read before and after a pass.

What it extracts, per chapter and for the whole volume:
  * word counts, em-dash density per 1,000 words, sentence-length spread
  * hard-ban hits from tics-list.md (lexical bans T1–T9, enumerator openers T11,
    anaphora runs T16, "None of this means" T13)
  * editorial residue: [GAP], 【NOTE】, [PLACEHOLDER], [VERIFY], [DECIDE], "Questions for you",
    handoff paragraphs, provenance tags, change notes
  * chapter cross-references and whether the target chapter exists in the snapshot,
    plus vague back-references with no number
  * pseudonym and tracked-term counts by chapter (first appearance flagged)
  * candidate definitions of tracked terms ("X is", "what I mean by X", "I call this X")
  * passages that appear nearly verbatim in two chapters (shared eight-word runs)
  * endnote markers per chapter, in order, with reused or missing numbers

Usage
  python3 manuscript_check.py --in revision/manuscript/working-copy-2026-09-12.md \
                              --out revision/reports/check-2026-09-12.md
  python3 manuscript_check.py --in <snapshot> --find "the bathroom policy that opened this chapter"
  python3 manuscript_check.py --in <snapshot> --packets revision/packets/   # verify Find strings

The lists below (pseudonyms, tracked terms, bans) are the ones that matter for this book.
Change them here, not in prose elsewhere; the skills point at this file.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

# Current names per the ledger (R18): Peter is the greenhouse student, Paul is the son.
# Retired names stay in the list so their occurrences are found: Eli (greenhouse), Maya
# and Joe (Nancy and John), Mekhi (Malik), Kalima (Zara). Tyaire, Jaylen, Theo, Diego,
# Jair, Christian are the practice chapter's names, unconfirmed as pseudonyms (open item).
PSEUDONYMS = [
    "Angie", "Nancy", "John", "Toma", "Heidi", "Marcus", "Priya", "Malik", "Ben", "Brian",
    "Peter", "Paul", "James", "Eli", "Zara", "Kalima", "Noelle", "Gustov", "Lezir", "Karen",
    "Dana", "Cindy", "Mike", "Frieda", "Freida", "Jair", "Christian", "Maya", "Joe", "Mekhi",
    "Tyaire", "Jaylen", "Theo", "Diego",
]

TRACKED_TERMS = [
    "standing as a knower", "agency", "origination", "answerability", "answerable",
    "recognition", "legible", "legibility", "sense-making", "sense making",
    "meaning-making", "meaning making", "shared object", "critical aspect", "dialogism",
    "dialogic", "Variation Theory", "intellectual apprenticeship", "intellectual mentorship",
    "apprenticeship in learning", "dialogue partner", "guided participation",
    "intellectual authorship", "authorial agency", "epistemic agency",
    "reframing epistemic agency", "engaged agency", "effortful agency",
    "democratic agency", "pseudo-agency", "dysfunctional agency", "adjacent agency",
    "time-world", "chronotope", "double booking", "control of variation",
    "control of error", "two-tier", "internally persuasive", "identified regulation",
    "agentic engagement", "autonomy support", "lurking", "messing around", "geeking out",
    "zombification", "agency sickness", "effort porn", "epistemic gaslighting",
]

# Lexical hard bans from tics-list.md (T1–T9). Each is (label, regex, note).
BANS = [
    ("T1 genuine", r"\bgenuine(ly)?\b", ""),
    ("T2 quietly", r"\bquietly\b", "literal uses about an actual quiet room or person are fine"),
    ("T3 deeper", r"\b(runs|goes) deeper\b|\bdeeper truth\b", ""),
    ("T4 felt sense", r"\bfelt sense\b", ""),
    ("T5 masquerading", r"\bmasquerad", ""),
    ("T6 precisely", r"\bprecisely\b", "'be precise about' is allowed"),
    ("T7 meaningful", r"\bmeaningful(ly)?\b", "filler praise only; check each"),
    ("T8 AI vocabulary", r"\b(delve|crucial|pivotal|foster(s|ed|ing)?|robust|tapestry|testament|unpack|nuanced|holistic|transformative|invaluable)\b", ""),
    ("T8 figurative landscape/journey/navigate", r"\b(landscape|journey|navigat(e|es|ed|ing))\b", "figurative uses only"),
    ("T9 profundity phrases", r"hidden curriculum of passivity|quiet mismatch|the work is theirs|authors of their (own )?learning", ""),
    ("T13 none of this means", r"\bNone of this (means|is)\b", ""),
]

RESIDUE = [
    ("GAP", r"\[GAP"),
    ("NOTE", r"【NOTE"),
    ("PLACEHOLDER", r"\[PLACEHOLDER"),
    ("VERIFY", r"\[VERIFY|\[verify"),
    ("DECIDE", r"\[DECIDE|DECIDE:"),
    ("Questions for you", r"Questions for you"),
    ("provenance tag", r"\[(?:Y\+?|CO|C|draft|notes)\]"),
    ("change notes", r"Change notes\.|Endnote fixes still to make|Two chapters drafted from your notes|Drafted from your field notes|Replaces Chapter"),
    ("cite slot", r"\[cite:|edition/wording|confirm pages"),
    ("vignette slot", r"\[VIGNETTE"),
]

RE_CHAPREF = re.compile(r"\b(?:Chapter|Ch\.?)\s*\[?(\d+[AB]?|[AB])\]?\b")
RE_VAGUE = re.compile(r"(?i)\b(as (?:I|we) (?:argued|showed|noted|claimed|established|discussed|saw|said)|(?:the|in the) (?:next|previous|last) chapter|earlier in this (?:book|chapter)|two chapters from now|later in the book|opened this (?:book|chapter))\b")
RE_HEAD = re.compile(r"^#\s+\**(.+?)\**\s*$")
RE_NOTEMARK = re.compile(r"\[(\d{1,2}[a-z]?)\]|[⁰¹²³⁴⁵⁶⁷⁸⁹]+")
SUPERS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def split_chapters(text: str):
    """Return list of (title, body). A top-level heading starts a chapter. A heading whose
    text is only '---' inherits the next heading's title with '(heading lost)' appended."""
    lines = text.split("\n")
    chapters = []
    title, buf = "Front matter", []
    pending_lost = False
    for ln in lines:
        m = RE_HEAD.match(ln)
        if m:
            t = m.group(1).strip()
            if t.strip("-* ") == "":
                pending_lost = True
                chapters.append((title, "\n".join(buf)))
                title, buf = "(chapter heading lost)", []
                continue
            if title.startswith("(chapter heading lost)") and pending_lost and not buf:
                title = t + " (chapter heading lost above)"
                pending_lost = False
                continue
            chapters.append((title, "\n".join(buf)))
            title, buf = t, []
            pending_lost = False
        else:
            buf.append(ln)
    chapters.append((title, "\n".join(buf)))
    return [(t, b) for t, b in chapters if b.strip()]


def words(text: str):
    return re.findall(r"[A-Za-z0-9'’-]+", text)


def sentences(text: str):
    text = re.sub(r"\s+", " ", text)
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", text) if len(s.split()) > 1]


def chapter_number(title: str):
    m = re.search(r"Chapter\s*\\?\[?(\d+[AB]?|[AB])\\?\]?", title)
    return m.group(1) if m else None


def report(text: str, out_lines: list[str]):
    chapters = split_chapters(text)
    numbers = {chapter_number(t) for t, _ in chapters} - {None}
    P = out_lines.append

    P("# Manuscript check\n")
    P(f"Whole volume: {len(words(text)):,} words, {len(chapters)} top-level sections.\n")

    # ---- per-chapter table
    P("## Per chapter: size, dashes, rhythm, bans, residue\n")
    P("| Section | Words | Em dashes | per 1,000 | Sent. σ (words) | 30+ word sent. | Ban hits | Residue |")
    P("|---|---|---|---|---|---|---|---|")
    ban_detail, residue_detail = [], []
    for title, body in chapters:
        w = words(body)
        n = len(w) or 1
        dashes = body.count("—")
        sl = [len(s.split()) for s in sentences(body)]
        if sl:
            mean = sum(sl) / len(sl)
            sd = (sum((x - mean) ** 2 for x in sl) / len(sl)) ** 0.5
        else:
            sd = 0.0
        long_ = sum(1 for x in sl if x >= 30)
        hits = 0
        for label, rx, note in BANS:
            for m in re.finditer(rx, body):
                hits += 1
                ctx = body[max(0, m.start() - 60): m.end() + 60].replace("\n", " ")
                ban_detail.append((title, label, ctx))
        # enumerator openers and anaphora
        for m in re.finditer(r"(?m)^(?:\*\*)?(First|Second|Third|Fourth|Finally),", body):
            hits += 1
            ban_detail.append((title, "T11 enumerator opener", m.group(0)))
        sents = sentences(body)
        for i in range(len(sents) - 2):
            a, b, c = (s.split()[:2] for s in sents[i:i + 3])
            if a == b == c and len(a) == 2:
                ban_detail.append((title, "T16 anaphora run", " ".join(a) + " … ×3"))
        res = 0
        for label, rx in RESIDUE:
            for m in re.finditer(rx, body):
                res += 1
                ctx = body[m.start(): m.start() + 110].replace("\n", " ")
                residue_detail.append((title, label, ctx))
        P(f"| {title[:60]} | {n:,} | {dashes} | {dashes * 1000 / n:.1f} | {sd:.1f} | {long_} | {hits} | {res} |")
    P("")
    P("Reference rates from the voice guide: at most 3–4 em dashes per 1,000 words; sentence-length standard deviation around 13–15 words is hers, about 9 is the AI default; at least one 30+ word sentence per section.\n")

    P("## Hard-ban hits (tics-list T1–T16), with context\n")
    if not ban_detail:
        P("none\n")
    for title, label, ctx in ban_detail:
        P(f"- **{title[:40]}** · {label} · …{ctx}…")
    P("")

    P("## Editorial residue still inside the text\n")
    if not residue_detail:
        P("none\n")
    for title, label, ctx in residue_detail:
        P(f"- **{title[:40]}** · {label} · {ctx}")
    P("")

    # ---- cross references
    P("## Chapter cross-references\n")
    P("Each line: section → the chapter it points at → whether a chapter with that number exists in this snapshot.\n")
    for title, body in chapters:
        own = chapter_number(title)
        for m in RE_CHAPREF.finditer(body):
            tgt = m.group(1)
            ok = "exists" if tgt in numbers else "NO SUCH CHAPTER"
            ctx = body[max(0, m.start() - 70): m.end() + 40].replace("\n", " ")
            P(f"- {title[:40]} → Chapter {tgt} ({ok}) · …{ctx}…")
    P("")
    P("### Vague back- and forward-references (no number; check by hand)\n")
    for title, body in chapters:
        for m in RE_VAGUE.finditer(body):
            ctx = body[max(0, m.start() - 70): m.end() + 60].replace("\n", " ")
            P(f"- {title[:40]} · …{ctx}…")
    P("")

    # ---- pseudonyms
    P("## Pseudonyms by chapter (count; first appearance marked ★)\n")
    seen = set()
    P("| Section | " + " | ".join(PSEUDONYMS) + " |")
    P("|---|" + "---|" * len(PSEUDONYMS))
    for title, body in chapters:
        row = []
        for name in PSEUDONYMS:
            c = len(re.findall(rf"\b{name}\b", body))
            mark = ""
            if c and name not in seen:
                seen.add(name)
                mark = "★"
            row.append(f"{c}{mark}" if c else "")
        P(f"| {title[:40]} | " + " | ".join(row) + " |")
    P("")

    # ---- tracked terms and definitions
    P("## Tracked terms by chapter\n")
    P("| Term | " + " | ".join(t[:14] for t, _ in chapters) + " |")
    P("|---|" + "---|" * len(chapters))
    for term in TRACKED_TERMS:
        counts = [len(re.findall(rf"(?i)\b{re.escape(term)}\b", body)) for _, body in chapters]
        if sum(counts):
            P(f"| {term} | " + " | ".join(str(c) if c else "" for c in counts) + " |")
    P("")
    P("### Candidate definitions (sentences that define a tracked term)\n")
    P("A term should have one canonical home; every other occurrence is a pointer. Read each hit and decide which is the home.\n")
    for title, body in chapters:
        for s in sentences(body):
            for term in TRACKED_TERMS:
                if re.search(rf"(?i)(what I (?:mean|call|will call|’ll call|'ll call) (?:by )?(?:\*\*)?{re.escape(term)}|\b{re.escape(term)}\b (?:is|means|begins|names|refers to) |I call (?:it|this) (?:\*\*)?{re.escape(term)}|the term {re.escape(term)})", s):
                    P(f"- **{title[:36]}** · *{term}* · {s[:220]}")
                    break
    P("")

    # ---- duplicates
    P("## Passages shared between two sections (eight-word runs)\n")
    P("Pairs with the most shared runs first. Some repetition is deliberate return; each pair is a decision.\n")
    shingles = collections.defaultdict(set)
    for idx, (title, body) in enumerate(chapters):
        w = [x.lower() for x in words(body)]
        for i in range(len(w) - 7):
            shingles[" ".join(w[i:i + 8])].add(idx)
    pair_counts = collections.Counter()
    examples = {}
    for sh, idxs in shingles.items():
        if len(idxs) > 1:
            idl = sorted(idxs)
            for a in range(len(idl)):
                for b in range(a + 1, len(idl)):
                    pair_counts[(idl[a], idl[b])] += 1
                    examples.setdefault((idl[a], idl[b]), sh)
    for (a, b), c in pair_counts.most_common(40):
        if c < 3:
            break
        P(f"- {c} shared runs · **{chapters[a][0][:36]}** ↔ **{chapters[b][0][:36]}** · e.g. “{examples[(a, b)]}”")
    P("")

    # ---- note markers
    P("## Endnote markers per chapter, in order of appearance\n")
    for title, body in chapters:
        marks = []
        cut = re.search(r"(?m)^##\s+\**(?:Endnotes|Notes|Preface note)", body)
        body_only = body[:cut.start()] if cut else body
        for m in RE_NOTEMARK.finditer(body_only):
            v = m.group(1) if m.group(1) else m.group(0).translate(SUPERS)
            marks.append(v)
        if marks:
            dup = [k for k, v in collections.Counter(marks).items() if v > 1]
            P(f"- {title[:40]}: {', '.join(marks[:40])}{' …' if len(marks) > 40 else ''}" + (f" · reused: {dup}" if dup else ""))
    P("")


def locate(text: str, needle: str):
    chapters = split_chapters(text)
    pos = text.find(needle)
    if pos < 0:
        # tolerate curly/straight quote differences
        alt = needle.replace("'", "’").replace('"', "“")
        pos = text.find(alt)
    if pos < 0:
        return None
    run = 0
    for title, body in chapters:
        idx = body.find(needle) if body.find(needle) >= 0 else body.find(needle.replace("'", "’"))
        if idx >= 0:
            # section = nearest preceding ## heading inside the chapter
            sec = None
            for m in re.finditer(r"(?m)^##+\s+\**(.+?)\**\s*$", body[:idx]):
                sec = m.group(1)
            return title, sec, body[max(0, idx - 80): idx + len(needle) + 80].replace("\n", " ")
    return None


RE_ROW_ID = re.compile(r"^[a-z]+-[\w-]+-\d+$")


def packet_finds(body: str):
    """Find strings from a packet: the second cell of every table row whose first cell is a
    row ID (lane-chapter-NN), plus any 'Find: `...`' in prose. A cell may hold several
    backticked strings separated by semicolons; each is checked on its own."""
    finds = []
    for ln in body.splitlines():
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2 and RE_ROW_ID.match(cells[0]):
                finds.extend(re.findall(r"`([^`]+)`", cells[1]))
    finds.extend(re.findall(r"Find:\s*`([^`]+)`", body))
    return finds


def check_packets(text: str, packets_dir: Path, out: list[str]):
    """Every packet row carries a Find string in backticks; confirm each exists once."""
    out.append("# Packet Find-string check\n")
    for p in sorted(packets_dir.rglob("*.md")):
        body = p.read_text(encoding="utf-8")
        finds = packet_finds(body)
        bad = []
        for f in finds:
            n = text.count(f) + (text.count(f.replace("'", "’")) if "'" in f else 0)
            if n == 0:
                bad.append((f, "not found"))
            elif n > 1:
                bad.append((f, f"{n} matches; lengthen it"))
        out.append(f"- {p}: {len(finds)} Find strings, {len(bad)} problems")
        for f, why in bad:
            out.append(f"    - `{f}` → {why}")
    out.append("")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True, help="markdown snapshot of the manuscript")
    ap.add_argument("--out", dest="out", help="report path (markdown); prints to stdout if omitted")
    ap.add_argument("--find", help="locate a Find string: chapter, section, context")
    ap.add_argument("--packets", help="directory of lane packets; verify their Find strings")
    a = ap.parse_args()
    text = Path(a.inp).read_text(encoding="utf-8")
    if a.find:
        r = locate(text, a.find)
        print("NOT FOUND" if r is None else f"{r[0]} › {r[1]} › …{r[2]}…")
        return
    out: list[str] = []
    if a.packets:
        check_packets(text, Path(a.packets), out)
    else:
        report(text, out)
    s = "\n".join(out)
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(s, encoding="utf-8")
        print(f"wrote {a.out} ({len(s):,} chars)")
    else:
        sys.stdout.write(s)


if __name__ == "__main__":
    main()
