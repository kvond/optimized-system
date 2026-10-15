from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path

class State:
    """Small idempotency/cache layer. Firestore in Cloud Run; private SQLite locally."""
    def __init__(self):
        self.project = os.environ.get("FIRESTORE_PROJECT")
        self._firestore = None
        self.db_path = None
        if self.project:
            from google.cloud import firestore
            self._firestore = firestore.Client(project=self.project)
        else:
            self.db_path = Path(os.environ.get("SLACK_GATEWAY_STATE", "~/.local/share/ai-ops/slack-gateway.sqlite")).expanduser()
            self.db_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            if self.db_path.exists() and self.db_path.stat().st_mode & 0o077:
                raise PermissionError("Slack gateway state must be private")
            self.db_path.touch(mode=0o600, exist_ok=True)
            with sqlite3.connect(self.db_path) as db:
                db.executescript("""
                CREATE TABLE IF NOT EXISTS events(event_id TEXT PRIMARY KEY, status TEXT NOT NULL, payload TEXT, updated REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS cache(cache_key TEXT PRIMARY KEY, payload TEXT NOT NULL, updated REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS usage(id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT NOT NULL, model TEXT NOT NULL, cost REAL NOT NULL, created REAL NOT NULL);
                """)

    def claim_event(self, event_id: str) -> bool:
        if self._firestore:
            ref = self._firestore.collection("ai_ops_slack_events").document(event_id)
            transaction = self._firestore.transaction()
            from google.cloud import firestore
            @firestore.transactional
            def claim(tx):
                snap = ref.get(transaction=tx)
                if snap.exists:
                    return False
                tx.set(ref, {"status": "processing", "updated": time.time()})
                return True
            return claim(transaction)
        with sqlite3.connect(self.db_path) as db:
            try:
                db.execute("INSERT INTO events VALUES (?,?,?,?)", (event_id, "processing", None, time.time()))
                db.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def complete_event(self, event_id: str, payload: dict):
        body = json.dumps(payload, sort_keys=True)
        if self._firestore:
            self._firestore.collection("ai_ops_slack_events").document(event_id).set({"status": "complete", "payload": payload, "updated": time.time()}, merge=True)
            return
        with sqlite3.connect(self.db_path) as db:
            db.execute("UPDATE events SET status='complete',payload=?,updated=? WHERE event_id=?", (body, time.time(), event_id))
            db.commit()

    def cache_get(self, key: str):
        if self._firestore:
            snap = self._firestore.collection("ai_ops_slack_cache").document(key).get()
            return snap.to_dict().get("payload") if snap.exists else None
        with sqlite3.connect(self.db_path) as db:
            row = db.execute("SELECT payload FROM cache WHERE cache_key=?", (key,)).fetchone()
            return json.loads(row[0]) if row else None

    def cache_put(self, key: str, payload: dict):
        if self._firestore:
            self._firestore.collection("ai_ops_slack_cache").document(key).set({"payload": payload, "updated": time.time()})
            return
        body = json.dumps(payload, sort_keys=True)
        with sqlite3.connect(self.db_path) as db:
            db.execute("INSERT OR REPLACE INTO cache VALUES (?,?,?)", (key, body, time.time()))
            db.commit()

    def log_usage(self, provider: str, model: str, cost: float, usage: dict):
        record = {"provider": provider, "model": model, "cost": cost, "usage": usage, "created": time.time()}
        if self._firestore:
            self._firestore.collection("ai_ops_slack_usage").add(record)
            return
        with sqlite3.connect(self.db_path) as db:
            db.execute("INSERT INTO usage(provider,model,cost,created) VALUES (?,?,?,?)", (provider, model, cost, time.time()))
            db.commit()
