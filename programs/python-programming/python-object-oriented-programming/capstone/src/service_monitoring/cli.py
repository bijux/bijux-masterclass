from __future__ import annotations

import argparse
from collections.abc import Sequence

from .scenario import (
    DEFAULT_RULE_REGISTRATIONS,
    DEFAULT_SAMPLES,
    build_default_observation,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="service-monitoring",
        description="Inspect the learner-facing monitoring capstone scenario.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("summary", help="Show the scenario summary and open incidents.")
    subparsers.add_parser("rules", help="Show the rule lifecycle summary.")
    subparsers.add_parser("history", help="Show incident history grouped by metric.")
    subparsers.add_parser("timeline", help="Show the scenario as an ordered event timeline.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    observation = build_default_observation()

    if args.command == "summary":
        print(f"policy_id: {observation.snapshot.summary.policy_id}")
        print(f"alerts_published: {observation.cycle_report.alerts_published}")
        print(f"active_rules: {', '.join(observation.snapshot.summary.active_rule_ids)}")
        print(f"open_incidents: {', '.join(sorted(observation.snapshot.open_incidents))}")
        return 0

    if args.command == "rules":
        summary = observation.snapshot.summary
        print(f"draft_rules: {', '.join(summary.draft_rule_ids) or '(none)'}")
        print(f"active_rules: {', '.join(summary.active_rule_ids) or '(none)'}")
        print(f"retired_rules: {', '.join(summary.retired_rule_ids) or '(none)'}")
        print("rule_details:")
        for rule in observation.snapshot.rules:
            print(
                "  "
                f"{rule.rule_id} state={rule.state} metric={rule.metric_name} "
                f"mode={rule.evaluation_mode} threshold={rule.threshold} "
                f"window={rule.window} severity={rule.severity}"
            )
        return 0

    if args.command == "timeline":
        print("step: register rules")
        for registration in DEFAULT_RULE_REGISTRATIONS:
            print(
                "  "
                f"{registration.rule_id} mode={registration.evaluation_mode} "
                f"threshold={registration.threshold} window={registration.window}"
            )
        print("step: activate rules")
        print("  cpu-hot")
        print("  cpu-sustained")
        print("step: observe samples")
        for sample in DEFAULT_SAMPLES:
            print(
                "  "
                f"{sample.observed_at.isoformat(timespec='seconds')} "
                f"{sample.metric_name}={sample.value}"
            )
        print("step: published alerts")
        for metric_name, incidents in observation.snapshot.incident_history.items():
            for incident in incidents:
                print(
                    "  "
                    f"{metric_name} {incident.rule_id} -> {incident.severity} "
                    f"observed={incident.observed_value} threshold={incident.threshold}"
                )
        return 0

    for metric_name, incidents in observation.snapshot.incident_history.items():
        print(f"metric: {metric_name}")
        for incident in incidents:
            print(
                "  "
                f"{incident.rule_id} -> {incident.severity} "
                f"observed={incident.observed_value} threshold={incident.threshold}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
