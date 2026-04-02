"""Module 09 Core 7: optional distributed compilation scaffolding (end-of-Module-09).

This module intentionally keeps hard dependencies optional. It provides a place
to host Dask/Beam compilers when those libraries are installed.
"""

from __future__ import annotations

import importlib
from typing import Any


def dask_available() -> bool:
    try:
        importlib.import_module("dask")
        importlib.import_module("dask.bag")
        return True
    except Exception:
        return False


def beam_available() -> bool:
    try:
        importlib.import_module("apache_beam")
        return True
    except Exception:
        return False


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


__all__ = ["dask_available", "beam_available", "compile_to_dask_bag", "compile_to_beam"]
