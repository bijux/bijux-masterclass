"""Executable evidence for descriptor systems and their architecture boundaries."""

from .cache import (
    CachedComputation,
    Document,
    InvalidatingField,
    cache_evidence,
)
from .composition import (
    AuditWrites,
    DeliveryPolicy,
    FieldWrapper,
    NormalizeText,
    OneOf,
    StoredField,
    composition_evidence,
    describe_layers,
)
from .external import (
    CountingStore,
    ExternalField,
    IncidentRecord,
    StoreUnavailable,
    external_storage_evidence,
)

__all__ = [
    "CachedComputation",
    "CountingStore",
    "Document",
    "DeliveryPolicy",
    "ExternalField",
    "FieldWrapper",
    "IncidentRecord",
    "InvalidatingField",
    "NormalizeText",
    "OneOf",
    "StoreUnavailable",
    "StoredField",
    "AuditWrites",
    "cache_evidence",
    "composition_evidence",
    "describe_layers",
    "external_storage_evidence",
]
