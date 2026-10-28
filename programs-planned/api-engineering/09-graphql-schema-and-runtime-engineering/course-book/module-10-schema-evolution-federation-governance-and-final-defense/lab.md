# Lab — Release the graph or reject it

> **Module 10:** Schema Evolution, Federation, Governance, and Final Defense

## Objective

Run a complete GraphQL release review against schema, active operations, ownership, demand, authorization, partial-failure behavior, and platform handoff evidence.

## Why this lab matters

This lab turns the module’s governing question—**How does the graph evolve without breaking clients, erasing service ownership, or becoming an ungoverned platform?**—into a falsifiable experiment. A candidate release passes only when the schema parses in an independent implementation, all active operations validate, field ownership is complete, cost budgets do not regress, authorization tests pass, old clients execute, and partial-response semantics remain truthful. Review-required changes pause for consumer evidence.

It advances the cumulative Analysis Runs Platform by requiring this result: **Approve Graph API 1.0, reject breaking candidates, and publish Course 10 handoff**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Modules 1–9. Restore a clean tree. Verify every persisted operation has an owner and supported client release. Run the current release as the baseline.

## Hypothesis

The clean implementation should satisfy this claim: **invalidates a supported operation; narrows accepted input unexpectedly; increases null-bubbling blast radius without migration evidence; creates unbounded demand or fan-out; bypasses source ownership; weakens authorization or partial-failure truth; exceeds active operation budgets; lacks client, field, or service ownership; cannot produce a sanitized exact handoff.** When the lab introduces this fault—**Inject source failure and retry cases**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

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

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject source failure and retry cases**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Run a complete GraphQL release review against schema, active operations, ownership, demand, authorization, partial-failure behavior, and platform handoff evidence**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

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

## Interpretation and defense

1. Which state or effect is authoritative for **Schema Evolution, Federation, Governance, and Final Defense**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject source failure and retry cases** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Delete generated candidate build output, restore the accepted release, regenerate only manifest-controlled handoff files, and run the full proof from a clean checkout.

## Completion gate

The accepted candidate passes every layer, unsafe candidates fail for the intended reasons, active operations remain valid and executable, the final defense is complete, and the Course 10 handoff verifies exactly.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Schema Evolution, Federation, Governance, and Final Defense**. A green command without the negative case and causal explanation does not satisfy this gate.
