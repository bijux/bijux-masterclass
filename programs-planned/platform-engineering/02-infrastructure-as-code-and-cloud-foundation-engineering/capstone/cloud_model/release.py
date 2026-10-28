from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


VALID_OUTCOMES = {"pass", "review", "fail", "not-executed"}


@dataclass(frozen=True)
class Finding:
    rule: str
    outcome: str
    message: str
    blocker: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _finding(rule: str, outcome: str, message: str, blocker: bool = False) -> Finding:
    if outcome not in VALID_OUTCOMES:
        raise ValueError(outcome)
    return Finding(rule, outcome, message, blocker)


def evaluate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    findings: list[Finding] = []
    if candidate.get("publicSsh"):
        findings.append(_finding("EDGE-001", "fail", "public SSH is not allowed without a bounded exception", True))
    else:
        findings.append(_finding("EDGE-001", "pass", "no public SSH"))
    if candidate.get("imdsTokens") != "required":
        findings.append(_finding("COMPUTE-001", "fail", "IMDSv2 tokens are not required", True))
    else:
        findings.append(_finding("COMPUTE-001", "pass", "IMDSv2 required"))
    if candidate.get("stateProtection") != "verified":
        outcome = "not-executed" if candidate.get("stateProtection") == "not-executed" else "fail"
        findings.append(_finding("STATE-001", outcome, "state protection evidence is incomplete", True))
    else:
        findings.append(_finding("STATE-001", "pass", "state versioning, encryption, and locking verified"))
    if candidate.get("destructiveCriticalChange") and not candidate.get("migrationRecord"):
        findings.append(_finding("MIGRATION-001", "fail", "critical destructive change has no migration record", True))
    if candidate.get("natArchitecture") == "per-az" and candidate.get("costEvidence") != "approved":
        findings.append(_finding("COST-001", "review", "per-zone NAT requires explicit cost/availability decision"))
    if candidate.get("liveCloudEvidence") == "not-executed":
        findings.append(_finding("EVIDENCE-001", "not-executed", "real-cloud control/data-plane evidence was not executed"))
    elif candidate.get("liveCloudEvidence") == "verified":
        findings.append(_finding("EVIDENCE-001", "pass", "real-cloud evidence verified"))
    if candidate.get("longLivedCiKey"):
        findings.append(_finding("IDENTITY-001", "fail", "CI uses a long-lived cloud key", True))
    else:
        findings.append(_finding("IDENTITY-001", "pass", "CI identity is short-lived or no cloud apply is performed"))

    blockers = [f for f in findings if f.blocker and f.outcome in {"fail", "not-executed"}]
    if any(f.outcome == "fail" for f in findings):
        decision = "reject"
    elif blockers:
        decision = "not-releasable"
    elif any(f.outcome == "review" for f in findings):
        decision = "review"
    elif any(f.outcome == "not-executed" for f in findings):
        decision = "dependency-light-only"
    else:
        decision = "accept"
    return {"decision": decision, "findings": [f.as_dict() for f in findings]}
