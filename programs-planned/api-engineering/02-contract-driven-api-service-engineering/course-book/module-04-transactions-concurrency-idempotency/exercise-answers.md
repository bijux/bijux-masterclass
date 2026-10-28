# Worked Answers — Module 04: Transactions, Concurrency, ETags, and Idempotency

Use these solutions to audit your reasoning for **Transactions, Concurrency, ETags, and Idempotency**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is an in-process mutex insufficient for idempotency?

It coordinates only one process and disappears on restart. The durable unique key must arbitrate across all instances.

The chapter’s decisive distinction is this: Concurrent first attempts race to insert one unique idempotency record. The winner performs the transaction; losers observe the record and replay when complete. An incomplete reservation requires explicit recovery policy rather than indefinite waiting.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 2. What belongs in the idempotency scope?

At least authenticated owner/principal, stable operation identifier, and client key; the request fingerprint binds content.

In the cumulative capstone, the rule becomes concrete: Replay preserves status, selected stable headers, and response body as originally committed. Volatile headers such as Date or request correlation ID need not be identical. The course names the stored header set.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 3. Why store the original response instead of only the run ID?

The response may include the accepted lifecycle snapshot and headers that differ from current state. Replay promises the original logical outcome, not a fresh GET.

A useful way to reason about the boundary is: Replay preserves status, selected stable headers, and response body as originally committed. Volatile headers such as Date or request correlation ID need not be identical. The course names the stored header set.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 4. Which headers should be replayed?

Stable operation headers such as `Location` and an explicit replay marker. Volatile transport headers such as `Date`, connection, and request correlation should be regenerated or excluded.

The implementation consequence is: The Transactions, Concurrency, ETags, and Idempotency increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 5. How can canonical JSON avoid object-key-order differences?

Recursively sort object keys, preserve array order, use a defined number/string encoding, and hash a structure that includes operation and principal.

The important nuance is: Claim Required evidence ---: --- --- 1 100 identical requests one run Write the narrow command and machine-readable oracle. 2 changed-body reuse conflicts Write the narrow command and machine-readable oracle. 3 different principal same key independent Write the narrow command and machine-readable oracle. 4 replay survives restart Write the narrow command and machine-readable oracle. 5 replay returns original accepted snapshot Write the narrow command and machine-readable oracle.

## 6. What does zero rows from conditional UPDATE mean?

Either resource is absent/foreign or expected version is stale. A follow-up ownership-concealed existence check distinguishes the documented outcomes without exposing foreign state.

Under concurrency or failure, the distinction becomes: The representation version becomes an HTTP validator. Parsing establishes that the tag belongs to the target resource; the conditional update proves it is still current. Zero updated rows are resolved into concealed not-found versus stale precondition without leaking ownership.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. Why not send a webhook before commit?

The database could roll back after the receiver accepts, creating an event for state that never became durable.

The design remains honest only if: The excerpt for Transactions, Concurrency, ETags, and Idempotency isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

**Evidence.** Inject failure between state transition and delivery and inspect the transaction, outbox row, retry identity, signature, and receiver deduplication.

## 8. When is transaction retry safe?

When the closure’s inputs are stable, all effects are transactional or pure, retry count is bounded, and no irreversible effect escaped.

The consumer-facing consequence is: PostgreSQL may abort transactions for deadlock or serialization conflicts. Only the transaction closure may be retried, with bounded attempts and only when its external effects have not escaped. Outbound HTTP never occurs inside the retried transaction.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 9. How do you test rollback at every statement boundary?

Inject a controlled exception after each mutation in turn, then assert all participating table counts and invariants are unchanged.

The operational consequence is: For Transactions, Concurrency, ETags, and Idempotency , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 10. Why can `SERIALIZABLE` not replace correct unique constraints?

Isolation can detect anomalies but does not define business identity; a unique constraint directly represents the one-record invariant and remains necessary.

The strongest engineering interpretation is: Concurrent first attempts race to insert one unique idempotency record. The winner performs the transaction; losers observe the record and replay when complete. An incomplete reservation requires explicit recovery policy rather than indefinite waiting.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace transactional idempotency and conditional mutation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` and `capstone/tracks/typescript-fastify/src/repository.ts`. The required invariant is that one key and fingerprint produce one durable outcome, while a stale version fails atomically.

The defect-oriented view is: The Transactions, Concurrency, ETags, and Idempotency increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 12. Compare transactional idempotency and conditional mutation across Python and TypeScript

Both tracks must preserve this invariant: one key and fingerprint produce one durable outcome, while a stale version fails atomically. The intentional difference is that context-manager transactions and promise-scoped clients differ without changing the commit boundary.

Across the Python and TypeScript tracks, the invariant is: The representation version becomes an HTTP validator. Parsing establishes that the tag belongs to the target resource; the conditional update proves it is still current. Zero updated rows are resolved into concealed not-found versus stale precondition without leaking ownership.
