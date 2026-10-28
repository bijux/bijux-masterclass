# Lab 05 — The stale primary that returns

## Goal

Demonstrate why statefulset identity and volume attachment are not sufficient writer fences.

## Safety boundary

Run only in the course workspace or an explicitly disposable cluster and storage account. Do not force detach, delete retained volumes, modify snapshot classes, or restore over an authoritative environment. Record the target context before every destructive command.

## Baseline

Start ordinal zero with generation one and commit a sentinel record.

## Hypothesis

The module’s governing invariant should predict the result before the failure is injected. Write that prediction and the first object or record expected to diverge.

## Controlled action

Issue generation two to a replacement, then let the old process attempt another write.

## Oracle

The stale generation is rejected even if it can reach storage; the replacement preserves the sentinel and advances the ledger.

## Required evidence

Fence ledger, writer identities, accepted and rejected mutations, readiness transitions.

## Interpretation

Explain why the observed result supports or falsifies the hypothesis. Separate Kubernetes object state, controller state, backend state, filesystem state, and application state. Record any evidence class that remained unavailable.

## Cleanup

Stop both simulated writers and leave one authoritative generation.

## Completion gate

The lab is complete only when the failure is reproduced, the earliest missing transition is identified, the unsafe intervention is rejected, cleanup is verified, and the evidence artifact can be reviewed without relying on terminal history.
