---
module_id: API-019
program: API & Service Engineering
level: 1
module_number: 19
title: Bulk and Batch Operations
status: complete
last_verified: 2026-09-01
---

# Bulk and Batch Operations

## One-Page Review

### Governing question

How can an API apply one declared intent to many targets without hiding target selection, authorization, atomicity, partial failure, retry, ordering, or cost?

### Essential definitions

- A **bulk operation** applies one homogeneous action to a selected set of resources.
- A **batch** packages multiple independently described requests or commands.
- A **target set** is the explicitly defined snapshot or live set to which a bulk action applies.
- **Atomicity** means all-or-nothing effect over a stated boundary, not merely one HTTP request.
- A **per-item outcome** records the result for one target without implying the whole request succeeded.
- A **dependency** makes one batch item require another item's outcome.

### Central model, mechanism, or theorem

For target set $X$ and action $a$, a bulk request denotes $B(a,X)=\{a(x)\mid x\in X\}$. A contract must state whether $X$ is resolved at acceptance or during execution, and whether its outcome is all-or-nothing, best effort, or partitioned. If results are per-item, each result must identify the input item or stable target and its independent status.

### Critical invariants

Selection precedes action under authorization. Limits bound target count, request size, fan-out, duration, and result retention. Atomicity names its datastore or business boundary. Per-item statuses cannot be silently collapsed into success. A retry preserves logical request identity. Dependency order is explicit and acyclic. Batch transport does not bypass normal auth, validation, rate, audit, or idempotency policy.

### Common failures

Calling every repeated call “batch”; accepting `ids=all`; applying authorization after pagination; returning `200` without item outcomes; claiming a distributed transaction; retrying already successful non-idempotent items; ordering effects by accidental JSON array order; exposing hidden targets in errors; and returning an enormous result that defeats the original cost limit.

### Compact example

`POST /users:deactivate` supplies a saved-selection identifier, reason, and idempotency key. The service snapshots 40 authorized users, creates a long-running bulk operation, and reports 38 successes and 2 conditional conflicts. The caller can retrieve each failed target only because it already had permission to see it. **Conclusion:** bulk selection, execution, and reporting are separate contracts.

### Connections

[Long-Running Operations](018-long-running-operations.md) supplies durable observation for expensive fan-out. [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) supplies bounded authorized selection. [Create, Read, Update, and Delete Semantics](015-create-read-update-and-delete-semantics.md) supplies individual method effects and preconditions.

## Governing Question

What operation shape gives clients efficient multi-resource work while preserving the same semantic, security, and failure precision expected of a single-resource request?

## Why This Matters

Bulk work appears everywhere: import records, deactivate accounts, tag documents, rebuild indexes, delete selected objects, or apply a policy to a fleet. A loop of individual calls is sometimes correct, but can be slow, non-atomic, difficult to observe, and vulnerable to client crashes. A single “bulk” endpoint is not automatically better: it can turn a narrow request into unbounded fan-out and conceal partial effects.

The first decision is semantic, not syntactic. A homogeneous bulk command means “perform one operation over a governed set.” A heterogeneous batch means “transport several separately specified operations.” They need different errors, dependencies, authorization checks, and retry rules. SCIM's bulk protocol is a concrete standardized example of a body containing multiple operations with `bulkId` references and an error threshold; it is a protocol-specific design, not a general REST prescription. RFC 4918's `207 Multi-Status` likewise demonstrates that an overall response may require per-resource status interpretation, but its XML format is WebDAV-specific. [RFC 7644](https://www.rfc-editor.org/rfc/rfc7644.html) and [RFC 4918](https://www.rfc-editor.org/rfc/rfc4918.html) were checked on 2026-09-01.

## Prerequisites and Retrieval

Retrieve resource collection semantics, authorization filtering, conditional writes, idempotency, transactions, distributed failure, pagination, queues, long-running operations, quotas, and problem details. Recall that a database transaction is only atomic for the resources and systems participating in that transaction.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish homogeneous bulk actions from heterogeneous batches;
2. specify target-set resolution, authorization, and limits;
3. choose all-or-nothing, per-item, and asynchronous execution semantics;
4. model dependencies, ordering, retries, and idempotency safely;
5. design useful aggregate and per-item reports without disclosure; and
6. test partial failure, stale selection, duplicate submission, and resource exhaustion.

## Core Exposition

### Choose the operation shape

Use a bulk action when one verb, policy, and input schema apply to a collection of targets. `POST /documents:archive` with an explicit selection and retention reason communicates more than a generic endpoint that embeds arbitrary mini-HTTP requests. It can validate shared parameters once and state common authorization and atomicity rules.

Use a heterogeneous batch only when independent operations genuinely need to travel together: perhaps a client is offline or a high-latency link benefits from multiplexing. A batch is an envelope, not permission to invent a second ungoverned HTTP stack. Each item still has a method/action, target, body, preconditions, identity, and result. Keep it bounded; a batch is not a general-purpose workflow language.

Avoid a bulk endpoint merely to save round trips when individual requests already have clear idempotency and the client can safely parallelize within quotas. The server-owned operation earns its complexity when shared selection, transaction boundary, audit, scheduling, or result reporting matters.

### Specify target sets before effects

Targets can be an explicit bounded list of public IDs, a server-side saved selection, or a filter grammar. Define which is accepted; never silently treat an omitted list as “all.” If a filter selects targets, document its maximum cardinality, authorization behavior, sorting/snapshot rules, and whether the set is evaluated at acceptance, execution start, or continually.

For a destructive action, a selection preview or dry-run can make the count, examples, policy exclusions, and estimated cost visible. Dry-run is a simulation under stated read conditions, not a promise that later execution sees the identical world. If repeatability matters, create a selection resource that records a snapshot identity and expiry, then make the bulk operation refer to it.

Authorization must define the target universe before selection and count. Fetching a broad list, taking its first thousand rows, then discarding unauthorized targets creates short work, unstable limits, and possible timing/count disclosure. Per-target authorization can still vary at execution time; state whether a revocation causes skip, failure, or whole-operation abort.

### Name the atomicity boundary honestly

There are three common contracts. **Atomic bulk** either changes every selected target or none, normally only within one transaction and bounded datastore scope. **Best-effort bulk** attempts each target independently and returns a report. **Partitioned atomic bulk** commits groups, such as tenant or shard partitions, and reports each partition outcome. The third can be operationally practical but must not be marketed as all-or-nothing.

One HTTP request does not create a distributed transaction across a database, object store, email provider, and payment service. If a command crosses those boundaries, use idempotent effects, an outbox, compensating actions, and explicit uncertainty/reconciliation. The public operation must say what users can rely on, not what a happy-path implementation usually does.

Preconditions have a scope. An operation may require a collection version, a selection snapshot version, or a version for every target. A single collection version is cheap but coarse; per-item conditions are precise but enlarge the request and report. Rejecting the whole request before effects differs from attempting each item and reporting conflicts.

### Design per-item reporting

For best-effort work, return aggregate totals plus a stable way to retrieve per-item outcomes. Each outcome should include input position or client item ID, authorized public target identifier where appropriate, state/status, safe problem detail, and any result reference. Do not report an unauthorized target merely to explain why it failed.

An overall HTTP success says that the API processed the bulk request according to its contract; it does not prove every item changed. `207 Multi-Status` is defined by WebDAV and should not be copied casually into a JSON API without a media-type and semantics specification. A `200` or `202` with an explicit application-level summary can be clearer. Use `202` plus an [operation resource](018-long-running-operations.md) when enumeration, fan-out, or report generation is expensive.

Result reporting itself needs bounds. Put a maximum inline number of outcomes, paginate a result collection, retain it for a declared window, and offer aggregate counts. An omitted result must be distinguishable from success; otherwise a client cannot reconcile a partial run.

### Retry, ordering, and dependencies

A bulk request needs logical identity. Bind an idempotency key to tenant/principal, action, normalized shared parameters, target selection identity, preconditions, and a retention period. A duplicate same-intent submission returns the existing operation/report. A key reused for another selection is a conflict. The current IETF idempotency-key draft is an Internet-Draft rather than a finished standard as checked 2026-09-01; use it as a current design reference, not a universal normative claim.

Items may be independent, sequential, or dependency-ordered. State this explicitly. A JSON array's order is transport order, not necessarily commit order. If batch item B consumes a resource created by A, use a declared reference mechanism and reject dependency cycles before execution. Bound dependency depth and total graph size. Independent items may run concurrently, so clients cannot infer deterministic inter-item timestamps.

Retrying only failed items is safe only if the action and side effects are idempotent or the request includes conditions that detect prior effect. “Retry all failures” is unsafe when failure means “outcome unknown.” Preserve enough per-item attempt identity to reconcile an uncertain external call instead of guessing.

### Govern cost, security, and audit

Set maximum item count, body size, parsed nesting, references, selected targets, concurrent execution, duration, report size, and retention. Apply quota fairly by principal/tenant and charge according to meaningful cost rather than one request token for a million-target delete. Reject over-limit work before effects where possible; if a live selection grows past a cap, state whether the operation fails, truncates, or requires a snapshot.

Authorize the batch envelope and every target/action. A batch must not let a caller invoke methods unavailable through ordinary routes, bypass CSRF or content validation, or smuggle arbitrary internal URLs. Normalize and validate target IDs; never route arbitrary embedded paths to internal services. Audit actor, common intent, resolved selection, policy revision where needed, per-item outcome, and correlation ID.

Protect reports like any other sensitive collection. An administrator may be allowed to start a policy action but not read all resulting resource fields. Provide identifiers and error detail consistent with the viewer's authorization at retrieval time, and retain minimally necessary evidence.

### Test visible guarantees

Construct fixtures with zero, one, exact-limit, over-limit, duplicate, stale, unauthorized, conflicted, and cross-partition targets. Test snapshot expiry, live-set growth, worker crash before/after a partition commit, duplicate submission, duplicate queue delivery, dependency cycle, callback failure, report pagination, authorization revocation, and cancellation.

The decisive test is not “did the loop finish?” It is whether a client can determine each promised outcome and safely choose retry, repair, or stop. Instrument queue delay, selected versus attempted counts, conflicts, unknown outcomes, report retrieval, cancellation, and cost per target so operators detect contracts that are technically alive but semantically stuck.

## Definitions and Notation

Let $X$ be the authorized resolved target set and $a$ a common action. $B(a,X)=\{a(x)\mid x\in X\}$ denotes requested work, not a promise that every effect commits. Let $r_x$ be the outcome for target $x$. An atomic contract requires either $\forall x\in X:r_x=success$ or $\forall x\in X:r_x=not\_applied$. A best-effort contract permits mixed outcomes and must expose a report over each attempted target. Let $V$ be the selection version/snapshot; a repeatable bulk action names $V$ rather than recomputing an unspecified live query.

**Batch envelope** is a transport representation for multiple operations. **Bulk action** is a single semantic command over a set. **Selection snapshot** fixes eligible membership under declared retention. **Partial success** means some independent effects completed; it is not an HTTP status class. **Unknown outcome** means evidence cannot establish whether an effect occurred and requires reconciliation.

## Mechanisms, Invariants, or Proof Structure

1. Choose homogeneous bulk or heterogeneous batch based on actual semantic ownership.
2. Define and authorize an explicit bounded target set.
3. Declare selection timing, snapshot/live behavior, and preconditions.
4. Choose atomic, best-effort, or partitioned atomicity with its real boundary.
5. Assign durable request and per-item identities for deduplication and audit.
6. Define ordering and dependency graph rules rather than relying on array order.
7. Return bounded aggregate and per-item outcomes with safe visibility.
8. Use an operation resource when execution or reporting outlives one response.
9. Bound cost and defend embedded targets and callback surfaces.
10. Test retries, partial commits, unknown outcomes, and report recovery.

The **selection invariant** means every effect target was selected under authorization and declared timing. The **atomicity invariant** ties all-or-nothing language to a named boundary. The **outcome invariant** requires an observable disposition for each attempted item. The **retry invariant** maps same logical request to one bulk operation. The **boundedness invariant** applies to both execution and report retrieval.

## Alternatives and Trade-Offs

**Explicit IDs versus filter selection.** IDs make targets auditable and reviewable but create large payloads. Filters are compact but require a selection grammar, authorization-safe count, and snapshot policy.

**Atomic versus best effort.** Atomicity simplifies caller reasoning but limits scale and cross-system reach. Best effort scales and isolates failures but demands detailed reconciliation and idempotent retries.

**Inline report versus result resource.** Inline reports minimize requests for small batches. A result resource handles large asynchronous work, pagination, retention, and stronger report authorization.

**Server batch versus client concurrency.** Server batching can enforce shared policy and reduce network overhead. Client concurrency preserves existing endpoint semantics and can be easier to throttle. Neither is inherently more correct.

## Failure Modes and Misconceptions

“Bulk” does not mean unbounded. A `207` response does not define a generic JSON partial-success schema. Atomicity in one database does not include email or another service. A retry key does not make unknown external effects safe. An item that is absent from a report is not necessarily successful. A filter is not an authorization mechanism. Request order is not execution order. Deleting a batch record does not undo completed work.

## Worked Examples

### Example 1

A client needs to apply the same retention tag to 20 documents. One bulk action with explicit IDs shares validation and audit intent; a heterogeneous batch would add needless per-item method syntax. **Conclusion:** choose bulk for one action over many targets.

### Example 2

`POST /records:delete` omits its selection. The API rejects it rather than interpreting omission as all records. **Conclusion:** destructive target sets must be explicit.

### Example 3

A filter matches 4,000 records at preview but 4,030 at execution. A snapshot-backed selection retains the original 4,000 until expiry. **Conclusion:** snapshot identity makes a time-dependent selection reproducible.

### Example 4

Ten profile updates share one database transaction. One stale version causes rollback of all ten, and the report says no target was applied. **Conclusion:** all-or-nothing is meaningful only when its transaction boundary is real.

### Example 5

Ten notifications call an external provider; two time out with uncertain provider outcome. The report marks them `unknown`, not `failed`, and reconciliation queries provider idempotency records. **Conclusion:** unknown is a necessary outcome category.

### Example 6

An item report exposes an ID for a user outside the requester's tenant. The implementation moves authorization before selection and suppresses non-visible detail. **Conclusion:** reports obey the same visibility rules as targets.

### Example 7

Batch item B refers to output of item A, while A refers to B. Validation rejects the dependency cycle before effects. **Conclusion:** dependency graphs must be acyclic and checked before execution.

### Example 8

A retry repeats a deactivation request with the same idempotency key and selection snapshot. It returns the existing operation. Reusing the key for a new snapshot conflicts. **Conclusion:** retry identity includes selection semantics.

### Example 9

An import runs across two shards. Shard one commits; shard two fails. The API calls the result partitioned, reports both shard outcomes, and offers compensation. **Conclusion:** partitioned completion is not global atomicity.

### Example 10

A 100,000-item report cannot fit a response. The bulk operation exposes aggregate counts and a paginated outcome collection retained for 30 days. **Conclusion:** reporting needs limits and retrieval semantics of its own.

## Cross-Program Connections

[Long-Running Operations](018-long-running-operations.md) provides durable handling for costly fan-out. [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) governs selection and outcome traversal. Databases supply transaction mechanisms; distributed systems supplies retries and partitions; security engineering supplies authorization and embedded-target defenses. The API program owns the externally observable promise across them.

## References

1. R. Fielding et al., *RFC 9110: HTTP Semantics*, Standards Track, June 2022, especially Sections 15.3 and 15.5. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
2. L. Dusseault, *RFC 4918: HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)*, Standards Track, June 2007, Section 13. Used as a scoped `207 Multi-Status` example. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc4918.html
3. P. Hunt et al., *RFC 7644: System for Cross-domain Identity Management: Protocol*, Proposed Standard, September 2015, Section 3.7. Used as a scoped bulk-operation example. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc7644.html
4. J. Jena and S. Dalal, *The Idempotency-Key HTTP Header Field*, Internet-Draft draft-ietf-httpapi-idempotency-key-header-07, October 2025. Current work in progress checked 2026-09-01. https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.html

## Exercises

### Exercise 1

Classify each as bulk or heterogeneous batch: applying one label to selected files; creating a customer, then an invoice, then an unrelated support ticket; deleting all records matched by an approved saved selection.

### Exercise 2

For a best-effort bulk update over $X$, explain why the implication $\forall x\in X:r_x=success$ is not required. State what report property replaces it.

### Exercise 3

Design a retry record for a tenant-scoped bulk deactivation request selected by snapshot ID. Include the fields used to reject unsafe key reuse.

### Exercise 4

Compare a one-database atomic bulk price update with a cross-service bulk update that also sends customer email. Specify an honest outcome model for each.

### Exercise 5

Design a bounded asynchronous batch endpoint for at most 500 heterogeneous operations with optional dependencies. State validation, authorization, result, and retry rules.

## Answers to the Exercises

### Answer 1

Applying one label and deleting an approved selected set are bulk actions: one homogeneous command governs all targets. Creating a customer, invoice, and unrelated ticket is a heterogeneous batch because each item has distinct semantics and may have dependencies. The latter should not be disguised as one resource mutation.

### Answer 2

Best effort permits a mixture of success, conflict, failure, skipped, and unknown outcomes, so universal success is not its invariant. The replacement is an outcome report that gives every attempted item an identifiable disposition, with aggregate totals and a recoverable paginated result when needed.

### Answer 3

Store `(tenant, action, idempotency_key) -> (snapshot_id, normalized reason and options, collection/precondition version if used, operation_id, original response, created_at, expiry)`. A retry matching all semantic fields returns the same operation. The same key with a different snapshot, action, or normalized option is rejected as conflict; downstream per-item effects still need idempotence or reconciliation.

### Answer 4

The database update can promise all-or-nothing only for rows inside its transaction and stated isolation boundary. The email-inclusive operation cannot honestly promise the same global atomicity. It should record durable per-target stages, use idempotent email/provider identifiers, report price update and notification outcomes separately, and provide reconciliation or compensation for incomplete notifications.

### Answer 5

Validate no more than 500 items, bounded bodies and references, a directed acyclic dependency graph, allowed operation types, and stable client item IDs before effects. Authorize the envelope and every item/target using ordinary route policy. Create an operation resource with aggregate status and paginated per-item results; do not expose unauthorized targets. Bind a request idempotency key to tenant and normalized item graph, return the same operation on an identical retry, reject semantic key reuse, and require idempotent/conditional effects for safe item retries.
