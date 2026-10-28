from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .models import MetricObservation, SegmentObservation

AnalysisDecision = Literal["pass", "fail", "inconclusive", "unavailable"]


@dataclass(frozen=True)
class AnalysisResult:
    decision: AnalysisDecision
    reasons: tuple[str, ...]


def evaluate_analysis(metrics: list[MetricObservation], segments: list[SegmentObservation], minimum_samples: int) -> AnalysisResult:
    failures: list[str] = []
    inconclusive: list[str] = []
    unavailable: list[str] = []
    for metric in metrics:
        if metric.candidate_value is None or metric.stable_value is None:
            if metric.required:
                unavailable.append(f"{metric.name}: required metric unavailable")
            continue
        if metric.candidate_samples < minimum_samples or metric.stable_samples < minimum_samples:
            inconclusive.append(f"{metric.name}: insufficient comparable samples")
        if metric.candidate_value > metric.absolute_limit:
            failures.append(f"{metric.name}: absolute limit exceeded")
        if metric.candidate_value > metric.stable_value + metric.relative_margin:
            failures.append(f"{metric.name}: stable-relative margin exceeded")
    for segment in segments:
        if segment.samples < minimum_samples:
            inconclusive.append(f"segment {segment.name}: insufficient samples")
            continue
        rate = segment.failures / segment.samples if segment.samples else 1.0
        if rate > segment.max_failure_rate:
            failures.append(
                f"segment {segment.name}: failure rate {rate:.4f} exceeds {segment.max_failure_rate:.4f}"
            )
    # A measured policy violation is a failure even when another population is
    # incomplete. Missing required telemetry is unavailable only when no direct
    # failure was already observed.
    if failures:
        return AnalysisResult("fail", tuple(failures + unavailable + inconclusive))
    if unavailable:
        return AnalysisResult("unavailable", tuple(unavailable + inconclusive))
    if inconclusive:
        return AnalysisResult("inconclusive", tuple(inconclusive))
    return AnalysisResult("pass", ("all required metrics and segments passed",))


@dataclass
class Canary:
    stable: str
    candidate: str
    configured_weight: int = 0
    actual_candidate_requests: int = 0
    state: str = "Pending"

    def expose(self, weight: int, observed_requests: int) -> None:
        if not 0 <= weight <= 100:
            raise ValueError("weight must be 0..100")
        self.configured_weight = weight
        self.actual_candidate_requests = observed_requests
        self.state = "Progressing"

    def complete(self, result: AnalysisResult) -> None:
        if result.decision == "pass":
            self.configured_weight = 100
            self.state = "Promoted"
        elif result.decision in {"fail", "unavailable"}:
            self.configured_weight = 0
            self.state = "Aborted"
        else:
            self.state = "Paused"
