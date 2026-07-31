from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ClassRecipe:
    """The three inputs consumed by a class-construction callable."""

    name: str
    bases: tuple[type[object], ...]
    namespace: dict[str, object]


def build_class(recipe: ClassRecipe) -> type[object]:
    """Create one class while keeping all construction inputs explicit."""

    if not recipe.name.isidentifier():
        raise ValueError(f"class name must be an identifier: {recipe.name!r}")
    namespace = dict(recipe.namespace)
    namespace.setdefault("__module__", __name__)
    return type(recipe.name, recipe.bases, namespace)


def manual_creation_evidence() -> dict[str, object]:
    """Expose the correspondence between a class statement and ``type(...)``."""

    def render(self: object) -> str:
        return f"{type(self).__name__}:{self.channel}"  # type: ignore[attr-defined]

    recipe = ClassRecipe(
        name="DeliveryNotice",
        bases=(object,),
        namespace={
            "channel": "console",
            "render": render,
        },
    )
    notice_type = build_class(recipe)
    notice = notice_type()

    invalid_name_failure = ""
    try:
        build_class(ClassRecipe("not a class", (), {}))
    except ValueError as error:
        invalid_name_failure = str(error)

    return {
        "recipe": {
            "name": recipe.name,
            "bases": [base.__name__ for base in recipe.bases],
            "declared_names": list(recipe.namespace),
        },
        "result": {
            "class_name": notice_type.__name__,
            "metaclass": type(notice_type).__name__,
            "module": notice_type.__module__,
            "base_names": [base.__name__ for base in notice_type.__bases__],
            "rendered": notice.render(),  # type: ignore[attr-defined]
        },
        "timing": {
            "class_created_before_instance": isinstance(notice_type, type),
            "instance_type_is_result": type(notice) is notice_type,
        },
        "failure": {
            "input": "not a class",
            "type": "ValueError",
            "message": invalid_name_failure,
        },
        "claim_limits": [
            "type(...) creates one class from explicit inputs",
            "it does not install policy across future subclasses",
            "it does not justify a custom metaclass",
        ],
    }
