"""Executable descriptor and attribute-lookup evidence for Module 07."""

from .binding import MethodBinding, inspect_method_binding, method_binding_evidence
from .precedence import LookupDecision, explain_lookup, precedence_evidence
from .protocol import (
    DescriptorProtocol,
    NameAware,
    ShadowableValue,
    StoredField,
    inspect_descriptor_protocol,
)
from .quantity import Quantity, QuantitySpec, QuantityValue

__all__ = [
    "DescriptorProtocol",
    "LookupDecision",
    "MethodBinding",
    "NameAware",
    "Quantity",
    "QuantitySpec",
    "QuantityValue",
    "ShadowableValue",
    "StoredField",
    "explain_lookup",
    "inspect_method_binding",
    "inspect_descriptor_protocol",
    "method_binding_evidence",
    "precedence_evidence",
]
