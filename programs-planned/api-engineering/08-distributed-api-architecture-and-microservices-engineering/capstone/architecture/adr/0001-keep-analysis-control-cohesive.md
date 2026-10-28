# ADR 0001 — Keep Analysis Control cohesive

**Decision:** projects, dataset metadata, run state, idempotency, leases, and authoritative event publication remain one service boundary.

**Reason:** their invariants share transaction authority and change together. Splitting them would replace local transactions with chatty coordination.

**Reversal evidence:** a stable team boundary, independent data authority, and measured release or scaling pressure that exceeds coordination cost.
