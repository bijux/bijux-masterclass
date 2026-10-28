# Lab — Release one service while the rest of the platform keeps running

> **Module 08:** Deployment Independence, Version Skew, and Release Choreography

## Objective

Prove a mixed-version rollout, data expansion, canary, rollback, and retirement sequence.

## Why this lab matters

This lab turns the module’s governing question—**How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?**—into a falsifiable experiment. Add nullable storage column under Artifact ownership. Deploy provider 1.1 that writes and returns the optional field. Verify old consumers ignore it. Deploy new consumers that tolerate absence. Backfill when useful. Observe mixed-version operation. Require the field only in a later contract version after old writers retire, if ever.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish and execute a mixed-version release matrix for Analysis Control, Artifact, Notification, Gateway, and Worker Plane with expand-and-contract changes and rollback evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the version ledger, release policy, service migration heads, and accepted/rejected candidate fixtures.

## Hypothesis

The clean implementation should satisfy this claim: **Every supported pair preserves existing outcomes; unsupported major skew is rejected; rollback reads all committed data; no other service writes Artifact schema.** When the lab introduces this fault—**Remove the old writer and contract only after the coexistence window passes**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Run all supported consumer/provider version pairs.
2. Add an optional Artifact Service field through expand-and-contract migration.
3. Shadow and canary Artifact 1.1 while Gateway and Control remain mixed 1.0/1.1.
4. Rollback the route after injecting candidate divergence.
5. Remove the old writer and contract only after the coexistence window passes.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove the old writer and contract only after the coexistence window passes**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove a mixed-version rollout, data expansion, canary, rollback, and retirement sequence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Every supported pair preserves existing outcomes; unsupported major skew is rejected; rollback reads all committed data; no other service writes Artifact schema.

## Required evidence

- `capstone/architecture/release-policy.yaml`
- `capstone/architecture/version-ledger.yaml`
- `reports/module-08-release-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Deployment Independence, Version Skew, and Release Choreography**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove the old writer and contract only after the coexistence window passes** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore service versions, route weights, and migration fixtures.

## Completion gate

Release proof passes accepted skew and rejects all incompatible candidates with exact reasons.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Deployment Independence, Version Skew, and Release Choreography**. A green command without the negative case and causal explanation does not satisfy this gate.
