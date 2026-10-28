# Lab — Module 02: Domain State and Invariants

## Objective

Implement and exhaustively test project, dataset, and analysis-run behavior as pure state transitions, then translate every failure into the predecessor problem vocabulary.

## Setup conditions

The previous baseline is: **Project operations run through framework-independent use cases while preserving the Course 1 contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which rules must remain true regardless of framework, database, worker, or deployment?*

## Failure action and investigation

1. **Complete the run state and command matrix before editing provider code.**
2. **Implement pure transition policy and state-specific field validation in the primary track.**
3. **Load shared vectors and execute them in both dependency-light cores.**
4. **Add project and dataset invariants needed by later persistence.**
5. **Build the application failure catalog and one transport translator.**
6. **Run direct tests for legal, illegal, repeated, and boundary commands.**
7. **Plant a direct status assignment in the worker path, prove the matrix does not protect callers that bypass policy, then repair and add a source/behavior regression.**
8. **Write a one-page race analysis for cancellation request versus completion commit.**

### Required planted defect

> Assign `status = completed` directly in one worker path. The repair must make bypass impossible or mechanically detectable, not merely remove this one line.

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

Every state/command pair has one explicit expected outcome; adding a new state or command must make the exhaustive proof fail until classified.

## Required evidence

- baseline transcript proving the previous checkpoint before **Domain State and Invariants** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Model legal and illegal state transitions.
- public, durable, security, or operational observation showing: The Analysis Runs state machine rejects impossible transitions before any database write.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **domain invariants and canonical values**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Domain State and Invariants**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=02`.
4. Confirm the system again provides this result: The Analysis Runs state machine rejects impossible transitions before any database write.

## Completion gate

- transition matrix exhaustive
- terminal states immutable
- progress monotonic
- cancellation semantics explicit
- artifact rule enforced
- stable failure mapping
- shared vectors pass both cores
- bypass defect permanently detected
