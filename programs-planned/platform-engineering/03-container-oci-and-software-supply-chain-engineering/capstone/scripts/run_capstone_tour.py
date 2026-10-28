#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]
CAPSTONE = COURSE / "capstone"
sys.path.insert(0, str(CAPSTONE))

from atlas_container.archive import LayerFile
from atlas_container.canonical import canonical_json_bytes, parse_json_object
from atlas_container.digest import sha256_digest
from atlas_container.handoff import write_handoff
from atlas_container.image import IMAGE_INDEX, IMAGE_MANIFEST, artifact_manifest, build_image, build_index
from atlas_container.layout import OciLayout
from atlas_container.mini_runtime import available as runtime_available, run_bundle
from atlas_container.platform import verify_platform_label
from atlas_container.policy import evaluate_release
from atlas_container.provenance import slsa_provenance
from atlas_container.registry import RegistryClient, RegistryServer, RegistryStore
from atlas_container.rootfs import unpack_manifest
from atlas_container.runtime_config import atlas_runtime_config
from atlas_container.sbom import cyclonedx_bom
from atlas_container.signing import fixture_private_key, key_fingerprint, private_key_pem, public_key_pem, sign_statement
from atlas_container.vulnerability import scan


def run(command: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{completed.stdout}\n{completed.stderr}")


def source_digest(source: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(source.rglob("*")):
        if path.is_file():
            rel = path.relative_to(source).as_posix().encode()
            digest.update(len(rel).to_bytes(4, "big"))
            digest.update(rel)
            body = path.read_bytes()
            digest.update(len(body).to_bytes(8, "big"))
            digest.update(body)
    return "sha256:" + digest.hexdigest()


def compile_binary(workload: Path, target: str, architecture: str, output: Path) -> bytes:
    env = dict(os.environ, CGO_ENABLED="0", GOOS="linux", GOARCH=architecture)
    run(
        ["go", "build", "-trimpath", "-ldflags=-s -w -buildid=", "-o", str(output), f"./cmd/{target}"],
        workload,
        env,
    )
    data = output.read_bytes()
    verify_platform_label(data, architecture)
    return data


def image_entries(binary_name: str, binary: bytes) -> list[LayerFile]:
    return [
        LayerFile("etc", mode=0o755, kind="directory"),
        LayerFile("etc/atlas", mode=0o755, kind="directory"),
        LayerFile("tmp", mode=0o1777, kind="directory"),
        LayerFile("proc", mode=0o555, kind="directory"),
        LayerFile("run", mode=0o755, kind="directory"),
        LayerFile("run/atlas", mode=0o755, kind="directory"),
        LayerFile("var", mode=0o755, kind="directory"),
        LayerFile("var/lib", mode=0o755, kind="directory"),
        LayerFile("var/lib/atlas", mode=0o770, kind="directory"),
        LayerFile("var/lib/atlas/spool", mode=0o770, kind="directory"),
        LayerFile("var/lib/atlas/results", mode=0o770, kind="directory"),
        LayerFile("usr", mode=0o755, kind="directory"),
        LayerFile("usr/local", mode=0o755, kind="directory"),
        LayerFile("usr/local/bin", mode=0o755, kind="directory"),
        LayerFile(f"usr/local/bin/{binary_name}", binary, 0o755),
        LayerFile("etc/atlas/release", b"1.0.0\n", 0o444),
    ]


def build_product(root: Path, workload: Path, target: str, binary_name: str) -> tuple[OciLayout, object, list[object], dict[str, bytes]]:
    layout = OciLayout(root)
    layout.initialize()
    manifests = []
    binaries = {}
    for architecture in ("amd64", "arm64"):
        output = root.parent / f"{target}-{architecture}"
        binary = compile_binary(workload, target, architecture, output)
        binaries[architecture] = binary
        built = build_image(
            layout,
            architecture=architecture,
            entries=image_entries(binary_name, binary),
            entrypoint=[f"/usr/local/bin/{binary_name}"],
            labels={
                "org.opencontainers.image.title": f"Atlas {target}",
                "org.opencontainers.image.version": "1.0.0",
                "org.opencontainers.image.licenses": "Apache-2.0",
            },
            annotations={
                "org.opencontainers.image.title": f"atlas-{target}",
                "org.opencontainers.image.version": "1.0.0",
            },
        )
        manifests.append(built.manifest)
    index = build_index(
        layout,
        manifests,
        {
            "org.opencontainers.image.title": f"atlas-{target}",
            "org.opencontainers.image.version": "1.0.0",
            "org.opencontainers.image.source": "https://example.invalid/atlas/platform",
        },
    )
    return layout, index, manifests, binaries


def push_layout(client: RegistryClient, repository: str, layout: OciLayout, root_index, manifests, tag: str) -> None:
    for blob in sorted(layout.blobs.glob("*")):
        client.push_blob(repository, blob.read_bytes())
    for descriptor in manifests:
        client.push_manifest(repository, descriptor.digest, layout.get_blob(descriptor.digest), IMAGE_MANIFEST)
    client.push_manifest(repository, root_index.digest, layout.get_blob(root_index.digest), IMAGE_INDEX)
    client.push_manifest(repository, tag, layout.get_blob(root_index.digest), IMAGE_INDEX)


def run_tour() -> dict[str, object]:
    checks: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="atlas-container-tour-") as td:
        work = Path(td)
        workload = CAPSTONE / "workload"
        api_layout, api_index, api_manifests, api_binaries = build_product(work / "api-layout", workload, "atlas-api", "atlas-api")
        worker_layout, worker_index, worker_manifests, _ = build_product(work / "worker-layout", workload, "atlas-worker", "atlas-worker")
        probe_layout, probe_index, probe_manifests, _ = build_product(work / "probe-layout", workload, "atlas-probe", "atlas-probe")
        second_layout, second_index, _, _ = build_product(work / "api-layout-second", workload, "atlas-api", "atlas-api")
        if api_index.digest != second_index.digest:
            raise AssertionError("two controlled builds did not produce the same OCI index digest")
        checks.append({"check": "deterministic-controlled-rebuild", "status": "passed", "digest": api_index.digest})

        # Source, per-image evidence, release policy, and registry transport.
        src_digest = source_digest(workload)
        components = json.loads((CAPSTONE / "sbom/components.json").read_text())
        vuln_db = json.loads((CAPSTONE / "sbom/vulnerability-database.json").read_text())
        findings = scan(components, vuln_db)
        vex = json.loads((CAPSTONE / "sbom/vex.json").read_text())
        key = fixture_private_key()
        policy = json.loads((CAPSTONE / "contracts/release-policy.json").read_text())
        policy["trustedKeyFingerprint"] = key_fingerprint(key.public_key())
        platforms = [
            {"os": "linux", "architecture": architecture}
            for architecture in ("amd64", "arm64")
        ]
        products = {
            "atlas-api": {
                "repository": "platform/atlas-api",
                "layout": api_layout,
                "index": api_index,
                "manifests": api_manifests,
                "runtime": atlas_runtime_config(executable="/usr/local/bin/atlas-api"),
            },
            "atlas-worker": {
                "repository": "platform/atlas-worker",
                "layout": worker_layout,
                "index": worker_index,
                "manifests": worker_manifests,
                "runtime": atlas_runtime_config(executable="/usr/local/bin/atlas-worker"),
            },
        }
        evidence: dict[str, dict[str, object]] = {}
        image_records: list[dict[str, object]] = []
        for ordinal, (name, product) in enumerate(products.items(), start=1):
            index = product["index"]
            assert hasattr(index, "digest")
            image_digest = index.digest
            repository = str(product["repository"])
            bom = cyclonedx_bom(
                image_digest=image_digest,
                name=name,
                version="1.0.0",
                components=components,
            )
            provenance = slsa_provenance(
                subject_name=f"registry.atlas.invalid/{repository}",
                subject_digest=image_digest,
                source_uri="git+https://example.invalid/atlas/platform@refs/tags/v1.0.0",
                source_digest=src_digest,
                builder_id="https://build.atlas.invalid/isolated-builder/v1",
                build_type="https://atlas.invalid/build-types/oci-go-v1",
                invocation_id=(
                    "urn:uuid:00000000-0000-0000-0000-"
                    f"{ordinal:012d}"
                ),
                parameters={
                    "target": name,
                    "platforms": ["linux/amd64", "linux/arm64"],
                },
                materials=[
                    {
                        "uri": "pkg:golang/stdlib@1.23.2",
                        "digest": {
                            "sha256": hashlib.sha256(b"go1.23.2").hexdigest()
                        },
                    }
                ],
            )
            envelope = sign_statement(provenance, key)
            image_release = {
                "release": "atlas-workload-release-1.0.0",
                "name": name,
                "repository": repository,
                "tag": "1.0.0",
                "imageDigest": image_digest,
                "sourceDigest": src_digest,
                "platforms": platforms,
                "tagOnlyReference": False,
                "evidenceClass": "dependency-light-local",
            }
            decision = evaluate_release(
                release=image_release,
                runtime_config=product["runtime"],
                sbom=bom,
                findings=findings,
                vex=vex,
                provenance_envelope=envelope,
                trusted_key=key.public_key(),
                policy=policy,
            )
            if decision.status != "accepted":
                raise AssertionError((name, decision.reasons))
            evidence[name] = {
                "bom": bom,
                "provenanceEnvelope": envelope,
                "decision": decision.status,
            }
            image_records.append(
                {
                    "name": name,
                    "repository": repository,
                    "digest": image_digest,
                    "platforms": platforms,
                    "runtimeUser": "65532:65532",
                    "entrypoint": product["runtime"]["process"]["args"],
                }
            )
        checks.append(
            {
                "check": "release-policy",
                "status": "passed",
                "acceptedImages": sorted(evidence),
            }
        )

        mutable = {
            "release": "atlas-workload-release-1.0.0",
            "name": "atlas-api",
            "repository": "platform/atlas-api",
            "tag": "latest",
            "imageDigest": api_index.digest,
            "sourceDigest": src_digest,
            "platforms": platforms,
            "tagOnlyReference": True,
            "evidenceClass": "dependency-light-local",
        }
        rejected_decision = evaluate_release(
            release=mutable,
            runtime_config=products["atlas-api"]["runtime"],
            sbom=evidence["atlas-api"]["bom"],
            findings=findings,
            vex=vex,
            provenance_envelope=evidence["atlas-api"]["provenanceEnvelope"],
            trusted_key=key.public_key(),
            policy=policy,
        )
        if rejected_decision.status != "rejected":
            raise AssertionError("tag-only release was not rejected")
        checks.append({"check": "mutable-tag-rejection", "status": "passed"})

        release = {
            "release": "atlas-workload-release-1.0.0",
            "sourceDigest": src_digest,
            "tag": "1.0.0",
            "tagOnlyReference": False,
            "evidenceClass": "dependency-light-local",
            # Compatibility fields used by the single-subject policy examples.
            "repository": "platform/atlas-api",
            "imageDigest": api_index.digest,
            "platforms": platforms,
            "images": image_records,
            "verificationImages": [
                {
                    "name": "atlas-probe",
                    "repository": "platform/atlas-probe",
                    "digest": probe_index.digest,
                    "platforms": platforms,
                    "deployByDefault": False,
                }
            ],
        }

        store = RegistryStore(work / "registry")
        server = RegistryServer(("127.0.0.1", 0), store)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        referrer_counts: dict[str, int] = {}
        try:
            client = RegistryClient(f"http://127.0.0.1:{server.server_port}")
            client.ping()
            for name, product in products.items():
                repository = str(product["repository"])
                layout = product["layout"]
                index = product["index"]
                manifests = product["manifests"]
                assert isinstance(layout, OciLayout)
                push_layout(client, repository, layout, index, manifests, "1.0.0")
                pulled, resolved_digest = client.get_manifest(repository, "1.0.0")
                if (
                    resolved_digest != index.digest
                    or sha256_digest(pulled) != index.digest
                ):
                    raise AssertionError(
                        f"registry tag for {name} did not resolve to the expected digest"
                    )

                sbom_desc = artifact_manifest(
                    layout,
                    subject=index,
                    artifact_type="application/vnd.cyclonedx+json",
                    payload=canonical_json_bytes(evidence[name]["bom"]),
                    payload_media_type="application/vnd.cyclonedx+json",
                    annotations={
                        "org.opencontainers.artifact.description": f"{name} CycloneDX SBOM"
                    },
                )
                provenance_desc = artifact_manifest(
                    layout,
                    subject=index,
                    artifact_type="application/vnd.in-toto+json",
                    payload=canonical_json_bytes(
                        evidence[name]["provenanceEnvelope"]
                    ),
                    payload_media_type="application/vnd.dsse.envelope.v1+json",
                    annotations={
                        "org.opencontainers.artifact.description": f"{name} signed SLSA provenance"
                    },
                )
                for blob in sorted(layout.blobs.glob("*")):
                    client.push_blob(repository, blob.read_bytes())
                for descriptor in (sbom_desc, provenance_desc):
                    client.push_manifest(
                        repository,
                        descriptor.digest,
                        layout.get_blob(descriptor.digest),
                        IMAGE_MANIFEST,
                    )
                refs = client.get_referrers(repository, index.digest)
                count = len(refs.get("manifests", []))
                if count != 2:
                    raise AssertionError(
                        f"registry did not return both evidence referrers for {name}"
                    )
                referrer_counts[name] = count
            checks.append(
                {
                    "check": "registry-distribution-and-referrers",
                    "status": "passed",
                    "referrers": referrer_counts,
                }
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

        # Runtime bundle for current architecture. The checked harness is
        # root-managed; it demonstrates workload identity and mount semantics,
        # not a fully rootless runtime architecture.
        runtime_cfg = atlas_runtime_config(executable="/usr/local/bin/atlas-probe")
        bundle = work / "bundle"
        rootfs = bundle / "rootfs"
        config = unpack_manifest(probe_layout, probe_manifests[0].digest, rootfs)
        # probe_manifests[0] is amd64 by construction
        (bundle / "config.json").write_text(json.dumps(runtime_cfg, indent=2, sort_keys=True) + "\n")
        if runtime_available():
            try:
                runtime_result = run_bundle(bundle, work / "state")
                expected = {
                    "uid": 65532,
                    "gid": 65532,
                    "hostname": "atlas-probe",
                    "tmpWritable": True,
                    "stateWritable": True,
                    "etcWritable": False,
                }
                for key_name, expected_value in expected.items():
                    if runtime_result.get(key_name) != expected_value:
                        raise AssertionError(f"runtime result {key_name}={runtime_result.get(key_name)!r}")
                checks.append({"check": "namespaced-readonly-runtime", "status": "passed", "result": runtime_result})
            except RuntimeError as exc:
                checks.append({"check": "namespaced-readonly-runtime", "status": "not-executed", "reason": str(exc)})
        else:
            checks.append({"check": "namespaced-readonly-runtime", "status": "not-executed", "reason": "required host privileges or commands unavailable"})

        # Generate the bounded successor handoff in the temporary proof tree.
        attachments = {
            "images": {
                name: {
                    "subjectDigest": product["index"].digest,
                    "sbomArtifactType": "application/vnd.cyclonedx+json",
                    "provenanceArtifactType": "application/vnd.in-toto+json",
                    "referrerCount": referrer_counts[name],
                }
                for name, product in products.items()
            },
            "signer": key_fingerprint(key.public_key()),
            "verificationPolicy": "atlas-workload-release-policy-1.0",
            "trustBoundary": "public deterministic course fixture; no production authority",
        }
        write_handoff(work / "handoff", release, attachments)
        if not (work / "handoff/MANIFEST.json").exists():
            raise AssertionError("Course 4 handoff was not generated")
        checks.append({"check": "course-4-handoff", "status": "passed"})

        supply_chain_report = {
            "images": {
                name: {
                    "subject": product["index"].digest,
                    "sbom": {
                        "mediaType": "application/vnd.cyclonedx+json",
                        "digest": sha256_digest(
                            canonical_json_bytes(evidence[name]["bom"])
                        ),
                        "profile": "CycloneDX 1.7 course fixture",
                    },
                    "provenanceEnvelope": {
                        "mediaType": "application/vnd.dsse.envelope.v1+json",
                        "digest": sha256_digest(
                            canonical_json_bytes(
                                evidence[name]["provenanceEnvelope"]
                            )
                        ),
                        "predicate": "https://slsa.dev/provenance/v1",
                    },
                    "policyDecision": evidence[name]["decision"],
                }
                for name, product in products.items()
            },
            "vulnerabilityDecision": {
                "findings": len(findings),
                "vexStatements": len(vex),
                "profile": (
                    "deterministic course database; not current public "
                    "vulnerability intelligence"
                ),
            },
            "signer": {
                "fingerprint": key_fingerprint(key.public_key()),
                "trust": "public deterministic course fixture; no production authority",
            },
            "policy": "atlas-workload-release-policy-1.0",
        }
        report = {
            "course": "03-container-oci-and-software-supply-chain-engineering",
            "release": release,
            "images": {
                "atlas-api": api_index.digest,
                "atlas-worker": worker_index.digest,
                "atlas-probe": probe_index.digest,
            },
            "sourceDigest": src_digest,
            "signerFingerprint": key_fingerprint(key.public_key()),
            "evidence": supply_chain_report,
            "checks": checks,
            "evidenceBoundary": {
                "controlledRebuild": (
                    "same source, compiler, environment, and semantic builder "
                    "implementation"
                ),
                "runtime": (
                    "root-managed bounded namespace/rootfs harness; not a fully "
                    "rootless runtime architecture, OCI conformance, or hostile "
                    "sandbox proof"
                ),
                "registry": (
                    "loopback instructional Distribution subset; not conformance, "
                    "authentication, retention, replication, or disaster-recovery proof"
                ),
                "supplyChain": (
                    "deterministic local fixture data and public fixture signer; "
                    "not operated builder or identity assurance"
                ),
                "capacity": "not measured",
            },
        }
    return report


def main() -> int:
    print(json.dumps(run_tour(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
