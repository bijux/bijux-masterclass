# Lab 01 — Trace one operation through every phase

## Purpose

Prove that the graph host distinguishes transport, document, validation, admission, execution, completion, and serialization. The lab also proves that rejected demand creates no business-service effect.

## Prerequisites

Run:

```bash
make predecessor-proof
make orientation-proof
make module-01-proof
```

Use the checked-in Analysis Graph API 1.0 schema, persisted-operation registry, loopback service lab, and one primary language track. Remove generated `dist`, cache, and report files before starting.

## Scenario

`GetProjectOverview` is a trusted query that crosses Analysis Control, Artifact Service, and Notification Service. You will send one valid request and four requests that fail at different phases:

1. unsupported media type;
2. unknown persisted digest;
3. syntactically malformed document in the development endpoint;
4. a valid but over-budget operation;
5. a mutation attempted through GET.

## Procedure

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

## Correctness oracle

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

## Interpretation questions

- Which rejected case consumed the most control-plane work?
- Which failure is retryable without changing the request?
- Which telemetry dimensions remain bounded?
- At what phase is caller identity first required, and at what phase is field authorization required?

## Cleanup

Stop loopback servers. Remove generated reports, caches, and TypeScript `dist`. Restore any scratch policy or document. Rerun `make module-01-proof` from the clean tree.

## Completion gate

The report matches the phase oracle, every rejected case made zero source calls, the valid call plan stayed bounded, Python and TypeScript classifiers agree, and the Course 8 handoff remains byte-identical.
