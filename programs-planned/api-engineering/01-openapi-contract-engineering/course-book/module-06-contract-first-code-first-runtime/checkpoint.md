# Checkpoint — Module 06: Contract-First and Code-First Runtimes

## Required result

Map every operation to both providers and compare generated observations with the canonical contract.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Contract-First and Code-First Runtimes** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Contract-First and Code-First Runtimes**
- focused result for: Keep the canonical contract authoritative.
- public, durable, security, or operational observation showing: Both providers implement the complete contract and pass one provider-neutral behavioral suite.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Contract-First and Code-First Runtimes**
- a limitation statement naming every live dependency required to support the strongest **Contract-First and Code-First Runtimes** claim but not exercised

## Defend the design

1. Answer the central question: **How do we implement one contract in two frameworks without letting framework defaults become accidental public behavior?**
2. Demonstrate this capstone result: Both providers implement the complete contract and pass one provider-neutral behavioral suite.
3. Show the **Contract-First and Code-First Runtimes** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Both providers implement the complete contract and pass one provider-neutral behavioral suite.—all focused checks pass, the **Contract-First and Code-First Runtimes** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
