---
module_id: DE-061
program: Data Engineering
level: 2
module_number: 61
title: Object Storage as a Data Substrate
status: complete
last_verified: 2026-09-03
---

# Object Storage as a Data Substrate

## One-Page Review

### Governing question

How should a data platform use object storage as a durable, economical substrate while preserving atomic publication, reproducible identity, integrity, access control, recovery, and cost visibility despite a flat key namespace, whole-object replacement, retries, concurrent writers, multipart state, version accumulation, and asynchronous consumers?

### Essential definitions

- An **object** is an opaque byte sequence plus service metadata addressed by bucket/container, key/name, and—when exposed—version or generation.
- A **key** is an identifier in a flat namespace. Slash-delimited prefixes can imitate hierarchy for listing, but they are not filesystem directories.
- A **generation/version ID** identifies one stored incarnation of a key. It is safer than a bare key for reproducible reads.
- An **entity tag (ETag)** is an HTTP validator or provider response value. It is not universally a content hash; interpret it only under the provider's documented rules.
- A **precondition** makes an operation contingent on observed state, such as create only if absent or replace only if the current generation/ETag still matches.
- **Immutable-object publication** writes data to never-reused keys, verifies it, then conditionally publishes a small manifest or pointer that names exactly those versions.
- A **manifest** is a data object that enumerates the members, identities, checksums, schema, and provenance of a logical dataset version.
- A **multipart/resumable upload** stages independently transferable pieces and exposes the final object only after a successful finalize/complete operation.
- A **delete marker** is a current version that makes an ordinary read appear absent while older versions may remain retained.
- **Lifecycle management** automatically transitions or expires current versions, noncurrent versions, delete markers, or incomplete uploads under explicit rules.
- **Object lock/WORM** prevents mutation or deletion of protected versions for a retention interval or legal hold; ordinary versioning alone is not WORM.
- **Range read** requests selected bytes from one representation. Multiple ranges must be pinned to one object version to avoid mixing generations.
- **Inventory/reconciliation** is a finite, authoritative comparison of intended objects, stored objects/versions, checksums, and consumer state; notifications are merely triggers.
- **Durability** concerns probability of retaining committed bytes; **availability** concerns ability to serve them now; **backup/recovery** concerns restoration after authorized or malicious logical loss.
- The **small-file problem** is excessive object count and per-object overhead relative to useful bytes, affecting request cost, listing, planning, metadata, and scan efficiency.

### Central model, mechanism, or theorem

Model an object identity as

$$
o=(b,k,g,h,n),
$$

where $b$ is bucket, $k$ key, $g$ provider generation/version, $h$ verified content digest, and $n$ byte length. A bare URI $(b,k)$ is mutable naming; a reproducible input includes $g$ and normally $h$.

For a logical dataset revision $r$, upload immutable data objects $O_r$, verify their lengths and digests, write manifest $M_r=H(r,O_r,s,p)$, and publish pointer $P$ only if its observed version is unchanged:

$$
publish(P,M_r,g_P)=CAS(P,g_P,M_r).
$$

Readers first resolve one pointer/manifest version, then read exactly its object identities. If the compare-and-swap fails, the writer has not published and must reconcile rather than overwrite the winner. Objects uploaded but not referenced are garbage candidates, not visible dataset members.

A useful request-and-capacity approximation is

$$
N=\left\lceil\frac{D}{F}\right\rceil,
\qquad
C\approx D c_s t+N_{put}c_{put}+N_{get}c_{get}+B_r c_r+B_e c_e+C_{rep}+C_{kms}.
$$

$D$ is logical bytes, $F$ target file size, $c_s$ storage price, $t$ retention, $B_r$ retrieved bytes, and $B_e$ transferred bytes. Prices, minimum durations, and operation classes are provider/location specific.

### Critical invariants

- A committed manifest names immutable data keys and exact versions/generations, sizes, digests, schema identity, and producer/run identity.
- No reader infers a committed dataset by listing a prefix while writers are active; listing supports discovery and reconciliation, not the commit boundary.
- A shared mutable pointer is changed only with an absence or observed-version precondition; concurrent publication never silently loses an update.
- Retried writes preserve one operation identity, target key, expected prior generation, content digest, and intended result.
- Success, explicit failure, and unknown outcome are distinct. After a timeout, the client reads metadata and reconciles before retrying destructively.
- Partial multipart state is never mistaken for a complete object, and abandoned uploads have bounded cleanup and ownership.
- Integrity uses a documented checksum/digest algorithm and byte length. An ETag is not assumed to be MD5.
- Range readers pin a generation/version and verify the intended representation.
- Prefixes encode organization but do not provide directory atomicity, rename, recursive transaction, lock, or POSIX append semantics.
- Deletion policy distinguishes logical removal, delete markers, noncurrent versions, permanent deletion, retention, legal hold, and erasure evidence.
- Versioning, replication, and high durability do not replace independent recovery design, least privilege, or tested restore.
- Notifications are deduplicated and reconciled against authoritative metadata/inventory because delivery may repeat or be delayed.
- Tenant, environment, region, sensitivity, retention, and encryption boundaries are explicit in bucket, key, identity, and policy design.
- Cost models include requests, stored versions, incomplete uploads, retrieval, network transfer, replication, encryption/KMS, inventory, and early-deletion exposure.

### Common failures

Common failures include treating an object store as a mounted POSIX filesystem; assuming slash creates a directory; renaming a large tree as if metadata-only; appending in place; publishing by copying into a shared prefix and then listing it; overwriting `latest.json` without a precondition; retrying an uncertain PUT under a different key; assuming ETag equals MD5; combining unpinned range reads across an overwrite; leaving multipart uploads indefinitely; enabling versioning without expiring noncurrent versions; calling versioning a backup; calling replication a backup; deleting a key while retained versions remain; applying lifecycle rules without retention/legal review; treating at-least-once notifications as a ledger; granting broad list/delete permissions to readers; embedding secrets in presigned URLs or logs; using predictable tenant prefixes without authorization boundaries; choosing archive tiers without retrieval and minimum-duration economics; creating millions of tiny files; and quoting vendor durability as proof of application recoverability.

### Compact example

Writer A stores `data/run-41/part-000.parquet` and `part-001.parquet` under unique keys, validates size and digest, and writes immutable `manifests/run-41.json`. It reads `tables/orders/current` at generation 8 and conditionally replaces it with the manifest identity if generation 8 still matches. Writer B attempts the same precondition and fails because the pointer is now generation 9. Readers that resolved generation 9 see one complete manifest; they never discover membership by listing `data/run-41/`. If Writer A timed out after publication, it reads the pointer and recognizes its manifest digest before deciding whether another request is needed.

### Connections

[DE-044](044-retries-timeouts-and-idempotency.md) establishes retry identity and uncertain-outcome reconciliation. [DE-046](046-backfill-planning.md) supplies isolated generations, [DE-049](049-run-metadata-and-operational-state.md) supplies run evidence, and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) supplies correction facts that durable objects must retain. DE-062 organizes raw, standardized, and curated zones; DE-063 adds table metadata and snapshots; DE-064 through DE-070 build evolution, time travel, compaction, clustering, catalogs, and transactional-table operations on this substrate.

## Governing Question

Object stores are compelling data substrates because they separate durable byte storage from elastic compute, address enormous namespaces, support independent readers and writers, and price capacity differently from database or local-filesystem storage. Those properties do not make them databases or filesystems.

The governing question is therefore not “Can this engine read an `s3://`, `gs://`, or blob URI?” It is: what protocol turns independently written objects into one authoritative, reproducible dataset state under concurrency, retry, deletion, and recovery?

The answer begins with the actual abstraction. An object has a key and bytes; many services also expose metadata, an ETag, and a version/generation. Prefix listing can project a directory-like view. It does not create a directory transaction, file lock, atomic tree rename, or append protocol.

Modern providers document strong consistency for important object and listing operations in their stated products. That removes older workarounds based solely on eventually consistent listing. It does not make a multi-object update atomic. Ten successful PUTs followed by a failed eleventh still leave ten objects. Two writers can each complete internally consistent sets and race on the shared name that declares which set is current.

Use immutable data plus a small conditional commit point. Unique keys make retry and ownership comprehensible. A manifest makes membership explicit. A generation or ETag precondition turns the mutable pointer into a compare-and-swap. Version-pinned readers avoid mixing revisions. Reconciliation handles uncertain outcomes and garbage.

This chapter treats vendor features as scoped mechanisms rather than universal semantics. S3 version IDs, Cloud Storage generations, Azure blob version IDs, ETags, multipart uploads, lifecycle rules, object locks, and pricing differ. The durable design names which guarantee it relies on and keeps provider-specific adapters at the boundary.

## Why This Matters

An analytical query can return a plausible but impossible result when it reads half of one production run and half of another. File counts may match, row totals may look reasonable, and no API call need fail. Without a manifest-level commit boundary, there may be no evidence of which collection was intended.

Retries create a second danger. A timeout means the client did not observe a result; it does not prove the service failed. Blindly generating a new destination key can duplicate data. Blindly overwriting a shared key can destroy another writer's publication. An operation identity and post-timeout HEAD/read turn uncertainty into a state comparison.

Filesystem assumptions create hidden scale and correctness costs. A “rename directory” may actually copy every object and then delete every source. A recursive list can require many paginated requests. An apparent empty directory may not exist at all. Append-oriented formats may require rewriting or composing complete objects.

The small-file problem changes economics and performance. One terabyte in four-kilobyte objects is not equivalent to one terabyte in a few thousand columnar files. Both store similar payload bytes, but the former multiplies PUT, GET/HEAD, list, scheduler, catalog, encryption, and open/close work.

Governance depends on version semantics. A simple delete in a versioned bucket may add a delete marker while older bytes remain. Lifecycle expiration can conflict with legal hold, evidence preservation, or privacy erasure. Replication can copy an accidental deletion or corrupt logical state. WORM controls can also make an erroneous retention policy difficult or impossible to reverse.

Security is data architecture. A bucket policy, service identity, encryption key, presigned URL, network boundary, and tenant prefix collectively determine who can enumerate, read, publish, and destroy data. Encryption at rest does not compensate for a principal with unrestricted decryption and delete rights.

Finally, advertised durability is a storage-service property under stated assumptions. It does not prove that the application wrote the right bytes, retained the required version, can find the manifest, can decrypt it, or has practiced restore. Recovery evidence must cover the full path.

## Prerequisites and Retrieval

Retrieve the provider and namespace contract: account/project/subscription, region/location, bucket/container type, object model, maximum key/object/metadata sizes, supported version identifiers, consistency scope, conditional request syntax, list pagination, copy/compose semantics, range behavior, and service quotas.

Retrieve the dataset contract: logical table/data product, schema ID, partition transforms, sort/clustering, file format, compression, target size, expected count, authoritative manifest/table format, snapshot identity, consumer discovery path, and allowed visibility latency.

Retrieve writer behavior: job/run ID, source cut, attempt ID, concurrency, multipart threshold/part size, checksum algorithm, server-side encryption mode, KMS key, destination key derivation, overwrite rules, pointer precondition, timeout behavior, and cleanup owner.

Retrieve reader behavior: pointer resolution, metadata caching, version pinning, range reads, predicate/column pruning, retry policy, stale cache tolerance, read-after-delete expectation, authorization, and behavior when a referenced object is absent or corrupt.

Retrieve mutation semantics: whether keys are immutable by policy, object versioning/soft delete state, delete markers, noncurrent-version retention, copy-and-delete moves, metadata replacement, legal holds, WORM mode, erasure workflow, and exceptions.

Retrieve integrity evidence: producer digest, wire checksum, provider-stored checksum, size, content encoding, multipart checksum semantics, ETag interpretation, encryption envelope/key version, validation time, corrupt-object route, and restoration source.

Retrieve lifecycle and recovery evidence: transition and expiration rules, minimum storage duration, incomplete-upload abort, version count/age, replication topology, replication lag, inventory cadence, backup isolation, recovery point objective, recovery time objective, restore drills, and key recovery.

Retrieve security boundaries: bucket policy, IAM roles, conditions, public-access controls, access points/endpoints, tenant mapping, read/list/write/delete separation, object ownership, KMS grants, presigned URL lifetime and constraints, audit logs, and break-glass procedure.

Retrieve volume and cost evidence: logical/stored bytes, compression, daily ingress, average and tail object sizes, requests by operation, list pages, range bytes, retrieval bytes, data transfer paths, noncurrent versions, incomplete parts, replication, inventory, monitoring, KMS calls, and lifecycle transition/early-delete charges.

Retrieve operational evidence: error and throttle codes, latency distributions by operation/region, multipart age, orphan objects, missing references, duplicate notifications, failed preconditions, pointer conflicts, checksum failures, restore time, inventory age, and cost anomaly ownership.

Distinguish key from object version; prefix from directory; latest name from immutable identity; service success from client observation; ETag from content digest; transport checksum from semantic validation; logical delete from permanent erasure; versioning from backup; replication from recovery; durability from availability; notification from authoritative inventory; and storage price from total workload cost.

Create a substrate contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Bucket, immutable key, generation/version, byte length, digest and schema |
| Publication | Data-first order, manifest, conditional pointer, conflict and timeout reconciliation |
| Read | Snapshot resolution, pinned versions, ranges, cache rules and missing/corrupt behavior |
| Upload | Single/multipart threshold, part identity, finalization, checksum and abort ownership |
| Mutation | Overwrite prohibition, copy/delete, versioning, delete marker and permanent-delete authority |
| Lifecycle | Current/noncurrent/part transitions, retention, legal hold, erasure and dry-run evidence |
| Security | Tenant/environment boundary, least privilege, encryption/KMS, URL and audit controls |
| Recovery | Replication scope, independent restore authority, inventory, RPO/RTO and drills |
| Economics | Capacity, operations, retrieval, transfer, versions, parts, encryption and observability |
| Operations | SLOs, throttling, reconciliation, garbage collection, rollout and rollback |

Write a falsifiable claim: “Dataset `orders` publishes immutable Parquet objects and a digest-bearing manifest per run; `current` changes only with an observed-generation precondition; readers pin the pointer, manifest, and object versions; uploads validate CRC32C and length; incomplete multipart uploads expire after seven days; unreferenced objects are quarantined for 30 days before deletion; versions and retention satisfy a documented 35-day recovery objective; permissions separate read, publish, lifecycle, and permanent delete; and daily inventory reconciliation reports every missing, corrupt, orphaned, or unexpectedly retained object.”

## Learning Objectives

After completing this module, you should be able to:

1. model objects, keys, prefixes, versions/generations, metadata, ETags, and checksums without importing filesystem assumptions;
2. design immutable-object and manifest publication with conditional shared-pointer updates;
3. reconcile retries and unknown outcomes using stable operation identity and observed object state;
4. implement safe single-part, multipart, range-read, copy, and delete workflows;
5. distinguish consistency, atomicity, durability, availability, versioning, replication, backup, and restore;
6. calculate object count, request amplification, multipart bounds, and lifecycle-aware cost;
7. design version, deletion, retention, WORM, legal-hold, and erasure controls;
8. enforce tenant-aware least privilege, encryption, KMS, URL, and audit boundaries;
9. observe and reconcile authoritative inventories rather than trusting notifications as a ledger; and
10. migrate filesystem-oriented pipelines to explicit object-storage protocols with fault-tested rollout and rollback.

## Core Exposition

### Start from the object abstraction

An object store maps a key to one current object representation, often with addressable historical versions. The bytes are normally replaced as a whole. Metadata may be set at creation or replacement. Provider APIs expose operations analogous to PUT, GET, HEAD, LIST, DELETE, COPY, multipart completion, and lifecycle configuration.

The namespace is flat even when consoles render `/` as folders. A key such as `tenant=7/date=2026-09-03/part-000.parquet` is one string. Prefix and delimiter parameters help list related keys. They do not create a parent inode or a transaction covering descendants.

Design key syntax as an API. Specify normalization, allowed characters, escaping, case, maximum length, tenant/environment prefix, dataset, generation, partition encoding, file identity, and whether any segment contains personal data. Avoid secrets and unstable display text.

Unique keys reduce contention and make ownership evident. A durable example is `prod/orders/data/run=01K.../part=00017.parquet`, where the run and part identities are immutable. A risky key is `prod/orders/data/latest/part-000.parquet`, which multiple attempts can overwrite.

### Separate consistency from multi-object atomicity

Current Amazon S3 documentation states strong read-after-write consistency for PUT and DELETE operations, and Cloud Storage documents strong object read/list consistency with scoped exceptions such as publicly cached objects and some configuration changes. Record the exact service, operation, bucket type, cache, and date when relying on such a claim.

Strong LIST means a successfully created object should appear under the documented conditions. It does not mean a set of objects has a transaction boundary. If a job writes 100 objects and fails after 63, a list faithfully returns the partial set.

Therefore do not define completeness as “all files currently under a prefix.” Define it with an immutable manifest or transactional table metadata. Listing remains useful for garbage discovery, inventory, audits, and tools whose contract explicitly tolerates partial collections.

Object operations are commonly atomic at one object: readers see the old or new complete representation, not a partial upload. That does not coordinate data objects, manifest, pointer, catalog, and downstream notification. The application protocol supplies this coordination.

### Publish data, manifest, then pointer

Use this order:

1. Allocate a stable run/attempt and immutable destination keys.
2. Upload each data object, recording version/generation, size, digest, schema, partition facts, and source provenance.
3. Verify provider metadata and, where required, read back or sample the stored bytes.
4. Write one immutable manifest containing the complete sorted member set and its own canonical digest.
5. Validate that every manifest member exists with the exact recorded identity.
6. Read the shared pointer/catalog entry and capture its current version or absence.
7. Replace/create it only with a matching-version or absent-object precondition.
8. Record publication result and reconcile timeouts.
9. Notify consumers using the committed snapshot identity.
10. Later collect unreferenced objects only after retention and reachability checks.

The pointer can be a small object, catalog transaction, or table-format metadata reference. The important property is one linearization point with conflict detection. A writer that loses the compare-and-swap may rebase, retry from a new source cut, or stop. It must not clobber the winner.

Manifest canonicalization matters. Define field ordering, path encoding, integer/time representation, digest algorithm, duplicate-key rejection, and whether members are sorted. Two semantically equal manifests should have the same digest only if that is an intentional invariant.

Readers resolve once. They do not reread `current` between files. Cache the resolved snapshot identity for the query, validate the manifest, and request exact data versions when the service supports them. This gives snapshot-like behavior even though storage operations occur independently.

### Make retries state-aware

Represent a write attempt with

$$
w=(operation\ id,b,k,g_{expected},h,n,encryption,metadata).
$$

The same logical retry preserves this tuple. Changing the key or bytes creates a new operation requiring new coordination.

Create-only preconditions prevent a retry or competitor from replacing an existing immutable key. Match-version preconditions protect mutable pointers. Provider syntax differs: S3 conditional writes use HTTP validators such as `If-None-Match`/`If-Match` in supported operations, while Cloud Storage exposes generation/metageneration match conditions.

When a request times out, classify the outcome as unknown. HEAD the exact key/version or read the pointer. If stored digest, length, metadata, and operation ID equal the intended result, adopt success. If absent, retry with the same precondition. If present but different, quarantine the conflict. If the state cannot be distinguished, escalate rather than overwrite.

Idempotence is scoped. Uploading the same bytes twice under two unique keys is not idempotent for dataset membership or cost. Repeating a conditional create under one key may return a precondition failure even though the first attempt succeeded; reconciliation maps that transport response to the logical prior success.

### Treat ETags and checksums precisely

HTTP entity tags are validators for representations. Provider ETag construction can vary with multipart upload, encryption, composition, or product type. Never generalize “ETag is the MD5 of the object.”

Select a supported end-to-end digest such as CRC32C or SHA-256 according to threat and interoperability requirements. Record algorithm, encoded value, byte length, content encoding, producer version, and validation result. A checksum catches accidental corruption; a keyed signature or authenticated manifest addresses adversarial substitution and provenance.

Transport validation and semantic validation are separate. A perfectly transferred Parquet file can contain the wrong partition or schema. Validate footer/schema, row/partition bounds, source cut, and manifest facts as well as bytes.

Encryption changes operational evidence. Server-side encryption protects stored bytes under service/KMS controls, but readers still need authorization and key availability. Customer-managed keys add policy, quota, cost, rotation, deletion, and recovery dependencies. Record the encryption mode and key identity without placing secret material in metadata.

### Engineer multipart and resumable uploads

Multipart upload transfers parts independently and finalizes them into one object. It improves parallelism and recovery for large objects, but introduces upload IDs, part numbers, per-part results, finalization, and orphan cleanup.

For object size $D$ and selected part size $P$,

$$
m=\left\lceil\frac{D}{P}\right\rceil.
$$

Choose $P$ so $m$ remains within provider limits, memory/concurrency remain safe, failed-part retransmission is tolerable, and request cost is justified. Provider recommendations and limits are current product facts, not universal constants.

Persist the upload ID, key, checksum algorithm, part number, byte interval, size, checksum/ETag response, and completion state. Do not reconstruct completion from an eventually observed or truncated listing when the API tells clients to retain exact part results.

Only a successful finalize creates the logical object. A client timeout around completion creates another unknown outcome: HEAD the destination and compare its evidence before starting a replacement upload. Configure lifecycle/operational cleanup for incomplete uploads, because staged parts can accrue storage and request charges.

### Pin range reads to one representation

Columnar formats exploit byte ranges to read footers and selected columns. HTTP range requests reduce transferred bytes and latency when supported. They do not identify the version by themselves.

Suppose a reader fetches footer range $R_1$, another writer replaces the bare key, and the reader fetches data range $R_2$. Without a version/generation or conditional validator, $R_1$ and $R_2$ may come from different representations. Pin every range to the resolved object version, or use a strong conditional request that fails on change.

Verify range boundaries and returned status/length. Retries must request the same representation. Caches, gateways, and client libraries can alter range behavior; test the complete path rather than assuming the SDK call maps directly to one service request.

### Treat copy, move, and append as workflows

An object copy usually creates a destination object; a “move” is copy then delete. Across many keys, partial progress is visible unless hidden behind a new manifest. Cost can include read/rewrite, write, retrieval, and transfer depending on class and location.

Do not rename a production prefix in place. Publish a new manifest referencing copied or original immutable objects, verify it, switch the pointer conditionally, and retire old reachability later. If physical relocation is mandatory, make it a resumable migration with per-object ledger and reconciliation.

In-place append is generally not the portable object abstraction. Buffer into larger objects, create new immutable segments, use provider-specific append/compose with its exact constraints, or use a transactional table/log layer. Do not let a filesystem connector hide repeated full-object rewrites.

Metadata changes can also be replacement operations or independently versioned metageneration changes. Use the relevant precondition and verify whether metadata modification changes version, encryption, cache, retention, or replication behavior.

### Design versions and deletion deliberately

Versioning protects prior incarnations from ordinary overwrite and can make recovery easier. It also accumulates billable bytes and metadata. A bare GET commonly returns the current version; a version-pinned GET returns the named historical representation.

In S3 versioning, an ordinary DELETE can create a delete marker and leave older versions. Permanently deleting a version requires its version ID and authority. Other providers expose distinct generations, soft-delete retention, or snapshots. Never report erasure from a successful unversioned-looking DELETE alone.

Define deletion states: logically removed from current dataset, hidden by marker, soft deleted, noncurrent but retrievable, replication pending, retention locked, legal hold, permanently deleted, encryption key scheduled for destruction, and verified erased from every required scope.

Lifecycle rules are executable policy. Test filters, dates, size thresholds, current/noncurrent behavior, delete markers, incomplete uploads, replication interaction, minimum-duration charges, and WORM/hold precedence. Stage changes on inventory reports and canary prefixes before broad activation.

Version count is an operational metric. A hot shared pointer can accumulate many versions; a broken writer can create an unbounded series. Apply retention that preserves recovery/audit needs while bounding cost and list/version-management load.

### Separate WORM, recovery, and erasure

WORM/object lock protects selected object versions against change or deletion for a time-based retention or legal hold. Governance and compliance modes can grant materially different bypass authority. Test on nonproduction data before locking large datasets.

WORM is not backup: it may preserve the wrong bytes in the same administrative/security domain. Backup is not WORM: privileged actors or automated retention may alter it. Versioning is neither by itself. A defensible recovery system combines isolated authority, immutable evidence where required, version selection, catalogs/manifests, keys, procedures, and drills.

Retention and privacy erasure can conflict. Classify data before upload, avoid unnecessary personal data in keys/metadata, minimize retention, document legal basis/holds, and design deletion across replicas, versions, inventories, caches, and derived datasets. Do not promise physical erasure while a legal hold prevents it.

Durability and availability are also separate. A service may durably retain an object while a region, identity provider, network path, or KMS key is unavailable. RTO testing must include listing/resolving manifests, authorization, decryption, and workload capacity, not just byte existence.

### Make notifications hints, not truth

Object-created/deleted notifications are useful triggers. Amazon S3 documents at-least-once delivery, so a handler must expect duplicates; all event systems can also encounter retries, reordering, configuration gaps, and consumer failure within their scoped contracts.

Give each handler an idempotency key containing bucket, key, version/generation, event kind, and destination contract. Read authoritative metadata before effects. A create event for a key that has since been replaced must not cause processing of an unintended current version.

Maintain a periodic authoritative reconciliation from inventory, version listing, manifests, or provider metadata. Compare intended reachable objects, actual objects/versions, processed identities, retention state, and corrupt/missing/orphan cohorts. Notifications reduce detection latency; reconciliation establishes completeness.

### Design least-privilege and tenant boundaries

Separate roles for upload-data, publish-pointer, read-data, list/inventory, lifecycle administration, retention/legal hold, replication, KMS administration, and permanent delete. A query engine rarely needs delete. A loader that writes immutable data may not need to advance the production pointer.

Tenant prefixes improve organization but do not enforce isolation without matching authorization conditions. Normalize and validate tenant identity before key construction. Prevent prefix traversal/confusion, cross-environment endpoints, wildcard principals, public access, and confused-deputy use of service roles.

Presigned URLs are bearer capabilities until expiry under their policy constraints. Keep scope, method, key, size/content conditions, and lifetime narrow; deliver them over protected channels; do not log query credentials; and understand revocation dependencies.

Encryption at rest is baseline, not a complete control. Protect transport, restrict decryption, rotate and recover keys, monitor unusual access, inventory public exposure, and retain audit trails in a separately protected destination. Destruction of a KMS key can make durable bytes unrecoverable, so key lifecycle belongs in RPO/RTO design.

### Model performance and cost from requests

Start with workload shape, not headline price per gigabyte. For daily logical data $D_d$, compression ratio $r$, retention $t$, and replication/storage multiplier $q$,

$$
S\approx D_d r t q+S_{versions}+S_{parts}+S_{orphans}.
$$

For target file size $F$, object count is approximately $D_d r/F$. Smaller $F$ increases PUTs, GET/HEADs, listing pages, catalog entries, task scheduling, footer reads, KMS operations, and lifecycle actions. Larger $F$ reduces metadata overhead but can reduce parallelism and make retries/rewrites more expensive.

Measure distributions, not averages: p50/p95/p99 file size, objects per partition, bytes per request, range-read selectivity, list pages, request latency, and throttles. Compaction belongs in DE-067, but DE-061 establishes why object shape is a substrate concern.

Price models must remain symbolic until provider, region, storage class, access pattern, and date are pinned. Include capacity duration; write/read/list/metadata operation classes; retrieval; network transfer; replication; early deletion/minimum duration; versioned bytes; incomplete parts; inventory; KMS; monitoring; and migration/rewrite operations.

Hot-key/prefix advice changes as providers evolve. Do not preserve folklore such as mandatory random prefixes without verifying the current bucket type and service guidance. Load-test the chosen key distribution and request mix, observe throttle responses, and use bounded exponential backoff with jitter under provider recommendations.

### Observe invariants and reconcile finite cuts

Record every write with run, operation, key, expected prior version, resulting version, size, checksum, encryption, source cut, attempt, latency, and response class. Record publication conflicts separately from infrastructure failures; a failed precondition can be a healthy concurrency signal.

Core metrics include bytes/objects by class and age; object-size distribution; request count/latency/error/throttle by operation; conditional failures; unknown outcomes; multipart age/bytes; checksum failures; pointer versions; missing references; orphans; notification duplicates/lag; version/delete-marker growth; lifecycle actions; replication lag; restore duration; KMS failures; and cost per data product/query.

Reconcile a finite snapshot. If $R$ is the set of manifest-reachable object identities and $A$ the authoritative inventory at a compatible cut:

$$
missing=R-A,\qquad orphan=A-R.
$$

Not every orphan is garbage: it may belong to an unpublished active run, retained old snapshot, legal hold, replica lag, or quarantine. Garbage collection requires age, ownership, reachability across retained snapshots, and policy checks.

Alert on unexplained residue, not simply nonzero orphans. A report should partition every inventoried object/version into current reachable, retained historical, active upload/run, quarantined, scheduled deletion, legal/retention protected, or unexplained.

### Migrate from filesystem assumptions safely

Inventory operations the old system assumes: atomic rename, directory existence, recursive transaction, advisory locks, append, seek, symlink, permissions, modification time, local caching, and read-after-close. Map each to an explicit object protocol or identify an incompatibility.

Introduce immutable destination keys and manifests before changing readers. Dual-write or copy historical data with a migration ledger, verify counts/bytes/digests/schema and representative queries, then dual-read pinned snapshots. Do not use an eventually changing prefix as the comparison oracle.

Cut over the shared pointer/catalog with a precondition and record the old identity for rollback. Keep old data and decryption authority through the rollback horizon. Freeze or isolate legacy writers so they cannot mutate both namespaces after cutover.

Fault-test upload interruption, lost completion response, concurrent publish, reader cache, replacement during ranges, delayed/duplicate notification, lifecycle conflict, permission revocation, KMS unavailability, region/path failure, inventory lag, and restoration at target scale.

## Definitions and Notation

For bucket/container $b$ and key $k$, define:

- $g$: provider version/generation identifying one incarnation.
- $h$: verified content digest under named algorithm.
- $n$: stored byte length.
- $o=(b,k,g,h,n)$: reproducible object identity.
- $O_r$: immutable data-object set for dataset revision $r$.
- $M_r$: immutable manifest for revision $r$.
- $P$: mutable pointer/catalog reference naming the current manifest.
- $g_P$: version of $P$ observed before publication.
- $D$: logical/stored data bytes under the stated context.
- $F$: target mean object/file size.
- $N$: object count.
- $P_s$: multipart part size; $m$ is part count.
- $R$: all object identities reachable from retained manifests.
- $A$: actual authoritative inventory at a compatible cut.
- $T$: protected/retained object identities not currently reachable.

Reproducible identity requires more than a URI:

$$
o=(b,k,g,h,n).
$$

When provider version addressing is unavailable, immutable never-reused keys plus digest/length reduce ambiguity, but the limitation must be explicit.

Publication is a conditional transition:

$$
publish(P,M_r,g_P)=
\begin{cases}
committed(g_P+1), & current(P)=g_P,\\
conflict, & current(P)\ne g_P.
\end{cases}
$$

The symbolic increment means “new version,” not necessarily a numeric provider identifier.

Object count and multipart count are

$$
N=\left\lceil\frac{D}{F}\right\rceil,
\qquad
m=\left\lceil\frac{D}{P_s}\right\rceil.
$$

A storage estimate is

$$
S=S_{current}+S_{noncurrent}+S_{parts}+S_{orphans}+S_{replicas}.
$$

A workload cost model is

$$
C=S c_s t+\sum_j N_jc_j+B_rc_r+B_ec_e+C_{early}+C_{rep}+C_{kms}+C_{obs},
$$

where $j$ ranges over provider operation classes and every coefficient is location/class/date specific.

For compatible inventory and reachability cuts:

$$
missing=R-A,
$$

$$
unclassified=A-(R\cup T\cup active\cup quarantine\cup scheduled).
$$

The safety property is:

> Every committed manifest references only verified immutable object identities, and a reader resolves exactly one committed manifest before reading members.

The publication property is:

> At most one contender can advance a pointer from the same observed version; every other contender receives a detectable conflict.

The recovery property is:

> For every claimed recovery point, retained manifests, object versions, authorization, encryption keys, catalog state, and tested procedures suffice to reconstruct and validate the dataset within the claimed RTO.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the substrate.** Record provider, bucket type/location, consistency/atomicity scope, limits, version identifiers, cache, and date.
2. **Define identity.** Specify immutable key grammar, generation/version, digest, length, schema, tenant/environment, and operation/run IDs.
3. **Define publication.** Require data-first uploads, verification, immutable manifest, conditional pointer/catalog transition, and loser behavior.
4. **Define reading.** Resolve one snapshot, pin object versions and ranges, verify integrity, and state cache/missing-object behavior.
5. **Define retries.** Preserve request identity and preconditions; reconcile unknown outcomes with authoritative metadata before mutation.
6. **Engineer upload.** Bound part size/count/concurrency, retain part evidence, finalize explicitly, and expire incomplete state.
7. **Govern mutation.** Distinguish overwrite, copy/move, logical delete, versions, markers, permanent delete, lifecycle, WORM, hold, and erasure.
8. **Secure and recover.** Separate roles, encryption/KMS, tenant boundaries, replication, backup authority, RPO/RTO, and restore drills.
9. **Model economics.** Measure object shape, operations, ranges, retrieval, transfer, versions, parts, replication, KMS, and lifecycle exposure.
10. **Observe and fault-test.** Reconcile inventory/reachability and inject uncertain completion, concurrent publication, corruption, notification disorder, lifecycle, identity, key, and regional failures.

Proof sketch for publication safety:

1. Each data key is unique and never overwritten.
2. Manifest $M_r$ is immutable and names exact verified object versions.
3. Pointer $P$ is the only discovery path for committed current state.
4. Writers A and B both observe $P$ at $g$.
5. The storage precondition permits at most one replacement conditional on $g$.
6. Suppose A succeeds; $P$ now has a version different from $g$ and names $M_A$.
7. B's condition is false, so B cannot silently replace $M_A$.
8. A reader resolves either the old pointer or the new pointer and then one immutable manifest; it never constructs membership from partially written data.

This is a protocol proof under assumptions, not a proof of every provider implementation. It assumes the documented conditional operation is atomic, clients cannot bypass policy, immutable keys are enforced, and the pointer read is not corrupted by an uncontrolled cache.

The following executable model demonstrates unique data objects, digest-bearing manifests, conditional create/replace, a competing publisher conflict, pinned range reads, uncertain-outcome reconciliation, and orphan classification. Its integer generations model a provider primitive; it does not prove real service durability, authentication, encryption, multipart behavior, or multi-region recovery.

<!-- bijux-verify: {"id":"object-manifest-publication","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"data=(('data/run-a/part-000', 1, 5, 1550), ('data/run-a/part-001', 1, 4, 1036))\nmanifest=('manifests/run-a', 1, 49, 8197)\nfirst_publish=('committed', 1)\ncompeting_publish=('conflict', 1)\ncurrent=('manifests/run-a@1', 1, 8197)\npinned_range=b'beta'\ntimeout_reconciled=True\nreachable=('data/run-a/part-000', 'data/run-a/part-001', 'manifests/run-a', 'tables/orders/current')\norphans=('data/run-b/part-000',)\n","stderr":""}} -->
```python
def digest(data):
    return sum((index + 1) * byte for index, byte in enumerate(data)) % 10007


class Store:
    def __init__(self):
        self.versions = {}

    def head(self, key):
        history = self.versions.get(key, ())
        return history[-1] if history else None

    def put(self, key, data, expected=None):
        current = self.head(key)
        generation = 0 if current is None else current[0]
        if expected is not None and generation != expected:
            return ("conflict", generation)
        new = (generation + 1, data, len(data), digest(data))
        self.versions.setdefault(key, []).append(new)
        return ("committed", new[0])

    def get(self, key, generation, start=None, end=None):
        matches = [item for item in self.versions[key] if item[0] == generation]
        if len(matches) != 1:
            raise KeyError((key, generation))
        data = matches[0][1]
        return data[slice(start, end)]


store = Store()
parts = {
    "data/run-a/part-000": b"alpha",
    "data/run-a/part-001": b"beta",
}
data_evidence = []
for key, payload in sorted(parts.items()):
    outcome = store.put(key, payload, expected=0)
    assert outcome == ("committed", 1)
    generation, _, size, checksum = store.head(key)
    data_evidence.append((key, generation, size, checksum))

manifest_bytes = b"part-000@1:5:1550\npart-001@1:4:1036\nsource=cut-42"
assert store.put("manifests/run-a", manifest_bytes, expected=0) == ("committed", 1)
manifest = store.head("manifests/run-a")
pointer_bytes = f"manifests/run-a@1:{manifest[3]}".encode()
first = store.put("tables/orders/current", pointer_bytes, expected=0)

store.put("data/run-b/part-000", b"loser", expected=0)
competing = store.put("tables/orders/current", b"manifests/run-b@1", expected=0)
current = store.head("tables/orders/current")
current_fields = current[1].decode().split(":")

pinned_range = store.get("data/run-a/part-001", 1, 0, 4)
timeout_reconciled = (
    current_fields[0] == "manifests/run-a@1"
    and int(current_fields[1]) == manifest[3]
)
reachable = set(parts) | {"manifests/run-a", "tables/orders/current"}
actual = set(store.versions)

print(f"data={tuple(data_evidence)}")
print(f"manifest={('manifests/run-a', manifest[0], manifest[2], manifest[3])}")
print(f"first_publish={first}")
print(f"competing_publish={competing}")
print(f"current={(current_fields[0], current[0], int(current_fields[1]))}")
print(f"pinned_range={pinned_range!r}")
print(f"timeout_reconciled={timeout_reconciled}")
print(f"reachable={tuple(sorted(reachable))}")
print(f"orphans={tuple(sorted(actual - reachable))}")
```

The model deliberately leaves `data/run-b/part-000` as an orphan candidate. A production collector would not delete it solely from this set difference; it would check run state, age, retained snapshots, holds, replication, and quarantine policy.

## Alternatives and Trade-Offs

**Mutable data keys versus immutable data keys.** Mutable keys reduce visible namespace growth and can suit replace-in-place products. Immutable keys simplify concurrency, replay, caching, lineage, and rollback at the cost of garbage collection and explicit discovery metadata.

**Prefix discovery versus manifest discovery.** Prefix listing is simple and useful for exploratory ingestion, but concurrent/failed writers expose ambiguous membership. Manifests add creation and validation work while supplying explicit completeness, ordering, identity, and reproducibility.

**Single manifest versus manifest tree.** One manifest offers one compact authority for moderate datasets. Hierarchical manifests bound metadata size and enable incremental planning, but add reachability, fan-out, and garbage-collection complexity.

**Object pointer versus external catalog transaction.** A conditional object keeps state in one substrate and can be portable. A catalog can coordinate richer metadata and authorization, but adds availability, transactional, and recovery dependencies.

**Overwrite versus copy-on-write.** Overwrite limits stored versions but risks readers, caches, and retries unless version pinned. Copy-on-write preserves history and supports safe snapshots while increasing stored bytes until lifecycle/compaction removes old reachability.

**Versioning versus application-unique keys.** Provider versioning captures accidental replacement under one key and supports restoration. Unique application keys make identity visible and portable. Strong systems often use both, with independent retention controls.

**Provider generation versus content-addressed key.** A generation identifies a stored incarnation under provider semantics. A content-addressed key deduplicates equal bytes and detects substitution naturally, but canonicalization, privacy leakage, garbage collection, encryption, and collision policy become design concerns.

**Single-part versus multipart upload.** Single PUT has less state and fewer requests for small objects. Multipart improves large-transfer parallelism and retry granularity while requiring persisted part evidence, completion reconciliation, and orphan cleanup.

**Full GET versus range GET.** Full reads are simple and validate whole objects naturally. Range reads enable columnar pruning and low transfer, but require pinned versions, careful integrity, more requests, and tested cache/proxy behavior.

**Replication versus independent backup.** Replication improves locality and some failure tolerance. It can propagate logical errors and share administrative failure modes. Independent recovery copies add isolation and restore complexity/cost.

**Versioning/soft delete versus WORM.** Versions and soft deletion make recovery convenient but privileged deletion may remain possible. WORM strengthens immutability for compliance or ransomware resistance but can block correction/erasure and demands rigorous policy testing.

**Hot storage versus colder classes.** Hot tiers provide immediate frequent access at higher capacity price. Colder tiers reduce capacity price but may add retrieval latency/fees and minimum-duration exposure. Use measured access and restore objectives.

**Many small files versus fewer large files.** Small files increase parallel granularity and reduce single-retry bytes but amplify requests, metadata, planning, and encryption calls. Larger files improve scan efficiency until reduced concurrency and rewrite blast radius dominate.

**Provider-native features versus portability layer.** Native generations, inventory, events, locks, and lifecycle can be powerful and precise. A lowest-common-denominator abstraction may ease migration but hide crucial semantics. Preserve a portable protocol while exposing required provider capabilities explicitly.

## Failure Modes and Misconceptions

1. **“It looks like a filesystem.”** A mounted connector can conceal flat keys, whole-object replacement, and remote request cost. Inspect generated API behavior and failure semantics.
2. **“Strong consistency gives a transaction.”** It can make each successful object/list result current while a multi-object run remains partial. Commit through explicit metadata.
3. **“Listing the prefix finds the dataset.”** Listing finds keys, including partial, orphaned, retained, temporary, and foreign-writer objects. It does not prove intended membership.
4. **“Rename is atomic and cheap.”** Object moves can be copy plus delete, multiplying time, cost, and partial-failure states.
5. **“PUT timeout means no object.”** The server may have committed. Reconcile the exact target before retry or compensating.
6. **“A random retry key is safer.”** It avoids overwrite but duplicates logical output and cost unless a manifest/idempotency ledger chooses one.
7. **“Last writer wins is acceptable for `current`.”** It silently drops a concurrent committed revision. Conditional publication makes conflict visible.
8. **“ETag is MD5.”** Multipart, encryption, composition, and provider behavior can invalidate this assumption. Use documented checksums.
9. **“One checksum proves correct data.”** It proves equality to some bytes under an algorithm, not correct schema, partition, source cut, authorization, or provenance.
10. **“Range reads cannot mix data.”** Bare-key ranges can cross an overwrite. Pin version/generation or validator.
11. **“Multipart parts disappear on failure.”** Incomplete parts may remain billable until complete, abort, or lifecycle cleanup.
12. **“Versioning prevents deletion.”** It retains historical versions under configured behavior; privileged permanent delete, lifecycle, or bucket deletion may still destroy them.
13. **“Delete succeeded, so bytes are erased.”** A delete marker, noncurrent version, soft-delete copy, replica, backup, cache, or legal hold may retain bytes.
14. **“Replication is backup.”** Replication may copy accidental overwrite/deletion and may share credentials or configuration failures.
15. **“Eleven nines proves my recovery.”** Service durability does not validate application content, manifest retention, catalog, keys, permissions, or restore time.
16. **“Notifications are exactly the object history.”** At-least-once/retry behavior and consumer/configuration gaps require deduplication plus inventory reconciliation.
17. **“Prefixes isolate tenants.”** Naming does not authorize. Policy conditions and normalized identity must enforce the boundary.
18. **“Encryption solves access control.”** Authorized decrypt/read and destructive permissions still require least privilege and audit.
19. **“Archive is simply cheaper.”** Retrieval, minimum duration, early deletion, operations, and RTO may dominate.
20. **“Tiny files only waste a little metadata.”** They amplify provider requests and every layer above storage: catalog, planner, scheduler, reader, KMS, and lifecycle.
21. **“Lifecycle is harmless housekeeping.”** A broad filter or wrong current/noncurrent interpretation can cause irreversible loss or retention violation.
22. **“Garbage equals not current.”** Retained snapshots, active runs, legal holds, and rollback windows may reference objects outside the current manifest.
23. **“Cached public objects follow origin consistency.”** Cache lifetime can expose stale representations even when origin operations are strongly consistent.
24. **“Old random-prefix advice is timeless.”** Performance guidance changes by provider and bucket type. Verify current official documentation and measure.

## Worked Examples

### Example 1

A job writes 20 of 24 files before its worker fails. Every completed PUT and LIST is strongly consistent, yet the prefix is not a complete dataset. Because no manifest/pointer was published, readers remain on the prior snapshot and the 20 files become age-gated orphan candidates.

### Example 2

Two writers read `current` at generation 14. Writer A conditionally publishes manifest A and creates generation 15. Writer B's generation-14 precondition fails. B records a publication conflict and rebases or stops; it never silently replaces A.

### Example 3

A PUT response is lost after the service commits `data/run-7/part-003`. The retry HEAD finds the same operation ID, length, and SHA-256 at generation 1. The client adopts logical success instead of uploading `part-003-retry` or overwriting unknown bytes.

### Example 4

A 640 MiB object uses 64 MiB parts, so $m=\lceil640/64\rceil=10$. Part 7 is retransmitted without restarting other parts. Completion times out; the client checks the final object evidence before creating another upload, and lifecycle bounds abandoned part storage.

### Example 5

A reader fetches a Parquet footer, then data columns. Both requests name generation 23. A concurrent overwrite creates generation 24 but cannot change the reader's representation. Without generation pinning, footer and column offsets could refer to incompatible bytes.

### Example 6

A versioned key is deleted without a version ID. The current read returns absent because a delete marker is current, while earlier versions remain billable and retrievable. The erasure workflow enumerates and removes authorized versions after hold/retention checks rather than treating the marker as proof.

### Example 7

Daily input is 1 TiB compressed to 0.25 TiB. At 1 MiB per object the job creates roughly 262,144 objects/day; at 256 MiB it creates about 1,024. The smaller layout may offer more task granularity but drives about 256 times as many per-object writes and opens before considering queries.

### Example 8

An object-created notification is delivered twice. The consumer's identity `(bucket,key,generation,event-kind)` maps both deliveries to one processing receipt. A daily inventory later finds one object whose notification route was misconfigured and schedules it, proving why events accelerate but do not establish completeness.

### Example 9

A team selects a cold class for 90-day retention but deletes most objects after 12 days and rereads them weekly. Retrieval, operations, and minimum-duration exposure exceed the capacity saving. A measured hot/cold policy partitions objects by actual access and recovery requirements.

### Example 10

A migration tool “renames” 10 million keys by copy/delete. The process stops halfway, leaving two prefixes and ambiguous ownership. The repaired design records each copy in a ledger, validates destination identities, publishes a manifest for the complete destination, conditionally switches discovery, then retires sources after rollback retention.

## Cross-Program Connections

- **Distributed Systems:** per-object atomicity, compare-and-swap, retries, unknown outcomes, linearization points, and immutable logs/manifests make publication a distributed protocol.
- **Computer Networks:** HTTP validators, conditional requests, byte ranges, caching, TLS, endpoints, timeouts, and backoff directly affect correctness and performance.
- **Data Structures Engineering:** flat keyspaces, prefix indexes, manifests, Merkle-like digest trees, Bloom-assisted inventory, and reachability graphs shape lookup and garbage collection.
- **Database Systems:** manifests and pointers resemble pages plus commit records; snapshots, write conflicts, MVCC, catalogs, and compaction build transactional tables above objects.
- **Information Security:** IAM, bearer URLs, KMS, tenant boundaries, WORM, legal holds, audit logs, integrity digests, and destructive authority determine confidentiality and resilience.
- **Reliability Engineering:** durability, availability, RPO/RTO, replication, fault injection, orphan reconciliation, restore drills, SLOs, and cost anomalies require explicit evidence.
- **Software Engineering Patterns:** immutable values, content identity, adapters, idempotency keys, state machines, and compare-and-swap isolate provider semantics from domain publication.
- **Operating Systems:** inode/directory/rename/append assumptions clarify exactly which POSIX guarantees an object store does not portably provide.
- **FinOps and Economics:** capacity duration, request amplification, retrieval, transfer, early deletion, versions, encryption, and compaction determine total cost rather than storage price alone.
- **Governance and Privacy:** classification, residency, minimization, retention, legal hold, erasure, lineage, and evidence must cover every version and replica.

## References

1. Amazon Web Services. [What is Amazon S3?](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html). Accessed 2026-09-03. Primary documentation for the object/bucket service model and current strong read-after-write consistency statement.
2. Amazon Web Services. [Naming Amazon S3 objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html). Accessed 2026-09-03. Primary documentation for flat object-key structure and console-inferred hierarchy.
3. Amazon Web Services. [Organizing objects using prefixes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-prefixes.html). Accessed 2026-09-03. Primary documentation for prefix/delimiter listing and the explicit distinction from directories.
4. Amazon Web Services. [How to prevent object overwrites with conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html). Accessed 2026-09-03. Primary documentation for `If-None-Match`, `If-Match`, concurrent creates, and conflict responses.
5. Amazon Web Services. [Uploading and copying objects using multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html). Accessed 2026-09-03. Primary documentation for initiation, part evidence, completion, checksums, billing, and abort responsibilities.
6. Amazon Web Services. [How S3 Versioning works](https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html). Accessed 2026-09-03. Primary documentation for version IDs, overwrites, delete markers, restoration, and version charges.
7. Amazon Web Services. [Lifecycle configuration elements](https://docs.aws.amazon.com/AmazonS3/latest/userguide/intro-lifecycle-rules.html). Accessed 2026-09-03. Primary documentation for lifecycle actions, including explicit cleanup of incomplete multipart uploads.
8. Amazon Web Services. [Locking objects with Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html). Accessed 2026-09-03. Primary documentation for WORM, retention modes, legal holds, versions, and delete behavior.
9. Amazon Web Services. [Amazon S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html). Accessed 2026-09-03. Primary documentation for event configuration and at-least-once delivery.
10. Google Cloud. [Cloud Storage consistency](https://cloud.google.com/storage/docs/consistency). Accessed 2026-09-03. Primary documentation for current object/list consistency, atomic individual operations, caching qualification, and version-pinned ranges.
11. Google Cloud. [Request preconditions](https://cloud.google.com/storage/docs/request-preconditions). Accessed 2026-09-03. Primary documentation for generation/metageneration conditions and race-free mutations.
12. Google Cloud. [Data validation and change detection with checksums](https://cloud.google.com/storage/docs/data-validation). Accessed 2026-09-03. Primary documentation for CRC32C/MD5 integrity scope, server validation, and composite-upload qualifications.
13. Google Cloud. [Object Versioning](https://cloud.google.com/storage/docs/object-versioning). Accessed 2026-09-03. Primary documentation for live/noncurrent generations, deletion, metadata, lifecycle, and billing considerations.
14. Google Cloud. [Cloud Storage pricing](https://cloud.google.com/storage/pricing). Accessed 2026-09-03. Primary pricing documentation for capacity, operations, retrieval, transfer, replication, and early-deletion components; rates remain location/date specific.
15. RFC Editor. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). Accessed 2026-09-03. Internet Standard defining representation metadata, validators, conditional requests, and range-request semantics used by object APIs.

## Exercises

### Exercise 1

Design a publication protocol for two concurrent writers producing a 48-file daily snapshot. State key grammar, manifest contents, pointer precondition, reader algorithm, timeout reconciliation, and garbage-collection rule. Identify the linearization point and prove why readers cannot observe a mixed committed snapshot under your assumptions.

### Exercise 2

A pipeline stores 6 TiB/day after compression. Compare target sizes of 8 MiB and 256 MiB. Calculate approximate daily object counts and the ratio of per-object PUTs. Then describe at least four costs or performance effects the arithmetic omits and how you would measure them.

### Exercise 3

Specify a safe multipart workflow for a 1.1 TiB export without assuming provider limits. Include how you select part size, persist evidence, retry parts, validate integrity, reconcile a lost completion response, and clean incomplete uploads. Explain which product facts must be retrieved before implementation.

### Exercise 4

Construct a deletion state machine for a versioned, replicated bucket containing regulated customer data. Include logical removal, delete marker/soft delete, noncurrent versions, legal hold, retention expiry, permanent delete, replica/backup propagation, KMS dependencies, and auditable erasure evidence.

### Exercise 5

Fault-test an object-backed analytical dataset. Cover interrupted upload, concurrent publish, corrupt bytes, stale cache, overwrite between range reads, duplicate/missing notifications, incorrect lifecycle filter, permission loss, KMS unavailability, regional/path outage, and inventory lag. Define a finite reconciliation oracle and pass criteria.

## Answers to the Exercises

### Answer 1

Use keys `data/date=<d>/run=<run-id>/part=<stable-id>` and never reuse them. Each manifest records sorted bucket/key/version, length, digest, schema, partition facts, source cut, run, and policy version. Writers verify all 48 members, create immutable manifests, read `current` generation $g$, and conditionally replace it only if $g$ matches. The successful conditional pointer update is the linearization point. A reader resolves one pointer version, validates one immutable manifest, then reads its pinned members. Thus it sees the prior or winning new set, never a list-built mixture. A timeout is reconciled by comparing pointer content/version with the intended manifest digest. Losing or failed-run objects remain attributed to run state and become deletable only after age, retained-snapshot reachability, legal/replication, and rollback checks.

### Answer 2

$6$ TiB is $6\times2^{40}$ bytes. At 8 MiB, $N=6\times2^{40}/(8\times2^{20})=786{,}432$ objects/day. At 256 MiB, $N=24{,}576$ objects/day. The smaller target creates 32 times as many objects and roughly 32 times as many initial PUTs. This omits multipart requests, compression variation, partition skew, query selectivity/ranges, list/HEAD operations, catalog/planner/task overhead, KMS calls, retries, compaction, versions, lifecycle, retrieval, and transfer. Measure object-size and request distributions, query bytes/objects opened, task latency, throttle/error rate, KMS calls, and end-to-end cost by product and workload.

### Answer 3

Retrieve maximum object size, allowed part count, minimum/maximum part sizes, checksum algorithms, completion semantics, list pagination, timeout/error codes, SDK behavior, request pricing, and lifecycle support. Choose $P_s$ so $m=\lceil1.1\ TiB/P_s\rceil$ is safely below the documented limit with bounded worker memory and acceptable retry bytes. Persist upload ID, key, operation/run, encryption/metadata, each part number/range/length/checksum and returned validator. Retry only failed parts under the same identity, complete from retained part evidence, validate final size and supported full-object digest, and on lost completion HEAD the exact destination before any new upload. Abort explicit failures and apply an age-bounded incomplete-upload lifecycle rule with monitoring.

### Answer 4

Model separate transitions: `reachable-current -> logically-removed -> marker-or-noncurrent -> retention-eligible -> permanently-deleted -> replica/backup-expired -> erasure-verified`. A legal hold blocks retention-eligible/permanent deletion; time retention blocks until its authoritative deadline. Each transition records requester, policy, object version, location, result, and next obligation. The workflow enumerates every version and marker, checks replication and separately governed backups, preserves required audit evidence without personal payload, and includes encryption-key state. KMS destruction is not silently substituted for deletion unless policy explicitly treats cryptographic erasure as sufficient and verifies no other key/plaintext copy exists.

### Answer 5

Inject each failure at the real API boundary and assert: no partial upload becomes a committed member; one concurrent writer advances a given pointer generation; digest/semantic validation quarantines corruption; readers pin pointer and object versions despite cache/overwrite; event duplicates produce one effect and missed events are found by inventory; lifecycle canary/dry-run prevents broad loss; denied identity/KMS/region failures preserve prior committed state and meet retry/failover policy; and delayed inventory is labeled by cut/age. For a compatible finite cut, traverse retained manifests to form $R$, acquire authoritative inventory $A$, classify every identity as reachable, retained historical, active, quarantine, scheduled, protected, or unexplained, require `missing = R - A` to be empty, and require no unexplained residue beyond the declared timing bounds.
