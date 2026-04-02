from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from incident_escalation_capstone.common import FEATURE_NAMES, load_params, read_json, sha256_file


def verify_manifest(publish_dir: Path) -> dict[str, object]:
    manifest = read_json(publish_dir / "manifest.json")
    artifacts = manifest["artifacts"]
    if not artifacts:
        raise ValueError("publish manifest must list at least one artifact")

    for entry in artifacts:
        target = publish_dir / entry["path"]
        if not target.exists():
            raise FileNotFoundError(f"manifest target missing: {entry['path']}")
        digest = sha256_file(target)
        if digest != entry["sha256"]:
            raise ValueError(f"sha256 mismatch for {entry['path']}: {digest} != {entry['sha256']}")
        if int(entry["bytes"]) != target.stat().st_size:
            raise ValueError(f"byte-size mismatch for {entry['path']}")

    expected = {
        "data-profile.json",
        "metrics.json",
        "model.json",
        "params.yaml",
        "predictions.csv",
        "report.md",
    }
    paths = {entry["path"] for entry in artifacts}
    if paths != expected:
        raise ValueError(f"publish manifest must list exactly {sorted(expected)}, got {sorted(paths)}")
    return {
        "check": "manifest",
        "artifact_paths": sorted(paths),
        "artifact_count": len(artifacts),
    }


def verify_metrics(publish_dir: Path) -> dict[str, object]:
    metrics = read_json(publish_dir / "metrics.json")
    for field in ("accuracy", "precision", "recall", "f1"):
        value = float(metrics[field])
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{field} must be between 0 and 1, got {value}")
    if int(metrics["eval_rows"]) < 3:
        raise ValueError("eval_rows must be at least 3 for this capstone")
    if not 0.0 <= float(metrics["brier_score"]) <= 1.0:
        raise ValueError("brier_score must be between 0 and 1")

    matrix = metrics["confusion_matrix"]
    total = sum(int(matrix[name]) for name in ("true_positive", "false_positive", "true_negative", "false_negative"))
    if total != int(metrics["eval_rows"]):
        raise ValueError("confusion matrix totals must equal eval_rows")
    return {
        "check": "metrics",
        "eval_rows": int(metrics["eval_rows"]),
        "accuracy": float(metrics["accuracy"]),
        "f1": float(metrics["f1"]),
        "brier_score": float(metrics["brier_score"]),
    }


def verify_params(publish_dir: Path) -> dict[str, object]:
    params = load_params(publish_dir / "params.yaml")
    for section in ("split", "training", "decision"):
        if section not in params:
            raise ValueError(f"params.yaml missing section: {section}")
    threshold = float(params["decision"]["threshold"])
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("decision.threshold must be between 0 and 1")
    return {
        "check": "params",
        "sections": ["split", "training", "decision"],
        "decision_threshold": threshold,
    }


def verify_model(publish_dir: Path) -> dict[str, object]:
    model = read_json(publish_dir / "model.json")
    feature_names = set(model["feature_names"])
    if feature_names != set(FEATURE_NAMES):
        raise ValueError("model feature_names must match the capstone feature contract")

    for section in ("weights", "means", "scales"):
        keys = set(model[section])
        if keys != set(FEATURE_NAMES):
            raise ValueError(f"model {section} keys must match the capstone feature contract")

    training = model["training"]
    for field in ("final_loss", "iterations", "l2", "learning_rate", "rows"):
        if field not in training:
            raise ValueError(f"model training metadata missing field: {field}")
    return {
        "check": "model",
        "feature_count": len(feature_names),
        "training_rows": int(training["rows"]),
        "iterations": int(training["iterations"]),
    }


def verify_predictions(publish_dir: Path) -> dict[str, object]:
    metrics = read_json(publish_dir / "metrics.json")
    with (publish_dir / "predictions.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    expected_headers = ["incident_id", "team", "actual", "predicted", "probability"]
    if not rows:
        raise ValueError("predictions.csv must contain at least one row")
    if list(rows[0].keys()) != expected_headers:
        raise ValueError("predictions.csv must preserve the published prediction columns")
    if len(rows) != int(metrics["eval_rows"]):
        raise ValueError("predictions.csv row count must equal metrics eval_rows")

    for row in rows:
        actual = int(row["actual"])
        predicted = int(row["predicted"])
        probability = float(row["probability"])
        if actual not in (0, 1) or predicted not in (0, 1):
            raise ValueError("predictions.csv actual and predicted values must be binary")
        if not 0.0 <= probability <= 1.0:
            raise ValueError("predictions.csv probabilities must be between 0 and 1")
    return {
        "check": "predictions",
        "rows": len(rows),
        "headers": expected_headers,
    }


def verify_report(publish_dir: Path) -> dict[str, object]:
    report = (publish_dir / "report.md").read_text(encoding="utf-8")
    headings = [
        "# Incident Escalation Reference Report",
        "## Data Profile",
        "## Evaluation Metrics",
        "## Model Summary",
        "## Review Queue",
    ]
    for heading in headings:
        if heading not in report:
            raise ValueError(f"report.md missing heading: {heading}")
    return {
        "check": "report",
        "headings": headings,
    }


def verify_publish(publish_dir: Path) -> list[dict[str, object]]:
    return [
        verify_manifest(publish_dir),
        verify_metrics(publish_dir),
        verify_params(publish_dir),
        verify_model(publish_dir),
        verify_predictions(publish_dir),
        verify_report(publish_dir),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    checks = verify_publish(args.publish)
    if args.report is not None:
        args.report.write_text(
            json.dumps(
                {
                    "publish_dir": args.publish.resolve().as_posix(),
                    "checks": checks,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
