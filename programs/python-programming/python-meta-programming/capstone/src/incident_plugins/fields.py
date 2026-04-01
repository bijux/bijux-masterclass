from __future__ import annotations

from dataclasses import dataclass
from typing import Any


UNSET = object()


@dataclass(frozen=True, slots=True)
class FieldSpec:
    name: str
    kind: str
    description: str
    required: bool
    default: object | None
    choices: tuple[str, ...] | None = None
    minimum: int | None = None
    maximum: int | None = None

    def manifest(self) -> dict[str, object]:
        return {
            "name": self.name,
            "kind": self.kind,
            "description": self.description,
            "required": self.required,
            "default": self.default,
            "choices": self.choices,
            "minimum": self.minimum,
            "maximum": self.maximum,
        }


class Field:
    kind = "field"

    def __init__(self, *, default: object = UNSET, description: str = "") -> None:
        self.default = default
        self.description = description
        self.name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        if self.storage_name in obj.__dict__:
            return obj.__dict__[self.storage_name]
        if self.default is not UNSET:
            value = self.default
            obj.__dict__[self.storage_name] = value
            return value
        raise AttributeError(f"{self.name} has not been configured")

    def __set__(self, obj: object, value: object) -> None:
        obj.__dict__[self.storage_name] = self.coerce(value)

    def required(self) -> bool:
        return self.default is UNSET

    def initialize(self, obj: object, values: dict[str, object]) -> None:
        if self.name in values:
            setattr(obj, self.name, values[self.name])
            return
        if self.default is UNSET:
            raise TypeError(f"missing required configuration field: {self.name}")
        setattr(obj, self.name, self.default)

    def spec(self) -> FieldSpec:
        default = None if self.default is UNSET else self.default
        return FieldSpec(
            name=self.name,
            kind=self.kind,
            description=self.description,
            required=self.required(),
            default=default,
        )

    def coerce(self, value: object) -> object:
        return value


class StringField(Field):
    kind = "string"

    def __init__(
        self,
        *,
        default: object = UNSET,
        description: str = "",
        min_length: int = 0,
    ) -> None:
        super().__init__(default=default, description=description)
        self.min_length = min_length

    def coerce(self, value: object) -> str:
        text = str(value).strip()
        if len(text) < self.min_length:
            raise ValueError(f"{self.name} must be at least {self.min_length} characters")
        return text

    def spec(self) -> FieldSpec:
        spec = super().spec()
        return FieldSpec(
            name=spec.name,
            kind=spec.kind,
            description=spec.description,
            required=spec.required,
            default=spec.default,
            minimum=self.min_length,
        )


class IntegerField(Field):
    kind = "integer"

    def __init__(
        self,
        *,
        default: object = UNSET,
        description: str = "",
        minimum: int | None = None,
        maximum: int | None = None,
    ) -> None:
        super().__init__(default=default, description=description)
        self.minimum = minimum
        self.maximum = maximum

    def coerce(self, value: object) -> int:
        number = int(value)
        if self.minimum is not None and number < self.minimum:
            raise ValueError(f"{self.name} must be >= {self.minimum}")
        if self.maximum is not None and number > self.maximum:
            raise ValueError(f"{self.name} must be <= {self.maximum}")
        return number

    def spec(self) -> FieldSpec:
        spec = super().spec()
        return FieldSpec(
            name=spec.name,
            kind=spec.kind,
            description=spec.description,
            required=spec.required,
            default=spec.default,
            minimum=self.minimum,
            maximum=self.maximum,
        )


class BooleanField(Field):
    kind = "boolean"

    def coerce(self, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "yes", "1", "on"}:
                return True
            if normalized in {"false", "no", "0", "off"}:
                return False
        raise ValueError(f"{self.name} must be a boolean value")


class ChoiceField(StringField):
    kind = "choice"

    def __init__(
        self,
        *choices: str,
        default: object = UNSET,
        description: str = "",
    ) -> None:
        if not choices:
            raise ValueError("ChoiceField requires at least one choice")
        super().__init__(default=default, description=description, min_length=1)
        self.choices = tuple(choice.strip() for choice in choices)

    def coerce(self, value: object) -> str:
        text = super().coerce(value)
        if text not in self.choices:
            raise ValueError(f"{self.name} must be one of {', '.join(self.choices)}")
        return text

    def spec(self) -> FieldSpec:
        spec = super().spec()
        return FieldSpec(
            name=spec.name,
            kind=spec.kind,
            description=spec.description,
            required=spec.required,
            default=spec.default,
            choices=self.choices,
            minimum=spec.minimum,
            maximum=spec.maximum,
        )
