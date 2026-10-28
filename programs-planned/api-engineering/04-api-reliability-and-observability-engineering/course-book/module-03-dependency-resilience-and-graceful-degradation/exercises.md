# Exercises — Module 03: Dependency Resilience and Graceful Degradation

## 1. When should a circuit breaker not be used?

## 2. Why is a bulkhead different from rate limiting?

## 3. May telemetry export use a circuit?

## 4. Can PostgreSQL reads use stale fallback?

## 5. What happens when artifact publication fails?

## 6. How should half-open probes be selected?

## 7. Why record transitions rather than unique rejection series?

## 8. What makes degradation truthful?

## 9. How can a bulkhead starve work?

## 10. Should an open circuit affect readiness?

## 11. Trace dependency-local resilience in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/circuit.py` or `capstone/tracks/typescript-fastify/src/reliability/circuit.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare dependency-local resilience across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/circuit.py` with `capstone/tracks/typescript-fastify/src/reliability/circuit.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 03 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
