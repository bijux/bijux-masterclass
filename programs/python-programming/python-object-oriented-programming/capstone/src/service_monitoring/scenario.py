from __future__ import annotations

from datetime import datetime

from dataclasses import dataclass

from .application import MonitoringApplication, MonitoringSnapshot, ObservationResult, RuleRegistration
from .model import MetricName, MetricSample

DEFAULT_POLICY_ID = "service-monitoring"
DEFAULT_RULE_REGISTRATIONS: tuple[RuleRegistration, ...] = (
    RuleRegistration(
        rule_id="cpu-hot",
        metric_name="cpu",
        threshold=0.9,
        severity="critical",
    ),
    RuleRegistration(
        rule_id="cpu-sustained",
        metric_name="cpu",
        threshold=0.8,
        severity="warning",
        window=3,
        evaluation_mode="consecutive",
    ),
)
DEFAULT_SAMPLES: tuple[MetricSample, ...] = (
    MetricSample(datetime(2026, 4, 2, 9, 0, 0), MetricName("cpu"), 0.82),
    MetricSample(datetime(2026, 4, 2, 9, 1, 0), MetricName("cpu"), 0.93),
    MetricSample(datetime(2026, 4, 2, 9, 2, 0), MetricName("cpu"), 0.95),
)
RETIREMENT_POLICY_ID = "service-monitoring-retirement"
RETIREMENT_RULE = RuleRegistration(
    rule_id="disk-hot",
    metric_name="disk",
    threshold=0.85,
    severity="warning",
)
RETIREMENT_SAMPLES: tuple[MetricSample, ...] = (
    MetricSample(datetime(2026, 4, 2, 10, 0, 0), MetricName("disk"), 0.91),
)
RETIREMENT_REASON = "replaced by storage saturation policy"


@dataclass(frozen=True, slots=True)
class RetirementReview:
    active_snapshot: MonitoringSnapshot
    retired_snapshot: MonitoringSnapshot
    retired_reason: str


def build_default_application() -> MonitoringApplication:
    app = MonitoringApplication()
    app.create_policy(DEFAULT_POLICY_ID)
    for registration in DEFAULT_RULE_REGISTRATIONS:
        app.register_rule(DEFAULT_POLICY_ID, registration)
    app.activate_rule(DEFAULT_POLICY_ID, "cpu-hot")
    app.activate_rule(DEFAULT_POLICY_ID, "cpu-sustained")
    return app


def build_default_observation() -> ObservationResult:
    app = build_default_application()
    return app.observe_samples(DEFAULT_POLICY_ID, list(DEFAULT_SAMPLES))


def build_retirement_review() -> RetirementReview:
    app = MonitoringApplication()
    app.create_policy(RETIREMENT_POLICY_ID)
    app.register_rule(RETIREMENT_POLICY_ID, RETIREMENT_RULE)
    app.activate_rule(RETIREMENT_POLICY_ID, RETIREMENT_RULE.rule_id)
    app.observe_samples(RETIREMENT_POLICY_ID, list(RETIREMENT_SAMPLES))
    active_snapshot = app.snapshot(RETIREMENT_POLICY_ID)
    app.retire_rule(RETIREMENT_POLICY_ID, RETIREMENT_RULE.rule_id, RETIREMENT_REASON)
    retired_snapshot = app.snapshot(RETIREMENT_POLICY_ID)
    return RetirementReview(
        active_snapshot=active_snapshot,
        retired_snapshot=retired_snapshot,
        retired_reason=RETIREMENT_REASON,
    )
