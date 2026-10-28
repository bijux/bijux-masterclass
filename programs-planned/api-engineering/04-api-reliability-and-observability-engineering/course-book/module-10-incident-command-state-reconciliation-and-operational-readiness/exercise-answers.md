# Worked Answers — Module 10: Incident Command, Reconciliation, and Readiness

Use these solutions to audit your reasoning for **Incident Command, Reconciliation, and Readiness**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What is the incident lead responsible for?

Objectives, severity, roles, decision approval, communication cadence, escalation, and declaring transitions—not personally performing every investigation.

The chapter’s decisive distinction is this: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=10 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 2. What is the difference between an observation and an inference?

An observation cites measured/public/durable evidence; an inference proposes a mechanism explaining it and carries confidence.

In the cumulative capstone, the rule becomes concrete: Apply Incident command, Severity, Mitigation to this module’s capstone increment: Execute a full non-security incident, produce a defensible timeline, run read-only reconciliation, plan idempotent repairs, validate runbooks and alerts, and generate the Course 4 handoff to performance engineering. State one misleading green signal and the durable observation that would overrule it.

## 3. Why mitigate before root-cause certainty?

User impact may require a bounded reversible action while investigation continues, provided the action preserves safety and evidence.

A useful way to reason about the boundary is: Begin with the failure Everyone is incident commander . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible. , and rerun the focused regression in both languages.

## 4. Why must reconciliation begin read-only?

It creates a stable inventory, preserves evidence, allows review, and prevents early repairs from hiding or worsening related inconsistencies.

The implementation consequence is: Incident response separates command, diagnosis, mitigation, repair, communication, and evidence. Recovery is incomplete until durable invariants are reconciled, repairs are idempotent and journaled, and the release can demonstrate its required observability and rollback boundaries.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 5. What is a stable repair key?

A deterministic identifier derived from finding type and authoritative object identity so planning/execution can be deduplicated and journaled.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=10 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 6. How should a missing outbox for a genuinely completed run be repaired?

Verify all terminal invariants and event semantics first, then insert exactly one outbox record under a stable repair key and journal the transaction.

**Common mistake.** Describing a procedure for “How should a missing outbox for a genuinely completed run be repaired?” without a falsifiable completion condition.

Under concurrency or failure, the distinction becomes: The ten module results now satisfy this course promise: A reliability profile with deadlines, resilience, lifecycle control, telemetry, SLIs, SLOs, alerting, fault injection, reconciliation, and incident readiness. The next course is API Performance, Capacity, and Traffic Engineering ; it consumes the outgoing handoff rather than reinterpreting completed work.

## 7. When is an incident resolved?

Impact is controlled, durable state is reconciled or bounded, monitoring is stable, required repairs/risks are owned, and communication records the current truth.

The design remains honest only if: Incident response separates command, diagnosis, mitigation, repair, communication, and evidence. Recovery is incomplete until durable invariants are reconciled, repairs are idempotent and journaled, and the release can demonstrate its required observability and rollback boundaries.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 8. What makes a release operationally incompatible?

It removes required evidence/control, changes health semantics unsafely, breaks runbook/alert linkage, violates migration/drain assumptions, or cannot be rolled back—even if API schema remains compatible.

The consumer-facing consequence is: The ten module results now satisfy this course promise: A reliability profile with deadlines, resilience, lifecycle control, telemetry, SLIs, SLOs, alerting, fault injection, reconciliation, and incident readiness. The next course is API Performance, Capacity, and Traffic Engineering ; it consumes the outgoing handoff rather than reinterpreting completed work.

## 9. Why distinguish event time and discovery time?

A failure may occur long before detection; the gap measures detection quality and affects causal reconstruction.

The operational consequence is: Begin with the failure Everyone is incident commander . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Assign one lead, one operations executor, focused investigators, and one recorder. Changes are proposed, approved, timestamped, and reversible. , and rerun the focused regression in both languages.

## 10. What should a post-incident action contain?

Specific defect/risk, owner, priority, due condition, linked requirement, regression/proof, and closure evidence.

The strongest engineering interpretation is: Apply Incident command, Severity, Mitigation to this module’s capstone increment: Execute a full non-security incident, produce a defensible timeline, run read-only reconciliation, plan idempotent repairs, validate runbooks and alerts, and generate the Course 4 handoff to performance engineering. State one misleading green signal and the durable observation that would overrule it.

## 11. Trace incident command and durable reconciliation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/reconcile.py` and `capstone/tracks/typescript-fastify/src/reliability/reconcile.ts`. The required invariant is that operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=10 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare incident command and durable reconciliation across Python and TypeScript

Both tracks must preserve this invariant: operators diagnose from telemetry but reconcile and repair from read-only durable facts using stable, idempotent repair identifiers. The intentional difference is that data-access mechanics differ; findings and repair plans must be deterministic and reviewable.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=10 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
