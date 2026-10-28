# Exercises — Module 08: Transactional Outbox and Webhook Delivery

## 1. State the dual-write problem in this service.

## 2. Why does an outbox solve lost intent but not exactly-once delivery?

## 3. Differentiate event ID, delivery ID, and attempt number.

## 4. Why sign exact serialized bytes?

## 5. What does timestamp freshness prevent?

## 6. Which responses should usually retry?

## 7. Why not store full receiver response bodies?

## 8. How can subscription secret rotation work without breaking in-flight delivery?

## 9. Why validate destination at delivery time as well as registration?

## 10. What should receiver return for exact duplicate?

## 11. Trace transactional outbox delivery in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/webhooks.py` or `capstone/tracks/typescript-fastify/src/webhooks.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare transactional outbox delivery across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/webhooks.py` with `capstone/tracks/typescript-fastify/src/webhooks.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
