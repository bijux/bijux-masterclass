from __future__ import annotations

import unittest

from labs.descriptor_lookup import (
    NameAware,
    ShadowableValue,
    StoredField,
    inspect_descriptor_protocol,
)


class DescriptorProtocolLabTests(unittest.TestCase):
    def test_set_name_alone_does_not_make_an_object_a_descriptor(self) -> None:
        class Delivery:
            marker = NameAware()

        marker = vars(Delivery)["marker"]
        protocol = inspect_descriptor_protocol(marker)

        self.assertEqual(marker.owner_name, "Delivery")
        self.assertEqual(marker.public_name, "marker")
        self.assertTrue(protocol.has_set_name)
        self.assertEqual(protocol.kind, "not-a-descriptor")

    def test_stored_field_is_a_data_descriptor_with_reviewable_class_access(self) -> None:
        class Delivery:
            endpoint = StoredField()

        descriptor = vars(Delivery)["endpoint"]
        protocol = inspect_descriptor_protocol(descriptor)

        self.assertEqual(protocol.kind, "data")
        self.assertTrue(protocol.has_get)
        self.assertTrue(protocol.has_set)
        self.assertIs(Delivery.endpoint, descriptor)
        self.assertEqual(descriptor.public_name, "endpoint")
        self.assertEqual(descriptor.storage_name, "_endpoint")

    def test_stored_field_keeps_values_on_each_instance(self) -> None:
        class Delivery:
            endpoint = StoredField()

        first = Delivery()
        second = Delivery()
        first.endpoint = "https://one.test"
        second.endpoint = "https://two.test"

        self.assertEqual(first.endpoint, "https://one.test")
        self.assertEqual(second.endpoint, "https://two.test")
        self.assertEqual(vars(first), {"_endpoint": "https://one.test"})
        self.assertEqual(vars(second), {"_endpoint": "https://two.test"})
        self.assertNotIn("value", vars(Delivery)["endpoint"].__dict__)

    def test_unset_stored_field_read_has_an_attribute_failure(self) -> None:
        class Delivery:
            endpoint = StoredField()

        with self.assertRaisesRegex(AttributeError, "endpoint is unset"):
            _ = Delivery().endpoint

    def test_get_only_descriptor_is_non_data(self) -> None:
        descriptor = ShadowableValue("descriptor")

        protocol = inspect_descriptor_protocol(descriptor)

        self.assertEqual(protocol.kind, "non-data")
        self.assertTrue(protocol.has_get)
        self.assertFalse(protocol.has_set)


if __name__ == "__main__":
    unittest.main()
