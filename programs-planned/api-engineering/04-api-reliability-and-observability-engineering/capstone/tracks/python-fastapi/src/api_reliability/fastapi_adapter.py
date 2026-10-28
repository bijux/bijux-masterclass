"""FastAPI integration for the dependency-light reliability profile.

The adapter preserves the public OpenAPI surface: all operational endpoints are
hidden from schema generation and use a separate ``/internal`` namespace.
"""
from __future__ import annotations

from dataclasses import dataclass
import inspect
import time
from typing import Any, Awaitable, Callable

from fastapi.responses import JSONResponse, PlainTextResponse

from .clock import SystemClock
from .context import TraceContextError, new_root, parse_traceparent
from .http import classify_http_outcome
from .health import (
    ComponentHealth,
    HealthEvaluator,
    LifecycleController,
    LifecyclePhase,
)
from .metrics import Counter, Gauge, Histogram, MetricDescriptor, MetricRegistry
from .telemetry import InMemoryEventSink, StructuredLogger

ReadinessCheck = Callable[[], None | Awaitable[None]]


@dataclass(slots=True)
class ReliabilityRuntime:
    lifecycle: LifecycleController
    registry: MetricRegistry
    events: InMemoryEventSink
    logger: StructuredLogger
    requests: Counter
    duration: Histogram
    active_requests: Gauge
    telemetry_dropped: Counter
    run_starts: Counter
    oldest_queue_age: Gauge
    _reported_drops: int = 0

    def begin_drain(self, *, reason: str = "shutdown-requested") -> None:
        if self.lifecycle.phase in {
            LifecyclePhase.STARTING,
            LifecyclePhase.ACCEPTING,
        }:
            self.lifecycle.transition(
                LifecyclePhase.DRAINING,
                reason=reason,
                timestamp_ms=int(time.time() * 1_000),
            )

    def record_run_start(self, *, within_objective: bool) -> None:
        self.run_starts.add(
            labels={"outcome": "good" if within_objective else "bad"}
        )

    def set_oldest_queue_age(self, seconds: float) -> None:
        self.oldest_queue_age.set(max(0.0, seconds))

    def account_for_drops(self) -> None:
        delta = self.events.dropped - self._reported_drops
        if delta > 0:
            self.telemetry_dropped.add(delta)
            self._reported_drops = self.events.dropped


def install_reliability(
    app: Any,
    *,
    lifecycle: LifecycleController,
    readiness_check: ReadinessCheck,
    service_name: str,
    service_version: str,
    environment: str,
) -> ReliabilityRuntime:
    clock = SystemClock()
    sink = InMemoryEventSink(maximum_events=10_000)
    logger = StructuredLogger(
        clock=clock,
        sink=sink,
        service_name=service_name,
        service_version=service_version,
        deployment_environment=environment,
        schema_version="1.0",
    )
    registry = MetricRegistry()
    requests = registry.counter(
        MetricDescriptor(
            name="analysis_http_server_requests_total",
            description="Completed HTTP requests classified for the availability SLI",
            unit="{request}",
            labels=("operation", "eligibility", "outcome", "status_class"),
            max_series=800,
        )
    )
    duration = registry.histogram(
        MetricDescriptor(
            name="analysis_http_server_duration_seconds",
            description="HTTP server request duration by stable operation identifier",
            unit="s",
            labels=("operation",),
            max_series=64,
        ),
        (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
    )
    active_requests = registry.gauge(
        MetricDescriptor(
            name="analysis_http_server_active_requests",
            description="Requests currently executing inside the application",
            unit="{request}",
        )
    )
    telemetry_dropped = registry.counter(
        MetricDescriptor(
            name="analysis_telemetry_dropped_total",
            description="Structured operational events dropped by the bounded local sink",
            unit="{event}",
        )
    )
    run_starts = registry.counter(
        MetricDescriptor(
            name="analysis_run_start_total",
            description="Accepted runs classified against the run-start objective",
            unit="{run}",
            labels=("outcome",),
            max_series=2,
        )
    )
    oldest_queue_age = registry.gauge(
        MetricDescriptor(
            name="analysis_worker_oldest_queued_age_seconds",
            description="Age in seconds of the oldest runnable queued job",
            unit="s",
        )
    )
    runtime = ReliabilityRuntime(
        lifecycle=lifecycle,
        registry=registry,
        events=sink,
        logger=logger,
        requests=requests,
        duration=duration,
        active_requests=active_requests,
        telemetry_dropped=telemetry_dropped,
        run_starts=run_starts,
        oldest_queue_age=oldest_queue_age,
    )

    active = 0

    @app.middleware("http")
    async def reliability_middleware(request: Any, call_next: Any) -> Any:
        nonlocal active
        received = request.headers.get("traceparent")
        try:
            parent = parse_traceparent(received) if received else new_root(sampled=False)
        except TraceContextError:
            parent = new_root(sampled=False)
            logger.emit(
                "http.trace_context.rejected",
                severity="WARN",
                attributes={"reason": "invalid-traceparent"},
            )
        context = parent.child()
        request.state.trace_context = context
        active += 1
        active_requests.set(float(active))
        started = time.perf_counter()
        response = None
        status = 500
        try:
            response = await call_next(request)
            status = int(response.status_code)
            response.headers["traceparent"] = context.traceparent()
            return response
        finally:
            elapsed = time.perf_counter() - started
            operation = _operation_id(request)
            classification = classify_http_outcome(operation, status)
            eligibility = classification.eligibility
            outcome = classification.outcome
            requests.add(
                labels={
                    "operation": operation,
                    "eligibility": eligibility,
                    "outcome": outcome,
                    "status_class": f"{status // 100}xx",
                }
            )
            duration.observe(elapsed, labels={"operation": operation})
            logger.emit(
                "http.server.request.completed",
                severity="ERROR" if status >= 500 else "INFO",
                context=context,
                attributes={
                    "http.request.method": request.method,
                    "http.route.operation_id": operation,
                    "http.response.status_code": status,
                    "sli.eligibility": eligibility,
                    "sli.outcome": outcome,
                    "duration_ms": round(elapsed * 1_000, 3),
                },
            )
            active -= 1
            active_requests.set(float(active))
            runtime.account_for_drops()

    @app.get(
        "/internal/health/live",
        include_in_schema=False,
        name="internalHealthLive",
    )
    async def internal_liveness() -> JSONResponse:
        snapshot = HealthEvaluator().evaluate(
            phase=lifecycle.phase,
            startup_complete=lifecycle.phase is not LifecyclePhase.STARTING,
            event_loop_progressing=True,
            components=[],
        )
        return JSONResponse(
            status_code=200 if snapshot.live else 503,
            content=_health_payload(snapshot),
        )

    @app.get(
        "/internal/health/ready",
        include_in_schema=False,
        name="internalHealthReady",
    )
    async def internal_readiness() -> JSONResponse:
        available = True
        detail = "available"
        try:
            result = readiness_check()
            if inspect.isawaitable(result):
                await result
        except Exception as error:  # readiness converts dependency failure to evidence
            available = False
            detail = type(error).__name__
        snapshot = HealthEvaluator().evaluate(
            phase=lifecycle.phase,
            startup_complete=lifecycle.phase is not LifecyclePhase.STARTING,
            event_loop_progressing=True,
            components=[
                ComponentHealth(
                    name="postgresql",
                    required_for_readiness=True,
                    available=available,
                    detail=detail,
                )
            ],
        )
        return JSONResponse(
            status_code=200 if snapshot.ready else 503,
            content=_health_payload(snapshot),
        )

    @app.get(
        "/internal/metrics",
        include_in_schema=False,
        name="internalMetrics",
    )
    async def internal_metrics() -> PlainTextResponse:
        runtime.account_for_drops()
        return PlainTextResponse(
            registry.render_prometheus(),
            media_type="application/openmetrics-text; version=1.0.0; charset=utf-8",
        )

    app.state.reliability = runtime
    return runtime


def _operation_id(request: Any) -> str:
    route = request.scope.get("route")
    value = getattr(route, "operation_id", None) or getattr(route, "name", None)
    if isinstance(value, str) and value:
        return value
    return "unmatched"



def _health_payload(snapshot: Any) -> dict[str, Any]:
    return {
        "live": snapshot.live,
        "ready": snapshot.ready,
        "startupComplete": snapshot.startup_complete,
        "phase": snapshot.phase.value,
        "reasons": list(snapshot.reasons),
    }
