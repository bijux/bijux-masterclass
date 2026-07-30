from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any


class CachedComputation:
    """Cache one derivation and expose its dependencies and invalidation state."""

    def __init__(
        self,
        compute: Callable[[object], object],
        *,
        depends_on: tuple[str, ...],
    ) -> None:
        if not depends_on:
            raise ValueError("a cached computation must name at least one dependency")
        self.compute = compute
        self.depends_on = depends_on
        self.public_name = ""
        self.cache_name = ""
        self.count_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.cache_name = f"_{name}_cached"
        self.count_name = f"_{name}_computations"

    def __get__(self, obj: object, owner: type[object] | None = None) -> Any:
        if obj is None:
            return self
        state = vars(obj)
        if self.cache_name not in state:
            state[self.cache_name] = self.compute(obj)
            state[self.count_name] = state.get(self.count_name, 0) + 1
        return state[self.cache_name]

    def invalidate(self, obj: object) -> bool:
        return vars(obj).pop(self.cache_name, None) is not None

    def evidence(self, obj: object) -> dict[str, object]:
        state = vars(obj)
        return {
            "public_name": self.public_name,
            "cache_name": self.cache_name,
            "dependencies": list(self.depends_on),
            "cached": self.cache_name in state,
            "computations": state.get(self.count_name, 0),
            "storage_owner": "instance.__dict__",
        }


class InvalidatingField:
    """Store one source value and invalidate named local derivations on assignment."""

    def __init__(self, *, invalidates: tuple[str, ...]) -> None:
        if not invalidates:
            raise ValueError("an invalidating field must name at least one cached field")
        self.invalidates = invalidates
        self.public_name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type[object], name: str) -> None:
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
        owner = type(obj)
        for cached_name in self.invalidates:
            cached = inspect.getattr_static(owner, cached_name)
            if not isinstance(cached, CachedComputation):
                raise TypeError(
                    f"{owner.__name__}.{cached_name} is not a CachedComputation"
                )
            cached.invalidate(obj)


class Document:
    text = InvalidatingField(invalidates=("word_count",))
    word_count = CachedComputation(
        lambda document: len(document.text.split()),
        depends_on=("text",),
    )

    def __init__(self, text: str) -> None:
        self.text = text


def cache_evidence() -> dict[str, object]:
    document = Document("one careful cache")
    first_read = document.word_count
    second_read = document.word_count
    before_change = Document.word_count.evidence(document)

    document.text = "one explicit cache invalidation rule"
    after_assignment = Document.word_count.evidence(document)
    refreshed_read = document.word_count

    return {
        "reads": {
            "first": first_read,
            "second": second_read,
            "after_dependency_change": refreshed_read,
        },
        "before_dependency_change": before_change,
        "after_dependency_change": after_assignment,
        "after_refresh": Document.word_count.evidence(document),
        "invalidation_owner": "Document.text assignment",
        "bypass_limit": "direct instance-dictionary mutation bypasses invalidation",
        "cross_instance_coherence": False,
    }
