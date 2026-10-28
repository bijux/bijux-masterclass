# Lab — Module 04: Lifecycle, Health, Shutdown, and Recovery

## Objective

Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence.


## Setup conditions

The previous baseline is: **PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does a process start, accept work, drain, stop, and recover without lying to orchestrators or losing durable work?*

## Failure action and investigation

1. Send the termination transition and verify readiness becomes false before work is awaited.
2. Attempt a new request and job claim; both must be rejected.
3. Complete one in-flight request and deliberately stall the SSE stream.
4. Expire the stream sub-budget and preserve durable run state.
5. Terminate a worker before completion, advance the lease clock, and recover with another worker.
6. Make telemetry flush fail and prove shutdown still completes.
7. Restart and run reconciliation against durable state.

### Required planted defect

Remove or bypass the central control for **Lifecycle, Health, Shutdown, and Recovery** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- No new admission occurs after drain begins.
- Acknowledged responses correspond to committed state.
- A stale worker cannot complete after takeover.
- Telemetry failure changes only diagnostic evidence.
- Restart produces no lost accepted run and no duplicate terminal artifact.

## Required evidence

- baseline transcript proving the previous checkpoint before **Lifecycle, Health, Shutdown, and Recovery** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Separate startup, liveness, and readiness.
- public, durable, security, or operational observation showing: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **explicit lifecycle and health**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Release all manual-clock resources.
2. Clear injected lifecycle faults.
3. Verify zero held bulkhead permits and no temporary files.
4. Retain transition and reconciliation reports.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=04` succeeds on the primary track.
