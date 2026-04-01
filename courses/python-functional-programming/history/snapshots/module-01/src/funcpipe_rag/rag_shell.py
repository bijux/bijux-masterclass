"""Impure shell and dependency-injection environment for the FuncPipe RAG pipeline.

This is the *only* place in the entire codebase where side effects are allowed:
- File I/O
- Logging
- Accessing the clock
- Random seeding (for future reproducibility)

Everything else remains pure and referentially transparent.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Callable

from funcpipe_rag.full_rag import full_rag
from funcpipe_rag.rag_types import Chunk, RagEnv, RawDoc


# --------------------------------------------------------------------------- #
# Dependency environments – explicit, immutable, injectable
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class LogEnv:
    """Where log messages go. Pure functions can’t print – they return logs."""
    log: Callable[[str], None]


@dataclass(frozen=True)
class TimeEnv:
    """Provides the current time. Makes timestamp-dependent logic testable."""
    now: Callable[[], datetime]


@dataclass(frozen=True)
class RandEnv:
    """Reproducible randomness source (used only by future pure stages)."""
    seed: int


@dataclass(frozen=True)
class RagCoreEnv:
    """Bundle of all external dependencies required by a context-aware pipeline."""
    log_env: LogEnv
    time_env: TimeEnv
    rand_env: RandEnv


# --------------------------------------------------------------------------- #
# Context-aware shell (pure core + side effects via env)
# --------------------------------------------------------------------------- #

def full_rag_shell(
    env: RagCoreEnv,
    docs: list[RawDoc],
    rag_env: RagEnv,
) -> tuple[Chunk, ...]:
    """Execute a *pure* pipeline that may emit logs, using injected dependencies.

    This function is still referentially transparent when the environment is fixed.
    It is only here to demonstrate how to wire a pure core with external capabilities
    without polluting the core with globals or print statements.
    """
    # NOTE: At the end of Module 01 we do not yet have a pure pipeline that
    # accumulates logs. Later modules will introduce a variant that returns
    # (chunks, logs) instead of printing. For now this shell simply delegates
    # to the pure `full_rag` and ignores the injected env.
    _ = env  # future-proofing – env will be used later
    return tuple(full_rag(docs, rag_env))


# --------------------------------------------------------------------------- #
# Classic imperative shell – the single allowed impure entry point
# --------------------------------------------------------------------------- #

def rag_shell(env: RagEnv, input_path: str, output_path: str) -> None:
    """Read CSV → run pure RAG pipeline → write JSONL.

    This is the *only* function in the entire package that performs I/O.
    Everything else is pure and can be tested in isolation.

    Args:
        env: Configuration controlling chunk size.
        input_path: Path to a UTF-8 encoded CSV with columns matching ``RawDoc``.
        output_path: Destination file; one JSON object per line (JSONL).

    Raises:
        ValueError: If the CSV cannot be parsed into ``RawDoc`` instances.
    """
    # ---- Load raw documents -------------------------------------------------
    try:
        with open(input_path, encoding="utf-8") as f_in:
            reader = csv.DictReader(f_in)
            docs = [RawDoc(**row) for row in reader]
    except (UnicodeDecodeError, csv.Error, TypeError, ValueError) as exc:
        raise ValueError(f"Failed to read or parse CSV file '{input_path}': {exc}") from exc

    # ---- Run the pure pipeline ---------------------------------------------
    chunks = full_rag(docs, env)

    # ---- Write results -------------------------------------------------------
    with open(output_path, "w", encoding="utf-8") as f_out:
        for chunk in chunks:
            json.dump(asdict(chunk), f_out, ensure_ascii=False)
            f_out.write("\n")