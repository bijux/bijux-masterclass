from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE_ROOT / "scripts" / "compare_performance_evidence.py"
sys.path.insert(0, str(CAPSTONE_ROOT / "scripts"))

from collect_performance_evidence import SCHEMA


def passing_evidence() -> dict[str, Any]:
    return {
        "context": {
            "compiler": {
                "command": "cc",
                "executable": "/usr/bin/cc",
                "version": "Example Compiler 1.0",
            },
            "make": {
                "command": "gmake",
                "executable": "/usr/bin/gmake",
                "version": "GNU Make 4.4",
            },
            "platform": "example-platform",
            "python": "3.14.0",
            "repository": {
                "revision": "a" * 40,
                "status": "clean",
                "status_sha256": "clean-digest",
            },
            "runner": "local-test",
        },
        "incremental_work": {
            "cases": [
                {
                    "expected_rebuild": ["all", "app", "build/util.o"],
                    "input": "src/util.c",
                    "missing_rebuild": [],
                    "observed_rebuild": ["all", "app", "build/util.o"],
                    "result": "PASS",
                    "unexpected_rebuild": [],
                },
                {
                    "expected_rebuild": [
                        "all",
                        "app",
                        "build/main.o",
                        "build/util.o",
                    ],
                    "input": "include/util.h",
                    "missing_rebuild": [],
                    "observed_rebuild": [
                        "all",
                        "app",
                        "build/main.o",
                        "build/util.o",
                    ],
                    "result": "PASS",
                    "unexpected_rebuild": [],
                }
            ],
            "policy_sha256": "incremental-policy-digest",
            "result": "PASS",
            "schema": "deep-dive-make-incremental-work-v2",
        },
        "policy_sha256": "policy-digest",
        "result": "PASS",
        "sample_count": 3,
        "scenarios": {
            "converged-noop": {
                "convergence": "PASS",
                "inventory": [{"path": "app", "sha256": "artifact-digest", "size": 3}],
                "jobs": 1,
                "route": "all",
                "samples": [
                    {"elapsed_seconds": 1.0, "exit_status": 0},
                    {"elapsed_seconds": 1.1, "exit_status": 0},
                    {"elapsed_seconds": 1.2, "exit_status": 0},
                ],
                "state": "converged",
                "summary": {
                    "maximum_seconds": 1.2,
                    "median_seconds": 1.1,
                    "minimum_seconds": 1.0,
                    "spread_seconds": 0.2,
                },
            }
        },
        "schema": SCHEMA,
    }


class PerformanceComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.owned_directory = TemporaryDirectory()
        self.workspace = Path(self.owned_directory.name)
        self.baseline = self.workspace / "baseline.json"
        self.candidate = self.workspace / "candidate.json"
        self.output = self.workspace / "comparison.json"

    def tearDown(self) -> None:
        self.owned_directory.cleanup()

    def compare(
        self,
        baseline: dict[str, Any],
        candidate: dict[str, Any],
    ) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
        self.baseline.write_text(json.dumps(baseline), encoding="utf-8")
        self.candidate.write_text(json.dumps(candidate), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--baseline",
                str(self.baseline),
                "--candidate",
                str(self.candidate),
                "--output",
                str(self.output),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        return result, json.loads(self.output.read_text(encoding="utf-8"))

    def test_accepts_matching_contract_and_semantics(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["scenarios"]["converged-noop"]["summary"]["median_seconds"] = 0.9
        candidate["context"]["repository"]["revision"] = "b" * 40

        result, report = self.compare(baseline, candidate)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["semantic_equivalence"], "PASS")
        self.assertEqual(report["execution_context"]["baseline_revision"], "a" * 40)
        self.assertEqual(report["execution_context"]["candidate_revision"], "b" * 40)
        self.assertEqual(report["incremental_work"]["result"], "PASS")
        self.assertEqual(len(report["incremental_work"]["cases"]), 2)
        self.assertEqual(report["scenarios"]["converged-noop"]["delta_seconds"], -0.2)

    def test_rejects_requested_work_drift_in_nonfirst_case(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["incremental_work"]["cases"][1]["observed_rebuild"].append(
            "build/sub/sub.o"
        )

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("include/util.h observed_rebuild mismatch", report["failure"])

    def test_rejects_missing_incremental_case(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["incremental_work"]["cases"].pop()

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incremental input set mismatch", report["failure"])

    def test_rejects_changed_incremental_policy(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["incremental_work"]["policy_sha256"] = "changed-policy"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("policy_sha256 mismatch", report["failure"])

    def test_rejects_compiler_drift(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["context"]["compiler"]["version"] = "Example Compiler 2.0"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compiler mismatch", report["failure"])

    def test_rejects_dirty_candidate_worktree(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["context"]["repository"]["status"] = "dirty"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate worktree is not clean", report["failure"])

    def test_rejects_policy_drift(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["policy_sha256"] = "different-policy"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["result"], "FAIL")
        self.assertIn("policy_sha256 mismatch", report["failure"])

    def test_rejects_sample_count_drift(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["sample_count"] = 5

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sample_count mismatch", report["failure"])

    def test_rejects_trusted_output_drift(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        inventory = candidate["scenarios"]["converged-noop"]["inventory"]
        inventory[0]["sha256"] = "changed-artifact"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("trusted-output inventory mismatch", report["failure"])

    def test_rejects_failed_candidate_evidence(self) -> None:
        baseline = passing_evidence()
        candidate = copy.deepcopy(baseline)
        candidate["result"] = "FAIL"

        result, report = self.compare(baseline, candidate)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence did not pass", report["failure"])


if __name__ == "__main__":
    unittest.main()
