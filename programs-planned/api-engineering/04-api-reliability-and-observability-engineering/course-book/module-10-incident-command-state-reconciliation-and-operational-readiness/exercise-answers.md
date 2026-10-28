# Reference Answers — Module 10: Incident Command, Reconciliation, and Readiness

Read after attempting all twelve Incident Command, Reconciliation, and Readiness exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What is the incident lead responsible for?

**Answer.** Objectives, severity, roles, decision approval, communication cadence, escalation, and declaring transitions—not personally performing every investigation.

## 2. What is the difference between an observation and an inference?

**Answer.** An observation cites measured/public/durable evidence; an inference proposes a mechanism explaining it and carries confidence.

## 3. Why mitigate before root-cause certainty?

**Answer.** User impact may require a bounded reversible action while investigation continues, provided the action preserves safety and evidence.

## 4. Why must reconciliation begin read-only?

**Answer.** It creates a stable inventory, preserves evidence, allows review, and prevents early repairs from hiding or worsening related inconsistencies.

## 5. What is a stable repair key?

**Answer.** A deterministic identifier derived from finding type and authoritative object identity so planning/execution can be deduplicated and journaled.

## 6. How should a missing outbox for a genuinely completed run be repaired?

**Answer.** Verify all terminal invariants and event semantics first, then insert exactly one outbox record under a stable repair key and journal the transaction.

**Common mistake.** Describing a procedure for “How should a missing outbox for a genuinely completed run be repaired?” without a falsifiable completion condition.

## 7. When is an incident resolved?

**Answer.** Impact is controlled, durable state is reconciled or bounded, monitoring is stable, required repairs/risks are owned, and communication records the current truth.

## 8. What makes a release operationally incompatible?

**Answer.** It removes required evidence/control, changes health semantics unsafely, breaks runbook/alert linkage, violates migration/drain assumptions, or cannot be rolled back—even if API schema remains compatible.

## 9. Why distinguish event time and discovery time?

**Answer.** A failure may occur long before detection; the gap measures detection quality and affects causal reconstruction.

## 10. What should a post-incident action contain?

**Answer.** Specific defect/risk, owner, priority, due condition, linked requirement, regression/proof, and closure evidence.

## 11. Trace incident command and durable reconciliation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py` and `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`. The required invariant is that operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers.

## 12. Compare incident command and durable reconciliation across Python and TypeScript

Both tracks must preserve this invariant: operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers. The intentional difference is that data-access mechanics differ; findings and repair plans must be deterministic and reviewable.
