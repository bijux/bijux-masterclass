"""Executable descriptor and attribute-lookup evidence for Module 07."""

from .precedence import LookupDecision, explain_lookup, precedence_evidence
from .protocol import (
    DescriptorProtocol,
    NameAware,
    ShadowableValue,
    StoredField,
    inspect_descriptor_protocol,
)

__all__ = [
    "DescriptorProtocol",
    "LookupDecision",
    "NameAware",
    "ShadowableValue",
    "StoredField",
    "explain_lookup",
    "inspect_descriptor_protocol",
    "precedence_evidence",
]
