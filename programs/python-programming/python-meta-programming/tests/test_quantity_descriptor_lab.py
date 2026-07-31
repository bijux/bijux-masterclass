from __future__ import annotations

import unittest

from labs.descriptor_lookup import Quantity


class QuantityDescriptorLabTests(unittest.TestCase):
    def test_quantity_stores_one_canonical_representation_per_instance(self) -> None:
        class DeliveryTiming:
            latency = Quantity("s", {"s": 1.0, "ms": 0.001})

        first = DeliveryTiming()
        second = DeliveryTiming()
        first.latency = (250, "ms")
        second.latency = 2

        self.assertEqual(vars(first), {"_latency_canonical": 0.25})
        self.assertEqual(vars(second), {"_latency_canonical": 2.0})
        self.assertEqual(first.latency.canonical_value, 0.25)
        self.assertEqual(second.latency.canonical_value, 2.0)

    def test_quantity_read_can_convert_without_changing_storage(self) -> None:
        class DeliveryTiming:
            latency = Quantity("s", {"s": 1.0, "ms": 0.001})

        timing = DeliveryTiming()
        timing.latency = (1500, "ms")

        self.assertEqual(timing.latency.in_unit("s"), 1.5)
        self.assertEqual(timing.latency.in_unit("ms"), 1500.0)
        self.assertEqual(vars(timing), {"_latency_canonical": 1.5})

    def test_quantity_class_access_exposes_the_descriptor_and_spec(self) -> None:
        class DeliveryTiming:
            latency = Quantity(
                "s",
                {"s": 1.0, "ms": 0.001},
                minimum=0.0,
                maximum=30.0,
            )

        descriptor = vars(DeliveryTiming)["latency"]

        self.assertIs(DeliveryTiming.latency, descriptor)
        self.assertEqual(
            descriptor.spec().manifest(),
            {
                "name": "latency",
                "storage_name": "_latency_canonical",
                "canonical_unit": "s",
                "accepted_units": ["s", "ms"],
                "minimum": 0.0,
                "maximum": 30.0,
            },
        )

    def test_quantity_rejects_unknown_units_and_non_numeric_magnitudes(self) -> None:
        class DeliveryTiming:
            latency = Quantity("s", {"s": 1.0, "ms": 0.001})

        timing = DeliveryTiming()

        with self.assertRaisesRegex(ValueError, "does not accept unit"):
            timing.latency = (1, "minutes")
        with self.assertRaisesRegex(TypeError, "magnitude must be numeric"):
            timing.latency = ("fast", "s")  # type: ignore[assignment]
        with self.assertRaisesRegex(TypeError, "magnitude must be numeric"):
            timing.latency = True

    def test_quantity_rejects_non_finite_and_out_of_range_values(self) -> None:
        class DeliveryTiming:
            latency = Quantity(
                "s",
                {"s": 1.0, "ms": 0.001},
                minimum=0.0,
                maximum=30.0,
            )

        timing = DeliveryTiming()

        with self.assertRaisesRegex(ValueError, "must be finite"):
            timing.latency = float("inf")
        with self.assertRaisesRegex(ValueError, "must be >= 0.0 s"):
            timing.latency = -1
        with self.assertRaisesRegex(ValueError, "must be <= 30.0 s"):
            timing.latency = 31

    def test_quantity_rejects_incoherent_configuration_at_definition_time(self) -> None:
        with self.assertRaisesRegex(ValueError, "factor of 1.0"):
            Quantity("s", {"s": 1000.0})
        with self.assertRaisesRegex(ValueError, "positive"):
            Quantity("s", {"s": 1.0, "ms": 0.0})
        with self.assertRaisesRegex(ValueError, "minimum cannot exceed"):
            Quantity("s", {"s": 1.0}, minimum=2.0, maximum=1.0)


if __name__ == "__main__":
    unittest.main()
