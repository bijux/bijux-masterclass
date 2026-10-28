# Lab — Module 02: Domain State and Invariants

> **Module 02:** Domain State and Invariants

## Objective

Implement and exhaustively test project, dataset, and analysis-run behavior as pure state transitions, then translate every failure into the predecessor problem vocabulary.

## Why this lab matters

This lab turns the module’s governing question—**Which state transitions and invariants must remain true regardless of framework or database?**—into a falsifiable experiment. Complete the run state and command matrix before editing provider code. Implement pure transition policy and state-specific field validation in the primary track. Load shared vectors and execute them in both local cores. Add project and dataset invariants needed by later persistence. Build the application failure catalog and one transport translator.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Project operations run through framework-independent use cases while preserving the Course 1 contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *Which rules must remain true regardless of framework, database, worker, or deployment?*

## Hypothesis

The clean implementation should satisfy this claim: **Every state/command pair has one explicit expected outcome; adding a new state or command must make the exhaustive proof fail until classified.** When the lab introduces this fault—**Plant a direct status assignment in the worker path, prove the matrix does not protect callers that bypass policy, then repair and add a source/behavior regression**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Plant a direct status assignment in the worker path, prove the matrix does not protect callers that bypass policy, then repair and add a source/behavior regression**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement and exhaustively test project, dataset, and analysis-run behavior as pure state transitions, then translate every failure into the predecessor problem vocabulary**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Every state/command pair has one explicit expected outcome; adding a new state or command must make the exhaustive proof fail until classified.

## Required evidence

- baseline transcript proving the previous checkpoint before **Domain State and Invariants** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Domain State and Invariants**
- focused result for: Model legal and illegal state transitions.
- public, durable, security, or operational observation showing: The Analysis Runs state machine rejects impossible transitions before any database write.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **domain invariants and canonical values**
- a limitation statement naming every live dependency required to support the strongest **Domain State and Invariants** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Domain State and Invariants**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Plant a direct status assignment in the worker path, prove the matrix does not protect callers that bypass policy, then repair and add a source/behavior regression** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Domain State and Invariants**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Domain State and Invariants** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Domain State and Invariants**. A green command without the negative case and causal explanation does not satisfy this gate.
