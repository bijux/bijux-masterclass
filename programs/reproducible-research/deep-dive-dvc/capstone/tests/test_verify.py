from pathlib import Path

from incident_escalation_capstone.common import sha256_file, write_json
from incident_escalation_capstone.verify import verify_manifest, verify_metrics, verify_report


def test_verify_manifest_accepts_matching_hashes(tmp_path: Path) -> None:
    payloads = {
        "data-profile.json": '{"rows": 8}',
        "metrics.json": '{"accuracy": 0.9}',
        "model.json": '{"feature_names": []}',
        "params.yaml": "split:\n  test_fraction: 0.25\ntraining:\n  learning_rate: 0.1\ndecision:\n  threshold: 0.5\n",
        "predictions.csv": "incident_id,team,actual,predicted,probability\n1,core,1,1,0.9\n",
        "report.md": "# Incident Escalation Reference Report\n## Data Profile\n## Evaluation Metrics\n## Model Summary\n## Review Queue\n",
    }
    manifest_artifacts = []
    for name, content in payloads.items():
        artifact = tmp_path / name
        artifact.write_text(content, encoding="utf-8")
        manifest_artifacts.append(
            {
                "path": name,
                "sha256": sha256_file(artifact),
                "bytes": artifact.stat().st_size,
            }
        )
    manifest = {"artifacts": manifest_artifacts}
    write_json(tmp_path / "manifest.json", manifest)
    report = verify_manifest(tmp_path)
    assert report["artifact_count"] == len(payloads)


def test_verify_metrics_rejects_out_of_range_values(tmp_path: Path) -> None:
    write_json(
        tmp_path / "metrics.json",
        {
            "accuracy": 1.2,
            "precision": 0.8,
            "recall": 0.7,
            "f1": 0.75,
            "eval_rows": 4,
        },
    )

    try:
        verify_metrics(tmp_path)
    except ValueError as exc:
        assert "accuracy" in str(exc)
    else:
        raise AssertionError("verify_metrics should reject invalid values")


def test_verify_report_requires_review_sections(tmp_path: Path) -> None:
    (tmp_path / "report.md").write_text("# Incident Escalation Reference Report\n", encoding="utf-8")

    try:
        verify_report(tmp_path)
    except ValueError as exc:
        assert "missing heading" in str(exc)
    else:
        raise AssertionError("verify_report should reject incomplete reports")


def test_verify_report_returns_heading_summary(tmp_path: Path) -> None:
    (tmp_path / "report.md").write_text(
        "\n".join(
            [
                "# Incident Escalation Reference Report",
                "## Data Profile",
                "## Evaluation Metrics",
                "## Model Summary",
                "## Review Queue",
            ]
        ),
        encoding="utf-8",
    )

    report = verify_report(tmp_path)
    assert report["check"] == "report"
    assert "## Evaluation Metrics" in report["headings"]
