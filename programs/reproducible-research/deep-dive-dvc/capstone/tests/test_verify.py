from pathlib import Path

from incident_escalation_capstone.common import sha256_file, write_json
from incident_escalation_capstone.verify import verify_manifest, verify_metrics, verify_report


def test_verify_manifest_accepts_matching_hashes(tmp_path: Path) -> None:
    artifact = tmp_path / "metrics.json"
    artifact.write_text('{"accuracy": 0.9}', encoding="utf-8")
    manifest = {
        "artifacts": [
            {
                "path": "metrics.json",
                "sha256": sha256_file(artifact),
                "bytes": artifact.stat().st_size,
            }
        ]
    }
    write_json(tmp_path / "manifest.json", manifest)
    verify_manifest(tmp_path)


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
