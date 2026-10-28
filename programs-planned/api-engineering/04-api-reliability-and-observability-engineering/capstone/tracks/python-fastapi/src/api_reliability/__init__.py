"""Reliability and observability primitives for the Analysis Runs service.

The dependency-light core is intentionally independent of FastAPI, PostgreSQL,
and OpenTelemetry packages. Framework and SDK adapters live in separate modules.
"""

from .alerts import BurnRateAlert, evaluate_burn_rate_alert
from .circuit import CircuitBreaker, CircuitState
from .clock import ManualClock, SystemClock
from .context import TraceContext, parse_traceparent
from .deadline import Deadline, DeadlineExceeded
from .health import ComponentHealth, HealthEvaluator, LifecyclePhase
from .metrics import MetricRegistry
from .retry import RetryPolicy, RetrySafety, plan_retry_delays
from .slo import SLODefinition, SLOWindow

__all__ = [
    "BurnRateAlert",
    "CircuitBreaker",
    "CircuitState",
    "ComponentHealth",
    "Deadline",
    "DeadlineExceeded",
    "HealthEvaluator",
    "LifecyclePhase",
    "ManualClock",
    "MetricRegistry",
    "RetryPolicy",
    "RetrySafety",
    "SLODefinition",
    "SLOWindow",
    "SystemClock",
    "TraceContext",
    "evaluate_burn_rate_alert",
    "parse_traceparent",
    "plan_retry_delays",
]
