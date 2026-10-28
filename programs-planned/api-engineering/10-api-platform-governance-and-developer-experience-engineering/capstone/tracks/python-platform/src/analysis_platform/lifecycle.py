from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping, Any


@dataclass(frozen=True)
class LifecycleDecision:
    allowed: bool
    reason: str
    missing: tuple[str, ...] = ()


def evaluate_transition(*, current: str, target: str, evidence: Iterable[str],
                        policy: Mapping[str, Any], blocking_consumers: int = 0,
                        now: datetime | None = None, notice_end: datetime | None = None) -> LifecycleDecision:
    transition = next((x for x in policy["transitions"] if x["from"] == current and x["to"] == target), None)
    if transition is None:
        return LifecycleDecision(False, "transition-not-allowed")
    present = set(evidence)
    missing = tuple(sorted(set(transition["requires"]) - present))
    if missing:
        return LifecycleDecision(False, "missing-evidence", missing)
    if target == "retired" and blocking_consumers:
        return LifecycleDecision(False, "blocking-consumers")
    if target == "retired" and notice_end and now and now < notice_end:
        return LifecycleDecision(False, "notice-period-open")
    return LifecycleDecision(True, "allowed")


def deprecation_impact(consumers: Iterable[Mapping[str, Any]], api_ref: str, version: str) -> dict[str, Any]:
    affected = [c for c in consumers if c["apiRef"] == api_ref and c["version"] == version and c.get("environment") == "production"]
    blockers = [c for c in affected if c.get("criticality") in {"high", "critical"} or c.get("migrationStatus") != "complete"]
    return {
        "apiRef": api_ref,
        "version": version,
        "affectedConsumers": [c["id"] for c in affected],
        "blockingConsumers": [c["id"] for c in blockers],
        "retirementDecision": "blocked" if blockers else "eligible",
    }
