from __future__ import annotations

from collections import defaultdict

from .events import RuleActivated, RuleRetired


class ActiveRuleIndex:
    """Projection of active rule ids grouped by metric name."""

    def __init__(self) -> None:
        self._rule_ids_by_metric: dict[str, set[str]] = defaultdict(set)

    def apply(self, event: object) -> None:
        if isinstance(event, RuleActivated):
            self._rule_ids_by_metric[event.metric_name].add(event.rule_id)
            return
        if isinstance(event, RuleRetired):
            metric_rules = self._rule_ids_by_metric[event.metric_name]
            metric_rules.discard(event.rule_id)
            if not metric_rules:
                self._rule_ids_by_metric.pop(event.metric_name, None)

    def snapshot(self) -> dict[str, tuple[str, ...]]:
        return {
            metric_name: tuple(sorted(rule_ids))
            for metric_name, rule_ids in sorted(self._rule_ids_by_metric.items())
        }
