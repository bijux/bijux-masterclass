from __future__ import annotations

import json
import unittest

from labs.descriptor_lookup.evidence import build_evidence, render_evidence


class DescriptorLookupEvidenceTests(unittest.TestCase):
    def test_protocol_packet_separates_set_name_from_descriptor_status(self) -> None:
        packet = build_evidence()["protocol"]

        self.assertEqual(packet["name_aware"]["kind"], "not-a-descriptor")
        self.assertTrue(packet["name_aware"]["has_set_name"])
        self.assertEqual(packet["stored_field"]["kind"], "data")
        self.assertTrue(packet["class_access_returns_descriptor"])

    def test_precedence_packet_names_each_winning_layer(self) -> None:
        packet = build_evidence()["precedence"]

        self.assertEqual(
            packet["decisions"]["enforced"]["winner"],
            "data-descriptor",
        )
        self.assertEqual(
            packet["decisions"]["shadowable"]["winner"],
            "instance-dictionary",
        )

    def test_quantity_packet_proves_canonical_independent_storage(self) -> None:
        packet = build_evidence()["quantity_field"]

        self.assertEqual(packet["first"]["canonical_value"], 0.25)
        self.assertEqual(packet["first"]["milliseconds"], 250.0)
        self.assertEqual(packet["second"]["canonical_value"], 2.0)
        self.assertNotEqual(
            packet["first"]["instance_dictionary"],
            packet["second"]["instance_dictionary"],
        )
        self.assertFalse(packet["descriptor_holds_instance_values"])
        self.assertIn("must be <= 30.0 s", packet["range_failure"])

    def test_rendered_evidence_is_stable_json(self) -> None:
        rendered = render_evidence()

        self.assertEqual(json.loads(rendered), build_evidence())
        self.assertEqual(
            list(json.loads(rendered)),
            ["method_binding", "precedence", "protocol", "quantity_field"],
        )


if __name__ == "__main__":
    unittest.main()
