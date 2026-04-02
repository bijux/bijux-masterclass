from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from incident_escalation_capstone.common import load_params, read_json


def release_summary(publish_dir: Path) -> dict[str, object]:
    manifest = read_json(publish_dir / "manifest.json")
    metrics = read_json(publish_dir / "metrics.json")
    params = load_params(publish_dir / "params.yaml")
    return {
        "publish_dir": publish_dir.as_posix(),
        "artifact_count": len(manifest["artifacts"]),
        "artifacts": [entry["path"] for entry in manifest["artifacts"]],
        "decision_threshold": float(params["decision"]["threshold"]),
        "accuracy": float(metrics["accuracy"]),
        "f1": float(metrics["f1"]),
        "brier_score": float(metrics["brier_score"]),
    }


def stage_summary(*, pipeline_path: Path, lock_path: Path) -> dict[str, object]:
    pipeline_data = load_params(pipeline_path)
    lock_data = load_params(lock_path)
    pipeline_stages = pipeline_data["stages"]
    locked_stages = lock_data["stages"]
    stages = []

    for stage_name, stage_def in pipeline_stages.items():
        locked = locked_stages.get(stage_name, {})
        stages.append(
            {
                "stage_name": stage_name,
                "declared_deps": list(stage_def.get("deps", [])),
                "declared_outs": list(stage_def.get("outs", [])),
                "declared_params": list(stage_def.get("params", [])),
                "declared_metrics": list(stage_def.get("metrics", [])),
                "recorded_deps": [entry["path"] for entry in locked.get("deps", [])],
                "recorded_outs": [entry["path"] for entry in locked.get("outs", [])],
            }
        )

    return {
        "pipeline_path": pipeline_path.as_posix(),
        "lock_path": lock_path.as_posix(),
        "stage_count": len(stages),
        "stages": stages,
    }


def state_summary(*, publish_dir: Path, metrics_path: Path, params_path: Path, lock_path: Path) -> dict[str, object]:
    manifest = read_json(publish_dir / "manifest.json")
    metrics = read_json(metrics_path)
    params = load_params(params_path)
    lock_data = load_params(lock_path)
    return {
        "publish_dir": publish_dir.as_posix(),
        "stage_names": list(lock_data["stages"].keys()),
        "artifact_count": len(manifest["artifacts"]),
        "training_rows": int(manifest["training"]["rows"]),
        "eval_rows": int(metrics["eval_rows"]),
        "decision_threshold": float(params["decision"]["threshold"]),
    }


def review_queue(publish_dir: Path, *, limit: int = 3) -> dict[str, object]:
    with (publish_dir / "predictions.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    false_positives = [
        {
            "incident_id": row["incident_id"],
            "team": row["team"],
            "probability": float(row["probability"]),
        }
        for row in rows
        if row["actual"] == "0" and row["predicted"] == "1"
    ][:limit]
    false_negatives = [
        {
            "incident_id": row["incident_id"],
            "team": row["team"],
            "probability": float(row["probability"]),
        }
        for row in rows
        if row["actual"] == "1" and row["predicted"] == "0"
    ][:limit]

    return {
        "publish_dir": publish_dir.as_posix(),
        "false_positive_count": len(false_positives),
        "false_negative_count": len(false_negatives),
        "false_positives": false_positives,
        "false_negatives": false_negatives,
    }


def threshold_review(publish_dir: Path, *, margin: float = 0.08, limit: int = 5) -> dict[str, object]:
    metrics = read_json(publish_dir / "metrics.json")
    threshold = float(metrics["threshold"])
    with (publish_dir / "predictions.csv").open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    near_threshold = []
    for row in rows:
        probability = float(row["probability"])
        distance = abs(probability - threshold)
        if distance <= margin:
            near_threshold.append(
                {
                    "incident_id": row["incident_id"],
                    "team": row["team"],
                    "actual": int(row["actual"]),
                    "predicted": int(row["predicted"]),
                    "probability": probability,
                    "distance_from_threshold": round(distance, 6),
                }
            )

    near_threshold.sort(key=lambda row: row["distance_from_threshold"])
    return {
        "publish_dir": publish_dir.as_posix(),
        "threshold": threshold,
        "margin": margin,
        "near_threshold_count": len(near_threshold),
        "near_threshold": near_threshold[:limit],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="incident-escalation-inspect",
        description="Render public summaries for the Deep Dive DVC capstone.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    release = subparsers.add_parser("release-summary", help="Render a summary of the promoted release bundle.")
    release.add_argument("--publish", type=Path, required=True)
    release.set_defaults(handler=_handle_release_summary)

    stage = subparsers.add_parser("stage-summary", help="Render a summary of declared and recorded stage contracts.")
    stage.add_argument("--pipeline", type=Path, required=True)
    stage.add_argument("--lock", type=Path, required=True)
    stage.set_defaults(handler=_handle_stage_summary)

    state = subparsers.add_parser("state-summary", help="Render a summary of declaration, execution, and publish state.")
    state.add_argument("--publish", type=Path, required=True)
    state.add_argument("--metrics", type=Path, required=True)
    state.add_argument("--params", type=Path, required=True)
    state.add_argument("--lock", type=Path, required=True)
    state.set_defaults(handler=_handle_state_summary)

    queue = subparsers.add_parser("review-queue", help="Render the structured review queue from published predictions.")
    queue.add_argument("--publish", type=Path, required=True)
    queue.add_argument("--limit", type=int, default=3)
    queue.set_defaults(handler=_handle_review_queue)

    threshold = subparsers.add_parser("threshold-review", help="Render borderline predictions near the decision threshold.")
    threshold.add_argument("--publish", type=Path, required=True)
    threshold.add_argument("--margin", type=float, default=0.08)
    threshold.add_argument("--limit", type=int, default=5)
    threshold.set_defaults(handler=_handle_threshold_review)

    args = parser.parse_args(argv)
    print(json.dumps(args.handler(args), indent=2, sort_keys=True))
    return 0


def _handle_release_summary(args: argparse.Namespace) -> dict[str, object]:
    return release_summary(args.publish)


def _handle_stage_summary(args: argparse.Namespace) -> dict[str, object]:
    return stage_summary(pipeline_path=args.pipeline, lock_path=args.lock)


def _handle_state_summary(args: argparse.Namespace) -> dict[str, object]:
    return state_summary(
        publish_dir=args.publish,
        metrics_path=args.metrics,
        params_path=args.params,
        lock_path=args.lock,
    )


def _handle_review_queue(args: argparse.Namespace) -> dict[str, object]:
    return review_queue(args.publish, limit=args.limit)


def _handle_threshold_review(args: argparse.Namespace) -> dict[str, object]:
    return threshold_review(args.publish, margin=args.margin, limit=args.limit)


if __name__ == "__main__":
    raise SystemExit(main())
