from __future__ import annotations

from .models import ReleaseCandidate


def classify_release(candidate: ReleaseCandidate) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if candidate.protected_deletions:
        reasons.extend(f"protected deletion: {item}" for item in candidate.protected_deletions)
    for gate in candidate.gates:
        if gate.status == "fail" and gate.blocker:
            reasons.append(f"{gate.name}: failed — {gate.reason}")
    if reasons:
        return "rejected", reasons
    missing = [gate for gate in candidate.gates if gate.status == "not-executed" and gate.blocker]
    if missing:
        return "not-executed", [f"{gate.name}: not executed — {gate.reason}" for gate in missing]
    reviews = [gate for gate in candidate.gates if gate.status == "review"]
    if reviews:
        if candidate.approvals:
            return "accepted", [f"approved review: {gate.name}" for gate in reviews]
        return "review-required", [f"{gate.name}: {gate.reason}" for gate in reviews]
    return "accepted", ["all blocker gates passed"]
