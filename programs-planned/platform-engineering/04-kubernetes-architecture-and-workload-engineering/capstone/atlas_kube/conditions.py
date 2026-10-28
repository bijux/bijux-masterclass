from __future__ import annotations

from typing import Any
from .models import Condition, now_rfc3339


def merge_condition(existing: list[dict[str, Any]], desired: Condition) -> list[dict[str, Any]]:
    """Preserve transition time when condition status has not changed."""
    output = [dict(item) for item in existing if item.get("type") != desired.type]
    previous = next((item for item in existing if item.get("type") == desired.type), None)
    item = desired.to_dict()
    if previous and previous.get("status") == desired.status:
        item["lastTransitionTime"] = previous.get("lastTransitionTime", now_rfc3339())
    output.append(item)
    return sorted(output, key=lambda value: value["type"])


def condition_status(conditions: list[dict[str, Any]], condition_type: str) -> str | None:
    item = next((c for c in conditions if c.get("type") == condition_type), None)
    return None if item is None else str(item.get("status"))
