import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as appmod
from providers import ProviderError
from routing import CHANNELS
from state import State
import test_app


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'FIRESTORE_PROJECT': '', 'SLACK_GATEWAY_STATE': str(Path(self.temp.name) / 'state.sqlite'), 'SLACK_SIGNING_SECRET': 'unit-test-secret'})
        self.env.start()
        self.state = State()
        self.state_patch = patch.object(appmod, '_state', self.state)
        self.state_patch.start()
        self.posts = patch.object(appmod, 'post').start()
        self.provider = patch.object(appmod, 'call_provider', side_effect=AssertionError('unexpected provider call')).start()
        self.addCleanup(patch.stopall)
        self.addCleanup(self.temp.cleanup)
        self.client = appmod.app.test_client()

    def deliver(self, event_id='Ev-live-test', text='Task: fix the router cache', **event_fields):
        import time
        event = dict(type='message', channel=CHANNELS['optimize'], user='U0C9C9QESRL', ts='1792060000.100000', text=text)
        event.update(event_fields)
        body = json.dumps(dict(type='event_callback', event_id=event_id, event=event)).encode()
        ts = str(int(time.time()))
        response = self.client.post('/slack/events', data=body, content_type='application/json', headers={
            'X-Slack-Request-Timestamp': ts,
            'X-Slack-Signature': test_app.AppTests().signature(body, ts),
        })
        self.assertEqual(response.status_code, 200)
        return response

    def completed(self, event_id='Ev-live-test'):
        with sqlite3.connect(self.state.db_path) as db:
            row = db.execute('SELECT status,payload FROM events WHERE event_id=?', (event_id,)).fetchone()
        self.assertEqual(row[0], 'complete')
        return json.loads(row[1])

    def test_signed_retry_posts_once_using_persisted_state(self):
        self.deliver()
        self.assertTrue(self.deliver().get_json()['duplicate'])
        self.assertEqual(self.posts.call_count, 2)
        self.assertEqual(self.posts.call_args_list[1].args[0], CHANNELS['work_que'])
        self.assertIn('<https://answerableteaching.slack.com/archives/C0C9AQ2FK3P/p1792060000100000|Original request>', self.posts.call_args_list[1].args[1])
        self.assertTrue(self.completed()['forwarded'])
        self.provider.assert_not_called()

    def test_connector_posts_with_owner_identity_are_ignored(self):
        for suffix in ('\n*Sent using* <@U0C9E4UU1QS|ChatGPT>', '\n**Sent using** <@U0C9E4UU1QS>\n',
                       '\n_Sent using_ Claude', '\n_Sent using_ Claude\n*Sent using* Claude'):
            self.deliver(text='Task: fix the router cache' + suffix)
        for field in ('app_id', 'bot_id', 'subtype'):
            self.deliver(**{field: 'generated'})
        self.posts.assert_not_called()
        self.provider.assert_not_called()
        with sqlite3.connect(self.state.db_path) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM events').fetchone()[0], 0)

    def test_human_mentions_of_chatgpt_still_route(self):
        self.deliver(text='Task: fix the router for <@U0C9E4UU1QS|ChatGPT>')
        self.assertEqual(self.posts.call_count, 2)

    def test_owner_and_channel_boundaries(self):
        self.deliver(event_id='Ev-other-user', user='UOTHER')
        self.deliver(event_id='Ev-other-channel', channel=CHANNELS['work_que'])
        self.posts.assert_not_called()
        self.provider.assert_not_called()
        self.assertEqual(self.completed('Ev-other-user')['ignored'], 'outside_owner_intake')

    def test_mocked_provider_result_is_cached_without_second_call(self):
        self.provider.side_effect = None
        self.provider.return_value = (json.dumps(dict(kind='task', area='ai_ops', destination='work-que', summary='Review the ambiguous request')), {'input_tokens': 10, 'output_tokens': 5})
        self.deliver(event_id='Ev-api-1', text='Where should this go?')
        self.deliver(event_id='Ev-api-2', text='Where should this go?')
        self.provider.assert_called_once()
        self.assertFalse(self.completed('Ev-api-1')['cache_hit'])
        self.assertTrue(self.completed('Ev-api-2')['cache_hit'])
        self.assertEqual(self.posts.call_count, 4)
        with sqlite3.connect(self.state.db_path) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM usage').fetchone()[0], 1)

    def test_provider_failure_does_not_try_another_provider(self):
        self.provider.side_effect = ProviderError('test failure')
        self.deliver(text='Where should this go?')
        self.provider.assert_called_once()
        self.posts.assert_called_once()
        self.assertIn('nothing was forwarded', self.posts.call_args.args[1])
        self.assertEqual(self.completed()['held'], 'classification_failed')
        self.deliver(text='Where should this go?')
        self.provider.assert_called_once()

    def test_invalid_model_output_is_held_and_not_cached(self):
        self.provider.side_effect = None
        self.provider.return_value = ('{"kind":"task","area":"ai_ops","destination":"not-a-channel","summary":"invalid"}', {})
        self.deliver(text='Where should this go?')
        self.posts.assert_called_once()
        self.assertEqual(self.completed()['held'], 'classification_failed')
        with sqlite3.connect(self.state.db_path) as db:
            self.assertEqual(db.execute('SELECT count(*) FROM cache').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
