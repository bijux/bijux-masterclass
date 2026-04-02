from __future__ import annotations

from collections.abc import Iterable

from .application import MonitoringApplication
from .model import MetricSample
from .scenario import DEFAULT_POLICY_ID, DEFAULT_RULE_REGISTRATIONS, DEFAULT_SAMPLES


def _render_samples(samples: Iterable[MetricSample]) -> str:
    return "\n".join(
        f"  - {sample.observed_at.isoformat(timespec='seconds')} {sample.metric_name}={sample.value}"
        for sample in samples
    )


def main() -> None:
    app = MonitoringApplication()

    print("Monitoring walkthrough")
    print(f"policy_id: {DEFAULT_POLICY_ID}")

    summary = app.create_policy(DEFAULT_POLICY_ID)
    print("\nStage 1: create policy")
    print(f"  draft_rules={len(summary.draft_rule_ids)} active_rules={len(summary.active_rule_ids)}")

    print("\nStage 2: register rules")
    for registration in DEFAULT_RULE_REGISTRATIONS:
        summary = app.register_rule(DEFAULT_POLICY_ID, registration)
        print(
            "  "
            f"registered {registration.rule_id} "
            f"mode={registration.evaluation_mode} threshold={registration.threshold} "
            f"window={registration.window} severity={registration.severity}"
        )
    print(f"  draft_rules={', '.join(summary.draft_rule_ids)}")

    print("\nStage 3: activate rules")
    for rule_id in ("cpu-hot", "cpu-sustained"):
        summary = app.activate_rule(DEFAULT_POLICY_ID, rule_id)
        print(f"  activated {rule_id}")
    print(f"  active_rules={', '.join(summary.active_rule_ids)}")

    print("\nStage 4: observe samples")
    print(_render_samples(DEFAULT_SAMPLES))
    result = app.observe_samples(DEFAULT_POLICY_ID, list(DEFAULT_SAMPLES))
    print(f"  alerts_published={result.cycle_report.alerts_published}")

    print("\nStage 5: inspect derived state")
    print(f"  active_rule_index={result.snapshot.active_rule_index}")
    print(f"  open_incidents={sorted(result.snapshot.open_incidents)}")
    print(
        "  incident_history="
        f"{ {metric: len(items) for metric, items in result.snapshot.incident_history.items()} }"
    )


if __name__ == "__main__":
    main()
