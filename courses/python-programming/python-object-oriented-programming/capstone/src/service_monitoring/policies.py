from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .model import DomainError, MetricSample, ThresholdRule


@dataclass(frozen=True, slots=True)
class EvaluationOutcome:
    observed_value: float
    observed_at: datetime


class EvaluationPolicy:
    name = "policy"

    def evaluate(
        self,
        rule: ThresholdRule,
        samples: list[MetricSample],
    ) -> EvaluationOutcome | None:
        raise NotImplementedError


class ThresholdPolicy(EvaluationPolicy):
    name = "threshold"

    def evaluate(
        self,
        rule: ThresholdRule,
        samples: list[MetricSample],
    ) -> EvaluationOutcome | None:
        window_samples = _latest_window(rule, samples)
        if not window_samples:
            return None
        observed = max(sample.value for sample in window_samples)
        if observed < rule.threshold:
            return None
        return EvaluationOutcome(observed_value=observed, observed_at=window_samples[-1].observed_at)


class ConsecutiveThresholdPolicy(EvaluationPolicy):
    name = "consecutive"

    def evaluate(
        self,
        rule: ThresholdRule,
        samples: list[MetricSample],
    ) -> EvaluationOutcome | None:
        window_samples = _latest_window(rule, samples)
        if not window_samples:
            return None
        if any(sample.value < rule.threshold for sample in window_samples):
            return None
        return EvaluationOutcome(
            observed_value=max(sample.value for sample in window_samples),
            observed_at=window_samples[-1].observed_at,
        )


class RateOfChangePolicy(EvaluationPolicy):
    name = "rate_of_change"

    def evaluate(
        self,
        rule: ThresholdRule,
        samples: list[MetricSample],
    ) -> EvaluationOutcome | None:
        window_samples = _latest_window(rule, samples)
        if not window_samples:
            return None
        first = window_samples[0].value
        last = window_samples[-1].value
        change = last - first
        if change < rule.threshold:
            return None
        return EvaluationOutcome(observed_value=change, observed_at=window_samples[-1].observed_at)


class RuleEvaluator:
    def __init__(self, policies: list[EvaluationPolicy] | None = None) -> None:
        selected = policies or [
            ThresholdPolicy(),
            ConsecutiveThresholdPolicy(),
            RateOfChangePolicy(),
        ]
        self._policies = {policy.name: policy for policy in selected}

    def evaluate(
        self,
        rule: ThresholdRule,
        samples: list[MetricSample],
    ) -> EvaluationOutcome | None:
        try:
            policy = self._policies[rule.evaluation_mode]
        except KeyError as exc:
            raise DomainError(f"unknown evaluation mode: {rule.evaluation_mode!r}") from exc
        return policy.evaluate(rule, samples)

    def available_modes(self) -> tuple[str, ...]:
        return tuple(sorted(self._policies))


def _latest_window(rule: ThresholdRule, samples: list[MetricSample]) -> list[MetricSample]:
    ordered = sorted(samples, key=lambda sample: sample.observed_at)
    if len(ordered) < rule.window:
        return []
    return ordered[-rule.window :]
