from __future__ import annotations

from .models import CapacitySegment, Node, PlacementDecision


class Scheduler:
    def __init__(self, nodes: list[Node], capacities: list[CapacitySegment]):
        self.nodes = nodes
        self.capacities = capacities

    def _capacity(self, zone: str, storage_class: str) -> int:
        return sum(
            item.available_gib
            for item in self.capacities
            if item.zone == zone and item.storage_class == storage_class
        )

    def place(
        self,
        pod: str,
        claims: list[tuple[str, int]],
        storage_class: str = "atlas-rwo-durable",
        required_zones: set[str] | None = None,
    ) -> PlacementDecision:
        explanations: dict[str, list[str]] = {}
        for node in self.nodes:
            failures: list[str] = []
            if required_zones and node.zone not in required_zones:
                failures.append("node zone is not permitted")
            if node.existing_attachments + len(claims) > node.attach_limit:
                failures.append("volume attachment limit exceeded")
            requested = sum(size for _, size in claims)
            if self._capacity(node.zone, storage_class) < requested:
                failures.append("insufficient accessible storage capacity")
            explanations[node.name] = failures
            if not failures:
                return PlacementDecision(node=node.name, explanations=explanations)
        return PlacementDecision(node=None, explanations=explanations)
