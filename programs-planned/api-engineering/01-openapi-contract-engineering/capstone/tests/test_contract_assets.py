from __future__ import annotations

from pathlib import Path

from scripts.spec_tools import (
    ROOT,
    SPEC_DIR,
    bundle_document,
    compare_contracts,
    operation_ledger,
    validate_arazzo,
    validate_examples,
    validate_fixture_manifest,
    validate_openapi_structure,
    validate_references,
    load_yaml,
)


def test_baseline_and_frontier_are_structurally_sound() -> None:
    baseline = bundle_document(SPEC_DIR / "openapi.yaml")
    frontier = bundle_document(SPEC_DIR / "openapi-3.2.yaml")
    assert validate_openapi_structure(baseline, "3.1.2") == []
    assert validate_openapi_structure(frontier, "3.2.0") == []
    assert validate_references(SPEC_DIR / "openapi.yaml") == []
    assert validate_references(SPEC_DIR / "openapi-3.2.yaml") == []
    assert validate_examples(baseline) == []
    assert validate_examples(frontier) == []


def test_contract_contains_real_provider_surface_and_events() -> None:
    rows = operation_ledger(bundle_document(SPEC_DIR / "openapi.yaml"))
    path_rows = [row for row in rows if row["path"].startswith("/")]
    assert len(path_rows) == 19
    assert any("callback:" in row["path"] for row in rows)
    assert any(row["path"].startswith("webhook:") for row in rows)
    assert len({row["operationId"] for row in rows}) == len(rows)


def test_schema_fixture_corpus_has_depth() -> None:
    count, errors = validate_fixture_manifest(
        bundle_document(SPEC_DIR / "openapi.yaml"),
        ROOT / "tests/fixtures/schema/manifest.yaml",
    )
    assert errors == []
    assert count >= 60


def test_release_fixture_blocks_minor_breaks() -> None:
    releases = ROOT / "releases"
    compatible = compare_contracts(
        load_yaml(releases / "v1.0/openapi.yaml"),
        load_yaml(releases / "v1.1/openapi.yaml"),
    )
    blocked = compare_contracts(
        load_yaml(releases / "v1.1/openapi.yaml"),
        load_yaml(releases / "attempted-v1.2-breaking/openapi.yaml"),
    )
    assert compatible["compatible"] is True
    assert blocked["compatible"] is False
    assert {item["reason"] for item in blocked["breaking"]} >= {
        "operationId changed",
        "response removed",
        "regular-expression constraint changed",
    }


def test_arazzo_references_real_operations() -> None:
    spec = bundle_document(SPEC_DIR / "openapi.yaml")
    workflow = load_yaml(SPEC_DIR / "workflows/analysis-run.arazzo.yaml")
    assert validate_arazzo(workflow, spec) == []
