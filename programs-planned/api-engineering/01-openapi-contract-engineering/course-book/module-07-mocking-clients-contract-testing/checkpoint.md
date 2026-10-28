# Checkpoint — Module 07: Mocks, Clients, and Contract Testing

Prism is excluded from the installable toolchain because its dependency chain
has unresolved security advisories. Mock/proxy lessons and fixtures remain as
reference material. `make prism-mock` and `make prism-smoke` stop with an explicit
error; `npm run mock` and `npm run proxy:python` are unavailable. Full course
qualification remains blocked until a maintained replacement is qualified.

## Required result

Build the consumer and contract-test ladder against the mock and both real providers.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Mocks, Clients, and Contract Testing** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Mocks, Clients, and Contract Testing**
- focused result for: Distinguish syntax, semantic linting, conformance, and consumer tests.
- public, durable, security, or operational observation showing: Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Mocks, Clients, and Contract Testing**
- a limitation statement naming every live dependency required to support the strongest **Mocks, Clients, and Contract Testing** claim but not exercised

## Defend the design

1. Answer the central question: **How do we turn the contract into a development and verification tool rather than a static document?**
2. Demonstrate this capstone result: Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.
3. Show the **Mocks, Clients, and Contract Testing** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Mock, generated-client, consumer, negative, and stateful checks exercise the same contract.—all focused checks pass, the **Mocks, Clients, and Contract Testing** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
