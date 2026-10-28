from __future__ import annotations

from dataclasses import dataclass

from .slo import SLODefinition, SLOWindow, burn_rate


@dataclass(frozen=True, slots=True)
class BurnRateAlert:
    identifier: str
    severity: str
    long_window_seconds: int
    short_window_seconds: int
    threshold: float
    minimum_events: int = 1

    def __post_init__(self) -> None:
        if self.long_window_seconds <= self.short_window_seconds:
            raise ValueError("long window must exceed short window")
        if self.threshold <= 0:
            raise ValueError("threshold must be positive")
        if self.minimum_events < 1:
            raise ValueError("minimum_events must be positive")


@dataclass(frozen=True, slots=True)
class AlertEvaluation:
    firing: bool
    long_burn_rate: float | None
    short_burn_rate: float | None
    reason: str


def evaluate_burn_rate_alert(
    definition: SLODefinition,
    alert: BurnRateAlert,
    *,
    long_window: SLOWindow,
    short_window: SLOWindow,
) -> AlertEvaluation:
    if long_window.total < alert.minimum_events or short_window.total < alert.minimum_events:
        return AlertEvaluation(False, None, None, "insufficient-traffic")
    long_rate = burn_rate(definition, long_window)
    short_rate = burn_rate(definition, short_window)
    assert long_rate is not None and short_rate is not None
    firing = long_rate >= alert.threshold and short_rate >= alert.threshold
    return AlertEvaluation(
        firing,
        long_rate,
        short_rate,
        "budget-burning" if firing else "within-alert-threshold",
    )
