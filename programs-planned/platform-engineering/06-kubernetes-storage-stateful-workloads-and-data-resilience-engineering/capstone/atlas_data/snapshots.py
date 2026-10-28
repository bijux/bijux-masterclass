from __future__ import annotations

from dataclasses import dataclass
import hashlib
import time
from collections.abc import Callable


@dataclass(frozen=True)
class SnapshotRecord:
    id: str
    group: str
    volumes: tuple[str, ...]
    consistency: str
    recovery_point: str
    created_ns: int


class SnapshotCoordinator:
    def __init__(self):
        self.records: dict[str, SnapshotRecord] = {}

    def crash_snapshot(self, group: str, volumes: list[str]) -> SnapshotRecord:
        return self._create(group, volumes, "crash", "uncoordinated")

    def application_snapshot(
        self,
        group: str,
        volumes: list[str],
        quiesce: Callable[[], str],
    ) -> SnapshotRecord:
        if not volumes:
            raise ValueError("at least one volume is required")
        recovery_point = quiesce()
        if not recovery_point:
            raise RuntimeError("application did not produce a recovery point")
        return self._create(group, volumes, "application", recovery_point)

    def _create(self, group: str, volumes: list[str], consistency: str, recovery_point: str) -> SnapshotRecord:
        material = f"{group}:{','.join(sorted(volumes))}:{consistency}:{recovery_point}"
        snapshot_id = hashlib.sha256(material.encode()).hexdigest()[:20]
        existing = self.records.get(snapshot_id)
        if existing:
            return existing
        record = SnapshotRecord(
            id=snapshot_id,
            group=group,
            volumes=tuple(sorted(volumes)),
            consistency=consistency,
            recovery_point=recovery_point,
            created_ns=time.time_ns(),
        )
        self.records[record.id] = record
        return record
