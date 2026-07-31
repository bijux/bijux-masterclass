from __future__ import annotations

from dataclasses import asdict, dataclass
import inspect
import json
from types import MemberDescriptorType


@dataclass(frozen=True, slots=True)
class DebugEntry:
    """One attachment-first observation that did not resolve a runtime value."""

    name: str
    owner: str
    kind: str
    display: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def build_debug_view(
    obj: object,
    *,
    include_private: bool = False,
    max_names: int = 50,
) -> list[DebugEntry]:
    """Describe attached objects without evaluating descriptors or fallback hooks."""

    if max_names < 1:
        raise ValueError("max_names must be at least 1")

    stored_state = _stored_state(obj)
    candidate_names = set(stored_state)
    for owner in type(obj).__mro__:
        candidate_names.update(vars(owner))

    selected_names = [
        name
        for name in sorted(candidate_names)
        if include_private or not name.startswith("_")
    ][:max_names]

    entries = []
    for name in selected_names:
        raw = inspect.getattr_static(obj, name)
        owner = "instance" if name in stored_state else _class_owner(obj, name)
        kind = _kind(raw)
        entries.append(
            DebugEntry(
                name=name,
                owner=owner,
                kind=kind,
                display=_display(raw, kind),
            )
        )
    return entries


def _stored_state(obj: object) -> dict[str, object]:
    try:
        return dict(vars(obj))
    except TypeError:
        return {}


def _class_owner(obj: object, name: str) -> str:
    for owner in type(obj).__mro__:
        if name in vars(owner):
            return owner.__name__
    return "<unattached>"


def _kind(raw: object) -> str:
    if isinstance(raw, property):
        return "property"
    if isinstance(raw, MemberDescriptorType):
        return "slot"
    if inspect.isroutine(raw):
        return "routine"
    return "stored-value"


def _display(raw: object, kind: str) -> str:
    if raw is None or isinstance(raw, (bool, int, float, str)):
        return repr(raw)
    return f"<{kind}>"


def main() -> int:
    """Render the worked example from the same module that owns its behavior."""

    from .evidence import IncidentObservationTarget

    target = IncidentObservationTarget("queue lag")
    payload = [entry.as_dict() for entry in build_debug_view(target)]
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
