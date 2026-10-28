from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    name: str
    event_type: str
    owner: str
    channel: str
    schema_uri: str
    partition_key: str
    classification: str
    retention_days: int
    replay_policy: str
    lifecycle: str = "active"
    deprecated: bool = False


class CatalogError(ValueError):
    pass


class EventCatalog:
    def __init__(self, entries: list[CatalogEntry]) -> None:
        self.entries = {entry.event_type: entry for entry in entries}
        if len(self.entries) != len(entries):
            raise CatalogError("duplicate event type")
        for entry in entries:
            required = [
                entry.name,
                entry.owner,
                entry.channel,
                entry.schema_uri,
                entry.partition_key,
                entry.classification,
                entry.replay_policy,
                entry.lifecycle,
            ]
            if not all(required):
                raise CatalogError(f"incomplete catalogue entry {entry.name}")
            if entry.retention_days <= 0:
                raise CatalogError("retention must be positive")

    def require(self, event_type: str) -> CatalogEntry:
        try:
            return self.entries[event_type]
        except KeyError as exc:
            raise CatalogError(f"unregistered event type {event_type}") from exc
