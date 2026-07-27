"""Acceptance and rejection tests for the abstraction contract audit."""

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
RUNNER = CAPSTONE_ROOT / "scripts/audit_abstraction_contracts.py"
SPECIMENS = CAPSTONE_ROOT / "repro/abstraction-contracts"
TEST_ARTIFACTS = REPO_ROOT / "artifacts/tests/deep-dive-make/abstraction-contracts"


class AbstractionContractAuditTests(unittest.TestCase):
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

    def assert_rejected(self, specimens: Path) -> None:
        result = self.run_audit(specimens)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.read_report()["result"], "FAIL")

    def test_all_three_abstraction_models_match_their_contracts(self) -> None:
        result = self.run_audit(self.copy_specimens())

        self.assertEqual(result.returncode, 0, result.stderr)
        report = self.read_report()
        self.assertEqual(report["result"], "PASS")
        cases = report["cases"]
        self.assertIsInstance(cases, list)
        assert isinstance(cases, list)
        self.assertEqual(len(cases), 3)
        self.assertEqual(
            {case["finding"] for case in cases},
            {
                "EXPLICIT_RULE_CONTRACT_CAPTURED",
                "BOUNDED_MACRO_CONTRACT_PRESERVED",
                "OPAQUE_MACRO_SIDE_EFFECTS_REPRODUCED",
            },
        )

    def test_existing_workspace_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        workspace = self.root / "workspace"
        workspace.mkdir()

        result = self.run_audit(specimens, workspace=workspace)

        self.assertEqual(result.returncode, 2)
        self.assertIn("workspace already exists", result.stderr)

    def test_bounded_macro_with_hidden_target_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "bounded-macro/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8")
            + "\n.PHONY: publish-alpha\npublish-alpha:\n> @:\n",
            encoding="utf-8",
        )

        self.assert_rejected(specimens)

    def test_bounded_macro_with_global_policy_mutation_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "bounded-macro/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8").replace(
                "MODE := ordinary",
                "MODE := release",
            ),
            encoding="utf-8",
        )

        self.assert_rejected(specimens)

    def test_bounded_macro_without_visible_call_domain_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "bounded-macro/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8").replace(
                "MACRO_CALLS := $(addprefix publish_owned_file:,$(OWNERS))",
                "MACRO_CALLS :=",
            ),
            encoding="utf-8",
        )

        self.assert_rejected(specimens)

    def test_opaque_macro_without_hidden_surface_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "opaque-macro/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8").replace(
                "publish-$1",
                "internal-$1",
            ),
            encoding="utf-8",
        )

        self.assert_rejected(specimens)

    def test_opaque_macro_without_policy_side_effect_is_rejected(self) -> None:
        specimens = self.copy_specimens()
        makefile = specimens / "opaque-macro/Makefile"
        makefile.write_text(
            makefile.read_text(encoding="utf-8").replace(
                "MODE := release",
                "MODE := ordinary",
            ),
            encoding="utf-8",
        )

        self.assert_rejected(specimens)


if __name__ == "__main__":
    unittest.main()
