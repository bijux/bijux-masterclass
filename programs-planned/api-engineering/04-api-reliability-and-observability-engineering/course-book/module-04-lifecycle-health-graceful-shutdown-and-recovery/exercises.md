# Exercises — Module 04: Lifecycle, Health, Shutdown, and Recovery

Work through all twelve problems before opening the answers. In **Lifecycle, Health, Shutdown, and Recovery**, every response must settle this question: **How do APIs, workers, and dispatchers start, become ready, drain, stop, and recover without losing accepted work?** For every answer, separate the authoritative boundary from convenient diagnostics, then explain which failing experiment would force you to revise the design.

## 1. Why should a database outage usually affect readiness but not liveness?

## 2. What must happen first during graceful shutdown?

## 3. How should a worker handle termination while holding a job lease?

## 4. May telemetry export delay shutdown?

## 5. What is the decisive oracle for safe restart recovery?

## 6. Why is a successful database ping insufficient for readiness?

## 7. When should liveness fail?

## 8. What prevents readiness flapping?

## 9. How should long-lived SSE connections drain?

## 10. What if the shutdown budget expires during a database transaction?

## 11. Trace explicit lifecycle and health in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/health.py` or `capstone/tracks/typescript-fastify/src/reliability/health.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare explicit lifecycle and health across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/health.py` with `capstone/tracks/typescript-fastify/src/reliability/health.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 04 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
