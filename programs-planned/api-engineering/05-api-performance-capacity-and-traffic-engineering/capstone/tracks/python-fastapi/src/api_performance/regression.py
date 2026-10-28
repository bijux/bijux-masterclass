"""Metric regression calculations with absolute and relative bounds."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .capacity import decimal


@dataclass(frozen=True, slots=True)
class MetricPolicy:
    name: str
    direction: str
    absolute_regression: Decimal
    relative_regression: Decimal
    hard_minimum: Decimal | None = None
    hard_maximum: Decimal | None = None

    def __post_init__(self) -> None:
        if self.direction not in {"lower", "higher"}:
            raise ValueError("direction must be lower or higher")
        if decimal(self.absolute_regression) < 0:
            raise ValueError("absolute regression must be non-negative")
        if decimal(self.relative_regression) < 0:
            raise ValueError("relative regression must be non-negative")


@dataclass(frozen=True, slots=True)
class MetricFinding:
    name: str
    baseline: Decimal
    candidate: Decimal
    absolute_change: Decimal
    relative_change: Decimal | None
    passed: bool
    reason: str


def evaluate_metric(
    baseline_value: Decimal,
    candidate_value: Decimal,
    policy: MetricPolicy,
) -> MetricFinding:
    baseline = decimal(baseline_value)
    candidate = decimal(candidate_value)
    absolute = candidate - baseline
    relative = None if baseline == 0 else absolute / abs(baseline)

    hard_pass = True
    hard_reason = ""
    if policy.hard_minimum is not None and candidate < decimal(policy.hard_minimum):
        hard_pass = False
        hard_reason = "below-hard-minimum"
    if policy.hard_maximum is not None and candidate > decimal(policy.hard_maximum):
        hard_pass = False
        hard_reason = "above-hard-maximum"

    if policy.direction == "lower":
        adverse_absolute = absolute
        adverse_relative = relative if relative is not None else (
            Decimal("Infinity") if candidate > 0 else Decimal("0")
        )
    else:
        adverse_absolute = -absolute
        adverse_relative = -relative if relative is not None else (
            Decimal("Infinity") if candidate < 0 else Decimal("0")
        )

    threshold_pass = not (
        adverse_absolute > decimal(policy.absolute_regression)
        and adverse_relative > decimal(policy.relative_regression)
    )
    passed = hard_pass and threshold_pass
    if not hard_pass:
        reason = hard_reason
    elif not threshold_pass:
        reason = "regression-threshold"
    else:
        reason = "within-policy"
    return MetricFinding(
        name=policy.name,
        baseline=baseline,
        candidate=candidate,
        absolute_change=absolute,
        relative_change=relative,
        passed=passed,
        reason=reason,
    )
