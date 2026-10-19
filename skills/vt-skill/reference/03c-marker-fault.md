<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 3c. The marker fault, and the `markers present:` line (added 2026-08-18)

Katherine hit this while the Concept Bank was being built. An ellipsis broke the
linter while the grader kept working. Nothing looked wrong. That is the version of
this bug that survives longest, so the rule below is now a standing check.

**The rule. Read the `markers present:` line on every build. Do not trust a
clean-looking deck.**

### Why the two scripts disagree

They match markers by different mechanisms, and the mechanisms fail on different
characters.

| | `extract_and_grade.py` | `deck_lint.py` |
|---|---|---|
| How | Plain substring, lowercased | Compiled regex, `re.I` |
| What if | `"what if?" in text` **or** `^\s*what[- ]if\b` at line start | `what if\?` only |
| Critical aspect | `Critical aspect:\s*(...)` | `critical aspect\s*:` |

The grader carries a second, looser test for the What if slide that matches
`what if` or `what-if` at the start of a line with no question mark. The linter has
no such fallback. A slide that reads `What if…` with an ellipsis in place of the
question mark therefore still classifies as `what_if` in the grader and vanishes
from the linter's marker set. The two counts then differ by one, and nothing on the
slide looks wrong, because an ellipsis is a plausible thing to type.

### Why a clean report hides it

`deck_lint.py` sorts its output into `errors`, `warnings`, and `notes`, and then
prints `clean — no tier/marker/color problems found` when there are no errors and
no warnings. A missing marker goes into **`notes`**, with the text
`diagnostic markers not found in deck: [...] (fine if this arc doesn't use them;
flagged for eyeball)`. So the deck prints `clean` on the last line while a note two
lines above says a marker is gone. The word `clean` is not a verdict on the markers.

### What to do on every build

1. Read the `markers present:` line. It must list every marker the deck actually
   uses: `Critical aspect`, `Pattern break`, `Build-a-rule`, and `What-if` for a
   normal two-aspect cycle.
2. Read the `notes` block even when the last line says `clean`.
3. Compare `diagnostic slides:` from the linter against the diagnostic count from
   the grader. See §7.1. A difference of one is this fault or the exclusion-list
   fault, not noise.
4. Where a marker is missing, find the slide and look at the punctuation before you
   change anything. The usual cause is a typographic character standing in for an
   ASCII one: `…` for `?`, a curly apostrophe, a non-breaking space, an en dash for
   a hyphen in `what-if`.

### The general rule

A marker string is matched by machine, not read by a person. Type it in ASCII,
verbatim, exactly as §7 gives it. Do not let a smart-punctuation pass, a paste from
a word processor, or a well-meant tidy of the wording touch a marker string. If a
marker has to change, it changes in §7, in both scripts, and in every deck, in one
pass — the same discipline as the exclusion list in §7.1.

[Challenge: the deeper fault is that two scripts implement the same concept twice,
by different means, and the only thing keeping them aligned is a comment and a
habit. One shared module holding the marker definitions, imported by both, removes
this whole class of bug. That is a change to the scripts, not to a deck, and §11
says not to rewrite them casually — but it is worth doing once, deliberately, and
it would retire both §3c and half of §7.1.]
