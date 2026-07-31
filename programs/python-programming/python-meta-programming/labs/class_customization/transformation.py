from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar, cast


ClassT = TypeVar("ClassT", bound=type[Any])


@dataclass(frozen=True, slots=True)
class ClassCustomization:
    """Public evidence attached by the post-construction class decorator."""

    label: str
    decorated_name: str
    timing: str = "after-class-creation"


def mark_class(label: str) -> Callable[[ClassT], ClassT]:
    """Attach an inspectable mark to an already-created class."""

    normalized_label = label.strip()
    if not normalized_label:
        raise ValueError("class customization label cannot be blank")

    def decorate(cls: ClassT) -> ClassT:
        if "__class_customization__" in vars(cls):
            raise TypeError(
                f"{cls.__name__} already defines reserved __class_customization__"
            )
        cls.__class_customization__ = ClassCustomization(  # type: ignore[attr-defined]
            label=normalized_label,
            decorated_name=cls.__name__,
        )
        return cls

    return decorate


def tracing_class_decorator(
    label: str,
    events: list[str],
) -> Callable[[ClassT], ClassT]:
    """Record factory and bottom-up application timing for one class decorator."""

    events.append(f"factory:{label}")

    def decorate(cls: ClassT) -> ClassT:
        events.append(f"decorate:{label}:{cls.__name__}")
        prior = cast(tuple[str, ...], getattr(cls, "__decorator_trace__", ()))
        cls.__decorator_trace__ = (*prior, label)  # type: ignore[attr-defined]
        return cls

    return decorate
