from __future__ import annotations

import unittest

from api_performance.statistics import (
    StatisticsError,
    bootstrap_mean_difference,
    nearest_rank,
    summarize,
)
from api_performance.workload import (
    coverage,
    estimated_closed_throughput,
    open_schedule,
)


class StatisticsTests(unittest.TestCase):
    def test_nearest_rank(self) -> None:
        values = [2, 4, 4, 8, 20]
        self.assertEqual(nearest_rank(values, 0.5), 4)
        self.assertEqual(nearest_rank(values, 0.9), 20)

    def test_summary(self) -> None:
        result = summarize([1, 2, 3, 4])
        self.assertEqual(result.count, 4)
        self.assertEqual(result.p50, 2)
        self.assertEqual(result.p95, 4)
        self.assertEqual(result.quantile_algorithm, "nearest-rank")

    def test_invalid_samples(self) -> None:
        with self.assertRaises(StatisticsError):
            summarize([])
        with self.assertRaises(StatisticsError):
            summarize([1, float("inf")])

    def test_bootstrap_is_deterministic(self) -> None:
        a = bootstrap_mean_difference([100, 105, 110], [90, 92, 94], resamples=500, seed=7)
        b = bootstrap_mean_difference([100, 105, 110], [90, 92, 94], resamples=500, seed=7)
        self.assertEqual(a, b)
        self.assertLess(a.estimate, 0)


class WorkloadTests(unittest.TestCase):
    def test_open_schedule_count(self) -> None:
        arrivals = open_schedule(100, 2)
        self.assertEqual(len(arrivals), 200)
        self.assertEqual(arrivals[1].scheduled_ns, 10_000_000)

    def test_closed_throughput(self) -> None:
        self.assertEqual(estimated_closed_throughput(40, 0.3, 0.2), 80)

    def test_schedule_coverage(self) -> None:
        arrivals = open_schedule(10, 1)
        starts = {item.sequence: item.scheduled_ns + 5 for item in arrivals[:-1]}
        result = coverage(arrivals, starts, delay_threshold_ns=4)
        self.assertEqual(result.offered, 10)
        self.assertEqual(result.started, 9)
        self.assertEqual(result.delayed, 9)


if __name__ == "__main__":
    unittest.main()
