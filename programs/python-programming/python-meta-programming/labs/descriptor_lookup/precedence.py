from __future__ import annotations

from dataclasses import asdict, dataclass
import inspect
from typing import Literal

from .protocol import ShadowableValue, StoredField, inspect_descriptor_protocol


LookupWinner = Literal[
    "data-descriptor",
    "instance-dictionary",
    "non-data-descriptor",
    "class-attribute",
    "missing",
]


@dataclass(frozen=True, slots=True)
class LookupDecision:
    """A non-executing explanation of ordinary instance lookup."""

    public_name: str
    static_type: str | None
    descriptor_kind: str
    instance_has_public_name: bool
    winner: LookupWinner

    def manifest(self) -> dict[str, object]:
        return asdict(self)


def explain_lookup(owner: type[object], instance: object, name: str) -> LookupDecision:
    """Predict the winning ordinary lookup layer without invoking a descriptor."""

    missing = object()
    static_value = inspect.getattr_static(owner, name, missing)
    instance_has_public_name = name in vars(instance)
    if static_value is missing:
        winner: LookupWinner = (
            "instance-dictionary" if instance_has_public_name else "missing"
        )
        return LookupDecision(
            public_name=name,
            static_type=None,
            descriptor_kind="not-present",
            instance_has_public_name=instance_has_public_name,
            winner=winner,
        )

    protocol = inspect_descriptor_protocol(static_value)
    if protocol.kind == "data":
        winner = "data-descriptor"
    elif instance_has_public_name:
        winner = "instance-dictionary"
    elif protocol.kind == "non-data":
        winner = "non-data-descriptor"
    else:
        winner = "class-attribute"
    return LookupDecision(
        public_name=name,
        static_type=type(static_value).__name__,
        descriptor_kind=protocol.kind,
        instance_has_public_name=instance_has_public_name,
        winner=winner,
    )


def precedence_evidence() -> dict[str, object]:
    """Compare actual reads with non-executing lookup predictions."""

    class Delivery:
        enforced = StoredField()
        shadowable = ShadowableValue("descriptor-value")
        category = "class-value"

    delivery = Delivery()
    delivery.enforced = "descriptor-storage"
    vars(delivery)["enforced"] = "same-name-instance-value"
    vars(delivery)["shadowable"] = "instance-value"

    decisions = {
        name: explain_lookup(Delivery, delivery, name).manifest()
        for name in ("enforced", "shadowable", "category")
    }
    return {
        "decisions": decisions,
        "actual_reads": {
            "enforced": delivery.enforced,
            "shadowable": delivery.shadowable,
            "category": delivery.category,
        },
        "instance_dictionary": dict(vars(delivery)),
        "ordinary_lookup_only": True,
    }
