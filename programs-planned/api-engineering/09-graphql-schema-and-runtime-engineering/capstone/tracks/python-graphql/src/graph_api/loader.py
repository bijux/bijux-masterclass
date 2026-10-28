from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable); V = TypeVar("V")

@dataclass
class LoadToken(Generic[V]):
    value: V | None = None
    ready: bool = False

    def get(self) -> V | None:
        if not self.ready: raise RuntimeError("loader has not been dispatched")
        return self.value

class BatchLoader(Generic[K, V]):
    """Request-scoped batching primitive with duplicate-key collapse."""
    def __init__(self, batch: Callable[[list[K]], dict[K, V]]) -> None:
        self._batch = batch; self._tokens: dict[K, LoadToken[V]] = {}; self.dispatches = 0

    def load(self, key: K) -> LoadToken[V]:
        if key not in self._tokens: self._tokens[key] = LoadToken()
        return self._tokens[key]

    def dispatch(self) -> None:
        pending = [key for key, token in self._tokens.items() if not token.ready]
        if not pending: return
        values = self._batch(pending); self.dispatches += 1
        for key in pending:
            token = self._tokens[key]; token.value = values.get(key); token.ready = True

    @property
    def key_count(self) -> int: return len(self._tokens)
