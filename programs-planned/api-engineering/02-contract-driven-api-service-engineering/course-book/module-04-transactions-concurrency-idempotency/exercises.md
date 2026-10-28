# Exercises — Module 04: Transactions, Concurrency, ETags, and Idempotency

## 1. Why is an in-process mutex insufficient for idempotency?

## 2. What belongs in the idempotency scope?

## 3. Why store the original response instead of only the run ID?

## 4. Which headers should be replayed?

## 5. How can canonical JSON avoid object-key-order differences?

## 6. What does zero rows from conditional UPDATE mean?

## 7. Why not send a webhook before commit?

## 8. When is transaction retry safe?

## 9. How do you test rollback at every statement boundary?

## 10. Why can `SERIALIZABLE` not replace correct unique constraints?

## 11. Trace transactional idempotency and conditional mutation in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` or `capstone/tracks/typescript-fastify/src/repository.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare transactional idempotency and conditional mutation across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/postgres.py` with `capstone/tracks/typescript-fastify/src/repository.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
