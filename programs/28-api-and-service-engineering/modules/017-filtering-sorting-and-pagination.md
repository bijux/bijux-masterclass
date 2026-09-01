---
module_id: API-017
program: API & Service Engineering
level: 1
module_number: 17
title: Filtering, Sorting, and Pagination
status: complete
last_verified: 2026-09-01
---

# Filtering, Sorting, and Pagination

## One-Page Review

### Governing question

How can an API expose bounded collection traversal with precise filtering, deterministic ordering, secure continuations, and honest behavior under concurrent change?

### Essential definitions

- A **filter** is a declared predicate selecting visible members from a collection.
- A **sort key** is an ordered tuple used to compare selected members.
- A **total order** compares every pair and breaks ties uniquely within the traversal scope.
- A **page** is a bounded representation of part of an ordered result, not a stable resource snapshot by default.
- **offset pagination** selects after skipping a count; **keyset pagination** continues after the last ordered key.
- A **cursor** is opaque client state encoding or referencing continuation context.
- A **snapshot** fixes the result or read point under a declared consistency and retention model.

### Central model, mechanism, or theorem

For principal $p$, time/read point $t$, and filter $F$, selected set is $R=\{x\in M_C(t,p)\mid F(x)\}$. Define total ordering key $K(x)=(k_1(x),\ldots,k_n(x),I(x))$ ending in unique stable identity $I$. A forward keyset page after cursor key $K_c$ selects the first $L$ elements with $K(x)>K_c$ under exactly the same normalized filter, ordering, visibility, and snapshot context.

### Critical invariants

Filtering occurs after authorization semantics are defined and cannot reveal hidden fields. Sort has explicit direction, null, collation, and unique tie-break rules. Cursor binds filter, ordering, scope, principal/tenant context, and version. Limits are bounded. Continuation never trusts client-supplied internal offsets or SQL. Live traversal admits mutation effects; snapshot traversal declares cutoff and expiry. Counts state exact scope and cost.

### Common failures

Unbounded lists; dynamic SQL from raw filter names; different gateway and origin query parsing; ordering by a non-unique timestamp; offset drift under insertion/deletion; cursor tampering; exposing protected sort/filter fields; locale-dependent collation changing between pages; returning `total` that leaks hidden members; treating a cursor as a permanent bookmark; and claiming completeness for a live traversal.

### Compact example

Orders sort by `(created_at DESC, id DESC)`. First page ends at `(2026-09-01T10:00Z, 817)`. The next predicate is `created_at < timestamp OR (created_at = timestamp AND id < 817)`. A signed cursor also binds `state=open`, tenant, order definition, and expiry. Newer inserts appear before the boundary and do not shift already traversed items, but a live traversal still is not a snapshot.

### Connections

Collections supply membership and visibility; URI design supplies query encoding; Web Linking supplies typed next/previous targets. Databases supply execution mechanisms, indexes, collations, and snapshots, while the API owns public semantics and security.

## Governing Question

Which selection, order, continuation, and consistency contract lets clients traverse large authorized collections without omissions, duplicates, disclosure, or unbounded cost beyond the stated model?

## Why This Matters

“Add `filter`, `sort`, `page`, and `limit`” sounds mechanical until data changes between requests, values tie, nulls move, collation versions differ, or authorization removes rows. A database can return correct rows for each individual query while the client receives an inconsistent traversal.

RFC 3986 establishes that the query component participates in resource identification but does not define key/value semantics. RFC 8288 supplies typed links suitable for continuation. RFC 8977 provides one standardized RDAP example of sorting/paging and recommends ready-made paging links; it is calibration, not a universal API format. PostgreSQL 17 documentation records a durable SQL fact: LIMIT/OFFSET produces inconsistent subsets without predictable ordering and large offsets can be inefficient. This chapter remains datastore-neutral.

Filtering, sorting, and pagination are one contract because each changes continuation meaning. A cursor for `state=open` sorted by creation time cannot safely be reused for `state=closed` or a different tenant.

## Prerequisites and Retrieval

Retrieve collections, member identity, query components, authorization, total orders, lexicographic comparison, null and collation behavior, indexes, transactions/snapshots, cache variation, signatures, and resource limits. Recall that storage order is not an API order.

## Learning Objectives

By the end of this module, you should be able to:

1. define typed filter operators and their missing/null semantics;
2. specify a deterministic total order with stable tie-breakers;
3. compare offset, keyset, cursor, and snapshot pagination;
4. derive forward and reverse keyset predicates;
5. bind and protect continuation context;
6. state mutation, authorization, count, and expiry behavior;
7. align public ordering with indexes without exposing storage; and
8. test duplicates, omissions, parser differentials, and adversarial cost.

## Core Exposition

### Define the collection view first

Pagination partitions a selected ordered view, so begin with authoritative collection meaning and visibility. Apply tenant and authorization boundaries before client filters. A filter cannot grant access, and a count or facet must not include hidden members unless explicitly permitted.

State whether query options identify distinct cacheable resources or are request controls. Define duplicate parameter behavior, empty values, percent-decoding, maximum names/values, and canonical form consistently across gateway, signature verifier, cache, and origin.

### Design a typed filter language

Allowlist public fields and operators. Define types before comparison: decimal is not binary float, timestamps need timezone/precision, identifiers are not free text, and enumerations have explicit unknown behavior. Reject unsupported fields and operators rather than silently ignoring them.

For each field define equality, range, membership, substring/full-text meaning, case, Unicode normalization, collation, missing, null, empty, and repeated-value behavior. `status!=closed` might include or exclude missing status depending on logic; make it testable.

Keep transport syntax separate from semantic expression. Whether filter is repeated query parameters or a structured document, parse it into a bounded abstract predicate. Never interpolate raw names, operators, or values into SQL, search queries, paths, or policy engines.

Bound expression depth, terms, value lengths, set cardinality, wildcard use, regex features, and execution time. A valid filter can still force a full scan or catastrophic regular expression. Cost policy needs a stable error and safer alternative.

### Keep filtering and authorization distinct

Authorization determines the candidate universe and visible fields; filters narrow it. Filtering by a protected field can leak its value through presence, count, timing, or ordering even if the field is omitted from output. Grant filter and sort capabilities separately from field read capability where required.

Run policy at a layer that the execution plan cannot bypass. “Fetch globally, paginate, then remove forbidden rows” produces short pages, missing results, incorrect totals, and timing leaks. Incorporate visibility into selection before ordering and limits or use a proven secure view.

### Specify a total order

Pagination requires deterministic order. Sort key `(created_at DESC)` is not total when several rows share a timestamp. Append a stable unique tie-breaker such as `(created_at DESC, id DESC)`. Every requested order needs a documented tie-breaker even if the client does not spell it.

Define null placement, direction per component, collation, case, normalization, numeric/time precision, and comparison version. Database defaults differ and can change with locale or upgrades. Cursor comparison must implement the exact same normalized comparator as initial selection.

Mutable sort keys complicate traversal. If an item's score changes after page one, it can move across the cursor boundary and appear twice or be missed. Use snapshots when completeness matters, choose less mutable ordering, or document live semantics.

### Offset pagination

Offset pagination requests a limit after skipping $O$ visible ordered results. It supports arbitrary page numbers and is easy to expose. Without a total order, pages are arbitrary. Under concurrent insert or delete before the offset, later pages shift, causing duplicates or omissions.

Large offsets can be expensive because the engine may still locate and skip preceding candidates. Count-plus-offset can add another expensive and consistency-sensitive query. Offset is reasonable for small, stable, human-browsed sets where page-number navigation matters and drift is acceptable.

Never let page number arithmetic overflow or create negative/unbounded offsets. Cap limit and offset, and state whether out-of-range returns an empty page or error.

### Keyset pagination

Keyset pagination continues from ordered values of the last delivered member. For ascending tuple $K$, next page uses $K(x)>K_c$; descending uses the corresponding reversed comparison. Mixed directions require an explicit lexicographic predicate, not one blanket greater-than sign.

Keyset usually scales with an index aligned to filter and order and resists shifts from inserts before the cursor. It cannot naturally jump to page 900 and still experiences changes to membership or sort keys. Deletion of the boundary item is harmless when cursor contains values; insertion after the boundary can appear in later pages under live semantics.

Do not expose raw database tuple IDs, shard coordinates, or index internals as the public cursor. Encode stable public ordering values or store continuation server-side.

### Cursor design

A cursor can be self-contained and integrity-protected or opaque reference to server state. Bind normalized filter, sort fields/directions, tie-breaker, tenant/principal scope, authorization-policy or data-version context where needed, snapshot/read point, page-size policy, schema version, issue time, and expiry.

Authenticate the cursor to prevent tampering. Encryption is needed only if contents are sensitive; opaque-looking base64 provides neither integrity nor confidentiality. Rotate signing keys with overlap, identify cursor version/key, and reject unknown, expired, wrong-scope, or malformed tokens consistently.

Treat cursor as a continuation capability, not authorization. Recheck current access. Avoid embedding personal data, raw queries, or indefinite snapshot handles. Cursor errors should tell clients whether to restart without exposing protected internals.

### Live versus snapshot traversal

Live traversal evaluates current state on each request. Define expected effects of insert, delete, authorization change, and sort-key mutation. Keyset pagination offers useful monotonic boundary behavior but does not prove each qualifying member appears exactly once.

Snapshot traversal fixes membership and ordering at a read point or materialized result. It supports reproducibility but consumes storage/transaction resources and needs identity, authorization, retention, expiry, correction, and maximum traversal time. Long-lived database snapshots can impede cleanup and are often unsafe as public cursors.

If exact export is needed, create an asynchronous snapshot/export resource rather than holding a request transaction across hours. State cutoff, completeness, checksum, and unavailable-member policy.

### Counts, facets, and page metadata

Exact `total` can be expensive, stale, or sensitive. Define whether count is exact, estimated, visible-only, snapshot-bound, capped, or omitted. Do not label an estimate as exact. A boolean `has_more` may be obtained by fetching one extra visible row without counting the universe.

Return continuation links or tokens, applied filter/sort canonical form, page size, and snapshot metadata. Page numbers are meaningful only for offset/page pagination. Avoid echoing unsanitized query text in links or errors.

RFC 8288 link relations can communicate navigation; clients should use supplied `next` targets rather than reconstruct internal query rules. Preserve authentication policy and avoid placing secrets in those targets.

### Align execution and contract

An index should align equality prefixes, range conditions, and ordering, but public semantics must not depend on a particular plan. Measure scanned-to-returned ratio, latency distributions, timeout/cancellation, cursor failures, and count cost using bounded labels.

Test against the actual datastore collation, null ordering, timestamp precision, and transaction model. A cursor produced before a collation or schema upgrade may be invalid; version it and either preserve comparator behavior or require restart.

Cache keys must include every query dimension that affects selected representation and authorization. Canonicalizing query order is safe only if the API defines equivalent semantics, especially for repeated parameters.

### Test traversal properties

Use fixtures with equal primary sort keys, nulls, Unicode variants, minimum/maximum values, duplicate relationship occurrences, and mutable visibility. Verify forward and reverse traversal, empty/single/exact-boundary/last pages, invalid cursors, and limit bounds.

Inject inserts, deletes, sort-key updates, authorization revocation, clock skew, replica lag, and cursor expiry between pages. Compare observed behavior with the declared live or snapshot model; do not demand snapshot properties from live traversal.

## Definitions and Notation

Let authorized membership be $M_C(t,p)$ and filter predicate $F$. Result $R=\{x\in M_C(t,p)\mid F(x)\}$. Total key $K(x)=(k_1(x),\ldots,k_n(x),I(x))$ uses stable unique $I$. For ascending order, forward continuation after $K_c$ is $\{x\in R\mid K(x)>K_c\}$, limited to $L$. Mixed directions expand into lexicographic disjunctions matching the comparator.

**Collation** defines string comparison. **Tie-breaker** completes otherwise equal keys. **Continuation context** is every dimension required to interpret the next page. **Cursor integrity** prevents undetected modification. **Traversal completeness** means every member in a declared fixed scope appears according to its occurrence model; it is not implied by successful live pages.

## Mechanisms, Invariants, or Proof Structure

1. Define authorized collection scope and filter grammar.
2. Type, normalize, bound, and authorize every filter/sort field and operator.
3. Define total ordering with null, collation, direction, and stable identity.
4. Choose offset, keyset, or snapshot based on navigation and consistency needs.
5. Bind cursor to canonical filter, order, scope, version, read model, and expiry.
6. Protect cursor integrity and re-evaluate authorization.
7. Define mutation, replica, count, and error semantics.
8. Align indexes and resource limits without exposing storage contracts.
9. Return ready continuation controls and bounded metadata.
10. Test boundary fixtures and inter-page concurrent events.

The **visibility invariant** filters only within authorized scope. The **total-order invariant** prevents tie ambiguity. The **context invariant** makes a cursor usable only with its original semantics. The **boundedness invariant** limits cost. The **evidence invariant** distinguishes live traversal from snapshot completeness.

## Alternatives and Trade-Offs

**Offset versus keyset.** Offset supports page numbers but drifts under mutation and degrades at depth. Keyset scales and resists prefix shifts but needs a total order and cannot jump arbitrarily.

**Client-visible versus opaque cursor.** Visible keys ease debugging but expose schema and sensitive values. Opaque signed tokens decouple clients but require versioning and key rotation. Neither replaces authorization.

**Live versus snapshot.** Live views are current and cheap but do not guarantee exact traversal. Snapshots are reproducible but require resource governance and bounded retention.

**Exact count versus no/estimated count.** Exact totals aid navigation but can be expensive and leaky. `has_more`, estimates, capped counts, or separate count operations can better match scale and privacy.

## Failure Modes and Misconceptions

LIMIT without total order is not deterministic. A unique ID tie-breaker is part of public order even when implicit. Offset does not denote stable membership. Keyset is not automatically snapshot-safe. Base64 is not a signature. Query parsing is not universal form decoding. Sorting by a hidden field can leak it. Exact totals can be both costly and sensitive. Database index order is not a durable API contract.

## Worked Examples

### Example 1

Three orders share timestamp 10:00. Sorting only by timestamp lets them swap between requests. Adding unique ID as descending tie-breaker yields one total order. **Conclusion:** pagination requires deterministic tie resolution.

### Example 2

Page one uses offset 0, limit 2. A new leading item arrives before page two uses offset 2, so the old second item repeats. **Conclusion:** offset shifts under prefix insertion.

### Example 3

Keyset page ends at `(10:00,817)` descending. Next predicate selects earlier timestamps or equal timestamp with ID below 817. A newer insert stays before the boundary. **Conclusion:** lexicographic continuation avoids offset prefix drift.

### Example 4

Cursor for tenant A is replayed against tenant B. Because token binds tenant and principal scope, verification rejects it before query execution. **Conclusion:** continuation context includes authorization scope.

### Example 5

A base64 cursor contains raw email and database row ID. It leaks personal data and topology and can be edited. A signed opaque version contains stable public key or server reference. **Conclusion:** opacity, integrity, and confidentiality are distinct.

### Example 6

Contractor sees 4 incidents but `total=900` counts all tenants. The count discloses protected volume. Query applies visibility before an explicitly visible-only count. **Conclusion:** aggregates obey authorization.

### Example 7

Item score changes after page one and moves behind the cursor, appearing again. Live contract permits movement; an audit client uses a snapshot. **Conclusion:** mutable sort keys defeat exactly-once live traversal.

### Example 8

Gateway treats duplicate `status` parameters as first-wins; origin uses last-wins. Signature covers `open`, execution uses `closed`. A shared canonical parser rejects ambiguous duplicates. **Conclusion:** parser agreement is a security invariant.

### Example 9

After collation upgrade, `Å` and `A` compare differently and old cursors resume at the wrong boundary. Cursor version identifies comparator version and requires restart. **Conclusion:** collation belongs to continuation semantics.

### Example 10

An exact count scans 200 million rows before returning a 20-item page. The API offers `has_more` and asynchronous aggregate reporting. **Conclusion:** metadata must be bounded like result data.

## Cross-Program Connections

[Collections and Individual Resources](014-collections-and-individual-resources.md) supplies membership and visibility; [URI Design](013-uri-design.md) supplies query processing. Caching, authorization, databases, distributed consistency, and observability constrain implementations. API-018 uses operation resources for long exports.

## References

1. T. Berners-Lee, R. Fielding, and L. Masinter, *RFC 3986: URI Generic Syntax*, Internet Standard 66, January 2005, Section 3.4. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc3986.html
2. M. Nottingham, *RFC 8288: Web Linking*, Standards Track, October 2017. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc8288.html
3. M. Loffredo et al., *RFC 8977: RDAP Query Parameters for Result Sorting and Paging*, Standards Track, January 2021. Used as a scoped protocol example. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc8977.html
4. PostgreSQL Global Development Group, *PostgreSQL 17 Documentation: LIMIT and OFFSET*, current maintained documentation checked 2026-09-01. https://www.postgresql.org/docs/17/queries-limit.html

## Exercises

### Exercise 1

Define a total order for tasks sorted by nullable due date ascending, priority descending, and ID ascending. State null placement and tie-break behavior.

### Exercise 2

Derive the next-page predicate after key `(due=2026-09-10, priority=3, id=90)` for that mixed-direction order, assuming non-null due dates.

### Exercise 3

Diagnose a cursor containing only database offset while clients may change tenant, filter, sort, and page size between requests.

### Exercise 4

Compare offset, keyset, and snapshot pagination for a small admin table, a high-write event stream, and a regulated export.

### Exercise 5

Design traversal for disaster-response incidents where visibility changes as teams rotate, connectivity is intermittent, and exact audit export is later required.

## Answers to the Exercises

### Answer 1

Use key `(due_is_null ASC, due ASC, priority DESC, id ASC)` where non-null has `due_is_null=0` and null has 1, placing nulls last. Equal due dates compare higher priority first; equal priority compares unique ID ascending. ID completes a total order. The exact null and collation policy is part of the contract.

### Answer 2

For ascending due, then descending priority, then ascending ID, select `due > 2026-09-10`, or equal due with `priority < 3`, or equal due and priority with `id > 90`. The second comparison reverses because priority is descending. Null-tail continuation needs additional explicit branches once the cursor reaches null due dates.

### Answer 3

Offset alone lacks filter, order, tenant/principal scope, policy version, comparator, snapshot/live mode, limit policy, and expiry. Reuse can skip, duplicate, disclose, or execute an expensive unrelated query. Bind normalized context in a signed versioned token or server-side reference, reauthorize every request, cap limit, reject mismatches, and provide a restart path.

### Answer 4

Offset is acceptable for a small, slowly changing admin table when page numbers matter and drift is tolerable. A high-write stream benefits from keyset order on immutable event time plus ID, with documented live semantics. A regulated export needs an identified snapshot or asynchronous materialization with cutoff, completeness, checksum, retention, and authorization. No one mechanism optimizes all three.

### Answer 5

Operational browsing uses signed keyset cursors bound to incident filter, severity/time/ID total order, team scope, comparator version, and short expiry; every request rechecks current visibility. Intermittent clients can restart and reconcile by stable incident ID rather than assuming cursor permanence. Visibility changes may cause live omissions and are stated. Audit export creates an authorized snapshot resource at a declared cutoff, records policy scope and membership evidence, retains checksums and corrections, and never infers completeness from live pages.
