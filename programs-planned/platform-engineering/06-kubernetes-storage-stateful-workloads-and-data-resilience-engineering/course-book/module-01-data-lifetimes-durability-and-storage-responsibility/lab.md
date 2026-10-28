# Lab 01 — The disposable directory presented as durable state

## Goal

Prove that identical application behavior can cross container and pod lifetimes while data survival changes.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Run the atlas writer against container-local, pod-scoped, and persistent directories and record identities and checksums.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Replace the process, then replace the pod-equivalent directory owner, then simulate node loss by removing the local backing root.

## Oracle

Only data assigned to a lifetime larger than the failed boundary remains; the catalogue predicts every outcome.

## Required evidence

Data-classification.json, before-after checksums, process and directory identities, failure-domain explanation.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Remove all temporary roots and verify no background process remains.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
