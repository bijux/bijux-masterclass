# Exercises — Module 10: Incident Command, Reconciliation, and Readiness

Work through all twelve problems before opening the answers. In **Incident Command, Reconciliation, and Readiness**, every response must settle this question: **How do responders command an incident, reconcile durable state, repair safely, and decide whether a release is operationally ready?** Conclude each problem with a release decision: what may proceed, what must be rejected, and what remains unproven by the available environment.

## 1. What is the incident lead responsible for?

## 2. What is the difference between an observation and an inference?

## 3. Why mitigate before root-cause certainty?

## 4. Why must reconciliation begin read-only?

## 5. What is a stable repair key?

## 6. How should a missing outbox for a genuinely completed run be repaired?

## 7. When is an incident resolved?

## 8. What makes a release operationally incompatible?

## 9. Why distinguish event time and discovery time?

## 10. What should a post-incident action contain?

## 11. Trace incident command and durable reconciliation in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py` or `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare incident command and durable reconciliation across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py` with `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 10 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
