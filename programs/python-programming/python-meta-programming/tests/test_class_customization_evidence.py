from __future__ import annotations

import json
import unittest

from labs.class_customization import TypedField
from labs.class_customization.evidence import build_evidence, render_evidence


class ClassCustomizationEvidenceTests(unittest.TestCase):
    def test_transformation_packet_exposes_post_construction_timing(self) -> None:
        packet = build_evidence()["class_transformation"]

        self.assertEqual(
            packet["events"],
            [
                "factory:outer",
                "factory:inner",
                "body:Delivery",
                "decorate:inner:Delivery",
                "decorate:outer:Delivery",
            ],
        )
        self.assertEqual(packet["application_trace"], ["inner", "outer"])
        self.assertTrue(packet["in_place_identity_preserved"])
        self.assertEqual(packet["customization"]["timing"], "after-class-creation")
        self.assertEqual(packet["metaclass"], "type")

    def test_dataclass_packet_separates_generation_validation_and_freezing(self) -> None:
        packet = build_evidence()["dataclass_boundary"]

        self.assertEqual(packet["generated_methods"], ["__init__", "__repr__", "__eq__"])
        self.assertTrue(packet["annotation_did_not_validate"])
        self.assertTrue(packet["default_factory_is_per_instance"])
        self.assertEqual(packet["nested_list_after_mutation"], ["urgent"])
        self.assertEqual(packet["rebinding_failure"], "FrozenInstanceError")
        self.assertFalse(packet["has_instance_dict"])

    def test_property_packet_proves_data_descriptor_precedence(self) -> None:
        packet = build_evidence()["property_boundary"]

        self.assertEqual(packet["visible_endpoint"], "https://example.test")
        self.assertEqual(packet["same_named_instance_entry"], "shadowed")
        self.assertTrue(packet["property_wins_over_instance_entry"])
        self.assertEqual(packet["invalid_assignment_failure"], "endpoint must use https")
        self.assertEqual(packet["descriptor_type"], "property")

    def test_descriptor_packet_exposes_reusable_owner_and_per_instance_state(self) -> None:
        packet = build_evidence()["descriptor_boundary"]

        self.assertEqual(packet["first"]["attempts"], 1)
        self.assertEqual(packet["second"]["attempts"], 2)
        self.assertEqual(
            packet["annotations_are_declarations"],
            {"endpoint": "str", "attempts": "int"},
        )
        self.assertIn("attempts must be int", packet["invalid_assignment_failure"])
        self.assertEqual(
            [field["name"] for field in packet["field_specs"]],
            ["endpoint", "attempts"],
        )

    def test_typed_field_returns_itself_from_class_access_and_rejects_unset_reads(self) -> None:
        class Delivery:
            attempts: int = TypedField(int)

        delivery = Delivery()

        self.assertIsInstance(Delivery.attempts, TypedField)
        with self.assertRaisesRegex(AttributeError, "attempts"):
            _ = delivery.attempts

    def test_frozen_packet_names_shallow_mutability_limit(self) -> None:
        packet = build_evidence()["frozen_surface"]

        self.assertFalse(packet["policy"]["deeply_immutable"])
        self.assertTrue(packet["policy"]["object_setattr_can_bypass"])
        self.assertEqual(packet["nested_list_after_mutation"], ["incident", "urgent"])
        self.assertIn("blocks attribute rebinding", packet["rebinding_failure"])

    def test_rendered_evidence_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            [
                "class_transformation",
                "dataclass_boundary",
                "descriptor_boundary",
                "frozen_surface",
                "property_boundary",
            ],
        )


if __name__ == "__main__":
    unittest.main()
