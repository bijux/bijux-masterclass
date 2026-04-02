"""Application-level boundary config (end-of-Module-07)."""

from __future__ import annotations

from dataclasses import dataclass

from funcpipe_rag.rag.config import RagConfig


@dataclass(frozen=True)
class AppConfig:
    input_path: str
    output_path: str
    rag: RagConfig


__all__ = ["AppConfig"]
