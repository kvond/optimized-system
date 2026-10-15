---
name: book-ops-inventory-rebuild
description: WEEKLY (Sun 3a) rebuild of the book-ops Roam inventory.json used by the on_create_check mint gate. Reduced from nightly Aug 11 2026 to cut recurring runs.
---

Rebuild the book-ops Roam graph inventory that the mint gate (on_create_check) runs against. This is a maintenance refresh only — it makes NO changes to the Roam graph. The Roam API graph name is "kvond".

Location: the user's connected workspace folder named `answerable-tag-pass`. Inside it is `book-ops-scripts/` containing `build_inventory.py`, `on_create_check.py`, and `vocabulary.json`. Resolve that folder to this session's actual mount path (do not hardcode a /sessions/... prefix from any prior run).

PREFERRED PATH (off-context, complete graph — always try this first):
1. Read the Roam read-token from the file `.roam_token` in the `answerable-tag-pass` folder (one line, the token only).
2. If it exists and is non-empty, run in bash:
   `ROAM_API_TOKEN="<token contents>" ROAM_GRAPH=kvond python3 <path>/book-ops-scripts/build_inventory.py --out <path>/book-ops-scripts/inventory.json`
   build_inventory.py calls Roam's backend API itself (header X-Authorization: Bearer <token>) and assembles the full ~2,000-page graph inside the script, so the page data never enters the conversation context. Do NOT pull page lists through the Roam MCP on this path.

FALLBACK (only if `.roam_token` is missing/empty, or api.roamresearch.com is unreachable): pull just the node + concept layer through the Roam MCP — the CLM/EVD/QUE node titles plus their backlink counts and child-block counts. Use `clojure.string/starts-with?` on the title to scope (the Datalog `#"regex"` reader tag is NOT supported by this MCP). Write the raw result rows to `pages.json`, `backlinks.json`, `children.json` in a temp dir, then assemble: `python3 <path>/book-ops-scripts/build_inventory.py --from-mcp <tempdir> --out <path>/book-ops-scripts/inventory.json`. Do NOT pull all ~2,000 pages through context; if you land here, the inventory is node-slice-only — say so.

AFTER BUILDING: run one sanity check — `python3 <path>/book-ops-scripts/on_create_check.py --title "student agency" --inventory <path>/book-ops-scripts/inventory.json --vocab <path>/book-ops-scripts/vocabulary.json` — and confirm it returns a verdict without error.

OUTPUT: a single short report line — the page count, whether it was the full (token) pull or the node-slice (MCP fallback) pull, the output path, and the sanity-check verdict. If the token file is absent, note that the user still needs to create `.roam_token` (Roam → Settings → Graph → API Tokens → New API Token, scope Read) for the complete pull.