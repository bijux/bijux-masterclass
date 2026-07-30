from __future__ import annotations

import inspect
import json
from dataclasses import asdict

from .bounded_cache import bounded_cache


def build_demo() -> dict[str, object]:
    executions: list[str] = []

    @bounded_cache(maxsize=2)
    def render_alert(incident_id: str, *, severity: str = "warning") -> str:
        executions.append(f"{incident_id}:{severity}")
        return f"{incident_id}:{severity}"

    results = [
        render_alert("INC-41"),
        render_alert("INC-41"),
        render_alert("INC-42", severity="critical"),
        render_alert("INC-43"),
        render_alert("INC-41"),
    ]
    return {
        "results": results,
        "underlying_executions": executions,
        "cache_info": asdict(render_alert.cache_info()),
        "least_to_most_recent_keys": [
            {
                "args": list(args),
                "kwargs": dict(kwargs),
            }
            for args, kwargs in render_alert.cache_snapshot()
        ],
        "metadata": {
            "name": render_alert.__name__,
            "signature": str(inspect.signature(render_alert)),
            "has_wrapped": hasattr(render_alert, "__wrapped__"),
        },
        "policy": {
            "eviction": "least-recently-used",
            "failed_calls_cached": False,
            "thread_safe": False,
            "normalizes_equivalent_call_styles": False,
        },
    }


def main() -> int:
    print(json.dumps(build_demo(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
