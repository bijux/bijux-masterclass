# Lab — Break the synchronous cycle before it reaches production

> **Module 04:** Synchronous Collaboration, API Composition, and Dependency Budgets

## Objective

Build and verify the complete synchronous dependency graph, deadline, retry, and composition policy.

## Why this lab matters

This lab turns the module’s governing question—**How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?**—into a falsifiable experiment. Course 8 removes the reverse authorization call with a capability and forbids cycles in dependency-graph.yaml. A graph traversal can detect declared cycles, but runtime traces and code review are still needed to find undeclared calls.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish an acyclic synchronous dependency graph, one edge-owned deadline budget, bounded fan-out rules, and a gateway composition path that degrades truthfully**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load service catalogue, public critical journeys, gRPC methods, and proposed gateway routes.

## Hypothesis

The clean implementation should satisfy this claim: **The graph is acyclic, public depth is at most two, every edge has one deadline/retry owner, and dependency failure never becomes false business data.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Draw every synchronous edge and mark caller, callee, purpose, deadline owner, retry owner, and fallback.
2. Introduce a Control↔Artifact cycle and prove the graph rejects it.
3. Calculate latency and availability for serial and parallel variants of `run-with-artifacts`.
4. Run `make network-lab-proof`, terminate Artifact Service through the controlled tour, and observe the gateway response.
5. Confirm that the run remains authoritative while `partial: true` and `artifactsUnavailable` describe the missing enrichment.
6. Run `make dependency-proof` and inspect attempt-count evidence.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build and verify the complete synchronous dependency graph, deadline, retry, and composition policy**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

The graph is acyclic, public depth is at most two, every edge has one deadline/retry owner, and dependency failure never becomes false business data.

## Required evidence

- `capstone/architecture/dependency-graph.yaml`
- `reports/module-04-dependency-proof.json`
- `reports/module-04-partial-response.json`
- `capstone/network-lab/README.md`
- the machine-readable output of `make network-lab-proof`

## Interpretation and defense

1. Which state or effect is authoritative for **Synchronous Collaboration, API Composition, and Dependency Budgets**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove the planted cycle and reset injected unavailability.

## Completion gate

Dependency proof passes and the completed-run response distinguishes unavailable artifacts from zero artifacts.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Synchronous Collaboration, API Composition, and Dependency Budgets**. A green command without the negative case and causal explanation does not satisfy this gate.
