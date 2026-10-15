import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from routing import CHANNELS, CHANNEL_NAMES, classifier_prompt, deterministic_route, validate_model_decision


class CurrentChannelsTests(unittest.TestCase):
    def test_current_destinations(self):
        cases = [
            ("Task: fix the router cache", "work_que", "task"),
            ("Please repair the failed Slack workflow", "work_que", "task"),
            ("Task: verify the completed router installation", "work_que", "task"),
            ("Blocked: the router cannot access its existing state", "exceptions", "thought"),
            ("Human action: approve the prepared change at its source link", "kathy", "thought"),
            ("Kathy needs to choose the final version", "kathy", "task"),
            ("Task: debug Kathy's router", "work_que", "task"),
            ("Retirement candidate: the duplicate archive workflow", "decomission", "thought"),
            ("Reflection: I noticed the biology lesson needs more examples", "teaching_reflection", "thought"),
            ("Decision: we will use this router", "decisions", "decision"),
            ("Which router should we choose?", "system_review", "question"),
            ("Is the router fixed?", "system_review", "question"),
            ("Task: organize my email", "work_que", "task"),
            ("Task: fix the router that posts to #kathy", "work_que", "task"),
        ]
        for message, destination, kind in cases:
            with self.subTest(message=message):
                result = deterministic_route(message)
                self.assertIsNotNone(result)
                self.assertEqual(result.destination_id, CHANNELS[destination])
                self.assertEqual(result.kind, kind)

    def test_explicit_destinations_in_plain_and_slack_format(self):
        for cid, name in CHANNEL_NAMES.items():
            for directive in (f"Send to #{name}: this router note", f"Route this to <#{cid}|{name}> this router note"):
                with self.subTest(directive=directive):
                    self.assertEqual(deterministic_route(directive).destination_id, cid)

    def test_classifier_uses_current_names_and_rejects_retired_destination(self):
        self.assertEqual(CHANNEL_NAMES[CHANNELS['optimize']], 'optimize-me')
        prompt = classifier_prompt('ambiguous intake')
        for name in ('work-que', 'kathy', 'exceptions', 'decomission', 'teaching-reflection'):
            self.assertIn(name, prompt)
        self.assertNotIn('delegated-kathy', prompt)
        with self.assertRaises(ValueError):
            validate_model_decision(dict(kind='task', area='personal_admin', destination='delegated-kathy', summary='A task'), provider='openai', model='test')


if __name__ == '__main__':
    unittest.main()
