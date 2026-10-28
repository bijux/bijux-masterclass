from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .evolution import compare_object_schemas


@dataclass(frozen=True, slots=True)
class ReleaseDecision:
    status: str
    reasons: tuple[str, ...]


def evaluate_event_release(
    old_schema: dict[str, Any],
    new_schema: dict[str, Any],
    *,
    replay_safe: bool,
    catalog_complete: bool,
    contract_valid: bool,
    security_valid: bool = True,
    reliability_ready: bool = True,
) -> ReleaseDecision:
    reasons: list[str] = []
    if not contract_valid:
        reasons.append("AsyncAPI contract is invalid")
    report = compare_object_schemas(old_schema, new_schema)
    reasons.extend(
        f"{issue.severity}: {issue.path}: {issue.message}"
        for issue in report.issues
    )
    if not replay_safe:
        reasons.append("candidate is not replay safe")
    if not catalog_complete:
        reasons.append("event catalogue is incomplete")
    if not security_valid:
        reasons.append("event security policy is not satisfied")
    if not reliability_ready:
        reasons.append("consumer reliability evidence is incomplete")
    if (
        not contract_valid
        or report.status == "rejected"
        or not replay_safe
        or not catalog_complete
        or not security_valid
        or not reliability_ready
    ):
        return ReleaseDecision("rejected", tuple(reasons))
    if report.status == "review-required":
        return ReleaseDecision("review-required", tuple(reasons))
    return ReleaseDecision("accepted", tuple(reasons))
