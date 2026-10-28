# Lab 08 — The green backup with no empty-destination proof

## Goal

Turn backup completion into measured recoverability.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Create a backup manifest and record the current transaction generation.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Remove the original state root, restore into a new empty location, withhold one required object, then repair and repeat.

## Oracle

The incomplete restore fails closed; the repaired restore verifies digests, schema, sentinel data, rpo, and elapsed phases.

## Required evidence

Manifest, missing-object failure, restored inventory, rpo/rto report, domain verification.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Remove restored test environments but retain the immutable report.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
