# Lab 02 — Break and repair nullability

## Purpose

Observe nullability as executable failure control rather than a type-style preference. Prove OneOf input coercion and output-completion behavior.

## Prerequisites

Complete Module 1. Copy `capstone/contracts/schema.graphql` to a scratch directory; never edit the released schema in place.

## Scenario

The released field is:

```graphql
type AnalysisRun {
  artifacts: [Artifact!]
}
```

Artifact Service can fail independently, so the list is nullable. You will compare that contract with an unsafe scratch version `[Artifact!]!`, then test invalid output values and `NodeLookup @oneOf` inputs.

## Procedure

### 1. Capture the released behavior

Execute `GetRun` with Artifact Service healthy and record a complete result. Inject Artifact Service unavailability and repeat. The run must remain present, `artifacts` must become null, and the error path must point to `analysisRun.artifacts`.

### 2. Strengthen nullability unsafely

Change only the scratch SDL to `[Artifact!]!`. Execute the same failure through a complete framework adapter when available or the checked-in completion simulator otherwise. Draw the exact propagation path from `artifacts` to its nearest nullable ancestor.

### 3. Violate item nullability

Return a list containing one null item for `[Artifact!]`. Confirm that the list itself becomes null and the error path includes the item index. Compare this with `[Artifact]`, and explain why the latter is not the chosen contract.

### 4. Test scalar and enum completion

Inject an invalid `size`, malformed `DateTime`, and unknown `RunStatus` output. These are server contract failures. They must not be reported as client variable errors.

### 5. Test OneOf coercion

Evaluate:

```text
{id: "..."}
{externalId: "..."}
{}
{id: "...", externalId: "..."}
{id: null}
```

Exactly one non-null member is required. Record whether rejection occurs before resolver execution.

## Correctness oracle

- released remote field failure preserves the `AnalysisRun` object;
- scratch non-null field increases the bubbling blast radius;
- null list items obey item nullability;
- invalid resolver output is an execution/completion error;
- OneOf accepts exactly one non-null alternative;
- every rejected input makes zero source calls.

## Required evidence

Create `reports/module-02-type-nullability.json` containing the released and scratch type declarations, completed data trees, error paths, bubble targets, and OneOf coercion table. Include a short design decision explaining why the released nullability is sustainable across authorization and source failure.

## Interpretation questions

- Would making `Query.analysisRun` non-null improve client safety or increase outage blast radius?
- When is an empty list authoritative?
- What evidence would justify changing a nullable field to non-null in a future release?
- Which client operations would be affected by the change?

## Cleanup

Delete the scratch schema and injected fixtures. Re-run schema, vector, and module proofs. The released SDL and predecessor handoff must have no diff.

## Completion gate

Your evidence predicts every completion tree before execution, OneOf outcomes match both language tracks, and the scratch non-null change is classified correctly by the release checker.
