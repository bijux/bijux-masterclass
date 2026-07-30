from __future__ import annotations

import importlib
import json
import sys
import types
from collections.abc import Mapping


SEVERITY_LABELS = {"warning": "WARN", "critical": "CRIT"}


class IncidentFormatter:
    """Small domain object used to expose ordinary runtime relationships."""

    def render(self, title: str, severity: str) -> str:
        return f"{SEVERITY_LABELS[severity]}: {title}"


def function_evidence() -> dict[str, object]:
    """Observe a closure without treating code-object details as application policy."""

    def make_prefixer(prefix: str):
        def prefix_title(title: str) -> str:
            return f"{prefix}: {title}"

        return prefix_title

    prefix_title = make_prefixer("incident")
    return {
        "callable": callable(prefix_title),
        "name": prefix_title.__name__,
        "qualname_has_enclosing_scope": "make_prefixer.<locals>" in prefix_title.__qualname__,
        "module": prefix_title.__module__,
        "free_variables": list(prefix_title.__code__.co_freevars),
        "result": prefix_title("queue lag"),
    }


def class_evidence() -> dict[str, object]:
    """Show that a class stores the function used to create a bound method."""

    formatter = IncidentFormatter()
    bound_render = formatter.render
    stored_render = IncidentFormatter.__dict__["render"]
    return {
        "class_metaclass": type(IncidentFormatter).__name__,
        "direct_bases": [base.__name__ for base in IncidentFormatter.__bases__],
        "class_stores_function": stored_render is IncidentFormatter.render,
        "bound_method_has_instance": bound_render.__self__ is formatter,
        "bound_method_has_function": bound_render.__func__ is stored_render,
        "result": bound_render("queue lag", "warning"),
    }


def module_evidence() -> dict[str, object]:
    """Prove module caching and stale copied values without leaving global state behind."""

    module_name = "_bijux_runtime_object_lab"
    module = types.ModuleType(module_name)
    module.status = "old"
    previous = sys.modules.get(module_name)
    sys.modules[module_name] = module

    try:
        imported = importlib.import_module(module_name)
        copied_status = module.status
        module.status = "new"
        return {
            "cached_import_preserves_identity": imported is module,
            "module_status": module.status,
            "copied_status": copied_status,
            "copied_value_is_stale": copied_status != module.status,
        }
    finally:
        if previous is None:
            sys.modules.pop(module_name, None)
        else:
            sys.modules[module_name] = previous


def instance_evidence() -> dict[str, object]:
    """Compare dictionary-backed and slotted storage through observable behavior."""

    class Incident:
        pass

    class SlottedIncident:
        __slots__ = ("title",)

    regular = Incident()
    regular.title = "queue lag"
    slotted = SlottedIncident()
    slotted.title = "queue lag"

    try:
        slotted.severity = "warning"
    except AttributeError:
        rejects_undeclared_attribute = True
    else:
        rejects_undeclared_attribute = False

    return {
        "regular_storage": vars(regular),
        "slotted_has_dict": hasattr(slotted, "__dict__"),
        "slotted_title": slotted.title,
        "slotted_rejects_undeclared_attribute": rejects_undeclared_attribute,
    }


def object_graph_evidence() -> dict[str, object]:
    """Trace one call from instance lookup back to class, function, and module state."""

    formatter = IncidentFormatter()
    bound_render = formatter.render
    function = bound_render.__func__
    defining_module = sys.modules[function.__module__]
    return {
        "instance_points_to_class": formatter.__class__ is IncidentFormatter,
        "bound_method_points_to_instance": bound_render.__self__ is formatter,
        "bound_method_points_to_function": function is IncidentFormatter.render,
        "function_points_to_module_namespace": function.__globals__ is defining_module.__dict__,
        "global_used_by_call": function.__globals__["SEVERITY_LABELS"] is SEVERITY_LABELS,
        "result": bound_render("queue lag", "critical"),
    }


def build_evidence() -> Mapping[str, dict[str, object]]:
    """Build the five evidence packets taught in Module 01."""

    return {
        "function": function_evidence(),
        "class": class_evidence(),
        "module": module_evidence(),
        "instance": instance_evidence(),
        "object_graph": object_graph_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON so learners can inspect or save the lab result."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
