from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .models import Decision, Endpoint, Service


@dataclass(slots=True)
class ProgrammedService:
    """Desired EndpointSlice generations versus per-node programmed state."""

    desired_generation: int
    programmed_by_node: dict[str, int]
    endpoints_by_generation: dict[int, tuple[Endpoint, ...]]

    def endpoints_for_node(self, node: str) -> tuple[Endpoint, ...]:
        generation = self.programmed_by_node[node]
        return self.endpoints_by_generation[generation]

    def program(self, node: str, generation: int) -> None:
        if generation not in self.endpoints_by_generation:
            raise ValueError("unknown endpoint generation")
        self.programmed_by_node[node] = generation


def eligible(
    endpoints: tuple[Endpoint, ...],
    family: str | None = None,
) -> list[Endpoint]:
    return [
        endpoint
        for endpoint in endpoints
        if endpoint.ready
        and endpoint.serving
        and (family is None or endpoint.family == family)
    ]


def select_backend(
    service: Service,
    endpoints: tuple[Endpoint, ...],
    *,
    client_node: str,
    client_zone: str,
    client_key: str,
    family: str,
    topology_preference: bool = False,
) -> Decision:
    candidates = eligible(endpoints, family)

    if service.internal_traffic_policy == "Local":
        candidates = [
            endpoint for endpoint in candidates if endpoint.node == client_node
        ]
        if not candidates:
            return Decision(
                False,
                "NoLocalEndpoints",
                {"node": client_node, "family": family},
            )
    elif topology_preference:
        local = [
            endpoint for endpoint in candidates if endpoint.zone == client_zone
        ]
        if local:
            candidates = local

    if not candidates:
        return Decision(False, "NoEligibleEndpoints", {"family": family})

    ordered = sorted(
        candidates,
        key=lambda endpoint: (
            endpoint.zone,
            endpoint.node,
            endpoint.pod,
            endpoint.address,
            endpoint.port,
        ),
    )
    digest = int.from_bytes(sha256(client_key.encode("utf-8")).digest()[:8], "big")
    endpoint = ordered[digest % len(ordered)]
    return Decision(
        True,
        "Selected",
        {"endpoint": endpoint, "population": len(ordered)},
    )
