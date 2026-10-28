from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .authorization import Policy


def load_policy_matrix(path: Path) -> dict[str, Policy]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    result: dict[str, Policy] = {}
    for row in raw["policies"]:
        relationship = row["relationship"]
        scopes = frozenset(row.get("scopes", []))
        roles = frozenset(row.get("roles", []))
        result[row["operationId"]] = Policy(
            operation_id=row["operationId"],
            scopes=scopes,
            roles=roles,
            relationship=relationship,
            tenant_bound=bool(row.get("tenantBound", True)),
            conceal=row.get("concealment") == "concealed",
            required_assurance=row.get("assurance", "baseline"),
            max_auth_age_seconds=300 if row.get("freshAuthentication") else None,
        )
    return result
