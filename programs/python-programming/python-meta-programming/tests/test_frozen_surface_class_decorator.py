from __future__ import annotations

import inspect
import unittest

from labs.class_customization import (
    FrozenSurfaceError,
    FrozenSurfacePolicy,
    surface_frozen,
)


class FrozenSurfaceClassDecoratorTests(unittest.TestCase):
    def test_initialization_succeeds_before_rebinding_and_deletion_are_blocked(self) -> None:
        @surface_frozen
        class DeliveryConfig:
            def __init__(self, endpoint: str) -> None:
                self.endpoint = endpoint
                self.attempts = 1

        config = DeliveryConfig("https://example.test")

        self.assertEqual(config.endpoint, "https://example.test")
        with self.assertRaisesRegex(FrozenSurfaceError, "blocks attribute rebinding"):
            config.endpoint = "https://other.test"
        with self.assertRaisesRegex(FrozenSurfaceError, "blocks attribute deletion"):
            del config.attempts

    def test_policy_names_mutability_and_bypass_limits(self) -> None:
        @surface_frozen
        class DeliveryConfig:
            def __init__(self) -> None:
                self.tags = ["incident"]

        config = DeliveryConfig()
        config.tags.append("urgent")
        object.__setattr__(config, "added_by_bypass", True)

        self.assertEqual(config.tags, ["incident", "urgent"])
        self.assertTrue(config.added_by_bypass)
        self.assertEqual(config.__surface_frozen__, FrozenSurfacePolicy())
        self.assertFalse(config.__surface_frozen__.deeply_immutable)

    def test_original_attribute_policy_still_runs_during_initialization(self) -> None:
        events: list[str] = []

        @surface_frozen
        class DeliveryConfig:
            def __setattr__(self, name: str, value: object) -> None:
                events.append(f"set:{name}")
                super().__setattr__(name, value)

            def __init__(self, endpoint: str) -> None:
                self.endpoint = endpoint

        config = DeliveryConfig("https://example.test")

        self.assertEqual(events, ["set:endpoint"])
        with self.assertRaises(FrozenSurfaceError):
            config.endpoint = "https://other.test"
        self.assertEqual(events, ["set:endpoint"])

    def test_wrapped_initializer_preserves_signature_and_provenance(self) -> None:
        @surface_frozen
        class DeliveryConfig:
            def __init__(self, endpoint: str, *, attempts: int = 1) -> None:
                """Initialize delivery configuration."""

                self.endpoint = endpoint
                self.attempts = attempts

        self.assertEqual(
            str(inspect.signature(DeliveryConfig)),
            "(endpoint: 'str', *, attempts: 'int' = 1) -> 'None'",
        )
        self.assertEqual(
            DeliveryConfig.__init__.__doc__,
            "Initialize delivery configuration.",
        )
        self.assertIs(
            inspect.unwrap(DeliveryConfig.__init__),
            DeliveryConfig.__init__.__wrapped__,
        )

    def test_slotted_classes_are_refused_instead_of_half_supported(self) -> None:
        with self.assertRaisesRegex(TypeError, "requires instances with a __dict__"):

            @surface_frozen
            class SlottedConfig:
                __slots__ = ("endpoint",)

                def __init__(self, endpoint: str) -> None:
                    self.endpoint = endpoint

    def test_subclass_can_replace_the_boundary_as_the_policy_warns(self) -> None:
        @surface_frozen
        class DeliveryConfig:
            def __init__(self, endpoint: str) -> None:
                self.endpoint = endpoint

        class MutableDeliveryConfig(DeliveryConfig):
            def __setattr__(self, name: str, value: object) -> None:
                object.__setattr__(self, name, value)

        config = MutableDeliveryConfig("https://example.test")
        config.endpoint = "https://other.test"

        self.assertEqual(config.endpoint, "https://other.test")
        self.assertTrue(DeliveryConfig.__surface_frozen__.subclass_can_override_boundary)


if __name__ == "__main__":
    unittest.main()
