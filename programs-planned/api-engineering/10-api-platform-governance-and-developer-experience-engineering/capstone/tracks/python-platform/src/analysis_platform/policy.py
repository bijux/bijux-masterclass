from __future__ import annotations

from datetime import datetime
from typing import Iterable, Mapping, Any

from .models import Finding

Decision = str


def evaluate_findings(findings: Iterable[Finding]) -> Decision:
    items = tuple(findings)
    if any(f.status == "fail" and f.severity == "blocker" for f in items):
        return "fail"
    if any(f.status in {"fail", "review"} for f in items):
        return "review"
    return "pass"


def validate_exception(record: Mapping[str, Any], now: datetime) -> tuple[bool, str]:
    required = {"id","ruleId","entityRef","owner","reason","compensatingControl","approvedBy","createdAt","expiresAt","status"}
    missing = sorted(required - record.keys())
    if missing:
        return False, "missing:" + ",".join(missing)
    if record["status"] != "active":
        return False, "exception-not-active"
    expiry = datetime.fromisoformat(str(record["expiresAt"]).replace("Z", "+00:00"))
    if expiry <= now:
        return False, "exception-expired"
    if not str(record["reason"]).strip() or not str(record["compensatingControl"]).strip():
        return False, "empty-justification"
    return True, "valid"


def apply_exception(finding: Finding, exceptions: Iterable[Mapping[str, Any]], now: datetime) -> Finding:
    for grant in exceptions:
        valid, _ = validate_exception(grant, now)
        if valid and grant["ruleId"] == finding.rule_id and grant["entityRef"] == finding.entity_ref:
            return Finding(
                rule_id=finding.rule_id, severity=finding.severity, status="review",
                entity_ref=finding.entity_ref,
                message=f"Exception {grant['id']} applies until {grant['expiresAt']}",
                evidence=finding.evidence,
            )
    return finding
