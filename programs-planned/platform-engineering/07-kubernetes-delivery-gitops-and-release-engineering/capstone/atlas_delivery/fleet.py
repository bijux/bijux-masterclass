from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClusterProfile:
    cluster_id: str
    owner: str
    environment: str
    region: str
    topology_class: str
    kubernetes: str
    gitops_controller: str
    capabilities: frozenset[str]
    lifecycle: str = "active"


@dataclass(frozen=True)
class ReleaseRequirements:
    minimum_kubernetes_minor: int
    required_capabilities: frozenset[str]
    controller_prefix: str


def compatible(cluster: ClusterProfile, requirements: ReleaseRequirements) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    try:
        minor = int(cluster.kubernetes.split(".")[1])
    except (IndexError, ValueError):
        reasons.append("invalid Kubernetes version")
        minor = -1
    if minor < requirements.minimum_kubernetes_minor:
        reasons.append("Kubernetes version below minimum")
    missing = requirements.required_capabilities - cluster.capabilities
    if missing:
        reasons.append(f"missing capabilities: {sorted(missing)}")
    if not cluster.gitops_controller.startswith(requirements.controller_prefix):
        reasons.append("unsupported GitOps controller profile")
    return not reasons, reasons


def generate_targets(catalogue: list[ClusterProfile], environment: str, source_available: bool = True) -> list[str] | None:
    if not source_available:
        return None
    return sorted(c.cluster_id for c in catalogue if c.lifecycle == "active" and c.environment == environment)


def promotion_waves(catalogue: list[ClusterProfile]) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for cluster in catalogue:
        groups.setdefault(cluster.topology_class, []).append(cluster.cluster_id)
    waves: list[list[str]] = []
    for topology in sorted(groups):
        ids = sorted(groups[topology])
        waves.append(ids[:1])
    remaining = sorted({c.cluster_id for c in catalogue} - {x for wave in waves for x in wave})
    if remaining:
        waves.append(remaining)
    return waves
