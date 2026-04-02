from __future__ import annotations

import json
from pathlib import Path

from incident_escalation_capstone.common import write_json
from incident_escalation_capstone.inspect import (
    main,
    model_summary,
    profile_summary,
    release_summary,
    review_queue,
    stage_summary,
    state_summary,
    threshold_review,
)


def _write_publish_fixture(base: Path) -> None:
    publish_dir = base / "publish"
    publish_dir.mkdir(parents=True)
    write_json(
        publish_dir / "data-profile.json",
        {
            "raw_rows": 24,
            "train_rows": 18,
            "eval_rows": 6,
            "escalated_rows": 12,
            "escalation_rate": 0.5,
            "feature_names": [
                "backlog_days",
                "reopened_count",
                "integration_touchpoints",
                "customer_tier",
                "weekend_handoff",
                "severity_score",
            ],
            "teams": {
                "billing": 5,
                "checkout": 5,
            },
        },
    )
    write_json(
        publish_dir / "model.json",
        {
            "feature_names": [
                "backlog_days",
                "reopened_count",
                "integration_touchpoints",
                "customer_tier",
                "weekend_handoff",
                "severity_score",
            ],
            "weights": {
                "backlog_days": 1.0,
                "reopened_count": 0.4,
                "integration_touchpoints": 0.8,
                "customer_tier": 0.3,
                "weekend_handoff": 0.9,
                "severity_score": 1.2,
            },
            "means": {},
            "scales": {},
            "bias": 0.1,
            "training": {
                "rows": 18,
                "iterations": 900,
                "learning_rate": 0.25,
                "l2": 0.02,
                "final_loss": 0.133515,
            },
        },
    )
    write_json(
        publish_dir / "manifest.json",
        {
            "artifacts": [
                {"path": "data-profile.json", "sha256": "w", "bytes": 4},
                {"path": "metrics.json", "sha256": "x", "bytes": 1},
                {"path": "model.json", "sha256": "m", "bytes": 5},
                {"path": "params.yaml", "sha256": "y", "bytes": 2},
                {"path": "predictions.csv", "sha256": "z", "bytes": 3},
            ],
            "training": {"rows": 18},
        },
    )
    write_json(
        publish_dir / "metrics.json",
        {"accuracy": 0.9, "f1": 0.88, "brier_score": 0.11, "threshold": 0.52},
    )
    (publish_dir / "params.yaml").write_text(
        "split:\n  seed: 17\ntraining:\n  iterations: 100\ndecision:\n  threshold: 0.52\n",
        encoding="utf-8",
    )
    (publish_dir / "predictions.csv").write_text(
        "\n".join(
            [
                "incident_id,team,actual,predicted,probability",
                "INC-1,core,0,1,0.91",
                "INC-2,billing,1,0,0.41",
                "INC-3,core,1,1,0.87",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_release_summary_returns_public_release_facts(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    summary = release_summary(tmp_path / "publish")

    assert summary["artifact_count"] == 5
    assert summary["decision_threshold"] == 0.52
    assert summary["brier_score"] == 0.11


def test_profile_summary_returns_promoted_population_facts(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    summary = profile_summary(tmp_path / "publish")

    assert summary["raw_rows"] == 24
    assert summary["feature_count"] == 6
    assert summary["largest_team"]["team"] == "billing"


def test_model_summary_returns_promoted_training_facts(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    summary = model_summary(tmp_path / "publish")

    assert summary["feature_count"] == 6
    assert summary["training_rows"] == 18
    assert summary["strongest_feature"]["name"] == "severity_score"


def test_state_summary_combines_declaration_execution_and_publish_state(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)
    write_json(tmp_path / "metrics.json", {"eval_rows": 6})
    (tmp_path / "params.yaml").write_text(
        "split:\n  seed: 17\ntraining:\n  iterations: 100\ndecision:\n  threshold: 0.52\n",
        encoding="utf-8",
    )
    (tmp_path / "dvc.lock").write_text(
        "stages:\n  prepare: {}\n  fit: {}\n  evaluate: {}\n  publish: {}\n",
        encoding="utf-8",
    )

    summary = state_summary(
        publish_dir=tmp_path / "publish",
        metrics_path=tmp_path / "metrics.json",
        params_path=tmp_path / "params.yaml",
        lock_path=tmp_path / "dvc.lock",
    )

    assert summary["stage_names"] == ["prepare", "fit", "evaluate", "publish"]
    assert summary["training_rows"] == 18
    assert summary["eval_rows"] == 6


def test_stage_summary_reports_declared_and_recorded_stage_edges(tmp_path: Path) -> None:
    (tmp_path / "dvc.yaml").write_text(
        "\n".join(
            [
                "stages:",
                "  prepare:",
                "    deps:",
                "      - data/raw/service_incidents.csv",
                "    params:",
                "      - split.seed",
                "    outs:",
                "      - data/derived/train.csv",
                "  publish:",
                "    deps:",
                "      - metrics/metrics.json",
                "    outs:",
                "      - publish/v1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (tmp_path / "dvc.lock").write_text(
        "\n".join(
            [
                "stages:",
                "  prepare:",
                "    deps:",
                "      - path: data/raw/service_incidents.csv",
                "    outs:",
                "      - path: data/derived/train.csv",
                "  publish:",
                "    deps:",
                "      - path: metrics/metrics.json",
                "    outs:",
                "      - path: publish/v1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    summary = stage_summary(pipeline_path=tmp_path / "dvc.yaml", lock_path=tmp_path / "dvc.lock")

    assert summary["stage_count"] == 2
    assert summary["stages"][0]["stage_name"] == "prepare"
    assert summary["stages"][0]["declared_params"] == ["split.seed"]
    assert summary["stages"][1]["recorded_outs"] == ["publish/v1"]


def test_review_queue_returns_false_positive_and_false_negative_rows(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    queue = review_queue(tmp_path / "publish")

    assert queue["false_positive_count"] == 1
    assert queue["false_negative_count"] == 1
    assert queue["false_negatives"][0]["incident_id"] == "INC-2"


def test_threshold_review_returns_borderline_predictions(tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    review = threshold_review(tmp_path / "publish", margin=0.12, limit=2)

    assert review["threshold"] == 0.52
    assert review["near_threshold_count"] == 1
    assert review["near_threshold"][0]["incident_id"] == "INC-2"


def test_cli_prints_release_summary_json(capsys, tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    exit_code = main(["release-summary", "--publish", str(tmp_path / "publish")])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["artifact_count"] == 5


def test_cli_prints_profile_summary_json(capsys, tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    exit_code = main(["profile-summary", "--publish", str(tmp_path / "publish")])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["team_count"] == 2
    assert payload["largest_team"]["team"] == "billing"


def test_cli_prints_model_summary_json(capsys, tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    exit_code = main(["model-summary", "--publish", str(tmp_path / "publish")])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["training_rows"] == 18
    assert payload["strongest_feature"]["name"] == "severity_score"


def test_cli_prints_stage_summary_json(capsys, tmp_path: Path) -> None:
    (tmp_path / "dvc.yaml").write_text(
        "stages:\n  evaluate:\n    deps:\n      - models/model.json\n    outs:\n      - state/predictions.csv\n",
        encoding="utf-8",
    )
    (tmp_path / "dvc.lock").write_text(
        "stages:\n  evaluate:\n    deps:\n      - path: models/model.json\n    outs:\n      - path: state/predictions.csv\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "stage-summary",
            "--pipeline",
            str(tmp_path / "dvc.yaml"),
            "--lock",
            str(tmp_path / "dvc.lock"),
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["stage_count"] == 1
    assert payload["stages"][0]["stage_name"] == "evaluate"


def test_cli_prints_threshold_review_json(capsys, tmp_path: Path) -> None:
    _write_publish_fixture(tmp_path)

    exit_code = main(
        [
            "threshold-review",
            "--publish",
            str(tmp_path / "publish"),
            "--margin",
            "0.12",
            "--limit",
            "1",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["near_threshold_count"] == 1
    assert payload["near_threshold"][0]["incident_id"] == "INC-2"
