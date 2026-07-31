from __future__ import annotations

import json
from pathlib import Path

from funcpipe_rag.boundaries.shells.review_cli import (
    _count_python_files,
    build_summary,
    main,
    render_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def test_build_summary_reports_expected_groups() -> None:
    summary = build_summary(PROJECT_ROOT)

    package_names = [group["name"] for group in summary["package_groups"]]
    test_names = [group["name"] for group in summary["test_groups"]]
    route_names = [route["name"] for route in summary["proof_routes"]]
    claim_names = [claim["name"] for claim in summary["evidence_claims"]]

    assert package_names == [
        "functional-core",
        "rag-model",
        "orchestration-and-policy",
        "effect-boundaries",
        "interop",
    ]
    assert test_names == [
        "algebra-and-laws",
        "functional-toolkit",
        "application-model",
        "pipeline-and-policy",
        "edges-and-effects",
    ]
    assert route_names == ["demo", "test", "tour", "proof"]
    assert claim_names == [
        "change-acceptance",
        "performance-decision",
        "regression-equivalence",
        "async-contracts",
        "migration-review",
    ]
    change_claim = summary["evidence_claims"][0]
    assert change_claim["required_paths"] == [
        "src/funcpipe_rag/review/change.py",
        "tests/unit/review/test_change.py",
    ]
    assert change_claim["command"] == "pytest -q tests/unit/review/test_change.py"
    assert change_claim["missing_paths"] == []
    assert all(claim["complete"] for claim in summary["evidence_claims"])
    assert all(group["python_file_count"] > 0 for group in summary["package_groups"])
    assert {group["owner"] for group in summary["package_groups"]} == {
        "boundary-integrations",
        "ecosystem-interop",
        "functional-foundations",
        "pipeline-runtime",
        "rag-domain",
    }
    assert all(group["python_file_count"] > 0 for group in summary["test_groups"])


def test_python_file_count_deduplicates_nested_review_paths(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    nested = package / "domain"
    nested.mkdir(parents=True)
    (package / "api.py").write_text("", encoding="utf-8")
    (nested / "model.py").write_text("", encoding="utf-8")

    assert _count_python_files((package, nested)) == 2


def test_render_text_mentions_review_surfaces() -> None:
    summary = build_summary(PROJECT_ROOT)

    rendered = render_text(summary)

    assert "FuncPipe review summary" in rendered
    assert "functional-core" in rendered
    assert "owner=functional-foundations" in rendered
    assert "algebra-and-laws" in rendered
    assert "make proof" in rendered
    assert "change-acceptance: complete" in rendered
    assert "regression-equivalence: complete" in rendered


def test_main_can_render_json(capsys) -> None:
    exit_code = main(["summary", "--format", "json", "--project-root", str(PROJECT_ROOT)])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["project_root"] == PROJECT_ROOT.resolve().as_posix()
    assert payload["proof_routes"][0]["name"] == "demo"


def test_check_returns_nonzero_when_evidence_paths_are_missing(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = main(["check", "--format", "json", "--project-root", str(tmp_path)])

    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert all(not claim["complete"] for claim in payload["evidence_claims"])
    assert all(claim["missing_paths"] for claim in payload["evidence_claims"])
