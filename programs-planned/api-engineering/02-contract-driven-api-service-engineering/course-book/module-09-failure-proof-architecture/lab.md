# Lab — Module 09: Failure-Oriented Verification

> **Module 09:** Failure-Oriented Verification

## Objective

Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak.

## Why this lab matters

This lab turns the module’s governing question—**How do tests prove transactions, concurrency, restart, storage, and delivery guarantees rather than only happy paths?**—into a falsifiable experiment. The Failure-Oriented Verification increment must preserve the frozen API and every earlier durability invariant while delivering this result: Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

It advances the cumulative Analysis Runs Platform by requiring this result: **Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Run completion and webhook intent cannot diverge; duplicate delivery is detectable and safe.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we prove the service’s guarantees rather than infer them from happy-path unit tests?*

## Hypothesis

The clean implementation should satisfy this claim: **Each planted defect fails the gate that claims to detect it; disabling PostgreSQL or Node changes status to not-executed rather than green.** When the lab introduces this fault—**Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Each planted defect fails the gate that claims to detect it; disabling PostgreSQL or Node changes status to not-executed rather than green.

## Required evidence

- baseline transcript proving the previous checkpoint before **Failure-Oriented Verification** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Failure-Oriented Verification**
- focused result for: Choose the narrowest oracle for each claim.
- public, durable, security, or operational observation showing: A single proof command exposes missing transactions, stale-worker writes, unstable cursors, unbounded uploads, and lost outbox intent.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **failure-sensitive proof architecture**
- a limitation statement naming every live dependency required to support the strongest **Failure-Oriented Verification** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Failure-Oriented Verification**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Assemble a proof runner that detects every planted defect: broken transaction, unstable cursor, lost replay, stale update, worker overwrite, unbounded upload, unsigned webhook, and cross-owner leak** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Failure-Oriented Verification**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Failure-Oriented Verification** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Failure-Oriented Verification**. A green command without the negative case and causal explanation does not satisfy this gate.
