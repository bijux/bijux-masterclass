# Lab — Module 02: Deadlines, Cancellation, and Retry Budgets

## Objective

Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency.


## Setup conditions

The previous baseline is: **The service gains a reliability case for create, submit, start, complete, retrieve, and notify journeys.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does one request carry a finite time budget through dependencies without multiplying work or reporting success too late?*

## Failure action and investigation

1. Implement absolute propagation.
2. Classify GET, idempotent update, idempotency-key POST, and unsafe POST.
3. Apply full jitter and Retry-After floor.
4. Plant a loop resetting timeout per attempt.
5. Plant a second retry owner and measure amplification.
6. Repair both and simulate disconnect after durable acceptance.

### Required planted defect

Remove or bypass the central control for **Deadlines, Cancellation, and Retry Budgets** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

- No child exceeds parent expiry.
- Unsafe POST gets one attempt.
- Delay plus minimum attempt fits remaining time.
- Attempt count matches named owner policy.
- Committed work survives disconnect.

## Required evidence

- baseline transcript proving the previous checkpoint before **Deadlines, Cancellation, and Retry Budgets** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Distinguish absolute deadlines from per-call timeouts.
- public, durable, security, or operational observation showing: Ingress requests, database calls, artifact operations, and webhooks share finite budgets without retry amplification.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **absolute deadline propagation**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Reset fault injector.
2. Clear deterministic attempt records.
3. Retain before/after amplification report.

## Completion gate

The lab is complete only when every listed oracle passes after repair, cleanup restores the stated steady state, and `make module-proof MODULE=02` succeeds on the primary track.
