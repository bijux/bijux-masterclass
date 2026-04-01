"""Pure, production-facing architecture primitives (end-of-Module-08).

Module 07 introduces a production architecture around the existing pure core:
- Capability protocols (typed `Protocol`s)
- Structured logs as pure data (`LogEntry` + Writer)
- Idempotent effect design for safe retries/replays

Note: `IOPlan` + IOPlan-specific retry/tx helpers live in `funcpipe_rag.domain.effects`.
"""

from .logging import LogEntry, Logs, LogMonoid, log_tell, trace_stage, trace_value
from .capabilities import Cache, Clock, Logger, Storage, StorageRead, StorageWrite
from .composition import chain_io, logged_read
from .idempotent import AtomicWriteCap, content_key, idempotent_write

__all__ = [
    # Logging (pure data)
    "LogEntry",
    "Logs",
    "LogMonoid",
    "log_tell",
    "trace_stage",
    "trace_value",
    # Capabilities
    "StorageRead",
    "StorageWrite",
    "Storage",
    "Clock",
    "Logger",
    "Cache",
    # Composition helpers
    "chain_io",
    "logged_read",
    # Idempotency + retry
    "AtomicWriteCap",
    "content_key",
    "idempotent_write",
]
