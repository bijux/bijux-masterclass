"""Module 09 Core 7: optional distributed compilation scaffolding (end-of-Module-09).

This module intentionally keeps hard dependencies optional. It provides a place
to host Dask/Beam compilers when those libraries are installed.
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
    """Extension seam stub for a Dask compiler (requires dask.bag installed)."""

    if not dask_available():
        raise ImportError("dask is not available")
    raise NotImplementedError("Dask compiler seam is documented, but no Dask backend ships in the default repo")


def compile_to_beam(*_args: Any, **_kwargs: Any) -> Any:
    """Extension seam stub for an Apache Beam compiler (requires apache-beam installed)."""

    if not beam_available():
        raise ImportError("apache-beam is not available")
    raise NotImplementedError("Beam compiler seam is documented, but no Beam backend ships in the default repo")


__all__ = [
    "BackendStatus",
    "backend_statuses",
    "beam_available",
    "compile_to_beam",
    "compile_to_dask_bag",
    "dask_available",
]
