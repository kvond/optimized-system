"""Synthetic checks for skills/student-feedback: layouts render, examples stay invented."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills' / 'student-feedback'
EXPECTED_PAGES = {'biology-lesson.json': 1, 'ap-lessons-grouped.json': 2,
                  'biology-writing.json': 2, 'forensics-writing-cer.json': 3}


class StudentFeedbackSkillTest(unittest.TestCase):
    def test_skill_names_itself_and_its_source(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\nname: student-feedback\n'))
        self.assertIn('10 pts summative extra credit', text)
        self.assertIn('no more than three per lesson', text)
        self.assertTrue((SKILL / 'reference' / 'prompt-2-feedback-for-students.md').exists())

    def test_examples_cover_every_layout_with_invented_names(self):
        layouts = set()
        for name in EXPECTED_PAGES:
            data = json.loads((SKILL / 'examples' / name).read_text())
            layouts.add(data['layout'])
            self.assertEqual(data['name'], 'Sam R.')
        self.assertEqual(layouts, {'lesson_onepage', 'lessons_grouped', 'writing_bio', 'writing_cer'})

    @unittest.skipUnless(importlib.util.find_spec('reportlab'), 'reportlab not installed')
    def test_examples_render_with_expected_page_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name, pages in EXPECTED_PAGES.items():
                out = Path(tmp) / (name + '.pdf')
                subprocess.run([sys.executable, str(SKILL / 'scripts' / 'render.py'),
                                str(SKILL / 'examples' / name), str(out)], check=True)
                body = out.read_bytes()
                self.assertTrue(body.startswith(b'%PDF'))
                self.assertEqual(body.count(b'/Type /Page\n') + body.count(b'/Type /Page>>'), pages, name)


if __name__ == '__main__':
    unittest.main()
