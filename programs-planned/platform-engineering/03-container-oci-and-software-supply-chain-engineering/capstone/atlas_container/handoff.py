from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def write_handoff(
    destination: Path,
    release: dict[str, Any],
    attachments: dict[str, Any],
) -> None:
    """Write the exact bounded Course 3 → Course 4 interface."""

    destination.mkdir(parents=True, exist_ok=True)
    for existing in destination.iterdir():
        if existing.is_file():
            existing.unlink()

    images = release.get("images")
    if not isinstance(images, list) or not images:
        images = [
            {
                "name": "atlas-api",
                "repository": release["repository"],
                "digest": release["imageDigest"],
                "platforms": release["platforms"],
                "runtimeUser": "65532:65532",
                "entrypoint": ["/usr/local/bin/atlas-api"],
            }
        ]
        for name, digest in sorted(release.get("additionalImages", {}).items()):
            images.append(
                {
                    "name": name,
                    "repository": f"platform/{name}",
                    "digest": digest,
                    "platforms": release["platforms"],
                    "runtimeUser": "65532:65532",
                    "entrypoint": [f"/usr/local/bin/{name}"],
                }
            )

    files: dict[str, Any] = {
        "README.md": """# Course 3 → Course 4 Handoff

This directory is the bounded workload handoff to Kubernetes Architecture and Workload Engineering. Kubernetes may schedule and reconcile Atlas, but it may not weaken the image, identity, storage, health, termination, or verification contracts recorded here.
""",
        "version-ledger.json": {
            "course1HostRuntime": "1.0.0",
            "course2CloudFoundation": "1.0.0",
            "course3WorkloadRelease": "1.0.0",
            "course4Target": "kubernetes-workload-1.0.0",
        },
        "image-release.json": {
            "release": release.get("release", "atlas-workload-release-1.0.0"),
            "sourceDigest": release.get("sourceDigest"),
            "discoveryTag": release.get("tag"),
            "deploymentIdentity": "repository plus immutable digest",
            "images": images,
            "verificationImages": release.get("verificationImages", []),
        },
        "workload-contract.json": {
            "containers": [
                {
                    "name": "atlas-api",
                    "port": 8080,
                    "user": "65532:65532",
                    "terminationGraceSeconds": 30,
                    "image": next(
                        (
                            f"{item['repository']}@{item['digest']}"
                            for item in images
                            if item.get("name") == "atlas-api"
                        ),
                        None,
                    ),
                },
                {
                    "name": "atlas-worker",
                    "port": None,
                    "user": "65532:65532",
                    "terminationGraceSeconds": 30,
                    "image": next(
                        (
                            f"{item['repository']}@{item['digest']}"
                            for item in images
                            if item.get("name") == "atlas-worker"
                        ),
                        None,
                    ),
                },
            ],
            "health": {
                "liveness": "/live",
                "readiness": "/ready",
                "worker": "fresh heartbeat plus durable queue access",
            },
            "rootFilesystem": "read-only",
            "capabilities": [],
            "noNewPrivileges": True,
        },
        "storage-contract.json": {
            "durable": ["/var/lib/atlas/spool", "/var/lib/atlas/results"],
            "ephemeral": ["/tmp", "/run/atlas"],
            "configuration": ["/etc/atlas"],
            "imageFilesystemIsDurable": False,
        },
        "configuration-contract.json": {
            "nonSecret": "environment or projected configuration",
            "secret": "runtime secret source; never image layer or manifest annotation",
            "cloudIdentity": "short-lived workload identity",
        },
        "resource-hypotheses.json": {
            "cpu": {
                "request": "100m",
                "limit": "500m",
                "evidence": "course-lab-hypothesis",
            },
            "memory": {
                "request": "64Mi",
                "limit": "128Mi",
                "evidence": "course-lab-hypothesis",
            },
            "pids": 64,
            "capacityClaim": "not production evidence",
        },
        "supply-chain-contract.json": attachments,
        "known-risks.json": {
            "risks": [
                "the checked mini-runtime is root-managed and is not proof of a fully rootless runtime architecture",
                "runtime default seccomp behavior remains platform dependent",
                "resource values require Course 4 and later representative measurement",
                "registry availability, authentication, retention, replication, and credential rotation remain environment-backed",
                "multi-platform indexes do not prove every target kernel or CPU feature",
                "fixture signing keys are public course material and provide no production trust",
            ]
        },
    }

    manifest_entries = []
    for name, value in files.items():
        path = destination / name
        data = value.encode() if isinstance(value, str) else _json_bytes(value)
        path.write_bytes(data)
        manifest_entries.append(
            {
                "path": name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    manifest = {
        "schemaVersion": "1.0",
        "files": sorted(manifest_entries, key=lambda item: item["path"]),
    }
    (destination / "MANIFEST.json").write_bytes(_json_bytes(manifest))
