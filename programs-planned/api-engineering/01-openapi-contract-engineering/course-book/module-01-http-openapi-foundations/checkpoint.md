# Checkpoint — Module 01: HTTP and OpenAPI Foundations

## Required result

The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.

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

## Defend the design

1. Answer the central question: **How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?**
2. Demonstrate this capstone result: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.—all focused checks pass, the **HTTP and OpenAPI Foundations** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
