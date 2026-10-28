# Lab — Build the service catalogue and remove fake autonomy

**Module:** Service Boundaries, Bounded Contexts, and Contract Ownership

## Objective

Define capability, contract, state, data, and operational ownership for every component.

## Setup

Load the approved boundary scorecard and inherited HTTP, event, and RPC catalogues.

## Controlled actions

1. Classify each component as business service, edge component, compute plane, platform component, or analytical consumer.
2. Assign one contract owner and one state authority to every inherited and new interface.
3. Create anti-corruption mappings for artifact and notification models.
4. Find and remove shared domain policies that would couple services.
5. Run `make ownership-proof` and review every single-writer assertion.

## Correctness oracle

Every business fact has one canonical writer, every interface has one owner, and no table-shaped service or shared domain policy survives.

## Required evidence

- `capstone/architecture/service-catalog.yaml`
- `capstone/architecture/data-ownership.yaml`
- `reports/module-02-ownership-proof.json`

## Cleanup

Remove experimental catalogue entries and restore canonical ownership.

## Completion gate

Ownership proof passes and you can explain why Worker Plane and Gateway are not business-state owners.

A successful command without the required evidence does not complete the lab.
