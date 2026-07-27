from __future__ import annotations

import gzip
import io
import json
import subprocess
import sys
import tarfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_ROOT = CAPSTONE_ROOT / "scripts"
WORK_ROOT = (
    REPOSITORY_ROOT / "artifacts" / "tests" / "deep-dive-make-release-candidate"
)


class ReleaseCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        WORK_ROOT.mkdir(parents=True, exist_ok=True)
        self.owned_directory = TemporaryDirectory(
            prefix="candidate-", dir=WORK_ROOT
        )
        self.workspace = Path(self.owned_directory.name)
        self.source = self.workspace / "app"
        self.source.write_bytes(b"release payload\n")
        self.policy = self.workspace / "package-policy.tsv"
        self.policy.write_text(
            "deep-dive-make-capstone/app\tapp\t0755\n", encoding="utf-8"
        )
        self.candidate = self.workspace / "candidate.tar.gz"
        self.checksum = self.workspace / "candidate.tar.gz.sha256"
        self.report = self.workspace / "candidate-acceptance.json"

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

    def build_candidate(self) -> None:
        self.run_script(
            "mkdist.py",
            "--policy",
            str(self.policy),
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

    def verify_candidate(self, *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.run_script(
            "verify_release_candidate.py",
            "--candidate",
            str(self.candidate),
            "--checksum",
            str(self.checksum),
            "--policy",
            str(self.policy),
            "--report",
            str(self.report),
            check=check,
        )

    def write_custom_archive(
        self,
        members: list[tuple[str, bytes, int]],
    ) -> None:
        with self.candidate.open("wb") as raw_output:
            with gzip.GzipFile(
                fileobj=raw_output, filename="", mode="wb", mtime=0
            ) as compressed:
                with tarfile.open(fileobj=compressed, mode="w") as archive:
                    for name, payload, mode in members:
                        info = tarfile.TarInfo(name)
                        info.size = len(payload)
                        info.mode = mode
                        info.mtime = 946684800
                        info.uid = 0
                        info.gid = 0
                        info.uname = "root"
                        info.gname = "root"
                        archive.addfile(info, io.BytesIO(payload))
        self.run_script(
            "write_release_checksum.py",
            "--candidate",
            str(self.candidate),
            "--output",
            str(self.checksum),
        )

    def test_accepts_candidate_matching_identity_and_policy(self) -> None:
        self.build_candidate()

        result = self.verify_candidate()

        self.assertIn("PASS:", result.stdout)
        report = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(report["checks"]["identity"], "PASS")
        self.assertEqual(
            report["members"], ["deep-dive-make-capstone/app"]
        )

    def test_rejects_candidate_changed_after_checksum(self) -> None:
        self.build_candidate()
        with self.candidate.open("ab") as handle:
            handle.write(b"unrecorded bytes")

        result = self.verify_candidate(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("identity mismatch", result.stdout)
        self.assertFalse(self.report.exists())

    def test_rejects_undeclared_member(self) -> None:
        self.write_custom_archive(
            [
                ("deep-dive-make-capstone/app", b"release payload\n", 0o755),
                ("deep-dive-make-capstone/debug.log", b"diagnostic\n", 0o644),
            ]
        )

        result = self.verify_candidate(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("member policy mismatch", result.stdout)
        self.assertIn("debug.log", result.stdout)

    def test_rejects_traversal_path_before_extraction(self) -> None:
        self.write_custom_archive(
            [("../escape.txt", b"must not escape\n", 0o644)]
        )

        result = self.verify_candidate(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe archive path", result.stdout)
        self.assertFalse((self.workspace.parent / "escape.txt").exists())

    def test_rejects_mode_drift(self) -> None:
        self.write_custom_archive(
            [("deep-dive-make-capstone/app", b"release payload\n", 0o644)]
        )

        result = self.verify_candidate(check=False)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mode mismatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
