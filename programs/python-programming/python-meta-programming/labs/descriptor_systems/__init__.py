"""Executable evidence for descriptor systems and their architecture boundaries."""

from .boundaries import (
    DesignPressure,
    OwnerDecision,
    boundary_evidence,
    decide_owner,
)
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
from .evidence import build_evidence, render_evidence
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
    "DesignPressure",
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
    "OwnerDecision",
    "RetryPolicy",
    "StoreUnavailable",
    "StoredField",
    "UnsupportedHint",
    "AuditWrites",
    "cache_evidence",
    "build_incident_model",
    "boundary_evidence",
    "build_evidence",
    "compile_hint",
    "composition_evidence",
    "describe_layers",
    "decide_owner",
    "external_storage_evidence",
    "hint_evidence",
    "inspect_columns",
    "relational_model_evidence",
    "render_evidence",
]
