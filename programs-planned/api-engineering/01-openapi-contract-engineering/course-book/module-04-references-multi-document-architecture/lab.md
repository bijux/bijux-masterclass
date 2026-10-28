# Lab — Module 04: References and Multi-Document Architecture

## Objective

Convert a monolithic contract into a multi-document source, relocate it, bundle it twice, and prove the publication artifact preserves operations, schemas, and examples.

## Setup conditions

The previous baseline is: **Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we split a growing contract without changing its meaning or creating a maze of fragile references?*

## Failure action and investigation

1. Inventory every candidate component and record why it deserves extraction: reuse, ownership, or conceptual identity.
2. Split path groups and component categories while tracing the base URI of every nested reference.
3. Run `make -C capstone refs` from the program root, capstone directory, and an unrelated working directory.
4. Copy the source tree to a temporary path and repeat resolution with network unavailable.
5. Run `bundle`, `bundle-check`, `operations`, and `examples`; inspect the digest and ledgers.
6. Introduce a wrong nested relative path and record the full diagnostic chain.
7. Repair the path and remove one needless reference hop found during review.

### Required planted defect

Choose one defect from Failure Modes. Before fixing it, keep:

```text
defect:
predicted first failing gate:
actual first failing gate:
minimal request/instance/diff:
root cause:
repair:
permanent regression location:
```

## Operational oracle

The system satisfies the chapter’s central question: How do we split a growing contract without changing its meaning or creating a maze of fragile references? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **References and Multi-Document Architecture** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Resolve relative references from the correct document base.
- public, durable, security, or operational observation showing: The contract becomes a modular source tree with deterministic baseline and frontier bundles.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **References and Multi-Document Architecture**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **References and Multi-Document Architecture**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=04`.
4. Confirm the system again provides this result: The contract becomes a modular source tree with deterministic baseline and frontier bundles.

## Completion gate

- all references resolve offline
- nested references use the correct document base
- two bundles are deterministic
- source and bundle operation ledgers match
- examples still validate after bundling
- no duplicate canonical schema remains
