from __future__ import annotations

import unittest

from api_reliability.health import ComponentHealth, HealthEvaluator, LifecyclePhase
from api_reliability.metrics import MetricDescriptor, MetricError, MetricRegistry


class MetricsHealthTests(unittest.TestCase):
    def test_cardinality_budget_is_enforced(self) -> None:
        registry = MetricRegistry()
        counter = registry.counter(
            MetricDescriptor("requests_total", "requests", "{request}", ("route",), 2)
        )
        counter.add(labels={"route": "/a"})
        counter.add(labels={"route": "/b"})
        with self.assertRaises(MetricError):
            counter.add(labels={"route": "/c"})

    def test_draining_is_live_but_not_ready(self) -> None:
        snapshot = HealthEvaluator().evaluate(
            phase=LifecyclePhase.DRAINING,
            startup_complete=True,
            event_loop_progressing=True,
            components=[ComponentHealth("postgres", True, True)],
        )
        self.assertTrue(snapshot.live)
        self.assertFalse(snapshot.ready)
        self.assertIn("draining", snapshot.reasons)


if __name__ == "__main__":
    unittest.main()
