from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseDecision:
    decision: str
    blockers: tuple[str, ...]
    reviews: tuple[str, ...]


class ReleaseEvaluator:
    required = (
        "predecessor",
        "single_writer",
        "restore_drill",
        "migration_compatibility",
    )

    def evaluate(self, evidence: dict[str, str]) -> ReleaseDecision:
        blockers = tuple(name for name in self.required if evidence.get(name) != "pass")
        if blockers:
            return ReleaseDecision("rejected", blockers, ())
        reviews = tuple(name for name, state in evidence.items() if state in {"review", "not-executed"})
        if reviews:
            return ReleaseDecision("review-required", (), reviews)
        return ReleaseDecision("accepted", (), ())
