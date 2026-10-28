from __future__ import annotations

from typing import Any


def slsa_provenance(
    *,
    subject_name: str,
    subject_digest: str,
    source_uri: str,
    source_digest: str,
    builder_id: str,
    build_type: str,
    invocation_id: str,
    parameters: dict[str, Any],
    materials: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {"name": subject_name, "digest": {"sha256": subject_digest.split(":", 1)[1]}}
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": build_type,
                "externalParameters": parameters,
                "internalParameters": {},
                "resolvedDependencies": [
                    {"uri": source_uri, "digest": {"sha256": source_digest.split(":", 1)[1]}}
                ] + materials,
            },
            "runDetails": {
                "builder": {"id": builder_id},
                "metadata": {
                    "invocationId": invocation_id,
                    "startedOn": "1970-01-01T00:00:00Z",
                    "finishedOn": "1970-01-01T00:00:00Z",
                },
                "byproducts": [],
            },
        },
    }


def validate_provenance(
    statement: dict[str, Any],
    *,
    subject_digest: str,
    trusted_builder: str,
    source_digest: str,
) -> list[str]:
    errors: list[str] = []
    if statement.get("_type") != "https://in-toto.io/Statement/v1":
        errors.append("unsupported in-toto statement type")
    if statement.get("predicateType") != "https://slsa.dev/provenance/v1":
        errors.append("unsupported provenance predicate")
    subjects = statement.get("subject", [])
    expected = subject_digest.split(":", 1)[1]
    if len(subjects) != 1 or subjects[0].get("digest", {}).get("sha256") != expected:
        errors.append("provenance subject digest mismatch")
    predicate = statement.get("predicate", {})
    if predicate.get("runDetails", {}).get("builder", {}).get("id") != trusted_builder:
        errors.append("provenance builder is not trusted")
    dependencies = predicate.get("buildDefinition", {}).get("resolvedDependencies", [])
    expected_source = source_digest.split(":", 1)[1]
    if not any(dep.get("digest", {}).get("sha256") == expected_source for dep in dependencies):
        errors.append("provenance does not identify the expected source digest")
    return errors
