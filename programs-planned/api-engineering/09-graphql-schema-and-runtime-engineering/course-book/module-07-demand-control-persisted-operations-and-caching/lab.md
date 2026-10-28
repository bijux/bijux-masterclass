# Lab 07 — Attack the admission layer

## Purpose

Demonstrate that standard validation, trusted-document policy, and resource admission are separate controls and that rejected operations cause zero source work.

## Prerequisites

Complete Module 6. Reset call logs and the persisted registry. Use the checked-in cost policy and a development endpoint that permits arbitrary documents only for the controlled lab identity.

## Procedure

### 1. Establish a trusted baseline

Execute the registered `GetProjectOverview` document with normal variables. Record digest, client, expanded field occurrences, cost, cardinality multipliers, distinct services, and final admission decision.

### 2. Submit malformed and invalid documents

Test an alias syntax error, fragment cycle, unknown field, invalid variable type, and missing operation name in a multi-operation document. Classify parse versus validation versus operation-selection failures.

### 3. Submit valid but unaffordable documents

Create:

- an alias storm repeating `artifacts`;
- nested connections with large `first` variables;
- broad cross-type search;
- repeated fragments that expand to expensive fields;
- a shallow document with high service fan-out.

Confirm standard validation passes where expected and admission rejects before execution.

### 4. Attack the persisted registry

Send an unknown digest to the trusted endpoint, then send document bytes alongside that digest. The endpoint must not self-register arbitrary demand. Change one whitespace-normalized or semantic byte and verify identity behavior follows the declared normalization profile.

### 5. Test caching identity

Attempt to reuse a parsed plan or response across schema releases, tenants, policy classes, or variable sets. Confirm keys include all required dimensions and that partial failure is not cached as complete success.

## Correctness oracle

- parse, validation, and admission failures are distinct;
- cost uses selected operation, expanded fragments, aliases, and coerced variables;
- list and nested cardinality are bounded;
- service fan-out enters the decision;
- unknown trusted digests cannot register themselves;
- all rejected cases make zero business-service calls;
- cache identities preserve schema, operation, variable, tenant, policy, and source-version semantics.

## Required evidence

Create `reports/module-07-demand.json` with case, last phase, expanded occurrences, depth, aliases, cardinality estimate, cost, service set, registry outcome, cache identity, and source calls. Do not store raw untrusted documents in production-shaped telemetry; attach them only to local lab evidence.

## Interpretation questions

- Which case defeats a depth-only limit?
- Why should a cost policy be versioned?
- How does a trusted registry differ from APQ caching?
- Which rejected requests should consume a smaller control-plane rate budget?

## Cleanup

Remove arbitrary scratch documents and cache entries. Restore the registry and rerun operation, demand, and manifest proofs.

## Completion gate

Every attack is classified at the correct phase, no rejected demand reaches a source, cache-crossing attempts fail, and Python/TypeScript cost decisions match every shared vector.
