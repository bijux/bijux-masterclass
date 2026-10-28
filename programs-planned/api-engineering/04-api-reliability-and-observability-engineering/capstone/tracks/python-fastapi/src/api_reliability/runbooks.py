from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Runbook:
    identifier: str
    title: str
    owner: str
    trigger: str
    customer_impact: str
    prerequisites: tuple[str, ...]
    immediate_actions: tuple[str, ...]
    stop_conditions: tuple[str, ...]
    diagnosis: tuple[str, ...]
    mitigation: tuple[str, ...]
    rollback: tuple[str, ...]
    recovery_validation: tuple[str, ...]
    closure_criteria: tuple[str, ...]
    escalation: tuple[str, ...]


_LIST_FIELDS = (
    "prerequisites",
    "immediateActions",
    "stopConditions",
    "diagnosis",
    "mitigation",
    "rollback",
    "recoveryValidation",
    "closureCriteria",
    "escalation",
)
_REQUIRED_FIELDS = {
    "id",
    "title",
    "owner",
    "trigger",
    "customerImpact",
    *_LIST_FIELDS,
}


def parse_runbook(value: dict[str, Any]) -> Runbook:
    missing = _REQUIRED_FIELDS - set(value)
    if missing:
        raise ValueError(f"runbook missing fields: {sorted(missing)}")
    for key in ("id", "title", "owner", "trigger", "customerImpact"):
        if not isinstance(value[key], str) or not value[key].strip():
            raise ValueError(f"runbook field {key} must be non-empty text")
    for key in _LIST_FIELDS:
        if not isinstance(value[key], list) or not value[key]:
            raise ValueError(f"runbook field {key} must be a non-empty list")
        if any(not isinstance(item, str) or not item.strip() for item in value[key]):
            raise ValueError(f"runbook field {key} contains an invalid step")
    return Runbook(
        identifier=value["id"],
        title=value["title"],
        owner=value["owner"],
        trigger=value["trigger"],
        customer_impact=value["customerImpact"],
        prerequisites=tuple(value["prerequisites"]),
        immediate_actions=tuple(value["immediateActions"]),
        stop_conditions=tuple(value["stopConditions"]),
        diagnosis=tuple(value["diagnosis"]),
        mitigation=tuple(value["mitigation"]),
        rollback=tuple(value["rollback"]),
        recovery_validation=tuple(value["recoveryValidation"]),
        closure_criteria=tuple(value["closureCriteria"]),
        escalation=tuple(value["escalation"]),
    )
