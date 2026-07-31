from __future__ import annotations

import json
from typing import Any


class StoreUnavailable(RuntimeError):
    """Raised when the educational backend cannot serve a read or write."""


class CountingStore:
    """A deterministic string store whose access path remains inspectable."""

    def __init__(self) -> None:
        self._values: dict[str, str] = {}
        self.events: list[dict[str, object]] = []
        self.available = True

    def get(self, key: str) -> str | None:
        self._require_available("read", key)
        value = self._values.get(key)
        self.events.append({"operation": "read", "key": key, "found": value is not None})
        return value

    def set(self, key: str, value: str) -> None:
        self._require_available("write", key)
        self._values[key] = value
        self.events.append({"operation": "write", "key": key})

    def snapshot(self) -> dict[str, str]:
        return dict(self._values)

    def _require_available(self, operation: str, key: str) -> None:
        if not self.available:
            raise StoreUnavailable(f"backend unavailable during {operation}: {key}")


class ExternalField:
    """Map one attribute to one stable backend slot with a local read cache."""

    def __init__(
        self,
        store: CountingStore,
        *,
        namespace: str,
        identity_name: str = "record_id",
    ) -> None:
        self.store = store
        self.namespace = namespace
        self.identity_name = identity_name
        self.owner_name = ""
        self.public_name = ""
        self.cache_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.owner_name = owner.__name__
        self.public_name = name
        self.cache_name = f"_{name}_external_cache"

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        state = vars(obj)
        if self.cache_name in state:
            return state[self.cache_name]

        raw = self.store.get(self.key_for(obj))
        if raw is None:
            raise AttributeError(f"{self.public_name} has no backend value")
        value = json.loads(raw)
        state[self.cache_name] = value
        return value

    def __set__(self, obj: object, value: object) -> None:
        encoded = json.dumps(value, sort_keys=True)
        self.store.set(self.key_for(obj), encoded)
        vars(obj)[self.cache_name] = value

    def key_for(self, obj: object) -> str:
        identity = getattr(obj, self.identity_name, None)
        if identity is None:
            raise ValueError(
                f"{self.identity_name} must exist before writing external state"
            )
        return f"{self.namespace}:{self.owner_name}:{identity}:{self.public_name}"

    def invalidate(self, obj: object) -> bool:
        return vars(obj).pop(self.cache_name, None) is not None

    def evidence(self, obj: object) -> dict[str, object]:
        return {
            "backend_key": self.key_for(obj),
            "cache_name": self.cache_name,
            "cached": self.cache_name in vars(obj),
            "source_of_truth": "CountingStore",
            "serialization": "JSON text",
            "read_policy": "read-through on local cache miss",
            "write_policy": "backend write before local cache update",
            "hidden_io": True,
        }


class IncidentRecord:
    store = CountingStore()
    title = ExternalField(store, namespace="incident")

    def __init__(self, record_id: int) -> None:
        self.record_id = record_id


def external_storage_evidence() -> dict[str, object]:
    store = CountingStore()

    class Record:
        title = ExternalField(store, namespace="incident")

        def __init__(self, record_id: int) -> None:
            self.record_id = record_id

    writer = Record(17)
    observer = Record(17)
    writer.title = "investigating"
    first_observed = observer.title
    field = Record.title
    key = field.key_for(observer)

    store.set(key, json.dumps("resolved"))
    stale_observed = observer.title
    field.invalidate(observer)
    refreshed_observed = observer.title

    return {
        "field": field.evidence(observer),
        "observed": {
            "first": first_observed,
            "after_backend_change_without_invalidation": stale_observed,
            "after_invalidation": refreshed_observed,
        },
        "backend_events": store.events,
        "authoritative_value": json.loads(store.snapshot()[key]),
        "transaction_support": False,
        "identity_map": False,
    }
