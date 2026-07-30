from __future__ import annotations

import inspect
import types
import warnings
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any, Literal, ParamSpec, Protocol, TypeVar, Union, cast, get_args, get_origin, get_type_hints


Parameters = ParamSpec("Parameters")
ResultT = TypeVar("ResultT")
MismatchMode = Literal["raise", "warn"]


class UnsupportedHintError(TypeError):
    """Signal that the partial validator refuses an annotation."""


@dataclass(frozen=True, slots=True)
class ValidationPolicy:
    """The complete public policy captured by ``validated``."""

    on_mismatch: MismatchMode
    validate_return: bool
    supported_hints: tuple[str, ...] = ("Any", "plain runtime classes", "Union", "Optional")


class ValidatedCallable(Protocol[Parameters, ResultT]):
    __validation_policy__: ValidationPolicy
    __validated_hints__: dict[str, object]

    def __call__(
        self,
        *args: Parameters.args,
        **kwargs: Parameters.kwargs,
    ) -> ResultT: ...


def _hint_name(hint: object) -> str:
    if hint is Any:
        return "Any"
    if isinstance(hint, type):
        return hint.__name__
    return str(hint)


def _validate_supported_hint(hint: object, *, location: str) -> None:
    if hint is Any or isinstance(hint, type):
        return

    origin = get_origin(hint)
    if origin in (Union, types.UnionType):
        for member in get_args(hint):
            _validate_supported_hint(member, location=location)
        return

    raise UnsupportedHintError(
        f"{location} uses unsupported runtime hint {_hint_name(hint)}; "
        "validated supports Any, plain runtime classes, Union, and Optional"
    )


def _matches_hint(value: object, hint: object) -> bool:
    if hint is Any:
        return True
    origin = get_origin(hint)
    if origin in (Union, types.UnionType):
        return any(_matches_hint(value, member) for member in get_args(hint))
    return isinstance(value, cast(type[object], hint))


def validated(
    *,
    on_mismatch: MismatchMode = "raise",
    validate_return: bool = True,
) -> Callable[
    [Callable[Parameters, ResultT]],
    ValidatedCallable[Parameters, ResultT],
]:
    """Check a deliberately small hint subset at one callable boundary."""

    if on_mismatch not in ("raise", "warn"):
        raise ValueError("on_mismatch must be 'raise' or 'warn'")

    policy = ValidationPolicy(
        on_mismatch=on_mismatch,
        validate_return=validate_return,
    )

    def decorate(
        function: Callable[Parameters, ResultT],
    ) -> ValidatedCallable[Parameters, ResultT]:
        signature = inspect.signature(function)
        hints = get_type_hints(function)
        for name, hint in hints.items():
            if name != "return" or validate_return:
                _validate_supported_hint(hint, location=name)

        def report_mismatch(message: str) -> None:
            if policy.on_mismatch == "raise":
                raise TypeError(message)
            warnings.warn(message, UserWarning, stacklevel=3)

        @wraps(function)
        def wrapped(
            *args: Parameters.args,
            **kwargs: Parameters.kwargs,
        ) -> ResultT:
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, value in bound.arguments.items():
                hint = hints.get(name, inspect.Signature.empty)
                if hint is not inspect.Signature.empty and not _matches_hint(value, hint):
                    report_mismatch(
                        f"argument {name}={value!r} has type {type(value).__name__}; "
                        f"expected {_hint_name(hint)}"
                    )

            result = function(*args, **kwargs)
            return_hint = hints.get("return", inspect.Signature.empty)
            if (
                validate_return
                and return_hint is not inspect.Signature.empty
                and not _matches_hint(result, return_hint)
            ):
                report_mismatch(
                    f"return value {result!r} has type {type(result).__name__}; "
                    f"expected {_hint_name(return_hint)}"
                )
            return result

        wrapped.__validation_policy__ = policy  # type: ignore[attr-defined]
        wrapped.__validated_hints__ = dict(hints)  # type: ignore[attr-defined]
        return cast(ValidatedCallable[Parameters, ResultT], wrapped)

    return decorate
