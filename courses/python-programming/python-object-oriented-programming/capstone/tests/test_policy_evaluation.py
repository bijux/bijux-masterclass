from __future__ import annotations

from datetime import datetime

from service_monitoring import (
    AlertTriggered,
    IncidentLedger,
    MetricName,
    MetricSample,
    MonitoringPolicy,
    RateOfChangePolicy,
    RuleEvaluator,
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


def test_policy_supports_consecutive_breach_rules() -> None:
    policy = MonitoringPolicy("policy-103")
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
    policy.activate_rule("cpu-sustained")
    policy.collect_events()

    missed = policy.evaluate(
        [
            MetricSample(datetime(2026, 4, 1, 12, 0, 0), MetricName("cpu"), 0.81),
            MetricSample(datetime(2026, 4, 1, 12, 1, 0), MetricName("cpu"), 0.79),
            MetricSample(datetime(2026, 4, 1, 12, 2, 0), MetricName("cpu"), 0.84),
        ]
    )
    hit = policy.evaluate(
        [
            MetricSample(datetime(2026, 4, 1, 12, 3, 0), MetricName("cpu"), 0.81),
            MetricSample(datetime(2026, 4, 1, 12, 4, 0), MetricName("cpu"), 0.82),
            MetricSample(datetime(2026, 4, 1, 12, 5, 0), MetricName("cpu"), 0.84),
        ]
    )

    assert missed == []
    assert len(hit) == 1


def test_policy_supports_rate_of_change_rules() -> None:
    evaluator = RuleEvaluator(policies=[RateOfChangePolicy()])
    policy = MonitoringPolicy("policy-104")
    policy.add_rule(
        ThresholdRule(
            rule_id="latency-spike",
            metric_name=MetricName("latency"),
            threshold=0.2,
            severity=Severity("critical"),
            window=3,
            evaluation_mode="rate_of_change",
        )
    )
    policy.activate_rule("latency-spike")
    policy.collect_events()

    alerts = policy.evaluate(
        [
            MetricSample(datetime(2026, 4, 1, 13, 0, 0), MetricName("latency"), 0.35),
            MetricSample(datetime(2026, 4, 1, 13, 1, 0), MetricName("latency"), 0.40),
            MetricSample(datetime(2026, 4, 1, 13, 2, 0), MetricName("latency"), 0.61),
        ],
        evaluator=evaluator,
    )

    assert len(alerts) == 1
    assert alerts[0].observed_value == 0.26


def test_incident_ledger_tracks_open_incidents_and_history() -> None:
    policy = MonitoringPolicy("policy-105")
    ledger = IncidentLedger()
    policy.add_rule(
        ThresholdRule(
            rule_id="mem-hot",
            metric_name=MetricName("memory"),
            threshold=0.85,
            severity=Severity("critical"),
        )
    )
    policy.activate_rule("mem-hot")
    policy.collect_events()

    policy.evaluate(
        [MetricSample(datetime(2026, 4, 1, 14, 0, 0), MetricName("memory"), 0.91)]
    )
    for event in policy.collect_events():
        if isinstance(event, AlertTriggered):
            ledger.apply(event)
    open_incidents = ledger.open_incidents()

    assert open_incidents["mem-hot"].metric_name == "memory"
    assert ledger.history()["memory"][0].observed_value == 0.91
