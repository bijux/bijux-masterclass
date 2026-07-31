from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE / "scripts" / "audit_environment_contracts.py"
SPECIMENS = CAPSTONE / "repro" / "environment-contracts"


class EnvironmentContractAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make = shutil.which("gmake") or shutil.which("make")
        if not self.make:
            self.skipTest("environment contract audit requires Make")

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

    def run_contract_probe(
        self,
        *,
        version: str,
        features: str,
    ) -> subprocess.CompletedProcess[str]:
        assert self.make
        makefile = (
            ".RECIPEPREFIX := >\n"
            "include mk/contract.mk\n"
            ".PHONY: show\n"
            "show:\n"
            "> @printf 'grouped=%s\\n' '$(HAVE_GROUPED_TARGETS)'\n"
        )
        return subprocess.run(
            [
                self.make,
                "--no-print-directory",
                "-f",
                "-",
                f"MAKE_VERSION={version}",
                f".FEATURES={features}",
                "show",
            ],
            cwd=CAPSTONE,
            input=makefile,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_future_version_with_required_capabilities(self) -> None:
        result = self.run_contract_probe(
            version="4.10",
            features="target-specific second-expansion grouped-target",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "grouped=grouped-target")

    def test_rejects_make_missing_a_required_capability(self) -> None:
        result = self.run_contract_probe(
            version="9.1",
            features="target-specific second-expansion",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "lacks required features: grouped-target",
            result.stderr,
        )

    def test_verifies_state_recursion_and_tool_contracts(self) -> None:
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
            report["schema"], "deep-dive-make-environment-contract-audit"
        )
        self.assertEqual(len(report["cases"]), 7)
        cases = {
            (case["specimen"], case["model"]): case for case in report["cases"]
        }
        self.assertEqual(
            cases[("non-file-state", "stale-manifest")]["observation"][
                "actual_mode"
            ],
            "release",
        )
        refreshed = cases[("non-file-state", "reevaluated-manifest")][
            "observation"
        ]
        self.assertEqual(refreshed["actual_mode"], "debug")
        self.assertTrue(refreshed["artifact_rebuilt_after_mode_change"])
        self.assertFalse(refreshed["artifact_rebuilt_for_equal_mode"])
        self.assertFalse(
            cases[("recursive-boundary", "literal-recursion")]["observation"][
                "child_plan_visible_in_dry_run"
            ]
        )
        declared = cases[("recursive-boundary", "declared-recursion")][
            "observation"
        ]
        self.assertTrue(declared["child_plan_visible_in_dry_run"])
        self.assertTrue(declared["budget_visible_in_actual_run"])
        late = cases[("required-tool", "late-tool-check")]["observation"]
        self.assertTrue(late["tool_version_exists"])
        self.assertEqual(late["tool_version_bytes"], 0)
        missing = cases[("required-tool", "contract-gate-missing")][
            "observation"
        ]
        self.assertTrue(missing["contract_message_visible"])
        self.assertFalse(missing["tool_version_exists"])
        self.assertIn("STALE_NON_FILE_STATE_REPRODUCED", summary)
        self.assertIn("DECLARED_RECURSION_EXPOSES_CHILD_PLAN", summary)
        self.assertIn("REQUIRED_TOOL_REJECTED_EARLY", summary)

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

    def test_rejects_stale_model_that_refreshes(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "environment-contracts"
            shutil.copytree(SPECIMENS, specimens)
            makefile = (
                specimens
                / "non-file-state"
                / "stale-manifest.mk"
            )
            makefile.write_text(
                makefile.read_text(encoding="utf-8").replace(
                    "$(MANIFEST): | build/",
                    ".PHONY: FORCE\nFORCE:\n\n$(MANIFEST): FORCE | build/",
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
        case = next(
            case
            for case in report["cases"]
            if case["model"] == "stale-manifest"
        )
        self.assertEqual(case["result"], "FAIL")
        self.assertEqual(case["observation"]["actual_mode"], "debug")

    def test_rejects_declared_recursion_that_hides_child_plan(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "environment-contracts"
            shutil.copytree(SPECIMENS, specimens)
            makefile = (
                specimens
                / "recursive-boundary"
                / "declared-recursion.mk"
            )
            makefile.write_text(
                makefile.read_text(encoding="utf-8").replace(
                    "+$(MAKE) -C child",
                    "$(MAKE_BIN) -C child",
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
        case = next(
            case
            for case in report["cases"]
            if case["model"] == "declared-recursion"
        )
        self.assertEqual(case["result"], "FAIL")
        self.assertFalse(
            case["observation"]["child_plan_visible_in_dry_run"]
        )

    def test_rejects_contract_gate_that_leaves_residue(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            specimens = root / "environment-contracts"
            shutil.copytree(SPECIMENS, specimens)
            makefile = specimens / "required-tool" / "contract-gate.mk"
            makefile.write_text(
                makefile.read_text(encoding="utf-8").replace(
                    "contract-check:\n",
                    (
                        "contract-check:\n"
                        "> @mkdir -p build\n"
                        "> @: > build/tool-version.txt\n"
                    ),
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
        case = next(
            case
            for case in report["cases"]
            if case["model"] == "contract-gate-missing"
        )
        self.assertEqual(case["result"], "FAIL")
        self.assertTrue(case["observation"]["tool_version_exists"])


if __name__ == "__main__":
    unittest.main()
