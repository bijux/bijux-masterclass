from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE / "scripts" / "capture_incremental_work.py"
POLICY = CAPSTONE / "performance" / "incremental-policy.tsv"


class IncrementalWorkTests(unittest.TestCase):
    def run_case(self, policy: Path, output: Path) -> subprocess.CompletedProcess[str]:
        make = shutil.which("gmake") or shutil.which("make")
        assert make
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--policy",
                str(policy),
                "--output",
                str(output),
                "--make",
                make,
            ],
            cwd=CAPSTONE,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_captures_expected_scope_and_restores_source(self) -> None:
        source = CAPSTONE / "src" / "util.c"
        before = source.stat().st_mtime_ns
        with TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            result = self.run_case(POLICY, output)
            report = json.loads(output.read_text())
            summary = (output.parent / "incremental-summary.tsv").read_text()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["schema"], "deep-dive-make-incremental-work-v2")
        self.assertEqual(len(report["cases"]), 5)
        self.assertEqual(
            report["policy_sha256"], hashlib.sha256(POLICY.read_bytes()).hexdigest()
        )
        self.assertIn("input\tresult\texpected_rebuild", summary)
        self.assertIn("src/util.c\tPASS", summary)
        self.assertIn("include/util.h\tPASS", summary)
        self.assertIn("include/sub.h\tPASS", summary)
        self.assertIn("scripts/gen_dynamic_h.py\tPASS", summary)
        self.assertIn("src/dynamic/dyn1.c\tPASS", summary)
        self.assertEqual(source.stat().st_mtime_ns, before)

    def test_rejects_missing_requested_work(self) -> None:
        with TemporaryDirectory() as directory:
            policy = Path(directory) / "policy.tsv"
            policy.write_text("src/util.c\tbuild/util.o,build/bin/dyn1\tapp,all\n")
            output = Path(directory) / "evidence.json"
            result = self.run_case(policy, output)
            report = json.loads(output.read_text())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("build/bin/dyn1", report["cases"][0]["missing_rebuild"])


if __name__ == "__main__":
    unittest.main()
