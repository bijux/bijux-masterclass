from __future__ import annotations

import uuid
from typing import Any

from .digest import digest_hex


def cyclonedx_bom(
    *,
    image_digest: str,
    name: str,
    version: str,
    components: list[dict[str, Any]],
) -> dict[str, Any]:
    serial = uuid.uuid5(uuid.NAMESPACE_URL, "urn:atlas:image:" + image_digest)
    normalized = []
    for component in sorted(components, key=lambda item: item["bom-ref"]):
        normalized.append(dict(component))
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.7",
        "serialNumber": f"urn:uuid:{serial}",
        "version": 1,
        "metadata": {
            "timestamp": "1970-01-01T00:00:00Z",
            "component": {
                "type": "container",
                "bom-ref": image_digest,
                "name": name,
                "version": version,
                "hashes": [{"alg": "SHA-256", "content": digest_hex(image_digest)}],
            },
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "name": "atlas-sbom-generator",
                        "version": "1.0.0",
                    }
                ]
            },
        },
        "components": normalized,
        "dependencies": [
            {"ref": image_digest, "dependsOn": [item["bom-ref"] for item in normalized]}
        ] + [{"ref": item["bom-ref"], "dependsOn": []} for item in normalized],
        "compositions": [{"aggregate": "complete", "assemblies": [image_digest]}],
    }


def validate_cyclonedx(bom: dict[str, Any], image_digest: str) -> list[str]:
    errors: list[str] = []
    if bom.get("bomFormat") != "CycloneDX" or bom.get("specVersion") != "1.7":
        errors.append("expected CycloneDX 1.7")
    component = bom.get("metadata", {}).get("component", {})
    if component.get("bom-ref") != image_digest:
        errors.append("SBOM subject does not match image digest")
    components = bom.get("components")
    if not isinstance(components, list) or not components:
        errors.append("SBOM contains no components")
    refs = set()
    for item in components or []:
        ref = item.get("bom-ref")
        if not ref or ref in refs:
            errors.append("component references must be present and unique")
        refs.add(ref)
        if not item.get("purl"):
            errors.append(f"component {ref!r} lacks a package URL")
        if not item.get("version"):
            errors.append(f"component {ref!r} lacks a version")
    compositions = bom.get("compositions", [])
    if not any(item.get("aggregate") == "complete" for item in compositions):
        errors.append("SBOM completeness is not declared")
    return errors
