# Checkpoint — Module 05: Production HTTP API Design

## Required result

Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details.

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

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Production HTTP API Design** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Production HTTP API Design**
- focused result for: Use `202 Accepted` with a status resource.
- public, durable, security, or operational observation showing: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Production HTTP API Design**
- a limitation statement naming every live dependency required to support the strongest **Production HTTP API Design** claim but not exercised

## Defend the design

1. Answer the central question: **How should an API express asynchronous work, retries, conflicts, pagination, and conditional mutation honestly?**
2. Demonstrate this capstone result: The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.
3. Show the **Production HTTP API Design** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—The API can submit, monitor, cancel, and retrieve analysis runs and artifacts with explicit lifecycle semantics.—all focused checks pass, the **Production HTTP API Design** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
