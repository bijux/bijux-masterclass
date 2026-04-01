from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class RuleRegistered:
    policy_id: str
    rule_id: str
    metric_name: str
    severity: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class RuleActivated:
    policy_id: str
    rule_id: str
    metric_name: str
    severity: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class RuleRetired:
    policy_id: str
    rule_id: str
    metric_name: str
    reason: str
    occurred_at: datetime


@dataclass(frozen=True, slots=True)
class AlertTriggered:
    policy_id: str
    rule_id: str
    metric_name: str
    severity: str
    threshold: float
    observed_value: float
    incident_id: str
    occurred_at: datetime
