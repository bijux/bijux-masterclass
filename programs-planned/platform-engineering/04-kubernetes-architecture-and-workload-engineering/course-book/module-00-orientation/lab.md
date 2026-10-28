# Orientation lab — prove the handoff before authoring workload state

## Goal

Create a machine-readable inventory of the Course 3 guarantees that Course 4 must preserve.

## Safety boundary

Do not create or mutate a cluster. This lab reads local artifacts only.

## Baseline

Run `make predecessor-proof`, then inspect every predecessor JSON file.

## Hypothesis

The handoff is sufficient to derive image identity, Pod security context, probes, writable mounts, shutdown budget, and resource hypotheses without consulting build internals.

## Controlled action

Run `python3 capstone/scripts/build_predecessor_inventory.py` and compare its report with the proposed API and worker manifests.

## Oracle

Every inherited field has one manifest expression or one explicit later-course owner. No digest, UID/GID, path class, or health endpoint changes silently.

## Evidence

Preserve `capstone/reports/predecessor-inventory.json` and a discrepancy note.

## Interpretation

A missing expression is a Course 4 defect or a named deferral. “Kubernetes handles it” is not sufficient.

## Cleanup

Run `make clean` to remove generated reports only.

## Completion gate

Advance only when the inventory has zero unexplained contradictions.
