from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InvocationScenario:
    group: str
    plugin_name: str
    action_name: str
    config: dict[str, object]
    arguments: dict[str, object]


DEFAULT_DEMO_SCENARIO = InvocationScenario(
    group="delivery",
    plugin_name="console",
    action_name="deliver",
    config={
        "prefix": "[ops]",
        "uppercase_severity": True,
    },
    arguments={
        "title": "CPU high",
        "severity": "warning",
        "summary": "node-1 crossed 90%",
    },
)


DEFAULT_TRACE_SCENARIO = InvocationScenario(
    group="delivery",
    plugin_name="pager",
    action_name="preview",
    config={
        "service": "core",
        "routing_key": "sev1",
    },
    arguments={
        "title": "Queue lag",
        "severity": "critical",
        "summary": "worker backlog growing",
    },
)
