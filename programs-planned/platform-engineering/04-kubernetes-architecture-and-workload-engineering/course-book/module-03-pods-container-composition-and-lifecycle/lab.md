# Lab — distinguish restart, replacement, and termination

## Goal

Prove the difference between container restart, Pod replacement, and graceful Pod termination.

## Safety boundary

Use the semantic lifecycle model. The optional kind lane uses only the Atlas probe image in a disposable namespace.

## Baseline

Start one Atlas API Pod with successful init, startup, liveness, and readiness state.

## Hypothesis

A container crash with restart policy Always preserves Pod UID; deleting the Pod causes a controller-owned replacement with a new UID; graceful deletion delivers the termination protocol within thirty seconds.

## Controlled action

1. Crash the application container and observe restart count.
2. Delete the Pod through its controller and observe replacement identity.
3. Configure a process that ignores SIGTERM and repeat deletion.
4. Restore signal handling and repeat.

## Oracle

The first action keeps the Pod UID. The second changes it. The non-cooperative process reaches forced termination; the repaired process records drain and exits before the deadline.

## Evidence

Preserve Pod/container timelines, UIDs, restart counts, owner references, signal events, exit reasons, and grace-budget use.

## Interpretation

Explain which local state survives each transition and why a higher-level controller—not the Pod name—is the durable workload identity.

## Cleanup

Remove the semantic state or disposable namespace after preserving evidence.

## Completion gate

Advance only after you can identify restart versus replacement from machine-readable evidence without relying on object names alone.
