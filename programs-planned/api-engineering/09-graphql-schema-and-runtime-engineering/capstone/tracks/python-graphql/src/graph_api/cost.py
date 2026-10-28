"""Dependency-light demand analysis for registered GraphQL operations.

The analyzer expands fragments, counts structural demand, and estimates list
multipliers. It demonstrates the mechanics behind a query budget. A production
gateway should apply equivalent rules to a standards-complete GraphQL AST.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import ValidationError
from .operation import Document, FragmentSpread, InlineFragment, Selection


@dataclass(frozen=True)
class CostPolicy:
    max_depth: int = 12
    max_aliases: int = 30
    max_root_fields: int = 8
    max_cost: int = 5_000
    max_fanout: int = 12
    default_page_size: int = 20
    max_page_size: int = 100


@dataclass(frozen=True)
class CostReport:
    depth: int
    aliases: int
    root_fields: int
    estimated_cost: int
    service_fanout: int


SERVICE_FIELDS = {
    "project": "analysis-control",
    "analysisRun": "analysis-control",
    "analysisRuns": "analysis-control",
    "artifact": "artifact-service",
    "artifacts": "artifact-service",
    "deliverySummary": "notification-service",
}

LIST_FIELDS = {
    "analysisRuns",
    "search",
    "edges",
    "artifacts",
}

BASE_COST = {
    "search": 8,
    "analysisRuns": 5,
    "artifacts": 5,
    "deliverySummary": 3,
}


def _page_size(
    arguments: tuple[str, ...],
    variables: dict[str, object],
    policy: CostPolicy,
) -> int:
    """Read a literal or variable-backed ``first`` argument."""

    tokens = list(arguments)
    for index, token in enumerate(tokens):
        if token != "first" or index + 2 >= len(tokens):
            continue
        if tokens[index + 1] != ":":
            continue

        value = tokens[index + 2]
        if value == "$" and index + 3 < len(tokens):
            raw = variables.get(tokens[index + 3], policy.default_page_size)
        elif value.startswith("$"):
            raw = variables.get(value[1:], policy.default_page_size)
        else:
            raw = value

        try:
            size = int(raw)
        except (TypeError, ValueError) as exc:
            raise ValidationError("first must be an integer") from exc

        if size < 1 or size > policy.max_page_size:
            raise ValidationError("page size outside policy")
        return size

    return policy.default_page_size


def analyze(
    document: Document,
    *,
    operation_name: str,
    variables: dict[str, object] | None = None,
    policy: CostPolicy = CostPolicy(),
) -> CostReport:
    """Analyze one named operation and enforce the supplied budget."""

    variables = variables or {}
    matches = [
        operation
        for operation in document.operations
        if operation.name == operation_name
    ]
    if len(matches) != 1:
        raise ValidationError(
            "operation name must select exactly one operation"
        )

    operation = matches[0]
    services: set[str] = set()
    aliases = 0
    max_depth = 0
    total_cost = 0

    def visit(
        selections: tuple[Selection, ...],
        depth: int,
        fragment_stack: tuple[str, ...],
        multiplier: int = 1,
    ) -> None:
        nonlocal aliases, max_depth, total_cost

        max_depth = max(max_depth, depth)
        for selection in selections:
            if isinstance(selection, FragmentSpread):
                if selection.name in fragment_stack:
                    raise ValidationError("fragment cycle")
                fragment = document.fragments.get(selection.name)
                if fragment is None:
                    raise ValidationError("undefined fragment")
                visit(
                    fragment.selections,
                    depth,
                    fragment_stack + (selection.name,),
                    multiplier,
                )
                continue

            if isinstance(selection, InlineFragment):
                visit(
                    selection.selections,
                    depth,
                    fragment_stack,
                    multiplier,
                )
                continue

            if selection.alias is not None:
                aliases += 1

            service = SERVICE_FIELDS.get(selection.name)
            if service is not None:
                services.add(service)

            child_multiplier = multiplier
            if selection.name in LIST_FIELDS:
                child_multiplier *= _page_size(
                    selection.arguments,
                    variables,
                    policy,
                )

            total_cost += BASE_COST.get(selection.name, 1) * multiplier
            if selection.selections:
                visit(
                    selection.selections,
                    depth + 1,
                    fragment_stack,
                    child_multiplier,
                )

    visit(operation.selections, 1, ())

    report = CostReport(
        depth=max_depth,
        aliases=aliases,
        root_fields=len(operation.selections),
        estimated_cost=total_cost,
        service_fanout=len(services),
    )

    if report.depth > policy.max_depth:
        raise ValidationError("query depth exceeds budget")
    if report.aliases > policy.max_aliases:
        raise ValidationError("alias count exceeds budget")
    if report.root_fields > policy.max_root_fields:
        raise ValidationError("root field count exceeds budget")
    if report.estimated_cost > policy.max_cost:
        raise ValidationError("estimated cost exceeds budget")
    if report.service_fanout > policy.max_fanout:
        raise ValidationError("service fanout exceeds budget")

    return report
