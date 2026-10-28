from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random


class FaultKind(str, Enum):
    DELAY = "delay"
    ERROR = "error"
    DROP = "drop"
    CORRUPT = "corrupt"


@dataclass(frozen=True, slots=True)
class FaultRule:
    target: str
    kind: FaultKind
    probability: float
    delay_ms: int = 0
    error_code: str = "injected-failure"

    def __post_init__(self) -> None:
        if not 0 <= self.probability <= 1:
            raise ValueError("probability must be between zero and one")
        if self.delay_ms < 0:
            raise ValueError("delay cannot be negative")


@dataclass(slots=True)
class FaultInjector:
    rules: list[FaultRule]
    seed: int = 0
    _rng: random.Random = field(init=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def decide(self, target: str) -> FaultRule | None:
        for rule in self.rules:
            if rule.target == target and self._rng.random() < rule.probability:
                return rule
        return None

@dataclass(frozen=True, slots=True)
class FaultPlan:
    identifier: str
    hypothesis: str
    steady_state: tuple[str, ...]
    blast_radius: str
    abort_conditions: tuple[str, ...]
    cleanup: tuple[str, ...]
    approved_environments: tuple[str, ...] = ("course", "test")

    def validate(self) -> None:
        if not self.identifier or len(self.identifier) > 80:
            raise ValueError("fault plan identifier must contain 1..80 characters")
        if len(self.hypothesis.strip()) < 12:
            raise ValueError("fault plan requires a falsifiable hypothesis")
        if not self.steady_state:
            raise ValueError("fault plan requires a steady-state definition")
        if not self.blast_radius.strip():
            raise ValueError("fault plan requires a blast radius")
        if not self.abort_conditions:
            raise ValueError("fault plan requires abort conditions")
        if not self.cleanup:
            raise ValueError("fault plan requires cleanup actions")
        if not self.approved_environments:
            raise ValueError("fault plan requires approved environments")

