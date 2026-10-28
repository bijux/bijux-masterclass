from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .models import Decision, Principal, ResourceFacts


@dataclass(frozen=True, slots=True)
class Policy:
    operation_id: str
    scopes: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    relationship: str = "none"
    tenant_bound: bool = True
    conceal: bool = False
    required_assurance: str = "baseline"
    max_auth_age_seconds: int | None = None


def _relationship_allowed(name: str, principal: Principal, resource: ResourceFacts) -> bool:
    if name in {"none", "tenant-query", "tenant-create"}:
        return True
    if name == "owner":
        return resource.owner == principal.subject
    if name in {"owner-or-member", "project-member", "project-member-and-dataset", "project-member-completed-run"}:
        return resource.owner == principal.subject or principal.subject in resource.members
    if name in {"project-owner-or-writer", "project-owner", "tenant-owner"}:
        return resource.owner == principal.subject or "tenant-admin" in principal.roles
    if name == "project-owner-or-run-creator":
        return resource.owner == principal.subject or resource.creator == principal.subject or "tenant-admin" in principal.roles
    if name == "fresh-high-assurance":
        return "operator" in principal.roles
    return False


def authorize(
    operation_id: str,
    *,
    principal: Principal | None,
    resource: ResourceFacts,
    policies: Mapping[str, Policy],
) -> Decision:
    policy = policies.get(operation_id)
    if policy is None:
        return Decision(False, "policy.missing")
    if operation_id == "getHealth" and principal is None:
        return Decision(True, "policy.public")
    if principal is None:
        return Decision(False, "credential.required", policy.conceal)
    if not policy.scopes.issubset(principal.scopes):
        return Decision(False, "scope.insufficient", policy.conceal)
    if policy.roles and not policy.roles.intersection(principal.roles):
        return Decision(False, "role.insufficient", policy.conceal)
    if policy.tenant_bound and resource.tenant is not None and resource.tenant != principal.tenant:
        return Decision(False, "tenant.foreign", policy.conceal)
    if not _relationship_allowed(policy.relationship, principal, resource):
        return Decision(False, "relationship.denied", policy.conceal)
    if policy.required_assurance == "high" and principal.assurance != "high":
        return Decision(False, "assurance.insufficient", policy.conceal)
    if policy.max_auth_age_seconds is not None and principal.auth_age_seconds > policy.max_auth_age_seconds:
        return Decision(False, "authentication.stale", policy.conceal, ("step-up",))
    return Decision(True, "policy.allow", obligations=("audit",))
