from __future__ import annotations

from decimal import Decimal
import unittest

from api_performance.capacity import (
    ResourceCapacity,
    WorkloadDemand,
    backlog_drain_seconds,
    cpu_demand,
    evaluate_capacity,
    storage_bytes,
    utilization_from_demand,
)
from api_performance.cost import cost_per_useful_completion
from api_performance.release import evaluate_release
from api_performance.regression import MetricPolicy, evaluate_metric
from api_performance.shedding import ResourceSignals, choose_shedding
from api_performance.traffic import (
    LimiterRegistry,
    TokenBucket,
    reserve_atomically,
)


class TrafficTests(unittest.TestCase):
    def test_bucket_refill(self) -> None:
        bucket = TokenBucket(
            capacity=10_000_000,
            refill_per_second=2_000_000,
            initial_tokens=5_000_000,
        )
        first = bucket.consume(0, 5_000_000)
        self.assertTrue(first.allowed)
        self.assertEqual(first.remaining, 0)
        second = bucket.consume(2_000_000_000, 5_000_000)
        self.assertFalse(second.allowed)
        self.assertEqual(second.remaining, 4_000_000)
        self.assertEqual(second.retry_after_ns, 500_000_000)

    def test_atomic_rollback(self) -> None:
        global_bucket = TokenBucket(capacity=10, refill_per_second=1)
        tenant_bucket = TokenBucket(
            capacity=2,
            refill_per_second=1,
            initial_tokens=0,
        )
        before = global_bucket.state
        result = reserve_atomically(
            ((global_bucket, 5), (tenant_bucket, 1)),
            now_ns=0,
        )
        self.assertFalse(result.allowed)
        self.assertEqual(global_bucket.state, before)

    def test_registry_is_bounded(self) -> None:
        registry = LimiterRegistry(
            max_keys=2,
            idle_ttl_ns=10,
            capacity=10,
            refill_per_second=1,
        )
        registry.bucket("a", now_ns=0)
        registry.bucket("b", now_ns=0)
        with self.assertRaises(RuntimeError):
            registry.bucket("c", now_ns=1)
        registry.bucket("c", now_ns=10)
        self.assertEqual(registry.size, 1)

    def test_shedding_order(self) -> None:
        normal = choose_shedding(ResourceSignals(0.2, 0.2, 0.2, True, True))
        self.assertEqual(normal.stage, 0)
        pressure = choose_shedding(ResourceSignals(0.9, 0.2, 0.2, True, True))
        self.assertEqual(pressure.stage, 1)
        unavailable = choose_shedding(
            ResourceSignals(0.1, 0.1, 0.1, True, False)
        )
        self.assertEqual(unavailable.stage, 5)
        self.assertIn("getRun", unavailable.allowed_operations)
        self.assertNotIn("submitRun", unavailable.allowed_operations)


class CapacityTests(unittest.TestCase):
    def test_cpu_demand(self) -> None:
        result = cpu_demand(
            cores=Decimal("4"),
            utilization=Decimal("0.60"),
            interval_seconds=Decimal("60"),
            completions=Decimal("12000"),
        )
        self.assertEqual(result, Decimal("0.012"))

    def test_utilization(self) -> None:
        result = utilization_from_demand(
            arrival_rate=Decimal("100"),
            demand_per_completion=Decimal("0.005"),
            capacity_units=Decimal("1"),
        )
        self.assertEqual(result, Decimal("0.500"))

    def test_backlog_drain(self) -> None:
        self.assertEqual(
            backlog_drain_seconds(
                backlog=Decimal("18000"),
                completion_rate=Decimal("140"),
                arrival_rate=Decimal("100"),
            ),
            Decimal("450"),
        )
        with self.assertRaises(ValueError):
            backlog_drain_seconds(
                backlog=Decimal("1"),
                completion_rate=Decimal("10"),
                arrival_rate=Decimal("10"),
            )

    def test_capacity_first_bottleneck(self) -> None:
        workloads = (
            WorkloadDemand(
                id="reads",
                rate_per_second=Decimal("100"),
                resource_demand={
                    "cpu": Decimal("0.005"),
                    "db": Decimal("0.008"),
                },
            ),
            WorkloadDemand(
                id="writes",
                rate_per_second=Decimal("10"),
                resource_demand={
                    "cpu": Decimal("0.01"),
                    "db": Decimal("0.03"),
                },
            ),
        )
        resources = (
            ResourceCapacity("cpu", Decimal("2"), Decimal("0.70")),
            ResourceCapacity("db", Decimal("1"), Decimal("0.70")),
        )
        result = evaluate_capacity(workloads, resources)
        self.assertEqual(result.first_bottleneck, "db")

    def test_storage(self) -> None:
        self.assertEqual(
            storage_bytes(
                daily_objects=Decimal("10"),
                mean_object_bytes=Decimal("100"),
                retention_days=Decimal("30"),
                replication_factor=Decimal("2"),
                overhead_fraction=Decimal("0.1"),
            ),
            Decimal("66000.0"),
        )

    def test_cost(self) -> None:
        result = cost_per_useful_completion(
            total_cost=Decimal("25"),
            useful_completions=Decimal("1000"),
        )
        self.assertEqual(result.cost_per_completion, Decimal("0.025"))


POLICY = {
    "metrics": [
        {
            "name": "p95Ms",
            "direction": "lower",
            "absoluteRegression": "5",
            "relativeRegression": "0.05",
            "hardMaximum": "200",
        },
        {
            "name": "throughputPerSecond",
            "direction": "higher",
            "absoluteRegression": "5",
            "relativeRegression": "0.03",
            "hardMinimum": "50",
        },
        {
            "name": "peakMemoryBytes",
            "direction": "lower",
            "absoluteRegression": "1000000",
            "relativeRegression": "0.05",
            "hardMaximum": "536870912",
        },
    ]
}


def envelope(
    *,
    workload_hash: str = "sha256:w",
    environment_hash: str = "sha256:e",
    correct: bool = True,
    started: int = 100,
    missing: int = 0,
    p95: str = "100",
    throughput: str = "100",
    memory: str = "100000000",
) -> dict[str, object]:
    return {
        "profileVersion": "1.0",
        "workloadHash": workload_hash,
        "environmentHash": environment_hash,
        "correctness": {"passed": correct},
        "outcomes": {
            "offered": 100,
            "started": started,
            "admitted": 100,
            "completed": 100 - missing,
            "rejected": 0,
            "failed": 0,
            "missing": missing,
        },
        "summary": {
            "p95Ms": p95,
            "throughputPerSecond": throughput,
            "peakMemoryBytes": memory,
        },
    }


class ReleaseTests(unittest.TestCase):
    def test_metric_rule(self) -> None:
        policy = MetricPolicy(
            name="p95Ms",
            direction="lower",
            absolute_regression=Decimal("5"),
            relative_regression=Decimal("0.05"),
        )
        self.assertTrue(evaluate_metric(Decimal("100"), Decimal("104"), policy).passed)
        self.assertFalse(evaluate_metric(Decimal("100"), Decimal("110"), policy).passed)

    def test_accepted(self) -> None:
        decision = evaluate_release(
            envelope(),
            envelope(p95="90", throughput="110", memory="95000000"),
            POLICY,
        )
        self.assertEqual(decision.status, "accepted")
        self.assertEqual(decision.gates[0].name, "comparability")
        self.assertEqual(decision.gates[1].name, "correctness")

    def test_correctness_rejected(self) -> None:
        decision = evaluate_release(envelope(), envelope(correct=False), POLICY)
        self.assertEqual(decision.status, "rejected")
        self.assertEqual(decision.gates[1].status, "failed")

    def test_coverage_rejected(self) -> None:
        decision = evaluate_release(
            envelope(),
            envelope(started=99, missing=1),
            POLICY,
        )
        self.assertEqual(decision.status, "rejected")
        self.assertEqual(decision.gates[2].status, "failed")

    def test_incomparable_is_inconclusive(self) -> None:
        decision = evaluate_release(
            envelope(),
            envelope(environment_hash="sha256:other"),
            POLICY,
        )
        self.assertEqual(decision.status, "inconclusive")

    def test_metric_regression_rejected(self) -> None:
        decision = evaluate_release(
            envelope(),
            envelope(p95="130", throughput="80", memory="600000000"),
            POLICY,
        )
        self.assertEqual(decision.status, "rejected")
        self.assertEqual(decision.gates[-1].status, "failed")


if __name__ == "__main__":
    unittest.main()
