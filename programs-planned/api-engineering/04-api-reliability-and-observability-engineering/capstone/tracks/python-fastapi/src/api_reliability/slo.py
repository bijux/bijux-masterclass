from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SLODefinition:
    identifier: str
    objective: float
    window_seconds: int
    description: str = ""
    version: str = "1.0"

    def __post_init__(self) -> None:
        if not 0 < self.objective < 1:
            raise ValueError("objective must be between zero and one")
        if self.window_seconds <= 0:
            raise ValueError("window must be positive")
        if not self.version or len(self.version) > 40:
            raise ValueError("SLO definition version must contain 1..40 characters")

    @property
    def allowed_bad_fraction(self) -> float:
        return 1.0 - self.objective


@dataclass(frozen=True, slots=True)
class SLOWindow:
    good: int
    total: int

    def __post_init__(self) -> None:
        if self.good < 0 or self.total < 0 or self.good > self.total:
            raise ValueError("invalid SLO event counts")

    @property
    def bad(self) -> int:
        return self.total - self.good

    @property
    def compliance(self) -> float | None:
        return None if self.total == 0 else self.good / self.total


def error_budget_events(definition: SLODefinition, total: int) -> float:
    if total < 0:
        raise ValueError("total must be non-negative")
    return definition.allowed_bad_fraction * total


def burn_rate(definition: SLODefinition, window: SLOWindow) -> float | None:
    if window.total == 0:
        return None
    observed_bad_fraction = window.bad / window.total
    return observed_bad_fraction / definition.allowed_bad_fraction


def budget_remaining_fraction(
    definition: SLODefinition,
    window: SLOWindow,
) -> float | None:
    allowed = error_budget_events(definition, window.total)
    if window.total == 0 or allowed == 0:
        return None
    return (allowed - window.bad) / allowed
