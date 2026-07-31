from __future__ import annotations

import inspect
import json
from collections.abc import Mapping


class IncidentObservationTarget:
    """Object whose counters expose when observation crosses into behavior."""

    def __init__(self, title: str) -> None:
        self.title = title
        self._property_reads = 0
        self._fallback_reads = 0

    @property
    def risk_score(self) -> int:
        self._property_reads += 1
        return 7

    def acknowledge(self) -> str:
        return f"acknowledged: {self.title}"

    def __getattr__(self, name: str) -> str:
        self._fallback_reads += 1
        return f"generated:{name}"


class DeliveryPolicy:
    """Base role used to compare polymorphic and exact classification."""


class CustomDeliveryPolicy(DeliveryPolicy):
    """Valid extension that an exact base-type check would reject."""


class CallableRouter:
    def __call__(self, incident_id: str) -> str:
        if not incident_id:
            raise ValueError("incident_id must not be empty")
        return f"route:{incident_id}"


class PlainRouter:
    pass


def visible_names_evidence() -> dict[str, object]:
    """Separate discoverable names from dictionary-backed stored state."""

    target = IncidentObservationTarget("queue lag")
    visible_names = set(dir(target))
    stored_state = vars(target)
    return {
        "acknowledge_is_visible": "acknowledge" in visible_names,
        "acknowledge_is_stored": "acknowledge" in stored_state,
        "risk_score_is_visible": "risk_score" in visible_names,
        "stored_names": sorted(stored_state),
        "title_is_stored": stored_state["title"] == "queue lag",
    }


def dynamic_access_evidence() -> dict[str, object]:
    """Show that static attachment checks and dynamic reads cross different boundaries."""

    target = IncidentObservationTarget("queue lag")
    raw_property = inspect.getattr_static(target, "risk_score")
    property_reads_after_static_lookup = target._property_reads
    resolved_score = getattr(target, "risk_score")
    property_reads_after_dynamic_lookup = target._property_reads
    attribute_exists = hasattr(target, "risk_score")
    return {
        "static_lookup_returns_property": isinstance(raw_property, property),
        "property_reads_after_static_lookup": property_reads_after_static_lookup,
        "resolved_score": resolved_score,
        "property_reads_after_dynamic_lookup": property_reads_after_dynamic_lookup,
        "hasattr_result": attribute_exists,
        "property_reads_after_hasattr": target._property_reads,
    }


def type_check_evidence() -> dict[str, object]:
    """Contrast role-compatible and exact-identity runtime questions."""

    extension = CustomDeliveryPolicy()
    return {
        "bool_is_instance_of_int": isinstance(True, int),
        "bool_is_exact_int": type(True) is int,
        "extension_matches_delivery_role": isinstance(extension, DeliveryPolicy),
        "extension_is_exact_base_type": type(extension) is DeliveryPolicy,
    }


def callability_evidence() -> dict[str, object]:
    """Keep callability separate from invocation validity."""

    router = CallableRouter()
    plain = PlainRouter()
    plain.__call__ = lambda incident_id: f"route:{incident_id}"

    try:
        router("")
    except ValueError as exc:
        failed_call = type(exc).__name__
    else:
        failed_call = None

    return {
        "callable_instance": callable(router),
        "instance_attribute_does_not_install_protocol": callable(plain),
        "valid_result": router("INC-42"),
        "invalid_call_error": failed_call,
    }


def static_lookup_evidence() -> dict[str, object]:
    """Inspect fallback machinery before intentionally triggering it."""

    target = IncidentObservationTarget("queue lag")
    raw_fallback = inspect.getattr_static(target, "__getattr__")

    try:
        inspect.getattr_static(target, "owner")
    except AttributeError:
        static_missing = True
    else:
        static_missing = False

    fallback_reads_after_static_lookup = target._fallback_reads
    resolved_owner = getattr(target, "owner")
    return {
        "fallback_is_attached": callable(raw_fallback),
        "static_lookup_reports_missing": static_missing,
        "fallback_reads_after_static_lookup": fallback_reads_after_static_lookup,
        "resolved_owner": resolved_owner,
        "fallback_reads_after_dynamic_lookup": target._fallback_reads,
    }


def build_evidence() -> Mapping[str, dict[str, object]]:
    """Build the five evidence packets taught in Module 02."""

    return {
        "visible_names": visible_names_evidence(),
        "dynamic_access": dynamic_access_evidence(),
        "type_checks": type_check_evidence(),
        "callability": callability_evidence(),
        "static_lookup": static_lookup_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON so learners can compare observation boundaries."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
