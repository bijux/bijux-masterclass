from __future__ import annotations

from datetime import datetime

import pytest

from service_monitoring import DomainError, MetricName, MetricSample, MonitoringApplication, RuleRegistration


def test_application_supports_a_full_monitoring_workflow() -> None:
    app = MonitoringApplication()

    created = app.create_policy("policy-app")
    assert created.draft_rule_ids == ()

    registered = app.register_rule(
        "policy-app",
        RuleRegistration(
            rule_id="cpu-hot",
            metric_name="cpu",
            threshold=0.9,
            severity="critical",
        ),
    )
    assert registered.draft_rule_ids == ("cpu-hot",)

    activated = app.activate_rule("policy-app", "cpu-hot")
    assert activated.active_rule_ids == ("cpu-hot",)

    observed = app.observe_samples(
        "policy-app",
        [MetricSample(datetime(2026, 4, 2, 10, 0, 0), MetricName("cpu"), 0.94)],
    )

    assert observed.cycle_report.alerts_published == 1
    assert observed.snapshot.summary.active_rule_ids == ("cpu-hot",)
    assert "cpu-hot" in observed.snapshot.open_incidents


def test_application_tracks_retired_rules_in_policy_summary() -> None:
    app = MonitoringApplication()
    app.create_policy("policy-retire")
    app.register_rule(
        "policy-retire",
        RuleRegistration(
            rule_id="latency-hot",
            metric_name="latency",
            threshold=0.7,
            severity="warning",
        ),
    )
    app.activate_rule("policy-retire", "latency-hot")

    retired = app.retire_rule("policy-retire", "latency-hot", "replaced by queue depth rule")

    assert retired.active_rule_ids == ()
    assert retired.retired_rule_ids == ("latency-hot",)


def test_application_blocks_duplicate_policy_creation() -> None:
    app = MonitoringApplication()
    app.create_policy("policy-dup")

    with pytest.raises(DomainError):
        app.create_policy("policy-dup")
