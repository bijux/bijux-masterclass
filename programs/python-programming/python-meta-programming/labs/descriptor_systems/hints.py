from __future__ import annotations

import types
from dataclasses import dataclass
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints


class UnsupportedHint(TypeError):
    """Raised when the lab cannot make an honest runtime promise for a hint."""


class ValueRule:
    label = "value rule"

    def apply(self, value: object) -> object:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Minimum(ValueRule):
    limit: int | float

    @property
    def label(self) -> str:
        return f"minimum={self.limit}"

    def apply(self, value: object) -> object:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Minimum can only validate numeric values")
        if value < self.limit:
            raise ValueError(f"value must be >= {self.limit}")
        return value


@dataclass(frozen=True, slots=True)
class NonBlank(ValueRule):
    label = "non-blank"

    def apply(self, value: object) -> object:
        if not isinstance(value, str):
            raise TypeError("NonBlank can only validate text")
        normalized = value.strip()
        if not normalized:
            raise ValueError("value must not be blank")
        return normalized


SUPPORTED_SCALARS = (str, int, float, bool)


@dataclass(frozen=True, slots=True)
class HintPlan:
    accepted_types: tuple[type[object], ...]
    nullable: bool
    rules: tuple[ValueRule, ...]

    def accept(self, value: object) -> tuple[object, str]:
        if value is None:
            if self.nullable:
                return None, "none"
            raise TypeError("None is not accepted by this hint")

        for accepted_type in self.accepted_types:
            if _matches_scalar(value, accepted_type):
                return self._apply_rules(value), "already-matched"

        failures: list[str] = []
        for accepted_type in self.accepted_types:
            try:
                coerced = _coerce_scalar(value, accepted_type)
            except (TypeError, ValueError) as error:
                failures.append(str(error))
                continue
            return self._apply_rules(coerced), f"coerced-to-{accepted_type.__name__}"

        accepted = ", ".join(item.__name__ for item in self.accepted_types)
        detail = "; ".join(failures)
        raise TypeError(f"value does not match {accepted}: {detail}")

    def manifest(self) -> dict[str, object]:
        return {
            "accepted_types": [item.__name__ for item in self.accepted_types],
            "nullable": self.nullable,
            "rules": [rule.label for rule in self.rules],
            "coercion_policy": {
                "int": "base-10 integer text",
                "float": "numeric text or non-boolean integer",
                "bool": "true/false, yes/no, on/off, or 1/0 text",
                "str": "no coercion",
            },
            "refused": [
                "parameterized generics",
                "unrecognized Annotated metadata",
                "arbitrary classes",
                "nested model validation",
            ],
        }

    def _apply_rules(self, value: object) -> object:
        for rule in self.rules:
            value = rule.apply(value)
        return value


def compile_hint(hint: object) -> HintPlan:
    rules: tuple[ValueRule, ...] = ()
    origin = get_origin(hint)
    if origin is Annotated:
        base, *metadata = get_args(hint)
        unknown = [item for item in metadata if not isinstance(item, ValueRule)]
        if unknown:
            raise UnsupportedHint(
                "Annotated metadata must contain only explicit ValueRule objects"
            )
        hint = base
        rules = tuple(metadata)
        origin = get_origin(hint)

    nullable = False
    if origin in (Union, types.UnionType):
        members = list(get_args(hint))
        nullable = type(None) in members
        members = [item for item in members if item is not type(None)]
    else:
        members = [hint]

    if not members:
        raise UnsupportedHint("a hint must accept at least one non-None scalar type")
    if any(get_origin(member) is not None for member in members):
        raise UnsupportedHint("parameterized generics are intentionally unsupported")
    if any(member not in SUPPORTED_SCALARS for member in members):
        raise UnsupportedHint("only str, int, float, bool, and optional unions are supported")

    return HintPlan(tuple(members), nullable, rules)


def _matches_scalar(value: object, accepted_type: type[object]) -> bool:
    if accepted_type in (int, float) and isinstance(value, bool):
        return False
    return isinstance(value, accepted_type)


def _coerce_scalar(value: object, accepted_type: type[object]) -> object:
    if accepted_type is str:
        raise TypeError("text values are not guessed from non-text input")
    if accepted_type is int:
        if isinstance(value, str):
            return int(value, 10)
        raise TypeError("integer coercion accepts only base-10 text")
    if accepted_type is float:
        if isinstance(value, int) and not isinstance(value, bool):
            return float(value)
        if isinstance(value, str):
            return float(value)
        raise TypeError("float coercion accepts numeric text or integers")
    if accepted_type is bool:
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "yes", "on", "1"}:
                return True
            if normalized in {"false", "no", "off", "0"}:
                return False
        raise TypeError("boolean coercion accepts explicit boolean text")
    raise AssertionError(f"unsupported scalar reached coercion: {accepted_type!r}")


class HintField:
    """Resolve one bounded runtime hint when its owner class is created."""

    def __init__(self) -> None:
        self.public_name = ""
        self.storage_name = ""
        self.plan: HintPlan | None = None

    def __set_name__(self, owner: type[object], name: str) -> None:
        hints = get_type_hints(owner, include_extras=True)
        if name not in hints:
            raise TypeError(f"{owner.__name__}.{name} requires a type annotation")
        self.public_name = name
        self.storage_name = f"_{name}"
        self.plan = compile_hint(hints[name])

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        try:
            return vars(obj)[self.storage_name]
        except KeyError as error:
            raise AttributeError(f"{self.public_name} has not been assigned") from error

    def __set__(self, obj: object, value: object) -> None:
        if self.plan is None:
            raise RuntimeError("HintField has not been bound to an owner")
        accepted, decision = self.plan.accept(value)
        vars(obj)[self.storage_name] = accepted
        vars(obj).setdefault("__hint_trace__", []).append({
            "field": self.public_name,
            "input": value,
            "stored": accepted,
            "decision": decision,
        })


class RetryPolicy:
    attempts: Annotated[int, Minimum(0)] = HintField()
    label: Annotated[str, NonBlank()] = HintField()
    timeout: float | None = HintField()
    enabled: bool = HintField()

    def __init__(
        self,
        *,
        attempts: object,
        label: object,
        timeout: object,
        enabled: object,
    ) -> None:
        self.attempts = attempts
        self.label = label
        self.timeout = timeout
        self.enabled = enabled


def hint_evidence() -> dict[str, object]:
    policy = RetryPolicy(
        attempts="3",
        label="  delivery retry  ",
        timeout=2,
        enabled="yes",
    )

    refused: dict[str, str] = {}
    for name, hint in {
        "parameterized_generic": list[int],
        "unknown_metadata": Annotated[int, "positive"],
        "arbitrary_class": bytes,
    }.items():
        try:
            compile_hint(hint)
        except UnsupportedHint as error:
            refused[name] = str(error)

    return {
        "stored": {
            "attempts": policy.attempts,
            "label": policy.label,
            "timeout": policy.timeout,
            "enabled": policy.enabled,
        },
        "trace": vars(policy)["__hint_trace__"],
        "plans": {
            "attempts": RetryPolicy.attempts.plan.manifest(),
            "timeout": RetryPolicy.timeout.plan.manifest(),
        },
        "refused": refused,
        "full_runtime_typing": False,
    }
