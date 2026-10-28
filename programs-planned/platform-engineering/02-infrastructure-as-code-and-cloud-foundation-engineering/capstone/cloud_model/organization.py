from __future__ import annotations

from typing import Any


REQUIRED_ACCOUNT_ROLES = {
    "management",
    "log-archive",
    "audit",
    "shared-services",
    "workload-nonprod",
    "workload-prod",
    "sandbox",
}


def validate_organization(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    accounts = model.get("accounts", [])
    roles = {a.get("role") for a in accounts}
    missing = sorted(REQUIRED_ACCOUNT_ROLES - roles)
    if missing:
        errors.append("missing account roles: " + ", ".join(missing))
    by_role = {a.get("role"): a for a in accounts}
    management = by_role.get("management", {})
    if management.get("workloads"):
        errors.append("organization management account must not host ordinary workloads")
    log_archive = by_role.get("log-archive", {})
    prod = by_role.get("workload-prod", {})
    if log_archive.get("id") and log_archive.get("id") == prod.get("id"):
        errors.append("log archive and production workload must not share an account")
    if log_archive.get("deleteAuthority") == "workload-admin":
        errors.append("workload administrators must not delete authoritative audit logs")
    identities = {i.get("name"): i for i in model.get("identities", [])}
    for name in ("plan", "apply", "workload", "audit", "break-glass"):
        if name not in identities:
            errors.append(f"missing identity class: {name}")
    if identities.get("plan", {}).get("canMutate"):
        errors.append("plan identity must not mutate cloud resources")
    if identities.get("workload", {}).get("canManageOrganization"):
        errors.append("workload identity must not manage the organization")
    if not model.get("accountLifecycle", {}).get("quarantine"):
        errors.append("account lifecycle must define quarantine")
    if not model.get("accountLifecycle", {}).get("retirement"):
        errors.append("account lifecycle must define retirement")
    return errors
