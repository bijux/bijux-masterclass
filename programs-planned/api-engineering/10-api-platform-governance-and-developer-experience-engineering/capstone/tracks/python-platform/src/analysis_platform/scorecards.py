from __future__ import annotations

from typing import Iterable, Mapping, Any


BLOCKING_KINDS={"ownership","compatibility","security","reliability"}


def scorecard(entity_ref: str, evidence: Iterable[Mapping[str,Any]]) -> dict[str,Any]:
    dimensions={e["kind"]:e["status"] for e in evidence if e["entityRef"]==entity_ref}
    blockers=sorted(kind for kind,status in dimensions.items() if kind in BLOCKING_KINDS and status!="pass")
    reviews=sorted(kind for kind,status in dimensions.items() if status=="review")
    status="blocked" if blockers else ("review" if reviews else "ready")
    return {"entityRef":entity_ref,"status":status,"dimensions":dimensions,"blockers":blockers,"reviews":reviews}
