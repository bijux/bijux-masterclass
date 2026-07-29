"""Impure shell for the FuncPipe RAG pipeline.

This is the *only* place in the entire codebase where side effects are allowed:
- File I/O

Everything else remains pure and referentially transparent.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict

from funcpipe_rag.full_rag import full_rag
from funcpipe_rag.rag_types import RagEnv, RawDoc


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
