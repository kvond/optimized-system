#!/usr/bin/env python3
"""
pipeline_lint.py - consistency/drift validator for the feedback+VT pipeline.

The rules analogue of deck_lint.py / workflow_b_lint.py: a dumb deterministic
gate that enforces the MANIFEST invariants across every rule-carrying surface
(onboarding doc, grading-rules reference, deployed SKILL.md files). Two checks:
  BLOCKLIST  - retired/forbidden phrasings; any hit = drift FAIL (file+line)
  REQUIRED   - each canonical surface must contain the current rule

Single source of truth = pipeline_invariants.json (mirrors the MANIFEST
'Invariants that must NEVER drift' section). Update a rule THERE; this enforces
conformance everywhere. Run at session start (KICKOFF Step 0) and after any
rule/skill edit. Runs inside the Composio workbench (uses run_composio_tool);
pass a fetch_fn to run elsewhere.
"""
import re, json, os

def _default_fetch(drive_id):
    # workbench: run_composio_tool is a global; returns (data, err)
    d, e = run_composio_tool("GOOGLEDRIVE_DOWNLOAD_FILE",
                             {"fileId": drive_id, "mime_type": "text/plain"},
                             account="kvond12")  # noqa: F821
    if e:
        return None
    import requests
    return requests.get(d["data"]["downloaded_file_content"]["s3url"]).content.decode("utf-8")

def lint(invariants_path, fetch_fn=_default_fetch):
    inv = json.load(open(invariants_path))
    surfaces = inv["surfaces"]
    texts = {name: fetch_fn(fid) for name, fid in surfaces.items()}
    fails = []

    # BLOCKLIST - scan every surface
    for name, txt in texts.items():
        if txt is None:
            fails.append(("FETCH", name, 0, "could not fetch surface"))
            continue
        lines = txt.splitlines()
        for rule in inv["blocklist"]:
            pat = re.compile(rule["pattern"])
            for i, line in enumerate(lines, 1):
                if pat.search(line):
                    fails.append(("BLOCK:" + rule["id"], name, i,
                                  rule["note"] + "  >> " + line.strip()[:120]))

    # REQUIRED - each applies_to surface must contain the pattern
    for rule in inv["required"]:
        pat = re.compile(rule["pattern"], re.S)
        for name in rule["applies_to"]:
            txt = texts.get(name)
            if txt is None:
                fails.append(("REQ-FETCH:" + rule["id"], name, 0, "surface missing"))
            elif not pat.search(txt):
                fails.append(("MISSING:" + rule["id"], name, 0,
                              "required rule absent: " + rule["note"]))
    return fails

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "pipeline_invariants.json")
    fails = lint(path)
    if not fails:
        print("PASS - all surfaces consistent with invariants")
        sys.exit(0)
    print(f"FAIL - {len(fails)} drift issue(s):")
    for kind, name, line, msg in fails:
        loc = f"{name}:{line}" if line else name
        print(f"  [{kind}] {loc}\n      {msg}")
    sys.exit(1)
