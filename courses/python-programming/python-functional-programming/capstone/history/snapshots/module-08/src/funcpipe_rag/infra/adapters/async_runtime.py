"""Module 08 infra: async runtime interpreter (shell-only)."""

from __future__ import annotations

from typing import TypeVar

from funcpipe_rag.domain.effects.async_.plan import AsyncPlan
from funcpipe_rag.result.types import ErrInfo, Result

A = TypeVar("A")


async def perform_async(plan: AsyncPlan[A]) -> Result[A, ErrInfo]:
    """Interpret an `AsyncPlan` by awaiting its coroutine."""

    return await plan()


__all__ = ["perform_async"]
