# Checkpoint — Module 06: Contract-First and Code-First Runtimes

## Required result

Both providers implement the complete contract and pass one provider-neutral behavioral suite.

## Demonstrate

- Keep the canonical contract authoritative.
- Translate framework validation errors into the public problem model.
- Validate responses as well as requests.
- Classify generated-description drift.
- Preserve equivalent observable behavior across FastAPI and Fastify.

## Commands

```bash
make -C capstone core-proof
make -C capstone python-test
make -C capstone typescript
make -C capstone handler-map
make -C capstone python-live
make -C capstone typescript-live
```

## Defend the design

1. Answer the central question: **How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior?**
2. Demonstrate this capstone result: Both providers implement the complete contract and pass one provider-neutral behavioral suite.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Both providers implement the complete contract and pass one provider-neutral behavioral suite.—all focused checks pass, the **Contract-First and Code-First Runtimes** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
