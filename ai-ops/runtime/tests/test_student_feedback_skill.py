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


    def _render(self, data, out):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / 'report.json'
            src.write_text(json.dumps(data))
            return subprocess.run([sys.executable, str(SKILL / 'scripts' / 'render.py'), str(src), str(out)],
                                  capture_output=True, text=True)

    @unittest.skipUnless(importlib.util.find_spec('reportlab'), 'reportlab not installed')
    def test_renderer_refuses_bad_content_instead_of_drawing_it(self):
        grouped = json.loads((SKILL / 'examples' / 'ap-lessons-grouped.json').read_text())
        grouped['lessons'][0]['aspects'] = grouped['lessons'][0]['aspects'] * 2
        lesson = json.loads((SKILL / 'examples' / 'biology-lesson.json').read_text())
        lesson['aspects'][0]['level'] = 'Almost there'
        with tempfile.TemporaryDirectory() as tmp:
            for data, message in ((grouped, 'at most three'), (lesson, 'outside the scale')):
                out = Path(tmp) / 'out.pdf'
                result = self._render(data, out)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertFalse(out.exists())

    @unittest.skipUnless(importlib.util.find_spec('reportlab'), 'reportlab not installed')
    def test_renderer_refuses_output_inside_a_git_checkout(self):
        lesson = json.loads((SKILL / 'examples' / 'biology-lesson.json').read_text())
        out = ROOT / 'should-not-exist.pdf'
        result = self._render(lesson, out)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('outside the repository', result.stderr)
        self.assertFalse(out.exists())

    @unittest.skipUnless(importlib.util.find_spec('reportlab'), 'reportlab not installed')
    def test_missing_comparison_is_stated_not_required(self):
        grouped = json.loads((SKILL / 'examples' / 'ap-lessons-grouped.json').read_text())
        grouped.pop('thinking_changed')
        with tempfile.TemporaryDirectory() as tmp:
            result = self._render(grouped, Path(tmp) / 'out.pdf')
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
