import unittest

from atlas_net.models import Route
from atlas_net.mtu import Encapsulation, effective_mtu, packet_fits
from atlas_net.routing import RouteError, select_route, validate_non_overlapping


class RoutingTests(unittest.TestCase):
    def test_longest_prefix(self) -> None:
        routes = [
            Route("0.0.0.0/0", "192.0.2.1", "eth0"),
            Route("10.244.2.0/24", "192.0.2.12", "vxlan0", 10),
        ]

        selected, candidates = select_route("10.244.2.19", routes)

        self.assertEqual(selected.prefix, "10.244.2.0/24")
        self.assertEqual(len(candidates), 2)

    def test_no_route_for_other_address_family(self) -> None:
        with self.assertRaises(RouteError):
            select_route(
                "2001:db8::1",
                [Route("0.0.0.0/0", None, "eth0")],
            )

    def test_non_overlapping_address_domains(self) -> None:
        self.assertTrue(
            validate_non_overlapping(
                {
                    "pods": ["10.0.0.0/8"],
                    "services": ["10.96.0.0/12"],
                }
            )
        )

    def test_encapsulation_reduces_effective_mtu(self) -> None:
        mtu = effective_mtu(
            1500,
            [
                Encapsulation("vxlan", 50),
                Encapsulation("encryption", 32),
            ],
        )
        self.assertEqual(mtu, 1418)
        self.assertTrue(packet_fits(1200, mtu))
        self.assertFalse(packet_fits(1450, mtu))


if __name__ == "__main__":
    unittest.main()
