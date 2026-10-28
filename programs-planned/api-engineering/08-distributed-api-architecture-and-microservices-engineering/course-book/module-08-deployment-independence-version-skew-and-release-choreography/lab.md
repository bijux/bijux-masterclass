# Lab — Release one service while the rest of the platform keeps running

**Module:** Deployment Independence, Version Skew, and Release Choreography

## Objective

Prove a mixed-version rollout, data expansion, canary, rollback, and retirement sequence.

## Setup

Load the version ledger, release policy, service migration heads, and accepted/rejected candidate fixtures.

## Controlled actions

1. Run all supported consumer/provider version pairs.
2. Add an optional Artifact Service field through expand-and-contract migration.
3. Shadow and canary Artifact 1.1 while Gateway and Control remain mixed 1.0/1.1.
4. Rollback the route after injecting candidate divergence.
5. Remove the old writer and contract only after the coexistence window passes.

## Correctness oracle

Every supported pair preserves existing outcomes; unsupported major skew is rejected; rollback reads all committed data; no other service writes Artifact schema.

## Required evidence

- `capstone/architecture/release-policy.yaml`
- `capstone/architecture/version-ledger.yaml`
- `reports/module-08-release-proof.json`

## Cleanup

Restore service versions, route weights, and migration fixtures.

## Completion gate

Release proof passes accepted skew and rejects all incompatible candidates with exact reasons.

A successful command without the required evidence does not complete the lab.
