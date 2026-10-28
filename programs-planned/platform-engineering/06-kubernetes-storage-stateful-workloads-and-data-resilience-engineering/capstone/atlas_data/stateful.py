from __future__ import annotations

from .models import StatefulIdentity


class StatefulSetPlanner:
    def __init__(self, name: str, namespace: str, service_name: str, claim_templates: tuple[str, ...]):
        self.name = name
        self.namespace = namespace
        self.service_name = service_name
        self.claim_templates = claim_templates

    def identity(self, ordinal: int) -> StatefulIdentity:
        if ordinal < 0:
            raise ValueError("ordinal cannot be negative")
        pod = f"{self.name}-{ordinal}"
        claims = tuple(f"{template}-{pod}" for template in self.claim_templates)
        dns = f"{pod}.{self.service_name}.{self.namespace}.svc.cluster.local"
        return StatefulIdentity(pod, ordinal, claims, dns)

    def scale_identities(self, replicas: int) -> tuple[StatefulIdentity, ...]:
        if replicas < 0:
            raise ValueError("replicas cannot be negative")
        return tuple(self.identity(index) for index in range(replicas))

    def ordered_update(self, replicas: int, partition: int = 0) -> tuple[int, ...]:
        if partition < 0 or partition > replicas:
            raise ValueError("invalid partition")
        return tuple(index for index in reversed(range(partition, replicas)))
