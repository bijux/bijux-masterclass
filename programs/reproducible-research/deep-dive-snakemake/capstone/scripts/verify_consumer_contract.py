#!/usr/bin/env python3
"""Verify a versioned publish bundle from one declared consumer's perspective."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

JSON_TYPES = {
    "array": list,
    "boolean": bool,
    "integer": int,
    "number": (int, float),
    "object": dict,
    "string": str,
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_bundle(bundle: Path, contract_path: Path) -> dict[str, Any]:
    contract = load_json(contract_path)
    failures: list[str] = []
    manifest_path = bundle / "manifest.json"

    if not manifest_path.is_file():
        return {
            "compatible": False,
            "failures": ["manifest.json is missing"],
            "observations": {"bundle": bundle.resolve().as_posix()},
        }

    manifest = load_json(manifest_path)
    expected_version = contract["publish_version"]
    observed_version = manifest.get("publish_version")
    if observed_version != expected_version:
        failures.append(f"publish version must be {expected_version}, observed {observed_version}")

    entries = manifest.get("files", [])
    manifest_paths = [entry.get("path") for entry in entries]
    if manifest_paths != sorted(manifest_paths):
        failures.append("manifest paths must be in canonical order")
    if len(manifest_paths) != len(set(manifest_paths)):
        failures.append("manifest paths must be unique")

    required_paths = contract["required_paths"]
    missing_paths = sorted(set(required_paths) - set(manifest_paths))
    if missing_paths:
        failures.append(f"required publish paths are missing: {missing_paths}")

    integrity: dict[str, bool] = {}
    for entry in entries:
        relative = entry.get("path")
        if not isinstance(relative, str):
            failures.append("manifest entry path must be a string")
            continue
        artifact = bundle / relative
        if not artifact.is_file():
            integrity[relative] = False
            failures.append(f"manifest-listed artifact is missing: {relative}")
            continue
        matches = sha256(artifact) == entry.get("sha256")
        integrity[relative] = matches
        if not matches:
            failures.append(f"checksum mismatch: {relative}")

    artifact_relative = contract["artifact_path"]
    artifact_path = bundle / artifact_relative
    record_count = 0
    observed_fields: list[str] = []
    if artifact_path.is_file():
        artifact = load_json(artifact_path)
        expected_schema = contract["artifact_schema_version"]
        if artifact.get("schema_version") != expected_schema:
            failures.append(
                "artifact schema_version must be "
                f"{expected_schema}, observed {artifact.get('schema_version')}"
            )

        observed_semantics = artifact.get("field_semantics", {})
        for field, expected in contract["field_semantics"].items():
            if observed_semantics.get(field) != expected:
                failures.append(
                    f"field semantics changed for {field}: "
                    f"expected {expected}, observed {observed_semantics.get(field)}"
                )

        records = artifact.get("records")
        if not isinstance(records, list):
            failures.append("artifact records must be an array")
        else:
            record_count = len(records)
            required_fields = contract["required_fields"]
            allowed_fields = set(required_fields) | set(contract.get("optional_fields", {}))
            for position, record in enumerate(records):
                if not isinstance(record, dict):
                    failures.append(f"record {position} must be an object")
                    continue
                observed_fields = sorted(set(observed_fields) | set(record))
                for field, type_name in required_fields.items():
                    if field not in record:
                        failures.append(f"record {position} is missing required field {field}")
                        continue
                    expected_type = JSON_TYPES[type_name]
                    value = record[field]
                    if type_name == "integer" and isinstance(value, bool):
                        failures.append(f"record {position} field {field} must be {type_name}")
                    elif not isinstance(value, expected_type):
                        failures.append(f"record {position} field {field} must be {type_name}")
                if not contract.get("allow_additional_fields", False):
                    extras = sorted(set(record) - allowed_fields)
                    if extras:
                        failures.append(
                            f"record {position} has unsupported additional fields: {extras}"
                        )
    elif artifact_relative not in missing_paths:
        failures.append(f"consumer artifact is missing: {artifact_relative}")

    return {
        "compatible": not failures,
        "failures": failures,
        "observations": {
            "bundle": bundle.resolve().as_posix(),
            "contract": contract_path.resolve().as_posix(),
            "expected_publish_version": expected_version,
            "observed_publish_version": observed_version,
            "required_paths": required_paths,
            "manifest_paths": manifest_paths,
            "integrity": integrity,
            "record_count": record_count,
            "observed_fields": observed_fields,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = verify_bundle(args.bundle, args.contract)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if report["compatible"]:
        print("ACCEPT: bundle satisfies the consumer contract")
        return 0
    print("REJECT: bundle violates the consumer contract")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
