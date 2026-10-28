# Lab — Trace one operation through every phase

> **Module 01:** Graph Interface Placement and the Operation Lifecycle

## Objective

Prove that the graph host distinguishes transport, document, validation, admission, execution, completion, and serialization. The lab also proves that rejected demand creates no business-service effect.

## Why this lab matters

This lab turns the module’s governing question—**Where does GraphQL belong, and what happens between receiving a document and returning a response?**—into a falsifiable experiment. A GraphQL request passes through identifiable phases: HTTP framing, document acquisition, parsing, operation selection, validation, variable coercion, admission policy, execution, value completion, and response serialization. Authentication and request context are established before field execution; field authorization remains part of execution because different selections can have different permissions.

It advances the cumulative Analysis Runs Platform by requiring this result: **Publish the graph boundary and operation-lifecycle trace**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Run:

```bash
make predecessor-proof
make orientation-proof
make module-01-proof
```

Use the checked-in Analysis Graph API 1.0 schema, persisted-operation registry, loopback service lab, and one primary language track. Remove generated `dist`, cache, and report files before starting.

## Hypothesis

The clean implementation should satisfy this claim: **Case Last reached phase Business calls Required outcome --- --- ---: --- valid persisted query serialization bounded expected calls complete or declared partial GraphQL response unsupported media HTTP framing 0 HTTP-profile error unknown digest document acquisition 0 stable persisted-operation error malformed document parsing 0 GraphQL request error over-budget document admission 0 stable admission rejection mutation via GET transport policy 0 method rejection** When the lab introduces this fault—**Remove generated dist, cache, and report files before starting**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Establish the valid trace

Run the valid operation for tenant `tenant-a`. Record:

- transport method and negotiated response media type;
- persisted digest and operation name;
- schema release;
- calculated cost and service fan-out;
- source-service call sequence;
- loader dispatch counts;
- final data/error classification.

The expected call plan is two Analysis Control calls, one batched Artifact call, and one batched Notification call. Exact endpoint names come from the checked-in service catalogue.

### 2. Reject at the HTTP boundary

Send a body with `Content-Type: text/plain`. Then request `application/xml`. Confirm that document lookup, parsing, validation, and source execution do not run.

### 3. Reject during document acquisition and parsing

Send an unknown persisted identifier. On the development-only arbitrary-document path, send unbalanced braces. Confirm that the first fails before parsing and the second fails after acquisition but before validation.

### 4. Reject during admission

Use a schema-valid query whose aliases, nested cardinality, or `first` variable exceed the policy. Capture the admission rule IDs and prove that all service call counters remain zero.

### 5. Test HTTP method semantics

Attempt `StartAnalysis` through GET. The operation may be valid GraphQL, but the transport profile must reject side-effecting execution through a safe method.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove generated dist, cache, and report files before starting**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove that the graph host distinguishes transport, document, validation, admission, execution, completion, and serialization. The lab also proves that rejected demand creates no business-service effect**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

| Case | Last reached phase | Business calls | Required outcome |
|---|---|---:|---|
| valid persisted query | serialization | bounded expected calls | complete or declared partial GraphQL response |
| unsupported media | HTTP framing | 0 | HTTP-profile error |
| unknown digest | document acquisition | 0 | stable persisted-operation error |
| malformed document | parsing | 0 | GraphQL request error |
| over-budget document | admission | 0 | stable admission rejection |
| mutation via GET | transport policy | 0 | method rejection |

## Required evidence

Create `reports/module-01-operation-lifecycle.json` with:

```json
{
  "schemaRelease": "1.0.0",
  "cases": [
    {
      "name": "valid",
      "lastPhase": "serialization",
      "operationId": "...",
      "sourceCalls": {},
      "responseClass": "complete"
    }
  ]
}
```

Do not include bearer tokens, raw arbitrary variables, or returned business data. Include assertions showing which planted defect would make the report fail.

## Interpretation and defense

1. Which state or effect is authoritative for **Graph Interface Placement and the Operation Lifecycle**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove generated dist, cache, and report files before starting** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Stop loopback servers. Remove generated reports, caches, and TypeScript `dist`. Restore any scratch policy or document. Rerun `make module-01-proof` from the clean tree.

## Completion gate

The report matches the phase oracle, every rejected case made zero source calls, the valid call plan stayed bounded, Python and TypeScript classifiers agree, and the Course 8 handoff remains byte-identical.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Graph Interface Placement and the Operation Lifecycle**. A green command without the negative case and causal explanation does not satisfy this gate.
