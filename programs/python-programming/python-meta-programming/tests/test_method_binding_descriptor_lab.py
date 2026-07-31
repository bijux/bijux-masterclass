from __future__ import annotations

import unittest

from labs.descriptor_lookup import inspect_method_binding, method_binding_evidence


class MethodBindingDescriptorLabTests(unittest.TestCase):
    def test_instance_access_binds_the_original_function_to_self(self) -> None:
        class Delivery:
            def render(self, title: str) -> str:
                return title

        delivery = Delivery()

        binding = inspect_method_binding(Delivery, delivery, "render")

        self.assertEqual(binding.static_type, "function")
        self.assertEqual(binding.descriptor_kind, "non-data")
        self.assertEqual(binding.class_access_type, "function")
        self.assertEqual(binding.instance_access_type, "method")
        self.assertTrue(binding.class_access_is_function)
        self.assertTrue(binding.bound_function_is_static_function)
        self.assertTrue(binding.bound_self_is_instance)

    def test_bound_method_exposes_func_and_self_identities(self) -> None:
        class Delivery:
            def render(self, title: str) -> str:
                return title

        delivery = Delivery()
        bound = delivery.render

        self.assertIs(bound.__func__, vars(Delivery)["render"])
        self.assertIs(bound.__self__, delivery)
        self.assertEqual(bound("CPU high"), "CPU high")

    def test_function_descriptor_can_be_shadowed_on_one_instance(self) -> None:
        class Delivery:
            def render(self) -> str:
                return "method"

        first = Delivery()
        second = Delivery()
        vars(first)["render"] = "replacement"

        self.assertEqual(first.render, "replacement")
        self.assertEqual(second.render(), "method")

    def test_evidence_keeps_binding_and_invocation_separate(self) -> None:
        packet = method_binding_evidence()

        self.assertTrue(packet["binding"]["bound_self_is_instance"])
        self.assertTrue(packet["binding"]["bound_function_is_static_function"])
        self.assertEqual(packet["bound_call_result"], "[incident]: CPU high")
        self.assertTrue(packet["shadowing_is_possible"])


if __name__ == "__main__":
    unittest.main()
