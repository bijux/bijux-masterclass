from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoundaryCandidate:
    name: str
    ownership: int
    data_autonomy: int
    change_independence: int
    scale_isolation: int
    failure_isolation: int
    security_boundary: int
    operational_cost: int
    synchronous_coupling: int

    def weighted_score(self) -> int:
        return (
            3 * self.ownership
            + 3 * self.data_autonomy
            + 2 * self.change_independence
            + 2 * self.scale_isolation
            + 2 * self.failure_isolation
            + 2 * self.security_boundary
            - 3 * self.operational_cost
            - 3 * self.synchronous_coupling
        )


def decision(candidate: BoundaryCandidate) -> str:
    score = candidate.weighted_score()
    if candidate.data_autonomy <= 0:
        return "reject"
    if score >= 14:
        return "extract"
    if score >= 8:
        return "conditional"
    return "keep-together"


def explain(candidate: BoundaryCandidate) -> dict[str, object]:
    return {
        "name": candidate.name,
        "score": candidate.weighted_score(),
        "decision": decision(candidate),
        "reversal_required": decision(candidate) != "extract",
    }
