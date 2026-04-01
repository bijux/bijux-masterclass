from __future__ import annotations

from datetime import datetime

import pytest

from service_monitoring import (
    ActiveRuleIndex,
    DomainError,
    IncidentLedger,
    MetricName,
    MetricSample,
    MonitoringPolicy,
    RuleActivated,
    RuleRegistered,
    RuleRetired,
    Severity,
    ThresholdRule,
)


def test_policy_emits_events_for_registration_activation_and_retirement() -> None:
    policy = MonitoringPolicy("policy-001")
    rule = ThresholdRule(
        rule_id="cpu-hot",
        metric_name=MetricName("cpu"),
        threshold=0.9,
        severity=Severity("critical"),
        window=2,
    )

    policy.add_rule(rule, occurred_at=datetime(2026, 4, 1, 9, 0, 0))
    policy.activate_rule("cpu-hot", occurred_at=datetime(2026, 4, 1, 9, 1, 0))
    policy.retire_rule("cpu-hot", "replaced by latency rule", occurred_at=datetime(2026, 4, 1, 9, 2, 0))

    events = policy.collect_events()

    assert isinstance(events[0], RuleRegistered)
    assert isinstance(events[1], RuleActivated)
    assert isinstance(events[2], RuleRetired)
    assert policy.collect_events() == []


def test_policy_blocks_duplicate_active_metric_window_signatures() -> None:
    policy = MonitoringPolicy("policy-002")
    first = ThresholdRule(
        rule_id="cpu-hot",
        metric_name=MetricName("cpu"),
        threshold=0.8,
        severity=Severity("warning"),
        window=3,
    )
    second = ThresholdRule(
        rule_id="cpu-hotter",
        metric_name=MetricName("cpu"),
        threshold=0.95,
        severity=Severity("critical"),
        window=3,
    )

    policy.add_rule(first)
    policy.add_rule(second)
    policy.activate_rule("cpu-hot")

    with pytest.raises(DomainError):
        policy.activate_rule("cpu-hotter")


def test_active_rule_projection_tracks_lifecycle_events() -> None:
    policy = MonitoringPolicy("policy-003")
    projection = ActiveRuleIndex()
    rule = ThresholdRule(
        rule_id="mem-hot",
        metric_name=MetricName("memory"),
        threshold=0.85,
        severity=Severity("warning"),
    )

    policy.add_rule(rule)
    for event in policy.collect_events():
        projection.apply(event)
    assert projection.snapshot() == {}

    policy.activate_rule("mem-hot")
    for event in policy.collect_events():
        projection.apply(event)
    assert projection.snapshot() == {"memory": ("mem-hot",)}

    policy.retire_rule("mem-hot", "service retired")
    for event in policy.collect_events():
        projection.apply(event)
    assert projection.snapshot() == {}


def test_retiring_a_rule_closes_open_incidents_in_the_read_model() -> None:
    policy = MonitoringPolicy("policy-004")
    ledger = IncidentLedger()
    rule = ThresholdRule(
        rule_id="queue-hot",
        metric_name=MetricName("queue"),
        threshold=0.7,
        severity=Severity("warning"),
    )
    policy.add_rule(rule)
    policy.activate_rule("queue-hot")
    policy.collect_events()
    policy.evaluate(
        [MetricSample(datetime(2026, 4, 1, 9, 30, 0), MetricName("queue"), 0.9)]
    )
    for event in policy.collect_events():
        ledger.apply(event)

    assert "queue-hot" in ledger.open_incidents()

    policy.retire_rule("queue-hot", "queue moved to dedicated service")
    for event in policy.collect_events():
        ledger.apply(event)

    assert ledger.open_incidents() == {}
