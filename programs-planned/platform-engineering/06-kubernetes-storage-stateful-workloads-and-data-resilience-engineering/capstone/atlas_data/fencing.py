from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FenceToken:
    resource: str
    generation: int


class FenceRegistry:
    def __init__(self):
        self._generation: dict[str, int] = {}
        self._data: dict[str, dict[str, str]] = {}

    def acquire(self, resource: str) -> FenceToken:
        generation = self._generation.get(resource, 0) + 1
        self._generation[resource] = generation
        self._data.setdefault(resource, {})
        return FenceToken(resource, generation)

    def write(self, resource: str, token: FenceToken, key: str, value: str) -> None:
        current = self._generation.get(resource)
        if token.resource != resource or token.generation != current:
            raise PermissionError("stale writer generation")
        self._data[resource][key] = value

    def read(self, resource: str, key: str) -> str | None:
        return self._data.get(resource, {}).get(key)

    def generation(self, resource: str) -> int:
        return self._generation.get(resource, 0)
