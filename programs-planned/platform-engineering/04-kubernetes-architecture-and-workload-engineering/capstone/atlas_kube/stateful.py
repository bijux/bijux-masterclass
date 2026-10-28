from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StatefulIdentity:
    ordinal: int
    pod_name: str
    dns_name: str
    claim_name: str


def identities(name: str, service_name: str, namespace: str,
               claim_template: str, replicas: int) -> list[StatefulIdentity]:
    if replicas < 0:
        raise ValueError("replicas must be non-negative")
    return [
        StatefulIdentity(
            ordinal=i,
            pod_name=f"{name}-{i}",
            dns_name=f"{name}-{i}.{service_name}.{namespace}.svc",
            claim_name=f"{claim_template}-{name}-{i}",
        )
        for i in range(replicas)
    ]


def controller_fit(*, finite: bool, per_node: bool, stable_identity: bool,
                   continuously_running: bool) -> str:
    flags = sum((finite, per_node, stable_identity, continuously_running))
    if flags != 1:
        raise ValueError("the workload invariant must select one primary lifecycle")
    if finite:
        return "Job"
    if per_node:
        return "DaemonSet"
    if stable_identity:
        return "StatefulSet"
    return "Deployment"
