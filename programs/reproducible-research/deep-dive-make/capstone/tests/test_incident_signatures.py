from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE / "scripts" / "audit_incident_signatures.py"
REPRO_DIR = CAPSTONE / "repro"


class IncidentSignatureAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make = shutil.which("gmake") or shutil.which("make")
        if not self.make:
            self.skipTest("incident signature audit requires Make")

    def run_audit(
        self,
        *,
        repro_dir: Path,
        workspace: Path,
        output: Path,
        case: str = "all",
    ) -> subprocess.CompletedProcess[str]:
        assert self.make
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repro-dir",
                str(repro_dir),
                "--workspace",
                str(workspace),
                "--output",
                str(output),
                "--make",
                self.make,
                "--case",
                case,
            ],
            cwd=CAPSTONE,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_verifies_three_distinct_incident_signatures(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                repro_dir=REPRO_DIR,
                workspace=root / "workspace",
                output=output,
            )
            report = json.loads(output.read_text(encoding="utf-8"))
            summary = output.with_name("summary.tsv").read_text(encoding="utf-8")
            artifacts = [
                output.parent / case["observation"]["artifact"]
                for case in report["cases"]
            ]

            self.assertTrue(all(path.is_file() for path in artifacts))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(
            report["schema"], "deep-dive-make-incident-signature-audit"
        )
        self.assertEqual(len(report["cases"]), 3)
        cases = {case["case"]: case for case in report["cases"]}
        self.assertEqual(
            cases["shared-log-interleaving"]["finding"],
            "SEMANTIC_CORRUPTION_REPRODUCED",
        )
        self.assertEqual(cases["shared-log-interleaving"]["exit_status"], 0)
        self.assertEqual(
            cases["directory-creation-race"]["finding"],
            "DIRECTORY_RACE_REPRODUCED",
        )
        self.assertNotEqual(cases["directory-creation-race"]["exit_status"], 0)
        self.assertEqual(
            cases["shared-staging-collision"]["finding"],
            "STAGING_COLLISION_REPRODUCED",
        )
        self.assertEqual(
            cases["shared-staging-collision"]["observation"]["observed_files"],
            {
                "shared.staging": False,
                "x.out": False,
                "y.out": True,
            },
        )
        self.assertIn("SEMANTIC_CORRUPTION_REPRODUCED", summary)
        self.assertIn("DIRECTORY_RACE_REPRODUCED", summary)
        self.assertIn("STAGING_COLLISION_REPRODUCED", summary)

    def test_can_isolate_one_incident_case(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                repro_dir=REPRO_DIR,
                workspace=root / "workspace",
                output=output,
                case="directory-creation-race",
            )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            [case["case"] for case in report["cases"]],
            ["directory-creation-race"],
        )

    def test_rejects_existing_workspace(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                repro_dir=REPRO_DIR,
                workspace=workspace,
                output=output,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("workspace already exists", result.stderr)
        self.assertFalse(output.exists())

    def test_rejects_a_missing_semantic_signature(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            repro_dir = root / "repro"
            repro_dir.mkdir()
            (repro_dir / "shared-log-interleaving.mk").write_text(
                ".PHONY: all\n"
                "all:\n"
                "\tprintf 'alpha:start\\nalpha:end\\n"
                "beta:start\\nbeta:end\\n' > shared.log\n",
                encoding="utf-8",
            )
            output = root / "evidence" / "report.json"
            result = self.run_audit(
                repro_dir=repro_dir,
                workspace=root / "workspace",
                output=output,
                case="shared-log-interleaving",
            )
            report = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("did not match promised signatures", result.stderr)
        self.assertEqual(report["result"], "FAIL")
        self.assertFalse(report["cases"][0]["signature_matches"])


if __name__ == "__main__":
    unittest.main()
