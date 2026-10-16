"""One-time, on YOUR machine (not CI): mint the Google refresh token.

Prereq (one time, ~5 min, all in the browser):
  console.cloud.google.com → new project "daily-brief" →
  APIs & Services → Enable: Gmail API, Google Calendar API, Google Sheets API →
  OAuth consent screen: Internal-or-Testing, add kvond12@gmail.com as test user →
  Credentials → Create credentials → OAuth client ID → Desktop app →
  download the JSON next to this script as client_secret.json

Then:  pip install google-auth-oauthlib && python mint_google_tokens.py
A browser opens; approve with kvond12. Output: google_oauth.json —
paste its contents into the GitHub secret GOOGLE_OAUTH_JSON, then delete
both local files.
"""
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
secrets = json.load(open("client_secret.json"))["installed"]
out = {"client_id": secrets["client_id"],
       "client_secret": secrets["client_secret"],
       "refresh_token": creds.refresh_token}
json.dump(out, open("google_oauth.json", "w"), indent=1)
print("Wrote google_oauth.json — paste into GitHub secret GOOGLE_OAUTH_JSON, then delete it.")
