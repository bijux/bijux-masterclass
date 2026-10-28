from __future__ import annotations

from dataclasses import dataclass

from .models import DesiredRevision, EvidenceGate


@dataclass(frozen=True)
class PromotionResult:
    accepted: bool
    reason: str


def evaluate_promotion(source: DesiredRevision, target: DesiredRevision, gates: list[EvidenceGate]) -> PromotionResult:
    if source.artifacts != target.artifacts:
        return PromotionResult(False, "promotion changed immutable artifact identities")
    blockers = [gate for gate in gates if gate.blocker and gate.status != "pass"]
    if blockers:
        return PromotionResult(False, "; ".join(f"{g.name}:{g.status}" for g in blockers))
    if target.predecessor is None:
        return PromotionResult(False, "target release lacks predecessor lineage")
    return PromotionResult(True, "same artifacts and all blocker gates passed")
