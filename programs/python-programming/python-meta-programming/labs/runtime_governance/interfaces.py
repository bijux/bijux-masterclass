from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class DeliveryABC(ABC):
    """Runtime nominal contract for constructed delivery adapters."""

    @abstractmethod
    def deliver(self, message: str) -> str:
        """Deliver one message."""


@runtime_checkable
class DeliveryProtocol(Protocol):
    """Static structural contract with shallow runtime presence checks."""

    def deliver(self, message: str) -> str: ...


class PreviewCapable(ABC):
    """Narrow structural classification based on a class-defined method."""

    @classmethod
    def __subclasshook__(cls, candidate: type[object]) -> bool:
        if cls is PreviewCapable:
            return any("preview" in vars(base) for base in candidate.__mro__)
        return NotImplemented


def interface_evidence() -> dict[str, object]:
    """Contrast enforcement and observation claims across interface tools."""

    class MissingDelivery(DeliveryABC):
        pass

    abc_failure = ""
    try:
        MissingDelivery()
    except TypeError as error:
        abc_failure = str(error)

    class WrongSignature:
        def deliver(self) -> str:
            return "delivered"

    class StaticPreview:
        def preview(self) -> str:
            return "preview"

    class DynamicPreview:
        def __getattr__(self, name: str) -> object:
            if name == "preview":
                return lambda: "preview"
            raise AttributeError(name)

    return {
        "abc": {
            "incomplete_class_created": True,
            "incomplete_instance_created": False,
            "failure_type": "TypeError",
            "mentions_abstract_method": "abstract method" in abc_failure,
            "claim": "nominal subclasses cannot instantiate with missing abstract methods",
        },
        "protocol": {
            "wrong_signature_passes_runtime_check": isinstance(
                WrongSignature(),
                DeliveryProtocol,
            ),
            "runtime_check_scope": "attribute presence only",
            "signature_compatibility_owner": "static type checker",
        },
        "subclass_hook": {
            "static_preview_matches": issubclass(StaticPreview, PreviewCapable),
            "dynamic_preview_matches": issubclass(DynamicPreview, PreviewCapable),
            "instance_fallback_executed": False,
            "claim": "classification uses names present in class dictionaries",
        },
        "selection": {
            "runtime_instantiation_rule": "ABC",
            "static structural consumer contract": "Protocol",
            "narrow runtime structural classification": "__subclasshook__",
        },
    }
