from atlas_net.models import NetworkPolicy, PolicyPeer, PolicyRule
from atlas_net.policy import evaluate

from common import emit, record


policies = [
    NetworkPolicy(
        "api-ingress",
        "atlas-system",
        frozenset({"api"}),
        frozenset({"Ingress"}),
        ingress=(
            PolicyRule(
                (
                    PolicyPeer(
                        namespaces=frozenset(
                            {"gateway-system", "atlas-clients"}
                        )
                    ),
                ),
                (("TCP", 8080),),
            ),
        ),
    ),
    NetworkPolicy(
        "gateway-egress",
        "gateway-system",
        frozenset({"gateway"}),
        frozenset({"Egress"}),
        egress=(
            PolicyRule(
                (
                    PolicyPeer(
                        namespaces=frozenset({"atlas-system"}),
                        pods=frozenset({"api"}),
                    ),
                ),
                (("TCP", 8080),),
            ),
        ),
    ),
]


def evaluate_flow(
    source_namespace: str,
    source_pod: str,
    destination_namespace: str,
    destination_pod: str,
    port: int = 8080,
):
    return evaluate(
        policies,
        src_namespace=source_namespace,
        src_pod=source_pod,
        src_address="10.1.0.2",
        dst_namespace=destination_namespace,
        dst_pod=destination_pod,
        dst_address="10.2.0.2",
        protocol="TCP",
        port=port,
    )


cases = {
    "gatewayToApi": record(
        evaluate_flow(
            "gateway-system",
            "gateway",
            "atlas-system",
            "api",
        )
    ),
    "attackerToApi": record(
        evaluate_flow(
            "tenant-b",
            "attacker",
            "atlas-system",
            "api",
        )
    ),
}

emit("module-05-network-policy.json", cases)
