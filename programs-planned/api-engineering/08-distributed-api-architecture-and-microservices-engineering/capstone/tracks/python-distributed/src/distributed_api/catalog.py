from __future__ import annotations

from dataclasses import dataclass, field
from .model import ValidationError


@dataclass(frozen=True)
class ServiceDefinition:
    name: str
    owner: str
    kind: str
    data_facts: frozenset[str] = frozenset()
    interfaces: frozenset[str] = frozenset()


@dataclass
class ServiceCatalog:
    services: dict[str, ServiceDefinition] = field(default_factory=dict)

    def add(self, service: ServiceDefinition) -> None:
        if service.name in self.services:
            raise ValidationError(f"duplicate service: {service.name}")
        if not service.owner:
            raise ValidationError(f"owner required: {service.name}")
        self.services[service.name] = service

    def validate_single_writers(self) -> None:
        writers: dict[str, list[str]] = {}
        for service in self.services.values():
            for fact in service.data_facts:
                writers.setdefault(fact, []).append(service.name)
        duplicates = {fact: owners for fact, owners in writers.items() if len(owners) != 1}
        if duplicates:
            raise ValidationError(f"facts require one writer: {duplicates}")

    def owner_of(self, fact: str) -> str:
        owners = [s.name for s in self.services.values() if fact in s.data_facts]
        if len(owners) != 1:
            raise ValidationError(f"fact has {len(owners)} owners: {fact}")
        return owners[0]

    def validate_no_table_services(self) -> None:
        forbidden = {"project-service", "dataset-table-service", "idempotency-service"}
        found = forbidden.intersection(self.services)
        if found:
            raise ValidationError(f"table-shaped services rejected: {sorted(found)}")
