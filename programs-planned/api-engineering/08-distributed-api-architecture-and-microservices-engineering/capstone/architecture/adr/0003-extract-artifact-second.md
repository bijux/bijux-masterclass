# ADR 0003 — Extract Artifact Delivery second

**Decision:** move artifact bytes, checksums, retention, and content delivery after capability-based authorization and reconciliation exist.

**Reason:** artifact traffic has distinct storage and egress characteristics, but extraction is unsafe while authorization depends on another service database.

**Residual risk:** an artifact can be stored before Analysis Control accepts completion; orphan reconciliation is mandatory.
