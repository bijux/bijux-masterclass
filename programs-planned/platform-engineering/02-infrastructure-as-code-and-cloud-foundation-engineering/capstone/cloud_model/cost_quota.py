from __future__ import annotations

from decimal import Decimal
from typing import Any


RECURRING_CLASSES = {
    "nat-gateway",
    "load-balancer",
    "compute",
    "block-storage",
    "object-storage",
    "logging",
    "data-transfer",
}


def evaluate_cost_profile(profile: dict[str, Any]) -> dict[str, Any]:
    monthly = sum(Decimal(str(row.get("monthlyEstimate", "0"))) for row in profile.get("items", []))
    budget = Decimal(str(profile.get("monthlyBudget", "0")))
    unowned = [row.get("name") for row in profile.get("items", []) if not row.get("owner")]
    unknown = [row.get("name") for row in profile.get("items", []) if row.get("evidence") == "unknown"]
    return {
        "estimatedMonthly": str(monthly),
        "budget": str(budget),
        "withinBudget": budget > 0 and monthly <= budget,
        "unownedItems": unowned,
        "unknownEvidenceItems": unknown,
        "decision": "pass" if budget > 0 and monthly <= budget and not unowned else "review",
    }


def evaluate_quotas(rows: list[dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for row in rows:
        limit = int(row["limit"])
        used = int(row["used"])
        required = int(row["requiredAdditional"])
        available = limit - used
        results.append({
            "name": row["name"],
            "available": available,
            "requiredAdditional": required,
            "sufficient": available >= required,
            "requestLeadDays": int(row.get("requestLeadDays", 0)),
        })
    return {"quotas": results, "allSufficient": all(r["sufficient"] for r in results)}
