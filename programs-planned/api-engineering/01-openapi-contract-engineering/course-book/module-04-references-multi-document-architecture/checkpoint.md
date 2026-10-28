# Checkpoint — Module 04: References and Multi-Document Architecture

## Required result

The contract becomes a modular source tree with deterministic baseline and frontier bundles.

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

## Defend the design

1. Answer the central question: **How do we split a growing contract without changing its meaning or creating a maze of fragile references?**
2. Demonstrate this capstone result: The contract becomes a modular source tree with deterministic baseline and frontier bundles.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The contract becomes a modular source tree with deterministic baseline and frontier bundles.—all focused checks pass, the **References and Multi-Document Architecture** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
