from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import copy

from .api_store import ApiStore
from .models import KubeObject, ObjectMeta, Condition, semantic_status_equal
from .conditions import merge_condition
from .controllers import DeploymentController, owner_reference

FINALIZER = "platform.bijux.dev/release-reservation"


@dataclass(slots=True)
class ReleaseReservationStore:
    reservations: set[str]
    deny_cleanup: bool = False

    def ensure(self, identity: str) -> bool:
        before = len(self.reservations)
        self.reservations.add(identity)
        return len(self.reservations) != before

    def remove(self, identity: str) -> bool:
        if self.deny_cleanup:
            raise PermissionError("release reservation cleanup denied")
        existed = identity in self.reservations
        self.reservations.discard(identity)
        return existed


class AtlasController:
    def __init__(self, store: ApiStore,
                 reservations: ReleaseReservationStore | None = None) -> None:
        self.store = store
        self.reservations = reservations or ReleaseReservationStore(set())
        self.deployment_controller = DeploymentController(store)

    def _deployment(self, cr: KubeObject, component: str, image: str,
                    replicas: int, port: int | None) -> KubeObject:
        labels = {
            "app.kubernetes.io/name": f"atlas-{component}",
            "app.kubernetes.io/part-of": "atlas",
            "app.kubernetes.io/managed-by": "atlas-controller",
        }
        container: dict[str, Any] = {
            "name": f"atlas-{component}",
            "image": image,
            "securityContext": {
                "runAsNonRoot": True,
                "runAsUser": 65532,
                "runAsGroup": 65532,
                "allowPrivilegeEscalation": False,
                "readOnlyRootFilesystem": True,
                "capabilities": {"drop": ["ALL"]},
            },
            "resources": {
                "requests": {"cpu": "100m", "memory": "64Mi"},
                "limits": {"cpu": "500m", "memory": "128Mi"},
            },
            "volumeMounts": [{"name": "tmp", "mountPath": "/tmp"}],
        }
        if port is not None:
            container["ports"] = [{"name": "http", "containerPort": port}]
            container["livenessProbe"] = {"httpGet": {"path": "/live", "port": "http"}}
            container["readinessProbe"] = {"httpGet": {"path": "/ready", "port": "http"}}
        pod_spec: dict[str, Any] = {
            "serviceAccountName": f"atlas-{component}",
            "automountServiceAccountToken": False,
            "terminationGracePeriodSeconds": 30,
            "securityContext": {"runAsNonRoot": True, "seccompProfile": {"type": "RuntimeDefault"}},
            "containers": [container],
            "volumes": [{"name": "tmp", "emptyDir": {"sizeLimit": "64Mi"}}],
        }
        if component == "worker":
            container["volumeMounts"].extend([
                {"name": "spool", "mountPath": "/var/lib/atlas/spool"},
                {"name": "results", "mountPath": "/var/lib/atlas/results"},
            ])
            pod_spec["volumes"].extend([
                {"name": "spool", "persistentVolumeClaim": {"claimName": "atlas-worker-spool"}},
                {"name": "results", "persistentVolumeClaim": {"claimName": "atlas-worker-results"}},
            ])
        return KubeObject(
            "apps/v1", "Deployment",
            ObjectMeta(
                name=f"atlas-{component}", namespace=cr.metadata.namespace,
                labels=labels, owner_references=[owner_reference(cr)],
            ),
            spec={
                "replicas": replicas,
                "selector": {"matchLabels": labels},
                "strategy": {"type": "RollingUpdate", "rollingUpdate": {
                    "maxSurge": 1, "maxUnavailable": 0}},
                "template": {"metadata": {"labels": labels}, "spec": pod_spec},
            },
        )

    def reconcile(self, cr: KubeObject, *, churn_status: bool = False) -> int:
        before = len(self.store.writes)
        current = self.store.get(*cr.key)
        reservation = f"{current.metadata.namespace}/{current.metadata.name}"
        if current.metadata.deletion_timestamp:
            try:
                self.reservations.remove(reservation)
            except PermissionError as exc:
                status = copy.deepcopy(current.status)
                status["conditions"] = merge_condition(
                    status.get("conditions", []),
                    Condition("Ready", "False", "CleanupDenied", str(exc), current.metadata.generation),
                )
                self.store.update_status(current, status, "atlas-controller")
                return len(self.store.writes) - before
            self.store.delete_owned_by(current.metadata.uid)
            self.store.remove_finalizer(current, FINALIZER, "atlas-controller")
            return len(self.store.writes) - before

        if FINALIZER not in current.metadata.finalizers:
            current = self.store.add_finalizer(current, FINALIZER, "atlas-controller")
        self.reservations.ensure(reservation)
        desired = [
            self._deployment(current, "api", current.spec["apiImage"],
                             int(current.spec.get("apiReplicas", 3)), 8080),
            self._deployment(current, "worker", current.spec["workerImage"],
                             int(current.spec.get("workerReplicas", 1)), None),
        ]
        for child in desired:
            existing = self.store.maybe_get(*child.key)
            if existing is None:
                existing = self.store.create(child, "atlas-controller")
            elif existing.spec != child.spec or existing.metadata.labels != child.metadata.labels:
                child.metadata.uid = existing.metadata.uid
                child.metadata.resource_version = existing.metadata.resource_version
                child.metadata.generation = existing.metadata.generation
                existing = self.store.replace(child, existing.metadata.resource_version,
                                              "atlas-controller")
            self.deployment_controller.reconcile(existing)

        current = self.store.get(*current.key)
        deployments = self.store.list(api_version="apps/v1", kind="Deployment",
                                      namespace=current.metadata.namespace)
        owned = [d for d in deployments if any(ref.get("uid") == current.metadata.uid
                                               for ref in d.metadata.owner_references)]
        ready = all(d.status.get("availableReplicas", 0) >= d.spec.get("replicas", 1)
                    for d in owned) and len(owned) == 2
        status = copy.deepcopy(current.status)
        status.update({
            "observedGeneration": current.metadata.generation,
            "childDeployments": sorted(d.metadata.name for d in owned),
            "conditions": merge_condition(
                status.get("conditions", []),
                Condition(
                    "Ready", "True" if ready else "False",
                    "ChildrenAvailable" if ready else "ChildrenProgressing",
                    "all child deployments are available" if ready else "waiting for child readiness",
                    current.metadata.generation,
                ),
            ),
        })
        if churn_status:
            # Deliberate defect used by the course: semantically meaningless write.
            status["reconcileNonce"] = str(len(self.store.writes))
        if not semantic_status_equal(current.status, status) or churn_status:
            self.store.update_status(current, status, "atlas-controller")
        return len(self.store.writes) - before
