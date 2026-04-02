from __future__ import annotations

from datetime import datetime

import pytest

from service_monitoring import DomainError, MetricName, MetricSample, MonitoringApplication, RuleRegistration
from service_monitoring.scenario import (
    DEFAULT_POLICY_ID,
    DEFAULT_RULE_REGISTRATIONS,
    DEFAULT_SAMPLES,
    RETIREMENT_REASON,
    build_default_observation,
    build_retirement_review,
)


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
    assert observed.snapshot.rules[0].evaluation_mode == "threshold"
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


def test_default_scenario_contract_stays_stable() -> None:
    observation = build_default_observation()

    assert DEFAULT_POLICY_ID == "service-monitoring"
    assert tuple(rule.rule_id for rule in DEFAULT_RULE_REGISTRATIONS) == (
        "cpu-hot",
        "cpu-sustained",
    )
    assert len(DEFAULT_SAMPLES) == 3
    assert observation.cycle_report.alerts_published == 2
    assert observation.snapshot.summary.active_rule_ids == ("cpu-hot", "cpu-sustained")


def test_retirement_scenario_contract_stays_stable() -> None:
    review = build_retirement_review()

    assert "disk-hot" in review.active_snapshot.open_incidents
    assert review.retired_snapshot.summary.retired_rule_ids == ("disk-hot",)
    assert review.retired_snapshot.open_incidents == {}
    assert review.retired_snapshot.incident_history["disk"][0].rule_id == "disk-hot"
    assert review.retired_reason == RETIREMENT_REASON
