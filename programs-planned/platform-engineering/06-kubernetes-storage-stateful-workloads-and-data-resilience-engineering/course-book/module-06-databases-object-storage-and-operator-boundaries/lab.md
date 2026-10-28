# Lab 06 — The operator no team actually owns

## Goal

Expose missing operational responsibilities in an apparently complete database deployment.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Review the atlas data-service catalogue and a candidate in-cluster database contract.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Inject an engine upgrade, expired credential, lagging replica, and failed restore ownership question.

## Oracle

The responsibility matrix identifies an accountable owner or rejects the service capability.

## Required evidence

Raci-style responsibility map, decision record, unresolved-risk list, managed-versus-operator comparison.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Revert fixture decisions and preserve the review record.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
