from __future__ import annotations

from ipaddress import ip_address, ip_network

from .models import Decision, NetworkPolicy, PolicyPeer, PolicyRule


def _peer_matches(
    peer: PolicyPeer,
    namespace: str,
    pod: str,
    address: str,
) -> bool:
    selector_present = peer.namespaces is not None or peer.pods is not None
    selector_match = True
    if peer.namespaces is not None:
        selector_match = selector_match and namespace in peer.namespaces
    if peer.pods is not None:
        selector_match = selector_match and pod in peer.pods

    cidr_match = False
    if peer.cidrs:
        peer_address = ip_address(address)
        cidr_match = any(
            peer_address in ip_network(cidr, strict=False) for cidr in peer.cidrs
        )
    return (selector_present and selector_match) or cidr_match


def _rule_matches(
    rule: PolicyRule,
    *,
    peer_namespace: str,
    peer_pod: str,
    peer_address: str,
    protocol: str,
    port: int,
) -> bool:
    port_allowed = not rule.ports or (protocol, port) in rule.ports
    peer_allowed = not rule.peers or any(
        _peer_matches(peer, peer_namespace, peer_pod, peer_address)
        for peer in rule.peers
    )
    return port_allowed and peer_allowed


def evaluate(
    policies: list[NetworkPolicy],
    *,
    src_namespace: str,
    src_pod: str,
    src_address: str,
    dst_namespace: str,
    dst_pod: str,
    dst_address: str,
    protocol: str,
    port: int,
) -> Decision:
    """Evaluate additive ingress and egress rules for one flow."""

    source_policies = [
        policy
        for policy in policies
        if policy.namespace == src_namespace
        and src_pod in policy.selected_pods
        and "Egress" in policy.policy_types
    ]
    destination_policies = [
        policy
        for policy in policies
        if policy.namespace == dst_namespace
        and dst_pod in policy.selected_pods
        and "Ingress" in policy.policy_types
    ]

    egress_allowed = not source_policies or any(
        _rule_matches(
            rule,
            peer_namespace=dst_namespace,
            peer_pod=dst_pod,
            peer_address=dst_address,
            protocol=protocol,
            port=port,
        )
        for policy in source_policies
        for rule in policy.egress
    )
    ingress_allowed = not destination_policies or any(
        _rule_matches(
            rule,
            peer_namespace=src_namespace,
            peer_pod=src_pod,
            peer_address=src_address,
            protocol=protocol,
            port=port,
        )
        for policy in destination_policies
        for rule in policy.ingress
    )

    allowed = egress_allowed and ingress_allowed
    return Decision(
        allowed,
        "Allowed" if allowed else "Denied",
        {
            "egressIsolated": bool(source_policies),
            "ingressIsolated": bool(destination_policies),
            "egressAllowed": egress_allowed,
            "ingressAllowed": ingress_allowed,
        },
    )
