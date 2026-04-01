"""Application-level config for Module 02 shells (M02C10)."""

from __future__ import annotations

from dataclasses import dataclass

from funcpipe_rag.api.config import RagConfig


@dataclass(frozen=True)
class AppConfig:
    input_path: str
    output_path: str
    rag: RagConfig


__all__ = ["AppConfig"]

