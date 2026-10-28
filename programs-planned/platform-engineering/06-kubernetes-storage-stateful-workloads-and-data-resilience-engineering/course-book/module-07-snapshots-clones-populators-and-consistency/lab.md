# Lab 07 — The ready snapshot that cannot recover

## Goal

Distinguish storage readiness from application-consistent recovery.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Write related data and log generations to two volumes and create an uncoordinated snapshot.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Restore the mismatched pair, observe invariant failure, then repeat with quiesce and group coordination.

## Oracle

Only the coordinated copy restores to one recovery generation and passes the application invariant.

## Required evidence

Snapshot records, checkpoint identity, volume generations, restore verification.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Delete temporary copies while retaining one manifest as evidence.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
