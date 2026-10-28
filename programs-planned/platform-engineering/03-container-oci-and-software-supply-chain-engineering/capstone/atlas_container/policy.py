from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .provenance import validate_provenance
from .runtime_config import validate_runtime_config
from .sbom import validate_cyclonedx
from .signing import verify_envelope
from .vulnerability import VulnerabilityFinding, evaluate


@dataclass(frozen=True)
class PolicyDecision:
    status: str
    reasons: tuple[str, ...]


def evaluate_release(
    *,
    release: dict[str, Any],
    runtime_config: dict[str, Any],
    sbom: dict[str, Any],
    findings: list[VulnerabilityFinding],
    vex: list[dict[str, Any]],
    provenance_envelope: dict[str, Any],
    trusted_key: Ed25519PublicKey,
    policy: dict[str, Any],
) -> PolicyDecision:
    errors: list[str] = []
    image_digest = release.get("imageDigest", "")
    if not image_digest.startswith("sha256:"):
        errors.append("release must identify an image by digest")
    platforms = {(item.get("os"), item.get("architecture")) for item in release.get("platforms", [])}
    required = {(item["os"], item["architecture"]) for item in policy.get("requiredPlatforms", [])}
    if not required.issubset(platforms):
        errors.append("release lacks one or more required platforms")
    errors.extend(validate_runtime_config(runtime_config))
    errors.extend(validate_cyclonedx(sbom, image_digest))
    errors.extend(evaluate(findings, vex, policy.get("blockSeverity", "critical")))
    try:
        statement = verify_envelope(
            provenance_envelope,
            trusted_key,
            policy.get("trustedKeyFingerprint"),
            "application/vnd.in-toto+json",
        )
        errors.extend(
            validate_provenance(
                statement,
                subject_digest=image_digest,
                trusted_builder=policy["trustedBuilder"],
                source_digest=release["sourceDigest"],
            )
        )
    except Exception as exc:
        errors.append(f"provenance signature verification failed: {exc}")
    if release.get("tagOnlyReference"):
        errors.append("deployment reference must not rely on a mutable tag")
    if release.get("evidenceClass") not in policy.get("allowedEvidenceClasses", []):
        errors.append("release evidence class is not accepted by policy")
    return PolicyDecision("accepted" if not errors else "rejected", tuple(errors))
