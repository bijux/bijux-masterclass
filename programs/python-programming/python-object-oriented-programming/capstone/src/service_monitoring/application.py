from __future__ import annotations

from dataclasses import dataclass

from .model import MetricName, MetricSample, MonitoringPolicy, RuleState, Severity, ThresholdRule
from .read_models import IncidentSnapshot
from .repository import InMemoryUnitOfWork
from .runtime import CycleReport, MetricSource, MonitoringRuntime


@dataclass(frozen=True, slots=True)
class RuleRegistration:
    rule_id: str
    metric_name: str
    threshold: float
    severity: str
    window: int = 1
    evaluation_mode: str = "threshold"

    def to_rule(self) -> ThresholdRule:
        return ThresholdRule(
            rule_id=self.rule_id,
            metric_name=MetricName(self.metric_name),
            threshold=self.threshold,
            severity=Severity(self.severity),
            window=self.window,
            evaluation_mode=self.evaluation_mode,
        )


@dataclass(frozen=True, slots=True)
class PolicySummary:
    policy_id: str
    draft_rule_ids: tuple[str, ...]
    active_rule_ids: tuple[str, ...]
    retired_rule_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RuleSnapshot:
    rule_id: str
    metric_name: str
    threshold: float
    severity: str
    window: int
    evaluation_mode: str
    state: str
    retired_reason: str | None


@dataclass(frozen=True, slots=True)
class MonitoringSnapshot:
    summary: PolicySummary
    rules: tuple[RuleSnapshot, ...]
    active_rule_index: dict[str, tuple[str, ...]]
    open_incidents: dict[str, IncidentSnapshot]
    incident_history: dict[str, tuple[IncidentSnapshot, ...]]


@dataclass(frozen=True, slots=True)
class ObservationResult:
    cycle_report: CycleReport
    snapshot: MonitoringSnapshot


class MonitoringApplication:
    """Scenario-level entrypoint over the capstone's runtime and domain model."""

    def __init__(self, runtime: MonitoringRuntime | None = None) -> None:
        self.runtime = runtime or MonitoringRuntime()

    def create_policy(self, policy_id: str) -> PolicySummary:
        self.runtime.register_policy(MonitoringPolicy(policy_id))
        return self.policy_summary(policy_id)

    def register_rule(self, policy_id: str, registration: RuleRegistration) -> PolicySummary:
        with InMemoryUnitOfWork(self.runtime.repository) as uow:
            policy = uow.load(policy_id)
            policy.add_rule(registration.to_rule())
            # Registration does not currently feed projections, so only the aggregate must persist it.
            policy.collect_events()
            uow.register(policy)
            uow.commit()
        return self.policy_summary(policy_id)

    def activate_rule(self, policy_id: str, rule_id: str) -> PolicySummary:
        self.runtime.activate_rule(policy_id, rule_id)
        return self.policy_summary(policy_id)

    def retire_rule(self, policy_id: str, rule_id: str, reason: str) -> PolicySummary:
        self.runtime.retire_rule(policy_id, rule_id, reason)
        return self.policy_summary(policy_id)

    def observe_samples(
        self,
        policy_id: str,
        samples: list[MetricSample],
    ) -> ObservationResult:
        cycle_report = self.runtime.run_cycle(policy_id, samples)
        return ObservationResult(cycle_report=cycle_report, snapshot=self.snapshot(policy_id))

    def observe_source(self, policy_id: str, source: MetricSource) -> ObservationResult:
        cycle_report = self.runtime.run_source(policy_id, source)
        return ObservationResult(cycle_report=cycle_report, snapshot=self.snapshot(policy_id))

    def policy_summary(self, policy_id: str) -> PolicySummary:
        policy = self.runtime.repository.get(policy_id)
        draft_rule_ids: list[str] = []
        active_rule_ids: list[str] = []
        retired_rule_ids: list[str] = []

        for managed_rule in policy.rules:
            if managed_rule.state is RuleState.DRAFT:
                draft_rule_ids.append(managed_rule.definition.rule_id)
            elif managed_rule.state is RuleState.ACTIVE:
                active_rule_ids.append(managed_rule.definition.rule_id)
            else:
                retired_rule_ids.append(managed_rule.definition.rule_id)

        return PolicySummary(
            policy_id=policy.policy_id,
            draft_rule_ids=tuple(sorted(draft_rule_ids)),
            active_rule_ids=tuple(sorted(active_rule_ids)),
            retired_rule_ids=tuple(sorted(retired_rule_ids)),
        )

    def snapshot(self, policy_id: str) -> MonitoringSnapshot:
        runtime_snapshot = self.runtime.snapshot()
        policy = self.runtime.repository.get(policy_id)
        rules = tuple(
            RuleSnapshot(
                rule_id=managed_rule.definition.rule_id,
                metric_name=str(managed_rule.definition.metric_name),
                threshold=managed_rule.definition.threshold,
                severity=str(managed_rule.definition.severity),
                window=managed_rule.definition.window,
                evaluation_mode=managed_rule.definition.evaluation_mode,
                state=managed_rule.state.value,
                retired_reason=managed_rule.retired_reason,
            )
            for managed_rule in sorted(
                policy.rules,
                key=lambda managed_rule: managed_rule.definition.rule_id,
            )
        )
        return MonitoringSnapshot(
            summary=self.policy_summary(policy_id),
            rules=rules,
            active_rule_index=runtime_snapshot["active_rule_index"],
            open_incidents=runtime_snapshot["open_incidents"],
            incident_history=runtime_snapshot["incident_history"],
        )
