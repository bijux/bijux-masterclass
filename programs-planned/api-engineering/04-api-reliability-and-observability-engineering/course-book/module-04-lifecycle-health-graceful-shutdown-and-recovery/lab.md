# Lab — Module 04: Lifecycle, Health, Shutdown, and Recovery

> **Module 04:** Lifecycle, Health, Shutdown, and Recovery

## Objective

Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence.

## Why this lab matters

This lab turns the module’s governing question—**How do APIs, workers, and dispatchers start, become ready, drain, stop, and recover without losing accepted work?**—into a falsifiable experiment. Apply Lifecycle state machine, Startup gate, Liveness to this module’s capstone increment: Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence. State one misleading green signal and the durable observation that would overrule it.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **PostgreSQL, artifact storage, webhook delivery, and telemetry export each receive a justified resilience policy.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does a process start, accept work, drain, stop, and recover without lying to orchestrators or losing durable work?*

## Hypothesis

The clean implementation should satisfy this claim: **No new admission occurs after drain begins; Acknowledged responses correspond to committed state; A stale worker cannot complete after takeover; Telemetry failure changes only diagnostic evidence; Restart produces no lost accepted run and no duplicate terminal artifact.** When the lab introduces this fault—**Remove or bypass the central control for Lifecycle, Health, Shutdown, and Recovery in a temporary branch**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Send the termination transition and verify readiness becomes false before work is awaited.
2. Attempt a new request and job claim; both must be rejected.
3. Complete one in-flight request and deliberately stall the SSE stream.
4. Expire the stream sub-budget and preserve durable run state.
5. Terminate a worker before completion, advance the lease clock, and recover with another worker.
6. Make telemetry flush fail and prove shutdown still completes.
7. Restart and run reconciliation against durable state.

### Required planted defect

Remove or bypass the central control for **Lifecycle, Health, Shutdown, and Recovery** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control for Lifecycle, Health, Shutdown, and Recovery in a temporary branch**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- No new admission occurs after drain begins.
- Acknowledged responses correspond to committed state.
- A stale worker cannot complete after takeover.
- Telemetry failure changes only diagnostic evidence.
- Restart produces no lost accepted run and no duplicate terminal artifact.

## Required evidence

- baseline transcript proving the previous checkpoint before **Lifecycle, Health, Shutdown, and Recovery** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Lifecycle, Health, Shutdown, and Recovery**
- focused result for: Separate startup, liveness, and readiness.
- public, durable, security, or operational observation showing: API, worker, and dispatcher processes expose explicit startup, accepting, draining, stopping, and recovery behavior.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **explicit lifecycle and health**
- a limitation statement naming every live dependency required to support the strongest **Lifecycle, Health, Shutdown, and Recovery** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Lifecycle, Health, Shutdown, and Recovery**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control for Lifecycle, Health, Shutdown, and Recovery in a temporary branch** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Release all manual-clock resources.
2. Clear injected lifecycle faults.
3. Verify zero held bulkhead permits and no temporary files.
4. Retain transition and reconciliation reports.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=04` succeeds on the primary track.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Lifecycle, Health, Shutdown, and Recovery**. A green command without the negative case and causal explanation does not satisfy this gate.
