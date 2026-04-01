"""CSV-in / JSONL-out boundary shell for the Module-02 API."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from typing import Iterable

from funcpipe_rag.api.config import RagBoundaryDeps, RagConfig, Reader, get_deps
from funcpipe_rag.api.core import full_rag_api
from funcpipe_rag.api.types import Observations
from funcpipe_rag.rag_types import Chunk, RawDoc
from funcpipe_rag.result import Err, Ok, Result


class FSReader(Reader):
    """Filesystem reader implementation (impure)."""

    def read_docs(self, path: str) -> Result[list[RawDoc]]:
        try:
            with open(path, encoding="utf-8") as f_in:
                reader = csv.DictReader(f_in)
                return Ok([RawDoc(**row) for row in reader])
        except (OSError, csv.Error, TypeError, ValueError) as exc:
            return Err(f"Load failed: {exc}")


def write_chunks_jsonl(path: str, chunks: Iterable[Chunk]) -> Result[None]:
    try:
        with open(path, "w", encoding="utf-8") as f_out:
            for chunk in chunks:
                json.dump(asdict(chunk), f_out, ensure_ascii=False)
                f_out.write("\n")
        return Ok(None)
    except OSError as exc:
        return Err(f"Write failed: {exc}")


def run(input_path: str, output_path: str, *, config: RagConfig) -> Result[Observations]:
    """Effectful boundary: read docs, run pure core, write chunks."""

    reader = FSReader()
    deps = RagBoundaryDeps(core=get_deps(config), reader=reader)
    docs_res = deps.reader.read_docs(input_path)
    if isinstance(docs_res, Err):
        return docs_res
    chunks, obs = full_rag_api(docs_res.value, config, deps.core)
    write_res = write_chunks_jsonl(output_path, chunks)
    if isinstance(write_res, Err):
        return write_res
    return Ok(obs)


__all__ = ["FSReader", "write_chunks_jsonl", "run"]

