from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class CompatibilityIssue:
    severity: str
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class CompatibilityReport:
    status: str
    issues: tuple[CompatibilityIssue, ...]


def _types(schema: dict[str, Any]) -> tuple[str, ...]:
    value = schema.get("type")
    if isinstance(value, str):
        return (value,)
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return ()


def compare_object_schemas(
    old: dict[str, Any], new: dict[str, Any]
) -> CompatibilityReport:
    issues: list[CompatibilityIssue] = []
    old_required = set(old.get("required", []))
    new_required = set(new.get("required", []))
    for name in sorted(new_required - old_required):
        issues.append(
            CompatibilityIssue(
                "breaking", f"$.{name}", "field became newly required"
            )
        )
    old_properties = old.get("properties", {})
    new_properties = new.get("properties", {})
    for name in sorted(set(old_properties) - set(new_properties)):
        issues.append(
            CompatibilityIssue(
                "breaking", f"$.{name}", "previously available field was removed"
            )
        )
    for name in sorted(set(old_properties) & set(new_properties)):
        before = old_properties[name]
        after = new_properties[name]
        if _types(before) != _types(after):
            issues.append(
                CompatibilityIssue("breaking", f"$.{name}", "field type changed")
            )
        old_enum = set(before.get("enum", []))
        new_enum = set(after.get("enum", []))
        if old_enum and not old_enum.issubset(new_enum):
            issues.append(
                CompatibilityIssue("breaking", f"$.{name}", "enum was narrowed")
            )
        elif new_enum - old_enum and old_enum:
            issues.append(
                CompatibilityIssue(
                    "review", f"$.{name}", "enum gained values; strict consumers may fail"
                )
            )
    for name in sorted(set(new_properties) - set(old_properties)):
        if name not in new_required:
            issues.append(
                CompatibilityIssue("additive", f"$.{name}", "optional field added")
            )
    if any(issue.severity == "breaking" for issue in issues):
        status = "rejected"
    elif any(issue.severity == "review" for issue in issues):
        status = "review-required"
    else:
        status = "accepted"
    return CompatibilityReport(status, tuple(issues))


class UpcasterChain:
    def __init__(self) -> None:
        self._steps: dict[tuple[int, int], Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(
        self,
        from_version: int,
        to_version: int,
        transform: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        if to_version != from_version + 1:
            raise ValueError("upcasters must be adjacent versions")
        identity = (from_version, to_version)
        if identity in self._steps:
            raise ValueError("duplicate upcaster")
        self._steps[identity] = transform

    def apply(
        self, value: dict[str, Any], from_version: int, to_version: int
    ) -> dict[str, Any]:
        current = dict(value)
        for version in range(from_version, to_version):
            try:
                transform = self._steps[(version, version + 1)]
            except KeyError as exc:
                raise ValueError(f"missing upcaster {version}->{version + 1}") from exc
            current = transform(dict(current))
        return current
