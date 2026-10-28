from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from .canonical import load_yaml_documents, resource_identity, validate_unique_identities

CLUSTER_SCOPED = {
    "ClusterRole",
    "ClusterRoleBinding",
    "CustomResourceDefinition",
    "GatewayClass",
    "Namespace",
    "Node",
    "PersistentVolume",
    "StorageClass",
    "VolumeSnapshotClass",
    "VolumeGroupSnapshotClass",
}


def _deep_merge(target: Any, patch: Any) -> Any:
    if isinstance(target, dict) and isinstance(patch, dict):
        result = copy.deepcopy(target)
        for key, value in patch.items():
            if key in result:
                result[key] = _deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)
        return result
    if isinstance(target, list) and isinstance(patch, list):
        if all(isinstance(item, dict) and "name" in item for item in target + patch):
            result = copy.deepcopy(target)
            positions = {item["name"]: index for index, item in enumerate(result)}
            for item in patch:
                if item["name"] in positions:
                    index = positions[item["name"]]
                    result[index] = _deep_merge(result[index], item)
                else:
                    positions[item["name"]] = len(result)
                    result.append(copy.deepcopy(item))
            return result
        return copy.deepcopy(patch)
    return copy.deepcopy(patch)


def _set_namespace(resource: dict[str, Any], namespace: str) -> None:
    if resource.get("kind") in CLUSTER_SCOPED:
        return
    resource.setdefault("metadata", {})["namespace"] = namespace


def _apply_labels(resource: dict[str, Any], labels: dict[str, str], include_selectors: bool) -> None:
    metadata = resource.setdefault("metadata", {})
    metadata.setdefault("labels", {}).update(labels)
    template = resource.get("spec", {}).get("template")
    if isinstance(template, dict):
        template.setdefault("metadata", {}).setdefault("labels", {}).update(labels)
    if include_selectors and resource.get("kind") in {"Deployment", "StatefulSet", "DaemonSet"}:
        resource.setdefault("spec", {}).setdefault("selector", {}).setdefault("matchLabels", {}).update(labels)


def _replace_image(resource: dict[str, Any], image_name: str, replacement: str) -> None:
    pod_specs: list[dict[str, Any]] = []
    spec = resource.get("spec", {})
    if resource.get("kind") == "Pod":
        pod_specs.append(spec)
    template = spec.get("template")
    if isinstance(template, dict) and isinstance(template.get("spec"), dict):
        pod_specs.append(template["spec"])
    job_template = spec.get("jobTemplate", {}).get("spec", {}).get("template", {})
    if isinstance(job_template, dict) and isinstance(job_template.get("spec"), dict):
        pod_specs.append(job_template["spec"])
    for pod_spec in pod_specs:
        for key in ("initContainers", "containers"):
            for container in pod_spec.get(key, []) or []:
                current = str(container.get("image", ""))
                base = current.split("@", 1)[0].split(":", 1)[0]
                if base == image_name:
                    container["image"] = replacement



def _walk_replace_name_references(value: Any, mapping: dict[str, str], key: str | None = None) -> Any:
    """Apply a bounded subset of Kustomize name-reference behavior.

    This semantic lane intentionally supports only the reference fields used by the
    Atlas fixtures. Native Kustomize remains the authority for the complete field
    specification.
    """
    reference_keys = {
        "serviceAccountName", "configMapName", "secretName", "claimName",
        "name",  # guarded below by parent-shape conventions in the fixture lane
    }
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for child_key, child in value.items():
            if child_key in {"serviceAccountName", "configMapName", "secretName", "claimName"} and isinstance(child, str):
                result[child_key] = mapping.get(child, child)
            elif child_key == "name" and isinstance(child, str) and key in {
                "configMapRef", "secretKeyRef", "secretRef", "service", "backendRef", "scaleTargetRef"
            }:
                result[child_key] = mapping.get(child, child)
            else:
                result[child_key] = _walk_replace_name_references(child, mapping, child_key)
        return result
    if isinstance(value, list):
        return [_walk_replace_name_references(item, mapping, key) for item in value]
    return value


def _apply_name_affixes(resources: list[dict[str, Any]], prefix: str, suffix: str) -> list[dict[str, Any]]:
    if not prefix and not suffix:
        return resources
    mapping: dict[str, str] = {}
    for resource in resources:
        metadata = resource.setdefault("metadata", {})
        old = str(metadata.get("name", ""))
        if old:
            mapping[old] = f"{prefix}{old}{suffix}"
    output: list[dict[str, Any]] = []
    for resource in resources:
        transformed = _walk_replace_name_references(resource, mapping)
        metadata = transformed.setdefault("metadata", {})
        old = str(resource.get("metadata", {}).get("name", ""))
        if old:
            metadata["name"] = mapping[old]
        output.append(transformed)
    return output

def build(directory: str | Path) -> list[dict[str, Any]]:
    root = Path(directory)
    kfile = root / "kustomization.yaml"
    config = yaml.safe_load(kfile.read_text(encoding="utf-8")) or {}
    resources: list[dict[str, Any]] = []
    for entry in config.get("resources", []) or []:
        path = (root / entry).resolve()
        if path.is_dir():
            resources.extend(build(path))
        else:
            resources.extend(load_yaml_documents(path))

    namespace = config.get("namespace")
    if namespace:
        for resource in resources:
            _set_namespace(resource, str(namespace))

    for label_rule in config.get("labels", []) or []:
        pairs = label_rule.get("pairs", {})
        include = bool(label_rule.get("includeSelectors", False))
        for resource in resources:
            _apply_labels(resource, pairs, include)

    for replica in config.get("replicas", []) or []:
        name = replica["name"]
        count = int(replica["count"])
        for resource in resources:
            if resource.get("kind") in {"Deployment", "StatefulSet"} and resource.get("metadata", {}).get("name") == name:
                resource.setdefault("spec", {})["replicas"] = count

    for image in config.get("images", []) or []:
        name = image["name"]
        new_name = image.get("newName", name)
        if image.get("digest"):
            replacement = f"{new_name}@{image['digest']}"
        elif image.get("newTag"):
            replacement = f"{new_name}:{image['newTag']}"
        else:
            replacement = new_name
        for resource in resources:
            _replace_image(resource, name, replacement)

    for patch_entry in config.get("patches", []) or []:
        patch_path = patch_entry["path"] if isinstance(patch_entry, dict) else patch_entry
        for patch in load_yaml_documents(root / patch_path):
            target_identity = resource_identity(patch)
            target_group, target_kind, target_namespace, target_name = target_identity
            for index, resource in enumerate(resources):
                group, kind, namespace, name = resource_identity(resource)
                namespace_matches = not target_namespace or namespace == target_namespace
                if (group, kind, name) == (target_group, target_kind, target_name) and namespace_matches:
                    resources[index] = _deep_merge(resource, patch)
                    break
            else:
                raise ValueError(f"patch target not found: {target_identity}")

    resources = _apply_name_affixes(
        resources, str(config.get("namePrefix", "")), str(config.get("nameSuffix", ""))
    )
    validate_unique_identities(resources)
    return resources
