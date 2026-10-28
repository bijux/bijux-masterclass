# Lab — Attack the admission layer

> **Module 07:** Demand Control, Persisted Operations, and Caching

## Objective

Demonstrate that standard validation, trusted-document policy, and resource admission are separate controls and that rejected operations cause zero source work.

## Why this lab matters

This lab turns the module’s governing question—**How can a client-shaped query language remain bounded under adversarial and accidental demand?**—into a falsifiable experiment. Rate limits and cost budgets must be charged consistently. A tenant should not evade limits by splitting one expensive operation into many cheap-looking aliases, nor should an invalid document consume the same source budget as executed work. The policy defines whether rejected admission consumes a smaller control-plane budget to resist validation abuse.

It advances the cumulative Analysis Runs Platform by requiring this result: **Admit only bounded trusted operations and record cost evidence**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 6. Reset call logs and the persisted registry. Use the checked-in cost policy and a development endpoint that permits arbitrary documents only for the controlled lab identity.

## Hypothesis

The clean implementation should satisfy this claim: **parse, validation, and admission failures are distinct; cost uses selected operation, expanded fragments, aliases, and coerced variables; list and nested cardinality are bounded; service fan-out enters the decision; unknown trusted digests cannot register themselves; all rejected cases make zero business-service calls; cache identities preserve schema, operation, variable, tenant, policy, and source-version semantics.** When the lab introduces this fault—**Confirm keys include all required dimensions and that partial failure is not cached as complete success**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Confirm keys include all required dimensions and that partial failure is not cached as complete success**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Demonstrate that standard validation, trusted-document policy, and resource admission are separate controls and that rejected operations cause zero source work**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- parse, validation, and admission failures are distinct;
- cost uses selected operation, expanded fragments, aliases, and coerced variables;
- list and nested cardinality are bounded;
- service fan-out enters the decision;
- unknown trusted digests cannot register themselves;
- all rejected cases make zero business-service calls;
- cache identities preserve schema, operation, variable, tenant, policy, and source-version semantics.

## Required evidence

Create `reports/module-07-demand.json` with case, last phase, expanded occurrences, depth, aliases, cardinality estimate, cost, service set, registry outcome, cache identity, and source calls. Do not store raw untrusted documents in production-shaped telemetry; attach them only to local lab evidence.

## Interpretation and defense

1. Which state or effect is authoritative for **Demand Control, Persisted Operations, and Caching**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Confirm keys include all required dimensions and that partial failure is not cached as complete success** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Remove arbitrary scratch documents and cache entries. Restore the registry and rerun operation, demand, and manifest proofs.

## Completion gate

Every attack is classified at the correct phase, no rejected demand reaches a source, cache-crossing attempts fail, and Python/TypeScript cost decisions match every shared vector.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Demand Control, Persisted Operations, and Caching**. A green command without the negative case and causal explanation does not satisfy this gate.
