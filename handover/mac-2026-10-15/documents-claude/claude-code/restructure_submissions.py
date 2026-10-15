#!/usr/bin/env python3
"""Bring every student submission to one shape:

    📥 Submissions 26-27 / <course> / <lesson> / <section> / <file>

Today a submission sits in one of seven shapes. The holding folder has three
spellings ("Submitted work — private", "… (F01)", "… (F04)") and the section
folder is sometimes there and sometimes not, so nothing can reliably say where
a student's work is — and a share cannot inherit evenly down a tree that
inconsistent.

Dry run by default: it prints every move and changes nothing. Pass --apply to
carry them out. It only ever moves files; it never deletes and never overwrites.

Section is decided by evidence, in this order:
  1. the section folder the file already sits in — where it is beats any list
  2. the roster, when the file has no section and the name matches exactly one
Anything it cannot settle is reported and left alone.
"""
import argparse
import csv
import os
import re
import shutil
import sys
from collections import defaultdict

DRIVE = os.path.expanduser(
    "~/Library/CloudStorage/GoogleDrive-katherine.vonduyke@redclay.k12.de.us/My Drive")
ROOT = os.path.join(DRIVE, "📥 Submissions 26-27")
ROSTER = os.path.expanduser("~/Documents/Claude/Claude code/student-rosters-2026-27.csv")
WORK = (".gslides", ".pptx", ".gdoc", ".docx", ".pdf")
HOLDING = re.compile(r"^Submitted work — private( \(\w+\))?$")
RESPONSES = re.compile(r"\(File responses\)$")
SECTION = re.compile(r"^[AB]\d\s+\w")          # "A2 Forensics", "B3 Anatomy"
SUBMISSION = re.compile(r"^s\.([a-z0-9'’-]+)\.([a-z0-9'’-]+)\s+—")


def norm(text):
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def roster_sections():
    """normalised first.last -> {sections}, from the teacher's own roster."""
    table = defaultdict(set)
    if not os.path.exists(ROSTER):
        return table
    for row in csv.DictReader(open(ROSTER, encoding="utf-8-sig")):
        course = row["Class"].strip()
        if not SECTION.match(course):
            continue
        for given in {row["First Name"], row.get("Nickname") or ""}:
            if given.strip():
                table[norm(given) + "." + norm(row["Last Name"])].add(course)
    return table


def plan():
    """Every submission, where it is, and where it belongs."""
    sections = roster_sections()
    moves, unresolved, already = [], [], 0
    for course in sorted(os.listdir(ROOT)):
        course_dir = os.path.join(ROOT, course)
        if not os.path.isdir(course_dir) or course.startswith("📥"):
            continue
        for lesson in sorted(os.listdir(course_dir)):
            lesson_dir = os.path.join(course_dir, lesson)
            if not os.path.isdir(lesson_dir):
                continue
            for base, dirs, names in os.walk(lesson_dir):
                for name in sorted(names):
                    if name == ".DS_Store" or not name.lower().endswith(WORK):
                        continue
                    source = os.path.join(base, name)
                    parts = os.path.relpath(base, lesson_dir).split(os.sep)
                    parts = [] if parts == ["."] else parts
                    # the section is whichever ancestor looks like one
                    found = [p for p in parts if SECTION.match(p)]
                    if found:
                        section = found[0]
                    else:
                        match = SUBMISSION.match(name)
                        key = norm(match[1]) + "." + norm(match[2]) if match else None
                        candidates = sections.get(key, set()) if key else set()
                        # only a course-appropriate, unambiguous roster hit counts
                        word = course.split()[-1].lower()
                        candidates = {c for c in candidates if word[:4] in c.lower()}
                        if len(candidates) != 1:
                            unresolved.append((source, sorted(candidates)))
                            continue
                        section = candidates.pop()
                    destination = os.path.join(lesson_dir, section, name)
                    if os.path.abspath(source) == os.path.abspath(destination):
                        already += 1
                    else:
                        moves.append((source, destination))
    return moves, unresolved, already


def show(moves, unresolved, already, apply):
    print(f"Submissions root: {ROOT}\n")
    if not os.path.isdir(ROOT):
        sys.exit("Submissions root not found — is Google Drive mounted?")
    shapes = defaultdict(int)
    for source, _ in moves:
        rel = os.path.relpath(os.path.dirname(source), ROOT).split(os.sep)
        shapes[" / ".join(rel[2:]) or "(lesson root)"] += 1
    print("SHAPES BEING NORMALISED")
    for shape, count in sorted(shapes.items(), key=lambda kv: -kv[1]):
        print(f"  {count:3}  <lesson> / {shape}")
    print(f"\n{len(moves)} file(s) to move · {already} already correct · "
          f"{len(unresolved)} need a decision\n")
    collisions = 0
    for source, destination in moves:
        flag = ""
        if os.path.exists(destination):
            flag = "   !! a file of this name is already there — skipped"
            collisions += 1
        print(f"  {os.path.basename(source)[:64]}")
        print(f"      from {os.path.relpath(os.path.dirname(source), ROOT)}")
        print(f"      to   {os.path.relpath(os.path.dirname(destination), ROOT)}{flag}")
    if unresolved:
        print("\nNEEDS A DECISION — no section on the file and the roster did not settle it")
        for source, candidates in unresolved:
            hint = ", ".join(candidates) if candidates else "no roster match"
            print(f"  {os.path.basename(source)[:64]}\n      in {os.path.relpath(os.path.dirname(source), ROOT)}  ({hint})")
    if collisions:
        print(f"\n{collisions} destination(s) already occupied. Those are skipped, never overwritten.")
    if not apply:
        print("\nDRY RUN — nothing was changed. Re-run with --apply to carry these out.")
    return collisions


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true",
                        help="actually move the files (default is a dry run)")
    args = parser.parse_args()
    moves, unresolved, already = plan()
    show(moves, unresolved, already, args.apply)
    if not args.apply:
        return
    done = skipped = 0
    for source, destination in moves:
        if os.path.exists(destination):
            skipped += 1
            continue
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.move(source, destination)
        done += 1
    print(f"\nMoved {done} file(s). Skipped {skipped}. Nothing deleted.")
    print("Empty holding folders are left in place — removing them stays your call.")


if __name__ == "__main__":
    main()
