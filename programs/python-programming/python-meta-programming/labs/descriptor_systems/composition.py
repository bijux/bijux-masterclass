from __future__ import annotations

from typing import Any


def _trace(obj: object, event: dict[str, object]) -> None:
    vars(obj).setdefault("__field_trace__", []).append(event)


class StoredField:
    responsibility = "store one accepted value on the instance"

    def __init__(self) -> None:
        self.public_name = ""
        self.storage_name = ""
        self.binding_count = 0

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.binding_count += 1
        self.public_name = name
        self.storage_name = f"_{name}"

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        try:
            return vars(obj)[self.storage_name]
        except KeyError as error:
            raise AttributeError(f"{self.public_name} has not been assigned") from error

    def __set__(self, obj: object, value: object) -> None:
        vars(obj)[self.storage_name] = value
        _trace(obj, {"layer": type(self).__name__, "stored": value})


class FieldWrapper:
    responsibility = "delegate the descriptor protocol"

    def __init__(self, inner: object) -> None:
        required = ("__get__", "__set__", "__set_name__")
        missing = [name for name in required if not hasattr(type(inner), name)]
        if missing:
            raise TypeError(f"inner field is missing descriptor hooks: {', '.join(missing)}")
        self.inner = inner
        self.public_name = ""
        self.binding_count = 0

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.binding_count += 1
        self.public_name = name
        self.inner.__set_name__(owner, name)

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        return self.inner.__get__(obj, owner)

    def __set__(self, obj: object, value: object) -> None:
        self.inner.__set__(obj, value)


class NormalizeText(FieldWrapper):
    responsibility = "strip surrounding whitespace and normalize case"

    def __set__(self, obj: object, value: object) -> None:
        if not isinstance(value, str):
            _trace(obj, {
                "layer": type(self).__name__,
                "accepted": False,
                "reason": "expected text",
            })
            raise TypeError(f"{self.public_name} expected text")
        normalized = value.strip().lower()
        _trace(obj, {
            "layer": type(self).__name__,
            "input": value,
            "output": normalized,
        })
        self.inner.__set__(obj, normalized)


class OneOf(FieldWrapper):
    responsibility = "accept one value from an explicit choice set"

    def __init__(self, inner: object, *, choices: tuple[str, ...]) -> None:
        if not choices:
            raise ValueError("OneOf requires at least one choice")
        super().__init__(inner)
        self.choices = choices

    def __set__(self, obj: object, value: object) -> None:
        accepted = value in self.choices
        _trace(obj, {
            "layer": type(self).__name__,
            "value": value,
            "accepted": accepted,
        })
        if not accepted:
            raise ValueError(
                f"{self.public_name} must be one of {', '.join(self.choices)}"
            )
        self.inner.__set__(obj, value)


class AuditWrites(FieldWrapper):
    responsibility = "record accepted writes after storage succeeds"

    def __set__(self, obj: object, value: object) -> None:
        self.inner.__set__(obj, value)
        stored = self.inner.__get__(obj, type(obj))
        vars(obj).setdefault("__field_audit__", []).append({
            "field": self.public_name,
            "stored": stored,
        })
        _trace(obj, {"layer": type(self).__name__, "accepted_write": stored})


class DeliveryPolicy:
    channel = AuditWrites(
        NormalizeText(
            OneOf(
                StoredField(),
                choices=("email", "pager"),
            )
        )
    )


def describe_layers(field: object) -> list[dict[str, object]]:
    layers: list[dict[str, object]] = []
    current = field
    while True:
        layers.append({
            "type": type(current).__name__,
            "responsibility": getattr(current, "responsibility", "unknown"),
            "binding_count": getattr(current, "binding_count", 0),
        })
        if not isinstance(current, FieldWrapper):
            return layers
        current = current.inner


def composition_evidence() -> dict[str, object]:
    policy = DeliveryPolicy()
    policy.channel = " PAGER "

    rejected = DeliveryPolicy()
    try:
        rejected.channel = "console"
    except ValueError as error:
        rejection = str(error)
    else:
        raise AssertionError("unsupported channel was unexpectedly accepted")

    return {
        "accepted": {
            "stored": policy.channel,
            "trace": vars(policy)["__field_trace__"],
            "audit": vars(policy)["__field_audit__"],
        },
        "rejected": {
            "error": rejection,
            "stored": "_channel" in vars(rejected),
            "trace": vars(rejected)["__field_trace__"],
            "audit_created": "__field_audit__" in vars(rejected),
        },
        "layers": describe_layers(DeliveryPolicy.channel),
        "wrapper_budget": "one inner field plus three visible single-purpose layers",
        "cross_field_coordination": False,
    }
