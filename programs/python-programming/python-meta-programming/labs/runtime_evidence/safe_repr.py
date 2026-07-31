from __future__ import annotations

import inspect
from collections.abc import Iterator, Mapping


def _slot_storage_names(cls: type[object]) -> Iterator[str]:
    """Yield concrete slot storage names across the class hierarchy."""

    seen: set[str] = set()
    for owner in cls.__mro__:
        declared = vars(owner).get("__slots__", ())
        slots = (declared,) if isinstance(declared, str) else declared
        for name in slots:
            if name in {"__dict__", "__weakref__"}:
                continue
            if name.startswith("__") and not name.endswith("__"):
                storage_name = f"_{owner.__name__.lstrip('_')}{name}"
            else:
                storage_name = name
            if storage_name not in seen:
                seen.add(storage_name)
                yield storage_name


def stored_state(instance: object) -> dict[str, object]:
    """Collect instance-backed values without broad dynamic attribute lookup."""

    state: dict[str, object] = {}
    try:
        dictionary = object.__getattribute__(instance, "__dict__")
    except AttributeError:
        dictionary = None
    if isinstance(dictionary, Mapping):
        state.update(dictionary)

    for name in _slot_storage_names(type(instance)):
        if name in state:
            continue
        try:
            state[name] = object.__getattribute__(instance, name)
        except AttributeError:
            continue
    return state


def _constructor_order(cls: type[object]) -> tuple[str, ...] | None:
    try:
        signature = inspect.signature(cls.__init__)
    except (TypeError, ValueError):
        return None
    return tuple(
        parameter.name
        for parameter in signature.parameters.values()
        if parameter.name != "self"
        and parameter.kind
        not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        )
    )


def ordered_state(instance: object) -> tuple[tuple[str, object], ...]:
    """Order stored state by constructor contract, then stable extra names."""

    state = stored_state(instance)
    constructor_order = _constructor_order(type(instance))
    if constructor_order is None:
        return tuple(sorted(state.items()))

    ordered = [(name, state[name]) for name in constructor_order if name in state]
    named = {name for name, _ in ordered}
    ordered.extend(sorted((name, value) for name, value in state.items() if name not in named))
    return tuple(ordered)


def safe_repr(instance: object) -> str:
    """Render stored state without evaluating properties or fallback hooks."""

    fields = ", ".join(f"{name}={value!r}" for name, value in ordered_state(instance))
    return f"{type(instance).__name__}({fields})"


class SignatureGuidedRepr:
    """Use constructor order and stored values for a bounded representation."""

    def __repr__(self) -> str:
        return safe_repr(self)
