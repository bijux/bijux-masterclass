import unittest

from atlas_net.gateway import (
    attach,
    canonical_forwarded,
    retry_allowed,
    select_route,
)
from atlas_net.models import Certificate, HttpMatch, HttpRoute, Listener
from atlas_net.tls import select_certificate, verify_backend


class GatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.listener = Listener(
            "https",
            "atlas.example.invalid",
            443,
            "HTTPS",
            "atlas-cert",
            frozenset({"atlas-system"}),
        )
        self.route = HttpRoute(
            "atlas",
            "atlas-system",
            "atlas-gateway",
            "https",
            ("atlas.example.invalid",),
            (HttpMatch(path="/api"),),
            "atlas-system",
            "atlas-api",
            8080,
        )

    def test_attach(self) -> None:
        self.assertTrue(attach(self.listener, self.route, []).allowed)

    def test_unauthorized_namespace(self) -> None:
        route = HttpRoute(
            "bad",
            "tenant-b",
            "atlas-gateway",
            "https",
            ("atlas.example.invalid",),
            (HttpMatch(),),
            "tenant-b",
            "evil",
            80,
        )
        self.assertFalse(attach(self.listener, route, []).allowed)

    def test_route_selection(self) -> None:
        decision = select_route(
            [self.route],
            self.listener,
            host="atlas.example.invalid",
            path="/api/runs",
            method="GET",
            headers={},
            grants=[],
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.details["route"], "atlas")

    def test_forwarded_identity_is_replaced(self) -> None:
        headers = canonical_forwarded(
            "203.0.113.7",
            "https",
            "atlas.example.invalid",
            {"X-Forwarded-For": "forged", "A": "b"},
        )
        self.assertEqual(headers["X-Forwarded-For"], "203.0.113.7")
        self.assertEqual(headers["A"], "b")

    def test_retry_requires_idempotency_for_post(self) -> None:
        self.assertFalse(retry_allowed("POST", None, True, 500).allowed)
        self.assertTrue(retry_allowed("POST", "key-1", True, 500).allowed)

    def test_certificate_and_backend_identity(self) -> None:
        certificate = Certificate(
            "atlas-cert",
            ("atlas.example.invalid",),
            "atlas-ca",
            0,
            100,
        )
        self.assertTrue(
            select_certificate(
                [certificate],
                "atlas.example.invalid",
                now=50,
            ).allowed
        )
        self.assertTrue(
            verify_backend(
                "atlas.example.invalid",
                certificate,
                {"atlas-ca"},
                now=50,
            ).allowed
        )


if __name__ == "__main__":
    unittest.main()
