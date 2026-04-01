"""Configuration and dependency wiring for the end-of-Module-04 codebase.

The config-as-data and dependency-wiring patterns are introduced in Module 02
and extended in Module 03 with streaming entry points.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable, Iterator
from typing import Callable, Mapping, Protocol

from funcpipe_rag.api.clean_cfg import CleanConfig, DEFAULT_CLEAN_CONFIG, RULES, make_cleaner
from funcpipe_rag.api.types import DebugConfig, Observations, RagTaps
from funcpipe_rag.core.rules_pred import DEFAULT_RULES, RulesConfig
from funcpipe_rag.pipeline_stages import embed_chunk
from funcpipe_rag.rag_types import Chunk, ChunkWithoutEmbedding, CleanDoc, RagEnv, RawDoc
from funcpipe_rag.result import Err, Ok, Result


class Reader(Protocol):
    def read_docs(self, path: str) -> Result[list[RawDoc], str]: ...


@dataclass(frozen=True)
class RagConfig:
    env: RagEnv
    keep: RulesConfig = DEFAULT_RULES
    clean: CleanConfig = DEFAULT_CLEAN_CONFIG
    debug: DebugConfig = DebugConfig()


@dataclass(frozen=True)
class RagCoreDeps:
    cleaner: Callable[[RawDoc], CleanDoc]
    embedder: Callable[[ChunkWithoutEmbedding], Chunk]
    taps: RagTaps | None = None


@dataclass(frozen=True)
class RagBoundaryDeps:
    core: RagCoreDeps
    reader: Reader


def get_deps(config: RagConfig, *, taps: RagTaps | None = None) -> RagCoreDeps:
    cleaner = make_cleaner(config.clean)
    return RagCoreDeps(cleaner=cleaner, embedder=embed_chunk, taps=taps)


def make_rag_fn(
    *,
    chunk_size: int,
    clean_cfg: CleanConfig = DEFAULT_CLEAN_CONFIG,
    keep: RulesConfig = DEFAULT_RULES,
    debug: DebugConfig = DebugConfig(),
    taps: RagTaps | None = None,
) -> Callable[[list[RawDoc]], tuple[list[Chunk], Observations]]:
    """Pure configurator: capture immutable config into a reusable callable."""

    from funcpipe_rag.api.core import full_rag_api

    config = RagConfig(env=RagEnv(chunk_size), keep=keep, clean=clean_cfg, debug=debug)
    deps = get_deps(config, taps=taps)

    def run(docs: list[RawDoc]) -> tuple[list[Chunk], Observations]:
        return full_rag_api(docs, config, deps)

    return run


def make_gen_rag_fn(
    *,
    chunk_size: int,
    max_chunks: int = 10_000,
    clean_cfg: CleanConfig = DEFAULT_CLEAN_CONFIG,
    keep: RulesConfig = DEFAULT_RULES,
) -> Callable[[Iterable[RawDoc]], Iterator[ChunkWithoutEmbedding]]:
    """Pure configurator: build a streaming docs -> chunk stream function (Module 03)."""

    from funcpipe_rag.api.core import gen_bounded_chunks

    config = RagConfig(env=RagEnv(chunk_size), keep=keep, clean=clean_cfg)
    deps = get_deps(config)

    def run(docs: Iterable[RawDoc]) -> Iterator[ChunkWithoutEmbedding]:
        return gen_bounded_chunks(docs, config, deps, max_chunks=max_chunks)

    return run


def boundary_rag_config(raw: Mapping[str, object]) -> Result[RagConfig, str]:
    """Parse untyped boundary config into frozen RagConfig."""

    chunk_size_raw = raw.get("chunk_size", 512)
    if not isinstance(chunk_size_raw, int):
        return Err(f"Invalid config: chunk_size must be int (got {type(chunk_size_raw).__name__})")

    rule_names_raw = raw.get("clean_rules", DEFAULT_CLEAN_CONFIG.rule_names)
    if not isinstance(rule_names_raw, (tuple, list)) or not all(isinstance(x, str) for x in rule_names_raw):
        return Err("Invalid config: clean_rules must be list[str] or tuple[str, ...]")
    rule_names = tuple(rule_names_raw)
    missing = [name for name in rule_names if name not in RULES]
    if missing:
        available = ", ".join(sorted(RULES))
        return Err(f"Invalid config: unknown clean rule(s): {missing}; available: {available}")

    return Ok(RagConfig(env=RagEnv(chunk_size_raw), clean=CleanConfig(rule_names=rule_names)))


__all__ = [
    "Reader",
    "RagConfig",
    "RagCoreDeps",
    "RagBoundaryDeps",
    "get_deps",
    "make_rag_fn",
    "make_gen_rag_fn",
    "boundary_rag_config",
]
