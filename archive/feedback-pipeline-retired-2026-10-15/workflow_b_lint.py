#!/usr/bin/env python3
"""
workflow_b_lint.py — deterministic fidelity check for Workflow B emails.

The Workflow-B analogue of deck_lint.py. Given a composed email and its inputs,
returns a list of failures; an email with zero failures is safe to draft.
Wired as Step 4.5 of 08-workflow-b-SKILL.md: run BEFORE GMAIL_CREATE_EMAIL_DRAFT.
Never draft an email that fails.

Checks:
  1. every diagnostic-slide question present verbatim in the body
  2. praise quote is a substring of the student's own answer text
  3. subject exactly 'Your work on <Lesson> - what to rewrite' (em dash)
  4. recipient 's.first.last@redclay.k12.de.us', hyphens stripped
  5. no rubric score / square color assigned by B (tier LABELS allowed)
  6. rewrite instruction + DRAFTS submission line present
"""
import re, unicodedata

REDCLAY = "@redclay.k12.de.us"
RUBRIC_COLORS = ("\U0001F7E5", "\U0001F7E8", "\U0001F7E9")  # red/yellow/green SQUARES
RUBRIC_SCORE = re.compile(r"\b(conceptual|depth|writing)\s*[:=]\s*", re.I)

def _norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()

def lint_email(*, subject, body, recipient, lesson, student_answers,
               slide_questions, praise_quote=None):
    fails = []
    nbody = _norm(body)

    for q in slide_questions:                                   # 1
        if _norm(q) not in nbody:
            fails.append("MISSING QUESTION verbatim: %r" % q[:70])

    if praise_quote:                                            # 2
        pq = _norm(praise_quote)
        if pq not in nbody:
            fails.append("PRAISE QUOTE not in body")
        if pq not in _norm(" ".join(student_answers)):
            fails.append("PRAISE QUOTE not a substring of student's answer: %r" % praise_quote[:60])
    else:
        if not re.search(r"missed your work|get your thinking down", body, re.I):
            fails.append("Blank deck but no warm line and no valid quote")

    exp = "Your work on %s \u2014 what to rewrite" % lesson      # 3
    if _norm(subject) != _norm(exp):
        fails.append("SUBJECT mismatch: %r != %r" % (subject, exp))

    if not re.fullmatch(r"s\.[a-z]+\.[a-z]+" + re.escape(REDCLAY), recipient.strip(), re.I):  # 4
        fails.append("RECIPIENT not s.first.last%s (hyphens stripped): %r" % (REDCLAY, recipient))

    for c in RUBRIC_COLORS:                                     # 5
        if c in body:
            fails.append("RUBRIC COLOR square present (B must not assign rubric colors)")
    if RUBRIC_SCORE.search(body):
        fails.append("RUBRIC SCORE pattern present (scoring is B2's job)")

    if not re.search(r"rewrite your answer", body, re.I):       # 6
        fails.append("Missing rewrite instruction")
    if "DRAFTS" not in body:
        fails.append("Missing DRAFTS submission line")

    return fails


if __name__ == "__main__":
    import sys, json
    p = json.load(sys.stdin)
    f = lint_email(**p)
    if f:
        print("FAIL:")
        for x in f: print("  -", x)
        sys.exit(1)
    print("PASS")
