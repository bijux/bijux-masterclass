from __future__ import annotations

from copy import deepcopy

import pytest

from atlas_container.policy import evaluate_release
from atlas_container.provenance import slsa_provenance, validate_provenance
from atlas_container.runtime_config import atlas_runtime_config
from atlas_container.sbom import cyclonedx_bom, validate_cyclonedx
from atlas_container.signing import (
    fixture_private_key,
    key_fingerprint,
    sign_statement,
    verify_envelope,
)
from atlas_container.vulnerability import scan


IMAGE = "sha256:" + "1" * 64
SOURCE = "sha256:" + "2" * 64
BUILDER = "https://build.atlas.invalid/isolated-builder/v1"


def _evidence():
    components = [
        {
            "type": "application",
            "bom-ref": "pkg:generic/atlas@1.0.0",
            "name": "atlas",
            "version": "1.0.0",
            "purl": "pkg:generic/atlas@1.0.0",
        }
    ]
    bom = cyclonedx_bom(
        image_digest=IMAGE, name="atlas", version="1.0.0", components=components
    )
    statement = slsa_provenance(
        subject_name="atlas",
        subject_digest=IMAGE,
        source_uri="git+https://example.invalid/atlas",
        source_digest=SOURCE,
        builder_id=BUILDER,
        build_type="https://atlas.invalid/build/v1",
        invocation_id="fixture",
        parameters={},
        materials=[],
    )
    return components, bom, statement


def test_complete_sbom_and_signed_provenance_bind_to_subject() -> None:
    _, bom, statement = _evidence()
    assert validate_cyclonedx(bom, IMAGE) == []
    key = fixture_private_key()
    envelope = sign_statement(statement, key)
    decoded = verify_envelope(envelope, key.public_key(), key_fingerprint(key.public_key()))
    assert validate_provenance(
        decoded,
        subject_digest=IMAGE,
        trusted_builder=BUILDER,
        source_digest=SOURCE,
    ) == []


def test_tampered_envelope_is_rejected() -> None:
    _, _, statement = _evidence()
    key = fixture_private_key()
    envelope = sign_statement(statement, key)
    envelope["payload"] = envelope["payload"][:-2] + "AA"
    with pytest.raises(Exception):
        verify_envelope(envelope, key.public_key())


def test_release_policy_rejects_tag_only_untrusted_builder_and_missing_platform() -> None:
    components, bom, statement = _evidence()
    key = fixture_private_key()
    findings = scan(
        components,
        [
            {
                "id": "CVE-X",
                "purl": "pkg:generic/atlas@1.0.0",
                "severity": "critical",
                "fixedVersion": "1.0.1",
            }
        ],
    )
    vex = [
        {
            "id": "CVE-X",
            "status": "not_affected",
            "justification": "code_not_reachable",
            "impactStatement": "controlled fixture",
        }
    ]
    policy = {
        "requiredPlatforms": [
            {"os": "linux", "architecture": "amd64"},
            {"os": "linux", "architecture": "arm64"},
        ],
        "trustedBuilder": BUILDER,
        "trustedKeyFingerprint": key_fingerprint(key.public_key()),
        "blockSeverity": "critical",
        "allowedEvidenceClasses": ["dependency-light-local"],
    }
    release = {
        "imageDigest": IMAGE,
        "sourceDigest": SOURCE,
        "platforms": [
            {"os": "linux", "architecture": "amd64"},
            {"os": "linux", "architecture": "arm64"},
        ],
        "tagOnlyReference": False,
        "evidenceClass": "dependency-light-local",
    }
    accepted = evaluate_release(
        release=release,
        runtime_config=atlas_runtime_config(),
        sbom=bom,
        findings=findings,
        vex=vex,
        provenance_envelope=sign_statement(statement, key),
        trusted_key=key.public_key(),
        policy=policy,
    )
    assert accepted.status == "accepted"

    tag_only = deepcopy(release)
    tag_only["tagOnlyReference"] = True
    assert evaluate_release(
        release=tag_only,
        runtime_config=atlas_runtime_config(),
        sbom=bom,
        findings=findings,
        vex=vex,
        provenance_envelope=sign_statement(statement, key),
        trusted_key=key.public_key(),
        policy=policy,
    ).status == "rejected"

    one_platform = deepcopy(release)
    one_platform["platforms"] = [{"os": "linux", "architecture": "amd64"}]
    assert evaluate_release(
        release=one_platform,
        runtime_config=atlas_runtime_config(),
        sbom=bom,
        findings=findings,
        vex=vex,
        provenance_envelope=sign_statement(statement, key),
        trusted_key=key.public_key(),
        policy=policy,
    ).status == "rejected"

    untrusted = deepcopy(statement)
    untrusted["predicate"]["runDetails"]["builder"]["id"] = "https://evil.invalid"
    assert evaluate_release(
        release=release,
        runtime_config=atlas_runtime_config(),
        sbom=bom,
        findings=findings,
        vex=vex,
        provenance_envelope=sign_statement(untrusted, key),
        trusted_key=key.public_key(),
        policy=policy,
    ).status == "rejected"


def test_policy_rejects_valid_signature_with_wrong_dsse_payload_type() -> None:
    components, bom, statement = _evidence()
    key = fixture_private_key()
    release = {
        "imageDigest": IMAGE,
        "sourceDigest": SOURCE,
        "platforms": [
            {"os": "linux", "architecture": "amd64"},
            {"os": "linux", "architecture": "arm64"},
        ],
        "tagOnlyReference": False,
        "evidenceClass": "dependency-light-local",
    }
    policy = {
        "requiredPlatforms": [
            {"os": "linux", "architecture": "amd64"},
            {"os": "linux", "architecture": "arm64"},
        ],
        "trustedBuilder": BUILDER,
        "trustedKeyFingerprint": key_fingerprint(key.public_key()),
        "blockSeverity": "critical",
        "allowedEvidenceClasses": ["dependency-light-local"],
    }
    envelope = sign_statement(statement, key, payload_type="application/json")
    decision = evaluate_release(
        release=release,
        runtime_config=atlas_runtime_config(),
        sbom=bom,
        findings=[],
        vex=[],
        provenance_envelope=envelope,
        trusted_key=key.public_key(),
        policy=policy,
    )
    assert decision.status == "rejected"
    assert any("payload type" in reason for reason in decision.reasons)
