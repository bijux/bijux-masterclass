from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

HealthStatus = Literal["Healthy", "Progressing", "Degraded", "Unknown"]


@dataclass(frozen=True)
class Health:
    status: HealthStatus
    reason: str


def assess(resource: dict) -> Health:
    kind = resource.get("kind")
    metadata = resource.get("metadata", {})
    spec = resource.get("spec", {})
    status = resource.get("status", {})
    generation = metadata.get("generation")
    observed = status.get("observedGeneration")
    if generation is not None and observed is not None and observed != generation:
        return Health("Progressing", "status has not observed current generation")
    if kind == "Deployment":
        desired = int(spec.get("replicas", 1))
        available = int(status.get("availableReplicas", 0))
        if status.get("conditions"):
            for condition in status["conditions"]:
                if condition.get("type") == "Progressing" and condition.get("status") == "False":
                    return Health("Degraded", str(condition.get("reason", "progress deadline")))
        return Health("Healthy", "available replicas satisfy desired") if available >= desired else Health("Progressing", f"{available}/{desired} available")
    if kind == "StatefulSet":
        desired = int(spec.get("replicas", 1))
        ready = int(status.get("readyReplicas", 0))
        return Health("Healthy", "all identities ready") if ready >= desired else Health("Progressing", f"{ready}/{desired} ready")
    if kind == "Job":
        if int(status.get("failed", 0)) > 0:
            return Health("Degraded", "job failed")
        if int(status.get("succeeded", 0)) >= int(spec.get("completions", 1)):
            return Health("Healthy", "job completed")
        return Health("Progressing", "job incomplete")
    conditions = status.get("conditions") or []
    for condition in conditions:
        if condition.get("type") == "Ready":
            if condition.get("status") == "True":
                return Health("Healthy", str(condition.get("reason", "Ready")))
            if condition.get("status") == "False":
                return Health("Degraded", str(condition.get("reason", "NotReady")))
    return Health("Unknown", "no authoritative health rule")
