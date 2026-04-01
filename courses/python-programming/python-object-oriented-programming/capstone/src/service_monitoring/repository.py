from __future__ import annotations

from copy import deepcopy

from .model import MonitoringPolicy


class InMemoryPolicyRepository:
    def __init__(self) -> None:
        self._items: dict[str, MonitoringPolicy] = {}

    def add(self, policy: MonitoringPolicy) -> None:
        self._items[policy.policy_id] = policy.clone()

    def get(self, policy_id: str) -> MonitoringPolicy:
        return self._items[policy_id].clone()

    def save(self, policy: MonitoringPolicy) -> None:
        self._items[policy.policy_id] = policy.clone()

    def snapshot(self) -> dict[str, MonitoringPolicy]:
        return deepcopy(self._items)

    def restore(self, snapshot: dict[str, MonitoringPolicy]) -> None:
        self._items = deepcopy(snapshot)


class InMemoryUnitOfWork:
    """Rollback-oriented unit of work for the capstone exercises."""

    def __init__(self, repository: InMemoryPolicyRepository):
        self.repository = repository
        self._loaded: dict[str, MonitoringPolicy] = {}
        self._baseline: dict[str, MonitoringPolicy] | None = None
        self._committed = False

    def __enter__(self) -> "InMemoryUnitOfWork":
        self._baseline = self.repository.snapshot()
        self._loaded.clear()
        self._committed = False
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None or not self._committed:
            assert self._baseline is not None
            self.repository.restore(self._baseline)
        self._loaded.clear()
        self._baseline = None
        return False

    def load(self, policy_id: str) -> MonitoringPolicy:
        policy = self.repository.get(policy_id)
        self._loaded[policy_id] = policy
        return policy

    def register(self, policy: MonitoringPolicy) -> None:
        self._loaded[policy.policy_id] = policy

    def commit(self) -> None:
        for policy in self._loaded.values():
            self.repository.save(policy)
        self._committed = True
