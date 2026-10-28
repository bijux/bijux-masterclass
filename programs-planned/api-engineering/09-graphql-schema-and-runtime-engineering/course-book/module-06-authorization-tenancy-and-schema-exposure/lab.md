# Lab — Attack nested authorization

> **Module 06:** Authorization, Tenancy, and Schema Exposure

## Objective

Prove that valid identity and plausible object identifiers cannot bypass scope, tenant, ownership, field, or subscription policy through graph traversal.

## Why this lab matters

This lab turns the module’s governing question—**How can clients select flexible fields without gaining flexible authority?**—into a falsifiable experiment. The decisive proof is adversarial traversal: a caller with a valid token and plausible identifiers attempts to reach foreign project, run, artifact, delivery, and subscription data through every available root and nested path. All paths must preserve the same authority model.

It advances the cumulative Analysis Runs Platform by requiring this result: **Prove field, tenant, collection, and sensitive-output authorization**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Complete Module 5. Prepare principals with:

- `RUN_READ` only;
- `ARTIFACT_READ` only;
- run and artifact permissions;
- full tenant permissions;
- correct scopes but wrong tenant;
- support role without required audit context.

## Hypothesis

The clean implementation should satisfy this claim: **correct scope without resource authority is insufficient; resource relationship without required permission is insufficient; collection membership is filtered at the owner; denied fields do not call protected sources unnecessarily; global IDs and typename do not become existence oracles; loaders and caches are request/tenant/policy partitioned; mutations are reauthorized by the owner; subscriptions do not retain authority indefinitely.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

### 1. Attack every root

Use known and guessed IDs with `project`, `analysisRun`, `artifact`, `node`, `analysisRuns`, and `search`. Record whether foreign and missing objects are distinguishable through data, errors, type names, timing class, or page information.

### 2. Attack nested fields

Start from an authorized run and select `artifacts`, `downloadUrl`, and `deliverySummary` under principals missing each required permission. Confirm denial occurs before the protected source call where policy allows early rejection.

### 3. Attack collections and pagination

Request a mixed-tenant population. Verify the source query contains tenant/policy constraints before ordering and page construction. Confirm page size, cursors, and `hasNextPage` do not reveal filtered foreign rows.

### 4. Attack loader and cache scope

Resolve a sensitive field as a privileged caller, then repeat the same local key in another request as an unprivileged or foreign caller. Request-scoped loaders and response caches must not reuse the privileged value.

### 5. Attack mutation and subscription paths

Attempt to cancel a foreign run, start work in another project, and subscribe to another tenant's run updates. Then revoke permission during an open subscription and confirm termination under the course profile.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Prove that valid identity and plausible object identifiers cannot bypass scope, tenant, ownership, field, or subscription policy through graph traversal**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- correct scope without resource authority is insufficient;
- resource relationship without required permission is insufficient;
- collection membership is filtered at the owner;
- denied fields do not call protected sources unnecessarily;
- global IDs and `__typename` do not become existence oracles;
- loaders and caches are request/tenant/policy partitioned;
- mutations are reauthorized by the owner;
- subscriptions do not retain authority indefinitely.

## Required evidence

Create `reports/module-06-authorization.json` with principal class, tenant, operation, field coordinate, decision, concealment behavior, source-call count, cache key class, and subscription closure reason. Pseudonymize subject and object identities.

## Interpretation and defense

1. Which state or effect is authoritative for **Authorization, Tenancy, and Schema Exposure**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Clear request caches, revoke fixture sessions, and stop subscription workers. Rerun the full authorization vector corpus in both tracks.

## Completion gate

Every traversal preserves tenant and field policy, no privileged cache entry crosses requests, owner-side mutation checks remain active, and the planted post-filter and global-loader defects are rejected.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Authorization, Tenancy, and Schema Exposure**. A green command without the negative case and causal explanation does not satisfy this gate.
