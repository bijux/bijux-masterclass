# Lab — Approve fewer services than you reject

> **Module 01:** Distribution Economics, Boundary Evidence, and Architecture Fitness Functions

## Objective

Use the Course 7 boundary dossier and measured criteria to decide which capabilities deserve extraction.

## Why this lab matters

This lab turns the module’s governing question—**When does a remote service boundary create more value than the coordination, latency, failure, and operational costs it introduces?**—into a falsifiable experiment. Artifact bytes, checksums, object storage, retention, and egress have a distinct scaling profile. The extraction is conditional because authorization and completion currently depend on run state. Course 8 first designs narrow capabilities, event-fed references, and orphan reconciliation.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Freeze the predecessor handoff. Load the boundary scorecard and the current transaction, event, RPC, and ownership records.

## Hypothesis

The clean implementation should satisfy this claim: **Every approved service has one owner, autonomous writes or an explicitly non-data role, independent value, acceptable coordination cost, and reversal criteria. At least three attractive but harmful services are rejected.** When the lab introduces this fault—**Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Fill every score with a cited source: change history, transaction boundary, workload, security rule, or owner statement.
2. Approve Notification Delivery, conditionally approve Artifact Delivery, and keep Analysis Control cohesive.
3. Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths.
4. Write reversal criteria for every approved and retained boundary.
5. Run `make boundary-proof` and inspect the machine-readable report.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Use the Course 7 boundary dossier and measured criteria to decide which capabilities deserve extraction**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Every approved service has one owner, autonomous writes or an explicitly non-data role, independent value, acceptable coordination cost, and reversal criteria. At least three attractive but harmful services are rejected.

## Required evidence

- `capstone/architecture/boundary-scorecard.yaml`
- `capstone/architecture/adr/0001-keep-analysis-control-cohesive.md`
- `reports/module-01-boundary-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Distribution Economics, Boundary Evidence, and Architecture Fitness Functions**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore the canonical scorecard after experimentation and remove any unapproved service entries.

## Completion gate

The scorecard and ADR proof pass, and you can defend one rejection as rigorously as one extraction.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Distribution Economics, Boundary Evidence, and Architecture Fitness Functions**. A green command without the negative case and causal explanation does not satisfy this gate.
