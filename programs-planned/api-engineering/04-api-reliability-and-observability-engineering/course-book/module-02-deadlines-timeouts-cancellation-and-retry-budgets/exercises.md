# Exercises — Module 02: Deadlines, Cancellation, and Retry Budgets

## 1. Why is a deadline stronger than a timeout?

## 2. May a child deadline equal the parent?

## 3. When is POST retryable?

## 4. What does a transport timeout prove about the server effect?

## 5. How should Retry-After interact with a deadline?

## 6. Why may jitter sequences differ across languages?

## 7. Where should automatic retry live?

## 8. Should disconnect cancel a committed run?

## 9. Which status codes are always retryable?

## 10. Why reserve minimum attempt time?

## 11. Trace absolute deadline propagation in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/deadline.py` or `capstone/tracks/typescript-fastify/src/reliability/deadline.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare absolute deadline propagation across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/deadline.py` with `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 02 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
