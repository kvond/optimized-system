#!/usr/bin/env python3
"""
render_reading.py  —  Roam-exported markdown -> clean reading prose.

Takes the faithful Roam export (the `source/` form) and produces the `writing/` form:
links removed, workflow tags stripped, components/block-refs/attributes/highlight markup
gone, outline bullets flattened to paragraphs. Headings, bold, and italics are kept.
Lossy by design — links don't survive — because this output is for *reading the
manuscript on GitHub*, not for reconstructing the graph.

Link handling (this is the fix over the original):
  - Aliased links  `[displayed text]([[Target Page]])`  -> `displayed text`
  - Plain markdown `[displayed text](anything)`          -> `displayed text`
  - Bare wikilinks `[[Phrase]]`                           -> `Phrase`
The first two are handled by RE_MDLINK BEFORE the wikilink pass; otherwise the inner
[[Target]] gets converted first and leaves a broken `[text](Target)` in the reading copy.

Inline content tags keep their words (`#[[double booking]]` -> "double booking"); workflow
tags are removed whole (`#near`, `#book`, `#[[parking lot]]`).

Usage:
  python3 scripts/render_reading.py --in source/ --out writing/     # whole folder
  python3 scripts/render_reading.py --in source/03-chapter-02.md    # to stdout
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

WORKFLOW_TAGS = {"next", "near", "book", "parkinglot", "parking", "todo",
                 "doing", "done", "waiting", "later", "someday"}

RE_ATTR = re.compile(r"^\s*[-*]?\s*[A-Za-z][\w /-]*::\s.*$")     # Roam attribute line
RE_COMPONENT = re.compile(r"\{\{.*?\}\}")                          # {{[[TODO]]}}, {{table}}
RE_BLOCKREF = re.compile(r"\(\([A-Za-z0-9_-]{6,16}\)\)")           # ((uid)) — UID-shaped only
RE_HIGHLIGHT = re.compile(r"\^\^(.+?)\^\^")                       # ^^text^^
RE_MDLINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")                  # [text](...) -> text
RE_TAG_BRACKET = re.compile(r"#\[\[([^\]]+)\]\]")                  # #[[phrase]]
RE_TAG_BARE = re.compile(r"(?<![\w/&?=.:~#-])#([A-Za-z][\w/-]*)")  # #word — skips URL #anchors
RE_WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")                      # [[phrase]]
RE_HEADING = re.compile(r"^#{1,6}\s")
RE_BULLET = re.compile(r"^\s*[-*]\s+")
RE_MULTISPACE = re.compile(r"[ \t]{2,}")
RE_SPACE_PUNCT = re.compile(r"\s+([,.;:!?])")


def _norm(tag: str) -> str:
    return re.sub(r"\s+", "", tag).lower()


def _tag_bracket(m: re.Match) -> str:
    inner = m.group(1)
    return "" if _norm(inner) in WORKFLOW_TAGS else inner


def _tag_bare(m: re.Match) -> str:
    word = m.group(1)
    return "" if _norm(word) in WORKFLOW_TAGS else word


def render(text: str) -> str:
    out_lines: list[str] = []
    for raw in text.splitlines():
        if RE_ATTR.match(raw):
            continue                                  # drop attribute lines
        is_heading = bool(RE_HEADING.match(raw))
        line = raw if is_heading else RE_BULLET.sub("", raw)  # flatten bullets

        line = RE_COMPONENT.sub("", line)
        line = RE_BLOCKREF.sub("", line)
        line = RE_HIGHLIGHT.sub(r"\1", line)
        line = RE_MDLINK.sub(r"\1", line)             # aliased + plain markdown links
        line = RE_TAG_BRACKET.sub(_tag_bracket, line)
        line = RE_TAG_BARE.sub(_tag_bare, line)
        line = RE_WIKILINK.sub(r"\1", line)

        line = RE_MULTISPACE.sub(" ", line)
        line = RE_SPACE_PUNCT.sub(r"\1", line).strip()

        if is_heading:
            out_lines.append("")
            out_lines.append(line)
            out_lines.append("")
        elif line:
            out_lines.append(line)
            out_lines.append("")                      # blank line = paragraph break

    cleaned: list[str] = []
    for ln in out_lines:
        if ln == "" and (not cleaned or cleaned[-1] == ""):
            continue
        cleaned.append(ln)
    return "\n".join(cleaned).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Render Roam markdown to clean reading prose.")
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", default=None)
    args = ap.parse_args()

    src = Path(args.inp)
    if src.is_dir():
        dst = Path(args.out or "writing")
        dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.glob("*.md")):
            (dst / f.name).write_text(render(f.read_text()))
        print(f"Rendered {len(list(src.glob('*.md')))} file(s) -> {dst}/")
    else:
        result = render(src.read_text())
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(result)
            print(f"Rendered -> {args.out}")
        else:
            print(result)


if __name__ == "__main__":
    main()
