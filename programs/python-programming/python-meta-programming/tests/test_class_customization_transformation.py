from __future__ import annotations

import unittest

from labs.class_customization import (
    ClassCustomization,
    mark_class,
    tracing_class_decorator,
)


class ClassCustomizationTransformationTests(unittest.TestCase):
    def test_class_decorator_receives_and_returns_the_created_class(self) -> None:
        class Delivery:
            pass

        original = Delivery
        decorated = mark_class("incident-delivery")(Delivery)

        self.assertIs(decorated, original)
        self.assertEqual(
            decorated.__class_customization__,
            ClassCustomization(
                label="incident-delivery",
                decorated_name="Delivery",
            ),
        )
        self.assertIs(type(decorated), type)

    def test_decorator_expression_precedes_body_and_application_is_bottom_up(self) -> None:
        events: list[str] = []

        @tracing_class_decorator("outer", events)
        @tracing_class_decorator("inner", events)
        class Delivery:
            events.append("body:Delivery")

        self.assertEqual(
            events,
            [
                "factory:outer",
                "factory:inner",
                "body:Delivery",
                "decorate:inner:Delivery",
                "decorate:outer:Delivery",
            ],
        )
        self.assertEqual(Delivery.__decorator_trace__, ("inner", "outer"))

    def test_factory_rejects_invalid_configuration_before_receiving_a_class(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be blank"):
            mark_class("  ")

    def test_decorator_rejects_collision_instead_of_overwriting_class_state(self) -> None:
        with self.assertRaisesRegex(TypeError, "already defines reserved"):

            @mark_class("incident-delivery")
            class Delivery:
                __class_customization__ = "owned by the class"

    def test_decorator_does_not_rewrite_instances_or_base_relationships(self) -> None:
        class DeliveryBase:
            pass

        @mark_class("incident-delivery")
        class ConsoleDelivery(DeliveryBase):
            pass

        instance = ConsoleDelivery()

        self.assertIsInstance(instance, ConsoleDelivery)
        self.assertIsInstance(instance, DeliveryBase)
        self.assertNotIn("__class_customization__", vars(instance))


if __name__ == "__main__":
    unittest.main()
