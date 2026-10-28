"""Correctness-first performance release decisions."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping

from .regression import MetricFinding, MetricPolicy, evaluate_metric


@dataclass(frozen=True, slots=True)
class GateFinding:
    name: str
    status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReleaseDecision:
    status: str
    gates: tuple[GateFinding, ...]
    metrics: tuple[MetricFinding, ...]


def _outcomes(envelope: Mapping[str, Any]) -> Mapping[str, int]:
    value = envelope.get("outcomes")
    if not isinstance(value, Mapping):
        raise ValueError("outcomes are required")
    return value


def _correctness(envelope: Mapping[str, Any]) -> bool:
    value = envelope.get("correctness")
    if not isinstance(value, Mapping) or not isinstance(value.get("passed"), bool):
        raise ValueError("correctness.passed is required")
    return bool(value["passed"])


def evaluate_release(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> ReleaseDecision:
    gates: list[GateFinding] = []
    metrics: list[MetricFinding] = []

    comparison_fields = ("workloadHash", "environmentHash", "profileVersion")
    mismatch = tuple(
        field
        for field in comparison_fields
        if baseline.get(field) != candidate.get(field)
    )
    if mismatch:
        gates.append(GateFinding("comparability", "inconclusive", mismatch))
    else:
        gates.append(GateFinding("comparability", "passed", ()))

    if not _correctness(baseline):
        raise ValueError("baseline correctness must pass")
    if _correctness(candidate):
        gates.append(GateFinding("correctness", "passed", ()))
    else:
        gates.append(
            GateFinding("correctness", "failed", ("candidate-correctness",))
        )

    candidate_outcomes = _outcomes(candidate)
    offered = int(candidate_outcomes.get("offered", -1))
    started = int(candidate_outcomes.get("started", -1))
    missing = int(candidate_outcomes.get("missing", -1))
    coverage_reasons: list[str] = []
    if offered <= 0:
        coverage_reasons.append("offered")
    if started != offered:
        coverage_reasons.append("schedule-coverage")
    if missing != 0:
        coverage_reasons.append("missing-outcomes")
    gates.append(
        GateFinding(
            "coverage",
            "passed" if not coverage_reasons else "failed",
            tuple(coverage_reasons),
        )
    )

    metric_values = policy.get("metrics")
    if not isinstance(metric_values, list):
        raise ValueError("policy.metrics must be a list")
    baseline_summary = baseline.get("summary")
    candidate_summary = candidate.get("summary")
    if not isinstance(baseline_summary, Mapping) or not isinstance(
        candidate_summary, Mapping
    ):
        raise ValueError("summary objects are required")

    for entry in metric_values:
        if not isinstance(entry, Mapping):
            raise ValueError("metric policy must be an object")
        name = str(entry["name"])
        metric_policy = MetricPolicy(
            name=name,
            direction=str(entry["direction"]),
            absolute_regression=Decimal(str(entry["absoluteRegression"])),
            relative_regression=Decimal(str(entry["relativeRegression"])),
            hard_minimum=(
                Decimal(str(entry["hardMinimum"]))
                if "hardMinimum" in entry
                else None
            ),
            hard_maximum=(
                Decimal(str(entry["hardMaximum"]))
                if "hardMaximum" in entry
                else None
            ),
        )
        metrics.append(
            evaluate_metric(
                Decimal(str(baseline_summary[name])),
                Decimal(str(candidate_summary[name])),
                metric_policy,
            )
        )

    metric_failures = tuple(item.name for item in metrics if not item.passed)
    gates.append(
        GateFinding(
            "performance",
            "passed" if not metric_failures else "failed",
            metric_failures,
        )
    )

    statuses = {gate.status for gate in gates}
    if "inconclusive" in statuses:
        status = "inconclusive"
    elif "failed" in statuses:
        status = "rejected"
    else:
        status = "accepted"
    return ReleaseDecision(status, tuple(gates), tuple(metrics))
