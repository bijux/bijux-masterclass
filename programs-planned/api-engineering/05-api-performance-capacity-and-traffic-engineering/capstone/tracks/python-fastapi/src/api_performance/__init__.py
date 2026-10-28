"""Course 5 performance engineering mechanisms.

The package is intentionally dependency-light. Framework and PostgreSQL adapters
live at the edges; core arithmetic and policy remain independently testable.
"""

from .models import BenchmarkEnvelope, CorrectnessReport, EnvironmentFingerprint, WorkloadSpec
from .statistics import SampleSummary, nearest_rank, summarize

__all__ = [
    "BenchmarkEnvelope",
    "CorrectnessReport",
    "EnvironmentFingerprint",
    "WorkloadSpec",
    "SampleSummary",
    "nearest_rank",
    "summarize",
]
