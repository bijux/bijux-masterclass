# Lab — Decide what the platform should own

> **Module 01:** Platform Product Model and Operating Boundaries

## Objective

Publish the platform product charter, user journeys, ownership boundary, and initial outcome model.

## Why this lab matters

This lab turns the module’s governing question—**Which recurring problems should an API platform own, and which decisions must stay with domain teams?**—into a falsifiable experiment. Analysis API Platform 1.0 begins with four user journeys: discover an API, publish a release, onboard a consumer, and deprecate a version. Every capstone mechanism must improve one of these journeys or protect an invariant established in earlier courses.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the platform product charter, user journeys, ownership boundary, and initial outcome model**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Read `capstone/predecessor/handoff/platform-boundary-brief.yaml` and inspect the
current catalog, registry, runtime policy, and support routes.

## Hypothesis

The clean implementation should satisfy this claim: **Digest publication, search, sandbox control, and consumer retirement tracking may belong to the platform. Project-owner authorization and domain repair remain with the owning services.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

Evaluate six proposed capabilities: contract digest publication, project-owner
authorization in the gateway, documentation search, domain-state repair, sandbox
creation, and consumer retirement tracking. For each, identify the user problem,
authority, repeated cost, central operating cost, and outcome metric.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish the platform product charter, user journeys, ownership boundary, and initial outcome model**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Digest publication, search, sandbox control, and consumer retirement tracking may
belong to the platform. Project-owner authorization and domain repair remain with
the owning services.

## Required evidence

Create `reports/module-01-platform-product.json` with one decision record per
capability and a reason that names the authority boundary.

## Interpretation and defense

1. Which state or effect is authoritative for **Platform Product Model and Operating Boundaries**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove scratch proposals. Rerun `make module-01-proof`.

## Completion gate

Every accepted capability improves a named user journey, and every rejected
capability protects a domain boundary rather than merely reflecting preference.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Platform Product Model and Operating Boundaries**. A green command without the negative case and causal explanation does not satisfy this gate.
