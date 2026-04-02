"""Module 07: domain-owned effect interfaces (end-of-Module-07).

Module 07’s architecture treats these effect descriptions as part of the domain layer:
- `IOPlan`: deferred, composable IO as pure data
- IOPlan-specific wrappers: retry (idempotent only) and transaction bracketing
"""

from .io_plan import IOPlan, io_bind, io_delay, io_map, io_pure, perform
from .io_retry import RetryPolicy, is_transient, retry_idempotent
from .tx import Session, Tx, TxProtocol, session_with, with_tx

__all__ = [
    "IOPlan",
    "io_pure",
    "io_delay",
    "io_bind",
    "io_map",
    "perform",
    "RetryPolicy",
    "is_transient",
    "retry_idempotent",
    "Session",
    "session_with",
    "TxProtocol",
    "Tx",
    "with_tx",
]

