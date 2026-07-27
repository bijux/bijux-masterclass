from __future__ import annotations

import sys
import unittest
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAPSTONE / "scripts"))

from analyze_trace_evidence import analyze

USEFUL_TRACE = """Makefile:127: update target 'build/' due to: target does not exist
mkdir -p build/
Makefile:111: update target 'all' due to: target does not exist
printf 'ok\\n' > all
"""


class TraceEvidenceTests(unittest.TestCase):
    def test_accepts_bounded_attributable_trace(self) -> None:
        report = analyze(
            USEFUL_TRACE, route="all", state="clean-plan", focus="all", maximum=10
        )
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["planned_targets"], ["build/", "all"])

    def test_rejects_trace_without_focus_target(self) -> None:
        report = analyze(
            USEFUL_TRACE, route="all", state="clean-plan", focus="app", maximum=10
        )
        self.assertEqual(report["result"], "FAIL")
        self.assertFalse(report["checks"]["focus_target_visible"])

    def test_rejects_unbounded_trace(self) -> None:
        report = analyze(
            USEFUL_TRACE, route="all", state="clean-plan", focus="all", maximum=2
        )
        self.assertEqual(report["result"], "FAIL")
        self.assertFalse(report["checks"]["bounded_volume"])

    def test_rejects_unattributed_output(self) -> None:
        report = analyze(
            "cc -o app\\n", route="all", state="clean-plan", focus="all", maximum=10
        )
        self.assertEqual(report["result"], "FAIL")
        self.assertFalse(report["checks"]["rule_locations_visible"])


if __name__ == "__main__":
    unittest.main()
