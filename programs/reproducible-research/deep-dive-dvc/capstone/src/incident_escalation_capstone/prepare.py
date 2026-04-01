from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from incident_escalation_capstone.common import (
    FEATURE_NAMES,
    as_float,
    as_int,
    load_params,
    read_csv_rows,
    stable_bucket,
    write_csv_rows,
    write_json,
)


def normalize_row(raw: dict[str, str]) -> dict[str, object]:
    row = {
        "incident_id": raw["incident_id"],
        "team": raw["team"],
        "backlog_days": as_int(raw["backlog_days"], "backlog_days"),
        "reopened_count": as_int(raw["reopened_count"], "reopened_count"),
        "integration_touchpoints": as_int(raw["integration_touchpoints"], "integration_touchpoints"),
        "customer_tier": as_int(raw["customer_tier"], "customer_tier"),
        "weekend_handoff": as_int(raw["weekend_handoff"], "weekend_handoff"),
        "severity_score": round(as_float(raw["severity_score"], "severity_score"), 4),
        "escalated": as_int(raw["escalated"], "escalated"),
    }

    if row["customer_tier"] not in {1, 2, 3}:
        raise ValueError(f"customer_tier must be one of 1, 2, 3, got {row['customer_tier']}")
    if row["weekend_handoff"] not in {0, 1}:
        raise ValueError(f"weekend_handoff must be 0 or 1, got {row['weekend_handoff']}")
    if row["escalated"] not in {0, 1}:
        raise ValueError(f"escalated must be 0 or 1, got {row['escalated']}")

    return row


def build_profile(rows: list[dict[str, object]], train_rows: list[dict[str, object]], eval_rows: list[dict[str, object]]) -> dict[str, object]:
    escalated_total = sum(int(row["escalated"]) for row in rows)
    team_counts = Counter(str(row["team"]) for row in rows)
    return {
        "raw_rows": len(rows),
        "train_rows": len(train_rows),
        "eval_rows": len(eval_rows),
        "escalated_rows": escalated_total,
        "escalation_rate": round(escalated_total / len(rows), 4),
        "feature_names": list(FEATURE_NAMES),
        "teams": dict(sorted(team_counts.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--eval", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()

    params = load_params(args.params)
    split = params["split"]
    seed = int(split["seed"])
    modulus = int(split["modulus"])
    eval_remainder = int(split["eval_remainder"])

    rows = [normalize_row(row) for row in read_csv_rows(args.raw)]
    train_rows: list[dict[str, object]] = []
    eval_rows: list[dict[str, object]] = []

    for row in rows:
        bucket = stable_bucket(str(row["incident_id"]), seed=seed, modulus=modulus)
        destination = eval_rows if bucket == eval_remainder else train_rows
        destination.append(row)

    if not train_rows or not eval_rows:
        raise ValueError("split configuration must produce both train and eval rows")

    fieldnames = [
        "incident_id",
        "team",
        *FEATURE_NAMES,
        "escalated",
    ]
    write_csv_rows(args.train, fieldnames, train_rows)
    write_csv_rows(args.eval, fieldnames, eval_rows)
    write_json(args.profile, build_profile(rows, train_rows, eval_rows))


if __name__ == "__main__":
    main()
