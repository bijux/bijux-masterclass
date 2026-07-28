from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_consumer_contract.py"
SPEC = importlib.util.spec_from_file_location("verify_consumer_contract", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
verify_bundle = MODULE.verify_bundle


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_contract(path: Path, *, allow_additional_fields: bool = True) -> None:
    write_json(
        path,
        {
            "publish_version": "v1",
            "required_paths": ["summary.json"],
            "artifact_path": "summary.json",
            "artifact_schema_version": 1,
            "required_fields": {"reads_count": "integer", "sample_id": "string"},
            "optional_fields": {"qc_status": "string"},
            "allow_additional_fields": allow_additional_fields,
            "field_semantics": {
                "reads_count": {
                    "definition": "number of sequencing reads",
                    "unit": "reads",
                }
            },
        },
    )


def write_bundle(
    path: Path,
    *,
    record: dict[str, object] | None = None,
    semantics: dict[str, object] | None = None,
) -> None:
    summary = path / "summary.json"
    write_json(
        summary,
        {
            "schema_version": 1,
            "field_semantics": semantics
            or {
                "reads_count": {
                    "definition": "number of sequencing reads",
                    "unit": "reads",
                }
            },
            "records": [record or {"sample_id": "alpha", "reads_count": 10}],
        },
    )
    write_json(
        path / "manifest.json",
        {
            "schema_version": 1,
            "publish_version": "v1",
            "files": [{"path": "summary.json", "sha256": digest(summary)}],
        },
    )


def test_consumer_accepts_required_fields_and_additive_optional_data(tmp_path: Path) -> None:
    contract = tmp_path / "consumer.json"
    write_contract(contract)
    bundle = tmp_path / "bundle"
    write_bundle(
        bundle,
        record={"sample_id": "alpha", "reads_count": 10, "qc_status": "pass"},
    )

    report = verify_bundle(bundle, contract)

    assert report["compatible"] is True
    assert report["failures"] == []
    assert report["observations"]["observed_fields"] == [
        "qc_status",
        "reads_count",
        "sample_id",
    ]


def test_consumer_rejects_missing_required_field(tmp_path: Path) -> None:
    contract = tmp_path / "consumer.json"
    write_contract(contract)
    bundle = tmp_path / "bundle"
    write_bundle(bundle, record={"sample_id": "alpha"})

    report = verify_bundle(bundle, contract)

    assert report["compatible"] is False
    assert "record 0 is missing required field reads_count" in report["failures"]


def test_consumer_rejects_semantic_drift_without_a_type_change(tmp_path: Path) -> None:
    contract = tmp_path / "consumer.json"
    write_contract(contract)
    bundle = tmp_path / "bundle"
    write_bundle(
        bundle,
        semantics={
            "reads_count": {
                "definition": "number of nucleotide bases",
                "unit": "bases",
            }
        },
    )

    report = verify_bundle(bundle, contract)

    assert report["compatible"] is False
    assert any("field semantics changed for reads_count" in item for item in report["failures"])


def test_consumer_rejects_checksum_mismatch(tmp_path: Path) -> None:
    contract = tmp_path / "consumer.json"
    write_contract(contract)
    bundle = tmp_path / "bundle"
    write_bundle(bundle)
    (bundle / "summary.json").write_text("{}\n", encoding="utf-8")

    report = verify_bundle(bundle, contract)

    assert report["compatible"] is False
    assert "checksum mismatch: summary.json" in report["failures"]


def test_closed_consumer_rejects_undeclared_fields(tmp_path: Path) -> None:
    contract = tmp_path / "consumer.json"
    write_contract(contract, allow_additional_fields=False)
    bundle = tmp_path / "bundle"
    write_bundle(
        bundle,
        record={"sample_id": "alpha", "reads_count": 10, "new_metric": 4},
    )

    report = verify_bundle(bundle, contract)

    assert report["compatible"] is False
    assert "record 0 has unsupported additional fields: ['new_metric']" in report["failures"]
