#!/usr/bin/env python3
"""
roam_bulk_ops.py — apply the zettel-registration handoff from the 2026-07-30 distill
scan WITHOUT going through the Roam MCP (which hangs on batch writes mid-session).

It writes through Roam's backend API — the same channel build_inventory.py reads from —
so it cannot hang the way roam_process_batch_actions does. One page at a time, idempotent,
dry-run by default.

WHAT IT DOES
  For each of the 34 Group-A zettels (see REVIEW-zettel-registration-2026-07-30.md), it
  ensures the registry backlink `Index:: [[🌿 Evergreen Notes]]` exists on the page:
    - already registered            -> skip
    - has a `Meta::` block          -> add the Index:: line under it
    - no `Meta::` block             -> mint `Meta::`, then add Index:: under it
  It does NOT fill Provenance:: / Origin:: (those need your judgment) and it never
  touches the 4 Group-B anomalies.

TOKENS  (Roam -> Settings -> Graph -> API Tokens -> New API Token)
  Reads (the idempotency check) use your existing read token:
      .roam_token   in this folder, or  ROAM_API_TOKEN=...
  Writes (--apply) need an EDIT-scoped token — the read token will 401 on write:
      ROAM_EDIT_TOKEN=...   (scope Edit)

USAGE
  # 1. dry run — prints the exact plan, writes nothing (read token is enough):
  python3 roam_bulk_ops.py

  # 2. apply — needs the edit token:
  ROAM_EDIT_TOKEN=roam-edit-xxxx python3 roam_bulk_ops.py --apply

SAFETY
  Adding a backlink is reversible and loses no distinction (chapter-bank auto-apply tier),
  so no graph export is required first. Still: run the dry-run, eyeball the plan, then --apply.
"""
import argparse, json, os, random, string, sys, time, urllib.request, urllib.error

API_BASE = "https://api.roamresearch.com"
GRAPH = os.environ.get("ROAM_GRAPH", "kvond")
REGISTRY = "Index:: [[🌿 Evergreen Notes]]"
EVERGREEN = "🌿 Evergreen Notes"

# Group A — register (34). uid -> title. From REVIEW-zettel-registration-2026-07-30.md.
TARGETS = {
    "w0YRFWyr0": "📇 Adjacency is developmental",
    "kgy2Q5CLN": "📇 What a teacher cannot see, a teacher cannot support",
    "k4jjJ7YJo": "📇 Marcus didn't need rebuilding; he needed translation",
    "edmnP3_yO": "📇 AI is a presence-augmenter, not a teacher replacement",
    "5Gjv-yPjd": "📇 AI trained on correct outputs will replicate the misreading of high-poverty students",
    "Wt7OGplmg": "📇 The teacher curates the object and retains evaluation while protecting the knower-stance",
    "3HWzVky4g": "📇 Under-prescription can exhaust curiosity as surely as over-prescription",
    "IlCYwOG64": "📇 The Germantown gap is the arithmetic of exhaustion, not a failure of parental love",
    "AjDW96_jQ": "📇 The school's engagement measure counts only engagement flowing toward the teacher's frame",
    "KaZlVd_aX": "📇 Prepare the play around the critical aspect rather than wait for interest to appear",
    "XTivY-9BQ": "📇 Nancy — epistemic agency (coin flowers)",
    "L62rRTiB4": "📇 Agency is a capacity built from the outside in, not a personality trait",
    "2evDOtfG8": "📇 A well-built question generates interest; interest is an output of design, not a precondition",
    "g1bLmDssm": "📇 Inquiry is a consequence of teaching, not its precondition",
    "dLjHYl0FQ": "📇 Being responsible for one's words means one's identity and self are present in them",
    "xpRI62PA6": "📇 Reading the room for knowers is a learnable skill, not a metaphysical gift",
    "qZpJd04cE": "📇 Structure that hands itself over — the developmental warrant",
    "pS_aF6-kF": "📇 The teacher's agency is also at stake and develops through these encounters",
    "50h8hWvs2": "📇 Authorial and epistemic agency are orthogonal, not sequential — they can coexist but need not",
    "0IDhT3nVi": "📇 The agency taxonomy is a perceptual instrument, not a production rubric",
    "WLXpvsk7g": "📇 Cultural capital is the experiences school expects; wealthy children can lack it too",
    "0Xo0g4DlZ": "📇 Agency lives in the held tension between centripetal curriculum and centrifugal student purposes",
    "EOsdpeh28": "📇 Biesta names the event, Bakhtin the medium, the taxonomy the terrain",
    "GoOo9gdZp": "📇 Unread thinking is invisible; misread thinking is seen as its opposite",
    "L3xgscROU": "📇 The book is diagnostic before it is prescriptive",
    "tKmlRGrGC": "📇 A property of a relation exists only in the relation, so stripping context strips the thing itself",
    "KVUlBw0I1": "📇 The five movements are not a recipe but the conditions under which the teacher's perceptual capacity sustains itself",
    "4dcHyt1kO": "📇 A student's originating move is legitimate at its source, which removes two gates the field erected — intentionality and teacher perception",
    "66wKZFjmc": "📇 Even a few experiences of being seen matter, most of all in high-poverty schools",
    "gGIwtL1tg": "📇 The progressive model suppresses origination; naive progressivism presupposes it; neither cultivates it",
    "NDq96NrY-": "📇 None of the agency forms is a goal; when a teacher perceives how a student is already engaging, they can support it to emerge and become answerable to others",
    "ts7MpqFMl": "📇 The equity injury is double: first the misreading, then the substitution",
    "Caz8piXo1": "📇 The seams are the perceptual frontier where a teacher feels a difference but cannot name it — where mētis operates",
    "8PZPlzbUL": "📇 Autonomy support works only for students who already have authorship (the Patall backfire)",
}

# Group B — flagged, never touched by this script (here for the record only).
FLAGGED = {
    "c_tBTzTLB": "📇 Projects",
    "dECUV6a54": "📇 QUE — …",
    "6UkBW8y7H": "📇 QUE — Is agency the book's aim, or a symptom of intellectual authorship whose real aim is answerability?",
    "0-mfN-DBE": "📇 QUE — Is withholding he teacher's opinion respect, or its own evasion?",
}


def _request(url, token, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("x-authorization", "Bearer " + token)
    return urllib.request.urlopen(req, timeout=60)


def _post(path, token, payload, _depth=0):
    """POST to a Roam backend endpoint, following its peer redirect (307/308)."""
    url = f"{API_BASE}{path}"
    try:
        resp = _request(url, token, payload)
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        if e.code in (307, 308) and _depth < 5:
            loc = e.headers.get("Location")
            if loc:
                resp = _request(loc, token, payload)
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw.strip() else {}
        raise


def query(token, q, args):
    return _post(f"/api/graph/{GRAPH}/q", token, {"query": q, "args": args}).get("result", [])


def write_action(token, action):
    return _post(f"/api/graph/{GRAPH}/write", token, action)


PAGE_BLOCKS_Q = ('[:find ?buid ?s :in $ ?puid :where '
                 '[?p :block/uid ?puid] [?b :block/page ?p] '
                 '[?b :block/string ?s] [?b :block/uid ?buid]]')


def new_uid():
    aln = string.ascii_letters + string.digits
    return "".join(random.choice(aln) for _ in range(9))


def plan_for_page(read_token, uid):
    """Return (status, meta_uid). status in {registered, has-meta, no-meta, missing}."""
    rows = query(read_token, PAGE_BLOCKS_Q, [uid])
    if not rows:
        return "missing", None
    meta_uid = None
    for buid, s in rows:
        if EVERGREEN in s:
            return "registered", None
        if s.strip().startswith("Meta::") and meta_uid is None:
            meta_uid = buid
    return ("has-meta", meta_uid) if meta_uid else ("no-meta", None)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true",
                    help="perform the writes (needs ROAM_EDIT_TOKEN). Default: dry run.")
    ap.add_argument("--i-understand-these-are-stubs", action="store_true",
                    help="override the 2026-07-30 hold (see REVIEW file). Required with --apply.")
    args = ap.parse_args()

    # HOLD (2026-07-30): inspection showed all 34 targets are title-only harvest stubs
    # (empty, or just a `Processed:: [[date]]` stamp) — NOT built-out zettels. Registering
    # them would file hollow shells into 🌿 Evergreen Notes. Do not --apply until Katherine
    # adjudicates. Override only if she has decided the title-as-claim is sufficient.
    if args.apply and not args.i_understand_these_are_stubs:
        sys.exit("HOLD: targets are harvest stubs, not built-out zettels (see "
                 "REVIEW-zettel-registration-2026-07-30.md). Refusing to register hollow "
                 "notes. Pass --i-understand-these-are-stubs to override.")

    here = os.path.dirname(os.path.abspath(__file__))
    read_token = os.environ.get("ROAM_API_TOKEN")
    if not read_token:
        tok_path = os.path.join(here, ".roam_token")
        # .roam_token lives one level up in the answerable-tag-pass folder
        if not os.path.exists(tok_path):
            tok_path = os.path.join(os.path.dirname(here), ".roam_token")
        if os.path.exists(tok_path):
            read_token = open(tok_path, encoding="utf-8").read().strip()
    if not read_token:
        sys.exit("ERROR: no read token. Set ROAM_API_TOKEN or put .roam_token in the folder.")

    edit_token = os.environ.get("ROAM_EDIT_TOKEN")
    if args.apply and not edit_token:
        sys.exit("ERROR: --apply needs an EDIT-scoped token in ROAM_EDIT_TOKEN "
                 "(the read token cannot write). Roam -> Settings -> Graph -> API Tokens, scope Edit.")

    print(f"{'APPLY' if args.apply else 'DRY-RUN'} — {len(TARGETS)} target zettels, graph '{GRAPH}'\n")
    counts = {"registered": 0, "will-add": 0, "will-mint-meta": 0, "missing": 0, "done": 0, "error": 0}

    for uid, title in TARGETS.items():
        try:
            status, meta_uid = plan_for_page(read_token, uid)
        except Exception as e:
            counts["error"] += 1
            print(f"  ERROR  {uid}  {title[:60]} :: {e}")
            continue

        short = title[:70]
        if status == "registered":
            counts["registered"] += 1
            print(f"  skip   {uid}  already registered   {short}")
            continue
        if status == "missing":
            counts["missing"] += 1
            print(f"  MISS   {uid}  page not found       {short}")
            continue

        if status == "has-meta":
            counts["will-add"] += 1
            print(f"  add    {uid}  Index:: under Meta:: {short}")
            if args.apply:
                write_action(edit_token, {"action": "create-block",
                    "location": {"parent-uid": meta_uid, "order": "last"},
                    "block": {"string": REGISTRY}})
                counts["done"] += 1
        else:  # no-meta
            counts["will-mint-meta"] += 1
            print(f"  mint   {uid}  Meta:: + Index::     {short}")
            if args.apply:
                mu = new_uid()
                write_action(edit_token, {"action": "create-block",
                    "location": {"parent-uid": uid, "order": "first"},
                    "block": {"string": "Meta::", "uid": mu}})
                write_action(edit_token, {"action": "create-block",
                    "location": {"parent-uid": mu, "order": "last"},
                    "block": {"string": REGISTRY}})
                counts["done"] += 1
        if args.apply:
            time.sleep(0.3)  # gentle on the API

    print("\nsummary:", json.dumps(counts))
    if not args.apply:
        print("dry run only — nothing written. Re-run with --apply and ROAM_EDIT_TOKEN to execute.")
    print(f"\n{len(FLAGGED)} Group-B anomalies left untouched (see the review file).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
