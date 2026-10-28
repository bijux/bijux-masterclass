"""Release decision logic for schema and runtime evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .compatibility import CompatibilityDecision


@dataclass(frozen=True)
class ReleaseEvidence:
    compatibility: tuple[CompatibilityDecision, ...]
    active_operations_valid: bool
    budgets_pass: bool
    ownership_complete: bool
    old_client_passes: bool


@dataclass(frozen=True)
class ReleaseDecision:
    accepted: bool
    classification: str
    reasons: tuple[str, ...]


def decide(evidence: ReleaseEvidence) -> ReleaseDecision:
    """Apply non-compensable release gates in a stable order."""

    reasons: list[str] = []

    if any(
        item.classification == "breaking"
        for item in evidence.compatibility
    ):
        reasons.append("breaking-schema-change")
    if not evidence.active_operations_valid:
        reasons.append("active-operation-invalid")
    if not evidence.budgets_pass:
        reasons.append("query-budget-regression")
    if not evidence.ownership_complete:
        reasons.append("field-owner-missing")
    if not evidence.old_client_passes:
        reasons.append("old-client-failed")

    if reasons:
        return ReleaseDecision(
            accepted=False,
            classification="rejected",
            reasons=tuple(reasons),
        )

    if any(
        item.classification == "review-required"
        for item in evidence.compatibility
    ):
        return ReleaseDecision(
            accepted=False,
            classification="review-required",
            reasons=("manual-consumer-review-required",),
        )

    return ReleaseDecision(
        accepted=True,
        classification="accepted",
        reasons=(),
    )
