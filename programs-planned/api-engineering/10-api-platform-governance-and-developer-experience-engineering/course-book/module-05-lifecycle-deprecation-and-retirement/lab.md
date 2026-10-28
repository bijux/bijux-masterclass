# Lab 05 — Attempt an unsafe retirement

## Setup

Run `make lifecycle-proof`. Inspect the consumer inventory, lifecycle policy, and
Analysis HTTP 1.1 deprecation record.

## Controlled action

Attempt retirement with the current consumer state. Then mark the legacy CLI as
migration-complete and rerun impact analysis. Finally, remove the consumer record
instead of completing migration and compare the evidence quality.

## Oracle

Current retirement is blocked. Verified migration can make it eligible. Deleting
the consumer record is not evidence of migration and must be detected as an
inventory-integrity problem.

## Required evidence

Create `reports/module-05-retirement.json` with affected consumers, evidence
sources, notice status, runtime plan, decision, and residual uncertainty.

## Cleanup

Restore the original inventory and rerun lifecycle proof.

## Completion gate

Retirement cannot advance while a blocking consumer or unresolved inventory gap
remains.
