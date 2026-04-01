from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .model import Alert, MetricSample, MonitoringPolicy
from .policies import RuleEvaluator
from .projections import ActiveRuleIndex
from .read_models import IncidentLedger
from .repository import InMemoryPolicyRepository, InMemoryUnitOfWork


class MetricSource(Protocol):
    def fetch_samples(self, policy_id: str) -> list[MetricSample]:
        ...


class IncidentSink(Protocol):
    def publish(self, alerts: list[Alert]) -> None:
        ...


class StaticMetricSource:
    def __init__(self, samples: list[MetricSample]) -> None:
        self._samples = list(samples)

    def fetch_samples(self, policy_id: str) -> list[MetricSample]:
        return list(self._samples)


class CollectingIncidentSink:
    def __init__(self) -> None:
        self._published_batches: list[list[Alert]] = []

    def publish(self, alerts: list[Alert]) -> None:
        self._published_batches.append(list(alerts))

    def published_batches(self) -> tuple[tuple[Alert, ...], ...]:
        return tuple(tuple(batch) for batch in self._published_batches)


@dataclass(frozen=True, slots=True)
class CycleReport:
    policy_id: str
    alerts_published: int
    active_rule_count: int
    open_incident_count: int


class MonitoringRuntime:
    """Facade over the capstone's domain, projections, and runtime adapters."""

    def __init__(
        self,
        *,
        repository: InMemoryPolicyRepository | None = None,
        evaluator: RuleEvaluator | None = None,
        sink: IncidentSink | None = None,
        active_rule_index: ActiveRuleIndex | None = None,
        incident_ledger: IncidentLedger | None = None,
    ) -> None:
        self.repository = repository or InMemoryPolicyRepository()
        self.evaluator = evaluator or RuleEvaluator()
        self.sink = sink or CollectingIncidentSink()
        self.active_rule_index = active_rule_index or ActiveRuleIndex()
        self.incident_ledger = incident_ledger or IncidentLedger()

    def register_policy(self, policy: MonitoringPolicy) -> None:
        self.repository.add(policy)

    def activate_rule(self, policy_id: str, rule_id: str) -> None:
        with InMemoryUnitOfWork(self.repository) as uow:
            policy = uow.load(policy_id)
            policy.activate_rule(rule_id)
            self._apply_events(policy.collect_events())
            uow.register(policy)
            uow.commit()

    def retire_rule(self, policy_id: str, rule_id: str, reason: str) -> None:
        with InMemoryUnitOfWork(self.repository) as uow:
            policy = uow.load(policy_id)
            policy.retire_rule(rule_id, reason)
            self._apply_events(policy.collect_events())
            uow.register(policy)
            uow.commit()

    def run_source(self, policy_id: str, source: MetricSource) -> CycleReport:
        samples = source.fetch_samples(policy_id)
        return self.run_cycle(policy_id, samples)

    def run_cycle(self, policy_id: str, samples: list[MetricSample]) -> CycleReport:
        with InMemoryUnitOfWork(self.repository) as uow:
            policy = uow.load(policy_id)
            alerts = policy.evaluate(samples, evaluator=self.evaluator)
            events = policy.collect_events()
            self.sink.publish(alerts)
            self._apply_events(events)
            uow.register(policy)
            uow.commit()
            return CycleReport(
                policy_id=policy_id,
                alerts_published=len(alerts),
                active_rule_count=len(policy.active_rules),
                open_incident_count=len(self.incident_ledger.open_incidents()),
            )

    def snapshot(self) -> dict[str, object]:
        return {
            "active_rule_index": self.active_rule_index.snapshot(),
            "open_incidents": self.incident_ledger.open_incidents(),
            "incident_history": self.incident_ledger.history(),
        }

    def _apply_events(self, events: list[object]) -> None:
        for event in events:
            self.active_rule_index.apply(event)
            self.incident_ledger.apply(event)
