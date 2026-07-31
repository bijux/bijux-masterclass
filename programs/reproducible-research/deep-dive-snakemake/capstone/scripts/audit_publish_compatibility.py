#!/usr/bin/env python3
"""Classify publish changes against explicit old and new consumer contracts."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from verify_consumer_contract import load_json, verify_bundle

CASE_ORDER = (
    "baseline",
    "additive-field",
    "required-field-removal",
    "path-rename",
    "semantic-drift",
    "integrity-corruption",
    "versioned-migration",
)

EXPECTED_DECISIONS = {
    "baseline": "ACCEPT_CURRENT",
    "additive-field": "ACCEPT_CURRENT",
    "required-field-removal": "REJECT_CURRENT",
    "path-rename": "REJECT_CURRENT",
    "semantic-drift": "REJECT_CURRENT",
    "integrity-corruption": "REJECT_CURRENT",
    "versioned-migration": "REQUIRE_MIGRATION",
}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_case(definition_path: Path, workspace: Path) -> tuple[Path, dict[str, Any]]:
    definition = load_json(definition_path)
    bundle = workspace / definition_path.stem / "publish" / definition["publish_version"]
    artifact = bundle / definition["artifact_path"]
    write_json(
        artifact,
        {
            "schema_version": definition["artifact_schema_version"],
            "field_semantics": definition["field_semantics"],
            "records": definition["records"],
        },
    )
    write_json(
        bundle / "manifest.json",
        {
            "schema_version": 1,
            "publish_version": definition["publish_version"],
            "files": [
                {
                    "path": definition["artifact_path"],
                    "sha256": digest(artifact),
                }
            ],
        },
    )
    if definition["corrupt_after_manifest"]:
        artifact.write_text(artifact.read_text(encoding="utf-8") + " \n", encoding="utf-8")
    return bundle, definition


def inspect_scenario(name: str, definition: dict[str, Any]) -> list[str]:
    records = definition["records"]
    first = records[0] if records else {}
    semantics = definition["field_semantics"]
    checks = {
        "baseline": (
            definition["publish_version"] == "v1"
            and definition["artifact_path"] == "summary.json"
            and first.get("reads_count") == 10
        ),
        "additive-field": (
            first.get("reads_count") == 10
            and first.get("qc_status") == "pass"
            and "qc_status" in semantics
        ),
        "required-field-removal": "reads_count" not in first,
        "path-rename": (
            definition["publish_version"] == "v1" and definition["artifact_path"] == "metrics.json"
        ),
        "semantic-drift": (
            "reads_count" in first and semantics.get("reads_count", {}).get("unit") == "bases"
        ),
        "integrity-corruption": definition["corrupt_after_manifest"] is True,
        "versioned-migration": (
            definition["publish_version"] == "v2"
            and definition["artifact_path"] == "metrics.json"
            and definition["artifact_schema_version"] == 2
            and "read_bases" in first
        ),
    }
    return [] if checks[name] else [f"{name} no longer exhibits its named change"]


def inspect_contracts(current: dict[str, Any], next_contract: dict[str, Any]) -> list[str]:
    failures = []
    if current.get("publish_version") != "v1":
        failures.append("current consumer must bind publish version v1")
    if current.get("artifact_path") != "summary.json":
        failures.append("current consumer must bind summary.json")
    if current.get("required_fields") != {
        "reads_count": "integer",
        "sample_id": "string",
    }:
        failures.append("current consumer required fields changed")
    expected_semantics = {
        "definition": "number of sequencing reads",
        "unit": "reads",
    }
    if current.get("field_semantics", {}).get("reads_count") != expected_semantics:
        failures.append("current consumer reads_count semantics changed")
    if next_contract.get("publish_version") != "v2":
        failures.append("next consumer must bind publish version v2")
    if next_contract.get("artifact_path") != "metrics.json":
        failures.append("next consumer must bind metrics.json")
    if next_contract.get("required_fields") != {
        "read_bases": "integer",
        "sample_id": "string",
    }:
        failures.append("next consumer required fields changed")
    return failures


def classify_case(
    name: str,
    definition_path: Path,
    workspace: Path,
    current_contract: Path,
    next_contract: Path,
) -> dict[str, Any]:
    bundle, definition = materialize_case(definition_path, workspace)
    current_report = verify_bundle(bundle, current_contract)
    next_report = verify_bundle(bundle, next_contract)

    if not current_report["compatible"] and next_report["compatible"]:
        decision = "REQUIRE_MIGRATION"
    elif current_report["compatible"]:
        decision = "ACCEPT_CURRENT"
    else:
        decision = "REJECT_CURRENT"

    failures = inspect_scenario(name, definition)
    expected = EXPECTED_DECISIONS[name]
    if decision != expected:
        failures.append(f"decision must be {expected}, observed {decision}")

    return {
        "case": name,
        "result": "PASS" if not failures else "FAIL",
        "decision": decision,
        "expected_decision": expected,
        "failures": failures,
        "definition": definition,
        "current_consumer": current_report,
        "next_consumer": next_report,
        "bundle": bundle.relative_to(workspace).as_posix(),
    }


def write_summary(path: Path, cases: list[dict[str, Any]]) -> None:
    lines = ["case\tresult\tdecision\tcurrent_compatible\tnext_compatible\tcurrent_first_failure"]
    for case in cases:
        current = case["current_consumer"]
        first_failure = current["failures"][0] if current["failures"] else ""
        lines.append(
            "\t".join(
                (
                    case["case"],
                    case["result"],
                    case["decision"],
                    str(current["compatible"]).lower(),
                    str(case["next_consumer"]["compatible"]).lower(),
                    first_failure,
                )
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--specimens", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    specimens = args.specimens.resolve()
    workspace = args.workspace.resolve()
    output = args.output.resolve()
    current_contract = specimens / "consumer-v1.json"
    next_contract = specimens / "consumer-v2.json"

    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)

    contract_failures = inspect_contracts(
        load_json(current_contract),
        load_json(next_contract),
    )
    cases = [
        classify_case(
            name,
            specimens / "cases" / f"{name}.json",
            workspace,
            current_contract,
            next_contract,
        )
        for name in CASE_ORDER
    ]
    report = {
        "schema": "deep-dive-snakemake-publish-compatibility-audit",
        "specimens": specimens.as_posix(),
        "workspace": workspace.as_posix(),
        "contract_failures": contract_failures,
        "cases": cases,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_summary(output.parent / "summary.tsv", cases)

    failed_cases = [case["case"] for case in cases if case["result"] != "PASS"]
    if contract_failures or failed_cases:
        details = contract_failures + [f"case failed: {name}" for name in failed_cases]
        print(f"FAIL: publish compatibility audit rejected: {'; '.join(details)}")
        return 1
    print(f"PASS: classified publish compatibility in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
