# Lab 08 — Prove truthful partial data

## Purpose

Prove that data, errors, null propagation, staleness, and telemetry tell the same story under independent source failures.

## Prerequisites

Complete Module 7. Use `GetRun` and `GetProjectOverview`. Enable deterministic failures for Analysis Control, Artifact Service, and Notification Service independently.

## Procedure

### 1. Record the complete response

Execute with all sources healthy. Capture the data tree, source versions, delivery observation time, operation trace, and loader summary.

### 2. Fail Artifact Service

The run remains authoritative. `artifacts` becomes null and the response includes a path-specific `SOURCE_UNAVAILABLE` error. Confirm it does not become `[]`, no stale artifact value is substituted, and unaffected delivery data remains.

### 3. Fail Notification Service

`deliverySummary` becomes null with its own path error. In a separate case, return an allowed stale projection and confirm `observedAt` and `stalenessSeconds` are present. Distinguish stale success from unavailable source.

### 4. Fail Analysis Control

Fail the authoritative root. Predict and observe the null-propagation boundary from the SDL. Confirm child resolvers are not called when the parent cannot be produced.

### 5. Violate an output type

Inject a null non-null ID or invalid scalar from a resolver. Confirm the runtime treats it as a server completion error and bubbles according to the field type.

### 6. Compare telemetry

For each case, verify phase, error code, source span outcome, partial/complete classification, and SLI population. HTTP status alone must not classify success.

## Correctness oracle

- authoritative emptiness is distinct from unavailable unknown state;
- each independent failure has the correct response path;
- null bubbling exactly follows the released type declarations;
- unaffected sibling data survives when permitted;
- stale projections disclose age;
- output-type violations are server errors;
- traces and metrics classify the same source and outcome without logging sensitive data.

## Required evidence

Create `reports/module-08-partial-data.json` with source state, data path, returned value class, error code, bubble target, unaffected siblings, consistency metadata, and trace outcome. Include one client decision for each case: render partial, refetch, retry, or stop.

## Interpretation questions

- Which operation might require complete product-level data even though GraphQL permits partial data?
- Why is an empty list dangerous as a fallback?
- How should a response cache treat a partial result?
- Which metric dimensions would create cardinality risk?

## Cleanup

Disable all failure injectors, clear partial-response caches, and rerun the healthy operation. Remove generated traces that are not part of the bounded report.

## Completion gate

Every returned value and error path is predicted from the schema and consistency policy, telemetry agrees with the response, and the planted silent-empty fallback is rejected.
