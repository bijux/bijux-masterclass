from __future__ import annotations

import inspect
import unittest

from labs.wrapper_runtime.bounded_cache import CacheInfo, bounded_cache
from labs.wrapper_runtime.cache_demo import build_demo


class BoundedCacheLabTests(unittest.TestCase):
    def test_repeated_call_returns_cached_result_without_execution(self) -> None:
        executions: list[str] = []

        @bounded_cache(maxsize=2)
        def render(incident_id: str) -> object:
            executions.append(incident_id)
            return object()

        first = render("INC-42")
        second = render("INC-42")

        self.assertIs(first, second)
        self.assertEqual(executions, ["INC-42"])
        self.assertEqual(render.cache_info(), CacheInfo(1, 1, 2, 1))

    def test_recent_hit_changes_the_lru_eviction_candidate(self) -> None:
        executions: list[str] = []

        @bounded_cache(maxsize=2)
        def render(incident_id: str) -> str:
            executions.append(incident_id)
            return incident_id

        render("INC-41")
        render("INC-42")
        render("INC-41")
        render("INC-43")
        render("INC-42")

        self.assertEqual(
            executions,
            ["INC-41", "INC-42", "INC-43", "INC-42"],
        )
        self.assertEqual(render.cache_info(), CacheInfo(1, 4, 2, 2))

    def test_keyword_order_is_canonical_but_call_style_is_not_normalized(self) -> None:
        executions: list[tuple[str, str]] = []

        @bounded_cache(maxsize=None)
        def render(incident_id: str, severity: str) -> str:
            executions.append((incident_id, severity))
            return f"{incident_id}:{severity}"

        render(incident_id="INC-42", severity="critical")
        render(severity="critical", incident_id="INC-42")
        render("INC-42", "critical")

        self.assertEqual(
            executions,
            [
                ("INC-42", "critical"),
                ("INC-42", "critical"),
            ],
        )
        self.assertEqual(render.cache_info(), CacheInfo(1, 2, None, 2))

    def test_failed_calls_count_as_misses_but_are_not_cached(self) -> None:
        attempts = 0

        @bounded_cache(maxsize=2)
        def fail() -> None:
            nonlocal attempts
            attempts += 1
            raise RuntimeError("not cacheable")

        for _ in range(2):
            with self.assertRaisesRegex(RuntimeError, "not cacheable"):
                fail()

        self.assertEqual(attempts, 2)
        self.assertEqual(fail.cache_info(), CacheInfo(0, 2, 2, 0))

    def test_unhashable_arguments_fail_before_wrapped_execution(self) -> None:
        executions = 0

        @bounded_cache(maxsize=2)
        def count(values: list[int]) -> int:
            nonlocal executions
            executions += 1
            return len(values)

        with self.assertRaisesRegex(TypeError, "requires hashable arguments"):
            count([1, 2])

        self.assertEqual(executions, 0)
        self.assertEqual(count.cache_info(), CacheInfo(0, 0, 2, 0))

    def test_zero_capacity_and_clear_have_explicit_state_semantics(self) -> None:
        @bounded_cache(maxsize=0)
        def render(incident_id: str) -> str:
            return incident_id

        render("INC-42")
        render("INC-42")
        self.assertEqual(render.cache_info(), CacheInfo(0, 2, 0, 0))

        render.cache_clear()

        self.assertEqual(render.cache_info(), CacheInfo(0, 0, 0, 0))
        self.assertEqual(render.cache_snapshot(), ())

    def test_decorator_preserves_metadata_and_rejects_invalid_capacity(self) -> None:
        @bounded_cache(maxsize=2)
        def render(incident_id: str, *, severity: str = "warning") -> str:
            """Render an incident."""

            return f"{incident_id}:{severity}"

        self.assertEqual(render.__name__, "render")
        self.assertEqual(render.__doc__, "Render an incident.")
        self.assertEqual(
            str(inspect.signature(render)),
            "(incident_id: 'str', *, severity: 'str' = 'warning') -> 'str'",
        )
        self.assertIs(inspect.unwrap(render), render.__wrapped__)
        with self.assertRaisesRegex(ValueError, "non-negative or None"):
            bounded_cache(-1)

    def test_demo_exposes_cache_policy_and_observable_state(self) -> None:
        packet = build_demo()

        self.assertEqual(
            packet["underlying_executions"],
            [
                "INC-41:warning",
                "INC-42:critical",
                "INC-43:warning",
                "INC-41:warning",
            ],
        )
        self.assertEqual(
            packet["cache_info"],
            {"hits": 1, "misses": 4, "maxsize": 2, "current_size": 2},
        )
        self.assertEqual(
            packet["policy"],
            {
                "eviction": "least-recently-used",
                "failed_calls_cached": False,
                "thread_safe": False,
                "normalizes_equivalent_call_styles": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
