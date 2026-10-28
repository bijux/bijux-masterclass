from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import yaml


class DuplicateKeyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def load_yaml_documents(path: str | Path) -> list[dict[str, Any]]:
    source = Path(path)
    documents = list(yaml.load_all(source.read_text(encoding="utf-8"), Loader=UniqueKeyLoader))
    result: list[dict[str, Any]] = []
    for document in documents:
        if document is None:
            continue
        if not isinstance(document, dict):
            raise ValueError(f"{source}: Kubernetes document must be a mapping")
        result.append(document)
    return result


def api_group(api_version: str) -> str:
    return api_version.split("/", 1)[0] if "/" in api_version else ""


def resource_identity(resource: dict[str, Any]) -> tuple[str, str, str, str]:
    metadata = resource.get("metadata") or {}
    return (
        api_group(str(resource.get("apiVersion", ""))),
        str(resource.get("kind", "")),
        str(metadata.get("namespace", "")),
        str(metadata.get("name", "")),
    )


def identity_string(resource: dict[str, Any]) -> str:
    group, kind, namespace, name = resource_identity(resource)
    return f"{group or 'core'}/{kind}/{namespace or '_cluster'}/{name}"


SERVER_METADATA = {
    "creationTimestamp",
    "deletionGracePeriodSeconds",
    "deletionTimestamp",
    "generation",
    "managedFields",
    "resourceVersion",
    "selfLink",
    "uid",
}


def desired_resource(resource: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(resource)
    value.pop("status", None)
    metadata = value.get("metadata")
    if isinstance(metadata, dict):
        for key in SERVER_METADATA:
            metadata.pop(key, None)
        annotations = metadata.get("annotations")
        if isinstance(annotations, dict):
            annotations.pop("kubectl.kubernetes.io/last-applied-configuration", None)
            if not annotations:
                metadata.pop("annotations", None)
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_resource(resource: dict[str, Any]) -> bytes:
    return canonical_bytes(desired_resource(resource))


def validate_unique_identities(resources: Iterable[dict[str, Any]]) -> None:
    seen: set[tuple[str, str, str, str]] = set()
    for resource in resources:
        identity = resource_identity(resource)
        if not all((identity[1], identity[3])):
            raise ValueError(f"incomplete Kubernetes identity: {identity}")
        if identity in seen:
            raise ValueError(f"duplicate Kubernetes identity: {identity}")
        seen.add(identity)


def canonical_set(resources: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    values = [desired_resource(resource) for resource in resources]
    validate_unique_identities(values)
    return sorted(values, key=resource_identity)


def render_digest(resources: Iterable[dict[str, Any]]) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(canonical_set(resources))).hexdigest()
