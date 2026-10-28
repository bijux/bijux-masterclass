# Lab — Route around failure without moving the domain into the gateway

**Module:** Discovery, Routing, Gateways, and Traffic Topology

## Objective

Implement health- and version-aware discovery, bounded canary routing, and a thin public edge.

## Setup

Load the dependency graph, lifecycle policies, service versions, and gateway responsibility ADR.

## Controlled actions

1. Register two Control instances and remove one from eligibility during drain.
2. Route only to versions supported by the caller matrix.
3. Shadow artifact reads and compare exact semantic results while returning legacy authority.
4. Canary a stable resource-key fraction and inject candidate failure.
5. Run `make routing-proof` and prove rollback occurs without gateway domain logic.

## Correctness oracle

Only healthy accepting compatible instances receive traffic; retries have one owner; shadow has no uncontrolled effects; gateway owns no business state.

## Required evidence

- `capstone/architecture/dependency-graph.yaml`
- `reports/module-07-routing-proof.json`
- `capstone/architecture/adr/0006-gateway-owns-no-business-state.md`

## Cleanup

Restore instance health, route phase, and canary fraction.

## Completion gate

Routing proof passes and a failed canary rolls back to a compatible authoritative path.

A successful command without the required evidence does not complete the lab.
