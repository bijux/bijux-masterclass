# Lab — Build the service catalogue and remove fake autonomy

> **Module 02:** Service Boundaries, Bounded Contexts, and Contract Ownership

## Objective

Define capability, contract, state, data, and operational ownership for every component.

## Why this lab matters

This lab turns the module’s governing question—**How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services?**—into a falsifiable experiment. The catalogue must classify every component, assign one accountable owner, declare canonical data, and reject table-shaped services. You must be able to explain why Worker Plane is a deployment boundary but not a business-state boundary.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the service catalogue, bounded-context map, contract ownership map, and explicit list of capabilities that remain inside Analysis Control**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the approved boundary scorecard and inherited HTTP, event, and RPC catalogues.

## Hypothesis

The clean implementation should satisfy this claim: **Every business fact has one canonical writer, every interface has one owner, and no table-shaped service or shared domain policy survives.** When the lab introduces this fault—**Find and remove shared domain policies that would couple services**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Classify each component as business service, edge component, compute plane, platform component, or analytical consumer.
2. Assign one contract owner and one state authority to every inherited and new interface.
3. Create anti-corruption mappings for artifact and notification models.
4. Find and remove shared domain policies that would couple services.
5. Run `make ownership-proof` and review every single-writer assertion.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Find and remove shared domain policies that would couple services**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Define capability, contract, state, data, and operational ownership for every component**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Every business fact has one canonical writer, every interface has one owner, and no table-shaped service or shared domain policy survives.

## Required evidence

- `capstone/architecture/service-catalog.yaml`
- `capstone/architecture/data-ownership.yaml`
- `reports/module-02-ownership-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Service Boundaries, Bounded Contexts, and Contract Ownership**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Find and remove shared domain policies that would couple services** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove experimental catalogue entries and restore canonical ownership.

## Completion gate

Ownership proof passes and you can explain why Worker Plane and Gateway are not business-state owners.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Service Boundaries, Bounded Contexts, and Contract Ownership**. A green command without the negative case and causal explanation does not satisfy this gate.
