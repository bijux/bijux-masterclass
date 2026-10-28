# Lab — Prove truthful partial data

> **Module 08:** Errors, Partial Data, Consistency, and Observability

## Objective

Prove that data, errors, null propagation, staleness, and telemetry tell the same story under independent source failures.

## Why this lab matters

This lab turns the module’s governing question—**How does the graph tell the truth when some fields succeed, some fail, and some are stale?**—into a falsifiable experiment. Execution errors occur after a valid operation begins: source unavailability, authorization denial, resolver exceptions, deadline expiry, or output completion failure. The response can contain both data and errors. Each error path identifies where the result became unavailable.

It advances the cumulative Analysis Runs Platform by requiring this result: **Return truthful partial data with path-specific errors and traces**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 7. Use `GetRun` and `GetProjectOverview`. Enable deterministic failures for Analysis Control, Artifact Service, and Notification Service independently.

## Hypothesis

The clean implementation should satisfy this claim: **authoritative emptiness is distinct from unavailable unknown state; each independent failure has the correct response path; null bubbling exactly follows the released type declarations; unaffected sibling data survives when permitted; stale projections disclose age; output-type violations are server errors; traces and metrics classify the same source and outcome without logging sensitive data.** When the lab introduces this fault—**Inject a null non-null ID or invalid scalar from a resolver**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject a null non-null ID or invalid scalar from a resolver**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove that data, errors, null propagation, staleness, and telemetry tell the same story under independent source failures**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- authoritative emptiness is distinct from unavailable unknown state;
- each independent failure has the correct response path;
- null bubbling exactly follows the released type declarations;
- unaffected sibling data survives when permitted;
- stale projections disclose age;
- output-type violations are server errors;
- traces and metrics classify the same source and outcome without logging sensitive data.

## Required evidence

Create `reports/module-08-partial-data.json` with source state, data path, returned value class, error code, bubble target, unaffected siblings, consistency metadata, and trace outcome. Include one client decision for each case: render partial, refetch, retry, or stop.

## Interpretation and defense

1. Which state or effect is authoritative for **Errors, Partial Data, Consistency, and Observability**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject a null non-null ID or invalid scalar from a resolver** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Disable all failure injectors, clear partial-response caches, and rerun the healthy operation. Remove generated traces that are not part of the bounded report.

## Completion gate

Every returned value and error path is predicted from the schema and consistency policy, telemetry agrees with the response, and the planted silent-empty fallback is rejected.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Errors, Partial Data, Consistency, and Observability**. A green command without the negative case and causal explanation does not satisfy this gate.
