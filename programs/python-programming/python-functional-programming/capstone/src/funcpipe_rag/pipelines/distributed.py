"""Module 09 Core 7: optional distributed compilation seam (end-of-Module-09).

The repository's default proof route is local and does not ship a Dask or Beam
backend. This module exists only as the attachment point for an explicitly added
distributed compiler that preserves the same pipeline contracts.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class BackendStatus:
    name: Literal["dask", "beam"]
    installed: bool
    compiler_shipped: bool = False


def dask_available() -> bool:
    try:
        importlib.import_module("dask")
        importlib.import_module("dask.bag")
        return True
    except ImportError:
        return False


def beam_available() -> bool:
    try:
        importlib.import_module("apache_beam")
        return True
    except ImportError:
        return False


def backend_statuses() -> tuple[BackendStatus, ...]:
    """Report installation separately from the repository's implementation claim."""

    return (
        BackendStatus(name="dask", installed=dask_available()),
        BackendStatus(name="beam", installed=beam_available()),
    )


def compile_to_dask_bag(*_args: Any, **_kwargs: Any) -> Any:
    """Documented Dask attachment point; no backend ships in the default repo."""

    if not dask_available():
        raise ImportError("dask is not available")
    raise NotImplementedError("Dask is an optional extension seam here; no Dask backend ships in the default repository")


def compile_to_beam(*_args: Any, **_kwargs: Any) -> Any:
    """Documented Beam attachment point; no backend ships in the default repo."""

    if not beam_available():
        raise ImportError("apache-beam is not available")
    raise NotImplementedError("Apache Beam is an optional extension seam here; no Beam backend ships in the default repository")


__all__ = [
    "BackendStatus",
    "backend_statuses",
    "beam_available",
    "compile_to_beam",
    "compile_to_dask_bag",
    "dask_available",
]
