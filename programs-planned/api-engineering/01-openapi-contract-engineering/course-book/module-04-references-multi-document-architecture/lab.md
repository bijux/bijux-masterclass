# Lab — Module 04: References and Multi-Document Architecture

> **Module 04:** References and Multi-Document Architecture

## Objective

Convert a monolithic contract into a multi-document source, relocate it, bundle it twice, and prove the publication artifact preserves operations, schemas, and examples.

## Why this lab matters

This lab turns the module’s governing question—**How can a multi-document contract remain understandable, relocatable, and deterministically buildable?**—into a falsifiable experiment. For every References and Multi-Document Architecture claim above, add one citation in personal notes and one counterexample. Mark the cheapest route that can falsify it—parse, examples, provider tests, live conformance, compatibility diff, or manual review—and combine routes where the claim crosses layers.

It advances the cumulative Analysis Runs Platform by requiring this result: **Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **Dataset sources, analysis parameters, artifacts, and Problem Details become precise schemas with boundary fixtures.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we split a growing contract without changing its meaning or creating a maze of fragile references?*

## Hypothesis

The clean implementation should satisfy this claim: **all references resolve offline; nested references use the correct document base; two bundles are deterministic; source and bundle operation ledgers match; examples still validate after bundling; no duplicate canonical schema remains.** When the lab introduces this fault—**Repair the path and remove one needless reference hop found during review**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Repair the path and remove one needless reference hop found during review**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Convert a monolithic contract into a multi-document source, relocate it, bundle it twice, and prove the publication artifact preserves operations, schemas, and examples**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- all references resolve offline
- nested references use the correct document base
- two bundles are deterministic
- source and bundle operation ledgers match
- examples still validate after bundling
- no duplicate canonical schema remains

## Required evidence

- baseline transcript proving the previous checkpoint before **References and Multi-Document Architecture** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **References and Multi-Document Architecture**
- focused result for: Resolve relative references from the correct document base.
- public, durable, security, or operational observation showing: The contract becomes a modular source tree with deterministic baseline and frontier bundles.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **References and Multi-Document Architecture**
- a limitation statement naming every live dependency required to support the strongest **References and Multi-Document Architecture** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **References and Multi-Document Architecture**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Repair the path and remove one needless reference hop found during review** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **References and Multi-Document Architecture**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **References and Multi-Document Architecture** experiment.
3. Rerun the focused regression and `make module-proof MODULE=04`.
4. Confirm the system again provides this result: The contract becomes a modular source tree with deterministic baseline and frontier bundles.

## Completion gate

- all references resolve offline
- nested references use the correct document base
- two bundles are deterministic
- source and bundle operation ledgers match
- examples still validate after bundling
- no duplicate canonical schema remains

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **References and Multi-Document Architecture**. A green command without the negative case and causal explanation does not satisfy this gate.
