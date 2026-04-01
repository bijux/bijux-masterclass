from __future__ import annotations

from datetime import datetime

from service_monitoring import (
    AlertTriggered,
    MetricName,
    MetricSample,
    MonitoringPolicy,
    Severity,
    ThresholdRule,
)


def test_policy_evaluates_active_rules_and_emits_alerts() -> None:
    policy = MonitoringPolicy("policy-101")
    policy.add_rule(
        ThresholdRule(
            rule_id="cpu-hot",
            metric_name=MetricName("cpu"),
            threshold=0.9,
            severity=Severity("critical"),
            window=2,
        )
    )
    policy.activate_rule("cpu-hot")
    policy.collect_events()

    alerts = policy.evaluate(
        [
            MetricSample(datetime(2026, 4, 1, 10, 0, 0), MetricName("cpu"), 0.72),
            MetricSample(datetime(2026, 4, 1, 10, 1, 0), MetricName("cpu"), 0.93),
            MetricSample(datetime(2026, 4, 1, 10, 1, 0), MetricName("memory"), 0.50),
        ]
    )

    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.rule_id == "cpu-hot"
    assert alert.observed_value == 0.93
    assert alert.incident_id.startswith("policy-101:cpu-hot:")

    events = policy.collect_events()
    assert isinstance(events[0], AlertTriggered)
    assert events[0].observed_value == 0.93


def test_policy_ignores_draft_and_retired_rules_during_evaluation() -> None:
    policy = MonitoringPolicy("policy-102")
    policy.add_rule(
        ThresholdRule(
            rule_id="disk-hot",
            metric_name=MetricName("disk"),
            threshold=0.8,
            severity=Severity("warning"),
        )
    )
    policy.collect_events()

    assert policy.evaluate(
        [MetricSample(datetime(2026, 4, 1, 11, 0, 0), MetricName("disk"), 0.95)]
    ) == []

    policy.activate_rule("disk-hot")
    policy.retire_rule("disk-hot", "using filesystem saturation policy instead")
    policy.collect_events()

    assert policy.evaluate(
        [MetricSample(datetime(2026, 4, 1, 11, 5, 0), MetricName("disk"), 0.99)]
    ) == []
