"""Lightweight, type-safe pipeline builder – a gentle introduction to function composition.

This module defines ``RagPipe``, a tiny wrapper that shows how objects can be used
to make functional composition feel more fluent while preserving full static typing.

It is deliberately minimal: no magic, no dunder abuse beyond ``__call__`` and ``then``.
Students should see this and immediately understand it is just syntactic sugar
over ordinary function composition.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class RagPipe(Generic[A, B]):
    """Chainable wrapper that turns ordinary callables into a fluent pipeline.

    Usage example (exactly what students will write in later cores)::

        pipeline = (
            RagPipe(clean_docs)
                .then(chunk_docs(env))
                .then(embed_chunks)
                .then(dedup_chunks)
        )
        final_chunks: list[Chunk] = pipeline(raw_docs)
    """

    def __init__(self, stage: Callable[[A], B]):
        """Wrap a single pure transformation stage.

        Args:
            stage: Any callable that takes a value of type ``A`` and returns ``B``.
                   It must be pure (no side effects) for the whole pipeline to stay pure.
        """
        self._stage = stage

    def __call__(self, value: A) -> B:
        """Execute the wrapped stage."""
        return self._stage(value)

    def then(self, next_stage: Callable[[B], C]) -> "RagPipe[A, C]":
        """Compose a new stage after the current one.

        This is ordinary function composition expressed as a method chain.

        Args:
            next_stage: Pure function that consumes the output of the current stage.

        Returns:
            A new ``RagPipe`` representing the combined transformation.
        """
        # λx. next_stage(current_stage(x))
        return RagPipe(lambda x: next_stage(self._stage(x)))

    # --------------------------------------------------------------------- #
    # Optional convenience – not required for Module 01 but nice to have
    # --------------------------------------------------------------------- #

    def __or__(self, next_stage: Callable[[B], C]) -> "RagPipe[A, C]":
        """Allow pipe operator syntax: ``pipeline | next_stage``."""
        return self.then(next_stage)

    def __repr__(self) -> str:
        name = getattr(self._stage, "__name__", "lambda")
        return f"<RagPipe {name}>"
