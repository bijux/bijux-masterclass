from __future__ import annotations

import unittest

from labs.descriptor_systems.composition import (
    AuditWrites,
    DeliveryPolicy,
    FieldWrapper,
    NormalizeText,
    OneOf,
    StoredField,
    composition_evidence,
    describe_layers,
)


class DescriptorSystemCompositionTests(unittest.TestCase):
    def test_assignment_traces_normalization_validation_storage_and_audit(self) -> None:
        policy = DeliveryPolicy()

        policy.channel = " PAGER "

        self.assertEqual(policy.channel, "pager")
        self.assertEqual(
            [event["layer"] for event in vars(policy)["__field_trace__"]],
            ["NormalizeText", "OneOf", "StoredField", "AuditWrites"],
        )
        self.assertEqual(vars(policy)["__field_audit__"], [
            {"field": "channel", "stored": "pager"}
        ])

    def test_rejected_value_never_reaches_storage_or_audit(self) -> None:
        policy = DeliveryPolicy()

        with self.assertRaisesRegex(ValueError, "must be one of email, pager"):
            policy.channel = "console"

        self.assertNotIn("_channel", vars(policy))
        self.assertNotIn("__field_audit__", vars(policy))
        self.assertEqual(
            [
                event["accepted"]
                for event in vars(policy)["__field_trace__"]
                if "accepted" in event
            ],
            [False],
        )

    def test_each_layer_receives_set_name_once(self) -> None:
        layers = describe_layers(DeliveryPolicy.channel)

        self.assertEqual(
            [layer["type"] for layer in layers],
            ["AuditWrites", "NormalizeText", "OneOf", "StoredField"],
        )
        self.assertEqual([layer["binding_count"] for layer in layers], [1, 1, 1, 1])

    def test_class_access_keeps_the_outer_descriptor_inspectable(self) -> None:
        self.assertIsInstance(DeliveryPolicy.channel, AuditWrites)
        self.assertIsInstance(DeliveryPolicy.channel.inner, NormalizeText)
        self.assertIsInstance(DeliveryPolicy.channel.inner.inner, OneOf)
        self.assertIsInstance(DeliveryPolicy.channel.inner.inner.inner, StoredField)

    def test_wrapper_refuses_an_object_without_the_full_protocol(self) -> None:
        with self.assertRaisesRegex(TypeError, "missing descriptor hooks"):
            FieldWrapper(object())

    def test_evidence_names_each_owner_and_the_stack_limit(self) -> None:
        evidence = composition_evidence()

        self.assertEqual(evidence["accepted"]["stored"], "pager")
        self.assertFalse(evidence["rejected"]["stored"])
        self.assertFalse(evidence["rejected"]["audit_created"])
        self.assertFalse(evidence["cross_field_coordination"])
        self.assertEqual(
            [layer["responsibility"] for layer in evidence["layers"]],
            [
                "record accepted writes after storage succeeds",
                "strip surrounding whitespace and normalize case",
                "accept one value from an explicit choice set",
                "store one accepted value on the instance",
            ],
        )


if __name__ == "__main__":
    unittest.main()
