---
module_id: LSDS-016
program: Large-Scale Data Systems Engineering
level: 1
module_number: 16
title: Object Storage Semantics
status: complete
last_verified: 2026-09-03
---

# Object Storage Semantics

## One-Page Review

### Governing question

How should applications reason about object identity, atomic replacement, conditional requests, versions, ranges, listings, deletion, and lifecycle when an object store exposes a flat key API rather than mutable filesystem inodes and directories?

### Essential definitions

- A **bucket/container** is a named administrative namespace with policy, location, and lifecycle configuration.
- An **object key** is an opaque byte/string identifier within a bucket; delimiter-rendered folders may be client conventions rather than directories.
- An **object version** or **generation** is an immutable identity for one object value and its version-scoped metadata.
- The **live/current version** is the version returned when a request names only bucket and key under the service contract.
- A **validator** such as an entity tag identifies a selected representation for conditional requests; its format and relation to content are service-specific.
- A **precondition** makes an operation apply only if current state matches an expected version, validator, existence, or timestamp.
- A **range read** returns a declared byte interval of one selected version.
- A **delete marker** is a current version-like tombstone that can hide older versions without erasing them immediately.
- **Soft delete** retains deleted state for recovery during a policy window.
- **Lifecycle management** applies retention, transition, expiration, and deletion policies asynchronously under documented rules.

### Central model, mechanism, or theorem

Model an object name as `(bucket,key)` and each committed value as immutable version `v=(generation, bytes, metadata)`. A key-only read selects the service-defined current version; an exact-version read selects `v`. A conditional mutation is safe when the origin evaluates its precondition atomically against current state immediately before the mutation and returns the resulting version identity.

Single-key atomic replacement does not imply a transaction across keys, a filesystem rename, an atomic recursive directory operation, or an application-consistent dataset. Multi-object publication normally uses immutable objects plus one conditional manifest/pointer update. Correct clients persist exact version/validator identifiers and never infer identity from key, timestamp, size, or a human-readable ETag.

### Critical invariants

- Bucket, key, version/generation, and tenant/account together identify object state.
- A successful write exposes a complete representation, never partially overwritten bytes, under the service contract.
- Lost-update protection uses an atomic precondition against the current selected version.
- Range responses bind exact version, total length, interval, and integrity evidence.
- Key prefixes and delimiters do not acquire directory invariants unless the API explicitly provides them.
- Delete, delete marker, soft delete, version expiration, retention lock, and physical erasure remain distinct.
- Listing semantics are taken from the current service contract and never inferred from GET behavior.
- Retry preserves operation/body identity or resolves the prior outcome before creating another version.
- Lifecycle automation cannot override active retention, holds, authorization, or recovery policy silently.

### Common failures

Frequent failures are treating keys as paths, assuming rename exists, overwriting after an unguarded read, using timestamps instead of strong validators, assuming every ETag is a content hash, resuming a range against a newer version, interpreting delete success as physical erasure, forgetting noncurrent versions and delete markers, inferring list consistency from object GET, treating prefix deletion as atomic, retrying a lost-response PUT with changed body, and applying lifecycle rules without version, hold, billing, or governance analysis.

### Compact example

Client A reads key `model/current` at generation 41. Client B replaces it and receives generation 42. A's update with precondition “generation must equal 41” fails rather than overwriting B. If A instead performs an unconditional PUT, it creates/replaces the current value according to the store contract and can cause a lost update. The precondition is concurrency control; the key name alone is not.

### Connections

[LSDS-011](011-distributed-block-storage.md) supplies physical block/object identity and ranges. [LSDS-012](012-metadata-servers-and-namespace.md) supplies names, versions, transactions, and snapshots. [LSDS-014](014-read-and-write-pipelines.md) supplies conditional transfer, retries, and integrity. [LSDS-017](../ROADMAP.md) develops multipart upload and commit; [LSDS-018](../ROADMAP.md) deepens listing and metadata consistency.

## Governing Question

Object storage presents a deceptively small interface: put bytes under a key, get them, list names, and delete them. At scale, the meaning depends on account and bucket identity, versioning mode, consistency contract, conditional headers, metadata fields, multipart state, retention, lifecycle, encryption, replication, and asynchronous control-plane changes.

Unlike a POSIX filesystem, an object store commonly replaces an entire object value atomically instead of exposing arbitrary shared in-place writes. Keys containing `/` may render as folders, but there may be no inode, parent directory, link count, rename transaction, or directory permission traversal. Copy-then-delete is not atomic rename.

The governing question is how to build correct workflows from the exact contract. Use immutable versions and conditional mutations as the primitive. Treat listings, metadata, lifecycle, and deletion as separately documented surfaces. Build multi-object commits explicitly rather than importing filesystem semantics.

## Why This Matters

Data lakes, backups, media systems, model registries, artifacts, and application blobs rely on object stores. A lost update to a manifest can publish an inconsistent dataset. A range retry against a replaced object can splice bytes from two versions. A delete marker can hide bytes that continue to incur cost and retention exposure.

Object APIs are designed for enormous namespaces and independent keys. Their strengths—whole-object atomicity, versioning, conditional requests, horizontal distribution, and lifecycle—support reliable patterns when used deliberately. They do not automatically provide cross-key transactions, append, locks, or directory atomicity.

Provider semantics evolve. Historical assumptions about eventual read-after-write or LIST behavior may no longer describe current services. Conversely, one provider's strong single-key and listing contract cannot be transferred to another endpoint, gateway, cache, replication layer, or older compatibility mode without verification.

Governance is inseparable from semantics. Versioning, soft delete, replication, object lock, backups, caches, and lifecycle all affect when information remains recoverable and when it is truly erased. Encryption keys and metadata can be independent recovery dependencies.

## Prerequisites and Retrieval

Recall partition identity and range/hash placement from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md), serialization from [LSDS-008](008-serialization-across-workers.md), and failures from [LSDS-009](009-cluster-failure-assumptions.md).

Retrieve block handles, range mapping, placement, and integrity from [LSDS-011](011-distributed-block-storage.md); namespace identity, transactions, snapshots, and garbage-collection roots from [LSDS-012](012-metadata-servers-and-namespace.md); protection versions from [LSDS-013](013-replication-and-erasure-coding.md); and acknowledgement, retries, conditionality, and stale reads from [LSDS-014](014-read-and-write-pipelines.md).

You should understand HTTP methods/status codes, headers, byte ranges, hashes, opaque validators, optimistic concurrency, immutable data, versioning, caches, encryption, retention, and eventual asynchronous workflows.

## Learning Objectives

After completing this module, you should be able to:

- distinguish bucket/container, key, live value, immutable version, metadata, and physical fragments;
- explain why prefix/delimiter folders differ from filesystem directories;
- state single-object atomicity and avoid assuming multi-object transactions;
- use create-if-absent and compare-and-swap-style conditional requests;
- distinguish opaque ETags, content digests, generations, and timestamps;
- bind range and resumed reads to one exact version;
- reason about versioning, delete markers, soft delete, retention, and lifecycle;
- design immutable-object plus manifest publication workflows;
- handle ambiguous PUT/DELETE outcomes and retry safely;
- evaluate listings separately from direct object reads;
- account versions, metadata, requests, transitions, retrieval, and delete lag;
- specify authorization, encryption, residency, audit, and erasure evidence; and
- test concurrency, cache, pagination, lifecycle, and recovery boundaries.

## Core Exposition

### Object identity and naming

The minimum logical name is usually `(account/project, bucket/container, key)`. Region, endpoint, API version, and tenant context may also affect resolution. Store these boundaries explicitly in durable references rather than concatenating an ambiguous URL.

An object version/generation identifies one committed value under a key. Replacing a key creates a new logical value and, when versioning retains history, a new immutable version. The same key can therefore identify different bytes over time.

Keys are often case-sensitive opaque strings with encoding, length, or reserved-character rules. Normalize only according to the service and application contract. Two visually equivalent Unicode strings can be distinct keys.

### Flat namespace versus directories

Clients often group keys by a prefix such as `tenant/date/file`. A delimiter can make a LIST response synthesize common prefixes that resemble folders. This does not prove a stored directory object or atomic parent-child relationship.

Creating `a/b` need not create `a`; deleting every child need not delete a folder; permissions may attach to bucket or object rather than each path ancestor. Some services add hierarchical namespace modes, but that is a different explicit contract.

There is commonly no atomic rename. Copy creates a new object/version, then delete changes the old key. Between operations both, either, or neither may be visible depending on failure and contract. Identity, metadata, encryption, billing, and timestamps may change.

### PUT and whole-object atomicity

A successful PUT commits one complete object representation under the service's current consistency contract. Concurrent unconditional writes to one key are ordered somehow by the service, but application intent can be lost: the later accepted value becomes current without proving it incorporated the earlier value.

The request should bind content length, integrity digest where supported, content type/encoding, application schema, metadata, encryption/key context, retention, and idempotency expectations. Validate the returned version/generation and store it.

Whole-object atomicity does not mean the transport is one packet. Multipart upload can assemble parts before a commit, developed in LSDS-017. Readers should not see an incomplete new representation under the promised atomic contract.

### GET, HEAD, and selected representations

A key-only GET selects the current representation according to service semantics. A version-specific GET selects historical state. HEAD-like metadata retrieval avoids body transfer but must be interpreted under the same version/condition contract.

Metadata includes service fields—length, type, modification time, validator, version, storage class, checksums, encryption—and user metadata. Some fields are version-scoped; some bucket policies are evaluated currently. Persist what the workflow needs instead of assuming HEAD can reconstruct historical policy.

Caches and gateways can alter observations. Bind cache keys to authorization and version where appropriate, honor validators, and verify that intermediaries preserve conditional and range semantics.

### Validators and entity tags

An ETag is an opaque validator for a selected representation. Only the service defines how it is generated. It may be a content digest in one mode and not in another, especially with multipart upload, encryption, compression, or transformations.

Use a documented end-to-end checksum for integrity and a validator/generation for concurrency unless the contract explicitly unifies them. Comparing human-readable ETags as hashes can silently fail across implementations.

Modification timestamps have coarse resolution, clock semantics, and collision risks. Strong validators or generation numbers are safer for lost-update prevention when supported.

### Conditional creation and replacement

Create-if-absent tests that no current object satisfies the service's existence rule. HTTP `If-None-Match: *` is a common mechanism. With versioning, a delete marker may count as no current object for a provider-specific conditional write; verify exact behavior.

Compare-and-swap replacement reads a version/ETag, computes a new value, and sends `If-Match` or a generation-match precondition. The origin evaluates the condition atomically immediately before mutation. A mismatch is a normal concurrency result, not an infrastructure failure.

Preconditions belong on COPY, metadata updates, DELETE, and manifest publication too. Distinguish source and destination preconditions for copy/rewrite operations.

### Lost update and merge

Suppose two clients read manifest version 7, independently add entries, and PUT unconditionally. One result overwrites the other. Strong read consistency does not prevent this; both clients made valid reads followed by unguarded writes.

With a version precondition, one write succeeds and the other receives conflict/precondition failure. The loser rereads, validates application invariants, merges if appropriate, and retries with the new expected version. Automatic byte-level retry is unsafe if merge meaning is domain-specific.

For high-contention keys, use a database, queue/log, sharded manifests, or serialization service rather than an unbounded compare-and-swap retry storm.

### Range reads and resume

A byte range selects part of one representation. Inclusive HTTP byte ranges differ from half-open intervals often used in code; convert carefully. Validate status, `Content-Range`, total length, returned length, version/validator, and checksum scope.

Resume must target the same immutable version. If a key was replaced, appending bytes from the new version to a cached prefix produces a synthetic object that never existed. Use exact generation/version or `If-Range` with a strong validator where semantics permit.

Compression and content encoding can change what range offsets address. Many tiny or overlapping ranges can be inefficient or rejected and can become a denial-of-service vector.

### DELETE semantics

An unversioned delete usually removes the current key mapping under the service consistency contract. In a versioned bucket, deleting without a version can create a delete marker that becomes current while older data versions remain retrievable by version identity.

Deleting a specific version removes that version subject to authorization, retention, hold, replication, and soft-delete behavior. A successful API response does not necessarily prove physical media erasure across replicas, backups, caches, logs, and failed devices.

Delete of an absent key may be idempotently successful. This simplifies retry but does not prove which prior version was deleted unless the request carries a version or precondition.

### Versioning and recovery

Versioning protects against accidental overwrite and deletion by retaining noncurrent versions. It consumes storage, request, listing, replication, and lifecycle cost. Noncurrent versions can have different metadata or permissions from the live value.

Recovery commonly makes a historical value current by copying/restoring it into a new version; it does not necessarily rewind history. Record the selected source generation and resulting generation.

Version IDs, delete markers, and ordering are provider-defined. Do not sort opaque version IDs or use timestamps alone as authority. Pagination must not skip or duplicate state when concurrent mutations occur.

### Soft delete, retention, and holds

Soft delete retains otherwise deleted data for a window. Versioning retains replacement/deletion history. Object lock/retention prevents deletion until a deadline or indefinitely under a legal hold. These mechanisms compose but are not synonyms.

Retention must be authorized and clock semantics trustworthy. Governance and compliance modes can differ in bypass permissions. Lifecycle expiration cannot remove a version protected by a stronger hold.

Recovery policy must include keys and metadata needed to discover and authorize retained objects. “Recoverable” bytes without version index, encryption keys, or permissions may be unusable.

### Lifecycle transitions

Lifecycle rules select objects/versions by age, prefix/tag, current/noncurrent status, count, storage class, or other provider-specific predicates. Actions can transition tier, expire current values, remove noncurrent versions, or abort incomplete multipart uploads.

Evaluation and action are asynchronous. A rule becoming true at midnight does not imply immediate deletion. Billing can change before or after physical action according to contract. Observe actual lifecycle status rather than scheduling downstream work from guessed timing.

Rule changes require simulation over inventory, canary scope, review, and rollback planning. An overbroad prefix or age predicate can delete an enormous namespace.

### Listing and pagination

LIST returns keys or versions under a filter and pagination scheme. Current major services may provide strong listing consistency, but clients must verify the exact endpoint and operation. GET consistency does not logically imply LIST consistency.

Continuation tokens are opaque. Do not synthesize or sort them. Concurrent writes and deletes interact with pagination according to the service contract; deduplicate by exact identity when building inventories.

Listing live keys hides noncurrent versions and delete markers unless a version-list API is used. A deletion audit must inspect every retained representation, not just ordinary LIST.

### Multi-object publication

Object stores commonly do not offer a transaction across arbitrary keys. Publish datasets by writing immutable uniquely named objects first, verifying them, then conditionally updating one small manifest or pointer from expected old version to new.

Readers resolve one manifest generation and read only objects/digests it names. Failed writers leave unreferenced candidates that garbage collection removes after grace and reconciliation. The manifest commit is the visibility point, not the last data upload by wall clock.

If the manifest itself exceeds one object or is highly contended, introduce levels, partitions, a catalog/transaction service, or immutable log. Do not approximate a transaction with “upload in filename order.”

### Copy, compose, and rewrite

Server-side copy or compose can avoid downloading bytes to the client. It is still a new destination write with source and destination version/condition concerns. Preserve or replace metadata, encryption, storage class, retention, and checksums explicitly.

Large rewrite operations can be resumable and multi-step internally. Store provider continuation state securely and bind it to exact source and destination preconditions. A successful destination does not authorize deleting the source automatically.

Composed objects can have part/component limits and validator behavior different from simple PUT. Record an application digest for portable integrity.

### Retry and ambiguous outcomes

A network timeout after PUT, COPY, or DELETE leaves an ambiguous outcome. Repeating identical immutable PUT content at the same unique key may be effectively safe, but can create extra versions or charges. A changed body under the same retry intent is unsafe.

Use operation identity where supported, conditional creation, content digest, exact target generation, and a subsequent HEAD/GET/list-versions query to resolve. For DELETE, precondition on version/ETag so a retry cannot delete a newer replacement.

Classify throttling, transient service failure, precondition failure, authorization failure, invalid range, retention denial, and checksum mismatch separately. Blindly retrying conflicts or policy denials creates load without progress.

### Metadata and schema

User metadata is usually small strings and may have case/canonicalization limits. Tags can support policy but may be governed by separate consistency and authorization behavior. Store authoritative schemas and provenance in durable manifests when they exceed header semantics.

Content type and encoding affect downstream interpretation. A byte-perfect object can still be semantically invalid. Validate file format, schema, row counts, partition boundaries, and application digest before publication.

Changing metadata may create a new metageneration, new object version, or server-side rewrite depending on provider. Use the provider's metadata preconditions rather than assuming data generation alone protects it.

### Security and tenancy

Authorize account, bucket, key/prefix, operation, version, conditions, network path, and encryption key. Pre-signed URLs/tokens should be narrowly scoped and short-lived; log exposure can grant object access.

Object names and metadata leak structure, identities, dates, classifications, and activity even when payloads are encrypted. Avoid secrets and sensitive personal information in keys. Protect inventory, access logs, lifecycle rules, and replication configuration.

Server-side and client-side encryption have different key, metadata, range, copy, and recovery behavior. Test key rotation and disaster restore. One deleted key can erase all versions cryptographically; one retained key can prolong disclosure.

### Capacity, cost, and observability

Account current and noncurrent bytes, delete markers, soft-deleted bytes, incomplete multipart parts, replication/coding, metadata, minimum storage duration, early deletion, requests, LIST pagination, retrieval, transition, egress, checksums, and inventory.

Metrics include operation latency/error by method/status, conditional conflict rate, ambiguous retries, versions/key, noncurrent age/bytes, delete markers, lifecycle backlog/action, incomplete uploads, range amplification, checksum failures, cache hits, and authorization denials.

Audit events bind principal, bucket/key/version, operation, source/destination conditions, validator/generation, digest, encryption/key, retention/hold, result, and request ID while minimizing sensitive names.

## Definitions and Notation

Let bucket `b` map key `k` to ordered committed versions `V(b,k)=[v_1,...,v_n]` under a service-defined current selection. Each `v_i` contains generation/version ID `g_i`, bytes `B_i`, metadata `M_i`, and state such as live value or delete marker.

A key-only selection `Current(b,k)` returns a live version or absence according to delete-marker and versioning semantics. Exact `Get(b,k,g)` selects one generation. Never infer `g` from modification time, size, or key.

Conditional replacement `PutIf(b,k,g_expected,B_new)` succeeds only if the origin's current validator/generation equals `g_expected` at evaluation; successful response returns `g_new`. Create-if-absent uses an explicit absence predicate defined by the provider.

For object length `L`, half-open requested range `[a,a+n)` is valid when `0<=a<=L`, `n>=0`, and `a+n<=L`. HTTP bytes syntax often expresses a nonempty equivalent as inclusive `a-(a+n-1)`. Bind it to one version and validate total/returned lengths.

Let manifest version `m` name immutable objects `(b,k,g,digest)`. A dataset publication is complete when all referenced versions validate and a conditional pointer update atomically selects `m`. Candidate object existence alone does not imply dataset membership.

## Mechanisms, Invariants, or Proof Structure

To design or audit an object-store workflow:

1. Name account, bucket/container, key encoding, region/endpoint, and tenant boundary.
2. Define live selection, immutable versions/generations, validators, and metadata scope.
3. State current PUT/GET/HEAD/LIST/DELETE consistency and single-operation atomicity.
4. Use exact preconditions for creation, replacement, metadata change, copy, and delete.
5. Bind ranges, resumes, caches, and integrity checks to one exact representation.
6. Model delete markers, noncurrent versions, soft delete, holds, lifecycle, and erasure.
7. Build multi-object visibility with immutable data and conditional manifest commit.
8. Resolve timeout outcomes and retry without changed bodies or newer-version damage.
9. Account every representation, request, tier, transition, recovery copy, and lag.
10. Test concurrency, pagination, cache, lifecycle, policy, key loss, and disaster restore.

The fixture models a versioned key with conditional replacement and a delete marker. It is not a provider implementation and does not model HTTP caches, replication, lifecycle timing, or authorization.

<!-- bijux-verify: {"id":"object-version-preconditions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"created_generation=1 current=b'alpha-data' range_2_7=b'pha-d'\nupdated_generation=2 current=b'beta-data' stale_update=precondition_failed\ndelete_marker_generation=3 current=None exact_v1=b'alpha-data' exact_v2=b'beta-data'\nversions=(1, 2, 3) live_keys=() retained_payload_bytes=19\n","stderr":""}} -->
```python
versions = {}
next_generation = 1


def put_if(key, body, *, expected):
    global next_generation
    current = versions.get(key, [])[-1] if versions.get(key) else None
    current_generation = (
        None if current is None or current["delete_marker"]
        else current["generation"]
    )
    if current_generation != expected:
        return "precondition_failed", None
    entry = {
        "generation": next_generation,
        "body": body,
        "delete_marker": False,
    }
    next_generation += 1
    versions.setdefault(key, []).append(entry)
    return "committed", entry["generation"]


def delete(key, *, expected):
    global next_generation
    current = versions[key][-1]
    if current["delete_marker"] or current["generation"] != expected:
        return "precondition_failed", None
    marker = {
        "generation": next_generation,
        "body": b"",
        "delete_marker": True,
    }
    next_generation += 1
    versions[key].append(marker)
    return "committed", marker["generation"]


def current_body(key):
    current = versions[key][-1]
    return None if current["delete_marker"] else current["body"]


def exact_body(key, generation):
    entry = next(v for v in versions[key] if v["generation"] == generation)
    return None if entry["delete_marker"] else entry["body"]


status, v1 = put_if("model/current", b"alpha-data", expected=None)
assert status == "committed"
print(
    f"created_generation={v1} current={current_body('model/current')!r} "
    f"range_2_7={current_body('model/current')[2:7]!r}"
)
status, v2 = put_if("model/current", b"beta-data", expected=v1)
stale, _ = put_if("model/current", b"stale", expected=v1)
print(
    f"updated_generation={v2} current={current_body('model/current')!r} "
    f"stale_update={stale}"
)
status, marker = delete("model/current", expected=v2)
print(
    f"delete_marker_generation={marker} current={current_body('model/current')} "
    f"exact_v1={exact_body('model/current', v1)!r} "
    f"exact_v2={exact_body('model/current', v2)!r}"
)
all_versions = tuple(v["generation"] for v in versions["model/current"])
live_keys = tuple(k for k in versions if current_body(k) is not None)
retained = sum(len(v["body"]) for v in versions["model/current"])
print(
    f"versions={all_versions} live_keys={live_keys} "
    f"retained_payload_bytes={retained}"
)
```

The delete marker hides both payload versions from a current-key read while exact-version reads remain possible. The 19 retained payload bytes show why live-key inventory is not a storage or erasure inventory. Real providers define version IDs, marker behavior, conditional evaluation, and retention precisely.

Correctness proof establishes exact identity, atomic precondition evaluation, complete representation visibility, and manifest reachability. Performance, durability, lifecycle timing, physical erasure, and governance require separate evidence.

## Alternatives and Trade-Offs

Unconditional overwrite is simple for single-writer or last-write-wins use and loses concurrent intent. Conditional overwrite detects conflict and may retry heavily. Unique immutable keys avoid overwrite and require a pointer/catalog.

Versioning improves recovery and raises storage, listing, lifecycle, and privacy costs. Unversioned storage simplifies current state and weakens recovery. Soft delete offers a bounded safety net and delays erasure.

Key prefixes are simple and portable. Hierarchical namespace modes add directory/rename semantics and provider coupling. An external catalog enables rich transactions and becomes another consistency and recovery dependency.

ETags are portable HTTP validators when used opaquely. Provider generations can offer clearer version identity and reduce portability. Application digests provide end-to-end integrity but not origin concurrency unless accepted as a precondition.

Whole-object replacement makes immutable workflows robust and amplifies small changes. Multipart and compose reduce transfer costs while complicating validators, candidates, and cleanup. Packing tiny objects lowers request/metadata cost and couples lifecycle and retrieval.

Strong listing simplifies inventories and publication discovery. Explicit manifests remain valuable for dataset membership, schema, digest, and atomic multi-object visibility. Polling LIST as a commit protocol is usually weaker and more expensive.

Server-side encryption simplifies operations and binds recovery to provider keys/policy. Client-side encryption limits provider plaintext access and complicates ranges, deduplication, copy, metadata, and key recovery.

Aggressive lifecycle expiration controls cost and narrows recovery. Long retention aids recovery and increases disclosure, compliance, and cost. Classify data and approve policies by consequence.

## Failure Modes and Misconceptions

- **“A key is a pathname.”** Slashes can be opaque characters and prefixes can be presentation conventions.
- **“Creating `a/b` creates directory `a`.”** Not in a flat namespace unless explicitly implemented.
- **“Copy then delete is atomic rename.”** It exposes two operations and can change identity/metadata.
- **“Strong read-after-write prevents lost updates.”** Unguarded concurrent read-modify-write still loses intent.
- **“ETag always equals an MD5 digest.”** Treat validators as opaque unless the service contract says otherwise.
- **“Last-Modified is a unique version.”** Timestamps can collide, round, and reflect service-specific events.
- **“A successful PUT proves my intended version is current forever.”** Later writes can replace it; retain returned identity.
- **“Range resume by key is safe.”** Replacement can splice two representations; bind exact version/validator.
- **“Delete removes every byte immediately.”** Versions, markers, soft delete, replication, caches, and backups remain.
- **“Ordinary LIST shows retained versions.”** A version-list surface is usually required.
- **“GET consistency proves LIST consistency.”** Verify each operation's contract independently.
- **“Prefix deletion is one transaction.”** Batch APIs can have per-object outcomes and partial failure.
- **“Version IDs sort by creation time.”** They are often opaque.
- **“A precondition failure should be retried unchanged forever.”** It is a concurrency result requiring reread/merge or abort.
- **“Lifecycle executes exactly when an object reaches age.”** Evaluation/action are asynchronous and provider-specific.
- **“Object lock is backup.”** It prevents certain deletion; it does not create an independent recoverable copy.
- **“Encryption guarantees erasure.”** Key scope, caches, plaintext copies, backups, and key retention determine that claim.
- **“Immutable objects make the dataset atomic.”** A manifest or transactional catalog defines multi-object visibility.
- **“Checksum success proves semantic validity.”** Schema, format, provenance, and application invariants remain.
- **“Provider documentation transfers to every S3-compatible endpoint.”** Verify the actual implementation and version.

## Worked Examples

### Example 1

**Situation:** Two writers create the same key only if absent. **Reasoning:** Use the service's atomic absence precondition. One succeeds; the other receives precondition/conflict behavior. A prior HEAD followed by unconditional PUT has a race.

### Example 2

**Situation:** Two clients update a JSON manifest read at generation 12. **Reasoning:** Both send a generation/ETag match. One commits generation 13; the other rereads 13, performs a domain-aware merge, and retries against 13 or aborts.

### Example 3

**Situation:** A 1-GiB download stops after 600 MiB and the key is replaced. **Reasoning:** Resume against the original exact version or strong `If-Range` validator. A key-only range can append bytes from the replacement and corrupt the local result.

### Example 4

**Situation:** A versioned key is deleted without a version. **Reasoning:** A delete marker can become current while old versions remain. Ordinary GET reports absence; version-specific recovery and billing still see retained bytes.

### Example 5

**Situation:** An application wants atomic rename of a 10-TiB object. **Reasoning:** A copy/delete workflow is not atomic and may move data or metadata. Prefer immutable identity plus a conditional small pointer/manifest update when application semantics allow.

### Example 6

**Situation:** A lifecycle rule expires `records/` after 30 days but a legal hold exists. **Reasoning:** The stronger hold prevents eligible deletion under the documented precedence. Audit rule evaluation and retained versions; do not assume physical erasure at day 30.

### Example 7

**Situation:** A multipart encrypted object's ETag differs from a local MD5. **Reasoning:** This is not sufficient evidence of corruption. Use documented checksum fields or an application digest and treat ETag as an opaque validator.

### Example 8

**Situation:** A timeout follows a conditional PUT with known digest. **Reasoning:** Query the exact key/version state and operation/request evidence. If the intended body committed, return that result; if the precondition is still valid, retry identically; never change the body under the same intent silently.

### Example 9

**Situation:** A live-key LIST is empty but storage billing is nonzero. **Reasoning:** Inspect noncurrent versions, delete markers, soft-deleted objects, incomplete multipart uploads, minimum-duration charges, replicas, and asynchronous lifecycle backlog.

### Example 10

**Situation:** A research dataset has 10,000 immutable parts. **Reasoning:** Validate every exact generation and digest, publish one versioned manifest conditionally, make readers pin that manifest, retain candidate grace, and obtain data-owner, ethics/privacy, records, security, accessibility, and recovery review.

## Cross-Program Connections

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies HTTP semantics, validators, conditional requests, idempotency, pagination, status codes, and rate limits. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistency, atomic registers, versioning, concurrency, replication, and failure ambiguity.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes object layouts, partition prefixes, manifests, range reads, publication, compaction, and lifecycle. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns dataset identity, metadata, lineage, retention, residency, authoritative versions, and erasure policy.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies scoped authorization, signed requests, encryption, keys, audit, tenant isolation, and deletion evidence. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies buckets, policies, observability, quotas, cost, multi-region design, and operational recovery.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies optimistic concurrency, transactions, MVCC, catalogs, indexes, and garbage collection. [Operating Systems](../../22-operating-systems/ROADMAP.md) provides the filesystem contrasts: directories, inodes, links, rename, open-unlinked files, and caches.

HTTP defines opaque validators, precondition evaluation, and range semantics. Current Amazon S3, Google Cloud Storage, and Azure Blob documentation illustrates strong object operations, conditional writes, generations/versions, delete retention, and provider-specific behavior. Those examples are evidence, not a universal compatibility specification.

## References

- IETF, [*HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), RFC 9110, 2022. Standards-track methods, representation metadata, ETags, conditional requests, ranges, and status semantics.
- Amazon Web Services, [*Amazon S3 Data Consistency Model*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel), checked 2026-09-03. Official current strong PUT/DELETE/GET/LIST and single-key atomicity contract.
- Amazon Web Services, [*How to Prevent Object Overwrites with Conditional Writes*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html), checked 2026-09-03. Official current create-if-absent, ETag match, conflict, and versioned delete-marker behavior.
- Amazon Web Services, [*Using Versioning in S3 Buckets*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html), checked 2026-09-03. Official current version IDs, current/noncurrent objects, overwrite, and delete-marker model.
- Google Cloud, [*Cloud Storage Consistency*](https://cloud.google.com/storage/docs/consistency), checked 2026-09-03. Official current object read/write/delete/list consistency and cache caveats.
- Google Cloud, [*Request Preconditions*](https://cloud.google.com/storage/docs/request-preconditions), checked 2026-09-03. Official current generation, metageneration, ETag, source/destination, and conditional request semantics.
- Google Cloud, [*Object Versioning*](https://cloud.google.com/storage/docs/object-versioning), checked 2026-09-03. Official current live/noncurrent generation, metadata, version deletion, and lifecycle behavior.
- Microsoft, [*Manage Concurrency in Blob Storage*](https://learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage), checked 2026-09-03. Official current ETag, conditional header, optimistic/pessimistic, and last-writer-wins behavior.
- Microsoft, [*Soft Delete for Blobs*](https://learn.microsoft.com/en-us/azure/storage/blobs/soft-delete-blob-overview), checked 2026-09-03. Official current soft delete, versioning composition, retention window, and recovery guidance.
- Microsoft, [*Delete Blob*](https://learn.microsoft.com/en-us/rest/api/storageservices/delete-blob), checked 2026-09-03. Official current conditional delete, snapshots, leases, soft-delete, and uncommitted-block behavior.

## Exercises

### Exercise 1

Design a lost-update-safe workflow for updating `catalog/current.json` when many clients may modify it. Include validators/generations, merge, retry limits, and a high-contention alternative.

### Exercise 2

An object is 1,000 bytes. Convert half-open ranges `[0,100)`, `[100,1000)`, and `[999,1000)` to HTTP inclusive byte ranges, and state the checks required on each response.

### Exercise 3

Explain the states and recovery options after a key with versions `v1`, `v2`, and current `v3` receives a key-only delete marker, then the marker is deleted explicitly.

### Exercise 4

Design an atomic-publication pattern for 50,000 data objects without assuming multi-key transactions or listing as the commit signal.

### Exercise 5

Specify deletion and review evidence for sensitive archival objects under versioning, cross-region replication, soft delete, lifecycle, legal hold, caches, and client-side encryption.

## Answers to the Exercises

### Answer 1

GET/HEAD the exact current representation and retain its strong ETag or generation plus application digest. Parse and validate the catalog, apply one domain mutation, then PUT with an origin-evaluated match precondition. On conflict, reread, revalidate, and perform a domain-aware merge; bound retries with jitter and surface an explicit conflict if intent cannot merge safely. Record the returned new version. If contention causes repeated conflicts or catalogs grow large, route mutations through a transactional database/log/serialized coordinator or shard immutable manifests rather than creating a compare-and-swap storm.

### Answer 2

The inclusive HTTP ranges are `bytes=0-99`, `bytes=100-999`, and `bytes=999-999`. Bind each request to the same exact immutable version or strong validator. Validate partial-content status, `Content-Range`, total length 1,000, returned length 100/900/1, validator/generation, content encoding, authorization, and checksum scope. Reject a full or differently versioned response unless the client deliberately handles it.

### Answer 3

The marker becomes current, so a key-only GET normally reports absence while `v1`, `v2`, and `v3` remain addressable by exact version subject to policy. Ordinary live-key LIST can hide the key; version listing shows history and marker. Deleting the marker by exact version exposes the prior latest data version—typically `v3`—as current under the provider contract; it does not create new bytes. Soft delete, retention, replication, lifecycle, permissions, and concurrent versions can alter allowed operations, so retain exact IDs and verify current state afterward.

### Answer 4

Write each data object to a unique immutable key and record bucket, key, exact version, length, application digest, schema, and provenance. Verify all 50,000 versions, then write an immutable manifest containing that inventory and validate its digest. Conditionally update one small well-known pointer from its expected old generation to the new manifest generation. Readers pin one pointer/manifest version and never discover dataset membership by a concurrent LIST. A failed writer leaves candidates; a reconciler removes only unreferenced objects after sufficient grace, active-writer, snapshot, hold, and retry checks.

### Answer 5

Inventory every current/noncurrent version, delete marker, soft-deleted representation, replica region, cache, incomplete upload, lifecycle rule/action, backup, encryption envelope, and key. Bind deletion requests to exact versions and preconditions; prove legal-hold and retention authorization before action. Account replication/lifecycle lag and failed media, invalidate caches and credentials, and retain tamper-evident service/request/audit evidence. For client-side encryption, map all ciphertext copies to key versions and distinguish cryptographic erasure from physical deletion while preserving any mandated records. Restore-test before destructive policy changes. Named review includes archive/data owners, records/legal/privacy, security/key management, regional/residency authorities, platform/storage operators, accessibility, affected-community or ethics representatives where applicable, and independent assurance. A successful key-only DELETE is not sufficient erasure evidence.
