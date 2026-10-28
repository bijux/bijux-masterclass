#!/usr/bin/env python3
"""Dependency-light tour through Course 4's operational mechanisms."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from api_reliability.alerts import BurnRateAlert, evaluate_burn_rate_alert
from api_reliability.circuit import CircuitBreaker, CircuitOpen
from api_reliability.clock import ManualClock
from api_reliability.context import new_root, parse_traceparent
from api_reliability.deadline import Deadline
from api_reliability.health import (
    ComponentHealth,
    HealthEvaluator,
    LifecycleController,
    LifecyclePhase,
)
from api_reliability.metrics import MetricDescriptor, MetricRegistry
from api_reliability.reconcile import (
    ArtifactRow,
    EventRow,
    JobRow,
    OutboxRow,
    RunRow,
    Snapshot,
    finding_counts,
    inspect,
)
from api_reliability.retry import RetryPolicy, fit_delays_to_deadline, plan_retry_delays
from api_reliability.slo import SLODefinition, SLOWindow
from api_reliability.telemetry import InMemoryEventSink, StructuredLogger

ROOT = Path(__file__).resolve().parents[2]


def emit(label: str, value: object) -> None:
    print(json.dumps({"step": label, "value": value}, sort_keys=True, default=str))


def main() -> None:
    journeys = yaml.safe_load(
        (ROOT / "capstone/reliability-case/journeys.yaml").read_text(encoding="utf-8")
    )["journeys"]
    emit("critical-journeys", [row["id"] for row in journeys])

    clock = ManualClock(1_000)
    parent = Deadline.after(clock, 1_000)
    child = parent.child(clock, 600)
    delays = plan_retry_delays(
        RetryPolicy(max_attempts=4, initial_delay_ms=100, maximum_delay_ms=400),
        seed=7,
    )
    fitted = fit_delays_to_deadline(
        delays,
        clock=clock,
        deadline=child,
        minimum_attempt_ms=125,
    )
    emit("retry-budget", {"planned": delays, "fitted": fitted})

    breaker = CircuitBreaker(failure_threshold=2, open_duration_ms=500)
    breaker.allow(clock)
    breaker.failure(clock)
    breaker.allow(clock)
    breaker.failure(clock)
    try:
        breaker.allow(clock)
    except CircuitOpen:
        emit("circuit", "open-after-two-failures")
    clock.advance(500)
    breaker.allow(clock)
    breaker.success()
    emit("circuit-recovery", breaker.state.value)

    lifecycle = LifecycleController()
    lifecycle.transition(
        LifecyclePhase.ACCEPTING,
        reason="startup checks passed",
        timestamp_ms=clock.now_ms(),
    )
    evaluator = HealthEvaluator()
    ready = evaluator.evaluate(
        phase=lifecycle.phase,
        startup_complete=True,
        event_loop_progressing=True,
        components=[ComponentHealth("postgres", True, True)],
    )
    lifecycle.transition(
        LifecyclePhase.DRAINING,
        reason="termination requested",
        timestamp_ms=clock.now_ms(),
    )
    draining = evaluator.evaluate(
        phase=lifecycle.phase,
        startup_complete=True,
        event_loop_progressing=True,
        components=[ComponentHealth("postgres", True, True)],
    )
    emit(
        "lifecycle",
        {
            "accepting": {"live": ready.live, "ready": ready.ready},
            "draining": {"live": draining.live, "ready": draining.ready},
        },
    )

    registry = MetricRegistry()
    requests = registry.counter(
        MetricDescriptor(
            name="analysis_http_requests_total",
            description="Completed HTTP requests by bounded operation and outcome.",
            unit="requests",
            labels=("operation", "eligibility", "outcome"),
            max_series=30,
        )
    )
    latency = registry.histogram(
        MetricDescriptor(
            name="analysis_http_request_duration_seconds",
            description="Request duration by bounded operation.",
            unit="seconds",
            labels=("operation",),
            max_series=10,
        ),
        (0.05, 0.1, 0.25, 0.5, 1.0),
    )
    requests.add(labels={"operation": "getAnalysisRun", "eligibility": "eligible", "outcome": "good"})
    latency.observe(0.08, labels={"operation": "getAnalysisRun"})
    emit("metrics", registry.render_prometheus().splitlines()[:8])

    root = new_root(sampled=True)
    remote = parse_traceparent(root.traceparent())
    sink = InMemoryEventSink(maximum_events=2)
    logger = StructuredLogger(
        clock=clock,
        sink=sink,
        service_name="analysis-python",
        service_version="1.3.0",
        deployment_environment="course",
    )
    logger.emit(
        "analysis.request.completed",
        context=remote,
        attributes={"operation": "getAnalysisRun", "authorization": "Bearer secret"},
    )
    emit("telemetry", sink.events[0].to_dict())

    slo = SLODefinition("api-availability", 0.999, 28 * 24 * 3600)
    alert = BurnRateAlert("api-fast-burn", "page", 3600, 300, 14.4, 100)
    decision = evaluate_burn_rate_alert(
        slo,
        alert,
        long_window=SLOWindow(good=9_980, total=10_000),
        short_window=SLOWindow(good=980, total=1_000),
    )
    emit("slo-alert", decision)

    snapshot = Snapshot(
        runs=(RunRow("run-1", "completed"),),
        jobs=(JobRow("run-1", "completed"),),
        artifacts=(),
        outbox=(OutboxRow("run-1", "analysis.completed"),),
        events=(EventRow("run-1", "completed"),),
    )
    findings = inspect(snapshot)
    emit("read-only-reconciliation", finding_counts(findings))

    if not findings:
        raise SystemExit("expected the tour to detect the planted missing artifact")
    print("PASS capstone tour completed without external services")


if __name__ == "__main__":
    main()
