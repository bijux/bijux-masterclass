from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import copy
import uuid


def now_rfc3339() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class Condition:
    type: str
    status: str
    reason: str
    message: str
    observed_generation: int
    last_transition_time: str = field(default_factory=now_rfc3339)

    def semantic_key(self) -> tuple[str, str, str, str, int]:
        return (
            self.type,
            self.status,
            self.reason,
            self.message,
            self.observed_generation,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "status": self.status,
            "reason": self.reason,
            "message": self.message,
            "observedGeneration": self.observed_generation,
            "lastTransitionTime": self.last_transition_time,
        }


@dataclass(slots=True)
class ObjectMeta:
    name: str
    namespace: str = "default"
    uid: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_version: int = 0
    generation: int = 1
    labels: dict[str, str] = field(default_factory=dict)
    annotations: dict[str, str] = field(default_factory=dict)
    owner_references: list[dict[str, Any]] = field(default_factory=list)
    finalizers: list[str] = field(default_factory=list)
    deletion_timestamp: str | None = None
    managed_fields: dict[str, set[str]] = field(default_factory=dict)

    def key(self, api_version: str, kind: str) -> tuple[str, str, str, str]:
        return api_version, kind, self.namespace, self.name

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "name": self.name,
            "namespace": self.namespace,
            "uid": self.uid,
            "resourceVersion": str(self.resource_version),
            "generation": self.generation,
            "labels": copy.deepcopy(self.labels),
            "annotations": copy.deepcopy(self.annotations),
            "ownerReferences": copy.deepcopy(self.owner_references),
            "finalizers": list(self.finalizers),
            "managedFields": [
                {"manager": manager, "fields": sorted(fields)}
                for manager, fields in sorted(self.managed_fields.items())
            ],
        }
        if self.deletion_timestamp is not None:
            data["deletionTimestamp"] = self.deletion_timestamp
        return data


@dataclass(slots=True)
class KubeObject:
    api_version: str
    kind: str
    metadata: ObjectMeta
    spec: dict[str, Any] = field(default_factory=dict)
    status: dict[str, Any] = field(default_factory=dict)

    @property
    def key(self) -> tuple[str, str, str, str]:
        return self.metadata.key(self.api_version, self.kind)

    def clone(self) -> "KubeObject":
        return copy.deepcopy(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": self.metadata.to_dict(),
            "spec": copy.deepcopy(self.spec),
            "status": copy.deepcopy(self.status),
        }


def semantic_status_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Compare status while ignoring transition timestamps for unchanged conditions."""
    def normalize(value: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(value)
        for condition in out.get("conditions", []):
            condition.pop("lastTransitionTime", None)
        return out
    return normalize(left) == normalize(right)
