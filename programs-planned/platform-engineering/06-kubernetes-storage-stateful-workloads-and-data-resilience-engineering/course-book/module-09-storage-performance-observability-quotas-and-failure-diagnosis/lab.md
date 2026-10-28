# Lab 09 — The latency incident that scaling cannot fix

## Goal

Separate application, filesystem, csi control-plane, and backend saturation signals.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Run a defined random-write/fsync workload and capture latency, queue depth, throughput, and capacity.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Increase snapshot delta pressure and concurrency, then apply one justified service-tier change.

## Oracle

The evidence locates the bottleneck and the candidate improves the declared workload without weakening correctness gates.

## Required evidence

Before-after workload identity, histograms, queue data, capacity state, release decision.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Restore original service tier and delete benchmark data.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
