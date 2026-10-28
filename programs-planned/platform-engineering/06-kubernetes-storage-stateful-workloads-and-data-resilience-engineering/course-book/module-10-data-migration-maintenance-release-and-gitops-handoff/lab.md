# Lab 10 — The rollback that cannot cross the data migration

## Goal

Prove that git history is not a universal data rollback mechanism.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Establish old binary, expansion schema, backfill state, new binary, and retained recovery point.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Attempt rollback before and after the contraction boundary and attempt pruning of retained assets.

## Oracle

Pre-contraction rollback is classified by compatibility; post-contraction rollback is blocked; recovery assets resist ordinary pruning.

## Required evidence

Migration ledger, compatibility matrix, release decisions, protected-resource inventory.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Return to the accepted release and verify the course 7 handoff manifest.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
