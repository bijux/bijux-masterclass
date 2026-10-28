"""Stable summaries for PostgreSQL EXPLAIN (FORMAT JSON) documents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


class PlanError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class PlanSummary:
    actual_rows: int
    estimated_rows: int
    shared_hit_blocks: int
    shared_read_blocks: int
    temp_read_blocks: int
    temp_written_blocks: int
    sequential_scans: tuple[str, ...]
    index_scans: tuple[str, ...]
    sort_nodes: int
    disk_sorts: int
    total_nodes: int


def _as_int(node: dict[str, Any], key: str) -> int:
    value = node.get(key, 0)
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise PlanError(f"{key} must be numeric")
    if value < 0:
        raise PlanError(f"{key} cannot be negative")
    return int(value)


def _root(document: Any) -> dict[str, Any]:
    if (
        isinstance(document, list)
        and len(document) == 1
        and isinstance(document[0], dict)
        and isinstance(document[0].get("Plan"), dict)
    ):
        return document[0]["Plan"]
    if isinstance(document, dict) and isinstance(document.get("Plan"), dict):
        return document["Plan"]
    if isinstance(document, dict) and "Node Type" in document:
        return document
    raise PlanError("unrecognized PostgreSQL JSON plan")


def _walk(node: dict[str, Any]) -> Iterable[dict[str, Any]]:
    yield node
    children = node.get("Plans", [])
    if not isinstance(children, list):
        raise PlanError("Plans must be a list")
    for child in children:
        if not isinstance(child, dict):
            raise PlanError("plan child must be an object")
        yield from _walk(child)


def summarize_plan(document: Any) -> PlanSummary:
    root = _root(document)
    nodes = tuple(_walk(root))
    seq: list[str] = []
    indexes: list[str] = []
    disk_sorts = 0
    for node in nodes:
        node_type = str(node.get("Node Type", ""))
        relation = str(node.get("Relation Name", ""))
        if node_type == "Seq Scan":
            seq.append(relation or "<unknown>")
        if "Index" in node_type or node_type == "Bitmap Heap Scan":
            indexes.append(str(node.get("Index Name", relation or "<unknown>")))
        if node_type == "Sort" and "Disk" in str(node.get("Sort Method", "")):
            disk_sorts += 1
    return PlanSummary(
        actual_rows=_as_int(root, "Actual Rows"),
        estimated_rows=_as_int(root, "Plan Rows"),
        shared_hit_blocks=sum(_as_int(n, "Shared Hit Blocks") for n in nodes),
        shared_read_blocks=sum(_as_int(n, "Shared Read Blocks") for n in nodes),
        temp_read_blocks=sum(_as_int(n, "Temp Read Blocks") for n in nodes),
        temp_written_blocks=sum(_as_int(n, "Temp Written Blocks") for n in nodes),
        sequential_scans=tuple(seq),
        index_scans=tuple(indexes),
        sort_nodes=sum(str(n.get("Node Type", "")) == "Sort" for n in nodes),
        disk_sorts=disk_sorts,
        total_nodes=len(nodes),
    )


@dataclass(frozen=True, slots=True)
class PlanComparison:
    read_block_delta: int
    actual_row_delta: int
    removed_sequential_scans: tuple[str, ...]
    added_indexes: tuple[str, ...]


def compare_plans(before: PlanSummary, after: PlanSummary) -> PlanComparison:
    return PlanComparison(
        read_block_delta=after.shared_read_blocks - before.shared_read_blocks,
        actual_row_delta=after.actual_rows - before.actual_rows,
        removed_sequential_scans=tuple(
            sorted(set(before.sequential_scans) - set(after.sequential_scans))
        ),
        added_indexes=tuple(
            sorted(set(after.index_scans) - set(before.index_scans))
        ),
    )
