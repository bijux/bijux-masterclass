from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable

from .events import AlertTriggered, RuleActivated, RuleRegistered, RuleRetired


class DomainError(ValueError):
    """Raised when a domain invariant is violated."""


class RuleState(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    RETIRED = "retired"


class MetricName(str):
    def __new__(cls, value: str) -> "MetricName":
        normalized = value.strip()
        if not normalized:
            raise DomainError("metric names must not be empty")
        return super().__new__(cls, normalized)


class Severity(str):
    _ALLOWED = {"warning", "critical"}

    def __new__(cls, value: str) -> "Severity":
        normalized = value.strip().lower()
        if normalized not in cls._ALLOWED:
            raise DomainError(f"unsupported severity: {value!r}")
        return super().__new__(cls, normalized)


@dataclass(frozen=True, slots=True)
class MetricSample:
    observed_at: datetime
    metric_name: MetricName
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise DomainError("metric values must be non-negative")


@dataclass(frozen=True, slots=True)
class ThresholdRule:
    rule_id: str
    metric_name: MetricName
    threshold: float
    severity: Severity
    window: int = 1
    evaluation_mode: str = "threshold"

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise DomainError("rule ids must not be empty")
        if not 0 <= self.threshold <= 1:
            raise DomainError("threshold must be between 0 and 1")
        if self.window < 1:
            raise DomainError("window must be at least 1")
        if not self.evaluation_mode.strip():
            raise DomainError("evaluation_mode must not be empty")


@dataclass(frozen=True, slots=True)
class Alert:
    incident_id: str
    rule_id: str
    metric_name: MetricName
    severity: Severity
    threshold: float
    observed_value: float
    observed_at: datetime


@dataclass(slots=True)
class ManagedRule:
    definition: ThresholdRule
    state: RuleState = RuleState.DRAFT
    retired_reason: str | None = None

    def activate(self) -> None:
        if self.state is RuleState.RETIRED:
            raise DomainError("retired rules cannot be activated")
        self.state = RuleState.ACTIVE

    def retire(self, reason: str) -> None:
        if not reason.strip():
            raise DomainError("retirement reason must not be empty")
        self.state = RuleState.RETIRED
        self.retired_reason = reason.strip()


class MonitoringPolicy:
    """Aggregate root for threshold monitoring rules."""

    def __init__(self, policy_id: str):
        if not policy_id.strip():
            raise DomainError("policy ids must not be empty")
        self.policy_id = policy_id
        self._rules: dict[str, ManagedRule] = {}
        self._pending_events: list[object] = []

    @staticmethod
    def _default_occurred_at() -> datetime:
        return datetime.now(timezone.utc)

    @property
    def rules(self) -> tuple[ManagedRule, ...]:
        return tuple(self._rules.values())

    @property
    def active_rules(self) -> tuple[ManagedRule, ...]:
        return tuple(rule for rule in self._rules.values() if rule.state is RuleState.ACTIVE)

    def add_rule(self, rule: ThresholdRule, *, occurred_at: datetime | None = None) -> None:
        if rule.rule_id in self._rules:
            raise DomainError(f"rule {rule.rule_id!r} already exists")
        self._rules[rule.rule_id] = ManagedRule(definition=rule)
        self._pending_events.append(
            RuleRegistered(
                policy_id=self.policy_id,
                rule_id=rule.rule_id,
                metric_name=str(rule.metric_name),
                severity=str(rule.severity),
                occurred_at=occurred_at or self._default_occurred_at(),
            )
        )

    def activate_rule(self, rule_id: str, *, occurred_at: datetime | None = None) -> None:
        managed = self._require_rule(rule_id)
        self._ensure_unique_active_signature(managed.definition, excluding=rule_id)
        managed.activate()
        rule = managed.definition
        self._pending_events.append(
            RuleActivated(
                policy_id=self.policy_id,
                rule_id=rule.rule_id,
                metric_name=str(rule.metric_name),
                severity=str(rule.severity),
                occurred_at=occurred_at or self._default_occurred_at(),
            )
        )

    def retire_rule(
        self,
        rule_id: str,
        reason: str,
        *,
        occurred_at: datetime | None = None,
    ) -> None:
        managed = self._require_rule(rule_id)
        managed.retire(reason)
        rule = managed.definition
        self._pending_events.append(
            RuleRetired(
                policy_id=self.policy_id,
                rule_id=rule.rule_id,
                metric_name=str(rule.metric_name),
                reason=reason.strip(),
                occurred_at=occurred_at or self._default_occurred_at(),
            )
        )

    def evaluate(
        self,
        samples: Iterable[MetricSample],
        evaluator: "RuleEvaluator | None" = None,
    ) -> list[Alert]:
        if evaluator is None:
            from .policies import RuleEvaluator

            evaluator = RuleEvaluator()
        samples_by_metric: dict[MetricName, list[MetricSample]] = defaultdict(list)
        for sample in samples:
            samples_by_metric[sample.metric_name].append(sample)

        alerts: list[Alert] = []
        for managed in self.active_rules:
            rule = managed.definition
            relevant = samples_by_metric.get(rule.metric_name, [])
            if not relevant:
                continue
            outcome = evaluator.evaluate(rule, relevant)
            if outcome is None:
                continue
            observed_at = outcome.observed_at
            incident_id = (
                f"{self.policy_id}:{rule.rule_id}:{observed_at.isoformat(timespec='seconds')}"
            )
            alert = Alert(
                incident_id=incident_id,
                rule_id=rule.rule_id,
                metric_name=rule.metric_name,
                severity=rule.severity,
                threshold=rule.threshold,
                observed_value=outcome.observed_value,
                observed_at=observed_at,
            )
            alerts.append(alert)
            self._pending_events.append(
                AlertTriggered(
                    policy_id=self.policy_id,
                    rule_id=rule.rule_id,
                    metric_name=str(rule.metric_name),
                    severity=str(rule.severity),
                    threshold=rule.threshold,
                    observed_value=outcome.observed_value,
                    incident_id=incident_id,
                    occurred_at=observed_at,
                )
            )
        return alerts

    def collect_events(self) -> list[object]:
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def clone(self) -> "MonitoringPolicy":
        return deepcopy(self)

    def _require_rule(self, rule_id: str) -> ManagedRule:
        try:
            return self._rules[rule_id]
        except KeyError as exc:
            raise DomainError(f"unknown rule: {rule_id!r}") from exc

    def _ensure_unique_active_signature(
        self,
        candidate: ThresholdRule,
        *,
        excluding: str | None = None,
    ) -> None:
        candidate_signature = (candidate.metric_name, candidate.window)
        for rule_id, managed in self._rules.items():
            if rule_id == excluding or managed.state is not RuleState.ACTIVE:
                continue
            current = managed.definition
            if (current.metric_name, current.window) == candidate_signature:
                raise DomainError(
                    "active rules must not share the same metric/window signature"
                )
