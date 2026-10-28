# Exercises — Module 10: Lifecycle and Compatible Release

## 1. Differentiate liveness and readiness for the API.

## 2. What should worker readiness check?

## 3. Why should application replicas not all run migrations automatically?

## 4. What is the safe rollback point in expand–backfill–enforce?

## 5. Why can old and new code coexist after expansion?

## 6. What makes a container build reproducible enough for this course?

## 7. How should a worker handle SIGTERM while processing?

## 8. Why is a long SSE connection relevant to drain?

## 9. What should startup logs include and exclude?

## 10. Why is breaking API 1.2.0 candidate rejected even if database migration succeeds?

## 11. Trace compatible service and schema release in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/config.py` or `capstone/tracks/typescript-fastify/src/config.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare compatible service and schema release across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/config.py` with `capstone/tracks/typescript-fastify/src/config.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 10 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
