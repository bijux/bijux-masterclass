# Lab — Refactor Without Recreating the VPC

## Goal

Move Atlas network resources from a flat root into a versioned module while preserving remote identity, then adopt one unmanaged route and classify one emergency drift.

## Safety boundary

The dependency-light path uses synthetic configuration/state and a deterministic plan model. The optional AWS lane must run against a disposable sandbox VPC or an explicitly approved existing sandbox resource. Do not practice import or state operations on production infrastructure.

## Baseline

Use:

```text
capstone/fixtures/migrations/flat-network-config.json
capstone/fixtures/migrations/flat-network-state.json
capstone/fixtures/migrations/remote-emergency-rule.json
```

## Hypothesis

Explicit moved mappings and a reviewed import can change configuration ownership without replacing the VPC or subnets, while the emergency rule remains visible for an intentional adopt-or-expire decision.

## Controlled action

1. Run the baseline plan and record zero destructive actions.
2. Refactor the network into `module.network` without moved mappings; observe the destroy/create proposal.
3. Add the explicit move map and re-plan.
4. Introduce an unmanaged route and create a declarative import record.
5. Adjust configuration until import no longer proposes accidental route loss.
6. Add the emergency security rule to remote reality.
7. Produce a drift report classifying it as intentional, with incident ID and expiry.
8. Evaluate a provider-normalization fixture and distinguish it from remote mutation.
9. Simulate a state-lineage mismatch and follow the recovery runbook rather than force-pushing.
10. Optional AWS lane: perform the module refactor and import against a disposable VPC and verify resource IDs and packet paths.

## Oracle

The accepted migration:

- preserves VPC and subnet remote IDs;
- contains explicit move history;
- imports the route into exactly one owner;
- does not erase the emergency rule automatically;
- reports provider-only normalization separately;
- refuses a lineage-conflicting state write;
- ends with a data-plane route check.

## Evidence

Retain:

```text
reports/module-09/baseline-plan.json
reports/module-09/unsafe-refactor-plan.json
reports/module-09/move-map.json
reports/module-09/import-plan.json
reports/module-09/drift-report.json
reports/module-09/lineage-recovery.json
reports/module-09/final-route-proof.json
```

For AWS, retain state versions, resource IDs, plan files/digests, CloudTrail events, route evidence, and cleanup record.

## Interpretation

Explain why a zero replacement count is necessary but not sufficient. A refactor can preserve IDs while changing routes, IAM, DNS, or module defaults. Data-plane evidence closes that gap.

## Cleanup

Remove only disposable imported resources created for the lab. Do not delete a pre-existing resource merely because it was imported. Restore or expire the emergency rule according to the fixture decision and verify the final plan.

## Completion gate

Show the before and after addresses, unchanged remote IDs, explicit import ownership, classified drift, and final packet-path evidence.
