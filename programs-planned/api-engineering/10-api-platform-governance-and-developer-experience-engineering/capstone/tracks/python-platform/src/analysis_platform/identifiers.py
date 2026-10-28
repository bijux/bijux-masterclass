from __future__ import annotations

import re

_NAME = re.compile(r"^[a-z][a-z0-9-]{0,62}$")
_KIND = re.compile(r"^[a-z][a-z0-9-]*$")


class IdentifierError(ValueError):
    pass


def normalize_kind(kind: str) -> str:
    value = kind.strip().lower()
    if not _KIND.fullmatch(value):
        raise IdentifierError("invalid-kind")
    return value


def validate_name(name: str) -> str:
    if not _NAME.fullmatch(name):
        raise IdentifierError("invalid-name")
    return name


def entity_ref(kind: str, namespace: str, name: str) -> str:
    return f"{normalize_kind(kind)}:{validate_name(namespace)}/{validate_name(name)}"


def parse_ref(value: str) -> tuple[str, str, str]:
    try:
        kind, rest = value.split(":", 1)
        namespace, name = rest.split("/", 1)
    except ValueError as exc:
        raise IdentifierError("invalid-entity-ref") from exc
    canonical = entity_ref(kind, namespace, name)
    if canonical != value:
        raise IdentifierError("noncanonical-entity-ref")
    return kind, namespace, name
