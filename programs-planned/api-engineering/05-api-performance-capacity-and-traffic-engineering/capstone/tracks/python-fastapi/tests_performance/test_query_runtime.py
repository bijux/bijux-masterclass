from __future__ import annotations

import unittest

from api_performance.db_budget import ConnectionBudget, pool_utilization
from api_performance.profiling import profile_callable
from api_performance.query_plans import compare_plans, summarize_plan
from api_performance.runtime import cpu_fraction, measure_callable


BEFORE = [
    {
        "Plan": {
            "Node Type": "Limit",
            "Plan Rows": 50,
            "Actual Rows": 50,
            "Shared Hit Blocks": 10,
            "Shared Read Blocks": 100,
            "Plans": [
                {
                    "Node Type": "Sort",
                    "Plan Rows": 10000,
                    "Actual Rows": 10000,
                    "Sort Method": "external merge Disk",
                    "Shared Hit Blocks": 10,
                    "Shared Read Blocks": 100,
                    "Temp Read Blocks": 20,
                    "Temp Written Blocks": 30,
                    "Plans": [
                        {
                            "Node Type": "Seq Scan",
                            "Relation Name": "analysis_runs",
                            "Plan Rows": 10000,
                            "Actual Rows": 10000,
                            "Shared Hit Blocks": 10,
                            "Shared Read Blocks": 100,
                        }
                    ],
                }
            ],
        }
    }
]

AFTER = [
    {
        "Plan": {
            "Node Type": "Limit",
            "Plan Rows": 50,
            "Actual Rows": 50,
            "Shared Hit Blocks": 20,
            "Shared Read Blocks": 2,
            "Plans": [
                {
                    "Node Type": "Index Scan",
                    "Index Name": "idx_runs_owner_status_created_id",
                    "Plan Rows": 50,
                    "Actual Rows": 50,
                    "Shared Hit Blocks": 20,
                    "Shared Read Blocks": 2,
                }
            ],
        }
    }
]


class PlanTests(unittest.TestCase):
    def test_plan_summary(self) -> None:
        before = summarize_plan(BEFORE)
        self.assertEqual(before.actual_rows, 50)
        self.assertEqual(before.sequential_scans, ("analysis_runs",))
        self.assertEqual(before.disk_sorts, 1)
        self.assertEqual(before.temp_written_blocks, 30)

    def test_plan_comparison(self) -> None:
        before = summarize_plan(BEFORE)
        after = summarize_plan(AFTER)
        comparison = compare_plans(before, after)
        self.assertLess(comparison.read_block_delta, 0)
        self.assertEqual(comparison.removed_sequential_scans, ("analysis_runs",))
        self.assertIn("idx_runs_owner_status_created_id", comparison.added_indexes)

    def test_connection_budget(self) -> None:
        budget = ConnectionBudget(8, 20, 4, 5, 10)
        self.assertEqual(budget.possible_connections, 190)
        self.assertTrue(budget.fits(200))
        self.assertFalse(budget.fits(180))

    def test_pool_utilization(self) -> None:
        self.assertEqual(pool_utilization(7, 10), 0.7)


class RuntimeTests(unittest.TestCase):
    def test_measure_callable(self) -> None:
        value, sample = measure_callable(lambda: sum(range(10_000)))
        self.assertEqual(value, 49_995_000)
        self.assertGreater(sample.wall_ns, 0)
        self.assertGreater(sample.cpu_ns, 0)
        self.assertGreaterEqual(cpu_fraction(sample), 0)

    def test_allocation_measurement(self) -> None:
        value, sample = measure_callable(
            lambda: [str(index) for index in range(1000)],
            measure_python_allocations=True,
        )
        self.assertEqual(len(value), 1000)
        self.assertIsNotNone(sample.allocated_peak_bytes)
        self.assertGreater(sample.allocated_peak_bytes or 0, 0)

    def test_profile_report(self) -> None:
        result = profile_callable(lambda: sum(range(1000)), limit=5)
        self.assertEqual(result.value, 499500)
        self.assertIn("function calls", result.report)


if __name__ == "__main__":
    unittest.main()
