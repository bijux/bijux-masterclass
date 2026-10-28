# Lab — Extract two services and defend keeping the rest together

> **Module 10:** Incremental Extraction, Strangler Migration, and Final Architecture Defense

## Objective

Execute the staged Notification and Artifact extraction, prove rollback and decommission, and publish the Course 9 handoff.

## Why this lab matters

This lab turns the module’s governing question—**How do we extract services incrementally, preserve every existing contract, and retain a safe path to stop, roll back, or merge a service back into the platform?**—into a falsifiable experiment. Course 8 includes merge-back criteria. If Notification and Control always release together, one team owns both, event lag creates no value, and on-call cost exceeds isolation benefit, merging Notification back into the modular service may be the correct architecture. The event contract can remain useful even if deployment changes.

It advances the cumulative Analysis Runs Platform by requiring this result: **Extract Notification Delivery and Artifact Delivery through shadow, compare, backfill, cutover, and decommission phases; retain Analysis Control; and publish the Course 9 graph-access handoff**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Start from the verified modular baseline, extraction plan, service-owned migrations, and clean reconciliation state.

## Hypothesis

The clean implementation should satisfy this claim: **Public HTTP, event, and RPC contracts remain valid; extracted services own their data; Analysis Control remains cohesive; rollback works; final reconciliation is empty.** When the lab introduces this fault—**Inject candidate divergence and execute rollback before final cutover**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Shadow and cut over Notification Delivery using event replay with external effects controlled.
2. Backfill and checksum Artifact data, shadow reads, then move write and read authority in stages.
3. Inject candidate divergence and execute rollback before final cutover.
4. Decommission legacy writers and routes only after the declared evidence window.
5. Run `make final-defense-proof`, generate the outgoing handoff, and defend every retained boundary.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject candidate divergence and execute rollback before final cutover**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Execute the staged Notification and Artifact extraction, prove rollback and decommission, and publish the Course 9 handoff**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Public HTTP, event, and RPC contracts remain valid; extracted services own their data; Analysis Control remains cohesive; rollback works; final reconciliation is empty.

## Required evidence

- `capstone/architecture/extraction-plan.yaml`
- `capstone/final-defense/architecture-summary.json`
- `capstone/handoff/`
- `reports/module-10-final-defense.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Incremental Extraction, Strangler Migration, and Final Architecture Defense**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject candidate divergence and execute rollback before final cutover** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Return the laboratory to the accepted distributed-1.0 topology and remove temporary shadow/backfill state.

## Completion gate

Final defense and handoff proofs pass, with zero shared writers, zero sync cycles, and zero unexplained reconciliation findings.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Incremental Extraction, Strangler Migration, and Final Architecture Defense**. A green command without the negative case and causal explanation does not satisfy this gate.
