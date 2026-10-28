# Lab — Complete a run across services without a global transaction

**Module:** Distributed Workflows, Sagas, Compensation, and Process Managers

## Objective

Implement and falsify the artifact publication and run completion saga.

## Setup

Load the saga catalogue, capability profile, current lease vectors, and artifact service reference.

## Controlled actions

1. Execute the happy path with stable saga, event, command, and effect identities.
2. Inject timeout after artifact commit and prove retry returns the existing artifact.
3. Advance the lease generation before completion and require compensation.
4. Replay duplicate ArtifactStored and CompleteRun messages.
5. Run `make saga-proof` and reconcile all final authority states.

## Correctness oracle

Happy and duplicate schedules complete once; stale attempts cannot complete; compensation is idempotent; no ambiguous effect remains unexplained.

## Required evidence

- `capstone/architecture/saga-catalog.yaml`
- `reports/module-05-saga-proof.json`
- `reports/module-05-reconciliation.json`

## Cleanup

Reset saga stores, artifacts, runs, and injected fault schedules.

## Completion gate

Saga proof passes every shared schedule and reconciliation has zero unexplained findings.

A successful command without the required evidence does not complete the lab.
