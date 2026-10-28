from __future__ import annotations

from dataclasses import dataclass
from math import prod
from .model import ValidationError


@dataclass(frozen=True)
class SyncEdge:
    source: str
    target: str
    purpose: str
    budget_ms: int


class DependencyGraph:
    def __init__(self, edges: list[SyncEdge] | None = None) -> None:
        self.edges = list(edges or [])

    def add(self, edge: SyncEdge) -> None:
        if edge.source == edge.target:
            raise ValidationError("self dependency is forbidden")
        if edge.budget_ms <= 0:
            raise ValidationError("edge budget must be positive")
        self.edges.append(edge)

    def adjacency(self) -> dict[str, list[str]]:
        graph: dict[str, list[str]] = {}
        for edge in self.edges:
            graph.setdefault(edge.source, []).append(edge.target)
            graph.setdefault(edge.target, [])
        return graph

    def cycle(self) -> list[str] | None:
        graph = self.adjacency()
        visiting: set[str] = set()
        visited: set[str] = set()
        stack: list[str] = []

        def visit(node: str) -> list[str] | None:
            if node in visiting:
                start = stack.index(node)
                return stack[start:] + [node]
            if node in visited:
                return None
            visiting.add(node)
            stack.append(node)
            for nxt in graph.get(node, []):
                found = visit(nxt)
                if found:
                    return found
            stack.pop()
            visiting.remove(node)
            visited.add(node)
            return None

        for node in graph:
            found = visit(node)
            if found:
                return found
        return None

    def longest_depth(self, root: str) -> int:
        if self.cycle():
            raise ValidationError("depth undefined for cyclic graph")
        graph = self.adjacency()
        memo: dict[str, int] = {}
        def depth(node: str) -> int:
            if node in memo:
                return memo[node]
            children = graph.get(node, [])
            memo[node] = 0 if not children else 1 + max(depth(x) for x in children)
            return memo[node]
        return depth(root)

    def validate(self, *, max_public_depth: int, forbidden: set[tuple[str, str]]) -> None:
        found = self.cycle()
        if found:
            raise ValidationError(f"synchronous cycle: {' -> '.join(found)}")
        for edge in self.edges:
            if (edge.source, edge.target) in forbidden:
                raise ValidationError(f"forbidden synchronous edge: {edge.source}->{edge.target}")
        if self.longest_depth("edge-gateway") > max_public_depth:
            raise ValidationError("public synchronous depth exceeds policy")


def serial_availability(probabilities: list[float]) -> float:
    if any(p < 0 or p > 1 for p in probabilities):
        raise ValidationError("availability must be within [0,1]")
    return prod(probabilities)


def serial_latency_ms(latencies: list[int]) -> int:
    if any(x < 0 for x in latencies):
        raise ValidationError("latency cannot be negative")
    return sum(latencies)


def parallel_latency_ms(latencies: list[int]) -> int:
    return max(latencies, default=0)
