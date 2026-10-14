# Scheduler conversion artifact format

Private candidate bundles use schema version 1 and operation
`same-owner-prompt-conversion`. They reference the existing sole registry by path,
one exact schedule key, workflow ID/version, contract/procedure SHA-256 pins,
canonical checkout/remote, owner hash, immutable original TOML/prompt backups,
private bindings and complete reviewed source-paragraph mappings. Local update
and rollback tool payloads preserve every existing scheduling field. No actual
binding or candidate is committed here.

Each source paragraph has its ordinal, exact UTF-8 SHA-256, disposition `covered`
or `superseded`, one or more exact versioned file/heading targets and a review
note. Explicit supersession retains the old source privately and identifies the
new governing instruction. Unresolved coverage blocks applying the candidate.
These mappings support review; they cannot mechanize semantic equivalence.

Cloud personal candidates use operation `blocked-provider-conversion` and have
no executable update payload until current native definition, exact accessible
contract/worker binding, provider cadence/timezone and output trial are resolved.
Never fabricate a provider ID, notification setting, model, target thread, worker
bridge or native API field to make a candidate appear runnable.

Approval/readiness lives in dated private evidence, never in this manifest:
published source, exact artifacts, unchanged native source, reviewed coverage,
current private bindings/authority, accepted exact-destination trial and no
running job. Destination cutover additionally requires disabled-old readback
before enable-new. Rollback requires disabled-new readback first. Lost readback
means stop and reconcile, not resend. See the scheduler cutover runbook.
