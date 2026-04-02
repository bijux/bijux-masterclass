from __future__ import annotations

from datetime import datetime

from .application import MonitoringApplication, ObservationResult, RuleRegistration
from .model import MetricName, MetricSample

DEFAULT_POLICY_ID = "service-monitoring"


def build_default_application() -> MonitoringApplication:
    app = MonitoringApplication()
    app.create_policy(DEFAULT_POLICY_ID)
    app.register_rule(
        DEFAULT_POLICY_ID,
        RuleRegistration(
            rule_id="cpu-hot",
            metric_name="cpu",
            threshold=0.9,
            severity="critical",
        ),
    )
    app.register_rule(
        DEFAULT_POLICY_ID,
        RuleRegistration(
            rule_id="cpu-sustained",
            metric_name="cpu",
            threshold=0.8,
            severity="warning",
            window=3,
            evaluation_mode="consecutive",
        ),
    )
    app.activate_rule(DEFAULT_POLICY_ID, "cpu-hot")
    app.activate_rule(DEFAULT_POLICY_ID, "cpu-sustained")
    return app


def build_default_observation() -> ObservationResult:
    app = build_default_application()
    return app.observe_samples(
        DEFAULT_POLICY_ID,
        [
            MetricSample(datetime(2026, 4, 2, 9, 0, 0), MetricName("cpu"), 0.82),
            MetricSample(datetime(2026, 4, 2, 9, 1, 0), MetricName("cpu"), 0.93),
            MetricSample(datetime(2026, 4, 2, 9, 2, 0), MetricName("cpu"), 0.95),
        ],
    )
