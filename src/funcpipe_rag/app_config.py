"""Application-level config for the end-of-Module-03 shells.

The thin CLI/boundary pattern was introduced in M02C10 and remains the
recommended way to keep I/O at the edges.
"""

from __future__ import annotations

from dataclasses import dataclass

from funcpipe_rag.api.config import RagConfig


@dataclass(frozen=True)
class AppConfig:
    input_path: str
    output_path: str
    rag: RagConfig


__all__ = ["AppConfig"]
