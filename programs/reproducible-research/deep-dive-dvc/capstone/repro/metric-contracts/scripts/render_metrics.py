from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    case = read_json(args.case)
    params = read_json(args.params)
    matrix = case["confusion_matrix"]
    metric_contract = case["metric"]
    assert isinstance(matrix, dict)
    assert isinstance(metric_contract, dict)

    true_positive = int(matrix["true_positive"])
    false_positive = int(matrix["false_positive"])
    false_negative = int(matrix["false_negative"])
    true_negative = int(matrix["true_negative"])
    precision = ratio(true_positive, true_positive + false_positive)
    recall = ratio(true_positive, true_positive + false_negative)
    f1 = ratio(2 * precision * recall, precision + recall)
    scale = 100.0 if metric_contract["unit"] == "percent" else 1.0

    population = case["population"]
    assert isinstance(population, dict)
    contract_population: dict[str, object] = {"rows": int(population["rows"])}
    if "identity" in population:
        contract_population["identity"] = population["identity"]

    decision = params["decision"]
    assert isinstance(decision, dict)
    output = {
        "comparison_contract": {
            "schema_version": int(case["schema_version"]),
            "population": contract_population,
            "controls": {
                "decision_threshold": float(decision["threshold"]),
            },
            "primary_metric": metric_contract,
        },
        "metrics": {
            str(metric_contract["name"]): {
                "direction": "higher_is_better",
                "value": round(f1 * scale, 4),
            },
            "precision_at_fixed_threshold": round(precision * scale, 4),
            "recall_at_fixed_threshold": round(recall * scale, 4),
        },
        "confusion_matrix": {
            "false_negative": false_negative,
            "false_positive": false_positive,
            "true_negative": true_negative,
            "true_positive": true_positive,
        },
    }

    additional_metrics = case.get("additional_metrics", [])
    assert isinstance(additional_metrics, list)
    if "false_positive_rate_at_fixed_threshold" in additional_metrics:
        output["metrics"]["false_positive_rate_at_fixed_threshold"] = round(
            ratio(false_positive, false_positive + true_negative) * scale,
            4,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
