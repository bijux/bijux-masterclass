from __future__ import annotations

import inspect
import unittest
import warnings
from typing import Any

from labs.decorator_policy import UnsupportedHintError, ValidationPolicy, validated


class DecoratorPolicyValidationTests(unittest.TestCase):
    def test_strict_mode_binds_defaults_and_rejects_wrong_argument_types(self) -> None:
        calls: list[tuple[str, str]] = []

        @validated()
        def render(incident_id: str, severity: str = "warning") -> str:
            calls.append((incident_id, severity))
            return f"{incident_id}:{severity}"

        self.assertEqual(render("INC-42"), "INC-42:warning")

        with self.assertRaisesRegex(TypeError, "argument incident_id=42"):
            render(42)  # type: ignore[arg-type]

        self.assertEqual(calls, [("INC-42", "warning")])

    def test_union_optional_and_any_form_the_supported_non_class_surface(self) -> None:
        @validated()
        def normalize(value: str | int | None, context: Any) -> str:
            return f"{value}:{context}"

        self.assertEqual(normalize(None, object()).split(":")[0], "None")
        self.assertEqual(normalize(7, "lab"), "7:lab")

        with self.assertRaisesRegex(TypeError, "expected str \\| int \\| None"):
            normalize(2.5, "lab")  # type: ignore[arg-type]

    def test_parameterized_generics_are_refused_when_the_function_is_decorated(self) -> None:
        with self.assertRaisesRegex(
            UnsupportedHintError,
            "values uses unsupported runtime hint list\\[int\\]",
        ):

            @validated()
            def total(values: list[int]) -> int:
                return sum(values)

    def test_disabled_return_validation_does_not_claim_to_check_returns(self) -> None:
        @validated(validate_return=False)
        def mislabeled() -> list[int]:
            return ["not", "integers"]  # type: ignore[list-item]

        self.assertEqual(mislabeled(), ["not", "integers"])
        self.assertFalse(mislabeled.__validation_policy__.validate_return)

    def test_strict_return_validation_runs_after_the_wrapped_function(self) -> None:
        calls = 0

        @validated()
        def mislabeled() -> str:
            nonlocal calls
            calls += 1
            return 42  # type: ignore[return-value]

        with self.assertRaisesRegex(TypeError, "return value 42"):
            mislabeled()

        self.assertEqual(calls, 1)

    def test_warning_mode_observes_a_mismatch_but_still_executes(self) -> None:
        calls: list[object] = []

        @validated(on_mismatch="warn", validate_return=False)
        def accept(value: str) -> object:
            calls.append(value)
            return value

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = accept(42)  # type: ignore[arg-type]

        self.assertEqual(result, 42)
        self.assertEqual(calls, [42])
        self.assertIn("argument value=42", str(caught[0].message))

    def test_factory_rejects_unknown_modes_before_it_receives_a_function(self) -> None:
        with self.assertRaisesRegex(ValueError, "on_mismatch"):
            validated(on_mismatch="ignore")  # type: ignore[arg-type]

    def test_wrapper_exposes_policy_hints_and_original_signature(self) -> None:
        @validated(on_mismatch="warn", validate_return=False)
        def render(incident_id: str, *, severity: str = "warning") -> str:
            """Render one incident."""

            return f"{incident_id}:{severity}"

        self.assertEqual(
            render.__validation_policy__,
            ValidationPolicy(on_mismatch="warn", validate_return=False),
        )
        self.assertEqual(
            {name: str(hint) for name, hint in render.__validated_hints__.items()},
            {"incident_id": "<class 'str'>", "severity": "<class 'str'>", "return": "<class 'str'>"},
        )
        self.assertEqual(render.__name__, "render")
        self.assertEqual(render.__doc__, "Render one incident.")
        self.assertEqual(
            str(inspect.signature(render)),
            "(incident_id: 'str', *, severity: 'str' = 'warning') -> 'str'",
        )
        self.assertIs(inspect.unwrap(render), render.__wrapped__)


if __name__ == "__main__":
    unittest.main()
