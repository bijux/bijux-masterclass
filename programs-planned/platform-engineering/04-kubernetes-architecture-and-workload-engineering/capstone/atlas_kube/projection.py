from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping
import hashlib
import json


def configuration_digest(data: Mapping[str, str]) -> str:
    encoded = json.dumps(dict(data), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


@dataclass(slots=True)
class Projection:
    source_version: str
    files: dict[str, str]


@dataclass(slots=True)
class ApplicationConfig:
    startup_values: dict[str, str]
    dynamic_values: dict[str, str] = field(default_factory=dict)
    loaded_projection_version: str | None = None

    def reload_projection(self, projection: Projection) -> bool:
        if projection.source_version == self.loaded_projection_version:
            return False
        self.dynamic_values = dict(projection.files)
        self.loaded_projection_version = projection.source_version
        return True


def secret_annotation_guard(annotations: Mapping[str, str]) -> list[str]:
    forbidden = ("password", "secret", "token", "private_key", "api_key")
    findings = []
    for key, value in annotations.items():
        normalized = f"{key}={value}".lower()
        if any(term in normalized for term in forbidden):
            findings.append(key)
    return sorted(findings)
