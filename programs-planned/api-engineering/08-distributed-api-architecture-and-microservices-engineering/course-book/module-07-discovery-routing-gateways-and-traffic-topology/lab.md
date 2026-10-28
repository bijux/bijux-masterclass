# Lab — Route around failure without moving the domain into the gateway

> **Module 07:** Discovery, Routing, Gateways, and Traffic Topology

## Objective

Implement health- and version-aware discovery, bounded canary routing, and a thin public edge.

## Why this lab matters

This lab turns the module’s governing question—**How do callers find healthy service instances and route traffic without moving business ownership into gateways or creating several competing retry layers?**—into a falsifiable experiment. A service is a logical capability. An instance is one running copy. An address is one route to an instance. A health observation is a time-bounded claim about whether an instance should receive a class of work.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement service registration, health-aware routing, gateway edge policy, bounded traffic shifting, and an optional Kubernetes topology with explicit ownership of each routing decision**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the dependency graph, lifecycle policies, service versions, and gateway responsibility ADR.

## Hypothesis

The clean implementation should satisfy this claim: **Only healthy accepting compatible instances receive traffic; retries have one owner; shadow has no uncontrolled effects; gateway owns no business state.** When the lab introduces this fault—**Canary a stable resource-key fraction and inject candidate failure**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Register two Control instances and remove one from eligibility during drain.
2. Route only to versions supported by the caller matrix.
3. Shadow artifact reads and compare exact semantic results while returning legacy authority.
4. Canary a stable resource-key fraction and inject candidate failure.
5. Run `make routing-proof` and prove rollback occurs without gateway domain logic.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Canary a stable resource-key fraction and inject candidate failure**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement health- and version-aware discovery, bounded canary routing, and a thin public edge**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Only healthy accepting compatible instances receive traffic; retries have one owner; shadow has no uncontrolled effects; gateway owns no business state.

## Required evidence

- `capstone/architecture/dependency-graph.yaml`
- `reports/module-07-routing-proof.json`
- `capstone/architecture/adr/0006-gateway-owns-no-business-state.md`

## Interpretation and defense

1. Which state or effect is authoritative for **Discovery, Routing, Gateways, and Traffic Topology**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Canary a stable resource-key fraction and inject candidate failure** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Restore instance health, route phase, and canary fraction.

## Completion gate

Routing proof passes and a failed canary rolls back to a compatible authoritative path.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Discovery, Routing, Gateways, and Traffic Topology**. A green command without the negative case and causal explanation does not satisfy this gate.
