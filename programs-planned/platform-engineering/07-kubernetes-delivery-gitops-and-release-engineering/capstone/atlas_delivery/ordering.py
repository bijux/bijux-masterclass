from __future__ import annotations

from collections import defaultdict, deque

from .canonical import identity_string

PHASE_ORDER = {"PreSync": 0, "Sync": 1, "PostSync": 2, "SyncFail": 3, "PostDelete": 4}


def phase(resource: dict) -> str:
    annotations = resource.get("metadata", {}).get("annotations", {}) or {}
    return annotations.get("argocd.argoproj.io/hook", "Sync")


def wave(resource: dict) -> int:
    annotations = resource.get("metadata", {}).get("annotations", {}) or {}
    return int(annotations.get("argocd.argoproj.io/sync-wave", "0"))


def depends_on(resource: dict) -> list[str]:
    annotations = resource.get("metadata", {}).get("annotations", {}) or {}
    raw = annotations.get("delivery.atlas.dev/depends-on", "")
    return [item.strip() for item in raw.split(",") if item.strip()]


def ordered(resources: list[dict]) -> list[dict]:
    by_id = {identity_string(r): r for r in resources}
    indegree = {identity: 0 for identity in by_id}
    edges: dict[str, list[str]] = defaultdict(list)
    for identity, resource in by_id.items():
        for dependency in depends_on(resource):
            if dependency not in by_id:
                raise ValueError(f"missing dependency {dependency} for {identity}")
            edges[dependency].append(identity)
            indegree[identity] += 1
    ready = [identity for identity, degree in indegree.items() if degree == 0]
    ready.sort(key=lambda i: (PHASE_ORDER.get(phase(by_id[i]), 99), wave(by_id[i]), i))
    output: list[dict] = []
    while ready:
        identity = ready.pop(0)
        output.append(by_id[identity])
        for child in sorted(edges[identity]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort(key=lambda i: (PHASE_ORDER.get(phase(by_id[i]), 99), wave(by_id[i]), i))
    if len(output) != len(resources):
        raise ValueError("dependency cycle in delivery order")
    return output
