import json, os, subprocess, urllib.request

def sh(c):
    return subprocess.run(c, shell=True, capture_output=True, text=True).stdout

def read(p, n=20000):
    try:
        return open(p, encoding="utf-8").read()[:n]
    except OSError:
        return f"(missing: {p})"

ctx = "\n\n".join([
    read("prompts/system-review.md"),
    "## Files\n" + sh("git ls-files | head -400"),
    "## Commits, last 7 days\n" + sh("git log --since='7 days ago' --pretty='%h %ad %s' --date=short"),
    "## ai-ops/NAMES.md\n" + read("ai-ops/NAMES.md"),
    "## ai-ops/HANDOFF.md\n" + read("ai-ops/HANDOFF.md"),
    "## roles-and-schedules\n" + read("ai-ops/worker-registry/roles-and-schedules.md"),
])

body = {
    "model": os.environ.get("REVIEW_MODEL", "claude-sonnet-5-5"),
    "max_tokens": 4000,
    "tools": [{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
    "messages": [{"role": "user", "content": ctx}],
}
req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps(body).encode(),
    headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"},
)
out = json.load(urllib.request.urlopen(req, timeout=600))
report = "\n".join(b.get("text", "") for b in out.get("content", []) if b.get("type") == "text").strip()

os.makedirs("ai-ops/reports/system-review", exist_ok=True)
path = f"ai-ops/reports/system-review/{sh('date +%F').strip()}.md"
open(path, "w", encoding="utf-8").write(report + "\n")

hook = os.environ.get("SLACK_WEBHOOK_URL")
if hook:
    msg = "*System Review* " + sh("date +%F").strip() + "\n" + report[:3500]
    urllib.request.urlopen(urllib.request.Request(hook, data=json.dumps({"text": msg}).encode(), headers={"content-type": "application/json"}))
print(path)
