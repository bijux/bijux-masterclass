from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .canonical import identity_string


DEFAULT_PROTECTED_KINDS = {
    "PersistentVolume",
    "PersistentVolumeClaim",
    "VolumeSnapshotContent",
    "VolumeGroupSnapshotContent",
}


@dataclass
class Inventory:
    application: str
    identities: set[str] = field(default_factory=set)

    @classmethod
    def from_resources(cls, application: str, resources: Iterable[dict]) -> "Inventory":
        return cls(application=application, identities={identity_string(r) for r in resources})


def is_protected(resource: dict, protected_kinds: set[str] | None = None) -> bool:
    kinds = protected_kinds or DEFAULT_PROTECTED_KINDS
    if resource.get("kind") in kinds:
        return True
    annotations = resource.get("metadata", {}).get("annotations", {}) or {}
    return str(annotations.get("delivery.atlas.dev/prune-protected", "false")).lower() == "true"
