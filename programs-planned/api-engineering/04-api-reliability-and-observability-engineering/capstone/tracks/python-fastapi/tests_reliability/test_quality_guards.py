from __future__ import annotations

import pytest

from api_reliability.faults import FaultPlan
from api_reliability.metrics import MetricDescriptor, MetricError
from api_reliability.slo import SLODefinition


def test_metric_profile_rejects_unique_identifier_labels() -> None:
    with pytest.raises(MetricError, match="forbidden identifier"):
        MetricDescriptor(
            name="analysis_run_events_total",
            description="Incorrect metric with one series per run.",
            unit="events",
            labels=("run_id",),
        )


def test_slo_definition_has_explicit_version_boundary() -> None:
    assert SLODefinition("api", 0.999, 60).version == "1.0"
    with pytest.raises(ValueError, match="version"):
        SLODefinition("api", 0.999, 60, version="")


def test_fault_plan_requires_hypothesis_and_cleanup() -> None:
    valid = FaultPlan(
        identifier="worker-loss",
        hypothesis="one expired lease is recovered without duplicate effects",
        steady_state=("one durable accepted run exists",),
        blast_radius="one synthetic run",
        abort_conditions=("duplicate terminal effect",),
        cleanup=("restore worker", "run reconciliation"),
    )
    valid.validate()

    invalid = FaultPlan(
        identifier="worker-loss",
        hypothesis="",
        steady_state=("one durable accepted run exists",),
        blast_radius="one synthetic run",
        abort_conditions=("duplicate terminal effect",),
        cleanup=("restore worker",),
    )
    with pytest.raises(ValueError, match="hypothesis"):
        invalid.validate()
