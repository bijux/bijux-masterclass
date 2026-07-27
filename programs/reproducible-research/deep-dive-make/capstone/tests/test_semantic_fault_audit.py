from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE / "scripts" / "audit_semantic_faults.py"
SPECIMENS = CAPSTONE / "repro" / "semantic-faults"


class SemanticFaultAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make = shutil.which("gmake") or shutil.which("make")
        if not self.make:
            self.skipTest("semantic fault audit requires Make")

    def run_audit(
        self,
        *,
        specimens: Path,
        workspace: Path,
        output: Path,
    ) -> subprocess.CompletedProcess[str]:
        assert self.make
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--specimens",
                str(specimens),
                "--workspace",
                str(workspace),
                "--output",
                str(output),
                "--make",
                self.make,
                "--python",
                sys.executable,
            ],
            cwd=CAPSTONE,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_verifies_state_edge_and_selection_models(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=SPECIMENS,
                workspace=root / "workspace",
                output=output,
            )
            report = json.loads(output.read_text(encoding="utf-8"))
            summary = output.with_name("summary.tsv").read_text(encoding="utf-8")
            traces = [
                output.parent / trace
                for case in report["cases"]
                for trace in case["traces"]
            ]
            self.assertTrue(all(trace.is_file() for trace in traces))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(
            report["schema"], "deep-dive-make-semantic-fault-audit"
        )
        self.assertEqual(len(report["cases"]), 7)
        cases = {
            (case["specimen"], case["model"]): case for case in report["cases"]
        }
        self.assertFalse(
            cases[("clock-state", "clock-derived")]["observation"][
                "hashes_equal"
            ]
        )
        self.assertTrue(
            cases[("clock-state", "declared-state")]["observation"][
                "hashes_equal"
            ]
        )
        self.assertEqual(
            cases[("order-only-edge", "order-only")]["observation"][
                "actual_output"
            ],
            "before",
        )
        self.assertEqual(
            cases[("order-only-edge", "semantic-edge")]["observation"][
                "actual_output"
            ],
            "after",
        )
        self.assertEqual(
            cases[("pattern-selection", "generated-rule-first")][
                "observation"
            ]["actual_outputs"],
            {"build/a.choice": "selected=generated"},
        )
        self.assertEqual(
            cases[("pattern-selection", "root-rule-first")]["observation"][
                "actual_outputs"
            ],
            {"build/a.choice": "selected=root"},
        )
        self.assertEqual(
            cases[("pattern-selection", "namespaced-targets")]["observation"][
                "actual_outputs"
            ],
            {
                "build/generated/a.choice": "selected=generated",
                "build/root/a.choice": "selected=root",
            },
        )
        self.assertIn("CLOCK_STATE_DRIFT_REPRODUCED", summary)
        self.assertIn("ORDER_ONLY_STALENESS_REPRODUCED", summary)
        self.assertIn("REORDERED_RULE_CHANGED_SELECTION", summary)

    def test_rejects_existing_workspace(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=SPECIMENS,
                workspace=workspace,
                output=output,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("workspace already exists", result.stderr)
        self.assertFalse(output.exists())

    def test_rejects_stable_clock_derived_state(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "semantic-faults"
            shutil.copytree(SPECIMENS, specimens)
            clock_makefile = specimens / "clock-state" / "clock-derived.mk"
            clock_makefile.write_text(
                clock_makefile.read_text(encoding="utf-8").replace(
                    "$(PYTHON) -c 'import time; print(time.time_ns())' > $@",
                    "cp mode.txt $@",
                ),
                encoding="utf-8",
            )
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=specimens,
                workspace=root / "workspace",
                output=output,
            )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("did not match model contracts", result.stderr)
        case = next(
            case
            for case in report["cases"]
            if case["model"] == "clock-derived"
        )
        self.assertEqual(case["result"], "FAIL")
        self.assertTrue(case["observation"]["hashes_equal"])

    def test_rejects_unexpected_pattern_selection(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "semantic-faults"
            shutil.copytree(SPECIMENS, specimens)
            generated = specimens / "pattern-selection" / "generated" / "a.src"
            generated.write_text("unexpected\n", encoding="utf-8")
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=specimens,
                workspace=root / "workspace",
                output=output,
            )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 1)
        case = next(
            case
            for case in report["cases"]
            if case["model"] == "generated-rule-first"
        )
        self.assertEqual(case["result"], "FAIL")
        self.assertEqual(
            case["observation"]["actual_outputs"]["build/a.choice"],
            "selected=unexpected",
        )

    def test_rejects_malformed_order_input(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "semantic-faults"
            shutil.copytree(SPECIMENS, specimens)
            semantic_input = specimens / "order-only-edge" / "input.txt"
            semantic_input.write_text("unknown\n", encoding="utf-8")
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=specimens,
                workspace=root / "workspace",
                output=output,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("input must contain the initial value", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
