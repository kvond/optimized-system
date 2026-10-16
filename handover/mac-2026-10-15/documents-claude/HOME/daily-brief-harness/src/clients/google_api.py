"""One authenticated client per Google service, from a single refresh token.

GOOGLE_OAUTH_JSON (env, GitHub secret) holds:
  {"client_id": ..., "client_secret": ..., "refresh_token": ...}
minted once by scripts/mint_google_tokens.py on Katherine's machine.
Scopes: gmail.readonly, calendar.readonly, spreadsheets.readonly.
"""
import json, os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

def _creds():
    blob = json.loads(os.environ["GOOGLE_OAUTH_JSON"])
    return Credentials(
        token=None,
        refresh_token=blob["refresh_token"],
        client_id=blob["client_id"],
        client_secret=blob["client_secret"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=SCOPES,
    )

def gmail():    return build("gmail", "v1", credentials=_creds(), cache_discovery=False)
def gcal():     return build("calendar", "v3", credentials=_creds(), cache_discovery=False)
def sheets():   return build("sheets", "v4", credentials=_creds(), cache_discovery=False)
