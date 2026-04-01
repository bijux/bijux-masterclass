from __future__ import annotations

from datetime import datetime
from pprint import pprint

from .application import MonitoringApplication, RuleRegistration
from .model import MetricName, MetricSample


def main() -> None:
    app = MonitoringApplication()
    app.create_policy("service-monitoring")
    app.register_rule(
        "service-monitoring",
        RuleRegistration(
            rule_id="cpu-hot",
            metric_name="cpu",
            threshold=0.9,
            severity="critical",
        ),
    )
    app.register_rule(
        "service-monitoring",
        RuleRegistration(
            rule_id="cpu-sustained",
            metric_name="cpu",
            threshold=0.8,
            severity="warning",
            window=3,
            evaluation_mode="consecutive",
        ),
    )
    app.activate_rule("service-monitoring", "cpu-hot")
    app.activate_rule("service-monitoring", "cpu-sustained")

    result = app.observe_samples(
        "service-monitoring",
        [
            MetricSample(datetime(2026, 4, 2, 9, 0, 0), MetricName("cpu"), 0.82),
            MetricSample(datetime(2026, 4, 2, 9, 1, 0), MetricName("cpu"), 0.93),
            MetricSample(datetime(2026, 4, 2, 9, 2, 0), MetricName("cpu"), 0.95),
        ],
    )

    print("Cycle report:")
    pprint(result.cycle_report)
    print("\nPolicy summary:")
    pprint(result.snapshot.summary)
    print("\nActive rule index:")
    pprint(result.snapshot.active_rule_index)
    print("\nOpen incidents:")
    pprint(result.snapshot.open_incidents)
