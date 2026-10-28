# Glossary — Contract-Driven API Service Engineering

These terms have precise meanings in Course 2. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## use case

An application-level action that coordinates domain rules and ports to achieve one user-visible outcome without depending on an HTTP framework.

## domain invariant

A rule that must remain true for valid business state regardless of transport, persistence technology, or process layout.

## transaction boundary

The exact set of durable changes that must commit or roll back as one atomic unit.

## migration

A versioned, ordered change to durable storage that can be applied predictably and reviewed as part of a release.

## constraint

A database-enforced rule—such as uniqueness, referential integrity, or a check condition—that prevents invalid durable state.

## optimistic concurrency

A strategy that allows concurrent reads but rejects a write when the durable version has changed since the client observed it.

## entity tag

An HTTP validator representing a selected version of a resource representation, commonly used with `If-Match` or `If-None-Match`.

## idempotency record

Durable state binding an idempotency key to a request fingerprint and the logical result that may be replayed.

## request fingerprint

A canonical digest of all request fields whose change would make reuse of an idempotency key unsafe.

## cursor

An opaque continuation handle bound to a query, principal, ordering position, and expiry rather than a client-editable page number.

## high-water mark

The maximum eligible ordering position captured when traversal starts, preventing later inserts from contaminating the same traversal.

## lease

A time-bounded claim granting a worker temporary authority to process a durable job.

## fencing token

A monotonically advancing generation attached to a lease so stale workers cannot overwrite effects produced by newer owners.

## worker recovery

The process of detecting abandoned work, deciding whether it may be retried, and restoring a valid durable job state without duplicating effects.

## artifact integrity

Evidence that stored and returned artifact bytes are complete, unmodified, correctly owned, and identified by the expected digest.

## content address

A storage key derived from content bytes, usually a cryptographic digest, so identical content has the same identity.

## transactional outbox

Rows committed in the same transaction as business state so outbound publication cannot be lost through a dual write.

## delivery attempt

One concrete try to deliver an outbox event, carrying its own timing, failure, and retry evidence while preserving the event identity.

## reconciliation

A read-oriented comparison between intended durable facts and observed effects that identifies missing, duplicate, stale, or orphaned work.

## compatible release

A release whose contract, code, and schema can coexist safely with supported previous clients and, during rollout, previous service versions.
