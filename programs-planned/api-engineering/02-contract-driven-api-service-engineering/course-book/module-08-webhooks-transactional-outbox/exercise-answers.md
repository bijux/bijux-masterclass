# Worked Answers — Module 08: Transactional Outbox and Webhook Delivery

Use these solutions to audit your reasoning for **Transactional Outbox and Webhook Delivery**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. State the dual-write problem in this service.

The terminal run state lives in PostgreSQL while webhook acceptance lives at a remote receiver; no local ACID transaction covers both.

The chapter’s decisive distinction is this: The excerpt for Transactional Outbox and Webhook Delivery isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 2. Why does an outbox solve lost intent but not exactly-once delivery?

It durably records that delivery is required, but sender/receiver response loss can still cause retry after acceptance. Receiver idempotency handles duplicates.

In the cumulative capstone, the rule becomes concrete: The same transaction that commits the terminal run and domain event inserts an immutable outbox row. After commit, a dispatcher can retry network delivery independently. Absence of delivery does not erase domain success.

**Evidence.** Inject failure between state transition and delivery and inspect the transaction, outbox row, retry identity, signature, and receiver deduplication.

## 3. Differentiate event ID, delivery ID, and attempt number.

Event ID identifies the logical domain event; delivery ID identifies one target’s delivery stream; attempt number counts sends for that delivery.

A useful way to reason about the boundary is: Commit domain state and an outbox event together; perform network delivery afterward with signed, identifiable, retryable, deduplicable attempts. HTTP delivery is at-least-once and receivers must treat event identity as the unit of idempotency.

**Evidence.** Inject failure between state transition and delivery and inspect the transaction, outbox row, retry identity, signature, and receiver deduplication.

## 4. Why sign exact serialized bytes?

HMAC authenticates bytes, not abstract JSON meaning. Different whitespace/key order/number encoding creates another digest.

The implementation consequence is: Claim Required evidence ---: --- --- 1 domain completion always outbox Write the narrow command and machine-readable oracle. 2 kill after commit still delivers Write the narrow command and machine-readable oracle. 3 event ID stable across retries Write the narrow command and machine-readable oracle. 4 exact bytes signature vectors Write the narrow command and machine-readable oracle. 5 stale signature rejected Write the narrow command and machine-readable oracle.

## 5. What does timestamp freshness prevent?

Indefinite replay of a captured valid request within policy; it does not prevent duplicates inside the window, which event dedup handles.

The important nuance is: Production code would resolve and connect to the approved destination while applying DNS/IP controls. This adapter intentionally keeps the course network-independent and does not pretend to be a general SSRF defence. """

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 6. Which responses should usually retry?

Network timeouts/connection errors and selected transient statuses such as 408, 429, and 5xx, bounded by attempts/backoff. Exact policy is documented.

Under concurrency or failure, the distinction becomes: Commit domain state and an outbox event together; perform network delivery afterward with signed, identifiable, retryable, deduplicable attempts. HTTP delivery is at-least-once and receivers must treat event identity as the unit of idempotency.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. Why not store full receiver response bodies?

They may be large or sensitive and are unnecessary for classification. Store bounded status/error evidence.

The design remains honest only if: For Transactional Outbox and Webhook Delivery , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 8. How can subscription secret rotation work without breaking in-flight delivery?

Version/encrypt secrets and bind each delivery to the secret version or support an overlap window; this course exposes the boundary but does not build a full key-management system.

The consumer-facing consequence is: The Transactional Outbox and Webhook Delivery increment must preserve the frozen API and every earlier durability invariant while delivering this result: Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 9. Why validate destination at delivery time as well as registration?

DNS and policy can change after registration, and redirects may introduce new targets.

The operational consequence is: For Transactional Outbox and Webhook Delivery , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Counterexample.** Domain state commits without the matching outbound record, or delivery occurs before the state is durable.

**Evidence.** Inject failure between state transition and delivery and inspect the transaction, outbox row, retry identity, signature, and receiver deduplication.

## 10. What should receiver return for exact duplicate?

A success status indicating the same event was already accepted, allowing sender to stop retrying.

The strongest engineering interpretation is: The same transaction that commits the terminal run and domain event inserts an immutable outbox row. After commit, a dispatcher can retry network delivery independently. Absence of delivery does not erase domain success.

**Counterexample.** The service passes in one process but loses the invariant after restart, concurrency, or a partial dependency failure.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace transactional outbox delivery in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/webhooks.py` and `capstone/tracks/typescript-fastify/src/webhooks.ts`. The required invariant is that terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated.

The defect-oriented view is: Production code would resolve and connect to the approved destination while applying DNS/IP controls. This adapter intentionally keeps the course network-independent and does not pretend to be a general SSRF defence. """

## 12. Compare transactional outbox delivery across Python and TypeScript

Both tracks must preserve this invariant: terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated. The intentional difference is that HTTP client libraries differ; exact event bytes, identifier, signature, and retry state must match.

Across the Python and TypeScript tracks, the invariant is: The Transactional Outbox and Webhook Delivery increment must preserve the frozen API and every earlier durability invariant while delivering this result: Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints The comparison track must expose the same public outcomes even when internal libraries and control flow differ.
