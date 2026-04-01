from __future__ import annotations

from service_monitoring import (
    InMemoryPolicyRepository,
    InMemoryUnitOfWork,
    MetricName,
    MonitoringPolicy,
    Severity,
    ThresholdRule,
)


def build_policy() -> MonitoringPolicy:
    policy = MonitoringPolicy("policy-201")
    policy.add_rule(
        ThresholdRule(
            rule_id="latency-hot",
            metric_name=MetricName("latency"),
            threshold=0.75,
            severity=Severity("warning"),
        )
    )
    return policy


def test_unit_of_work_persists_registered_changes_on_commit() -> None:
    repository = InMemoryPolicyRepository()
    repository.add(build_policy())

    with InMemoryUnitOfWork(repository) as uow:
        policy = uow.load("policy-201")
        policy.activate_rule("latency-hot")
        uow.register(policy)
        uow.commit()

    stored = repository.get("policy-201")
    assert stored.active_rules[0].definition.rule_id == "latency-hot"


def test_unit_of_work_restores_repository_state_on_error() -> None:
    repository = InMemoryPolicyRepository()
    repository.add(build_policy())

    try:
        with InMemoryUnitOfWork(repository) as uow:
            policy = uow.load("policy-201")
            policy.activate_rule("latency-hot")
            uow.register(policy)
            raise RuntimeError("downstream persistence failed")
    except RuntimeError:
        pass

    stored = repository.get("policy-201")
    assert stored.active_rules == ()
