# Checkpoint — Module 07: Mocks, Clients, and Contract Testing

## Required result

Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.

## Demonstrate

- Distinguish syntax, semantic linting, conformance, and consumer tests.
- Develop consumers against a mock without mistaking examples for complete behavior.
- Generate and review clients in Python and TypeScript.
- Use generated and property-based tests to explore boundaries.
- Record tool capability limits instead of hiding them.

## Commands

```bash
make -C capstone lint-contract
make -C capstone bundle-check
make -C capstone prism-smoke
make -C capstone clients-generate
make -C capstone clients-test
make -C capstone schemathesis
make -C capstone confirm
```

## Defend the design

1. Answer the central question: **How do we turn the contract into a development and verification tool rather than a static document?**
2. Demonstrate this capstone result: Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.—all focused checks pass, the **Mocks, Clients, and Contract Testing** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
