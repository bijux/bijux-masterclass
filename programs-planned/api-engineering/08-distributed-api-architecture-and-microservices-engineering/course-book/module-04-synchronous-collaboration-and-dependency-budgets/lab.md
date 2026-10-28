# Lab — Break the synchronous cycle before it reaches production

**Module:** Synchronous Collaboration, API Composition, and Dependency Budgets

## Objective

Build and verify the complete synchronous dependency graph, deadline, retry, and composition policy.

## Setup

Load service catalogue, public critical journeys, gRPC methods, and proposed gateway routes.

## Controlled actions

1. Draw every synchronous edge and mark caller, callee, purpose, deadline owner, retry owner, and fallback.
2. Introduce a Control↔Artifact cycle and prove the graph rejects it.
3. Calculate latency and availability for serial and parallel variants of `run-with-artifacts`.
4. Run `make network-lab-proof`, terminate Artifact Service through the controlled tour, and observe the gateway response.
5. Confirm that the run remains authoritative while `partial: true` and `artifactsUnavailable` describe the missing enrichment.
6. Run `make dependency-proof` and inspect attempt-count evidence.

## Correctness oracle

The graph is acyclic, public depth is at most two, every edge has one deadline/retry owner, and dependency failure never becomes false business data.

## Required evidence

- `capstone/architecture/dependency-graph.yaml`
- `reports/module-04-dependency-proof.json`
- `reports/module-04-partial-response.json`
- `capstone/network-lab/README.md`
- the machine-readable output of `make network-lab-proof`

## Cleanup

Remove the planted cycle and reset injected unavailability.

## Completion gate

Dependency proof passes and the completed-run response distinguishes unavailable artifacts from zero artifacts.

A successful command without the required evidence does not complete the lab.
