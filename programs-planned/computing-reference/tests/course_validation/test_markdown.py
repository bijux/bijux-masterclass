from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.markdown import headings, prose_only


class MarkdownStructureTests(unittest.TestCase):
    def test_atx_headings_outside_fences_are_found(self) -> None:
        text = "# Real\n\n```text\n## Not Real\n```\n\n## Also Real ##\n"
        self.assertEqual(["Real", "Also Real"], [heading.title for heading in headings(text)])

    def test_tilde_fence_content_is_removed_from_prose(self) -> None:
        text = "before\n~~~markdown\n[missing](missing.md)\n~~~\nafter\n"
        prose = prose_only(text)
        self.assertIn("before", prose)
        self.assertIn("after", prose)
        self.assertNotIn("missing.md", prose)


if __name__ == "__main__":
    unittest.main()
