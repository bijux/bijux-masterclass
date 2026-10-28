# Lab — Module 01: HTTP and OpenAPI Foundations

## Objective

Build the first four operations from raw HTTP messages, then plant an undocumented success status in one provider and prove the shared evidence catches it.

## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?*

## Failure action and investigation

1. Write request/response transcripts for health, project listing, project creation, and project retrieval before editing YAML.
2. Create or repair the root OpenAPI Object, servers, Paths Objects, four Operation Objects, and minimal response schemas.
3. Run `make -C capstone parse`, `refs`, `bundle-check`, and `operations`; inspect the ledger rather than only command exit codes.
4. Implement the operations in FastAPI with explicit operation IDs, response models, statuses, and creation headers.
5. Implement the same operations in Fastify with runtime schemas and response serialization.
6. Add positive and negative tests in each provider and one provider-neutral scenario.
7. Temporarily change one provider to return `200` for project creation. Record the failing assertion, repair it, and retain the regression test.

### Required planted defect

Choose one defect from Failure Modes. Before fixing it, keep:

```text
defect:
predicted first failing gate:
actual first failing gate:
minimal request/instance/diff:
root cause:
repair:
permanent regression location:
```

## Operational oracle

The system satisfies the chapter’s central question: How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **HTTP and OpenAPI Foundations** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Read requests and responses as protocol messages.
- public, durable, security, or operational observation showing: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **HTTP and OpenAPI Foundations**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **HTTP and OpenAPI Foundations**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=01`.
4. Confirm the system again provides this result: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.

## Completion gate

- four introductory operations have unique stable IDs
- project creation is `201` with `Location` and JSON
- the path parameter is explicitly required
- health is explicitly anonymous
- both providers pass equivalent positive and negative cases
- the planted status defect is detected
