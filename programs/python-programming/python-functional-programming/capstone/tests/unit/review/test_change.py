from __future__ import annotations

from funcpipe_rag.review.change import ChangeEvidence, review_change
from funcpipe_rag.review.evidence import (
    EvidenceAssessment,
    EvidenceClaim,
    assess_evidence,
)
from funcpipe_rag.review.migration import ContractShape, assess_migration
from funcpipe_rag.review.performance import BudgetDecision


def claim_assessment(*, complete: bool) -> EvidenceAssessment:
    claim = EvidenceClaim(
        name="ranking-order",
        statement="Ranking retains stable score ordering.",
        required_paths=("src/ranking.py", "tests/test_ranking.py"),
        command="pytest -q tests/test_ranking.py",
    )
    available = (
        frozenset(claim.required_paths)
        if complete
        else frozenset({"src/ranking.py"})
    )
    return assess_evidence(claim, available)


def test_review_change_accepts_complete_equivalent_evidence() -> None:
    decision = review_change(
        ChangeEvidence(
            semantic_equivalent=True,
            claims=(claim_assessment(complete=True),),
            budget=BudgetDecision(within_budget=True, violations=()),
        )
    )

    assert decision.acceptable is True
    assert decision.blockers == ()


def test_review_change_reports_independent_blockers_in_review_order() -> None:
    previous = ContractShape(
        "chunk-metadata",
        frozenset({"source"}),
        frozenset({"source"}),
    )
    current = ContractShape(
        "chunk-metadata",
        frozenset({"source", "language"}),
        frozenset({"source", "language"}),
    )

    decision = review_change(
        ChangeEvidence(
            semantic_equivalent=False,
            claims=(claim_assessment(complete=False),),
            budget=BudgetDecision(
                within_budget=False,
                violations=("peak_memory",),
            ),
            migration=assess_migration(previous, current),
        )
    )

    assert decision.acceptable is False
    assert decision.blockers == (
        "semantic-equivalence",
        "evidence:ranking-order",
        "performance:peak_memory",
        "migration:requires-migration",
    )


def test_review_change_does_not_require_irrelevant_checks() -> None:
    decision = review_change(
        ChangeEvidence(
            semantic_equivalent=True,
            claims=(claim_assessment(complete=True),),
        )
    )

    assert decision.acceptable is True
