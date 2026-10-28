from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class Entity:
    kind: str
    namespace: str
    name: str
    title: str
    owner: str | None
    lifecycle: str
    system: str | None = None
    provides_apis: tuple[str, ...] = ()
    consumes_apis: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ContractRelease:
    api_ref: str
    protocol: str
    version: str
    source: str
    sha256: str
    lifecycle: str
    owner: str
    compatibility_evidence: str
    published_at: datetime


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    status: str
    entity_ref: str
    message: str
    evidence: str | None = None


@dataclass(frozen=True)
class ExceptionGrant:
    id: str
    rule_id: str
    entity_ref: str
    owner: str
    reason: str
    compensating_control: str
    approved_by: str
    created_at: datetime
    expires_at: datetime
    status: str
