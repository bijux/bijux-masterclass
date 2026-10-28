# Exercises — Module 06: Metrics and Service-Level Indicators

## 1. When should a counter be used?

## 2. When should a gauge be used?

## 3. Why use histograms for latency?

## 4. May operation ID be a metric label?

## 5. Why is run ID forbidden as a label?

## 6. How should 401 responses affect availability?

## 7. What is the SLI for run-start freshness?

## 8. Why can a queue-depth gauge be misleading?

## 9. What does a counter reset mean?

## 10. Why version recording rules?

## 11. Trace metrics and SLI populations in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/metrics.py` or `capstone/tracks/typescript-fastify/src/reliability/metrics.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare metrics and SLI populations across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/metrics.py` with `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
