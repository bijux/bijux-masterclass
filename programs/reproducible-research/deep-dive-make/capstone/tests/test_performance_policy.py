from __future__ import annotations

import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAPSTONE_ROOT / "scripts"))

from performance_policy import read_performance_policy  # noqa: E402


class PerformancePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.owned_directory = TemporaryDirectory()
        self.policy = Path(self.owned_directory.name) / "scenarios.tsv"

    def tearDown(self) -> None:
        self.owned_directory.cleanup()

    def write_policy(self, text: str) -> None:
        self.policy.write_text(text, encoding="utf-8")

    def test_reads_explicit_scenario_contract(self) -> None:
        self.write_policy("converged-noop\tconverged\t1\tall\n")

        scenarios = read_performance_policy(self.policy)

        self.assertEqual(scenarios[0].name, "converged-noop")
        self.assertEqual(scenarios[0].state, "converged")
        self.assertEqual(scenarios[0].jobs, 1)
        self.assertEqual(scenarios[0].route, "all")

    def test_rejects_duplicate_scenario_names(self) -> None:
        self.write_policy(
            "clean-build\tclean\t4\tall\n"
            "clean-build\tconverged\t1\tall\n"
        )

        with self.assertRaisesRegex(ValueError, "duplicate scenario"):
            read_performance_policy(self.policy)

    def test_rejects_unknown_state(self) -> None:
        self.write_policy("warm-build\twarm\t1\tall\n")

        with self.assertRaisesRegex(ValueError, "unsupported state"):
            read_performance_policy(self.policy)

    def test_rejects_arbitrary_route(self) -> None:
        self.write_policy("custom-command\tconverged\t1\trm-build\n")

        with self.assertRaisesRegex(ValueError, "unsupported route"):
            read_performance_policy(self.policy)

    def test_rejects_nonpositive_job_count(self) -> None:
        self.write_policy("converged-noop\tconverged\t0\tall\n")

        with self.assertRaisesRegex(ValueError, "positive integer"):
            read_performance_policy(self.policy)


if __name__ == "__main__":
    unittest.main()
