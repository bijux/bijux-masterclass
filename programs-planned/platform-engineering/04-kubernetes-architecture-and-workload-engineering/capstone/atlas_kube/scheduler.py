from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Taint:
    key: str
    value: str
    effect: str = "NoSchedule"


@dataclass(frozen=True, slots=True)
class Toleration:
    key: str
    value: str
    effect: str = "NoSchedule"


@dataclass(slots=True)
class Node:
    name: str
    cpu_m: int
    memory_mib: int
    labels: dict[str, str]
    taints: list[Taint] = field(default_factory=list)
    allocated_cpu_m: int = 0
    allocated_memory_mib: int = 0


@dataclass(slots=True)
class PodRequest:
    name: str
    cpu_m: int
    memory_mib: int
    required_labels: dict[str, str] = field(default_factory=dict)
    tolerations: list[Toleration] = field(default_factory=list)
    prohibited_hostnames: set[str] = field(default_factory=set)
    topology_key: str | None = None
    occupied_domains: dict[str, int] = field(default_factory=dict)
    max_skew: int = 1


@dataclass(frozen=True, slots=True)
class NodeDecision:
    node: str
    feasible: bool
    reasons: tuple[str, ...]


def _tolerated(taint: Taint, tolerations: Iterable[Toleration]) -> bool:
    return any(
        t.key == taint.key and t.value == taint.value and t.effect == taint.effect
        for t in tolerations
    )


def evaluate_node(node: Node, pod: PodRequest) -> NodeDecision:
    reasons: list[str] = []
    if node.cpu_m - node.allocated_cpu_m < pod.cpu_m:
        reasons.append("InsufficientCPU")
    if node.memory_mib - node.allocated_memory_mib < pod.memory_mib:
        reasons.append("InsufficientMemory")
    for key, value in pod.required_labels.items():
        if node.labels.get(key) != value:
            reasons.append(f"LabelMismatch:{key}")
    for taint in node.taints:
        if taint.effect in {"NoSchedule", "NoExecute"} and not _tolerated(taint, pod.tolerations):
            reasons.append(f"UntoleratedTaint:{taint.key}")
    if node.name in pod.prohibited_hostnames:
        reasons.append("PodAntiAffinity")
    if pod.topology_key:
        domain = node.labels.get(pod.topology_key)
        if domain is None:
            reasons.append(f"MissingTopologyLabel:{pod.topology_key}")
        elif pod.occupied_domains:
            prospective = dict(pod.occupied_domains)
            prospective[domain] = prospective.get(domain, 0) + 1
            values = list(prospective.values())
            if max(values) - min(values) > pod.max_skew:
                reasons.append("TopologySkew")
    return NodeDecision(node.name, not reasons, tuple(sorted(set(reasons))))


def schedule(nodes: Iterable[Node], pod: PodRequest) -> tuple[str | None, list[NodeDecision]]:
    decisions = [evaluate_node(node, pod) for node in nodes]
    feasible = [d.node for d in decisions if d.feasible]
    return (sorted(feasible)[0] if feasible else None), decisions
