---
module_id: LSDS-018
program: Large-Scale Data Systems Engineering
level: 1
module_number: 18
title: Consistency of Listings and Metadata
status: complete
last_verified: 2026-09-03
---

# Consistency of Listings and Metadata

## One-Page Review

### Governing question

How should a large-scale storage client reason about direct object reads, metadata reads, prefix listings, multi-page enumeration, versions, caches, replicas, and secondary indexes when each surface can have a different consistency and concurrency contract?

### Essential definitions

- **Read-after-write consistency** means a read begun after a successful write returns that write or a later value under the named scope.
- **Listing consistency** defines which namespace mutations a LIST operation must reflect and how concurrent mutations affect enumeration.
- A **linearization point** is the logical instant at which one operation takes effect in a legal sequential history.
- A **snapshot listing** enumerates one namespace state fixed at a declared revision or time.
- A **live listing** may evaluate successive pages against changing namespace state.
- A **continuation token** is opaque service state used to continue one query; it is not generally an object key, revision, or portable bookmark.
- **Object metadata** describes one object/version; **namespace metadata** maps names to versions and supports discovery.
- A **secondary index** maps derived attributes such as tags to object identities and can lag the authoritative object namespace.
- **Reconciliation** compares an authoritative set with derived state and repairs missing, extra, or mismatched records.

### Central model, mechanism, or theorem

Represent a namespace state at revision `r` as `N_r: key -> (version, metadata)`. A direct read names one key, while `LIST(q, token)` returns a bounded page matching query `q`. Strong read-after-write or strong listing means mutations completed before an operation begins are reflected according to the service scope. It does not by itself prove that every page of a long scan shares one `r`.

A complete inventory therefore needs one of three proofs: a provider snapshot/revision held across pages; an immutable manifest that names exact object versions; or a live-scan protocol with change capture and reconciliation. Treat each page token as opaque, preserve the entire query and authority context, detect token expiry/restart, deduplicate by exact object identity, and never use a mutable listing alone as a multi-object commit record.

### Critical invariants

- Every observation records endpoint, account, bucket/container, query, API version, authorization scope, and object version identity.
- A direct HEAD/GET result and a LIST row are not assumed to be one atomic observation.
- Pagination keeps query parameters and scope stable and uses the returned token unchanged.
- Scan correctness states whether it means snapshot membership, at-least-once discovery, eventual convergence, or a bounded staleness objective.
- Object generations/versions and metadata revisions are distinguished where the API distinguishes them.
- Prefixes and delimiter groups remain query projections, not transactional directories.
- Caches, geo-secondary endpoints, inventory exports, event streams, and tag indexes have separately measured freshness.
- Destructive action is authorized from an immutable manifest or revalidated exact version, never an old LIST row alone.
- Reconciliation is idempotent, version-aware, observable, and safe under retry.

### Common failures

Frequent failures are repeating historical eventual-consistency folklore after contracts changed, assuming strong per-request LIST gives a scan-wide snapshot, parsing continuation tokens as keys, changing filters between pages, ignoring empty pages with another token, using timestamps as version identities, joining LIST and HEAD without detecting replacement, treating tags as immediately searchable, reading an asynchronous geo-secondary as the primary, treating cache freshness as origin consistency, using prefix discovery as dataset commit, and deleting objects from a stale inventory without version preconditions.

### Compact example

A live lexicographic scan reads page `a,c`. Before its next request, another writer inserts `b,d,f` and deletes `e`. Continuing strictly after `c` can return `d,f`, then `g`: the scan misses final key `b`, omits deleted initial key `e`, and includes new keys `d,f`. Every page can be internally valid while the combined result equals neither the initial nor final namespace. A snapshot token, immutable manifest, or change-log reconciliation is required if the application needs a point-in-time set.

### Connections

[LSDS-012](012-metadata-servers-and-namespace.md) supplies namespace state and snapshots. [LSDS-016](016-object-storage-semantics.md) supplies object versions and conditional reads. [LSDS-017](017-multipart-upload-and-commit.md) supplies commit visibility and ambiguous completion. [LSDS-019](../ROADMAP.md) applies listing cost to small-file pathologies.

## Governing Question

Listing looks like a read of a directory, but distributed object namespaces rarely behave like one local directory iterator. The service may shard names, merge results from metadata partitions, cap page size, project delimiter prefixes, omit versions by default, and expose different endpoints for primary and replicated state. An SDK then wraps opaque continuation state in an iterator that makes multiple requests over seconds or hours.

The first question is not simply “is LIST strongly consistent?” It is: consistent with what operations, within which resource and endpoint, at what request boundary, under what concurrent history, and across how many pages? A provider can promise that a LIST begun after a successful PUT contains the object while making no claim that page one and page one thousand describe one frozen revision.

Metadata complicates the answer. A key's bytes, system properties, custom metadata, access policy, tags, retention state, and secondary-index entries can be updated through different operations. A list response may project only a subset. An object-specific HEAD can race replacement after the list row was emitted. A public cache or asynchronous disaster-recovery endpoint can return older state even when the primary namespace is strongly consistent.

The governing question is how to define the observation the application actually needs and then choose a protocol that proves it. Discovery, monitoring, billing inventory, garbage collection, dataset publication, migration, and destructive cleanup require different guarantees.

## Why This Matters

Large namespaces are often the source for batch planning. A job lists an input prefix, creates one task per key, and declares success when every task finishes. If the enumeration is a hybrid of revisions, the job can silently omit input, process replacement bytes under an old name, or include files not part of the intended dataset.

Operational systems also use listing for backups, migrations, retention enforcement, orphan cleanup, quota accounting, search, and incident response. Missing one object during a backup affects recoverability. Deleting one replacement version from a stale row affects correctness. Treating a delayed tag index as complete can violate policy or create false evidence of compliance.

Provider semantics are current product contracts, not timeless folklore. Amazon S3 and Google Cloud Storage currently document strong object listing for their named primary services, while some bucket configuration, access-policy propagation, caches, secondary indexes, and geo-secondary reads have different behavior. Compatible gateways and older deployments can differ again. Engineering must record the exact surface and retrieval date.

Scale turns minor ambiguity into a recurring event. A billion-key scan spans many pages and concurrent mutations. Tokens expire, workers restart, permissions change, partitions rebalance, and throttling extends scan duration. Correctness comes from explicit identities, revision boundaries, durable checkpoints, change capture, and reconciliation—not from an iterator that happened to work in a quiet test bucket.

## Prerequisites and Retrieval

Recall partitioning and ordered ranges from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), distributed failure assumptions from [LSDS-009](009-cluster-failure-assumptions.md), and scale/resource accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve metadata ownership, revisions, rename, snapshots, and garbage collection from [LSDS-012](012-metadata-servers-and-namespace.md); read/write acknowledgement and stale-replica behavior from [LSDS-014](014-read-and-write-pipelines.md); version, validator, prefix, cache, and lifecycle semantics from [LSDS-016](016-object-storage-semantics.md); and final visibility plus incomplete uploads from [LSDS-017](017-multipart-upload-and-commit.md).

You should understand partial orders, real-time precedence, linearizability, snapshot isolation, opaque tokens, lexicographic ordering, set difference, idempotency, object versions, conditional requests, caches, asynchronous replication, access control, and durable checkpoints.

## Learning Objectives

After completing this module, you should be able to:

- distinguish per-request strong listing from scan-wide snapshot enumeration;
- specify read-after-create, read-after-update, read-after-delete, and concurrent-write cases;
- separate object data, object metadata, namespace metadata, policy, and secondary indexes;
- use continuation tokens without inferring undocumented structure;
- reason about inserts, deletes, replacements, and permission changes between pages;
- bind LIST rows and later HEAD/GET requests to exact object versions;
- choose snapshot, immutable manifest, live scan plus change capture, or periodic reconciliation;
- design durable, restartable, partitioned inventory scans;
- quantify page/request cost, scan duration, mutation exposure, and reconciliation lag;
- prevent stale discovery from authorizing unsafe deletion or publication;
- test primary, cache, replica, index, and inventory freshness independently; and
- state governance evidence and residual uncertainty precisely.

## Core Exposition

### Consistency vocabulary

Sequential consistency preserves some process order but not necessarily real-time order. Linearizability adds the requirement that if operation A completes before operation B begins, A precedes B in the legal sequential history. Read-after-write is a narrower client-visible property and must name whose write, which operation type, and which endpoint.

Eventual consistency says replicas converge when updates stop, but gives no useful completion time without a bound or observed service objective. Bounded staleness adds a time or version limit. Monotonic reads prevent one session from moving backward. Read-your-writes lets a client observe its own completed mutations. None of these phrases should be used without scope.

“Strong consistency” is also insufficient shorthand for a workflow. It may apply to individual object PUT, GET, HEAD, DELETE, and LIST requests at a primary endpoint while configuration propagation, permissions, caches, cross-region replicas, search indexes, and batch inventory remain asynchronous.

### Operation histories and real-time edges

Model each operation with invocation and response times. If PUT `p` returns success before LIST `l` begins, then a read-after-write listing guarantee can require `l` to reflect `p`. If `p` overlaps `l`, either ordering can be legal. A client must not claim anomaly merely because an overlapping write is absent.

The same reasoning applies to delete and metadata update. Record request IDs, server versions, client monotonic timestamps, endpoint, and response status. Wall-clock timestamps from different machines do not establish a precise real-time edge unless clock uncertainty is controlled.

A timeout creates no completed-success edge. The write may be absent, committed, or still resolving. Query exact object identity or retry under idempotency/precondition semantics before using LIST absence as evidence.

### Per-request listing versus whole-scan snapshot

One LIST request can be linearized at an instant and return a bounded page. The next request can be linearized later. Unless the token pins a revision or the contract promises snapshot pagination, concatenating pages creates a traversal through changing states rather than one atomic namespace image.

Concurrent insertion behind the cursor can be missed. Insertion ahead can be included. Deletion ahead can vanish. Replacement can yield an old list row followed by new HEAD data. Rebalancing and retry can also produce duplicates under APIs that specify at-least-once page behavior.

Define scan semantics explicitly. “All keys existing at revision `r` exactly once” requires a snapshot. “Eventually discover every stable key” can use repeated live scans with deduplication. “Continuously project current state” is better served by a change stream plus checkpoints and reconciliation.

### Continuation tokens

A continuation token is returned service state for resuming the same query. It may encode a last name/generation, partition cursor, snapshot handle, or signed internal state, but clients must treat it as opaque unless the API documents otherwise.

Persist token, full query, bucket/container identity, endpoint, API version, authorization principal/scope, requested projection, page size, and scan generation together. Reusing a token with another prefix, delimiter, version mode, endpoint, or credential context can fail or change meaning.

An empty page can still carry another token. A page shorter than requested need not be final. Stop only under the documented terminal signal. Bound repeated-token and no-progress loops, and preserve raw responses/request IDs for diagnosis.

Tokens can expire or become invalid after configuration changes. Restart policy must state whether to abandon the earlier scan, restart from the beginning with exact-identity deduplication, or resume from an application range boundary under documented ordering. A lexical start key is not equivalent to an opaque token.

### Ordering and namespace projections

Some APIs order ordinary bucket results lexicographically; other bucket types do not. Delimiter grouping returns common prefixes as a projection, not stored parent objects. Key encoding, normalization, byte ordering, and locale rules matter.

Never partition work by assumed lexical order unless the exact bucket/API contract provides it. Hash-prefix layouts distribute load but destroy human chronological traversal. Directory-bucket or hierarchical namespace features may define different rules from flat buckets.

Listings often omit noncurrent versions, delete markers, snapshots, soft-deleted records, uncommitted blocks, and multipart candidate state unless explicitly requested through the right API. “Bucket is empty” is meaningless without naming these populations.

### Object and metadata identity

An object value has a key and version/generation. Metadata may share that version or have its own revision counter. Google Cloud Storage, for example, distinguishes generation from metageneration. A metadata-only update need not create new data bytes, yet concurrent metadata writers still need a precondition.

LIST commonly returns selected fields such as key, size, modification time, storage class, and validator. HEAD/GET can return richer current metadata. If the key changes between LIST and HEAD, the two responses may describe different versions. Send a version-specific request or a condition derived from the list row where supported.

Opaque ETags, timestamps, sizes, and tag counts are not universal version identities. Record the provider's exact generation/version field. When no immutable identifier is available, state the resulting uncertainty and use an application manifest or checksum.

### Metadata updates and read-modify-write

Changing content type, cache control, custom metadata, tags, retention, or tier can involve different APIs. Some replace the entire metadata map, so a stale read-modify-write can erase another client's fields. Use metadata-specific revision preconditions where available.

Distinguish user metadata stored with the object from derived catalog records and search tags. A successful metadata update can be strongly visible through HEAD while a tag query remains stale because it uses an asynchronously maintained secondary index.

Schema metadata also needs ownership. Reserve namespaces, validate size and encoding limits, avoid secrets in cleartext headers/logs, and version application fields. Metadata is data for privacy, retention, and residency analysis.

### Secondary indexes and tag queries

A secondary index maps a predicate such as `project=x AND retention=expired` to candidate object identities. Updating object tags and reading the object may be strongly consistent while querying the index is eventual. The query result is discovery evidence, not necessarily authority.

For destructive workflows, fetch each candidate's exact current version and metadata, reevaluate policy, and delete conditionally. For search and dashboards, expose index watermark or lag and tolerate false positives/negatives according to product requirements.

Backfill and repair compare the authoritative namespace/object state with index state. Index entries should carry object version and indexing revision so an older asynchronous update cannot overwrite a newer projection.

### Caches and intermediaries

Public caches and CDNs can serve an earlier representation until freshness expires or invalidation completes. This does not contradict a strong origin contract. Test the origin endpoint and cache path separately, and record cache status, Age, ETag/version, and Cache-Control.

Mutable keys with long cache lifetimes make freshness difficult. Prefer immutable versioned asset names and a short-lived or conditionally fetched pointer. Authorization changes can be especially dangerous if a previously public object remains cached.

Client SDK caches, DNS, proxies, gateways, filesystem adapters, and metadata catalogs are additional layers. A system claim is only as strong as the actual request path.

### Replication and alternate endpoints

Primary-region writes can be acknowledged before asynchronous replication to a disaster-recovery region. A secondary read may therefore lag or observe transactions in a different order under its documented contract. Record endpoint role and last-synchronization evidence.

Failover changes the authority boundary. Recovery-point objective describes tolerated data loss; recovery-time objective describes service restoration. Neither implies a globally linearizable namespace across primary and secondary endpoints.

Cross-region replication can copy object bytes, metadata, tags, deletes, and retention under different rules and delays. Reconcile each population and do not infer replication completion from destination key presence alone.

### Immutable manifests as dataset commits

A data job should publish immutable objects under unique names, validate their exact versions and digests, then conditionally publish one small manifest or pointer. Consumers read the manifest version and fetch only named object versions. Prefix LIST becomes discovery or audit, not the commit boundary.

The manifest records schema, partition identity, ordered/unordered membership, length, digest, provenance, and producer operation. A successor manifest can add or remove members atomically at the pointer level without renaming thousands of objects.

Garbage collection traces reachability from retained manifest versions and revalidates exact object versions before deletion. This separates logical publication from physical cleanup.

### Snapshot enumeration

If the provider or an external catalog offers a snapshot/revision, bind all pages to it. Persist snapshot identity and expiry, and verify page tokens belong to the same snapshot and query. Snapshot isolation fixes membership but can still require exact version reads for object bytes.

A metadata database can maintain its own transactional catalog of objects. Then the catalog, not object LIST, defines dataset membership. The ingestion protocol must atomically or recoverably connect object creation with catalog commit, usually through an outbox, intent record, or reconciler.

Provider inventory exports can provide bulk point-in-time or scheduled views. They reduce request pressure but are delayed and may omit fields or populations. Record inventory generation time, coverage, schema, delivery completeness, and checksum.

### Live scan plus change capture

When snapshots are unavailable, combine a live baseline scan with an ordered change stream. Record change-stream position before the scan, enumerate and upsert exact version identities, then consume changes from that position through a watermark after scan completion.

This only works if retention covers the scan duration plus outages, events are replayable or deduplicable, and creation/deletion/version identity is sufficient. Event delivery can be at-least-once and out of order; consumers need idempotent version-aware application.

Periodically perform a full authoritative reconciliation because event loss, permission errors, schema bugs, and retention gaps occur. A change stream accelerates convergence; it does not eliminate audit.

### Reconciliation algebra

Let authoritative snapshot set `A` and derived set `D` contain `(key,version)` identities. Missing entries are `A - D`; extra entries are `D - A`; keys present with different versions form the mismatch relation. Counts alone cannot detect compensating errors.

Apply repair with compare-and-set rules. Upsert authoritative version only if it is newer under provider semantics. Delete an index entry only if its recorded source version remains absent or superseded in the authoritative view. A repeated repair must converge without duplicating side effects.

For live sets without a shared snapshot, partition comparisons by captured revision or use repeated passes until a declared quiet-window/watermark condition. Report residual uncertainty rather than manufacturing exactness.

### Restartable and parallel scans

Persist a scan record containing identity, purpose, query, authority scope, started time, token/range checkpoints, page request IDs, item counts, exact-identity deduplication state, errors, and completion state. Commit page output and its next checkpoint atomically so crash/retry cannot create an invisible gap.

Parallelize only along stable disjoint ranges or provider-supported partitions. Prefixes can overlap through delimiters or encoding mistakes. Prove coverage and non-overlap, and assign each range an independent durable cursor.

Use bounded queues and backpressure. Listing faster than consumers can persist results merely moves failure into memory. Rate-limit requests, honor throttling, and measure scan age rather than only page throughput.

### Cost and freshness accounting

For `K` returned keys and effective page capacity `P`, a quiet full scan needs at least `ceil(K/P)` page requests, but filtering, delimiter prefixes, permissions, empty pages, retries, and service caps can increase it. Duration is governed by request latency, throttling, downstream processing, and parallel range safety.

If mutations arrive at rate `lambda` per second during scan duration `T`, the expected number of mutations overlapping the scan is `lambda*T` under a stationary approximation. This is exposure, not an exact error count: placement relative to cursors and contract determines omissions/duplicates.

Track requests, pages, keys, bytes of metadata, retries, throttles, token restarts, duplicate identities, version mismatches, scan duration, oldest observation age, event lag, index lag, inventory age, and reconciliation deltas.

### Safe destructive workflows

Never delete solely because a key appeared in an old LIST or failed to appear in one live scan. Establish an immutable candidate manifest, policy version, retention/hold state, minimum age, ownership, and approval. Re-HEAD the exact version and issue a version-specific conditional delete.

Use quarantine or soft delete where recovery requirements justify it. Rate-limit deletion, retain audit records, sample canaries, and stop on unexpected mismatch rates. A stale index can propose candidates but cannot waive authoritative checks.

For regulated or research data, name data owners, records/privacy/legal reviewers, participant/community representation where relevant, security/key management, accessibility, operations, and independent assurance. Technical consistency does not establish lawful or ethical disposition.

### Testing consistency boundaries

Create histories with known nonoverlapping and overlapping operations. After a write response, issue LIST, HEAD, GET, tag query, cache request, primary read, and replica read separately. Assert only the documented contract for each surface.

Exercise concurrent insert before/after cursor, delete before/after cursor, same-key replacement, metadata-only update, page size one, empty continuation page, repeated token, invalid/expired token, permission change, throttling, SDK retry, worker crash, endpoint failover, cache expiry, and index backlog.

At scale, inject mutations during long scans and compare with a snapshot or operation log. Measure empirical lag distributions without upgrading them into universal guarantees. Preserve product/API versions and dates with results.

## Definitions and Notation

- `N_r` is namespace mapping at revision `r`.
- `N_r(k)=(v,m)` maps key `k` to object version `v` and metadata revision/value `m`.
- `q=(prefix,delimiter,versions,projection,filters)` is an immutable listing query.
- `page(q,t)` returns items and next opaque token from token `t`.
- `S` is the multiset emitted by a complete scan attempt.
- `A_r` is the authoritative `(key,version)` set at revision `r`.
- `D` is a derived catalog, index, or inventory set.
- `P` is effective items per page and `K` is result cardinality.
- `T` is scan duration and `lambda` is mutation rate per second.
- `w` is an ordered change-stream watermark.
- `L_index` and `L_replica` are observed secondary-index and replica lag.
- `M=A_r-D`, `E=D-A_r`, and `X` are missing, extra, and version-mismatch sets.

A point lookup result is `R(k)` and a projected listing row is `L(k)`. Equality of keys does not prove `R(k)` and `L(k)` describe the same version. Bind both to `v`, or treat their join as a concurrent observation with explicit validation.

For a quiescent listing with maximum `P` results per response, request lower bound is `ceil(K/P)`. If a service can return fewer than `P`, only terminal-token semantics establish completion.

## Mechanisms, Invariants, or Proof Structure

Use this audit for any workflow driven by storage listings:

1. Name the exact provider, service, resource type, endpoint, API version, and consistency contract.
2. Define the desired result: snapshot, discovery, convergence, or bounded freshness.
3. Record write/read real-time edges and ambiguous operations separately.
4. Freeze query, authority, projection, version mode, and token with one scan identity.
5. Bind every row to exact object version or record the inability to do so.
6. Choose snapshot, immutable manifest, or live scan plus change capture/reconciliation.
7. Make page output and cursor checkpoint atomic and retry-idempotent.
8. Treat cache, replica, inventory, event stream, and secondary index as separate surfaces.
9. Revalidate exact current version before mutation, especially deletion.
10. Measure lag, restart, mismatch, and residual uncertainty under concurrency.

The fixture models lexicographic keyset pagination over a live namespace. It demonstrates a valid hybrid traversal, not any named provider's undocumented behavior.

<!-- bijux-verify: {"id":"live-list-pagination","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"page1=('a', 'c') cursor=c\npage2=('d', 'f') cursor=f\npage3=('g',) cursor=g\nscan=('a', 'c', 'd', 'f', 'g')\ninitial=('a', 'c', 'e', 'g')\nfinal=('a', 'b', 'c', 'd', 'f', 'g')\nmissing_from_final=('b',) new_since_initial=('d', 'f') snapshot_equal=False\n","stderr":""}} -->
```python
def page(keys: set[str], after: str | None, limit: int) -> tuple[str, ...]:
    ordered = sorted(key for key in keys if after is None or key > after)
    return tuple(ordered[:limit])


namespace = {"a", "c", "e", "g"}
initial = tuple(sorted(namespace))

first = page(namespace, None, 2)
cursor = first[-1]
print(f"page1={first} cursor={cursor}")

# These mutations occur after page one. The model intentionally has no snapshot.
namespace.update({"b", "d", "f"})
namespace -= {"e"}

second = page(namespace, cursor, 2)
cursor = second[-1]
print(f"page2={second} cursor={cursor}")

third = page(namespace, cursor, 2)
cursor = third[-1]
print(f"page3={third} cursor={cursor}")

scan = first + second + third
final = tuple(sorted(namespace))
missing = tuple(sorted(set(final) - set(scan)))
new_since_initial = tuple(sorted(set(scan) - set(initial)))
snapshot_equal = scan == initial or scan == final

print(f"scan={scan}")
print(f"initial={initial}")
print(f"final={final}")
print(
    f"missing_from_final={missing} new_since_initial={new_since_initial} "
    f"snapshot_equal={snapshot_equal}"
)
```

The insert `b` falls behind the cursor and is missed; inserts `d,f` fall ahead and are included; deleted `e` disappears before its page. The emitted set equals neither endpoint snapshot. A provider may define stronger or different pagination semantics, so production behavior comes from its exact contract and tests.

Proof obligations differ by target. Snapshot inventory proves fixed revision and full token exhaustion. Manifest consumption proves exact named versions. Continuous projection proves checkpointed change application plus reconciliation. A successful iterator loop alone proves none of them.

## Alternatives and Trade-Offs

A provider LIST is simple and authoritative for its documented surface. It can be expensive and long-running at billions of keys. Scheduled inventory exports reduce request load and add delivery delay.

Snapshot enumeration gives clean membership and consumes snapshot/catalog capacity. Live scans need no snapshot support and require deduplication, change capture, or repeated reconciliation for stronger outcomes.

Immutable manifests make dataset reads reproducible and shift responsibility to producers. Prefix discovery is flexible and makes membership implicit. A transactional external catalog supports rich queries and introduces dual-write/recovery complexity.

Lexicographic keyset pagination scales better than numeric offset in mutable ordered sets, but inserts behind a live cursor can be missed without snapshot/change capture. Opaque provider tokens preserve service freedom and cannot be synthesized for arbitrary partitioning.

Event streams provide low-latency updates and require retention, replay, ordering, deduplication, and gap detection. Periodic scans converge slowly and detect drift that events miss. Mature systems use both.

Secondary tags enable search without scanning all objects and can lag. An authoritative database provides explicit index transactions and must stay connected to object commit through recoverable workflow state.

Caching lowers latency and origin load while making mutable-name freshness dependent on cache policy. Immutable versioned names make caching safer at the cost of pointer/version management.

Parallel prefix/range scans reduce wall time and increase request bursts, checkpoint count, merge complexity, and coverage risk. Start with proven disjoint boundaries and bounded consumers.

## Failure Modes and Misconceptions

- **“Object stores are eventually consistent.”** Verify the current exact service; major primary services document stronger semantics for many object operations.
- **“Strong LIST means my entire paginated scan is a snapshot.”** Per-request visibility and cross-page snapshot isolation are different claims.
- **“A continuation token is the last key.”** It is opaque unless the contract says otherwise.
- **“A short or empty page ends enumeration.”** Termination follows the documented next-token signal.
- **“Changing the prefix while keeping the token is harmless.”** Query and token form one continuation context.
- **“Lexicographic ordering is universal.”** Resource types and namespace modes can differ.
- **“LIST contains every stored byte population.”** Versions, delete markers, snapshots, candidates, and soft-deleted records may require separate APIs.
- **“HEAD after LIST enriches the same row.”** Replacement can occur between requests; bind a version or condition.
- **“ETag and timestamp uniquely identify content.”** Use documented version/generation and digest semantics.
- **“Tag update success means tag search is current.”** Object/tag state and the secondary search index can have different visibility.
- **“A CDN stale read disproves origin consistency.”** Cache and origin are separate surfaces.
- **“Geo-redundant means globally current.”** Secondary replication can be asynchronous.
- **“Events eliminate scans.”** Retention gaps, loss, bugs, and permission failures still require reconciliation.
- **“Counts prove equality.”** Missing and extra entries can cancel; compare exact identities.
- **“A missing listing row authorizes deletion from another system.”** Revalidate authoritative exact versions and policy.
- **“Prefix contents are a committed dataset.”** Publish an immutable versioned manifest.
- **“One quiet integration test proves consistency.”** Test concurrent histories, long scans, faults, caches, indexes, and replicas.
- **“Technical consistency proves governance compliance.”** Authorization, retention, provenance, ethics, and deletion evidence need named review.

## Worked Examples

### Example 1

**Situation:** PUT of `x` succeeds, then a primary LIST begins. **Reasoning:** Under a documented strong read-after-write LIST contract, `x` must appear if it matches the query. A timed-out PUT or an overlapping PUT does not create the same real-time obligation.

### Example 2

**Situation:** A scan reads `a,c`, then another client inserts `b`. **Reasoning:** If pagination is live and continues after `c`, `b` can be missed despite individually valid pages. Use a snapshot, manifest, or change capture for complete point-in-time membership.

### Example 3

**Situation:** The SDK returns 300 items although page size was 1,000, plus a continuation token. **Reasoning:** Process and checkpoint the 300, then follow the token. Requested page size is a maximum, not a terminal condition.

### Example 4

**Situation:** LIST reports key `model` at version 41; HEAD without a version returns 42. **Reasoning:** The key was replaced between observations. Fetch version 41 explicitly if processing the listed identity, or restart/reconcile rather than merging fields from two versions.

### Example 5

**Situation:** A tag was updated and HEAD shows it, but tag search does not. **Reasoning:** Measure the index's documented/observed lag, carry exact version in index records, and revalidate candidates against authoritative object state before action.

### Example 6

**Situation:** Primary reads show a new object while a read-access geo-secondary does not. **Reasoning:** This can be valid under asynchronous replication. Route freshness-critical traffic to the authority and expose replica watermark/RPO rather than calling the object lost.

### Example 7

**Situation:** A billion-key inventory crashes after persisting page output but before its token. **Reasoning:** Restarting the page may duplicate rows; exact `(key,version,scan)` upserts make retry harmless. Atomically persisting output and next cursor reduces ambiguity.

### Example 8

**Situation:** A batch dataset consists of 10,000 objects under a prefix while unrelated writers use that prefix. **Reasoning:** Consumers read a committed manifest listing exact versions and digests. LIST audits reachability but does not define dataset membership.

### Example 9

**Situation:** A cleanup index says 50,000 objects are expired. **Reasoning:** Freeze candidates, re-read exact versions and retention/holds, conditionally delete approved versions, stop on mismatch, and reconcile results. Index membership alone is not deletion authority.

### Example 10

**Situation:** A public object is replaced but users still receive old bytes. **Reasoning:** Inspect cache headers/status and immutable version identity. Origin consistency cannot purge every intermediary; use versioned URLs or appropriate cache invalidation/freshness policy.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies linearizability, snapshot isolation, logical time, change streams, replicas, and reconciliation. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies pagination, opaque cursors, conditional requests, idempotency, and API evolution.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes manifests, inventories, partition discovery, incremental ingestion, checkpoints, and backfills. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns authoritative identity, catalogs, provenance, retention, and lifecycle policy.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies managed object storage, observability, quotas, cost controls, failover, and reconciliation automation. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization propagation, cache exposure, scoped credentials, audit, and safe deletion.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies indexes, MVCC snapshots, isolation, outbox protocols, and compare-and-set updates. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies boundary definition, evidence, hazards, and socio-technical review for destructive workflows.

Current Amazon S3 documentation states strong consistency for object PUT/DELETE followed by GET/LIST at the named service and separately documents eventual behavior for some bucket configurations. Google Cloud Storage documents strong object listing while describing cache and policy exceptions. Azure documents strong primary-region consistency alongside eventual secondary replication and an eventually consistent blob-tag secondary index. These are scoped contracts, not interchangeable slogans.

## References

- Amazon Web Services, [*What Is Amazon S3? — Data Consistency Model*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel), checked 2026-09-03. Official current object PUT/DELETE, GET/HEAD, metadata, LIST, atomic update, concurrency, and bucket-configuration consistency scope.
- Amazon Web Services, [*ListObjectsV2 API*](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html), checked 2026-09-03. Official current page limit, continuation token, prefix, delimiter, ordering differences, and response parsing contract.
- Google Cloud, [*Cloud Storage Consistency*](https://cloud.google.com/storage/docs/consistency), checked 2026-09-03. Official current strong object/listing operations, eventual access-control behavior, cache exception, atomicity, and range-read warning.
- Google Cloud, [*Objects: list*](https://cloud.google.com/storage/docs/json_api/v1/objects/list), checked 2026-09-03. Official current lexical ordering, page token, concurrent insertion note, page termination, prefixes, versions, and soft-deleted query fields.
- Google Cloud, [*Object Metadata*](https://cloud.google.com/storage/docs/metadata), checked 2026-09-03. Official current system/custom metadata, generation, metageneration, cache control, retention, and mutability semantics.
- Google Cloud, [*Caching*](https://cloud.google.com/storage/docs/caching), checked 2026-09-03. Official current built-in and external cache behavior, freshness controls, and stale-content risk.
- Microsoft, [*List Blobs (REST API)*](https://learn.microsoft.com/en-us/rest/api/storageservices/list-blobs), checked 2026-09-03. Official current prefix/delimiter, marker pagination, metadata projection, versions/snapshots/uncommitted populations, and tag-index consistency scope.
- Microsoft, [*Use Geo-Redundancy to Design Highly Available Applications*](https://learn.microsoft.com/en-us/azure/storage/common/geo-redundant-design), checked 2026-09-03. Official current primary/secondary asynchronous replication and eventual secondary-read behavior.
- Microsoft, [*Managing Concurrency in Blob Storage*](https://learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage), checked 2026-09-03. Official current strong consistency, snapshot isolation, ETag, optimistic concurrency, and last-writer-wins mechanisms.
- Maurice P. Herlihy and Jeannette M. Wing, [*Linearizability: A Correctness Condition for Concurrent Objects*](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), checked 2026-09-03. Primary paper defining real-time-respecting concurrent-object histories and linearization points; provider behavior remains governed by official service documentation.

## Exercises

### Exercise 1

A live lexicographic scan returns page `a,c`. Before page two, a writer inserts `b,d` and deletes `e`; the pre-scan set was `a,c,e,g`. Show one legal continuation after `c`, compare it with initial/final snapshots, and state a correct remedy.

### Exercise 2

Design a crash-safe inventory of 2.4 billion matching keys when the service returns at most 1,000 items per page. Give the request lower bound and checkpoint invariants.

### Exercise 3

A LIST row names key `report` at version 17, then an unversioned HEAD returns version 18. Explain the observation and design safe processing and deletion paths.

### Exercise 4

Design a complete continuously updated catalog when LIST pagination has no snapshot but an at-least-once change stream retains seven days. State conditions under which the design fails.

### Exercise 5

Specify evidence and named review for deleting regulated objects selected by an eventually consistent tag index and observed through a geo-secondary endpoint.

## Answers to the Exercises

### Answer 1

After `a,c`, a live keyset continuation can return `d,g`: `b` is behind the cursor, `d` is ahead, and deleted `e` is absent. The combined result `a,c,d,g` equals neither initial `a,c,e,g` nor final `a,b,c,d,g`. Each page can satisfy its own request contract without scan-wide snapshot isolation. Use a provider snapshot/revision, consume an immutable manifest, or combine a live baseline with change capture and exact-identity reconciliation. Merely rerunning one missing prefix without a watermark does not prove completeness.

### Answer 2

The quiet-set lower bound is `ceil(2,400,000,000/1,000)=2,400,000` page requests; retries, short/empty pages, delimiter projections, throttling, and mutations increase it. Persist scan identity, exact resource/endpoint/API/auth scope, immutable query/projection/version mode, token or proven disjoint range, page request ID, item count, and terminal state. Commit page rows as idempotent `(scan,key,version)` upserts atomically with the next checkpoint, or ensure replay cannot skip data. Follow tokens until the documented terminal condition, bound repeated-token loops, backpressure consumers, record restart reason, and reconcile against a snapshot, change watermark, or later authoritative pass.

### Answer 3

The object was replaced between LIST and HEAD, or the two requests reached surfaces with different contracts; key equality does not join versions. To process the listed object, GET/HEAD exact version 17 and verify length/digest/metadata. To process current state, accept 18 explicitly and update the work item rather than mixing fields. For deletion, reevaluate policy and retention on exact current identity and send a version-specific or `If-Match` conditional delete. A mismatch is a safe conflict; an unconditional delete could remove version 18 contrary to intent.

### Answer 4

Capture stream position `w0`, begin a durable baseline live scan, and upsert every `(key,version)` idempotently. Consume/replay changes from `w0`, applying version-aware create/update/delete rules, until reaching a watermark beyond scan completion; then declare convergence and keep streaming. Partition checkpoints and page output must be crash-safe, events deduplicated, and periodic full reconciliation retained. The design fails to prove completeness if stream retention is shorter than scan plus outage, `w0` cannot cover mutations around scan start, events omit exact identities/deletes, ordering cannot be resolved, permissions hide objects, baseline query changes, or the stream has an undetectable gap.

### Answer 5

Treat the tag index and geo-secondary as candidate sources only. Record their query, index/replica watermarks, observed lag, endpoint, policy version, and exact candidate identities. At the primary authority, fetch exact current version, tags, owner, retention, hold, legal basis, provenance, and replication/recovery dependencies; compare with an approved immutable deletion manifest and issue conditional version-specific deletes. Use canaries, rate limits, mismatch stop thresholds, soft-delete/quarantine where required, post-delete primary and replica reconciliation, and immutable audit evidence. Named review includes data owner/steward, records/privacy/legal, compliance, affected community or research-ethics/IRB representation where applicable, security/key management, storage/replication operators, incident recovery, accessibility, and independent assurance. Strong primary deletion semantics do not prove cache purge, replica erasure, backup expiry, or lawful disposition by themselves.
