# Reference Answers — Module 08: Transactional Outbox and Webhook Delivery

Read after attempting all twelve Transactional Outbox and Webhook Delivery exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. State the dual-write problem in this service.

The terminal run state lives in PostgreSQL while webhook acceptance lives at a remote receiver; no local ACID transaction covers both.

## 2. Why does an outbox solve lost intent but not exactly-once delivery?

It durably records that delivery is required, but sender/receiver response loss can still cause retry after acceptance. Receiver idempotency handles duplicates.

## 3. Differentiate event ID, delivery ID, and attempt number.

Event ID identifies the logical domain event; delivery ID identifies one target’s delivery stream; attempt number counts sends for that delivery.

## 4. Why sign exact serialized bytes?

HMAC authenticates bytes, not abstract JSON meaning. Different whitespace/key order/number encoding creates another digest.

## 5. What does timestamp freshness prevent?

Indefinite replay of a captured valid request within policy; it does not prevent duplicates inside the window, which event dedup handles.

## 6. Which responses should usually retry?

Network timeouts/connection errors and selected transient statuses such as 408, 429, and 5xx, bounded by attempts/backoff. Exact policy is documented.

## 7. Why not store full receiver response bodies?

They may be large or sensitive and are unnecessary for classification. Store bounded status/error evidence.

## 8. How can subscription secret rotation work without breaking in-flight delivery?

Version/encrypt secrets and bind each delivery to the secret version or support an overlap window; this course exposes the boundary but does not build a full key-management system.

## 9. Why validate destination at delivery time as well as registration?

DNS and policy can change after registration, and redirects may introduce new targets.

## 10. What should receiver return for exact duplicate?

A success status indicating the same event was already accepted, allowing sender to stop retrying.

## 11. Trace transactional outbox delivery in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/webhooks.py` and `capstone/tracks/typescript-fastify/src/webhooks.ts`. The required invariant is that terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated.

## 12. Compare transactional outbox delivery across Python and TypeScript

Both tracks must preserve this invariant: terminal run state and its outbound event commit together, while delivery attempts remain retryable and deduplicated. The intentional difference is that HTTP client libraries differ; exact event bytes, identifier, signature, and retry state must match.
