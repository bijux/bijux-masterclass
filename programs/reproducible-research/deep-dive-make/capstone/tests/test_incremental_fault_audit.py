from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE / "scripts" / "audit_incremental_faults.py"
SPECIMENS = CAPSTONE / "repro" / "incremental-edges"


class IncrementalFaultAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make = shutil.which("gmake") or shutil.which("make")
        self.compiler = shutil.which("cc")
        if not self.make or not self.compiler:
            self.skipTest("incremental fault audit requires Make and a C compiler")

    def run_audit(
        self,
        *,
        specimens: Path,
        workspace: Path,
        output: Path,
    ) -> subprocess.CompletedProcess[str]:
        assert self.make
        assert self.compiler
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
                "--compiler",
                self.compiler,
                "--python",
                sys.executable,
            ],
            cwd=CAPSTONE,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_reproduces_faults_and_verifies_declared_edges(self) -> None:
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
            traces = {
                case["model"] + "/" + case["specimen"]: (
                    output.parent / case["trace"]
                ).read_text(encoding="utf-8")
                for case in report["cases"]
            }

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(
            report["schema"], "deep-dive-make-incremental-fault-audit"
        )
        self.assertEqual(len(report["cases"]), 4)
        cases = {
            (case["specimen"], case["model"]): case for case in report["cases"]
        }
        self.assertEqual(
            cases[("authored-header", "missing-edge")]["finding"],
            "FAULT_REPRODUCED",
        )
        self.assertEqual(
            cases[("authored-header", "declared-edge")]["changed_outputs"],
            ["app"],
        )
        self.assertEqual(
            cases[("generated-producer", "missing-edge")]["actual_output"],
            "before",
        )
        self.assertEqual(
            cases[("generated-producer", "declared-edge")]["changed_outputs"],
            ["app", "generated.h"],
        )
        self.assertIn("Nothing to be done", traces["missing-edge/authored-header"])
        self.assertIn("config.h", traces["declared-edge/authored-header"])
        self.assertIn(
            "scripts/render_header.py",
            traces["declared-edge/generated-producer"],
        )
        self.assertNotIn("Clock skew", "".join(traces.values()))
        self.assertIn("FAULT_REPRODUCED", summary)
        self.assertIn("REPAIR_VERIFIED", summary)

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

    def test_rejects_specimen_without_mutation_marker(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "specimens"
            shutil.copytree(SPECIMENS, specimens)
            config = specimens / "authored-header" / "config.h"
            config.write_text(
                '#define MESSAGE "before"\n/* duplicate marker: "before" */\n',
                encoding="utf-8",
            )
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                specimens=specimens,
                workspace=root / "workspace",
                output=output,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn("one mutation marker", result.stderr)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
