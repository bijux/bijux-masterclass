# Lab — Reconcile runtime state and product outcomes

> **Module 09:** Runtime Control Plane, Usage Intelligence, and Support Operations

## Objective

Publish runtime desired state, drift proof, product metrics, and support routing evidence.

## Why this lab matters

This lab turns the module’s governing question—**How can platform metadata remain connected to the running system and to consumer outcomes without becoming a new domain owner or surveillance system?**—into a falsifiable experiment. Desired state and observed state have different authorities. The release and runtime policy produce desired routes. Deployment and gateway systems report observed routes. Reconciliation compares them and raises missing, extra, or changed records. It should not silently overwrite either side: an unexpected observed route may be an incident, while a missing route may be an incomplete deployment.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish runtime desired state, drift proof, product metrics, and support routing evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make runtime-proof`, `make analytics-proof`, and `make support-proof`.

## Hypothesis

The clean implementation should satisfy this claim: **Runtime drift is visible. Gateway-owned domain authorization is rejected. Deprecated use appears in migration impact. Support reaches the domain owner for semantics and the platform owner for portal failure.** When the lab introduces this fault—**Then route one contract question and one portal failure through support**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Add an undocumented gateway route, change domain authorization to the gateway,
and simulate continued traffic on a deprecated version. Then route one contract
question and one portal failure through support.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Then route one contract question and one portal failure through support**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish runtime desired state, drift proof, product metrics, and support routing evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Runtime drift is visible. Gateway-owned domain authorization is rejected.
Deprecated use appears in migration impact. Support reaches the domain owner for
semantics and the platform owner for portal failure.

## Required evidence

Create `reports/module-09-runtime-product.json` with drift, policy boundary,
consumer outcome metrics, deprecated impact, support owner, and privacy notes.

## Interpretation and defense

1. Which state or effect is authoritative for **Runtime Control Plane, Usage Intelligence, and Support Operations**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Then route one contract question and one portal failure through support** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore desired and current route parity, remove synthetic usage, and rerun
proofs.

## Completion gate

Runtime state, release identity, owner, support, and product outcomes can be
connected without moving business policy or collecting unnecessary personal
data.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Runtime Control Plane, Usage Intelligence, and Support Operations**. A green command without the negative case and causal explanation does not satisfy this gate.
