from __future__ import annotations

from funcpipe_rag.pipelines.distributed import BackendStatus
from funcpipe_rag.review.scaling import REQUIRED_SCALING_PROOFS, assess_scaling


def test_installed_package_does_not_imply_implemented_backend() -> None:
    status = BackendStatus(name="dask", installed=True, compiler_shipped=False)

    assessment = assess_scaling(status, REQUIRED_SCALING_PROOFS)

    assert assessment.implementation_ready is False
    assert assessment.runtime_ready is False


def test_implemented_backend_can_be_ready_before_local_installation() -> None:
    status = BackendStatus(name="beam", installed=False, compiler_shipped=True)

    assessment = assess_scaling(status, REQUIRED_SCALING_PROOFS)

    assert assessment.implementation_ready is True
    assert assessment.runtime_ready is False


def test_missing_semantic_proofs_block_implementation_readiness() -> None:
    status = BackendStatus(name="dask", installed=True, compiler_shipped=True)

    assessment = assess_scaling(status, frozenset({"ordering", "delivery"}))

    assert assessment.missing_proofs == ("backpressure", "failure")
    assert assessment.implementation_ready is False
