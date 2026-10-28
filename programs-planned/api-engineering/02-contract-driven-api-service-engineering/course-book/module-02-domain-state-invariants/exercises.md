# Exercises — Module 02: Domain State and Invariants

## 1. Why is a run status enum insufficient by itself?

## 2. Can a failed run return to queued for retry? State the course decision and alternative.

## 3. Why does progress 100 imply completion?

## 4. What is emitted when the same idempotent cancellation request is repeated?

## 5. Distinguish cancellation requested from cancelled.

## 6. Why should event identity be persisted rather than recomputed?

## 7. Classify a stale ETag and malformed ETag.

## 8. Why conceal foreign ownership as 404?

## 9. Design a property for progress sequences.

## 10. Where should an event timestamp be assigned?

## 11. Trace domain invariants and canonical values in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/domain.py` or `capstone/tracks/typescript-fastify/src/domain.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare domain invariants and canonical values across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/domain.py` with `capstone/tracks/typescript-fastify/src/domain.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
