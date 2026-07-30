from __future__ import annotations

import unittest

from labs.descriptor_lookup import (
    ShadowableValue,
    StoredField,
    explain_lookup,
    precedence_evidence,
)


class DescriptorPrecedenceLabTests(unittest.TestCase):
    def test_data_descriptor_beats_a_same_named_instance_entry(self) -> None:
        class Delivery:
            endpoint = StoredField()

        delivery = Delivery()
        delivery.endpoint = "descriptor-storage"
        vars(delivery)["endpoint"] = "attempted-shadow"

        decision = explain_lookup(Delivery, delivery, "endpoint")

        self.assertEqual(decision.winner, "data-descriptor")
        self.assertEqual(delivery.endpoint, "descriptor-storage")
        self.assertEqual(vars(delivery)["endpoint"], "attempted-shadow")

    def test_non_data_descriptor_yields_to_a_same_named_instance_entry(self) -> None:
        class Delivery:
            endpoint = ShadowableValue("descriptor-value")

        delivery = Delivery()
        self.assertEqual(delivery.endpoint, "descriptor-value")

        vars(delivery)["endpoint"] = "instance-value"
        decision = explain_lookup(Delivery, delivery, "endpoint")

        self.assertEqual(decision.winner, "instance-dictionary")
        self.assertEqual(delivery.endpoint, "instance-value")

    def test_non_data_descriptor_wins_when_the_instance_name_is_absent(self) -> None:
        class Delivery:
            endpoint = ShadowableValue("descriptor-value")

        delivery = Delivery()

        decision = explain_lookup(Delivery, delivery, "endpoint")

        self.assertEqual(decision.winner, "non-data-descriptor")
        self.assertEqual(delivery.endpoint, "descriptor-value")

    def test_plain_class_and_missing_attributes_are_classified_separately(self) -> None:
        class Delivery:
            category = "delivery"

        delivery = Delivery()

        self.assertEqual(
            explain_lookup(Delivery, delivery, "category").winner,
            "class-attribute",
        )
        self.assertEqual(
            explain_lookup(Delivery, delivery, "missing").winner,
            "missing",
        )

    def test_evidence_compares_predictions_with_actual_reads(self) -> None:
        packet = precedence_evidence()

        self.assertEqual(
            packet["decisions"]["enforced"]["winner"],
            "data-descriptor",
        )
        self.assertEqual(
            packet["decisions"]["shadowable"]["winner"],
            "instance-dictionary",
        )
        self.assertEqual(packet["actual_reads"]["enforced"], "descriptor-storage")
        self.assertEqual(packet["actual_reads"]["shadowable"], "instance-value")
        self.assertTrue(packet["ordinary_lookup_only"])


if __name__ == "__main__":
    unittest.main()
