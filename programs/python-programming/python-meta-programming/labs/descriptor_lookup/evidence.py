from __future__ import annotations

import json

from .binding import method_binding_evidence
from .precedence import precedence_evidence
from .protocol import NameAware, StoredField, inspect_descriptor_protocol
from .quantity import Quantity


def protocol_evidence() -> dict[str, object]:
    """Separate naming configuration from descriptor protocol status."""

    class Delivery:
        marker = NameAware()
        endpoint = StoredField()

    return {
        "name_aware": inspect_descriptor_protocol(
            vars(Delivery)["marker"]
        ).manifest(),
        "stored_field": inspect_descriptor_protocol(
            vars(Delivery)["endpoint"]
        ).manifest(),
        "field_name": Delivery.endpoint.public_name,
        "class_access_returns_descriptor": (
            Delivery.endpoint is vars(Delivery)["endpoint"]
        ),
    }


def quantity_evidence() -> dict[str, object]:
    """Show canonical storage, conversion, independence, and bounded failure."""

    class DeliveryTiming:
        latency = Quantity(
            "s",
            {"s": 1.0, "ms": 0.001},
            minimum=0.0,
            maximum=30.0,
        )

    first = DeliveryTiming()
    second = DeliveryTiming()
    first.latency = (250, "ms")
    second.latency = 2
    try:
        first.latency = (31, "s")
    except ValueError as error:
        range_failure = str(error)

    return {
        "field": DeliveryTiming.latency.spec().manifest(),
        "first": {
            **first.latency.manifest(),
            "milliseconds": first.latency.in_unit("ms"),
            "instance_dictionary": dict(vars(first)),
        },
        "second": {
            **second.latency.manifest(),
            "instance_dictionary": dict(vars(second)),
        },
        "range_failure": range_failure,
        "descriptor_holds_instance_values": False,
    }


def build_evidence() -> dict[str, dict[str, object]]:
    """Build deterministic evidence packets for Module 07."""

    return {
        "method_binding": method_binding_evidence(),
        "precedence": precedence_evidence(),
        "protocol": protocol_evidence(),
        "quantity_field": quantity_evidence(),
    }


def render_evidence() -> str:
    """Render the complete learner evidence route as stable JSON."""

    return json.dumps(build_evidence(), indent=2, sort_keys=True)
