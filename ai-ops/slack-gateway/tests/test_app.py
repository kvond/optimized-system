import hashlib
import hmac
import json
import os
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
os.environ.setdefault("SLACK_SIGNING_SECRET", "unit-test-secret")
import app as appmod
from routing import CHANNELS

class FakeState:
    def __init__(self):
        self.claimed = set()
        self.completed = {}
    def claim_event(self, event_id):
        if event_id in self.claimed:
            return False
        self.claimed.add(event_id)
        return True
    def complete_event(self, event_id, payload):
        self.completed[event_id] = payload
    def cache_get(self, key): return None
    def cache_put(self, key, payload): raise AssertionError("deterministic route should not cache model result")
    def log_usage(self, *args, **kwargs): raise AssertionError("deterministic route should not call provider")

class AppTests(unittest.TestCase):
    def signature(self, body, ts):
        base = b"v0:" + ts.encode() + b":" + body
        return "v0=" + hmac.new(b"unit-test-secret", base, hashlib.sha256).hexdigest()

    def test_signature(self):
        body = b'{"type":"event_callback"}'
        ts = str(int(time.time()))
        sig = self.signature(body, ts)
        self.assertTrue(appmod.verify_slack_signature(body, ts, sig, now=float(ts)))
        self.assertFalse(appmod.verify_slack_signature(body, ts, "v0=bad", now=float(ts)))
        self.assertFalse(appmod.verify_slack_signature(body, ts, sig, now=float(ts) + 301))

    def test_signed_deterministic_event_routes_without_provider(self):
        fake = FakeState()
        payload = {
            "type": "event_callback", "event_id": "Ev-test-1",
            "event": {"type": "message", "channel": CHANNELS["optimize"],
                      "user": "U0C9C9QESRL", "ts": "1792060000.100000",
                      "text": "Task: revise the OLI 7106 DIP feedback workflow"},
        }
        body = json.dumps(payload, separators=(",", ":")).encode()
        ts = str(int(time.time()))
        with patch.object(appmod, "_state", fake), patch.object(appmod, "post") as post:
            client = appmod.app.test_client()
            response = client.post("/slack/events", data=body, content_type="application/json", headers={
                "X-Slack-Request-Timestamp": ts,
                "X-Slack-Signature": self.signature(body, ts),
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.call_count, 2)
        self.assertEqual(post.call_args_list[0].args[0], CHANNELS["optimize"])
        self.assertEqual(post.call_args_list[1].args[0], CHANNELS["higher_ed"])
        self.assertTrue(fake.completed["Ev-test-1"]["decision"]["deterministic"])
        self.assertEqual(fake.completed["Ev-test-1"]["cost"], 0.0)

    def test_duplicate_event_is_acked_without_second_post(self):
        fake = FakeState(); fake.claimed.add("Ev-dup")
        payload = {"type": "event_callback", "event_id": "Ev-dup",
                   "event": {"type": "message", "channel": CHANNELS["optimize"], "user": "U0C9C9QESRL", "ts": "1.1", "text": "Task: test"}}
        body = json.dumps(payload).encode(); ts = str(int(time.time()))
        with patch.object(appmod, "_state", fake), patch.object(appmod, "post") as post:
            response = appmod.app.test_client().post("/slack/events", data=body, content_type="application/json", headers={
                "X-Slack-Request-Timestamp": ts, "X-Slack-Signature": self.signature(body, ts)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["duplicate"])
        post.assert_not_called()

if __name__ == "__main__":
    unittest.main()
