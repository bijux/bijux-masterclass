from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def divide(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 4) if denominator else 0.0


def evaluate(data_path: Path, params_path: Path) -> dict[str, object]:
    params = read_json(params_path)
    decision = params["decision"]
    evaluation = params["evaluation"]
    assert isinstance(decision, dict)
    assert isinstance(evaluation, dict)
    threshold = float(decision["threshold"])

    rows = list(csv.DictReader(data_path.read_text(encoding="utf-8").splitlines()))
    incident_ids = sorted(row["incident_id"] for row in rows)
    population_digest = hashlib.sha256(
        "\n".join(incident_ids).encode("utf-8")
    ).hexdigest()

    true_positive = false_positive = false_negative = 0
    for row in rows:
        predicted = float(row["score"]) >= threshold
        observed = row["escalated"] == "1"
        true_positive += int(predicted and observed)
        false_positive += int(predicted and not observed)
        false_negative += int(not predicted and observed)

    precision = divide(true_positive, true_positive + false_positive)
    recall = divide(true_positive, true_positive + false_negative)
    return {
        "controls": {"decision_threshold": threshold},
        "metric_schema": evaluation["metric_schema"],
        "metrics": {
            "f1": divide(
                int(2 * precision * recall * 10_000),
                int((precision + recall) * 10_000),
            ),
            "precision": precision,
            "recall": recall,
        },
        "population": {
            "id": evaluation["population_id"],
            "record_count": len(rows),
            "record_ids_sha256": population_digest,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = evaluate(args.data, args.params)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
