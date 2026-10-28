from __future__ import annotations

from typing import Iterable, Mapping, Any


def route_ticket(category: str, routes: Iterable[Mapping[str,Any]], *, catalog_owner: str | None = None) -> str:
    route=next((r for r in routes if r["category"]==category),None)
    if route is None:
        raise ValueError("unknown-support-category")
    if route.get("ownerSource") in {"api catalog entity owner","component catalog entity owner"}:
        if not catalog_owner:
            raise ValueError("catalog-owner-required")
        return catalog_owner
    return str(route["owner"])


def response_seconds(ticket: Mapping[str,Any]) -> float:
    from datetime import datetime
    parse=lambda v:datetime.fromisoformat(str(v).replace("Z","+00:00"))
    return (parse(ticket["firstResponseAt"])-parse(ticket["openedAt"])).total_seconds()
