"""Bounded authorization-aware cache with injected time."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


def _length_prefix(value: str) -> str:
    return f"{len(value)}:{value}"


@dataclass(frozen=True, slots=True)
class AuthorizedCacheKey:
    tenant_id: str
    policy_partition: str
    resource_type: str
    resource_id: str
    version: str
    representation: str

    def __post_init__(self) -> None:
        if any(
            not value
            for value in (
                self.tenant_id,
                self.policy_partition,
                self.resource_type,
                self.resource_id,
                self.version,
                self.representation,
            )
        ):
            raise ValueError("cache key fields must be non-empty")

    @property
    def canonical(self) -> str:
        return "|".join(
            _length_prefix(value)
            for value in (
                self.tenant_id,
                self.policy_partition,
                self.resource_type,
                self.resource_id,
                self.version,
                self.representation,
            )
        )


@dataclass(frozen=True, slots=True)
class CacheEntry(Generic[T]):
    value: T
    expires_at_ns: int
    size_bytes: int
    classification: str


@dataclass(frozen=True, slots=True)
class CacheLookup(Generic[T]):
    state: str
    value: T | None


@dataclass(frozen=True, slots=True)
class CacheSnapshot:
    entries: int
    estimated_bytes: int
    hits: int
    misses: int
    stale: int
    evictions: int


class BoundedTTLCache(Generic[T]):
    def __init__(self, *, max_entries: int, max_bytes: int) -> None:
        if max_entries <= 0 or max_bytes <= 0:
            raise ValueError("cache bounds must be positive")
        self._max_entries = max_entries
        self._max_bytes = max_bytes
        self._entries: OrderedDict[str, CacheEntry[T]] = OrderedDict()
        self._bytes = 0
        self._hits = 0
        self._misses = 0
        self._stale = 0
        self._evictions = 0

    def get(self, key: AuthorizedCacheKey, *, now_ns: int) -> CacheLookup[T]:
        canonical = key.canonical
        entry = self._entries.get(canonical)
        if entry is None:
            self._misses += 1
            return CacheLookup("miss", None)
        if now_ns >= entry.expires_at_ns:
            self._entries.pop(canonical)
            self._bytes -= entry.size_bytes
            self._stale += 1
            return CacheLookup("stale", None)
        self._entries.move_to_end(canonical)
        self._hits += 1
        return CacheLookup("hit", entry.value)

    def put(
        self,
        key: AuthorizedCacheKey,
        value: T,
        *,
        now_ns: int,
        ttl_ns: int,
        size_bytes: int,
        classification: str = "positive",
    ) -> None:
        if ttl_ns <= 0 or size_bytes < 0:
            raise ValueError("invalid cache entry bounds")
        if classification not in {"positive", "negative"}:
            raise ValueError("invalid cache classification")
        canonical = key.canonical
        existing = self._entries.pop(canonical, None)
        if existing is not None:
            self._bytes -= existing.size_bytes
        if size_bytes > self._max_bytes:
            return
        entry = CacheEntry(
            value=value,
            expires_at_ns=now_ns + ttl_ns,
            size_bytes=size_bytes,
            classification=classification,
        )
        self._entries[canonical] = entry
        self._bytes += size_bytes
        while (
            len(self._entries) > self._max_entries
            or self._bytes > self._max_bytes
        ):
            _, evicted = self._entries.popitem(last=False)
            self._bytes -= evicted.size_bytes
            self._evictions += 1

    def delete(self, key: AuthorizedCacheKey) -> bool:
        entry = self._entries.pop(key.canonical, None)
        if entry is None:
            return False
        self._bytes -= entry.size_bytes
        return True

    def clear(self) -> None:
        self._entries.clear()
        self._bytes = 0

    @property
    def snapshot(self) -> CacheSnapshot:
        return CacheSnapshot(
            entries=len(self._entries),
            estimated_bytes=self._bytes,
            hits=self._hits,
            misses=self._misses,
            stale=self._stale,
            evictions=self._evictions,
        )
