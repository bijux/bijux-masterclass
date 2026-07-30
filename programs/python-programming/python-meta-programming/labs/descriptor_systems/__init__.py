"""Executable evidence for descriptor systems and their architecture boundaries."""

from .cache import (
    CachedComputation,
    Document,
    InvalidatingField,
    cache_evidence,
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
    "ExternalField",
    "IncidentRecord",
    "InvalidatingField",
    "StoreUnavailable",
    "cache_evidence",
    "external_storage_evidence",
]
