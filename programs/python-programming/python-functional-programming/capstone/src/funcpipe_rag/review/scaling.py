"""Pure readiness decisions for optional distributed execution."""

from __future__ import annotations

from dataclasses import dataclass

from funcpipe_rag.pipelines.distributed import BackendStatus

REQUIRED_SCALING_PROOFS: frozenset[str] = frozenset(
    {
        "backpressure",
        "delivery",
        "failure",
        "ordering",
    }
)


@dataclass(frozen=True, slots=True)
class ScalingAssessment:
    implementation_ready: bool
    runtime_ready: bool
    missing_proofs: tuple[str, ...]


def assess_scaling(
    status: BackendStatus,
    verified_proofs: frozenset[str],
) -> ScalingAssessment:
    """Separate implemented semantics from local package availability."""

    missing = tuple(sorted(REQUIRED_SCALING_PROOFS - verified_proofs))
    implementation_ready = status.compiler_shipped and not missing
    return ScalingAssessment(
        implementation_ready=implementation_ready,
        runtime_ready=implementation_ready and status.installed,
        missing_proofs=missing,
    )
