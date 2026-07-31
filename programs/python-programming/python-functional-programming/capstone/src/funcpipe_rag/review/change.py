"""Pure acceptance decision for a proposed FuncPipe change."""

from __future__ import annotations

from dataclasses import dataclass

from .evidence import EvidenceAssessment
from .migration import MigrationAssessment
from .performance import BudgetDecision


@dataclass(frozen=True, slots=True)
class ChangeEvidence:
    """Already-observed facts needed to review one application change."""

    semantic_equivalent: bool
    claims: tuple[EvidenceAssessment, ...]
    budget: BudgetDecision | None = None
    migration: MigrationAssessment | None = None


@dataclass(frozen=True, slots=True)
class ChangeDecision:
    """Deterministic result of applying the sustainment rules."""

    acceptable: bool
    blockers: tuple[str, ...]


def review_change(evidence: ChangeEvidence) -> ChangeDecision:
    """Compose independent proof results without performing their effects."""

    blockers: list[str] = []
    if not evidence.semantic_equivalent:
        blockers.append("semantic-equivalence")

    blockers.extend(
        f"evidence:{assessment.claim.name}"
        for assessment in evidence.claims
        if not assessment.complete
    )

    if evidence.budget is not None:
        blockers.extend(
            f"performance:{violation}" for violation in evidence.budget.violations
        )

    if (
        evidence.migration is not None
        and evidence.migration.compatibility != "backward-compatible"
    ):
        blockers.append(f"migration:{evidence.migration.compatibility}")

    return ChangeDecision(acceptable=not blockers, blockers=tuple(blockers))
