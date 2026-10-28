from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Route:
    """One route candidate in a named routing table."""

    prefix: str
    next_hop: str | None
    interface: str
    metric: int = 100
    table: int = 254


@dataclass(frozen=True, slots=True)
class Endpoint:
    """A backend endpoint as published through an EndpointSlice."""

    address: str
    port: int
    pod: str
    node: str
    zone: str
    ready: bool = True
    serving: bool = True
    terminating: bool = False
    family: str = "IPv4"


@dataclass(frozen=True, slots=True)
class Service:
    """The subset of Service fields used by the semantic data plane."""

    name: str
    namespace: str
    port: int
    target_port: int
    cluster_ips: tuple[str, ...]
    internal_traffic_policy: str = "Cluster"
    external_traffic_policy: str = "Cluster"
    session_affinity: str = "None"


@dataclass(frozen=True, slots=True)
class Packet:
    """A packet-flow identity used by policy and routing exercises."""

    source_ip: str
    destination_ip: str
    protocol: str
    destination_port: int
    source_namespace: str = "atlas-system"
    source_pod: str = "client"
    source_node: str = "node-a"
    source_zone: str = "zone-a"


@dataclass(frozen=True, slots=True)
class PolicyPeer:
    namespaces: frozenset[str] | None = None
    pods: frozenset[str] | None = None
    cidrs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PolicyRule:
    peers: tuple[PolicyPeer, ...]
    ports: tuple[tuple[str, int], ...]


@dataclass(frozen=True, slots=True)
class NetworkPolicy:
    name: str
    namespace: str
    selected_pods: frozenset[str]
    policy_types: frozenset[str]
    ingress: tuple[PolicyRule, ...] = ()
    egress: tuple[PolicyRule, ...] = ()


@dataclass(frozen=True, slots=True)
class Certificate:
    name: str
    dns_names: tuple[str, ...]
    issuer: str
    not_before: int
    not_after: int


@dataclass(frozen=True, slots=True)
class Listener:
    name: str
    hostname: str
    port: int
    protocol: str
    certificate: str | None
    allowed_namespaces: frozenset[str]


@dataclass(frozen=True, slots=True)
class HttpMatch:
    path_type: str = "PathPrefix"
    path: str = "/"
    method: str | None = None
    headers: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class HttpRoute:
    name: str
    namespace: str
    parent_gateway: str
    listener: str
    hostnames: tuple[str, ...]
    matches: tuple[HttpMatch, ...]
    backend_namespace: str
    backend_service: str
    backend_port: int
    generation: int = 1


@dataclass(frozen=True, slots=True)
class ReferenceGrant:
    namespace: str
    from_namespaces: frozenset[str]
    from_kinds: frozenset[str]
    to_kinds: frozenset[str]


@dataclass(slots=True)
class Decision:
    allowed: bool
    reason: str
    details: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class TraceLedger:
    """Ordered transition evidence with an explicit first failure."""

    transitions: list[dict[str, object]] = field(default_factory=list)

    def add(self, name: str, ok: bool, owner: str, evidence: object) -> None:
        self.transitions.append(
            {
                "transition": name,
                "ok": ok,
                "owner": owner,
                "evidence": evidence,
            }
        )

    @property
    def first_failure(self) -> dict[str, object] | None:
        return next(
            (transition for transition in self.transitions if not transition["ok"]),
            None,
        )
