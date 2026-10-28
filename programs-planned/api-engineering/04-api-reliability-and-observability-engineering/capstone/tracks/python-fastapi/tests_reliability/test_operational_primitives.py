from __future__ import annotations

import json
import unittest

from api_reliability.alerts import BurnRateAlert
from api_reliability.circuit import CircuitBreaker, CircuitState
from api_reliability.clock import ManualClock
from api_reliability.metrics import MetricDescriptor, MetricError, MetricRegistry
from api_reliability.runbooks import parse_runbook
from api_reliability.telemetry import InMemoryEventSink, StructuredLogger


class OperationalPrimitiveTests(unittest.TestCase):
    def test_histogram_is_cumulative_and_renderable(self) -> None:
        registry = MetricRegistry()
        histogram = registry.histogram(
            MetricDescriptor(
                name="analysis_duration_seconds",
                description="Observed duration",
                unit="s",
                labels=("operation",),
            ),
            (0.1, 0.5, 1.0),
        )
        histogram.observe(0.3, labels={"operation": "startAnalysis"})
        histogram.observe(2.0, labels={"operation": "startAnalysis"})
        point = next(iter(histogram.values.values()))
        self.assertEqual(point.buckets, [0, 1, 1, 2])
        output = registry.render_prometheus()
        self.assertIn('le="0.5"} 1', output)
        self.assertIn('le="+Inf"} 2', output)

    def test_metric_descriptor_rejects_duplicate_labels(self) -> None:
        with self.assertRaises(MetricError):
            MetricDescriptor("valid_name", "description", "1", ("a", "a"))

    def test_canceled_half_open_probe_reopens(self) -> None:
        clock = ManualClock(0)
        breaker = CircuitBreaker(1, 100)
        breaker.failure(clock)
        clock.advance(100)
        breaker.allow(clock)
        self.assertEqual(breaker.state, CircuitState.HALF_OPEN)
        breaker.abandon_probe(clock)
        self.assertEqual(breaker.state, CircuitState.OPEN)

    def test_alert_rejects_zero_minimum_traffic(self) -> None:
        with self.assertRaises(ValueError):
            BurnRateAlert("bad", "page", 3600, 300, 14.4, 0)

    def test_telemetry_resource_and_bounded_sink(self) -> None:
        sink = InMemoryEventSink(maximum_events=1)
        logger = StructuredLogger(
            clock=ManualClock(10),
            sink=sink,
            service_name="analysis-runs-api",
            service_version="1.3.0",
            deployment_environment="test",
            schema_version="1.0",
        )
        self.assertTrue(logger.emit("worker.job.claimed"))
        self.assertFalse(logger.emit("worker.job.completed"))
        self.assertEqual(sink.dropped, 1)
        payload = json.loads(sink.events[0].to_json())
        self.assertEqual(payload["deployment_environment"], "test")
        self.assertEqual(payload["schema_version"], "1.0")

    def test_runbook_requires_operational_stop_and_closure_fields(self) -> None:
        with self.assertRaises(ValueError):
            parse_runbook({"id": "RB-X"})


if __name__ == "__main__":
    unittest.main()
