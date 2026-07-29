"""Module 09: pipeline building and cross-process specs (end-of-Module-09)."""

from .configured import PipelineConfig, StepConfig, build_rag_pipeline
from .distributed import (
    BackendStatus,
    backend_statuses,
    beam_available,
    compile_to_beam,
    compile_to_dask_bag,
    dask_available,
)
from .specs import (
    ErrorPolicy,
    OperatorSpec,
    PipelineSpec,
    SpecRegistry,
    canonical_json,
    reconstruct_pipeline,
    spec_hash,
)

__all__ = [
    "BackendStatus",
    "ErrorPolicy",
    "OperatorSpec",
    "PipelineConfig",
    "PipelineSpec",
    "SpecRegistry",
    "StepConfig",
    "backend_statuses",
    "beam_available",
    "build_rag_pipeline",
    "canonical_json",
    "compile_to_beam",
    "compile_to_dask_bag",
    "dask_available",
    "reconstruct_pipeline",
    "spec_hash",
]
