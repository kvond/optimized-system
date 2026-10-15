# Forms and Schoology mechanics

Read only the portions needed for the current repair. Browser identity and accessible tools can change; reacquire current state and use documented APIs. Do not reuse stale element indices or assume a remembered browser profile is authenticated.

## Google Forms

- Forms API reads can establish exact item/question IDs, responder URL, publishing state and file-upload folder ID when that identity has access. Owner, collaborator, student and Hub access are separate.
- Google Forms API does not support creating file-upload questions; even an apparently types-only batch update can fail with `Creation of file_upload question not supported`. Do not promise an API-only workflow. Use normal Forms UI, or a verified exact template copy when appropriate, then independently verify the new Form's questions and **fresh upload-folder association**. Never assume copied questions imply an independent upload destination.
- For an existing question, preserve its ID, Required state, file count/size and existing destination. Change only the requested accepted types. Example: a document assignment may need Documents added while keeping Presentations; changing the title alone does not make upload work.
- Owner UI `Published options` exposes `Accepting responses`. Inspect intended responder audience separately. The question's `View folder` opens its actual destination; avoid browsing student contents. Open the question to inspect Required and allowed types. Capture selected file limits only when actually visible—do not infer from a default.
- After a native missing-folder Restore, verify the alert clears, published/accepting state remains correct, owner View folder works, and required class/upload settings remain. Record a potentially newly created folder and recheck Hub access. Existing Form IDs/responses must remain; do not replace the Form.
- A collaborator's alert and an owner read can differ, or a restore may complete asynchronously. Compare action timestamps and folder creation/modification metadata before explaining the cause or repeating a repair.

## Schoology

- Inspect the exact course's four marking-period folders and real assignment pages. Expand each observed folder once, using fresh state. For the first folder, avoid confusing a `Next` breadcrumb link with the actual folder row. Page existence is not body-link verification.
- Read saved page body links. Resolve existing `forms.gle` links normally to the final responder URL; match that to the live Form ID before declaring a route missing. An empty early AX body while the page loads is not a missing-link finding.
- Use the normal Add Page UI in the exact observed folder. A previously observed create route can be reused with that course/folder identity; do not invent hidden endpoints or bypass UI. Fill title and body, retain existing availability, save once, then confirm the saved page ID and exact hrefs. Duplicate prevention must check both existing page contents and pending save state.
- To change only an existing href, the editor's upper-right `Switch to HTML` control exposes native source text. It may be poorly labeled to accessibility tools; use a fresh screenshot when needed. Capture the complete visible HTML, require exactly one occurrence of the old URL, replace only that URL, save, and read back the rendered href. Preserve all other HTML. Native text-selection offsets can be inaccurate around emoji; do not save a partial/cross-paragraph link selection.
- Moving a whole folder preserves its contents but can retain its old sort weight. After correcting dates/week/marking-period placement, verify chronological order separately. Native drag is only successful when a fresh saved list/reload proves the order; parent placement alone is insufficient.
- Navigation may complete after an AX timeout. If the exact intended URL is already in the address field, finish that navigation and inspect current state instead of repeating a mutation. Bounded sequential read batches can use fresh AX/screenshot state to confirm each expected page identity; stop a batch at the first uncertain page.
- Reuse a task tab; after a saved checkpoint, replace only a completed task-created tab if Chrome slows. Preserve user tabs and restore temporary zoom changes. Never close a tab with an uncertain save.

## Local historical locators

For Katherine's current installation, prior evidence is under `/Users/katherinevonduyke/Documents/Claude/2026-10-02/other-x20/outputs/oct14-immediate-problems/schoology/`. These are **historical locators, not current completion proof**: `*-form-route-coverage.private.json`, `biology-extra-forms-owner-verification.private.json`, `forensics-native-inventory.private.json`, and `progress.private.json`.

The surrounding `outputs/oct14-immediate-problems/` artifacts document pending access choices and multi-lesson mappings. Re-read the current decision state before permission writes. Keep personal IDs and receipts local; do not copy these into a public repository, skill listing, or generated public artifact. Discover current Agenda and Hub source bindings from the installed school workflow/repository instructions and connected metadata rather than freezing them in this skill.
