# Lab — Module 10: OpenAPI 3.2, Streaming, Webhooks, and Workflows

> **Module 10:** OpenAPI 3.2, Streaming, Webhooks, and Workflows

## Objective

Publish and defend the 3.2 frontier plus Arazzo workflow, with feature-by-feature evidence and explicit fallbacks to the executable 3.1 baseline.

## Why this lab matters

This lab turns the module’s governing question—**How do current OpenAPI features express streaming, webhooks, links, query methods, and multi-step workflows?**—into a falsifiable experiment. The executable baseline uses OpenAPI 3.1.2 because the selected generators and framework integrations have broad 3.1 support. The frontier description upgrades the same API to 3.2.0 and exercises current constructs. The two artifacts share operation identity and domain semantics; the frontier is not a speculative rewrite.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **API 1.1 is released, a breaking candidate is rejected, and public/partner views are derived from the canonical contract.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How do we use current OpenAPI capabilities without claiming that every tool supports them equally?*

## Hypothesis

The clean implementation should satisfy this claim: **3.2 frontier validates independently; common operation identities remain stable; tag hierarchy resolves without cycles; QUERY/querystring and sequential itemSchema are present; callbacks/webhooks/links have correct direction and expressions; Arazzo references real operations; capability claims distinguish unsupported from not executed.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Publish and defend the 3.2 frontier plus Arazzo workflow, with feature-by-feature evidence and explicit fallbacks to the executable 3.1 baseline**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- 3.2 frontier validates independently
- common operation identities remain stable
- tag hierarchy resolves without cycles
- QUERY/querystring and sequential itemSchema are present
- callbacks/webhooks/links have correct direction and expressions
- Arazzo references real operations
- capability claims distinguish unsupported from not executed

## Required evidence

- baseline transcript proving the previous checkpoint before **OpenAPI 3.2, Streaming, Webhooks, and Workflows** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **OpenAPI 3.2, Streaming, Webhooks, and Workflows**
- focused result for: Maintain a broadly executable OpenAPI 3.1 baseline.
- public, durable, security, or operational observation showing: Course 1 ends with API 1.1, an OpenAPI 3.2 frontier, and an executable create-to-artifact workflow.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**
- a limitation statement naming every live dependency required to support the strongest **OpenAPI 3.2, Streaming, Webhooks, and Workflows** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **OpenAPI 3.2, Streaming, Webhooks, and Workflows** experiment.
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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **OpenAPI 3.2, Streaming, Webhooks, and Workflows**. A green command without the negative case and causal explanation does not satisfy this gate.
