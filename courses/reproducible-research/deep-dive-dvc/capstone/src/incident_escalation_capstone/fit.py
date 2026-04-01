from __future__ import annotations

import argparse
import math
from pathlib import Path

from incident_escalation_capstone.common import FEATURE_NAMES, load_params, read_csv_rows, write_json


def sigmoid(value: float) -> float:
    if value >= 0:
        scale = math.exp(-value)
        return 1.0 / (1.0 + scale)
    scale = math.exp(value)
    return scale / (1.0 + scale)


def standardize_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, float], dict[str, float]]:
    means = {
        feature: sum(float(row[feature]) for row in rows) / len(rows)
        for feature in FEATURE_NAMES
    }
    scales = {}
    for feature in FEATURE_NAMES:
        variance = sum((float(row[feature]) - means[feature]) ** 2 for row in rows) / len(rows)
        scales[feature] = math.sqrt(variance) or 1.0

    transformed: list[dict[str, object]] = []
    for row in rows:
        transformed.append(
            {
                "incident_id": row["incident_id"],
                "team": row["team"],
                "escalated": int(row["escalated"]),
                "features": {
                    feature: (float(row[feature]) - means[feature]) / scales[feature]
                    for feature in FEATURE_NAMES
                },
            }
        )
    return transformed, means, scales


def fit_model(
    rows: list[dict[str, object]],
    learning_rate: float,
    iterations: int,
    l2: float,
) -> tuple[float, dict[str, float], float]:
    positive_rate = sum(int(row["escalated"]) for row in rows) / len(rows)
    positive_rate = min(max(positive_rate, 1e-6), 1 - 1e-6)
    bias = math.log(positive_rate / (1 - positive_rate))
    weights = {feature: 0.0 for feature in FEATURE_NAMES}
    loss = 0.0

    for _ in range(iterations):
        gradients = {feature: 0.0 for feature in FEATURE_NAMES}
        bias_gradient = 0.0
        loss = 0.0

        for row in rows:
            linear = bias + sum(weights[feature] * float(row["features"][feature]) for feature in FEATURE_NAMES)
            probability = sigmoid(linear)
            label = float(row["escalated"])
            error = probability - label
            bias_gradient += error
            for feature in FEATURE_NAMES:
                gradients[feature] += error * float(row["features"][feature])
            clipped = min(max(probability, 1e-9), 1 - 1e-9)
            loss += -(label * math.log(clipped) + (1.0 - label) * math.log(1.0 - clipped))

        batch_size = len(rows)
        bias -= learning_rate * (bias_gradient / batch_size)
        for feature in FEATURE_NAMES:
            penalty = l2 * weights[feature]
            weights[feature] -= learning_rate * ((gradients[feature] / batch_size) + penalty)

        regularized_norm = sum(weight * weight for weight in weights.values())
        loss = (loss / batch_size) + (0.5 * l2 * regularized_norm)

    return bias, weights, loss


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--train", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()

    params = load_params(args.params)
    training = params["training"]
    learning_rate = float(training["learning_rate"])
    iterations = int(training["iterations"])
    l2 = float(training["l2"])

    rows = read_csv_rows(args.train)
    prepared_rows, means, scales = standardize_rows(rows)
    bias, weights, loss = fit_model(prepared_rows, learning_rate=learning_rate, iterations=iterations, l2=l2)

    payload = {
        "feature_names": list(FEATURE_NAMES),
        "means": means,
        "scales": scales,
        "weights": weights,
        "bias": bias,
        "training": {
            "learning_rate": learning_rate,
            "iterations": iterations,
            "l2": l2,
            "rows": len(rows),
            "final_loss": round(loss, 6),
        },
    }
    write_json(args.model, payload)


if __name__ == "__main__":
    main()
