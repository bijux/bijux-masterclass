"""Executable learning proofs for the Module 10 sustainment workflow."""

from __future__ import annotations

from pathlib import Path

from funcpipe_rag.boundaries.shells.review_cli import build_summary
from funcpipe_rag.rag.domain import (
    Chunk,
    ChunkMetadata,
    ChunkText,
    embedding_batches_equivalent,
    process_batch_hybrid,
)
from funcpipe_rag.review.observability import (
    StageObservation,
    summarize_observations,
)
from funcpipe_rag.review.performance import (
    PerformanceBudget,
    PerformanceObservation,
    evaluate_budget,
)
from hypothesis import given
from hypothesis import strategies as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_review_inventory_counts_nested_sources_once() -> None:
    """A refactor starts with a trustworthy observation, not an inflated metric."""

    summary = build_summary(PROJECT_ROOT)
    rag_group = next(
        group for group in summary["package_groups"] if group["name"] == "rag-model"
    )
    observed_files = {
        path.resolve()
        for relative in rag_group["paths"]
        for path in (PROJECT_ROOT / relative).rglob("*.py")
    }

    assert rag_group["python_file_count"] == len(observed_files)


def test_performance_budget_is_a_pure_multi_dimensional_decision() -> None:
    """A faster stage still fails review when it exceeds the memory contract."""

    budget = PerformanceBudget(
        max_latency_ms=80,
        max_peak_memory_mb=32,
        min_throughput_per_second=25,
    )
    observation = PerformanceObservation(
        latency_ms=60,
        peak_memory_mb=48,
        throughput_per_second=30,
    )

    decision = evaluate_budget(budget, observation)

    assert decision.within_budget is False
    assert decision.violations == ("peak_memory",)


def test_observability_is_data_that_does_not_change_pipeline_decisions() -> None:
    """Observation order and totals are reviewable without becoming control flow."""

    observations = (
        StageObservation("clean", processed=2, failures=0, latency_ms=1.0),
        StageObservation("chunk", processed=4, failures=1, latency_ms=2.0),
        StageObservation("embed", processed=3, failures=0, latency_ms=5.0),
    )

    summary = summarize_observations(observations)

    assert summary.stages == ("clean", "chunk", "embed")
    assert (summary.processed, summary.failures, summary.latency_ms) == (9, 1, 8.0)


@given(texts=st.lists(st.text(min_size=1, max_size=32), max_size=8))
def test_optimized_embedding_preserves_the_domain_contract(
    texts: list[str],
) -> None:
    """Generated examples compare semantics, not implementation identity."""

    batch = [
        Chunk(
            text=ChunkText(content=text),
            metadata=ChunkMetadata(
                source="learning",
                tags=(),
                embedding_model="local-hash",
            ),
        )
        for text in texts
    ]

    pure = process_batch_hybrid(batch, mode="pure")
    optimized = process_batch_hybrid(batch, mode="hybrid")

    assert embedding_batches_equivalent(pure, optimized)
