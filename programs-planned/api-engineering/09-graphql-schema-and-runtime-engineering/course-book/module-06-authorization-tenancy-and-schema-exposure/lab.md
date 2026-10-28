# Lab 06 — Attack nested authorization

## Purpose

Prove that valid identity and plausible object identifiers cannot bypass scope, tenant, ownership, field, or subscription policy through graph traversal.

## Prerequisites

Complete Module 5. Prepare principals with:

- `RUN_READ` only;
- `ARTIFACT_READ` only;
- run and artifact permissions;
- full tenant permissions;
- correct scopes but wrong tenant;
- support role without required audit context.

## Procedure

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

## Correctness oracle

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

## Interpretation questions

- When is null plus `FORBIDDEN` preferable to object concealment?
- Which policy belongs in the graph and which must be repeated by the owner?
- Why can introspection restriction not substitute for authorization?
- What side channel remains after response values are concealed?

## Cleanup

Clear request caches, revoke fixture sessions, and stop subscription workers. Rerun the full authorization vector corpus in both tracks.

## Completion gate

Every traversal preserves tenant and field policy, no privileged cache entry crosses requests, owner-side mutation checks remain active, and the planted post-filter and global-loader defects are rejected.
