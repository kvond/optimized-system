# On-demand DOE source check

This operator tool reads only the fixed approved anonymous DOE Frontline location filter. It does not assess candidates, invoke AI/API workers, register a schedule, send notifications or replace either personal job.

Run from the authorized Mac runtime:

```sh
python3 ai-ops/runtime/doe_check.py --request-id DOE-operator-YYYYMMDD-unique
```

The encrypted APFS image and backing T7 must already be mounted and verified by `storage.py`; missing storage fails closed before retrieval. Ordinary storage resolver environment overrides are supported, but a substituted destination still must pass the same encrypted-mount, backing-image and privacy gates. There is no configurable URL or command. Source acquisition uses the macOS-safe spawn start method in an owned child session with a 45-second acquisition deadline followed by at most 4 seconds of cleanup joins. The socket timeout is not its sole deadline. A partial pipe frame cannot extend the acquisition wait. The trusted fixed reader creates no descendants; this is not universal process confinement. Unconfirmed cleanup fails closed before gate writes. Blocked worker diagnostics retain only start method, exit code and exception class; source bodies remain private. Preserve earlier blocked request artifacts; use a new request ID only for an explicit diagnosed repair test.

Request namespace `doe-operator-watch` is separate. Identical approved public-source fingerprints are shared by the existing grant-keyed cache; no candidate profiles or analysis are stored. The first complete read for that grant seeds source state; subsequent fresh request IDs classify exact-scope changes. An incomplete read preserves prior listings and reports NULL counts, never closures. Repeating an existing request ID reads back its stored receipt without fetching. An atomic request missing its artifact stops for explicit readback recovery, never blind refetch. Identity conflicts fail closed.

Complete public listings, adapter evidence and receipt are stored only in encrypted private state; stdout contains status, counts, hashes and receipt path. Do not put private state/databases/receipt bodies in Git. Status 0 means complete bounded source/readback; status 1 means blocked source; status 2 means storage/request/readback failure. A complete receipt is not a suitability decision, notification, paid run or scheduled delivery.
