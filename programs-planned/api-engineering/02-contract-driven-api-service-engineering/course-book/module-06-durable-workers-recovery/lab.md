# Lab — Module 06: Durable Workers and Recovery

## Objective

Submit work, kill the worker after claim or partial progress, recover the expired lease, avoid duplicate artifacts, and resolve cancellation-versus-completion races deterministically.

## Setup conditions

The previous baseline is: **Project, dataset, and run listings are stable, owner-bound, and resistant to cursor tampering.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *What internal machinery makes `202 Accepted` honest after API or worker processes die?*

## Failure action and investigation

1. **Implement job claim SQL and document lock, order, and lease predicates.**
2. **Run API with workers stopped; submit and verify durable queued state after restart.**
3. **Run multiple workers and verify distinct claims.**
4. **Implement heartbeats, retry classification, attempt cap, and exponential delay.**
5. **Implement generation-guarded progress and terminal transactions.**
6. **Kill a worker after claim and after partial progress, then recover after expiry.**
7. **Exercise cancellation-before-completion and completion-before-cancellation races.**
8. **Plant a terminal update by run ID only; prove a stale worker overwrites, repair with generation fencing, and retain the process test.**

### Required planted defect

> Remove lease generation from terminal UPDATE and release a paused old worker after a recovered worker completes.

Preserve the following evidence:

```text
prediction:
change introduced:
minimal setup:
first failing command:
public symptom:
durable/process state:
root cause:
repair:
regression path:
remaining limitation:
```

## Operational oracle

After a worker is killed, no terminal effect occurs before lease expiry; a new generation completes once, and the stale generation cannot overwrite it.

## Required evidence

- baseline transcript proving the previous checkpoint before **Durable Workers and Recovery** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Separate durable acceptance from execution.
- public, durable, security, or operational observation showing: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **durable job leasing and fencing**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Durable Workers and Recovery**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=06`.
4. Confirm the system again provides this result: Analysis work survives restart, abandoned leases are recovered, and stale workers cannot overwrite newer results.

## Completion gate

- durable 202
- atomic claim
- lease recovery
- generation fencing
- short transactions
- idempotent effects
- bounded retry
- safe shutdown
