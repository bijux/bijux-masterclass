# Lab — Build and reconcile the ownership graph

> **Module 02:** Catalog, Ownership Graph, and Metadata Authority

## Objective

Publish the Analysis Platform catalog and ownership graph.

## Why this lab matters

This lab turns the module’s governing question—**How can a central catalog be useful without pretending to own every fact it displays?**—into a falsifiable experiment. Take component:default/analysis-graph-gateway. Its owner is the API Platform team, its system is Analysis Platform, it provides Analysis Graph API, and it consumes Analysis HTTP, Artifact HTTP, and Notification HTTP capabilities. This record does not mean the platform team owns project or artifact facts. It means the team owns the component that composes those facts under source-service contracts.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the Analysis Platform catalog and ownership graph**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run `make catalog-proof`. Inspect `capstone/catalog/entities.json` and
`catalog-info.yaml`.

## Hypothesis

The clean implementation should satisfy this claim: **The first four defects fail catalog validation. The runtime-only component is reported as an unregistered observation, not silently adopted as an authoritative entity.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Create four scratch defects: an unknown owner, an API with no provider, a
component consuming an unknown API, and two records with the same canonical
identity. Also create one observed runtime component not present in the source
catalog.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish the Analysis Platform catalog and ownership graph**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The first four defects fail catalog validation. The runtime-only component is
reported as an unregistered observation, not silently adopted as an authoritative
entity.

## Required evidence

Produce `reports/module-02-catalog-reconciliation.json` containing rejected
records, source authority, derived relations, freshness, and reconciliation
recommendations.

## Interpretation and defense

1. Which state or effect is authoritative for **Catalog, Ownership Graph, and Metadata Authority**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove scratch entities and rerun catalog proof.

## Completion gate

You can answer who owns, implements, consumes, and supports every active API
without relying on a free-text search.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Catalog, Ownership Graph, and Metadata Authority**. A green command without the negative case and causal explanation does not satisfy this gate.
