import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from routing import CHANNELS, default_provider_for, deterministic_route, provider_override

class RoutingTests(unittest.TestCase):
    def test_school_lesson_routes_without_api(self):
        value = deterministic_route("Need to print the Biology lesson and lab setup for Monday")
        self.assertIsNotNone(value)
        self.assertEqual(value.area, "school")
        self.assertEqual(value.destination_id, CHANNELS["lesson_preflight"])
        self.assertTrue(value.deterministic)

    def test_book_routes_to_writing(self):
        value = deterministic_route("I think this belongs in the Answerable Teaching chapter on agency")
        self.assertEqual(value.area, "writing")
        self.assertEqual(value.destination_id, CHANNELS["writing_flow"])

    def test_higher_ed_routes_to_new_lane(self):
        value = deterministic_route("Task: revise the OLI 7106 DIP feedback workflow")
        self.assertEqual(value.area, "higher_ed")
        self.assertEqual(value.destination_id, CHANNELS["higher_ed"])

    def test_provider_override_forces_model_classification(self):
        provider, clean = provider_override("claude: organize this ambiguous note")
        self.assertEqual(provider, "claude")
        self.assertEqual(clean, "organize this ambiguous note")
        self.assertIsNone(deterministic_route("claude: organize this ambiguous note"))
        self.assertEqual(default_provider_for("claude: organize this ambiguous note"), ("claude", "claude-haiku-5-5"))

    def test_ambiguous_operational_defaults_openai(self):
        self.assertEqual(default_provider_for("Where should this go?"), ("openai", "gpt-6-luna"))

    def test_addressed_requests_take_precedence_over_completion_context(self):
        for address in ("<@U00000001>", "<@U00000001|Helper>", "<@U00000001>, <@U00000002>:"):
            for request in (
                "please update the GitHub tracker.\nDone: the router was fixed.",
                "Please repair the failed Slack workflow",
            ):
                with self.subTest(address=address, request=request):
                    message = f"{address} {request}"
                    result = deterministic_route(message)
                    self.assertEqual(result.kind, "task")
                    self.assertEqual(result.destination_id, CHANNELS["work_que"])
                    self.assertTrue(result.deterministic)
                    self.assertIsNone(result.model)
                    self.assertIn(address, result.summary)

    def test_addressed_explicit_directive_beats_incidental_topic(self):
        for directive in (
            "Route this to #work-que:",
            f"Send to <#{CHANNELS['work_que']}|work-que>:",
        ):
            with self.subTest(directive=directive):
                result = deterministic_route(f"<@U00000001|Helper> {directive} the biology deck is finished")
                self.assertEqual(result.kind, "task")
                self.assertEqual(result.destination_id, CHANNELS["work_que"])

    def test_address_does_not_turn_status_or_ambiguity_into_a_task(self):
        result = deterministic_route("<@U00000001|Helper> the router is finished")
        self.assertEqual(result.kind, "accomplishment")
        self.assertEqual(result.destination_id, CHANNELS["system_review"])
        self.assertEqual(deterministic_route("<@U00000001> this one").destination_id, CHANNELS["needs_rerouting"])

if __name__ == "__main__":
    unittest.main()
