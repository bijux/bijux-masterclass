# Lab — Module 01: HTTP and OpenAPI Foundations

> **Module 01:** HTTP and OpenAPI Foundations

## Objective

Build the first four operations from raw HTTP messages, then plant an undocumented success status in one provider and prove the shared evidence catches it.

## Why this lab matters

This lab turns the module’s governing question—**How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?**—into a falsifiable experiment. A specification can parse while the provider returns 200 instead of 201, emits text/plain, accepts undocumented input, or leaks an internal field. Conversely, a working provider may have no complete contract. Static checks prove document properties; live checks prove observed behavior.

It advances the cumulative Analysis Runs Platform by requiring this result: **Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **the orientation baseline** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do raw HTTP exchanges become a public contract without confusing documentation with runtime behavior?*

## Hypothesis

The clean implementation should satisfy this claim: **four introductory operations have unique stable IDs; project creation is 201 with Location and JSON; the path parameter is explicitly required; health is explicitly anonymous; both providers pass equivalent positive and negative cases; the planted status defect is detected.** When the lab introduces this fault—**Temporarily change one provider to return 200 for project creation**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Temporarily change one provider to return 200 for project creation**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Build the first four operations from raw HTTP messages, then plant an undocumented success status in one provider and prove the shared evidence catches it**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- four introductory operations have unique stable IDs
- project creation is `201` with `Location` and JSON
- the path parameter is explicitly required
- health is explicitly anonymous
- both providers pass equivalent positive and negative cases
- the planted status defect is detected

## Required evidence

- baseline transcript proving the previous checkpoint before **HTTP and OpenAPI Foundations** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **HTTP and OpenAPI Foundations**
- focused result for: Read requests and responses as protocol messages.
- public, durable, security, or operational observation showing: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **HTTP and OpenAPI Foundations**
- a limitation statement naming every live dependency required to support the strongest **HTTP and OpenAPI Foundations** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **HTTP and OpenAPI Foundations**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Temporarily change one provider to return 200 for project creation** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **HTTP and OpenAPI Foundations**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **HTTP and OpenAPI Foundations** experiment.
3. Rerun the focused regression and `make module-proof MODULE=01`.
4. Confirm the system again provides this result: The Analysis Runs API gains `/health`, project creation, project listing, and project retrieval.

## Completion gate

- four introductory operations have unique stable IDs
- project creation is `201` with `Location` and JSON
- the path parameter is explicitly required
- health is explicitly anonymous
- both providers pass equivalent positive and negative cases
- the planted status defect is detected

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **HTTP and OpenAPI Foundations**. A green command without the negative case and causal explanation does not satisfy this gate.
