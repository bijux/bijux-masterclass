from __future__ import annotations
import hashlib
from dataclasses import dataclass
from pathlib import Path
from .model import ValidationError
from .operation import parse_document

@dataclass(frozen=True)
class PersistedOperation:
    sha256: str
    name: str
    document: str

class PersistedOperationRegistry:
    def __init__(self) -> None:
        self._by_hash: dict[str, PersistedOperation] = {}
        self._by_name: dict[str, PersistedOperation] = {}

    @staticmethod
    def digest(document: str) -> str:
        return hashlib.sha256(document.encode("utf-8")).hexdigest()

    def register(self, name: str, document: str) -> PersistedOperation:
        parsed = parse_document(document)
        matches = [op for op in parsed.operations if op.name == name]
        if len(matches) != 1: raise ValidationError("persisted operation name mismatch")
        digest = self.digest(document)
        current = self._by_hash.get(digest)
        if current and current.document != document: raise ValidationError("hash collision")
        if name in self._by_name and self._by_name[name].sha256 != digest:
            raise ValidationError("operation name already registered to another document")
        operation = PersistedOperation(digest, name, document)
        self._by_hash[digest] = operation; self._by_name[name] = operation
        return operation

    def get(self, digest: str) -> PersistedOperation:
        try: return self._by_hash[digest]
        except KeyError as exc: raise ValidationError("unknown persisted operation") from exc

    def by_name(self, name: str) -> PersistedOperation:
        try: return self._by_name[name]
        except KeyError as exc: raise ValidationError("unknown operation name") from exc

    @classmethod
    def from_directory(cls, directory: Path) -> "PersistedOperationRegistry":
        registry = cls()
        for path in sorted(directory.glob("*.graphql")):
            registry.register(path.stem, path.read_text())
        return registry
