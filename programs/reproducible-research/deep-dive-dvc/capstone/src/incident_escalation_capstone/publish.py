from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from incident_escalation_capstone.common import load_params, read_csv_rows, read_json, sha256_file, write_json


def write_report(
    report_path: Path,
    *,
    profile: dict[str, object],
    metrics: dict[str, object],
    model: dict[str, object],
    predictions: list[dict[str, str]],
) -> None:
    false_positives = [row for row in predictions if row["actual"] == "0" and row["predicted"] == "1"][:3]
    false_negatives = [row for row in predictions if row["actual"] == "1" and row["predicted"] == "0"][:3]

    lines = [
        "# Incident Escalation Reference Report",
        "",
        "This publish set is the stable interface for the capstone pipeline.",
        "",
        "## Data Profile",
        "",
        f"- Raw rows: {profile['raw_rows']}",
        f"- Train rows: {profile['train_rows']}",
        f"- Eval rows: {profile['eval_rows']}",
        f"- Escalation rate: {profile['escalation_rate']}",
        "",
        "## Evaluation Metrics",
        "",
        f"- Accuracy: {metrics['accuracy']}",
        f"- Precision: {metrics['precision']}",
        f"- Recall: {metrics['recall']}",
        f"- F1: {metrics['f1']}",
        f"- Brier score: {metrics['brier_score']}",
        "",
        "## Decision Policy",
        "",
        f"- Threshold: {metrics['threshold']}",
        "",
        "## Training Summary",
        "",
        f"- Learned bias: {round(float(model['bias']), 4)}",
        f"- Training rows: {model['training']['rows']}",
        f"- Iterations: {model['training']['iterations']}",
        f"- Final training loss: {model['training']['final_loss']}",
        "",
        "## Release Boundary",
        "",
        "- `metrics.json` is the promoted quantitative summary.",
        "- `params.yaml` is the promoted control surface.",
        "- `predictions.csv` is the record-level review surface.",
        "- `manifest.json` is the integrity and inventory checkpoint.",
        "",
        "## Review Queue",
        "",
        "False positives worth review:",
    ]

    if false_positives:
        for row in false_positives:
            lines.append(
                f"- {row['incident_id']} ({row['team']}): predicted={row['probability']}, actual=0"
            )
    else:
        lines.append("- none")

    lines.extend(["", "False negatives worth review:"])
    if false_negatives:
        for row in false_negatives:
            lines.append(
                f"- {row['incident_id']} ({row['team']}): predicted={row['probability']}, actual=1"
            )
    else:
        lines.append("- none")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", type=Path, required=True)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--publish", type=Path, required=True)
    args = parser.parse_args()

    publish_dir = args.publish
    publish_dir.mkdir(parents=True, exist_ok=True)

    params_path = publish_dir / "params.yaml"
    profile_path = publish_dir / "data-profile.json"
    model_path = publish_dir / "model.json"
    metrics_path = publish_dir / "metrics.json"
    predictions_path = publish_dir / "predictions.csv"
    report_path = publish_dir / "report.md"

    shutil.copy2(args.params, params_path)
    shutil.copy2(args.profile, profile_path)
    shutil.copy2(args.model, model_path)
    shutil.copy2(args.metrics, metrics_path)
    shutil.copy2(args.predictions, predictions_path)

    profile = read_json(args.profile)
    metrics = read_json(args.metrics)
    model = read_json(args.model)
    predictions = read_csv_rows(args.predictions)
    write_report(report_path, profile=profile, metrics=metrics, model=model, predictions=predictions)

    entries = []
    for path in sorted(publish_dir.iterdir()):
        if path.name == "manifest.json":
            continue
        entries.append(
            {
                "path": path.name,
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )

    write_json(
        publish_dir / "manifest.json",
        {
            "artifacts": entries,
            "training": model["training"],
            "decision": load_params(args.params)["decision"],
        },
    )


if __name__ == "__main__":
    main()
