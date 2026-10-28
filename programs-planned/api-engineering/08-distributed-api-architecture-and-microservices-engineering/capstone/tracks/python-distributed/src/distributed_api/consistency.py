from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .model import ValidationError


@dataclass
class ProjectionEntry:
    version: int
    value: Any
    updated_at_ms: int


class VersionedProjection:
    def __init__(self) -> None:
        self._items: dict[str, ProjectionEntry] = {}
        self._gaps: dict[str, tuple[int, int]] = {}

    def apply(self, key: str, version: int, value: Any, *, now_ms: int) -> str:
        if version <= 0:
            raise ValidationError("version must be positive")
        current = self._items.get(key)
        if current is None:
            if version != 1:
                self._gaps[key] = (0, version)
                return "gap"
            self._items[key] = ProjectionEntry(version, value, now_ms)
            return "apply"
        if version == current.version:
            return "duplicate"
        if version < current.version:
            return "stale"
        if version > current.version + 1:
            self._gaps[key] = (current.version, version)
            return "gap"
        self._items[key] = ProjectionEntry(version, value, now_ms)
        self._gaps.pop(key, None)
        return "apply"

    def get(self, key: str, *, now_ms: int, max_staleness_ms: int) -> Any:
        if key in self._gaps:
            raise ValidationError(f"projection has unresolved gap: {key}")
        entry = self._items[key]
        if now_ms - entry.updated_at_ms > max_staleness_ms:
            raise ValidationError(f"projection stale: {key}")
        return entry.value

    def version(self, key: str) -> int:
        return self._items[key].version

    def gaps(self) -> dict[str, tuple[int, int]]:
        return dict(self._gaps)
