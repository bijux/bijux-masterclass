from __future__ import annotations

import argparse
import csv
from pathlib import Path

from incident_escalation_capstone.common import FEATURE_NAMES, load_params, read_csv_rows, read_json, write_csv_rows, write_json
from incident_escalation_capstone.fit import sigmoid


def predict_probability(row: dict[str, str], model: dict[str, object]) -> float:
    linear = float(model["bias"])
    for feature in FEATURE_NAMES:
        mean = float(model["means"][feature])
        scale = float(model["scales"][feature])
        normalized = (float(row[feature]) - mean) / scale
        linear += float(model["weights"][feature]) * normalized
    return sigmoid(linear)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--eval", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    args = parser.parse_args()

    params = load_params(args.params)
    threshold = float(params["decision"]["threshold"])
    model = read_json(args.model)
    rows = read_csv_rows(args.eval)

    predictions: list[dict[str, object]] = []
    tp = fp = tn = fn = 0
    brier_total = 0.0

    for row in rows:
        probability = predict_probability(row, model)
        actual = int(row["escalated"])
        predicted = 1 if probability >= threshold else 0
        if predicted == 1 and actual == 1:
            tp += 1
        elif predicted == 1 and actual == 0:
            fp += 1
        elif predicted == 0 and actual == 0:
            tn += 1
        else:
            fn += 1
        brier_total += (probability - actual) ** 2
        predictions.append(
            {
                "incident_id": row["incident_id"],
                "team": row["team"],
                "actual": actual,
                "predicted": predicted,
                "probability": round(probability, 6),
            }
        )

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    accuracy = (tp + tn) / len(rows)
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    write_csv_rows(
        args.predictions,
        ["incident_id", "team", "actual", "predicted", "probability"],
        predictions,
    )
    write_json(
        args.metrics,
        {
            "eval_rows": len(rows),
            "threshold": threshold,
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "brier_score": round(brier_total / len(rows), 6),
            "confusion_matrix": {
                "true_positive": tp,
                "false_positive": fp,
                "true_negative": tn,
                "false_negative": fn,
            },
        },
    )


if __name__ == "__main__":
    main()
