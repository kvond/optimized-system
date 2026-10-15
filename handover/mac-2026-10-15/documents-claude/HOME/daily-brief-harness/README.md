# Daily Brief — cheap-lane harness

The morning brief, off the Claude subscription: GitHub Actions (free) runs
Python each day at 5:45 AM Panama, reads the Master Agenda, all Google
calendars, Gmail, and Roam directly through their own APIs, calls DeepSeek
only for the judgment spans (mail triage, headline, acts, attend-first),
and produces the same two outputs as the `daily-brief` skill: the HTML page
at one stable password-gated URL, and the 📅 Daily Brief stamp on the Roam
daily page — with the stable URL as its first line. Run cost ≈ $0.02–0.05.

The terrain drawing is deterministic Python (`src/build/terrain.py`) — the
elevation math comes from the calendar, not from a model.

## Setup — every command is copy-pasteable, in order

### 0. Keys you mint in a browser (the only non-terminal steps)
- **DeepSeek**: platform.deepseek.com → sign up, add ~$5 credit → API Keys → create. Copy it.
- **Roam**: Roam Desktop → your graph → Settings → Graph → API tokens → new token, read+edit. Copy it.
- **Netlify token**: app.netlify.com → User settings → Applications → New access token. Copy it.
- **Google**: follow the docstring at the top of `scripts/mint_google_tokens.py` (~5 min), run it, keep `google_oauth.json` handy for step 3.

### 1. Repo (private) — from this folder
```bash
gh auth login          # once, if needed
gh repo create daily-brief-harness --private --source . --push
```

### 2. Netlify site + password gate
```bash
npx --yes netlify-cli login
npx --yes netlify-cli sites:create --name kvd-daily-brief
# note the Site ID it prints, and the URL: https://kvd-daily-brief.netlify.app
npx --yes netlify-cli env:set BRIEF_USER katherine
npx --yes netlify-cli env:set BRIEF_PASS "$(openssl rand -base64 12)"
npx --yes netlify-cli env:get BRIEF_PASS   # save this in your password manager
```

### 3. GitHub secrets (paste each value when prompted)
```bash
gh secret set LLM_API_KEY
gh secret set ROAM_API_TOKEN
gh secret set NETLIFY_AUTH_TOKEN
gh secret set NETLIFY_SITE_ID
gh secret set GOOGLE_OAUTH_JSON < scripts/google_oauth.json
rm scripts/google_oauth.json scripts/client_secret.json   # secrets never live on disk after this
```

### 4. Config
Edit `config.yaml`: set `roam_graph` and `site_url` (from step 2). Commit and push.

### 5. First run + parallel period
```bash
gh workflow run daily-brief
gh run watch
```
Open the site URL, check the page against that morning's Cowork brief.
Run both lanes in parallel for 3–5 mornings. Only then disable the Cowork
scheduled task, and only then look at whether the Max tier can drop.

## Failure posture
A dead source degrades to one honest line on the page ("Gmail unreachable
this morning") — the brief still renders. A failed Roam write prints the
full block tree in the Actions log for pasting, same contract as the skill.
Actions emails you if the whole job fails.

## Swapping the model
`config.yaml → llm`. DeepSeek, Moonshot/Kimi, and Anthropic's
OpenAI-compatible endpoint all work with the same client. If the voice
grates after a week, that is the one-line upgrade to try before anything
else.

## Known first-run calibration
`src/sources/agenda.py` scans the Master Agenda grid for the week row by
date match rather than fixed columns. The first SCHOOL-mode run should be
eyeballed against the sheet; if the v5 grid names weeks differently, the
match logic is the one function to adjust (`week_row_for`).
