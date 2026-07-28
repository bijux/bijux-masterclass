from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = CAPSTONE_ROOT / "scripts" / "audit_publish_compatibility.py"
SPECIMENS = CAPSTONE_ROOT / "repro" / "publish-compatibility"


def run_audit(tmp_path: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, object]]:
    specimens = tmp_path / "specimens"
    if not specimens.exists():
        shutil.copytree(SPECIMENS, specimens)
    output = tmp_path / "report" / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--specimens",
            str(specimens),
            "--workspace",
            str(tmp_path / "workspace"),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result, json.loads(output.read_text(encoding="utf-8"))


def case(payload: dict[str, object], name: str) -> dict[str, object]:
    cases = payload["cases"]
    assert isinstance(cases, list)
    return next(item for item in cases if item["case"] == name)


def update_json(path: Path, mutate) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_audit_classifies_compatible_breaking_and_versioned_changes(tmp_path: Path) -> None:
    result, payload = run_audit(tmp_path)

    assert result.returncode == 0
    assert payload["schema"] == "deep-dive-snakemake-publish-compatibility-audit"
    assert payload["contract_failures"] == []
    assert [(item["case"], item["decision"]) for item in payload["cases"]] == [
        ("baseline", "ACCEPT_CURRENT"),
        ("additive-field", "ACCEPT_CURRENT"),
        ("required-field-removal", "REJECT_CURRENT"),
        ("path-rename", "REJECT_CURRENT"),
        ("semantic-drift", "REJECT_CURRENT"),
        ("integrity-corruption", "REJECT_CURRENT"),
        ("versioned-migration", "REQUIRE_MIGRATION"),
    ]


def test_audit_rejects_an_additive_case_that_removes_required_data(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    definition = tmp_path / "specimens" / "cases" / "additive-field.json"
    update_json(definition, lambda payload: payload["records"][0].pop("reads_count"))

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert case(payload, "additive-field")["result"] == "FAIL"
    assert any(
        "decision must be ACCEPT_CURRENT" in failure
        for failure in case(payload, "additive-field")["failures"]
    )


def test_audit_rejects_a_semantic_counterexample_that_no_longer_drifts(
    tmp_path: Path,
) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    definition = tmp_path / "specimens" / "cases" / "semantic-drift.json"

    def restore_reads(payload):
        payload["field_semantics"]["reads_count"] = {
            "definition": "number of sequencing reads",
            "unit": "reads",
        }

    update_json(definition, restore_reads)
    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    failures = case(payload, "semantic-drift")["failures"]
    assert "semantic-drift no longer exhibits its named change" in failures


def test_audit_rejects_integrity_evidence_without_corruption(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    definition = tmp_path / "specimens" / "cases" / "integrity-corruption.json"
    update_json(definition, lambda payload: payload.update(corrupt_after_manifest=False))

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    failures = case(payload, "integrity-corruption")["failures"]
    assert "integrity-corruption no longer exhibits its named change" in failures


def test_audit_rejects_a_weakened_current_consumer_contract(tmp_path: Path) -> None:
    shutil.copytree(SPECIMENS, tmp_path / "specimens")
    contract = tmp_path / "specimens" / "consumer-v1.json"
    update_json(contract, lambda payload: payload["required_fields"].pop("reads_count"))

    result, payload = run_audit(tmp_path)

    assert result.returncode == 1
    assert "current consumer required fields changed" in payload["contract_failures"]
