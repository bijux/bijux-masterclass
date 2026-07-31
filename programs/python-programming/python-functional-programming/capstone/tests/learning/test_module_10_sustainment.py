"""Executable learning proofs for the Module 10 sustainment workflow."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from funcpipe_rag.boundaries.shells.review_cli import build_summary, main
from funcpipe_rag.domain.effects.async_ import async_gather, async_pure
from funcpipe_rag.pipelines.distributed import BackendStatus
from funcpipe_rag.rag.domain import (
    Chunk,
    ChunkMetadata,
    ChunkMetadataV1,
    ChunkText,
    embedding_batches_equivalent,
    process_batch_hybrid,
    upcast_metadata_v1,
)
from funcpipe_rag.result.types import Ok
from funcpipe_rag.review.change import ChangeEvidence, review_change
from funcpipe_rag.review.evidence import EvidenceClaim, assess_evidence
from funcpipe_rag.review.migration import ContractShape, assess_migration
from funcpipe_rag.review.observability import (
    StageObservation,
    summarize_observations,
)
from funcpipe_rag.review.performance import (
    PerformanceBudget,
    PerformanceObservation,
    evaluate_budget,
)
from funcpipe_rag.review.scaling import REQUIRED_SCALING_PROOFS, assess_scaling

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


@given(
    values=st.lists(st.integers(), max_size=12),
    concurrency=st.integers(min_value=1, max_value=4),
)
def test_bounded_async_gather_preserves_input_order(
    values: list[int],
    concurrency: int,
) -> None:
    """Concurrency changes scheduling, not the ordered gather contract."""

    gathered = asyncio.run(
        async_gather(
            [async_pure(value) for value in values],
            concurrency=concurrency,
        )()
    )

    assert isinstance(gathered, Ok)
    assert gathered.value == values


def test_scaling_review_separates_installation_implementation_and_proof() -> None:
    """An importable library is not evidence that FuncPipe can compile to it."""

    installed_only = BackendStatus(
        name="dask",
        installed=True,
        compiler_shipped=False,
    )
    implemented_elsewhere = BackendStatus(
        name="beam",
        installed=False,
        compiler_shipped=True,
    )

    assert assess_scaling(
        installed_only,
        REQUIRED_SCALING_PROOFS,
    ).implementation_ready is False
    assessment = assess_scaling(implemented_elsewhere, REQUIRED_SCALING_PROOFS)
    assert assessment.implementation_ready is True
    assert assessment.runtime_ready is False


def test_package_groups_name_review_ownership_not_only_directories() -> None:
    """A change has an accountable review boundary even across nested packages."""

    summary = build_summary(PROJECT_ROOT)
    ownership = {
        group["name"]: group["owner"] for group in summary["package_groups"]
    }

    assert ownership == {
        "functional-core": "functional-foundations",
        "rag-model": "rag-domain",
        "orchestration-and-policy": "pipeline-runtime",
        "effect-boundaries": "boundary-integrations",
        "interop": "ecosystem-interop",
    }


def test_metadata_migration_pairs_shape_review_with_an_executable_upcaster() -> None:
    """Additive shape evidence is necessary, but the translator proves semantics."""

    previous = ContractShape(
        "chunk-metadata",
        frozenset({"source", "tags"}),
        frozenset({"source", "tags"}),
    )
    current = ContractShape(
        "chunk-metadata",
        frozenset({"source", "tags", "embedding_model", "expected_dim"}),
        frozenset({"source", "tags"}),
    )

    assessment = assess_migration(previous, current)
    migrated = upcast_metadata_v1(
        ChunkMetadataV1(source="manual", tags=["fp", "rag"])
    )

    assert assessment.compatibility == "backward-compatible"
    assert migrated == ChunkMetadata(source="manual", tags=("fp", "rag"))


def test_governance_claim_fails_closed_when_executable_evidence_is_missing() -> None:
    """A statement and source file are insufficient without the named proof."""

    claim = EvidenceClaim(
        name="ranking-law",
        statement="Ranking order remains stable after refactoring.",
        required_paths=("src/ranking.py", "tests/test_ranking.py"),
        command="pytest -q tests/test_ranking.py",
    )

    assessment = assess_evidence(claim, frozenset({"src/ranking.py"}))

    assert assessment.complete is False
    assert assessment.missing_paths == ("tests/test_ranking.py",)


def test_delivery_check_exposes_a_machine_readable_release_gate(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The endpoint exits successfully only when declared evidence is discoverable."""

    exit_code = main(
        ["check", "--format", "json", "--project-root", str(PROJECT_ROOT)]
    )

    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["evidence_claims"]
    assert all(claim["complete"] for claim in payload["evidence_claims"])


def test_change_review_composes_only_applicable_application_evidence() -> None:
    """The final decision combines proofs without pretending every check applies."""

    claim = EvidenceClaim(
        name="cleaning-fixed-point",
        statement="Repeated document cleaning reaches the same value.",
        required_paths=(
            "src/funcpipe_rag/rag/stages.py",
            "tests/unit/rag/test_stages.py",
        ),
        command="pytest -q tests/unit/rag/test_stages.py -k clean_doc_is_idempotent",
    )
    assessment = assess_evidence(claim, frozenset(claim.required_paths))
    budget = PerformanceBudget(80, 32, 25)
    observation = PerformanceObservation(60, 48, 30)

    decision = review_change(
        ChangeEvidence(
            semantic_equivalent=True,
            claims=(assessment,),
            budget=evaluate_budget(budget, observation),
        )
    )

    assert decision.acceptable is False
    assert decision.blockers == ("performance:peak_memory",)
