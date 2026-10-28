# Lab — Module 10: OpenAPI 3.2, Streaming, Webhooks, and Workflows

## Objective

Publish and defend the 3.2 frontier plus Arazzo workflow, with feature-by-feature evidence and explicit fallbacks to the executable 3.1 baseline.

## Setup conditions

The previous baseline is: **API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we use current OpenAPI capabilities without claiming that every tool supports them equally?*

## Failure action and investigation

1. Upgrade a copy of the canonical root to 3.2.0, validate it with the course structural route, and verify all common operation IDs remain stable.
2. Add hierarchical tags with summary, parent, and kind; detect unresolved parents and cycles.
3. Add the QUERY experiment through `additionalOperations` and a complete `querystring` parameter, while retaining a 3.1-compatible POST fallback.
4. Describe SSE and NDJSON progress with item schemas, then validate individual events and framing against both providers.
5. Add callback, root webhook, and response links; evaluate every runtime expression against concrete fixtures.
6. Complete the Arazzo 1.1 workflow from project creation through artifact retrieval and validate all operation references and captured outputs.
7. Run every available tool probe, classify each feature/stage, record not-executed cases accurately, and write frontier promotion criteria.

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

The system satisfies the chapter’s central question: How do we use current OpenAPI capabilities without claiming that every tool supports them equally? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **OpenAPI 3.2, Streaming, Webhooks, and Workflows** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Maintain a broadly executable OpenAPI 3.1 baseline.
- public, durable, security, or operational observation showing: Course 1 ends with API 1.1, an OpenAPI 3.2 frontier, and an executable create-to-artifact workflow.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
3. Rerun the focused regression and `make module-proof MODULE=10`.
4. Confirm the system again provides this result: Course 1 ends with API 1.1, an OpenAPI 3.2 frontier, and an executable create-to-artifact workflow.

## Completion gate

- 3.2 frontier validates independently
- common operation identities remain stable
- tag hierarchy resolves without cycles
- QUERY/querystring and sequential itemSchema are present
- callbacks/webhooks/links have correct direction and expressions
- Arazzo references real operations
- capability claims distinguish unsupported from not executed
