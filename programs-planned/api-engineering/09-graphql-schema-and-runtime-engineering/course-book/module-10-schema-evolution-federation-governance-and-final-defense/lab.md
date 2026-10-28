# Lab 10 — Release the graph or reject it

## Purpose

Run a complete GraphQL release review against schema, active operations, ownership, demand, authorization, partial-failure behavior, and platform handoff evidence.

## Prerequisites

Complete Modules 1–9. Restore a clean tree. Verify every persisted operation has an owner and supported client release. Run the current release as the baseline.

## Candidate set

Evaluate these checked-in candidates:

1. optional output field with source and policy evidence;
2. output enum value addition;
3. field removal;
4. new required input field;
5. nullable output changed to non-null;
6. unbounded list field;
7. resolver moved to a direct private-database join;
8. remote failure replaced silently with empty data;
9. field authority moved without service-owner approval;
10. cost increase that pushes an active operation over budget.

## Procedure

### 1. Validate the candidate type system

Parse and validate the candidate SDL with the available complete framework or independent CLI. Record tool and version. The dependency-light structural checker is supplementary, not independent conformance evidence.

### 2. Classify schema changes

Produce a coordinate-level diff. Classify breaking, review-required, and additive changes. Explain direction: input requiredness and output nullability do not have the same compatibility meaning.

### 3. Revalidate active operations

Validate all active persisted documents and variable fixtures against the candidate. Do not sample only popular operations. Record client owner and support window for each failure.

### 4. Re-evaluate non-SDL policy

Recompute cost, fan-out, authorization coordinates, source authority, nullability failure behavior, and cache identity. A schema-identical runtime can still be an incompatible release.

### 5. Execute representative old clients

Run at least one query, mutation, and subscription from the current supported client set against the candidate runtime. Inject source failure and retry cases.

### 6. Decide and publish evidence

Only the fully evidenced additive candidate can be accepted automatically. Enum addition remains review-required. Every other unsafe candidate is rejected with an exact coordinate, operation, policy, or architecture reason.

### 7. Build the Course 10 handoff

Publish the released SDL, schema catalogue, persisted-operation catalogue, client ownership, field ownership, demand policy, version ledger, and release summary. Exclude private tokens, source databases, and internal incident data.

## Correctness oracle

The release gate must reject any candidate that:

- invalidates a supported operation;
- narrows accepted input unexpectedly;
- increases null-bubbling blast radius without migration evidence;
- creates unbounded demand or fan-out;
- bypasses source ownership;
- weakens authorization or partial-failure truth;
- exceeds active operation budgets;
- lacks client, field, or service ownership;
- cannot produce a sanitized exact handoff.

## Required evidence

Create `reports/module-10-release.json`, `capstone/final-defense/defense-record.json`, and the Course 10 handoff manifest. The release report includes tool versions, schema digest, operation population, change classification, policy deltas, runtime scenarios, decision, approvers by role, and residual risks.

## Final defense

Defend one query, mutation, and subscription from client document to source authority. For each, name identity, authorization, cardinality, deadline, downstream calls, consistency, failure behavior, telemetry, compatibility, and decisive proof.

## Cleanup

Delete generated candidate build output, restore the accepted release, regenerate only manifest-controlled handoff files, and run the full proof from a clean checkout.

## Completion gate

The accepted candidate passes every layer, unsafe candidates fail for the intended reasons, active operations remain valid and executable, the final defense is complete, and the Course 10 handoff verifies exactly.
