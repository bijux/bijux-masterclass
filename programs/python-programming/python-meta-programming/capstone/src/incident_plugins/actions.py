from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
import inspect
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class ActionSpec:
    name: str
    summary: str
    signature: inspect.Signature

    def manifest(self) -> dict[str, object]:
        parameters = []
        for parameter in self.signature.parameters.values():
            if parameter.name == "self":
                continue
            parameters.append(
                {
                    "name": parameter.name,
                    "kind": parameter.kind.name.lower(),
                    "default": None if parameter.default is inspect._empty else parameter.default,
                    "annotation": _annotation_name(parameter.annotation),
                }
            )
        return {
            "name": self.name,
            "summary": self.summary,
            "parameters": parameters,
            "returns": _annotation_name(self.signature.return_annotation),
        }


def action(summary: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Wrap a plugin method while preserving its signature and recording invocations."""

    def decorate(function: Callable[..., Any]) -> Callable[..., Any]:
        signature = inspect.signature(function)
        spec = ActionSpec(
            name=function.__name__,
            summary=summary.strip() or (inspect.getdoc(function) or ""),
            signature=signature,
        )

        @wraps(function)
        def wrapped(self, *args: Any, **kwargs: Any) -> Any:
            bound = signature.bind(self, *args, **kwargs)
            bound.apply_defaults()
            result = function(self, *args, **kwargs)
            self._action_history.append(
                {
                    "action": function.__name__,
                    "arguments": {k: v for k, v in bound.arguments.items() if k != "self"},
                    "result_type": type(result).__name__,
                }
            )
            return result

        wrapped.__signature__ = signature
        wrapped.__plugin_action__ = spec
        return wrapped

    return decorate


def describe_action_wrapper(function: Callable[..., Any]) -> dict[str, object]:
    """Describe one action wrapper chain without invoking any callable."""

    original = inspect.unwrap(function)
    chain = []
    current = function
    depth = 0
    while True:
        chain.append(
            {
                "depth": depth,
                "name": current.__name__,
                "implementation_signature": str(
                    inspect.signature(current, follow_wrapped=False)
                ),
                "owns_action_spec": hasattr(current, "__plugin_action__"),
                "owns_explicit_signature": "__signature__" in vars(current),
            }
        )
        if not hasattr(current, "__wrapped__"):
            break
        current = current.__wrapped__
        depth += 1

    spec = getattr(function, "__plugin_action__", None)
    return {
        "visible_name": function.__name__,
        "visible_signature": str(inspect.signature(function)),
        "original_name": original.__name__,
        "original_signature": str(inspect.signature(original)),
        "wrapper_depth": depth,
        "chain": chain,
        "metadata_preserved": {
            "has_wrapped": hasattr(function, "__wrapped__"),
            "name_matches": function.__name__ == original.__name__,
            "qualname_matches": function.__qualname__ == original.__qualname__,
            "doc_matches": function.__doc__ == original.__doc__,
            "annotations_match": function.__annotations__ == original.__annotations__,
        },
        "action_spec_signature_matches_original": (
            spec is not None and spec.signature == inspect.signature(original)
        ),
    }


def _annotation_name(annotation: Any) -> str | None:
    if annotation is inspect._empty:
        return None
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation)
