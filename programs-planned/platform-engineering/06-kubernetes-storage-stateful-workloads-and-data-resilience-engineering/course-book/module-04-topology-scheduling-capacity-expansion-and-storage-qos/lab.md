# Lab 04 — The multi-volume Pod that strands itself

## Goal

Show how stale capacity and partial provisioning can pin a pod to an unusable topology.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Define two claims, asymmetric zone capacity, and nodes with attach limits.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Schedule with stale capacity, provision the first claim, fail the second, then recover through capacity correction and a clean retry.

## Oracle

The system explains the stranded state and refuses silent cross-zone rebinding.

## Required evidence

Capacity snapshots, selected-node annotations, provision attempts, attach-slot accounting.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Release test volumes and restore initial capacity catalogue.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
