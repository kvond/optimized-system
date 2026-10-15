#!/usr/bin/env python3
"""
check_consistency.py  —  Job 1 extractor (deterministic; Claude adjudicates).

Walks the manuscript and pulls out the raw material a consistency pass needs, into one
report. It does NOT judge and it NEVER edits the manuscript — it surfaces:
  - chapter cross-references ("Ch. 4", "Chapter 2") and whether the target chapter exists,
  - vague back-references ("as I argued earlier") with no number, for manual check,
  - every occurrence of tracked terms (anchor students, the stool, coined concepts) with
    context, grouped so Claude can eyeball whether usage stays consistent.

Claude then reads the report and flags the judgment calls (does the cross-ref's claim
actually live where it points; is "double booking" used consistently with its Ch.5
definition). Script extracts; Claude decides; you approve.

Usage:
  python3 check_consistency.py --in writing/ --out consistency_report.md
  python3 check_consistency.py --in writing/ --terms "Abraham,Aliyah,double booking,agency"
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

DEFAULT_TERMS = ["Abraham", "Aliyah", "double booking", "agency", "perception", "ecology"]

RE_CHAPREF = re.compile(r"(?i)\b(?:chapter|ch\.?)\s*(\d+)\b")
RE_VAGUE = re.compile(r"(?i)\bas (?:i|we) (?:argued|showed|noted|claimed|established|discussed|saw)\b")
RE_HEADCH = re.compile(r"(?i)\b(?:chapter|ch\.?)\s*(\d+)\b")


def chapter_of(path: Path, text: str) -> int | None:
    """Best-effort: chapter number from the first heading, else from the filename."""
    first = next((l for l in text.splitlines() if l.startswith("#")), "")
    m = RE_HEADCH.search(first) or RE_HEADCH.search(path.stem)
    return int(m.group(1)) if m else None


def context(line: str, term: str, width: int = 90) -> str:
    i = line.lower().find(term.lower())
    if i < 0:
        return line.strip()[:width]
    start = max(0, i - width // 2)
    end = min(len(line), i + len(term) + width // 2)
    return ("…" if start else "") + line[start:end].strip() + ("…" if end < len(line) else "")


def scan(files: list[Path], terms: list[str]) -> dict:
    present_chapters: dict[int, str] = {}
    texts: dict[Path, str] = {}
    for f in files:
        t = f.read_text()
        texts[f] = t
        ch = chapter_of(f, t)
        if ch is not None:
            present_chapters[ch] = f.name

    crossrefs, vague = [], []
    term_hits: dict[str, list[tuple[str, int, str]]] = {t: [] for t in terms}

    for f, t in texts.items():
        for ln_no, line in enumerate(t.splitlines(), 1):
            for m in RE_CHAPREF.finditer(line):
                target = int(m.group(1))
                crossrefs.append((f.name, ln_no, m.group(0), target,
                                  target in present_chapters))
            if RE_VAGUE.search(line):
                vague.append((f.name, ln_no, line.strip()[:120]))
            for term in terms:
                if re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE):
                    term_hits[term].append((f.name, ln_no, context(line, term)))
    return {"present_chapters": present_chapters, "crossrefs": crossrefs,
            "vague": vague, "term_hits": term_hits}


def report(data: dict, terms: list[str]) -> str:
    L = ["# Consistency extract",
         "_Raw material for review. No judgments made, nothing edited._", ""]

    pc = data["present_chapters"]
    L.append(f"Chapters detected: {', '.join(str(c) for c in sorted(pc)) or 'none'}")
    L.append("")

    L.append("## Cross-references")
    if data["crossrefs"]:
        for fn, ln, txt, target, ok in data["crossrefs"]:
            flag = "" if ok else "  ⚠️ target chapter not found"
            L.append(f"- `{fn}:{ln}` → \"{txt}\" (Ch. {target}){flag}")
    else:
        L.append("- none found")
    L.append("")

    L.append("## Vague back-references (no chapter number — verify by hand)")
    if data["vague"]:
        for fn, ln, txt in data["vague"]:
            L.append(f"- `{fn}:{ln}` — {txt}")
    else:
        L.append("- none found")
    L.append("")

    L.append("## Tracked-term usage (eyeball for consistent meaning)")
    for term in terms:
        hits = data["term_hits"][term]
        L.append(f"### {term} — {len(hits)} occurrence(s)")
        for fn, ln, ctx in hits:
            L.append(f"- `{fn}:{ln}` — {ctx}")
        L.append("")
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract cross-refs and tracked-term usage.")
    ap.add_argument("--in", dest="inp", required=True, help="manuscript file or folder")
    ap.add_argument("--out", dest="out", default=None)
    ap.add_argument("--terms", default=",".join(DEFAULT_TERMS))
    args = ap.parse_args()

    terms = [t.strip() for t in args.terms.split(",") if t.strip()]
    src = Path(args.inp)
    files = sorted(src.glob("*.md")) if src.is_dir() else [src]

    out = report(scan(files, terms), terms)
    if args.out:
        Path(args.out).write_text(out)
        print(f"Wrote {args.out} ({len(files)} file(s), {len(terms)} term(s)).")
    else:
        print(out)


if __name__ == "__main__":
    main()
