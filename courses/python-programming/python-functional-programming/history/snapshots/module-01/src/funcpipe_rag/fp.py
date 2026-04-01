"""Minimal functional helpers – Module 01 scope only.

This module is intentionally small and only exposes the core ideas used in
Module 01:

- Functions as first-class values
- Simple higher-order functions
- Left-to-right function composition
- Mapping over lists (List as a functor)

Deliberately *not* included here (introduced in later modules):
- ParamSpec / Concatenate type plumbing
- Context injection and decorators
- foldl / ffilter / iterator folds
- Pipeline abstractions and effectful helpers
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def identity(x: A) -> A:
    """Identity function: returns its input unchanged.

    Useful for functor law checks and as a default no-op callback.
    """
    return x


def flow(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose unary functions left-to-right into a single callable.

    Evaluates as:
        flow(f1, f2, f3)(x) == f3(f2(f1(x)))

    Example:
        pipeline = flow(clean_docs, chunk_docs(env), embed_chunks, dedup)
        result = pipeline(docs)
    """

    def composed(x: Any) -> Any:
        result = x
        for f in functions:
            result = f(result)
        return result

    return composed


def fmap(func: Callable[[A], B]) -> Callable[[Iterable[A]], list[B]]:
    """Lift a pure function over a list (List functor).

    Given a function A -> B, produce a function [A] -> [B].

    Functor laws (checked in tests):
        fmap(identity) == identity
        fmap(g ∘ f) == fmap(g) ∘ fmap(f)
    """

    def mapped(items: Iterable[A]) -> list[B]:
        return [func(item) for item in items]

    return mapped


# Omitted on purpose (introduced in later modules):
# - pipe(...)           → Module 02 (data-first style)
# - ffilter, foldl      → Module 03+ (iterator / fold patterns)
# - Pipeline class      → rag_pipe.RagPipe (OO alternative)
# - log_calls           → Module 07 (effects / tracing)
# - with_context        → Module 06 (Reader-like context passing)
