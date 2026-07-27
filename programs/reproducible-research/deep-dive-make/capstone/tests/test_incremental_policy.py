from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

CAPSTONE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAPSTONE / "scripts"))

from incremental_policy import read_incremental_policy


class IncrementalPolicyTests(unittest.TestCase):
    def test_reads_requested_work_boundary(self) -> None:
        with TemporaryDirectory() as directory:
            policy = Path(directory) / "policy.tsv"
            policy.write_text("src/a.c\tbuild/a.o,app\tbuild/b.o\n")
            case = read_incremental_policy(policy)[0]
            self.assertEqual(case.input_path.as_posix(), "src/a.c")
            self.assertEqual(case.must_rebuild[0].as_posix(), "build/a.o")

    def test_rejects_conflicting_output_claims(self) -> None:
        with TemporaryDirectory() as directory:
            policy = Path(directory) / "policy.tsv"
            policy.write_text("src/a.c\tapp\tapp\n")
            with self.assertRaisesRegex(ValueError, "both rebuilt and unchanged"):
                read_incremental_policy(policy)


if __name__ == "__main__":
    unittest.main()
