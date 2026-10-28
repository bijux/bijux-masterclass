from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Mapping, Any

from .models import ContractRelease


class RegistryError(ValueError):
    pass


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class ContractRegistry:
    releases: dict[tuple[str,str], ContractRelease] = field(default_factory=dict)

    def publish(self, *, api_ref: str, protocol: str, version: str, source: str,
                data: bytes, owner: str, compatibility_evidence: str,
                published_at: datetime, lifecycle: str = "active") -> str:
        if not compatibility_evidence:
            raise RegistryError("missing-compatibility-evidence")
        digest = digest_bytes(data)
        key = (api_ref, version)
        existing = self.releases.get(key)
        if existing:
            if existing.sha256 != digest:
                raise RegistryError("immutable-release")
            return "idempotent"
        self.releases[key] = ContractRelease(
            api_ref=api_ref, protocol=protocol, version=version, source=source,
            sha256=digest, lifecycle=lifecycle, owner=owner,
            compatibility_evidence=compatibility_evidence, published_at=published_at,
        )
        return "published"

    def verify_file(self, api_ref: str, version: str, root: Path) -> bool:
        release = self.releases[(api_ref, version)]
        path = root / release.source
        return path.is_file() and digest_bytes(path.read_bytes()) == release.sha256

    @classmethod
    def from_records(cls, records: Iterable[Mapping[str, Any]]) -> "ContractRegistry":
        registry = cls()
        for record in records:
            key = (str(record["apiRef"]), str(record["version"]))
            if key in registry.releases:
                raise RegistryError("duplicate-release-record")
            digest = str(record["sha256"])
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise RegistryError("invalid-digest")
            registry.releases[key] = ContractRelease(
                api_ref=key[0], protocol=str(record["protocol"]), version=key[1],
                source=str(record["source"]), sha256=digest,
                lifecycle=str(record["lifecycle"]), owner=str(record["owner"]),
                compatibility_evidence=str(record["compatibilityEvidence"]),
                published_at=datetime.fromisoformat(str(record["publishedAt"]).replace("Z", "+00:00")),
            )
        return registry
