# Exercises — Module 05: Telemetry Architecture and Structured Events

## 1. Why are logs, metrics, and traces not interchangeable?

## 2. What should happen when an incoming traceparent is invalid?

## 3. May tenant ID be a trace attribute?

## 4. Why redact before buffering?

## 5. What is the correct customer behavior during collector outage?

## 6. Should baggage carry an access token?

## 7. How should elapsed time be measured?

## 8. What does a trace ID prove?

## 9. Why version event names and fields?

## 10. When is dropping telemetry acceptable?

## 11. Trace bounded structured telemetry in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py` or `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare bounded structured telemetry across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py` with `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 05 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
