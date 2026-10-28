# Checkpoint — Module 04: References and Multi-Document Architecture

## Required result

Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles.

## Demonstrate

- Resolve relative references from the correct document base.
- Use components where identity or reuse justifies them.
- Distinguish schema recursion from file-reference cycles.
- Bundle deterministically and work offline.
- Relocate the source tree without breaking resolution.

## Commands

```bash
make -C capstone refs
make -C capstone bundle
make -C capstone bundle-check
make -C capstone operations
make -C capstone examples
make -C capstone core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **References and Multi-Document Architecture** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **References and Multi-Document Architecture**
- focused result for: Resolve relative references from the correct document base.
- public, durable, security, or operational observation showing: The contract becomes a modular source tree with deterministic baseline and frontier bundles.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **References and Multi-Document Architecture**
- a limitation statement naming every live dependency required to support the strongest **References and Multi-Document Architecture** claim but not exercised

## Defend the design

1. Answer the central question: **How do we split a growing contract without changing its meaning or creating a maze of fragile references?**
2. Demonstrate this capstone result: The contract becomes a modular source tree with deterministic baseline and frontier bundles.
3. Show the **References and Multi-Document Architecture** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The contract becomes a modular source tree with deterministic baseline and frontier bundles.—all focused checks pass, the **References and Multi-Document Architecture** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
