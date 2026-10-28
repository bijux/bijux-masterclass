# Worked answers — Distributed Verification, Fault Injection, and Operability

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why can all service unit tests pass while the system is wrong?

They do not prove ownership, timing, cross-service version behavior, network ambiguity, or final durable outcome.

**Decisive evidence:** distributed proof ladder

## 2. What is the decisive oracle after a timeout following commit?

Durable state and stable effect identity at the owning service, not the caller’s exception or trace alone.

**Decisive evidence:** after-commit reconciliation

## 3. Why must fault injection name an exact timing point?

Failure before receive, before commit, after commit, and after publish have different outcomes and recovery requirements.

**Decisive evidence:** fault schedule definition

## 4. What makes a topology test different from an end-to-end test?

It verifies graph, ownership, trust, routing, and version properties across components, while end-to-end tests exercise selected user outcomes.

**Decisive evidence:** topology policy proof

## 5. Why should a planted defect have an assigned rejecting proof?

It demonstrates proof sensitivity. A happy-path suite that cannot reject its intended defect is weak.

**Decisive evidence:** mutation/defect evidence

## 6. How do traces help after an artifact orphan?

They locate attempts and timing, but reconciliation between Artifact and Control authorities determines the actual divergence.

**Decisive evidence:** trace plus durable-state report

## 7. What is wrong with declaring all services healthy during an incident?

Process health does not prove a critical journey. One missing cross-service effect can violate the outcome while every process responds.

**Decisive evidence:** critical-journey evidence

## 8. What should a bounded fault plan include?

Hypothesis, injection point, blast radius, expected user and durable outcome, telemetry, abort, cleanup, and residual uncertainty.

**Decisive evidence:** fault plan review

## 9. Why do consumer-driven contract tests not prove a good boundary?

They validate known expectations, not data ownership, synchronous coupling, or organizational autonomy.

**Decisive evidence:** boundary evidence versus contract evidence

## 10. How do you test a synchronous cycle rejection?

Construct the proposed graph and require the architecture fitness function to fail before deployment.

**Decisive evidence:** cycle mutant

## 11. Why is a live Compose test stronger than an in-process model but still limited?

It exercises real process and network behavior, but not production scale, platform, data, or every failure schedule.

**Decisive evidence:** evidence classification

## 12. What is the final operator question during distributed ambiguity?

Which service owns the truth, what effect identity can be reconciled, and what safe repair or compensation is available?

**Decisive evidence:** incident decision record
