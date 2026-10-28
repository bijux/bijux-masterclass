from __future__ import annotations

from datetime import datetime
from statistics import median
from typing import Iterable, Mapping, Any


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z","+00:00"))


def product_metrics(events: Iterable[Mapping[str,Any]], deprecated_versions: set[tuple[str,str]]) -> dict[str,Any]:
    items=sorted((dict(e) for e in events),key=lambda e:e["at"])
    issued: dict[tuple[str,str],datetime]={}
    first_success_seconds=[]
    active_consumers=set()
    deprecated_uses=0
    for event in items:
        key=(event["consumerId"],event["apiRef"])
        if event["event"]=="credential_issued":
            issued[key]=_dt(event["at"])
        elif event["event"]=="first_success" and key in issued:
            first_success_seconds.append((_dt(event["at"])-issued[key]).total_seconds())
            active_consumers.add(event["consumerId"])
        elif event["event"]=="active_use":
            active_consumers.add(event["consumerId"])
        if (event["apiRef"],event["version"]) in deprecated_versions and event["event"] in {"active_use","first_success"}:
            deprecated_uses+=1
    return {
        "activeConsumers":len(active_consumers),
        "medianTimeToFirstSuccessSeconds":median(first_success_seconds) if first_success_seconds else None,
        "deprecatedVersionUses":deprecated_uses,
    }


def search_success(events: Iterable[Mapping[str,Any]]) -> dict[str,float]:
    items=list(events); zero=sum(1 for e in items if int(e["results"])==0)
    return {"queries":len(items),"zeroResultRate":zero/len(items) if items else 0.0}
