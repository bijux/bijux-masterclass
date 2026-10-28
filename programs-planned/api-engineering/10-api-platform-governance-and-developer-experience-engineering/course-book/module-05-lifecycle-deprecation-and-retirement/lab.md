# Lab — Attempt an unsafe retirement

> **Module 05:** Lifecycle, Compatibility, Deprecation, and Retirement

## Objective

Publish the lifecycle policy, consumer inventory, deprecation impact report, and retirement decision.

## Why this lab matters

This lab turns the module’s governing question—**How can an API evolve and eventually disappear without transferring hidden cost to consumers?**—into a falsifiable experiment. evaluate transition checks allowed edges and required evidence. deprecation impact calculates affected and blocking consumers from the inventory. These functions are intentionally separate: lifecycle policy defines what is required, while consumer data supplies current impact.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the lifecycle policy, consumer inventory, deprecation impact report, and retirement decision**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make lifecycle-proof`. Inspect the consumer inventory, lifecycle policy, and
Analysis HTTP 1.1 deprecation record.

## Hypothesis

The clean implementation should satisfy this claim: **Current retirement is blocked. Verified migration can make it eligible. Deleting the consumer record is not evidence of migration and must be detected as an inventory-integrity problem.** When the lab introduces this fault—**Finally, remove the consumer record instead of completing migration and compare the evidence quality**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Attempt retirement with the current consumer state. Then mark the legacy CLI as
migration-complete and rerun impact analysis. Finally, remove the consumer record
instead of completing migration and compare the evidence quality.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Finally, remove the consumer record instead of completing migration and compare the evidence quality**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish the lifecycle policy, consumer inventory, deprecation impact report, and retirement decision**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Current retirement is blocked. Verified migration can make it eligible. Deleting
the consumer record is not evidence of migration and must be detected as an
inventory-integrity problem.

## Required evidence

Create `reports/module-05-retirement.json` with affected consumers, evidence
sources, notice status, runtime plan, decision, and residual uncertainty.

## Interpretation and defense

1. Which state or effect is authoritative for **Lifecycle, Compatibility, Deprecation, and Retirement**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Finally, remove the consumer record instead of completing migration and compare the evidence quality** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore the original inventory and rerun lifecycle proof.

## Completion gate

Retirement cannot advance while a blocking consumer or unresolved inventory gap
remains.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Lifecycle, Compatibility, Deprecation, and Retirement**. A green command without the negative case and causal explanation does not satisfy this gate.
