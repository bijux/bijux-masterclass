from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    tenant: str
    scopes: FrozenSet[str]
    roles: FrozenSet[str] = frozenset()
    client_id: str | None = None
    token_id: str | None = None
    assurance: str = "baseline"
    auth_age_seconds: int = 0


@dataclass(frozen=True, slots=True)
class ResourceFacts:
    tenant: str | None = None
    owner: str | None = None
    members: FrozenSet[str] = frozenset()
    creator: str | None = None
    status: str | None = None
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Decision:
    allowed: bool
    reason: str
    conceal: bool = False
    obligations: tuple[str, ...] = ()
