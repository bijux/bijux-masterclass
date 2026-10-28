from __future__ import annotations

from .models import Decision, Endpoint, Service
from .services import select_backend


def choose(
    service: Service,
    endpoints: tuple[Endpoint, ...],
    *,
    client_node: str,
    client_zone: str,
    client_key: str,
    family: str,
    mode: str,
) -> Decision:
    if mode == "hard-local":
        local_service = Service(
            name=service.name,
            namespace=service.namespace,
            port=service.port,
            target_port=service.target_port,
            cluster_ips=service.cluster_ips,
            internal_traffic_policy="Local",
            external_traffic_policy=service.external_traffic_policy,
            session_affinity=service.session_affinity,
        )
        return select_backend(
            local_service,
            endpoints,
            client_node=client_node,
            client_zone=client_zone,
            client_key=client_key,
            family=family,
        )
    if mode == "prefer-local":
        return select_backend(
            service,
            endpoints,
            client_node=client_node,
            client_zone=client_zone,
            client_key=client_key,
            family=family,
            topology_preference=True,
        )
    if mode == "cluster":
        return select_backend(
            service,
            endpoints,
            client_node=client_node,
            client_zone=client_zone,
            client_key=client_key,
            family=family,
        )
    raise ValueError(f"unknown locality mode: {mode}")
