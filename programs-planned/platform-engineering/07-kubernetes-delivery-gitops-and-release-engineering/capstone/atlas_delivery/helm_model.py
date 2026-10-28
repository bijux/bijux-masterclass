from __future__ import annotations

import copy
import re
from typing import Any


class ValuesError(ValueError):
    pass


def validate_values(schema: dict[str, Any], values: dict[str, Any], path: str = "$" ) -> None:
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(values, dict):
            raise ValuesError(f"{path}: expected object")
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in values:
                raise ValuesError(f"{path}: missing required value {required}")
        if schema.get("additionalProperties") is False:
            unknown = set(values) - set(properties)
            if unknown:
                raise ValuesError(f"{path}: unknown values {sorted(unknown)}")
        for key, value in values.items():
            if key in properties:
                validate_values(properties[key], value, f"{path}.{key}")
    elif expected == "string":
        if not isinstance(values, str):
            raise ValuesError(f"{path}: expected string")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], values):
            raise ValuesError(f"{path}: does not match {schema['pattern']}")
        if "enum" in schema and values not in schema["enum"]:
            raise ValuesError(f"{path}: not in enum")
    elif expected == "integer":
        if not isinstance(values, int) or isinstance(values, bool):
            raise ValuesError(f"{path}: expected integer")
        if "minimum" in schema and values < schema["minimum"]:
            raise ValuesError(f"{path}: below minimum")
        if "maximum" in schema and values > schema["maximum"]:
            raise ValuesError(f"{path}: above maximum")
    elif expected == "boolean":
        if not isinstance(values, bool):
            raise ValuesError(f"{path}: expected boolean")


def render_atlas(values: dict[str, Any]) -> list[dict[str, Any]]:
    image = values["image"]["repository"] + "@" + values["image"]["digest"]
    name = values.get("nameOverride", "atlas-api")
    namespace = values["namespace"]
    labels = {"app.kubernetes.io/name": "atlas", "app.kubernetes.io/component": "api"}
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace, "labels": copy.deepcopy(labels)},
        "spec": {
            "replicas": values["replicas"],
            "selector": {"matchLabels": copy.deepcopy(labels)},
            "template": {
                "metadata": {"labels": copy.deepcopy(labels)},
                "spec": {
                    "serviceAccountName": "atlas-api",
                    "securityContext": {"runAsNonRoot": True, "runAsUser": 65532, "runAsGroup": 65532},
                    "containers": [{
                        "name": "api",
                        "image": image,
                        "ports": [{"name": "http", "containerPort": 8080}],
                        "securityContext": {"allowPrivilegeEscalation": False, "readOnlyRootFilesystem": True, "capabilities": {"drop": ["ALL"]}},
                        "resources": values["resources"],
                        "readinessProbe": {"httpGet": {"path": "/ready", "port": "http"}},
                        "livenessProbe": {"httpGet": {"path": "/live", "port": "http"}},
                    }],
                },
            },
        },
    }
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": "atlas-api", "namespace": namespace},
        "spec": {"selector": labels, "ports": [{"name": "http", "port": 80, "targetPort": "http"}]},
    }
    return [deployment, service]
