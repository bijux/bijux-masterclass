# Lab — Module 09: Failure-Oriented Verification

## Objective

Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak.

## Setup conditions

The previous baseline is: **Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we prove the service’s guarantees rather than infer them from happy-path unit tests?*

## Failure action and investigation

1. **Create the complete claim-to-proof matrix for all non-compensable gates.**
2. **Implement dependency-light `core-proof` and environment-backed proof groups.**
3. **Build safe disposable PostgreSQL and artifact-root fixtures.**
4. **Add barrier-based idempotency/ETag tests and named worker/outbox process hooks.**
5. **Run every planted defect one at a time and predict the first failing gate before execution.**
6. **Minimize each counterexample and map it to a permanent regression.**
7. **Generate JSON reports and an honest capability matrix.**
8. **Have a reviewer run final proof from a clean extraction using only documented commands.**

### Required planted defect

> Configure final proof to treat missing Docker/PostgreSQL as “unsupported/pass.” The capability audit must reject this false green result.

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

Each planted defect fails the gate that claims to detect it; disabling PostgreSQL or Node changes status to not-executed rather than green.

## Required evidence

- baseline transcript proving the previous checkpoint before **Failure-Oriented Verification** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Choose the narrowest oracle for each claim.
- public, durable, security, or operational observation showing: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **failure-sensitive proof architecture**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Failure-Oriented Verification**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=09`.
4. Confirm the system again provides this result: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.

## Completion gate

- proof matrix complete
- core deterministic
- real dependency evidence
- race oracles strong
- process boundaries controlled
- all defects caught
- capability honesty
- clean-checkout rerun
