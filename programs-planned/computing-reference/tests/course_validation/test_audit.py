from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from course_validation.audit import audit_modules, select_modules
from course_validation.manifest import module_rows
from fixtures import copy_blueprint


class AuditSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = module_rows(ROOT)

    def test_program_and_level_select_fifty_modules(self) -> None:
        scope, expected, selected = select_modules(self.rows, program="pls", level=1)
        self.assertEqual("program-pls-level-1", scope)
        self.assertEqual(50, expected)
        self.assertEqual(50, len(selected))

    def test_horizontal_scope_selects_thirty_modules(self) -> None:
        scope, expected, selected = select_modules(self.rows, module_number=1)
        self.assertEqual("module-001", scope)
        self.assertEqual(30, expected)
        self.assertEqual(30, len(selected))


class AuditExecutionTests(unittest.TestCase):
    def test_planned_horizontal_scope_is_reported_as_skipped(self) -> None:
        with copy_blueprint() as directory:
            result, report, path = audit_modules(Path(directory), module_number=1)
        self.assertEqual((), result.issues)
        self.assertEqual(30, report.counts["skipped"])
        self.assertTrue(path.name == "report.json")

    def test_completion_gate_rejects_planned_scope(self) -> None:
        with copy_blueprint() as directory:
            result, report, _ = audit_modules(
                Path(directory),
                program="PLS",
                level=1,
                require_complete=True,
            )
        self.assertFalse(result.ok)
        self.assertEqual(50, report.counts["skipped"])
        self.assertTrue(any("still planned" in issue for issue in result.issues))


if __name__ == "__main__":
    unittest.main()
