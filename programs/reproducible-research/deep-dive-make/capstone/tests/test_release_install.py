from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_ROOT = CAPSTONE_ROOT / "scripts"
WORK_ROOT = (
    REPOSITORY_ROOT / "artifacts" / "tests" / "deep-dive-make-release-install"
)


class ReleaseInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        WORK_ROOT.mkdir(parents=True, exist_ok=True)
        self.owned_directory = TemporaryDirectory(prefix="install-", dir=WORK_ROOT)
        self.workspace = Path(self.owned_directory.name)
        self.source = self.workspace / "app"
        self.source.write_bytes(b"release payload\n")
        self.package_policy = self.workspace / "package-policy.tsv"
        self.package_policy.write_text(
            "deep-dive-make-capstone/app\tapp\t0755\n", encoding="utf-8"
        )
        self.install_policy = self.workspace / "install-policy.tsv"
        self.install_policy.write_text(
            "deep-dive-make-capstone/app\tusr/local/bin/capstone\t0755\n",
            encoding="utf-8",
        )
        self.candidate = self.workspace / "candidate.tar.gz"
        self.checksum = self.workspace / "candidate.tar.gz.sha256"
        self.candidate_report = self.workspace / "candidate-acceptance.json"
        self.install_report = self.workspace / "install-acceptance.json"
        self.release_report = self.workspace / "release-acceptance.json"
        self.install_root = self.workspace / "install-root"
        self.build_and_verify_candidate()

    def tearDown(self) -> None:
        self.owned_directory.cleanup()

    def run_script(
        self, script_name: str, *arguments: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_ROOT / script_name), *arguments],
            cwd=self.workspace,
            check=check,
            text=True,
            capture_output=True,
        )

    def build_and_verify_candidate(self) -> None:
        self.run_script(
            "mkdist.py",
            "--policy",
            str(self.package_policy),
            "--output",
            str(self.candidate),
        )
        self.run_script(
            "write_release_checksum.py",
            "--candidate",
            str(self.candidate),
            "--output",
            str(self.checksum),
        )
        self.run_script(
            "verify_release_candidate.py",
            "--candidate",
            str(self.candidate),
            "--checksum",
            str(self.checksum),
            "--policy",
            str(self.package_policy),
            "--report",
            str(self.candidate_report),
        )

    def rehearse_install(self, *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.run_script(
            "rehearse_release_install.py",
            "--candidate",
            str(self.candidate),
            "--acceptance",
            str(self.candidate_report),
            "--package-policy",
            str(self.package_policy),
            "--install-policy",
            str(self.install_policy),
            "--root",
            str(self.install_root),
            "--report",
            str(self.install_report),
            check=check,
        )

    def test_archive_bytes_do_not_depend_on_output_basename(self) -> None:
        other_candidate = self.workspace / "renamed-candidate.tar.gz"

        self.run_script(
            "mkdist.py",
            "--policy",
            str(self.package_policy),
            "--output",
            str(other_candidate),
        )

        self.assertEqual(self.candidate.read_bytes(), other_candidate.read_bytes())

    def test_install_rehearsal_converges_across_invocations(self) -> None:
        self.rehearse_install()
        first_report = json.loads(self.install_report.read_text(encoding="utf-8"))

        self.rehearse_install()
        second_report = json.loads(self.install_report.read_text(encoding="utf-8"))

        self.assertEqual(first_report, second_report)
        self.assertEqual(
            first_report["files"][0]["path"], "usr/local/bin/capstone"
        )
        self.assertEqual(first_report["files"][0]["mode"], "0755")

    def test_install_rejects_symbolic_link_ancestor(self) -> None:
        outside = self.workspace / "outside"
        outside.mkdir()
        self.install_root.mkdir()
        (self.install_root / "usr").symlink_to(outside, target_is_directory=True)

        result = self.rehearse_install(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stdout)
        self.assertEqual(list(outside.iterdir()), [])

    def test_install_rejects_unowned_file(self) -> None:
        self.install_root.mkdir()
        (self.install_root / "unowned.txt").write_text("unowned\n", encoding="utf-8")

        result = self.rehearse_install(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unowned paths", result.stdout)

    def test_acceptance_rejects_reports_for_different_bytes(self) -> None:
        self.rehearse_install()
        install_report = json.loads(self.install_report.read_text(encoding="utf-8"))
        install_report["sha256"] = "0" * 64
        self.install_report.write_text(
            json.dumps(install_report), encoding="utf-8"
        )

        result = self.run_script(
            "write_release_acceptance.py",
            "--candidate-report",
            str(self.candidate_report),
            "--install-report",
            str(self.install_report),
            "--output",
            str(self.release_report),
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("different bytes", result.stdout)
        self.assertFalse(self.release_report.exists())


if __name__ == "__main__":
    unittest.main()
