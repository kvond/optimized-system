---
name: github-maintenance
description: >
  Review and steer the monthly maintenance of the kvond GitHub account: read the latest
  report, decide which proposals to approve, start archive or enforce runs, change a
  retention rule, undo an action, or renew the token. Triggers: "maintenance report",
  "stale repos", "archive that repo", "GitHub cleanup", "retention rule", "MAINT_TOKEN",
  or any question about what the maintenance process did or will do.
---

# GitHub Maintenance

The process itself lives in the private repository `kvond/github-maintenance`. Read its
`README.md` for the rules and `AGENTS.md` for how an agent behaves inside it. This skill
is the procedure for a session with Katherine. It is a review-and-approve loop, not an
automation: the schedule only reports, and every archive or delete action starts with a
person saying so.

The GitHub connection is the Composio `github` account (`kvond`), which can read every
file in the repository, commit files (including workflow files), start a workflow run,
and store a secret.

## Where things are

| What | Where |
|---|---|
| Latest report | `reports/latest.md` in `kvond/github-maintenance`, and the newest comment on the **Maintenance log** issue |
| Findings as data | `reports/latest.json` |
| Rules | `retention.yml` (the only file to edit) |
| Start a run by hand | GitHub → `github-maintenance` → **Actions** → **maintenance** → **Run workflow** |
| Off switch | Repository variable `MAINT_ENABLED` = `false` (Settings → Secrets and variables → Actions → Variables) |
| Token | Repository secret `MAINT_TOKEN`; creation steps in `docs/TOKEN_SETUP.md` |
| Reversals | `docs/UNDO.md` |

## Each review (after the monthly report, or on request)

1. Read `reports/latest.md`. Give Katherine the outcome line and then the items marked
   *proposed* and *waiting*, one per line, each with its reason as the report states it.
   Leave out the storage table unless a flag is raised there.
2. If the scope line says `public listing only`, stop and say so: `MAINT_TOKEN` is
   missing or expired, and the report covered only public repositories. Offer the token
   renewal steps below before anything else.
3. Ask one question at a time, each a menu with a recommendation, for example:
   "Archive `answerableteaching-com` (no push for 190 days, not cloned)? Yes / Not yet /
   Never (add to protected)." Record each answer before asking the next.
4. Carry out the answers:
   - **Yes** to reversible actions → start an `archive` run (step "Starting a run").
     If the item is still *waiting* in the grace period, say when it becomes eligible
     instead of forcing it.
   - **Not yet** → nothing; the flag stays and the item returns next month.
   - **Never** → add the repository to `safety.protected_repos`, or the label `keep` to the
     issue, or the name under `visibility.public_allowed`, by editing `retention.yml`
     through the GitHub connection with a commit message starting `policy:`.
5. After a run, read the new `reports/latest.md` and confirm what was performed, with the
   undo line for each action.

## Starting a run

Through the Composio GitHub connection, dispatch the workflow (the tool is
`GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT`; the inputs are shown as the API body):

```
POST /repos/kvond/github-maintenance/actions/workflows/maintenance.yml/dispatches
{"ref": "main", "inputs": {"mode": "dry-run"}}
{"ref": "main", "inputs": {"mode": "archive"}}
{"ref": "main", "inputs": {"mode": "archive", "only": "answerableteaching-com"}}
{"ref": "main", "inputs": {"mode": "enforce", "confirm": "ENFORCE"}}
```

Wait about two minutes, then read `reports/latest.md` again (the workflow commits it).

## STOP-AND-CONFIRM checkpoint

Start `enforce` only if Katherine wrote the word ENFORCE in this conversation. Deleted
workflow runs, artifacts and caches cannot be recovered. If she asks for enforce without
the word, show what the last dry run listed under *proposed* with proposal `delete`, name
the count and total size, and ask for the word. Enforce also needs the secret
`MAINT_TOKEN_ENFORCE`, a token with Actions write and a seven-day expiry that she creates
for the occasion (`docs/TOKEN_SETUP.md`, step 4); the standing token cannot delete anything.
Never propose giving the standing token Actions write instead.

Never edit `state/flags.json`, `state/sizes.json` or `state/engine_pushes.json`. Never remove a repository from
`safety.protected_repos` on your own judgment; restate the consequence and get a yes.

## Changing a rule

Edit `retention.yml` only. Every threshold has a comment beside it. Commit with a message
starting `policy:` and say which line changed. The `ci` workflow validates the file; if it
fails, the Actions tab shows the line.

## Renewing the token

Give these directions, then store the value when she pastes it:

GitHub → avatar → Settings → Developer settings → Personal access tokens → Fine-grained
tokens → Generate new token. Name `github-maintenance`, expiration one year, repository
access "All repositories", and the permissions in the table in `docs/TOKEN_SETUP.md`
(Administration, Contents, Issues, Pull requests: read and write; Actions: read only).

To store it: fetch the repository public key (`GITHUB_GET_A_REPOSITORY_PUBLIC_KEY`),
encrypt the value as a libsodium sealed box, and write it with
`GITHUB_CREATE_OR_UPDATE_A_REPOSITORY_SECRET` under the name `MAINT_TOKEN`. Then start a
`dry-run` and check that the scope line reads `user token`.

## Undoing something

Follow `docs/UNDO.md`. The short version: archived repository → Settings → Unarchive;
removed branch → recreate it from the tag `archive/<branch>/<date>`; closed issue →
Reopen; moved files → close or revert the pull request.

## Notes

- The schedule is the 1st of each month, 07:23 New York in summer (06:23 in winter).
  It runs report-only no matter what anyone dispatches; the engine forces the mode.
- Nothing is acted on the first time it is reported. The item must be at least 14 days
  in `state/flags.json` first. This is deliberate; do not work around it.
- `scheduled-runs` looks stale by push date but is read by the scheduler; it is protected
  for that reason. If a new repository plays the same role, add it to the protected list.
