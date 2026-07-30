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
from .hints import (
    HintField,
    HintPlan,
    Minimum,
    NonBlank,
    RetryPolicy,
    UnsupportedHint,
    compile_hint,
    hint_evidence,
)
from .relational import (
    ColumnContract,
    build_incident_model,
    inspect_columns,
    relational_model_evidence,
)

__all__ = [
    "CachedComputation",
    "ColumnContract",
    "CountingStore",
    "Document",
    "DeliveryPolicy",
    "ExternalField",
    "FieldWrapper",
    "HintField",
    "HintPlan",
    "IncidentRecord",
    "InvalidatingField",
    "Minimum",
    "NormalizeText",
    "NonBlank",
    "OneOf",
    "RetryPolicy",
    "StoreUnavailable",
    "StoredField",
    "UnsupportedHint",
    "AuditWrites",
    "cache_evidence",
    "build_incident_model",
    "compile_hint",
    "composition_evidence",
    "describe_layers",
    "external_storage_evidence",
    "hint_evidence",
    "inspect_columns",
    "relational_model_evidence",
]
