from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ServiceError(Exception):
    status: int
    title: str
    detail: str
    code: str
    errors: list[dict[str, Any]] | None = None
    public: bool = True

    def __str__(self) -> str:
        return self.detail


class LeaseLost(RuntimeError):
    """A stale worker mutated state after its lease generation changed."""
