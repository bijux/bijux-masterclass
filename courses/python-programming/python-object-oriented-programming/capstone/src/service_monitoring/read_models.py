from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .events import AlertTriggered, RuleRetired


@dataclass(frozen=True, slots=True)
class IncidentSnapshot:
    incident_id: str
    rule_id: str
    metric_name: str
    severity: str
    threshold: float
    observed_value: float
    occurred_at: str


class IncidentLedger:
    """Projection of incident history and currently open incidents."""

    def __init__(self) -> None:
        self._open_by_rule: dict[str, IncidentSnapshot] = {}
        self._history_by_metric: dict[str, list[IncidentSnapshot]] = defaultdict(list)

    def apply(self, event: object) -> None:
        if isinstance(event, AlertTriggered):
            snapshot = IncidentSnapshot(
                incident_id=event.incident_id,
                rule_id=event.rule_id,
                metric_name=event.metric_name,
                severity=event.severity,
                threshold=event.threshold,
                observed_value=event.observed_value,
                occurred_at=event.occurred_at.isoformat(timespec="seconds"),
            )
            self._open_by_rule[event.rule_id] = snapshot
            self._history_by_metric[event.metric_name].append(snapshot)
            return
        if isinstance(event, RuleRetired):
            self._open_by_rule.pop(event.rule_id, None)

    def open_incidents(self) -> dict[str, IncidentSnapshot]:
        return dict(sorted(self._open_by_rule.items()))

    def history(self) -> dict[str, tuple[IncidentSnapshot, ...]]:
        return {
            metric_name: tuple(items)
            for metric_name, items in sorted(self._history_by_metric.items())
        }
