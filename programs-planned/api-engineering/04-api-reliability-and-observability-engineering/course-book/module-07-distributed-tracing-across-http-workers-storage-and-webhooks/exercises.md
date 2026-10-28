# Exercises — Module 07: Distributed Tracing Across Asynchronous Work

## 1. Why should a durable worker usually not be a direct child of the request span?

## 2. Where should trace context be stored for a job?

## 3. How do you measure queue delay?

## 4. What does a span status of error mean?

## 5. Should every retry be a new trace?

## 6. Why can head sampling miss important failures?

## 7. May run ID be a span attribute?

## 8. What if context extraction fails from a job row?

## 9. How should webhook delivery be linked?

## 10. What proves an artifact was published?

## 11. Trace trace context across asynchronous work in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/context.py` or `capstone/tracks/typescript-fastify/src/reliability/context.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare trace context across asynchronous work across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/context.py` with `capstone/tracks/typescript-fastify/src/reliability/context.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 07 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
