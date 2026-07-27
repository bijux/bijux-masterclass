"""Acceptance and rejection tests for the architecture contract audit."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
RUNNER = CAPSTONE_ROOT / "scripts/audit_architecture_contracts.py"
SPECIMENS = CAPSTONE_ROOT / "repro/architecture-contracts"
TEST_ARTIFACTS = REPO_ROOT / "artifacts/tests/deep-dive-make/architecture-contracts"


class ArchitectureContractAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        TEST_ARTIFACTS.mkdir(parents=True, exist_ok=True)
        self.temporary_directory = tempfile.TemporaryDirectory(
            prefix="audit-",
            dir=TEST_ARTIFACTS,
        )
        self.root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def copy_specimens(self) -> Path:
        destination = self.root / "specimens"
        shutil.copytree(SPECIMENS, destination)
        return destination

    def run_audit(
        self,
        specimens: Path,
        *,
        workspace: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        workspace_path = workspace or self.root / "workspace"
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--specimens",
                str(specimens),
                "--workspace",
                str(workspace_path),
                "--output",
                str(self.root / "bundle/report.json"),
                "--make",
                "gmake",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def read_report(self) -> dict[str, object]:
        return json.loads((self.root / "bundle/report.json").read_text(encoding="utf-8"))

    def test_all_six_architecture_models_match_their_contracts(self) -> None:
        result = self.run_audit(self.copy_specimens())

        self.assertEqual(result.returncode, 0, result.stderr)
        report = self.read_report()
        self.assertEqual(report["result"], "PASS")
        cases = report["cases"]
        self.assertIsInstance(cases, list)
        assert isinstance(cases, list)
        self.assertEqual(len(cases), 6)
        self.assertEqual(
            {case["finding"] for case in cases},
            {
                "PRIVATE_TARGET_DEPENDENCE_REPRODUCED",
                "PUBLIC_TARGET_CONTRACT_HONORED",
                "CROSS_LAYER_POLICY_LEAK_REPRODUCED",
                "TARGET_SCOPED_POLICY_PRESERVED",
                "FLAT_OUTPUT_OWNERSHIP_COLLAPSED",
                "SUBSYSTEM_OUTPUT_OWNERSHIP_PRESERVED",
            },
        )

    def test_existing_workspace_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        workspace = self.root / "workspace"
        workspace.mkdir()

        result = self.run_audit(specimens, workspace=workspace)

        self.assertEqual(result.returncode, 2)
        self.assertIn("workspace already exists", result.stderr)

    def test_private_caller_that_runs_verification_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        script = specimens / "public-api/automation-private.sh"
        script.write_text(
            script.read_text(encoding="utf-8").replace(
                "internal-build",
                "verify",
            ),
            encoding="utf-8",
        )

        result = self.run_audit(specimens)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.read_report()["result"], "FAIL")

    def test_global_model_without_policy_leak_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        release_policy = (
            specimens
            / "include-ownership/global-mutation/mk/release.mk"
        )
        release_policy.write_text("", encoding="utf-8")

        result = self.run_audit(specimens)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.read_report()["result"], "FAIL")

    def test_namespaced_model_with_one_output_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "output-ownership/namespaced-output/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8").replace(
                "OUTPUTS := $(patsubst src/%,build/%,$(SOURCES))",
                "OUTPUTS := build/cli/util.txt",
            ),
            encoding="utf-8",
        )

        result = self.run_audit(specimens)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.read_report()["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
