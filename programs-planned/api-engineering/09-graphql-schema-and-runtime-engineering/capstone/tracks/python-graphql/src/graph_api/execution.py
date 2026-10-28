"""Small execution helpers that demonstrate GraphQL null propagation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import GraphError


@dataclass(frozen=True)
class TypeRef:
    name: str
    non_null: bool = False


@dataclass(frozen=True)
class Completion:
    value: Any
    errors: tuple[GraphError, ...]
    bubbled: bool = False


def complete_field(
    value: Any,
    type_ref: TypeRef,
    *,
    path: tuple[str | int, ...],
    error: GraphError | None = None,
) -> Completion:
    """Complete one field and mark a non-null violation for propagation."""

    errors = (error,) if error is not None else ()
    if value is None and type_ref.non_null:
        if error is None:
            errors = (
                GraphError(
                    "Cannot return null for non-nullable field",
                    path,
                    "NON_NULL_VIOLATION",
                ),
            )
        return Completion(value=None, errors=errors, bubbled=True)

    return Completion(value=value, errors=errors, bubbled=False)


def complete_object(
    fields: dict[str, tuple[Any, TypeRef, GraphError | None]],
    *,
    path: tuple[str | int, ...] = (),
) -> Completion:
    """Complete an object and stop when a child violation reaches it."""

    result: dict[str, Any] = {}
    errors: list[GraphError] = []

    for name, (value, type_ref, error) in fields.items():
        completed = complete_field(
            value,
            type_ref,
            path=path + (name,),
            error=error,
        )
        errors.extend(completed.errors)
        if completed.bubbled:
            return Completion(
                value=None,
                errors=tuple(errors),
                bubbled=True,
            )
        result[name] = completed.value

    return Completion(
        value=result,
        errors=tuple(errors),
        bubbled=False,
    )
