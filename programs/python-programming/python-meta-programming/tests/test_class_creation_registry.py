from __future__ import annotations

import unittest

from labs.class_creation.registry import (
    PluginRegistry,
    make_plugin_family,
    registry_evidence,
)


class PluginRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = PluginRegistry()
        _, self.PluginBase = make_plugin_family(self.registry)

    def test_abstract_family_classes_are_not_registered(self) -> None:
        class DeliveryPlugin(self.PluginBase):
            __abstract__ = True
            group = "delivery"

        self.assertEqual(self.registry.names("default"), ())
        self.assertEqual(self.registry.names("delivery"), ())

    def test_concrete_subclasses_register_without_opt_in(self) -> None:
        class DeliveryPlugin(self.PluginBase):
            __abstract__ = True
            group = "delivery"

        class Webhook(DeliveryPlugin):
            pass

        class Console(DeliveryPlugin):
            pass

        self.assertEqual(self.registry.names("delivery"), ("console", "webhook"))
        self.assertIs(self.registry.resolve("delivery", "webhook"), Webhook)

    def test_creation_trace_separates_shape_from_bookkeeping(self) -> None:
        class Console(self.PluginBase):
            group = "delivery"

        self.assertEqual(
            Console.__creation_trace__,
            (
                "new:Console:shape",
                "init:Console:bookkeeping",
                "register:delivery:console",
            ),
        )

    def test_duplicate_failure_preserves_the_original_registration(self) -> None:
        class Console(self.PluginBase):
            group = "delivery"
            plugin_name = "console"

        with self.assertRaisesRegex(
            ValueError,
            "duplicate plugin 'console' in group 'delivery'",
        ):

            class DuplicateConsole(self.PluginBase):
                group = "delivery"
                plugin_name = "console"

        self.assertIs(self.registry.resolve("delivery", "console"), Console)

    def test_registry_reset_is_explicit_and_group_scoped(self) -> None:
        class Console(self.PluginBase):
            group = "delivery"

        class Formatter(self.PluginBase):
            group = "formatting"

        self.registry.clear("delivery")

        self.assertEqual(self.registry.names("delivery"), ())
        self.assertEqual(self.registry.names("formatting"), ("formatter",))

    def test_evidence_names_scope_and_non_claims(self) -> None:
        evidence = registry_evidence()

        self.assertEqual(  # type: ignore[index]
            evidence["concrete_plugins"]["names_before_clear"],
            ["console", "webhook"],
        )
        self.assertTrue(evidence["duplicate"]["original_preserved"])  # type: ignore[index]
        self.assertEqual(evidence["reset"]["names_after_clear"], [])  # type: ignore[index]
        self.assertIn(  # type: ignore[operator]
            "registration alone does not prove a metaclass is smaller than __init_subclass__",
            evidence["claim_limits"],
        )


if __name__ == "__main__":
    unittest.main()
