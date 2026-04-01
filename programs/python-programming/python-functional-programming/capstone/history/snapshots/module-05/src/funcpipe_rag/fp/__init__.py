"""Functional programming utilities for the end-of-Module-05 codebase.

This package groups two related layers:
- Module 02–03: small iterator/pipeline combinators and instrumentation helpers.
- Module 05: type-driven utilities (ADTs, functors, applicatives, monoids, etc.).

Module 02–03 helpers are re-exported at the package root for convenience.
Module 05 functionality is organized into submodules (e.g. `functor`,
`validation`, `monoid`).
"""

from .combinators import (
    FakeTime,
    StageInstrumentation,
    compose,
    ffilter,
    flatmap,
    flow,
    fmap,
    identity,
    instrument_stage,
    pipe,
    probe,
    producer_pipeline,
    tee,
)

__all__ = [
    "identity",
    "compose",
    "producer_pipeline",
    "flow",
    "pipe",
    "fmap",
    "ffilter",
    "flatmap",
    "tee",
    "probe",
    "StageInstrumentation",
    "instrument_stage",
    "FakeTime",
]

