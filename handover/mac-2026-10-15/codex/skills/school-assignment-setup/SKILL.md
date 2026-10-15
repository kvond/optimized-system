---
name: school-assignment-setup
description: Complete a one-time school assignment setup or repair across selected classes and marking periods, connecting the live Agenda, correct lesson material, Google submission Form, upload folder, Hub reader, and saved Schoology page. Use when the user wants these parts made functional, not merely inventoried. Does not create a recurring schedule or perform grading.
---

# School assignment setup

Deliver a working assignment chain, not a list of existing links. Perform the authorized repairs, read back the saved results, and stop only for a concrete decision or access requirement that cannot be resolved within current authorization. This is a bounded invocation; do not install a recurring check, automation, watcher, or background loop.

## Establish the actual scope

1. Discover an existing receipt and current connections before creating anything. Read the current checkout's `docs/START_HERE.md` for Hub work. Use installed Google Drive tools for metadata, live Agenda cells/formulas/link targets, and source content; use authenticated native UI for capabilities those tools lack. Read [references/native-workflow.md](references/native-workflow.md) when working in Forms or Schoology.
2. Read the **fresh actual Agenda course tabs**, dates, daily lesson plans, linked folders, and notes for every selected class/marking period. A previously completed inventory is a locator, not current proof. Include Study Hall in an all-class scope check; inspect other listed courses without inventing assignments in empty classes.
3. Build one expected record per real assignment/component, not one per week number. Match course/section + lesson identity + dates/marking period + actual source content. Inspect the actual current source folder and trash state; do not substitute a similarly named search result. Keep separate lessons in the same week separate. Reconcile material-cycle labels and calendar weeks without silently renumbering history.
4. Record grading exclusions independently: a Week 01/02 exclusion or retired lesson does not erase an explicitly requested future setup. No student submissions yet is neither a setup failure nor a reason to report future work as missing or hold grading. Unassigned/open/break slots are not missing assignments.

## Complete each assignment

Use the smallest sufficient repair and verify each factor:

- **Identity/source:** Current Agenda lesson, dates, course, actual teacher source and assignment component agree. Resolve factual stale links from current folder/content evidence; ask only about genuine contradictory teaching choices, naming the exact alternatives and slide numbers when relevant.
- **Google Form:** Reuse the correct existing Form ID and response history. Confirm school owner/collaborator readability, published state, accepting responses, intended student responder audience, full-name/class questions, correct class option (for Biology, A4 BIOLOGY), and the required upload question/type. A Form title or HTTP200 alone proves none of the remaining factors.
- **Upload destination:** Inspect the upload question's actual **View folder** destination, ownership, parent/location, existence/trash state, and accepted upload configuration. A shortcut or unrelated same-name folder is not the destination. Distinguish teacher-owner access from student response access and Hub service-reader access. Verify the latter as the actual Hub identity, including list/read where required.
- **Schoology:** Reuse or repair the exact existing course/marking-period/lesson folder and page. Save the correct Form responder link plus the current intended student lesson link when required and authorized. Check the actual body hrefs, including redirects from short links, not just page titles. Verify published/availability settings, the saved page ID, folder parent, week label and chronological placement. Do not silently turn a full lesson page into Form-only completion.
- **Student material:** Confirm that the linked file is the current intended student copy, readable by the intended audience, content-matched to the Agenda, and free of teacher-only answers. A `/copy` suffix does not grant source access. A Form-only interim page can be a useful saved repair, but is **not full setup completion** when student lesson material is required.

An approved shared Form may legitimately serve multiple components or continuing weeks. Keep the exact approved component-to-Form mapping and upload destination; do not create a new Form per week or merge separate lessons by title similarity. Multiple sections may reuse a Form only when its class selector and existing routing support those sections.

## Preserve, resume, and verify

- Preserve original sources, Form/page/folder IDs, responses, submissions, grades and historical routes. Do not restore retired Forms, reopen closed historical work, move originals, change grading rules, or broaden sharing merely to clear a count.
- For a missing file-upload folder alert, establish the account and exact Form, then use the existing Form's native **Restore** when the current task authorizes that repair. Wait for owner-side saved readback; record the resulting folder ID/metadata. A delayed restore may succeed after the initial UI appears unchanged. Do not create a second folder or retry after success. Do not assume the alert is merely a permission issue.
- Pending permission choices remain pending; a prior request is not approval, and newly found Forms/folders are separate scope. Complete independent setup work while that decision remains open. Follow the active tool's confirmation rules at the actual permission change.
- Save private before/after receipts outside public repositories. Before retrying a creation or save, freshly inspect the exact target to avoid duplicates. Resume at the first unverified factor, not the beginning. One writer per browser surface or remote object; parallel agents may prepare disjoint evidence only when authorized.
- Never submit fake student work or inspect response contents just to test setup. Use published responder configuration, intended-audience access, saved question settings, exact route readback, and owner/Hub folder reads.

Use [scripts/reconcile_setup.py](scripts/reconcile_setup.py) with the [receipt schema](references/receipt-schema.md) to reconcile the complete expected scope against fresh evidence. It is a local, read-only gate checker, **not a live verifier or executor**. Its `ready` count requires every applicable factor; a valid Form href cannot make an inaccessible upload folder or missing lesson link ready. Use the missing-factor output to perform the next authorized repair, then refresh the affected receipt and rerun.

Finish with the same line-by-line checklist: completed repairs with exact saved evidence; remaining decisions/access/source/order issues; counts of full setups versus Form/page-only repairs, retired exceptions, and unassigned slots. Put the receipt/checklist link in the user's requested working document when authorized. Do not equate all links present, all Forms counted, or a Hub deployment with completed assignment setup.
