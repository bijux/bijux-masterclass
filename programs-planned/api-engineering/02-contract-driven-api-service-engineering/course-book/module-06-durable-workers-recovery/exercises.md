# Exercises — Module 06: Durable Workers and Recovery

Work through all twelve problems before opening the answers. In **Durable Workers and Recovery**, every response must settle this question: **What makes a 202 Accepted operation honest after the API process or worker dies?** Answer as though another team must implement and operate the design. Ambiguous ownership, unbounded behavior, and evidence-free claims are defects.

## 1. Why is 202 dishonest for an in-memory task?

## 2. What guarantee does `SKIP LOCKED` provide and not provide?

## 3. Why increment lease generation on reclaim?

## 4. Can exactly-once execution be guaranteed here?

## 5. Why process outside the claim transaction?

## 6. How should cancellation race with completion?

## 7. What makes a retryable job error?

## 8. Why can a heartbeat not prove useful progress?

## 9. What is a poison job?

## 10. How can duplicate artifact publication converge?

## 11. Trace durable job leasing and fencing in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/worker.py` or `capstone/tracks/typescript-fastify/src/worker.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare durable job leasing and fencing across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/worker.py` with `capstone/tracks/typescript-fastify/src/worker.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 06 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
