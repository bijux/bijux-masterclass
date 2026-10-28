"""Field-level authorization policy used by the semantic gateway."""

from __future__ import annotations

from .model import AuthorizationError, Principal


FIELD_PERMISSIONS = {
    "Query.project": "PROJECT_READ",
    "Query.analysisRun": "RUN_READ",
    "Query.artifact": "ARTIFACT_READ",
    "Query.deliverySummary": "DELIVERY_READ",
    "AnalysisRun.artifacts": "ARTIFACT_READ",
    "AnalysisRun.deliverySummary": "DELIVERY_READ",
    "Mutation.createProject": "PROJECT_WRITE",
    "Mutation.startAnalysis": "RUN_WRITE",
    "Mutation.cancelAnalysis": "RUN_WRITE",
    "Subscription.analysisRunUpdated": "RUN_READ",
}


def require_field(
    principal: Principal,
    coordinate: str,
    *,
    resource_tenant: str | None = None,
) -> None:
    """Require both the field permission and the resource tenant boundary."""

    permission = FIELD_PERMISSIONS.get(coordinate)
    if permission is not None and permission not in principal.permissions:
        raise AuthorizationError(
            f"missing permission for {coordinate}"
        )

    if (
        resource_tenant is not None
        and principal.tenant_id != resource_tenant
    ):
        raise AuthorizationError("tenant mismatch")
