# Lab — Module 08: Abuse Resistance and Resource Budgets

## Objective

Apply operation-specific budgets to run submission, uploads, event streams, artifact reads, and webhook registration. Simulate time deterministically, test cancellation, and plant a permit leak plus global-only limiter; prove starvation/leak before repair.


## Setup conditions

The previous baseline is: **Secrets become non-rendering values, audit records are privacy-bounded, and key rotation is testable.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does the API keep expensive operations bounded when valid-looking clients consume resources aggressively?*

## Failure action and investigation

1. Implement and test: Choose rate-limit dimensions from abuse paths.
2. Implement and test: Implement deterministic token-bucket behavior.
3. Implement and test: Limit simultaneous expensive work with leak-free permits.
4. Implement and test: Bound uploads, streams, queue depth, and storage.
5. Implement and test: Return coherent `429` or `503` outcomes without amplifying retries.

### Required planted defect

Remove or bypass the central control for **Abuse Resistance and Resource Budgets** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: How does the API keep expensive operations bounded when valid-looking clients consume resources aggressively? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Abuse Resistance and Resource Budgets** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Choose rate-limit dimensions from abuse paths.
- public, durable, security, or operational observation showing: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **resource budgets and abuse admission**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Abuse Resistance and Resource Budgets**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=08`.
4. Confirm the system again provides this result: Analysis submission, upload, streaming, and webhook registration have explicit resource budgets.

## Completion gate

- cost-aware budget keys
- deterministic token bucket
- exception-safe concurrency permits
- upload/stream budgets
- tenant plus global admission
- bounded queue/storage quota
- coherent 429/503
- scope claim for single/multi-process
