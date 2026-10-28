# Lab — Complete a run across services without a global transaction

> **Module 05:** Distributed Workflows, Sagas, Compensation, and Process Managers

## Objective

Implement and falsify the artifact publication and run completion saga.

## Why this lab matters

This lab turns the module’s governing question—**How do we preserve business intent when one workflow crosses services that cannot share a transaction?**—into a falsifiable experiment. Analysis Control owns the process manager because it owns the final run decision and current attempt. Artifact Service owns artifact effects and compensation execution. Notification is outside the completion saga because its outcome does not change run truth.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement the artifact-publication and run-completion saga with durable step identity, semantic locks, compensation, timeout handling, and operator-visible reconciliation**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the saga catalogue, capability profile, current lease vectors, and artifact service reference.

## Hypothesis

The clean implementation should satisfy this claim: **Happy and duplicate schedules complete once; stale attempts cannot complete; compensation is idempotent; no ambiguous effect remains unexplained.** When the lab introduces this fault—**Inject timeout after artifact commit and prove retry returns the existing artifact**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Execute the happy path with stable saga, event, command, and effect identities.
2. Inject timeout after artifact commit and prove retry returns the existing artifact.
3. Advance the lease generation before completion and require compensation.
4. Replay duplicate ArtifactStored and CompleteRun messages.
5. Run `make saga-proof` and reconcile all final authority states.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject timeout after artifact commit and prove retry returns the existing artifact**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement and falsify the artifact publication and run completion saga**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Happy and duplicate schedules complete once; stale attempts cannot complete; compensation is idempotent; no ambiguous effect remains unexplained.

## Required evidence

- `capstone/architecture/saga-catalog.yaml`
- `reports/module-05-saga-proof.json`
- `reports/module-05-reconciliation.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Distributed Workflows, Sagas, Compensation, and Process Managers**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject timeout after artifact commit and prove retry returns the existing artifact** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Reset saga stores, artifacts, runs, and injected fault schedules.

## Completion gate

Saga proof passes every shared schedule and reconciliation has zero unexplained findings.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Distributed Workflows, Sagas, Compensation, and Process Managers**. A green command without the negative case and causal explanation does not satisfy this gate.
