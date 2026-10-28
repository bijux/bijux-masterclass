from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AttemptResult(str, Enum):
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"


@dataclass(slots=True)
class EffectStore:
    effects: dict[str, str] = field(default_factory=dict)

    def commit(self, identity: str, digest: str) -> bool:
        existing = self.effects.get(identity)
        if existing is None:
            self.effects[identity] = digest
            return True
        if existing != digest:
            raise ValueError("logical effect identity reused with different result")
        return False


@dataclass(slots=True)
class JobState:
    completions: int = 1
    backoff_limit: int = 6
    succeeded: set[int] = field(default_factory=set)
    failures: dict[int, int] = field(default_factory=dict)

    def record(self, index: int, result: AttemptResult) -> None:
        if index < 0 or index >= self.completions:
            raise ValueError("completion index out of range")
        if result is AttemptResult.SUCCEEDED:
            self.succeeded.add(index)
        else:
            self.failures[index] = self.failures.get(index, 0) + 1

    @property
    def complete(self) -> bool:
        return len(self.succeeded) == self.completions

    @property
    def failed(self) -> bool:
        return any(count > self.backoff_limit for count in self.failures.values())


class CronConcurrency(str, Enum):
    ALLOW = "Allow"
    FORBID = "Forbid"
    REPLACE = "Replace"


def cron_decision(policy: CronConcurrency, active_runs: int) -> str:
    if active_runs == 0 or policy is CronConcurrency.ALLOW:
        return "start"
    if policy is CronConcurrency.FORBID:
        return "skip"
    return "replace"
