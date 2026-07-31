from __future__ import annotations

import json
from dataclasses import FrozenInstanceError, asdict, dataclass, field
from typing import get_type_hints

from .attributes import TypedField
from .frozen_surface import FrozenSurfaceError, surface_frozen
from .transformation import mark_class, tracing_class_decorator


def transformation_evidence() -> dict[str, object]:
    """Expose class-body timing, bottom-up application, and identity."""

    events: list[str] = []

    @tracing_class_decorator("outer", events)
    @tracing_class_decorator("inner", events)
    class Delivery:
        events.append("body:Delivery")

    undecorated = type("UndecoratedDelivery", (), {})
    identity_before = id(undecorated)
    decorated = mark_class("incident-delivery")(undecorated)
    return {
        "events": events,
        "application_trace": list(Delivery.__decorator_trace__),
        "in_place_identity_preserved": id(decorated) == identity_before,
        "customization": asdict(decorated.__class_customization__),
        "metaclass": type(decorated).__name__,
    }


def dataclass_evidence() -> dict[str, object]:
    """Separate generated convenience from validation and deep immutability."""

    @dataclass(frozen=True, slots=True)
    class DeliveryPlan:
        attempts: int
        tags: list[str] = field(default_factory=list)

    plan = DeliveryPlan(attempts="three")  # type: ignore[arg-type]
    other = DeliveryPlan(attempts=3)
    plan.tags.append("urgent")
    try:
        plan.attempts = 3  # type: ignore[misc]
    except FrozenInstanceError as error:
        rebinding_failure = type(error).__name__

    return {
        "generated_methods": [
            name for name in ("__init__", "__repr__", "__eq__") if name in vars(DeliveryPlan)
        ],
        "annotation_did_not_validate": plan.attempts == "three",
        "default_factory_is_per_instance": plan.tags is not other.tags,
        "nested_list_after_mutation": plan.tags,
        "rebinding_failure": rebinding_failure,
        "has_instance_dict": hasattr(plan, "__dict__"),
    }


def property_evidence() -> dict[str, object]:
    """Show one property owning validation and lookup over instance state."""

    class DeliveryConfig:
        def __init__(self, endpoint: str) -> None:
            self.endpoint = endpoint

        @property
        def endpoint(self) -> str:
            return self._endpoint

        @endpoint.setter
        def endpoint(self, value: str) -> None:
            if not value.startswith("https://"):
                raise ValueError("endpoint must use https")
            self._endpoint = value

    config = DeliveryConfig("https://example.test")
    vars(config)["endpoint"] = "shadowed"
    try:
        config.endpoint = "http://insecure.test"
    except ValueError as error:
        failure = str(error)

    return {
        "visible_endpoint": config.endpoint,
        "same_named_instance_entry": vars(config)["endpoint"],
        "property_wins_over_instance_entry": config.endpoint != vars(config)["endpoint"],
        "invalid_assignment_failure": failure,
        "descriptor_type": type(vars(DeliveryConfig)["endpoint"]).__name__,
    }


def descriptor_evidence() -> dict[str, object]:
    """Show one reusable descriptor owning shallow runtime enforcement."""

    class DeliveryConfig:
        endpoint: str = TypedField(str)
        attempts: int = TypedField(int)

        def __init__(self, endpoint: str, attempts: int) -> None:
            self.endpoint = endpoint
            self.attempts = attempts

    first = DeliveryConfig("https://one.test", 1)
    second = DeliveryConfig("https://two.test", 2)
    try:
        first.attempts = "three"  # type: ignore[assignment]
    except TypeError as error:
        failure = str(error)

    return {
        "first": {"endpoint": first.endpoint, "attempts": first.attempts},
        "second": {"endpoint": second.endpoint, "attempts": second.attempts},
        "field_specs": [
            asdict(DeliveryConfig.endpoint.spec()),
            asdict(DeliveryConfig.attempts.spec()),
        ],
        "invalid_assignment_failure": failure,
        "annotations_are_declarations": {
            name: hint.__name__ for name, hint in get_type_hints(DeliveryConfig).items()
        },
    }


def frozen_surface_evidence() -> dict[str, object]:
    """Expose the narrow frozen promise and its deliberate limits."""

    @surface_frozen
    class DeliveryConfig:
        def __init__(self) -> None:
            self.endpoint = "https://example.test"
            self.tags = ["incident"]

    config = DeliveryConfig()
    config.tags.append("urgent")
    try:
        config.endpoint = "https://other.test"
    except FrozenSurfaceError as error:
        rebinding_failure = str(error)

    return {
        "policy": asdict(DeliveryConfig.__surface_frozen__),
        "nested_list_after_mutation": config.tags,
        "rebinding_failure": rebinding_failure,
    }


def build_evidence() -> dict[str, dict[str, object]]:
    """Build the deterministic evidence packets taught in Module 06."""

    return {
        "class_transformation": transformation_evidence(),
        "dataclass_boundary": dataclass_evidence(),
        "descriptor_boundary": descriptor_evidence(),
        "frozen_surface": frozen_surface_evidence(),
        "property_boundary": property_evidence(),
    }


def render_evidence() -> str:
    """Render stable JSON for learner inspection and review."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
