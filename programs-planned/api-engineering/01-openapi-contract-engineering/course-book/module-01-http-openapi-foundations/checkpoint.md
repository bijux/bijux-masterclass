# Checkpoint — Module 01: HTTP and OpenAPI Foundations

## Required result

Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior.

## Demonstrate

- Read requests and responses as protocol messages.
- Separate API behavior, OpenAPI description, implementation, and documentation rendering.
- Choose methods and status codes from HTTP semantics.
- Write a minimal valid OpenAPI description.
- Prove that the two reference providers expose the same public behavior.

## Commands

```bash
make -C capstone parse
make -C capstone refs
make -C capstone operations
make -C capstone handler-map
make -C capstone python-test
make -C capstone typescript
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **HTTP and OpenAPI Foundations** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **HTTP and OpenAPI Foundations**
- focused result for: Read requests and responses as protocol messages.
- public, durable, security, or operational observation showing: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **HTTP and OpenAPI Foundations**
- a limitation statement naming every live dependency required to support the strongest **HTTP and OpenAPI Foundations** claim but not exercised

## Defend the design

1. Answer the central question: **How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?**
2. Demonstrate this capstone result: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.
3. Show the **HTTP and OpenAPI Foundations** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.—all focused checks pass, the **HTTP and OpenAPI Foundations** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
