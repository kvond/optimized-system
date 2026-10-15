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

if __name__ == "__main__":
    unittest.main()
