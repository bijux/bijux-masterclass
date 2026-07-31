from __future__ import annotations

import unittest

from labs.class_creation.namespace import (
    DeclarationMeta,
    DeclarationNamespace,
    namespace_evidence,
)


class DeclarationNamespaceTests(unittest.TestCase):
    def test_prepare_returns_the_mapping_used_for_the_class_body(self) -> None:
        namespace = DeclarationMeta.__prepare__("Delivery", ())

        self.assertIsInstance(namespace, DeclarationNamespace)

    def test_custom_namespace_records_public_declaration_order(self) -> None:
        class Delivery(metaclass=DeclarationMeta):
            endpoint = "https://example.test"
            attempts = 3

            def send(self) -> None:
                pass

        self.assertEqual(
            Delivery.__declaration_order__,
            ("endpoint", "attempts", "send"),
        )

    def test_duplicate_public_assignment_fails_during_body_execution(self) -> None:
        with self.assertRaisesRegex(
            TypeError,
            "duplicate public declaration: endpoint",
        ):

            class InvalidDelivery(metaclass=DeclarationMeta):
                endpoint = "first"
                endpoint = "second"

    def test_dunder_assignments_remain_available_to_python(self) -> None:
        class Delivery(metaclass=DeclarationMeta):
            pass

        self.assertEqual(Delivery.__name__, "Delivery")
        self.assertTrue(Delivery.__module__)

    def test_evidence_contrasts_custom_and_plain_namespace_behavior(self) -> None:
        evidence = namespace_evidence()

        self.assertEqual(  # type: ignore[index]
            evidence["duplicate_rule"]["message"],
            "duplicate public declaration: channel",
        )
        self.assertFalse(evidence["duplicate_rule"]["class_bound"])  # type: ignore[index]
        self.assertEqual(  # type: ignore[index]
            evidence["plain_mapping_limit"]["visible_value"],
            "webhook",
        )


if __name__ == "__main__":
    unittest.main()
