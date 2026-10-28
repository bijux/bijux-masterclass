from __future__ import annotations

from typing import Any


CATEGORIES = {
    "remote-change",
    "unapplied-configuration",
    "provider-normalization",
    "state-conflict",
    "intentional-emergency-change",
}


def classify_difference(row: dict[str, Any]) -> dict[str, Any]:
    signals = row.get("signals", {})
    if signals.get("lineageMismatch") or signals.get("serialRegression"):
        category = "state-conflict"
        default_action = "isolate-and-recover-state"
    elif signals.get("providerVersionChanged") and not signals.get("remoteAuditEvent"):
        category = "provider-normalization"
        default_action = "review-provider-read-semantics"
    elif signals.get("incidentId") and signals.get("remoteAuditEvent"):
        category = "intentional-emergency-change"
        default_action = "adopt-or-expire-with-owner"
    elif signals.get("repositoryChanged") and not signals.get("remoteAuditEvent"):
        category = "unapplied-configuration"
        default_action = "review-and-apply-declared-change"
    else:
        category = "remote-change"
        default_action = "investigate-and-reconcile"
    return {
        "address": row.get("address"),
        "category": category,
        "defaultAction": default_action,
        "owner": row.get("owner"),
        "incidentId": signals.get("incidentId"),
    }


def validate_move_map(moves: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    sources: set[str] = set()
    targets: set[str] = set()
    for row in moves:
        source, target = row.get("from"), row.get("to")
        if not source or not target:
            errors.append("move needs from and to")
            continue
        if source in sources:
            errors.append(f"duplicate move source: {source}")
        if target in targets:
            errors.append(f"duplicate move target: {target}")
        if source == target:
            errors.append(f"move source and target are identical: {source}")
        sources.add(source)
        targets.add(target)
    return errors
