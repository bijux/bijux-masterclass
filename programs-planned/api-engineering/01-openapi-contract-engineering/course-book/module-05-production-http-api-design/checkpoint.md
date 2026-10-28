# Checkpoint — Module 05: Production HTTP API Design

## Required result

The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.

## Demonstrate

- Use `202 Accepted` with a status resource.
- Define idempotency-key behavior precisely.
- Use ETags and preconditions for optimistic concurrency.
- Design stable pagination and lifecycle-aware errors.
- Use RFC 9457 Problem Details as a public error vocabulary.

## Commands

```bash
make -C capstone python-test
make -C capstone typescript
make -C capstone python-live
make -C capstone typescript-live
make -C capstone releases
```

## Defend the design

1. Answer the central question: **How should an API express asynchronous work, retries, conflicts, pagination, and conditional mutation honestly?**
2. Demonstrate this capstone result: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.—all focused checks pass, the **Production HTTP API Design** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
