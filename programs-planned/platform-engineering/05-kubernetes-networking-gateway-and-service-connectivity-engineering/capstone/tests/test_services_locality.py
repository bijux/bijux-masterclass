import unittest

from atlas_net.locality import choose
from atlas_net.models import Endpoint, Service
from atlas_net.services import ProgrammedService, select_backend


IPV4_LOCAL = Endpoint(
    "10.244.1.10",
    8080,
    "api-a",
    "node-a",
    "zone-a",
    family="IPv4",
)
IPV4_REMOTE = Endpoint(
    "10.244.2.10",
    8080,
    "api-b",
    "node-b",
    "zone-b",
    family="IPv4",
)
IPV6_LOCAL = Endpoint(
    "fd00:10:244::10",
    8080,
    "api-v6",
    "node-a",
    "zone-a",
    family="IPv6",
)
SERVICE = Service(
    "atlas-api",
    "atlas-system",
    8080,
    8080,
    ("10.96.0.10", "fd00:10:96::10"),
)


class ServiceTests(unittest.TestCase):
    def test_programmed_generation_can_lag_per_node(self) -> None:
        programmed = ProgrammedService(
            2,
            {"node-a": 1, "node-b": 2},
            {1: (IPV4_LOCAL, IPV4_REMOTE), 2: (IPV4_LOCAL,)},
        )

        self.assertEqual(len(programmed.endpoints_for_node("node-a")), 2)
        programmed.program("node-a", 2)
        self.assertEqual(len(programmed.endpoints_for_node("node-a")), 1)

    def test_selection_preserves_address_family(self) -> None:
        decision = select_backend(
            SERVICE,
            (IPV4_LOCAL, IPV6_LOCAL),
            client_node="node-a",
            client_zone="zone-a",
            client_key="client-1",
            family="IPv6",
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.details["endpoint"].family, "IPv6")

    def test_hard_locality_fails_without_local_endpoint(self) -> None:
        decision = choose(
            SERVICE,
            (IPV4_REMOTE,),
            client_node="node-a",
            client_zone="zone-a",
            client_key="client-1",
            family="IPv4",
            mode="hard-local",
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "NoLocalEndpoints")

    def test_prefer_locality_falls_back(self) -> None:
        decision = choose(
            SERVICE,
            (IPV4_REMOTE,),
            client_node="node-a",
            client_zone="zone-a",
            client_key="client-1",
            family="IPv4",
            mode="prefer-local",
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.details["endpoint"].zone, "zone-b")


if __name__ == "__main__":
    unittest.main()
