# Exercises — Module 01: Reliability Model and Critical Journeys

Work through all twelve problems before opening the answers. In **Reliability Model and Critical Journeys**, every response must settle this question: **Which user journeys matter, what makes them good or bad, and which durable facts establish the outcome?** A complete response identifies the contract owner, predicts one observable failure, and names the evidence that decides the case; a definition by itself is incomplete.

## 1. Why is process uptime not a user-journey SLI?

## 2. Define the eligible population for run-start freshness.

## 3. Should an invalid bearer token count against API availability?

## 4. What is the decisive oracle for artifact completion?

## 5. How should low traffic affect an SLO conclusion?

## 6. Distinguish a failure mode from a symptom.

## 7. Why version SLI definitions?

## 8. What makes a reliability requirement falsifiable?

## 9. When may telemetry be the only available evidence?

## 10. Why keep security failures in the reliability model?

## 11. Trace critical-journey outcome classification in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/http.py` or `capstone/tracks/typescript-fastify/src/reliability/http.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare critical-journey outcome classification across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/http.py` with `capstone/tracks/typescript-fastify/src/reliability/http.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 01 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
