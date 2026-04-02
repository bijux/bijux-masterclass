from __future__ import annotations

import json
from pathlib import Path

from funcpipe_rag.boundaries.shells.review_cli import build_summary, main, render_text


PROJECT_ROOT = Path(__file__).resolve().parents[4]


def test_build_summary_reports_expected_groups() -> None:
    summary = build_summary(PROJECT_ROOT)

    package_names = [group["name"] for group in summary["package_groups"]]
    test_names = [group["name"] for group in summary["test_groups"]]
    route_names = [route["name"] for route in summary["proof_routes"]]

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
    assert all(group["python_file_count"] > 0 for group in summary["package_groups"])
    assert all(group["python_file_count"] > 0 for group in summary["test_groups"])


def test_render_text_mentions_review_surfaces() -> None:
    summary = build_summary(PROJECT_ROOT)

    rendered = render_text(summary)

    assert "FuncPipe review summary" in rendered
    assert "functional-core" in rendered
    assert "algebra-and-laws" in rendered
    assert "make proof" in rendered


def test_main_can_render_json(capsys) -> None:
    exit_code = main(["summary", "--format", "json", "--project-root", str(PROJECT_ROOT)])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["project_root"] == PROJECT_ROOT.resolve().as_posix()
    assert payload["proof_routes"][0]["name"] == "demo"
