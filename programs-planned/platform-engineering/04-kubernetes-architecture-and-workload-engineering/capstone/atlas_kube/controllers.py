from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import hashlib
import json

from .api_store import ApiStore, NotFound
from .models import KubeObject, ObjectMeta, Condition
from .conditions import merge_condition


def stable_hash(value: Any, length: int = 10) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()[:length]


def owner_reference(obj: KubeObject, *, controller: bool = True) -> dict[str, Any]:
    return {
        "apiVersion": obj.api_version,
        "kind": obj.kind,
        "name": obj.metadata.name,
        "uid": obj.metadata.uid,
        "controller": controller,
        "blockOwnerDeletion": controller,
    }


@dataclass(slots=True)
class ReconcileResult:
    writes: int
    reason: str
    requeue: bool = False


class DeploymentController:
    """A bounded, idempotent Deployment → ReplicaSet → Pod semantic controller."""

    def __init__(self, store: ApiStore) -> None:
        self.store = store

    def reconcile(self, deployment: KubeObject) -> ReconcileResult:
        before = len(self.store.writes)
        current = self.store.get(*deployment.key)
        namespace = current.metadata.namespace
        replicas = int(current.spec.get("replicas", 1))
        template = current.spec["template"]
        revision = stable_hash(template)
        rs_name = f"{current.metadata.name}-{revision}"
        rs = self.store.maybe_get("apps/v1", "ReplicaSet", namespace, rs_name)
        labels = dict(template.get("metadata", {}).get("labels", {}))
        labels["pod-template-hash"] = revision
        if rs is None:
            rs = KubeObject(
                "apps/v1", "ReplicaSet",
                ObjectMeta(
                    name=rs_name,
                    namespace=namespace,
                    labels={"app.kubernetes.io/name": current.metadata.name,
                            "pod-template-hash": revision},
                    owner_references=[owner_reference(current)],
                ),
                spec={"replicas": replicas, "selector": {"matchLabels": labels},
                      "template": template},
            )
            rs = self.store.create(rs, "deployment-controller")
        elif rs.spec.get("replicas") != replicas:
            rs.spec["replicas"] = replicas
            rs = self.store.replace(rs, rs.metadata.resource_version,
                                    "deployment-controller")

        pods = self.store.list(api_version="v1", kind="Pod", namespace=namespace,
                               labels={"pod-template-hash": revision})
        controlled = [p for p in pods if any(ref.get("uid") == rs.metadata.uid
                                             for ref in p.metadata.owner_references)]
        while len(controlled) < replicas:
            index = 0
            names = {p.metadata.name for p in controlled}
            while f"{rs_name}-{index}" in names:
                index += 1
            pod = KubeObject(
                "v1", "Pod",
                ObjectMeta(
                    name=f"{rs_name}-{index}", namespace=namespace,
                    labels=labels,
                    owner_references=[owner_reference(rs)],
                ),
                spec=dict(template.get("spec", {})),
                status={"phase": "Pending", "conditions": []},
            )
            controlled.append(self.store.create(pod, "replicaset-controller"))
        while len(controlled) > replicas:
            victim = sorted(controlled, key=lambda p: p.metadata.name)[-1]
            self.store.delete(victim, "replicaset-controller")
            controlled.remove(victim)

        ready = sum(
            1 for pod in controlled
            if any(c.get("type") == "Ready" and c.get("status") == "True"
                   for c in pod.status.get("conditions", []))
        )
        status = dict(current.status)
        status.update({
            "observedGeneration": current.metadata.generation,
            "replicas": len(controlled),
            "updatedReplicas": len(controlled),
            "readyReplicas": ready,
            "availableReplicas": ready,
            "conditions": merge_condition(
                status.get("conditions", []),
                Condition(
                    "Available", "True" if ready >= replicas else "False",
                    "MinimumReplicasAvailable" if ready >= replicas else "ReplicasNotReady",
                    f"{ready}/{replicas} replicas are ready",
                    current.metadata.generation,
                ),
            ),
        })
        self.store.update_status(current, status, "deployment-controller")
        return ReconcileResult(len(self.store.writes) - before, "reconciled")
