#!/usr/bin/env python3
"""Prove that the build-system selftest accepts truth and rejects schedule drift."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

CAPSTONE = Path(__file__).resolve().parents[1]
REPOSITORY = Path(__file__).resolve().parents[5]
TEST_ROOT = (
    REPOSITORY
    / "artifacts"
    / "tests"
    / "reproducible-research"
    / "deep-dive-make"
    / "selftest-harness"
)


class SelftestHarnessTests(unittest.TestCase):
    def run_harness(self, case: str, fault: str = "none") -> tuple[subprocess.CompletedProcess[str], Path]:
        report = TEST_ROOT / case
        shutil.rmtree(report, ignore_errors=True)
        report.mkdir(parents=True)
        make = shutil.which("gmake") or shutil.which("make")
        self.assertIsNotNone(make)
        environment = os.environ.copy()
        environment.update(
            {
                "MAKE": str(make),
                "PYTHON": sys.executable,
                "SELFTEST_FAULT": fault,
                "SELFTEST_REPORT_DIR": str(report),
                "SELFTEST_WORK_DIR": str(report / "workspace"),
            }
        )
        result = subprocess.run(
            [str(CAPSTONE / "tests" / "run.sh")],
            cwd=CAPSTONE,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )
        return result, report

    def test_truthful_schedules_write_reviewable_evidence(self) -> None:
        result, report = self.run_harness("truthful-schedules")
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = (report / "summary.txt").read_text(encoding="utf-8")
        self.assertIn("result=PASS\n", summary)
        comparison = json.loads((report / "schedule-comparison.json").read_text(encoding="utf-8"))
        self.assertEqual(comparison["result"], "PASS")
        self.assertTrue((report / "logs" / "parallel-build.log").is_file())

    def test_parallel_artifact_drift_is_rejected_and_preserved(self) -> None:
        result, report = self.run_harness("parallel-artifact-drift", "parallel-artifact-drift")
        self.assertNotEqual(result.returncode, 0)
        summary = (report / "summary.txt").read_text(encoding="utf-8")
        self.assertIn("result=FAIL\n", summary)
        self.assertIn("failed_check=serial_parallel_equivalence\n", summary)
        comparison = json.loads((report / "schedule-comparison.json").read_text(encoding="utf-8"))
        self.assertEqual(comparison["result"], "FAIL")
        changed_paths = [entry["path"] for entry in comparison["changed_artifacts"]]
        self.assertEqual(changed_paths, ["build/include/dynamic.h"])
        self.assertTrue((report / "workspace" / "build" / "include" / "dynamic.h").is_file())

    def test_publication_candidates_reach_shell_with_process_identity(self) -> None:
        make = shutil.which("gmake") or shutil.which("make")
        self.assertIsNotNone(make)
        commands = (
            [str(make), "--no-print-directory", "-n", "-B", "all"],
            [
                str(make),
                "--no-print-directory",
                "-n",
                "-B",
                "USE_EVAL=yes",
                "eval-demo",
            ],
        )
        output = ""
        for command in commands:
            result = subprocess.run(
                command,
                cwd=CAPSTONE,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            output += result.stdout

        candidate_assignments = [
            line
            for line in output.splitlines()
            if ".candidate." in line and "candidate" in line
        ]
        self.assertGreaterEqual(len(candidate_assignments), 9)
        for assignment in candidate_assignments:
            self.assertIn(".candidate.$$", assignment)


if __name__ == "__main__":
    unittest.main()
