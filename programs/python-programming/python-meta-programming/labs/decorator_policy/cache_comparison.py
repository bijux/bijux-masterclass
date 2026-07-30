from __future__ import annotations

from dataclasses import asdict
from functools import lru_cache

from labs.wrapper_runtime.bounded_cache import bounded_cache


def build_cache_comparison() -> dict[str, object]:
    """Compare the teaching cache with the standard-library policy surface."""

    bounded_executions: list[str] = []

    @bounded_cache(maxsize=2)
    def bounded_render(incident_id: str, severity: str) -> str:
        bounded_executions.append(f"{incident_id}:{severity}")
        return bounded_executions[-1]

    bounded_render(incident_id="INC-42", severity="critical")
    bounded_render(severity="critical", incident_id="INC-42")
    bounded_render("INC-42", "critical")

    standard_executions: list[str] = []

    @lru_cache(maxsize=2, typed=True)
    def standard_render(incident_id: int | float) -> str:
        standard_executions.append(type(incident_id).__name__)
        return standard_executions[-1]

    standard_render(42)
    standard_render(42.0)
    standard_render(42)
    standard_info = standard_render.cache_info()

    packet = {
        "teaching_cache": {
            "executions": bounded_executions,
            "info": asdict(bounded_render.cache_info()),
            "equivalent_keyword_order_is_one_key": True,
            "equivalent_call_styles_are_one_key": False,
            "thread_safe": False,
        },
        "stdlib_lru_cache": {
            "executions": standard_executions,
            "info": {
                "hits": standard_info.hits,
                "misses": standard_info.misses,
                "maxsize": standard_info.maxsize,
                "current_size": standard_info.currsize,
            },
            "parameters": standard_render.cache_parameters(),
            "typed_key_distinguishes_int_and_float": True,
            "thread_safe": True,
        },
    }

    bounded_render.cache_clear()
    standard_render.cache_clear()
    packet["after_clear"] = {
        "teaching_cache_size": bounded_render.cache_info().current_size,
        "stdlib_cache_size": standard_render.cache_info().currsize,
    }
    return packet
