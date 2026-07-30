from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


DescriptorKind = Literal["data", "non-data", "not-a-descriptor"]


@dataclass(frozen=True, slots=True)
class DescriptorProtocol:
    """Reviewable protocol evidence for one class attribute."""

    descriptor_type: str
    has_get: bool
    has_set: bool
    has_delete: bool
    has_set_name: bool
    kind: DescriptorKind

    def manifest(self) -> dict[str, object]:
        return asdict(self)


def inspect_descriptor_protocol(value: object) -> DescriptorProtocol:
    """Classify a value using the special methods Python actually consults."""

    owner = type(value)
    has_get = hasattr(owner, "__get__")
    has_set = hasattr(owner, "__set__")
    has_delete = hasattr(owner, "__delete__")
    if has_set or has_delete:
        kind: DescriptorKind = "data"
    elif has_get:
        kind = "non-data"
    else:
        kind = "not-a-descriptor"
    return DescriptorProtocol(
        descriptor_type=owner.__name__,
        has_get=has_get,
        has_set=has_set,
        has_delete=has_delete,
        has_set_name=hasattr(owner, "__set_name__"),
        kind=kind,
    )


class NameAware:
    """Learn an installation name without participating in attribute lookup."""

    def __init__(self) -> None:
        self.owner_name = ""
        self.public_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.owner_name = owner.__name__
        self.public_name = name


class StoredField:
    """A minimal data descriptor with per-instance dictionary storage."""

    def __init__(self) -> None:
        self.public_name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.storage_name = f"_{name}"

    def __get__(
        self,
        instance: object | None,
        owner: type[object] | None = None,
    ) -> object:
        if instance is None:
            return self
        try:
            return vars(instance)[self.storage_name]
        except KeyError as error:
            raise AttributeError(f"{self.public_name} is unset") from error

    def __set__(self, instance: object, value: object) -> None:
        vars(instance)[self.storage_name] = value


class ShadowableValue:
    """A non-data descriptor whose result can yield to instance state."""

    def __init__(self, value: object) -> None:
        self.value = value

    def __get__(
        self,
        instance: object | None,
        owner: type[object] | None = None,
    ) -> object:
        if instance is None:
            return self
        return self.value
