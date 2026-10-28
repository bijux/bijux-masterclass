from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import re
import yaml

DIGEST_IMAGE = re.compile(r"^[^\s:@]+(?:/[^\s:@]+)*@sha256:[0-9a-f]{64}$")


def load_documents(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [doc for doc in yaml.safe_load_all(handle) if doc is not None]


def iter_pod_specs(doc: dict[str, Any]) -> Iterable[dict[str, Any]]:
    kind = doc.get("kind")
    spec = doc.get("spec", {})
    if kind == "Pod":
        yield spec
    elif kind in {"Deployment", "ReplicaSet", "DaemonSet", "StatefulSet", "Job"}:
        template = spec.get("template", {})
        if template:
            yield template.get("spec", {})
    elif kind == "CronJob":
        yield spec.get("jobTemplate", {}).get("spec", {}).get("template", {}).get("spec", {})


def validate_selector(doc: dict[str, Any]) -> list[str]:
    if doc.get("kind") not in {"Deployment", "ReplicaSet", "DaemonSet", "StatefulSet"}:
        return []
    spec = doc.get("spec", {})
    selector = spec.get("selector", {}).get("matchLabels", {})
    labels = spec.get("template", {}).get("metadata", {}).get("labels", {})
    return [f"selector label {k} does not match template" for k, v in selector.items()
            if labels.get(k) != v]


def validate_document(doc: dict[str, Any], *, allow_observation_images: bool = False) -> list[str]:
    errors: list[str] = []
    for key in ("apiVersion", "kind", "metadata"):
        if key not in doc:
            errors.append(f"missing {key}")
    errors.extend(validate_selector(doc))
    for pod_spec in iter_pod_specs(doc):
        if pod_spec.get("hostNetwork") is True:
            errors.append("hostNetwork is forbidden in Course 4 release")
        if pod_spec.get("hostPID") is True:
            errors.append("hostPID is forbidden in Course 4 release")
        for container in list(pod_spec.get("initContainers", [])) + list(pod_spec.get("containers", [])):
            image = str(container.get("image", ""))
            if image and not DIGEST_IMAGE.fullmatch(image):
                if not (allow_observation_images and image.startswith("registry.k8s.io/")):
                    errors.append(f"container {container.get('name')} image is not digest pinned")
            security = container.get("securityContext", {})
            if security.get("runAsNonRoot") is not True:
                errors.append(f"container {container.get('name')} must set runAsNonRoot")
            if security.get("allowPrivilegeEscalation") is not False:
                errors.append(f"container {container.get('name')} must disable privilege escalation")
            if security.get("readOnlyRootFilesystem") is not True:
                errors.append(f"container {container.get('name')} must use read-only root filesystem")
            drops = security.get("capabilities", {}).get("drop", [])
            if "ALL" not in drops:
                errors.append(f"container {container.get('name')} must drop ALL capabilities")
            if "resources" not in container:
                errors.append(f"container {container.get('name')} must declare resources")
    return errors


def validate_tree(root: Path, *, allow_observation_images: bool = False) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.rglob("*.yaml")):
        for index, doc in enumerate(load_documents(path), start=1):
            for error in validate_document(doc, allow_observation_images=allow_observation_images):
                findings.append(f"{path}:{index}: {error}")
    return findings
