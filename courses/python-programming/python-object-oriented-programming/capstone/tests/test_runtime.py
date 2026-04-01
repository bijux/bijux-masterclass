from __future__ import annotations

from datetime import datetime

import pytest

from service_monitoring import (
    CollectingIncidentSink,
    MetricName,
    MetricSample,
    MonitoringPolicy,
    MonitoringRuntime,
    Severity,
    StaticMetricSource,
    ThresholdRule,
)


def build_runtime_policy() -> MonitoringPolicy:
    policy = MonitoringPolicy("policy-runtime")
    policy.add_rule(
        ThresholdRule(
            rule_id="cpu-hot",
            metric_name=MetricName("cpu"),
            threshold=0.9,
            severity=Severity("critical"),
        )
    )
    policy.add_rule(
        ThresholdRule(
            rule_id="cpu-sustained",
            metric_name=MetricName("cpu"),
            threshold=0.8,
            severity=Severity("warning"),
            window=3,
            evaluation_mode="consecutive",
        )
    )
    return policy


def test_runtime_coordinates_activation_projection_and_alert_publication() -> None:
    runtime = MonitoringRuntime(sink=CollectingIncidentSink())
    runtime.register_policy(build_runtime_policy())

    runtime.activate_rule("policy-runtime", "cpu-hot")
    runtime.activate_rule("policy-runtime", "cpu-sustained")

    report = runtime.run_source(
        "policy-runtime",
        StaticMetricSource(
            [
                MetricSample(datetime(2026, 4, 1, 15, 0, 0), MetricName("cpu"), 0.81),
                MetricSample(datetime(2026, 4, 1, 15, 1, 0), MetricName("cpu"), 0.92),
                MetricSample(datetime(2026, 4, 1, 15, 2, 0), MetricName("cpu"), 0.95),
            ]
        ),
    )
    snapshot = runtime.snapshot()

    assert report.alerts_published == 2
    assert report.active_rule_count == 2
    assert snapshot["active_rule_index"] == {"cpu": ("cpu-hot", "cpu-sustained")}
    assert len(snapshot["incident_history"]["cpu"]) == 2
    assert set(snapshot["open_incidents"]) == {"cpu-hot", "cpu-sustained"}


def test_runtime_retirement_updates_read_models() -> None:
    runtime = MonitoringRuntime()
    runtime.register_policy(build_runtime_policy())
    runtime.activate_rule("policy-runtime", "cpu-hot")
    runtime.run_cycle(
        "policy-runtime",
        [MetricSample(datetime(2026, 4, 1, 16, 0, 0), MetricName("cpu"), 0.97)],
    )

    assert "cpu-hot" in runtime.snapshot()["open_incidents"]

    runtime.retire_rule("policy-runtime", "cpu-hot", "service replaced")
    snapshot = runtime.snapshot()

    assert snapshot["active_rule_index"] == {}
    assert snapshot["open_incidents"] == {}


def test_runtime_rolls_back_projection_updates_when_sink_fails() -> None:
    class FailingSink:
        def publish(self, alerts):
            raise RuntimeError("notification backend unavailable")

    runtime = MonitoringRuntime(sink=FailingSink())
    runtime.register_policy(build_runtime_policy())
    runtime.activate_rule("policy-runtime", "cpu-hot")

    with pytest.raises(RuntimeError):
        runtime.run_cycle(
            "policy-runtime",
            [MetricSample(datetime(2026, 4, 1, 17, 0, 0), MetricName("cpu"), 0.99)],
        )

    snapshot = runtime.snapshot()
    assert snapshot["open_incidents"] == {}
    assert snapshot["incident_history"] == {}
