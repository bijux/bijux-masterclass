# Lab 03 — The timeout after a successful attach

## Goal

Prove idempotent csi retries and distinguish controller attachment from node staging and publication.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Create one volume, node, and target path; record empty controller and node state.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Inject a timeout after controllerpublish commits, retry the call, then fail nodestage and recover it.

## Oracle

Retry returns one attachment, no second backend volume appears, and the pod remains unavailable until node publication completes.

## Required evidence

Rpc ledger, volume handle, attachment set, stage and publish states, injected-failure record.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Unpublish, unstage, detach, and delete in safe reverse order.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
