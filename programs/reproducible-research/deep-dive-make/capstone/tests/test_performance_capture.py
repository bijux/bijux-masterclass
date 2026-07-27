from __future__ import annotations

import json
import stat
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE_ROOT / "scripts" / "collect_performance_evidence.py"


SUCCESSFUL_MAKE = """#!/bin/sh
set -eu
if [ "${1:-}" = "--version" ]; then
  printf '%s\\n' 'GNU Make 4.4 (performance test double)'
  exit 0
fi
case " $* " in
  *" clean "*)
    find . -type f \\( -path './all' -o -path './app' -o -path './build/*' \\) -delete
    exit 0
    ;;
  *" -q "*)
    test -f all && test -f app && test -f build/bin/dyn1 &&
      test -f build/bin/dyn2 && test -f build/include/dynamic.h
    exit
    ;;
  *" -n "*)
    printf '%s\\n' 'cc -o app'
    exit 0
    ;;
esac
mkdir -p build/bin build/include
printf '%s\\n' all > all
printf '%s\\n' app > app
printf '%s\\n' dyn1 > build/bin/dyn1
printf '%s\\n' dyn2 > build/bin/dyn2
printf '%s\\n' header > build/include/dynamic.h
"""


FAILING_MAKE = """#!/bin/sh
set -eu
if [ "${1:-}" = "--version" ]; then
  printf '%s\\n' 'GNU Make 4.4 (failing performance test double)'
  exit 0
fi
case " $* " in
  *" clean "*) exit 0 ;;
esac
printf '%s\\n' 'controlled route failure' >&2
exit 7
"""


class PerformanceCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.owned_directory = TemporaryDirectory()
        self.workspace = Path(self.owned_directory.name)
        self.policy = self.workspace / "scenarios.tsv"
        self.policy.write_text("clean-build\tclean\t2\tall\n", encoding="utf-8")
        self.incremental = self.workspace / "incremental-work.json"
        self.incremental.write_text(
            json.dumps(
                {
                    "expected_rebuild": ["app"],
                    "input": "src/util.c",
                    "missing_rebuild": [],
                    "observed_rebuild": ["app"],
                    "policy_sha256": "incremental-policy-digest",
                    "result": "PASS",
                    "schema": "deep-dive-make-incremental-work-v1",
                    "trace": "omitted from combined evidence",
                    "unexpected_rebuild": [],
                }
            ),
            encoding="utf-8",
        )
        self.output = self.workspace / "evidence" / "evidence.json"

    def tearDown(self) -> None:
        self.owned_directory.cleanup()

    def write_make(self, source: str) -> Path:
        make = self.workspace / "make-double"
        make.write_text(source, encoding="utf-8")
        make.chmod(make.stat().st_mode | stat.S_IXUSR)
        return make

    def collect(
        self, make: Path, *, samples: int = 3
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--policy",
                str(self.policy),
                "--output",
                str(self.output),
                "--samples",
                str(samples),
                "--make",
                str(make),
                "--incremental-evidence",
                str(self.incremental),
                "--workspace",
                str(self.workspace),
            ],
            cwd=self.workspace,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_captures_all_samples_and_semantic_evidence(self) -> None:
        result = self.collect(self.write_make(SUCCESSFUL_MAKE))

        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(self.output.read_text(encoding="utf-8"))
        scenario = evidence["scenarios"]["clean-build"]
        self.assertEqual(evidence["result"], "PASS")
        self.assertEqual(evidence["context"]["make"]["version"], "GNU Make 4.4 (performance test double)")
        self.assertEqual(evidence["context"]["repository"]["status"], "unavailable")
        self.assertEqual(evidence["context"]["runner"], "local")
        self.assertIn("version", evidence["context"]["compiler"])
        self.assertEqual(evidence["incremental_work"]["result"], "PASS")
        self.assertNotIn("trace", evidence["incremental_work"])
        self.assertEqual(len(scenario["samples"]), 3)
        self.assertEqual(scenario["convergence"], "PASS")
        self.assertEqual(len(scenario["inventory"]), 5)
        self.assertTrue((self.output.parent / "summary.tsv").is_file())
        self.assertTrue((self.output.parent / "logs" / "clean-build.txt").is_file())

    def test_rejects_too_few_samples_before_execution(self) -> None:
        result = self.collect(self.write_make(SUCCESSFUL_MAKE), samples=2)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least 3", result.stderr)
        self.assertFalse(self.output.exists())

    def test_preserves_failed_scenario_as_failed_evidence(self) -> None:
        result = self.collect(self.write_make(FAILING_MAKE))

        self.assertNotEqual(result.returncode, 0)
        evidence = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(evidence["result"], "FAIL")
        self.assertIn("status 7", evidence["failure"])
        self.assertFalse((self.output.parent / "summary.tsv").exists())

    def test_rejects_failed_incremental_evidence_before_timing(self) -> None:
        report = json.loads(self.incremental.read_text(encoding="utf-8"))
        report["result"] = "FAIL"
        self.incremental.write_text(json.dumps(report), encoding="utf-8")

        result = self.collect(self.write_make(SUCCESSFUL_MAKE))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incremental evidence did not pass", result.stderr)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
