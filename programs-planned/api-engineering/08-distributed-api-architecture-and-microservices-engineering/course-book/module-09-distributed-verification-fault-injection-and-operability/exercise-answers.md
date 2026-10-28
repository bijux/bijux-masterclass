# Worked Answers — Module 09: Distributed Verification, Fault Injection, and Operability

Use these solutions to audit your reasoning for **Distributed Verification, Fault Injection, and Operability**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why can all service unit tests pass while the system is wrong?

They do not prove ownership, timing, cross-service version behavior, network ambiguity, or final durable outcome.

**Decisive evidence:** distributed proof ladder

The chapter’s decisive distinction is this: Claim Minimum evidence --- --- one writer per fact ownership catalogue plus credential/database tests no synchronous cycle declared graph proof plus runtime trace review idempotent cross-service effect duplicate and lost-response schedule compensatable workflow failure before and after every durable step bounded version skew old/new matrix and rollback rehearsal tenant isolation negative cross-tenant tests at every owner safe cutover shadow comparison, canary, reconciliation, route rollback operable service SLO, alerts, runbook, owner, recovery exercise

## 2. What is the decisive oracle after a timeout following commit?

Durable state and stable effect identity at the owning service, not the caller’s exception or trace alone.

**Decisive evidence:** after-commit reconciliation

In the cumulative capstone, the rule becomes concrete: While a run is running, terminate Artifact Service after it commits an artifact but before the worker receives the response. The worker retries with the same effect identity. Exactly one artifact remains published, Control eventually attaches that artifact or marks it for compensation, and no run is reported complete without an authoritative reference.

## 3. Why must fault injection name an exact timing point?

Failure before receive, before commit, after commit, and after publish have different outcomes and recovery requirements.

**Decisive evidence:** fault schedule definition

A useful way to reason about the boundary is: If a proposed service split requires an unmanageable proof matrix, that is architecture evidence. Complexity in testing, release, and reconciliation is not an external inconvenience; it is part of the boundary’s cost.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 4. What makes a topology test different from an end-to-end test?

It verifies graph, ownership, trust, routing, and version properties across components, while end-to-end tests exercise selected user outcomes.

**Decisive evidence:** topology policy proof

The implementation consequence is: Consumer-driven contract tests can prove that known consumer expectations remain valid. They cannot prove that the service has a good boundary, that data ownership is correct, or that an unknown consumer is safe. Use them within the larger proof ladder.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 5. Why should a planted defect have an assigned rejecting proof?

It demonstrates proof sensitivity. A happy-path suite that cannot reject its intended defect is weak.

**Decisive evidence:** mutation/defect evidence

The important nuance is: Both tracks run shared semantic vectors and independent unit tests. The course tool separately verifies architecture YAML, service-owned migrations, release candidates, and planted defects. The optional Compose/Kubernetes routes are classified as environment-backed rather than silently simulated.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 6. How do traces help after an artifact orphan?

They locate attempts and timing, but reconciliation between Artifact and Control authorities determines the actual divergence.

**Decisive evidence:** trace plus durable-state report

Under concurrency or failure, the distinction becomes: A trace should preserve causal structure without inventing parentage. Synchronous downstream calls are child spans. Asynchronous consumers commonly link to the producing context while starting a new trace or processing span according to the instrumentation model.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 7. What is wrong with declaring all services healthy during an incident?

Process health does not prove a critical journey. One missing cross-service effect can violate the outcome while every process responds.

**Decisive evidence:** critical-journey evidence

The design remains honest only if: Claim Minimum evidence --- --- one writer per fact ownership catalogue plus credential/database tests no synchronous cycle declared graph proof plus runtime trace review idempotent cross-service effect duplicate and lost-response schedule compensatable workflow failure before and after every durable step bounded version skew old/new matrix and rollback rehearsal tenant isolation negative cross-tenant tests at every owner safe cutover shadow comparison, canary, reconciliation, route rollback operable service SLO, alerts, runbook, owner, recovery exercise

## 8. What should a bounded fault plan include?

Hypothesis, injection point, blast radius, expected user and durable outcome, telemetry, abort, cleanup, and residual uncertainty.

**Decisive evidence:** fault plan review

The consumer-facing consequence is: While a run is running, terminate Artifact Service after it commits an artifact but before the worker receives the response. The worker retries with the same effect identity. Exactly one artifact remains published, Control eventually attaches that artifact or marks it for compensation, and no run is reported complete without an authoritative reference.

## 9. Why do consumer-driven contract tests not prove a good boundary?

They validate known expectations, not data ownership, synchronous coupling, or organizational autonomy.

**Decisive evidence:** boundary evidence versus contract evidence

The operational consequence is: Consumer-driven contract tests can prove that known consumer expectations remain valid. They cannot prove that the service has a good boundary, that data ownership is correct, or that an unknown consumer is safe. Use them within the larger proof ladder.

**Evidence.** Apply the boundary scorecard and ownership catalogue, then reject duplicate writers, shared private data, cyclic dependencies, and capabilities lacking reversal criteria.

## 10. How do you test a synchronous cycle rejection?

Construct the proposed graph and require the architecture fitness function to fail before deployment.

**Decisive evidence:** cycle mutant

The strongest engineering interpretation is: If a proposed service split requires an unmanageable proof matrix, that is architecture evidence. Complexity in testing, release, and reconciliation is not an external inconvenience; it is part of the boundary’s cost.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 11. Why is a live Compose test stronger than an in-process model but still limited?

It exercises real process and network behavior, but not production scale, platform, data, or every failure schedule.

**Decisive evidence:** evidence classification

The defect-oriented view is: A trace should preserve causal structure without inventing parentage. Synchronous downstream calls are child spans. Asynchronous consumers commonly link to the producing context while starting a new trace or processing span according to the instrumentation model.

**Evidence.** Require a remote-process fault experiment, ownership/reconciliation evidence, operational responsibility, and a quantified benefit exceeding distribution cost.

## 12. What is the final operator question during distributed ambiguity?

Which service owns the truth, what effect identity can be reconciled, and what safe repair or compensation is available?

**Decisive evidence:** incident decision record

Across the Python and TypeScript tracks, the invariant is: Both tracks run shared semantic vectors and independent unit tests. The course tool separately verifies architecture YAML, service-owned migrations, release candidates, and planted defects. The optional Compose/Kubernetes routes are classified as environment-backed rather than silently simulated.
