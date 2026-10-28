from __future__ import annotations

from dataclasses import dataclass
from .model import Unavailable, ValidationError


@dataclass
class Instance:
    instance_id: str
    service: str
    version: str
    healthy: bool = True
    accepting: bool = True


class ServiceRegistry:
    def __init__(self) -> None:
        self._instances: dict[str, list[Instance]] = {}
        self._cursor: dict[str, int] = {}

    def register(self, instance: Instance) -> None:
        items = self._instances.setdefault(instance.service, [])
        if any(x.instance_id == instance.instance_id for x in items):
            raise ValidationError("duplicate instance id")
        items.append(instance)

    def set_health(self, service: str, instance_id: str, healthy: bool) -> None:
        for instance in self._instances.get(service, []):
            if instance.instance_id == instance_id:
                instance.healthy = healthy
                return
        raise ValidationError("unknown instance")

    def choose(self, service: str, *, supported_versions: set[str] | None = None) -> Instance:
        candidates = [x for x in self._instances.get(service, []) if x.healthy and x.accepting]
        if supported_versions is not None:
            candidates = [x for x in candidates if x.version in supported_versions]
        if not candidates:
            raise Unavailable(f"no healthy instance for {service}")
        candidates.sort(key=lambda x: x.instance_id)
        index = self._cursor.get(service, 0) % len(candidates)
        self._cursor[service] = index + 1
        return candidates[index]
