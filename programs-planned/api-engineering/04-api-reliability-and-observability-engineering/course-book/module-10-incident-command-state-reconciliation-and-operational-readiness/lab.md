# Lab — Module 10: Incident Command, Reconciliation, and Readiness

## Objective

Execute a full non-security incident, produce a defensible timeline, run read-only reconciliation, plan idempotent repairs, validate runbooks and alerts, and generate the Course 4 handoff to performance engineering.


## Setup conditions

The previous baseline is: **A stalled-worker game day burns run-start freshness while API availability remains healthy, then recovers without duplicate completion.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *During a real incident, how do people coordinate, determine durable truth, repair safely, and decide that the service is ready again?*

## Failure action and investigation

1. Declare severity and record initial observations separately from hypotheses.
2. Use journey and durable evidence to identify stalled accepted runs.
3. Apply a bounded mitigation without deleting jobs or weakening security.
4. Run read-only reconciliation and generate stable findings/repair keys.
5. Review and execute one idempotent repair in a journaled transaction.
6. Rerun reconciliation and objective calculations.
7. Evaluate reliability-1.0 and the rejected unobservable release.
8. Produce post-incident actions and outgoing Course 4 handoff.

### Required planted defect

Remove or bypass the central control for **Incident Command, Reconciliation, and Readiness** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- Decision log has one command owner and source-linked entries.
- Mitigation reduces impact without duplicate terminal effects.
- Initial reconciliation performs no mutation.
- Repeated repair execution is idempotent.
- Final run, job, event, artifact, checksum, and outbox agree.
- Good release passes and unobservable release fails.

## Required evidence

- baseline transcript proving the previous checkpoint before **Incident Command, Reconciliation, and Readiness** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Assign incident command, operations, communication, and recording roles.
- public, durable, security, or operational observation showing: Course 4 ends with reliability profile 1.0, migration 008, tested runbooks, and an operational handoff to performance engineering.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **incident command and durable reconciliation**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Resolve or remove all synthetic incident data through supported paths.
2. Verify no active faults, held permits, stale leases, or unresolved critical findings.
3. Regenerate manifests and handoff.
4. Archive timeline, reconciliation, repair journal, release proof, and residual risks.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=10` succeeds on the primary track.
