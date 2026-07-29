from __future__ import annotations

import pytest
from funcpipe_rag.review.observability import (
    ObservationSummary,
    StageObservation,
    summarize_observations,
)


def test_summarize_observations_preserves_stage_order() -> None:
    observations = (
        StageObservation("clean", processed=3, failures=0, latency_ms=1.5),
        StageObservation("chunk", processed=5, failures=1, latency_ms=2.5),
    )

    assert summarize_observations(observations) == ObservationSummary(
        processed=8,
        failures=1,
        latency_ms=4.0,
        stages=("clean", "chunk"),
    )


def test_empty_observations_have_an_identity_summary() -> None:
    assert summarize_observations(()) == ObservationSummary(0, 0, 0.0, ())


def test_stage_observation_rejects_impossible_counts() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        StageObservation("embed", processed=1, failures=2, latency_ms=1)
