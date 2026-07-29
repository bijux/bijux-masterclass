"""Executable learning proofs for the Module 10 sustainment workflow."""

from __future__ import annotations

from pathlib import Path

from funcpipe_rag.boundaries.shells.review_cli import build_summary

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_review_inventory_counts_nested_sources_once() -> None:
    """A refactor starts with a trustworthy observation, not an inflated metric."""

    summary = build_summary(PROJECT_ROOT)
    rag_group = next(
        group for group in summary["package_groups"] if group["name"] == "rag-model"
    )
    observed_files = {
        path.resolve()
        for relative in rag_group["paths"]
        for path in (PROJECT_ROOT / relative).rglob("*.py")
    }

    assert rag_group["python_file_count"] == len(observed_files)
