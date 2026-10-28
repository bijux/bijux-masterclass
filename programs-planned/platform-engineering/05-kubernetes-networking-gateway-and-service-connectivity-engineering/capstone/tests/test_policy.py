import unittest

from atlas_net.models import NetworkPolicy, PolicyPeer, PolicyRule
from atlas_net.policy import evaluate


class PolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policies = [
            NetworkPolicy(
                "api-ingress",
                "atlas-system",
                frozenset({"api"}),
                frozenset({"Ingress"}),
                ingress=(
                    PolicyRule(
                        (
                            PolicyPeer(
                                namespaces=frozenset({"gateway-system"}),
                                pods=frozenset({"gateway"}),
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

    def evaluate_gateway_flow(self, source_namespace: str, source_pod: str):
        return evaluate(
            self.policies,
            src_namespace=source_namespace,
            src_pod=source_pod,
            src_address="10.1.0.2",
            dst_namespace="atlas-system",
            dst_pod="api",
            dst_address="10.2.0.2",
            protocol="TCP",
            port=8080,
        )

    def test_allowed_both_sides(self) -> None:
        decision = self.evaluate_gateway_flow("gateway-system", "gateway")
        self.assertTrue(decision.allowed)

    def test_denied_ingress(self) -> None:
        decision = self.evaluate_gateway_flow("tenant-b", "attacker")
        self.assertFalse(decision.allowed)
        self.assertFalse(decision.details["ingressAllowed"])

    def test_unselected_workloads_are_default_allow(self) -> None:
        decision = evaluate(
            [],
            src_namespace="a",
            src_pod="x",
            src_address="10.0.0.1",
            dst_namespace="b",
            dst_pod="y",
            dst_address="10.0.0.2",
            protocol="TCP",
            port=1,
        )
        self.assertTrue(decision.allowed)


if __name__ == "__main__":
    unittest.main()
