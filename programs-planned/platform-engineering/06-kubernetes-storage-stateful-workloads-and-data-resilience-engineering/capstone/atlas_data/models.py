from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class FailureDomain(str, Enum):
    PROCESS = "process"
    POD = "pod"
    NODE = "node"
    ZONE = "zone"
    REGION = "region"
    ACCOUNT = "account"


@dataclass(frozen=True)
class DataClass:
    name: str
    authoritative: bool
    maximum_loss: FailureDomain
    allowed_rpo_seconds: int
    allowed_rto_seconds: int
    writers: int

    def validate(self) -> None:
        if not self.name:
            raise ValueError("data class name is required")
        if self.allowed_rpo_seconds < 0 or self.allowed_rto_seconds <= 0:
            raise ValueError("invalid recovery objective")
        if self.authoritative and self.writers < 1:
            raise ValueError("authoritative data requires a writer")
        if self.writers < 0:
            raise ValueError("writer count cannot be negative")


@dataclass(frozen=True)
class StorageClass:
    name: str
    provisioner: str
    binding_mode: str = "WaitForFirstConsumer"
    reclaim_policy: str = "Retain"
    allow_expansion: bool = True
    allowed_zones: tuple[str, ...] = ()

    @classmethod
    def atlas_default(cls) -> "StorageClass":
        return cls(
            name="atlas-rwo-durable",
            provisioner="csi.atlas.example.invalid",
            binding_mode="WaitForFirstConsumer",
            reclaim_policy="Retain",
            allow_expansion=True,
            allowed_zones=("zone-a", "zone-b"),
        )

    def validate(self) -> None:
        if self.binding_mode not in {"Immediate", "WaitForFirstConsumer"}:
            raise ValueError("unsupported binding mode")
        if self.reclaim_policy not in {"Retain", "Delete"}:
            raise ValueError("unsupported reclaim policy")
        if not self.name or not self.provisioner:
            raise ValueError("class identity is required")


@dataclass
class Claim:
    namespace: str
    name: str
    requested_gib: int
    access_modes: tuple[str, ...]
    storage_class: str
    volume_mode: str = "Filesystem"
    selected_zone: str | None = None
    bound_volume: str | None = None
    phase: str = "Pending"

    @property
    def key(self) -> str:
        return f"{self.namespace}/{self.name}"

    def validate(self) -> None:
        if self.requested_gib <= 0:
            raise ValueError("claim capacity must be positive")
        if not self.access_modes:
            raise ValueError("claim needs an access mode")
        valid = {"ReadWriteOnce", "ReadWriteOncePod", "ReadOnlyMany", "ReadWriteMany"}
        if not set(self.access_modes).issubset(valid):
            raise ValueError("unsupported access mode")
        if self.volume_mode not in {"Filesystem", "Block"}:
            raise ValueError("unsupported volume mode")


@dataclass
class Volume:
    name: str
    handle: str
    capacity_gib: int
    access_modes: tuple[str, ...]
    storage_class: str
    zone: str
    reclaim_policy: str
    volume_mode: str = "Filesystem"
    claim_key: str | None = None
    phase: str = "Available"


@dataclass(frozen=True)
class Node:
    name: str
    zone: str
    attach_limit: int
    existing_attachments: int = 0


@dataclass(frozen=True)
class CapacitySegment:
    zone: str
    storage_class: str
    available_gib: int


@dataclass(frozen=True)
class PlacementDecision:
    node: str | None
    explanations: dict[str, list[str]]


@dataclass(frozen=True)
class BindingResult:
    claim: Claim
    volume: Volume
    created: bool
    transitions: tuple[str, ...]


@dataclass(frozen=True)
class StatefulIdentity:
    pod_name: str
    ordinal: int
    pvc_names: tuple[str, ...]
    dns_name: str


def ensure_unique(values: Iterable[str], label: str) -> None:
    values = list(values)
    if len(values) != len(set(values)):
        raise ValueError(f"duplicate {label}")
