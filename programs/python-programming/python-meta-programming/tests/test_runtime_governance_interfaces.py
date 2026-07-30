from __future__ import annotations

import unittest

from labs.runtime_governance.interfaces import (
    DeliveryABC,
    DeliveryProtocol,
    PreviewCapable,
    interface_evidence,
)


class InterfaceGovernanceTests(unittest.TestCase):
    def test_abc_blocks_instantiation_not_class_creation(self) -> None:
        class MissingDelivery(DeliveryABC):
            pass

        self.assertTrue(isinstance(MissingDelivery, type))
        with self.assertRaisesRegex(TypeError, "abstract method"):
            MissingDelivery()

    def test_complete_nominal_subclass_satisfies_the_runtime_contract(self) -> None:
        class ConsoleDelivery(DeliveryABC):
            def deliver(self, message: str) -> str:
                return f"console:{message}"

        self.assertEqual(ConsoleDelivery().deliver("incident"), "console:incident")

    def test_runtime_protocol_check_does_not_validate_signature(self) -> None:
        class WrongSignature:
            def deliver(self) -> str:
                return "delivered"

        self.assertIsInstance(WrongSignature(), DeliveryProtocol)
        with self.assertRaises(TypeError):
            WrongSignature().deliver("incident")  # type: ignore[call-arg]

    def test_subclass_hook_uses_static_class_dictionaries(self) -> None:
        class StaticPreview:
            def preview(self) -> str:
                return "preview"

        class DynamicPreview:
            def __getattr__(self, name: str) -> object:
                return lambda: "dynamic"

        self.assertTrue(issubclass(StaticPreview, PreviewCapable))
        self.assertFalse(issubclass(DynamicPreview, PreviewCapable))

    def test_evidence_assigns_a_distinct_claim_to_each_tool(self) -> None:
        evidence = interface_evidence()

        self.assertFalse(evidence["abc"]["incomplete_instance_created"])  # type: ignore[index]
        self.assertTrue(  # type: ignore[index]
            evidence["protocol"]["wrong_signature_passes_runtime_check"],
        )
        self.assertFalse(  # type: ignore[index]
            evidence["subclass_hook"]["instance_fallback_executed"],
        )


if __name__ == "__main__":
    unittest.main()
