from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast


ValueT = TypeVar("ValueT")


@dataclass(frozen=True, slots=True)
class TypedFieldSpec:
    name: str
    expected_type: str
    storage_name: str


class TypedField(Generic[ValueT]):
    """Own one shallow runtime type rule for a reusable attribute boundary."""

    def __init__(self, expected_type: type[ValueT]) -> None:
        self.expected_type = expected_type
        self.name: str | None = None
        self.storage_name: str | None = None

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name
        self.storage_name = f"_{type(self).__name__}__{name}"

    def __get__(
        self,
        instance: object | None,
        owner: type[object] | None = None,
    ) -> ValueT | TypedField[ValueT]:
        if instance is None:
            return self
        if self.storage_name is None:
            raise RuntimeError("TypedField has not received __set_name__")
        try:
            return cast(ValueT, vars(instance)[self.storage_name])
        except KeyError as error:
            raise AttributeError(self.name or "unbound field") from error

    def __set__(self, instance: object, value: ValueT) -> None:
        if self.storage_name is None or self.name is None:
            raise RuntimeError("TypedField has not received __set_name__")
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}; "
                f"got {type(value).__name__}"
            )
        vars(instance)[self.storage_name] = value

    def spec(self) -> TypedFieldSpec:
        if self.storage_name is None or self.name is None:
            raise RuntimeError("TypedField has not received __set_name__")
        return TypedFieldSpec(
            name=self.name,
            expected_type=self.expected_type.__name__,
            storage_name=self.storage_name,
        )
