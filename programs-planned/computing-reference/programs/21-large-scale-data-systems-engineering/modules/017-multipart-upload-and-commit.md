---
module_id: LSDS-017
program: Large-Scale Data Systems Engineering
level: 1
module_number: 17
title: Multipart Upload and Commit
status: complete
last_verified: 2026-09-03
---

# Multipart Upload and Commit

## One-Page Review

### Governing question

How can a client upload a large object in parallel, resume after interruption, verify every part, and publish exactly one complete object without exposing partial state, leaking abandoned parts, or misinterpreting an ambiguous completion response?

### Essential definitions

- An **upload session** is a server-created identity binding destination, metadata, policy, and in-progress parts or byte ranges.
- An **upload ID/session URI** is the capability used to address that session; it can be security-sensitive.
- A **part** or **chunk** is a numbered/offset transfer unit stored before final object visibility.
- A **part manifest** records ordered part identities, lengths, validators, and checksums intended for completion.
- **Completion/commit** atomically constructs or publishes the final object from the declared parts under the service contract.
- An **uncommitted part/block** consumes storage but is not yet part of a visible final object.
- **Resume** discovers authoritative received progress and retransmits only missing or invalid ranges.
- **Abort** requests disposal of an incomplete session; concurrent part requests and asynchronous cleanup need explicit handling.
- A **composite checksum** derives from part checksums; a **full-object checksum** covers the concatenated logical bytes.
- An **ambiguous completion** occurs when the commit may have succeeded but the response was lost or timed out.

### Central model, mechanism, or theorem

Let upload session `u` target `(bucket,key)` and contain authoritative part map `P_u(number)=(length,validator,digest)`. Completion supplies an ordered manifest `M=[(number,validator)]`; the service validates that every selected part belongs to `u`, matches its validator, obeys part constraints, and concatenates bytes in manifest/part-number order into one object version. Parts not named by `M` are not implicitly object data.

Parallel upload changes scheduling, not logical order. Retry of a part must preserve session, number/offset, length, and bytes; some services replace the prior value for the same part number. Final success is proved by the returned object version plus length and end-to-end integrity, not by counting successful part requests. Completion should use destination preconditions when concurrent writers matter.

### Critical invariants

- Session identity binds exact destination, principal, metadata, encryption, and policy context.
- Each part/range has one authoritative position, valid length, and verified content identity.
- Client manifests are durable, versioned, and reconciled against server-reported parts after restart.
- Concurrency and buffered bytes are bounded independently.
- Commit selects a complete ordered compatible part set and exposes one complete object version.
- Completion retry resolves prior outcome before creating a different upload or overwriting a newer object.
- Destination create/replace preconditions are evaluated at commit, not merely initiation.
- Abort and lifecycle cleanup never delete an already committed object version.
- Incomplete sessions, parts, request costs, credentials, and cleanup lag are observable.

### Common failures

Frequent failures are using filenames as upload identity, losing the session URI, trusting only local progress, reusing a part number with different bytes accidentally, sorting part numbers lexically, exceeding memory by bounding task count but not bytes, assuming part ETags are portable content hashes, completing without a full-object digest, checking destination absence only at initiation, starting a new upload after an ambiguous completion, aborting while part requests remain in flight, and ignoring storage/cost/security exposure of incomplete sessions.

### Compact example

A 25-GiB object split into 128-MiB parts has 200 parts. With eight concurrent parts, ideal scheduling needs 25 waves and buffers up to 1 GiB of payload if every worker holds a full part. Actual memory is higher. Upload order can be arbitrary; completion order must produce parts 1 through 200. A lost completion response is resolved by querying the destination version/session rather than immediately initiating a second upload.

### Connections

[LSDS-014](014-read-and-write-pipelines.md) supplies packets, checksums, backpressure, and ambiguous outcomes. [LSDS-016](016-object-storage-semantics.md) supplies versions, conditional writes, and whole-object visibility. [LSDS-018](../ROADMAP.md) deepens listing consistency, and [LSDS-019](../ROADMAP.md) develops small-file pathologies.

## Governing Question

Single-request upload makes one large transfer vulnerable to any connection failure and can underuse available bandwidth. Multipart or resumable protocols divide work so independent parts can transfer concurrently and retry. The service retains candidate bytes until an explicit completion selects them or an abort/expiration removes them.

This creates a small transaction protocol. Initiation declares destination metadata and returns a capability. Part uploads mutate session state. Listing/querying reconciles progress. Completion validates a manifest and publishes the object. Abort changes cleanup eligibility. A crash can occur between every pair of steps.

The governing question is how to preserve exact bytes and intent across concurrency, retry, restart, and uncertain responses. The client needs a durable local upload record, and the service needs versioned session state. Neither “all workers succeeded” nor “the SDK returned no error” is enough without final object verification.

## Why This Matters

Large backups, datasets, media, models, and VM images can take hours over real networks. Restarting from zero wastes time, bandwidth, request cost, energy, and limited transfer windows. Parallel parts can saturate paths and isolate retransmission to failed units.

Unbounded parallelism can saturate client memory, sockets, network, service quotas, encryption/checksum workers, and storage queues. Large parts reduce request overhead but enlarge retry units and buffers. Small parts improve granularity and can hit provider part-count/minimum-size limits.

Completion is the correctness boundary. A client may have uploaded every byte while the final object is absent because completion failed. Conversely, completion may have committed while the client timed out. Initiating another upload or deleting candidate state without resolving that ambiguity can duplicate versions or overwrite another writer.

Incomplete parts have lifecycle and security consequences. They can incur storage charges, hold encrypted/plaintext content, outlive client credentials, and escape ordinary object listings. Organizations need inventory, expiration, abort, and audit controls.

## Prerequisites and Retrieval

Recall serialization and byte identity from [LSDS-008](008-serialization-across-workers.md), failure ambiguity from [LSDS-009](009-cluster-failure-assumptions.md), and resource accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve block/range identity and checksums from [LSDS-011](011-distributed-block-storage.md), metadata transactions and idempotency from [LSDS-012](012-metadata-servers-and-namespace.md), protection acknowledgement from [LSDS-013](013-replication-and-erasure-coding.md), bounded data pipelines from [LSDS-014](014-read-and-write-pipelines.md), and conditional object/version semantics from [LSDS-016](016-object-storage-semantics.md).

You should understand byte ranges, ceiling division, parallel tasks, queues, HTTP requests, validators, checksums, immutable versions, preconditions, credentials, encryption, retries, pagination, and garbage collection.

## Learning Objectives

After completing this module, you should be able to:

- distinguish multipart, resumable, block-list, compose, and single-request uploads;
- define session identity, destination intent, part identity, and durable client state;
- choose part size and concurrency from limits, memory, bandwidth, latency, and retry cost;
- map arbitrary upload completion order into exact object byte order;
- use part validators/checksums without treating every ETag as a content hash;
- resume by reconciling local intent with authoritative server progress;
- specify atomic completion and destination preconditions;
- resolve ambiguous part and completion outcomes safely;
- abort and garbage-collect incomplete sessions without racing in-flight requests;
- verify final version, length, metadata, encryption, and end-to-end digest;
- account requests, payload, retries, buffers, parts, candidates, and cleanup lag;
- protect session capabilities and delegated browser/client uploads; and
- design concurrency, crash, lifecycle, and recovery tests.

## Core Exposition

### Upload protocol families

Multipart upload stores independently numbered parts and completes with an ordered list. A resumable byte-stream session accepts contiguous or provider-defined chunks and reports the committed offset. A block-blob protocol uploads named blocks and commits a block list. Compose creates a destination from existing source objects.

These mechanisms share candidate-state and commit ideas but differ in order, parallelism, overwrite, limits, expiry, checksum, and visibility. Do not transfer assumptions between APIs because they all say “multipart.” HTTP multipart/form-data is also unrelated to a storage multipart session unless the service says otherwise.

Select the exact provider/API/version first. Client libraries can hide protocol details, but operators still need session recovery, checksums, limits, and cleanup behavior.

### Initiation and upload intent

Initiation creates `u` and binds destination bucket/key, content metadata, checksum algorithm/type, encryption/key, storage class, retention, access policy, and perhaps destination preconditions. Record every field needed to reproduce or audit completion.

The upload ID or session URI can authorize writes without repeated credentials. Treat it as a secret: restrict logs, URLs, referrers, browser history, telemetry, and support bundles. Give delegated clients only required destination, size, origin, content, and expiry scope.

Persist a client-side intent before distributing part work. It includes application operation ID, source identity, stable file snapshot, total length/digest, part plan, destination precondition, session, and state version.

### Stable source bytes

Multipart correctness assumes part bytes come from one logical source version. A local file changing during upload can produce a final object assembled from different times. Bind inode/file identity, size, modification/version evidence, or make an immutable snapshot/copy.

For streaming generation, preserve deterministic offsets or durable produced parts. A restart must not regenerate part number 12 with different nondeterministic bytes while retaining part 11 from the earlier run.

Compute an application end-to-end digest over the exact logical byte sequence when consequence warrants. Part checksums localize transfer errors; full digest proves concatenation and source identity under its assumptions.

### Part sizing

For object length `L` and nominal part size `P`, part count is `ceil(L/P)`. Provider rules can require all nonfinal parts above a minimum, impose a maximum part size, and cap part count. Choose `P` so worst-case `L` fits.

Larger parts reduce requests, manifest entries, and per-request overhead. They increase retry bytes, completion latency of the slowest unit, buffer needs, and work lost on credential expiry. Smaller parts improve retry and scheduling granularity but add request and checksum cost.

Variable part sizes can adapt to network or source boundaries. Preserve exact ordered offsets and provider constraints. Never reconstruct byte order by assuming every earlier part has the nominal size.

### Part identity and numbering

A part is addressed by session plus number, block ID, or byte offset. Part number is logical order for some protocols even when upload completion order differs. Sort numerically, not as strings where `10` can precede `2`.

Some services replace an earlier uploaded part when the same session and part number are reused. This supports retry but makes a changed-body retry dangerous. Record length, checksum, returned ETag/validator, and request ID for each accepted part.

Block IDs can be opaque and require consistent encoding/length within a blob. Resumable offsets usually require contiguous progress. Implement the exact model rather than forcing every provider into part numbers.

### Parallel scheduling

Use a bounded worker pool plus a byte semaphore. Eight tasks can mean 64 MiB or 8 GiB depending on part size. Limit sockets, queued file reads, checksum/encryption buffers, and outstanding service requests separately where necessary.

Schedule independent parts out of order to keep workers busy. Prioritize retry carefully so one failing part does not starve progress or loop hot. Exponential backoff with jitter and service retry hints reduce synchronized storms.

Measure source disk, checksum/encryption CPU, upload bandwidth, request latency, throttling, and remote service limits. More workers stop helping at the bottleneck and can deepen tails.

### Part integrity

Calculate the provider-supported checksum over the exact transmitted representation and verify the returned acknowledgement. Persist checksum algorithm/value with part identity. TLS protects transport but does not replace stored-data or end-to-end integrity evidence.

Treat part ETags as opaque completion validators unless the provider explicitly documents content-hash behavior for that upload mode. Multipart encryption and composite validators often differ from a plain content digest.

A successful part request means session candidate state exists under the documented durability contract. It does not mean the final object exists or that other parts are compatible.

### Durable client manifests

The local manifest is a recoverable state machine, not a transient array in worker memory. Store intent version, session, source fingerprint, part plan, each returned validator/checksum/length, completion attempts, destination version, and abort state.

Update it atomically or through a journal. A process crash between remote acceptance and local recording creates ambiguity; server list/status reconciles. Local success without remote confirmation does not authorize completion.

Protect and expire manifests because they contain session capabilities, sensitive keys, checksums, paths, and metadata. Encrypt at rest and minimize logs.

### Resume and reconciliation

After restart, validate the source is unchanged and credentials/session remain valid. Query authoritative server progress: uploaded parts with numbers/validators/checksums, or the committed byte offset. Compare against the local plan.

Accept a server part only if session, position, length, and integrity match expected intent. Reupload missing/mismatched parts with exact intended bytes. Treat unexpected parts as evidence of a wrong session, concurrent actor, or stale local record.

Paginated part listings require complete traversal and stable semantics. A list can race in-flight uploads; pause/coordinate workers or reconcile again before completion.

### Completion manifest

Completion names the session and exact ordered selected parts. For numbered multipart, order is commonly ascending part number or supplied manifest order per contract. The service verifies validators and constraints, constructs the object, and returns final version/validator/checksum metadata.

Validate no gap, duplicate, overlap, unintended part, wrong length, or stale validator. Some checksum modes require consecutive numbering. Compute expected total length from selected parts before sending.

Completion should carry create-if-absent or match-current precondition when concurrent destination writers matter. Checking absence only at initiation leaves a race during a long upload.

### Atomic visibility

Before completion, parts are candidate state accessed through the session API, not a partial object at the destination key under normal multipart semantics. Successful completion publishes one whole object representation. Readers see the old or new version according to object-store consistency, never the concatenation-in-progress.

Atomic object publication does not make related metadata/database rows or other objects atomic. Use the immutable-manifest pattern from LSDS-016 for datasets.

After completion, verify exact destination version, total length, content metadata, encryption, retention, checksum/application digest, and range samples where appropriate.

### Ambiguous part outcomes

A part timeout can mean not received, in progress, accepted, or accepted with lost response. Reuploading identical bytes to the same part identity is often safe under replacement/idempotency semantics, but must be confirmed for the API.

If the retry body differs, do not reuse the identity silently. Query/list the part or intentionally replace it and update the durable manifest. Request IDs and checksums help investigation.

Avoid counting attempts as distinct logical progress. Metrics separate attempted bytes, accepted unique bytes, and retransmitted bytes.

### Ambiguous completion

Completion can commit just before the response is lost. Do not immediately start another session or assume abort can undo it. Query the exact destination key/version and session status, using expected destination precondition, length, metadata, and end-to-end digest.

If the intended object version exists and validates, record success. If the session remains completable and destination precondition still holds, retry the identical completion manifest. If another version is current, preserve evidence and apply conflict policy.

Completion APIs may return success at the HTTP layer while embedding an operation error or may be asynchronous internally; clients must follow exact response parsing and status semantics.

### Abort semantics

Abort marks the session no longer intended for completion and makes candidate parts cleanup-eligible. Coordinate or cancel part workers first. Some services warn that in-flight part uploads can still finish around abort, requiring another reconciliation or abort.

Abort success does not delete a previously committed destination version. Session state and object state are distinct. Retain enough tombstone/operation evidence to prevent a stale worker from recreating progress.

Client crash can prevent explicit abort. Configure provider lifecycle expiration for incomplete sessions and monitor it, while retaining enough time for legitimate long uploads and incident recovery.

### Garbage collection and cost

Incomplete parts may be billed until completion, abort, or lifecycle cleanup. Ordinary object LIST may not show them. Inventory multipart sessions or uncommitted blocks through the dedicated API.

Track session age, owner/application, intended bytes, stored candidate bytes, last activity, expiry, retry window, and hold/incident state. Avoid deleting active uploads based only on age; use leases/heartbeats or durable workflow ownership.

Completion can leave unselected/replaced parts subject to provider cleanup rules. Verify billing and deletion rather than assuming final object creation immediately frees all candidate state.

### Conditional destination control

Long uploads widen the race between initiation and commit. Bind the expected destination state to completion when supported: absent for immutable unique creation or exact validator/generation for replacement.

If the native completion lacks needed preconditions, upload to a unique immutable staging key, validate, then conditionally publish a manifest/pointer. Copying into a shared key is another write needing source and destination conditions.

Do not use upload ID secrecy as concurrency control. Authorized workflows can still conflict.

### Encryption and compression

Client-side encryption must define part boundaries, nonce/key derivation, authentication tags, final format, resume determinism, and range-read behavior. Never reuse a nonce when retrying changed plaintext.

Server-side encryption parameters and key authorization must be bound at initiation/completion. A resume may fail after key policy changes. Preserve key/version metadata for recovery.

Compression streams can make independent parts impossible unless the format supports splittable frames. Compress deterministically into stable part bytes before retry, or store independent frames plus a manifest.

### Observability and testing

Metrics include initiated/active/completed/aborted/expired sessions, age and bytes, part attempts/success/retry, accepted and retransmitted bytes, worker/byte concurrency, throughput, throttling, checksum failures, completion latency/error/ambiguity, cleanup lag, and final verification.

Trace operation/session, destination, source version, part number/offset, length, checksum, request ID, attempt, worker, response, manifest version, completion precondition, and final object version while redacting capability secrets.

Test zero/small/exact/partial part sizes; max count; out-of-order completion; duplicate and changed-body retry; crash before/after remote part acceptance; lost completion response; concurrent destination writer; session expiry; abort with in-flight work; list pagination; checksum mismatch; key revocation; disk/memory pressure; and lifecycle cleanup.

## Definitions and Notation

Let source length be `L>=0`, nominal part size `P>0`, and count `n=ceil(L/P)` for `L>0`, else zero. Part `i` has logical half-open interval `[o_i,o_i+l_i)`. The ordered parts must cover `[0,L)` exactly without gap or overlap.

Upload session `u` binds destination `d`, intent `q`, policy `C`, and authoritative accepted part map `A_u`. A client record `R_u` is evidence to reconcile, not authority over server state.

Completion manifest `M_u=[(p_i,v_i,l_i,h_i)]` identifies part position/number, returned validator, length, and checksum. Commit predicate verifies every selected authoritative part matches `M_u`, provider constraints hold, destination precondition holds, and concatenated length/digest match intent.

With concurrency `c` and equal part buffers `P`, modeled payload buffer bound is `cP`; actual resident memory includes source, checksum/encryption, protocol, SDK, socket, retry, and queue copies. Ideal wave count is `ceil(n/c)` but completion time depends on part latency distribution and bottlenecks.

Let attempted bytes be `B_a`, unique accepted selected bytes `B_u=L`, and retransmitted bytes `B_r=B_a-B_u` in the simple successful model. Protocol overhead, abandoned/unselected parts, and server-side copying require additional terms.

## Mechanisms, Invariants, or Proof Structure

To design or audit multipart upload:

1. Select exact API and record destination, source version, metadata, policy, and precondition.
2. Initiate one protected session and persist a durable application upload intent.
3. Choose legal part size/concurrency from object bounds, memory, bandwidth, and retries.
4. Bind every part number/offset to exact stable bytes, length, checksum, and validator.
5. Reconcile durable local records with authoritative server status after ambiguity/restart.
6. Build and validate one ordered completion manifest plus total length/full digest.
7. Commit under destination precondition and verify returned exact object version.
8. Resolve lost completion responses before new sessions, overwrites, or abort assumptions.
9. Quiesce in-flight workers before abort and monitor lifecycle garbage collection.
10. Test concurrency, crash points, changed bytes, expiry, cleanup, and key/policy changes.

The fixture models numbered parts, replacement of one part, ordered commit, and resource sizing for the compact example. It is not a provider protocol or cryptographic integrity implementation.

<!-- bijux-verify: {"id":"multipart-commit-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"object_bytes=26843545600 part_bytes=134217728 part_count=200 concurrency=8 waves=25\nmax_payload_buffer=1073741824\naccepted_parts=((1, 3), (2, 2), (3, 3)) committed=b'AAAB2CCC' committed_length=8\nfull_sha256_prefix=8c7632a93f639477\nunselected_part_present=True\n","stderr":""}} -->
```python
import hashlib

MIB = 1024 * 1024
GIB = 1024 * MIB
object_bytes = 25 * GIB
part_bytes = 128 * MIB
concurrency = 8
part_count = (object_bytes + part_bytes - 1) // part_bytes
waves = (part_count + concurrency - 1) // concurrency

print(
    f"object_bytes={object_bytes} part_bytes={part_bytes} "
    f"part_count={part_count} concurrency={concurrency} waves={waves}"
)
print(f"max_payload_buffer={concurrency * part_bytes}")

accepted = {}
accepted[1] = b"AAA"
accepted[2] = b"BBB"
accepted[4] = b"unused"
accepted[2] = b"B2"  # same part identity intentionally replaces prior bytes
accepted[3] = b"CCC"

manifest = (1, 2, 3)
committed = b"".join(accepted[number] for number in manifest)
selected = tuple((number, len(accepted[number])) for number in manifest)
print(
    f"accepted_parts={selected} committed={committed!r} "
    f"committed_length={len(committed)}"
)
print(f"full_sha256_prefix={hashlib.sha256(committed).hexdigest()[:16]}")
print(f"unselected_part_present={4 in accepted}")
```

The final object uses only manifest parts 1, 2, and 3; accepted part 4 remains candidate state in this model. Part 2's final two bytes demonstrate replacement, so changed-body reuse must be intentional. The SHA-256 prefix is display evidence only; production retains the full digest and algorithm.

Proof obligations establish source stability, exact coverage/order, part integrity, destination precondition, one commit decision, and final validation. Throughput, durability, security, lifecycle cleanup, and governance require separate evidence.

## Alternatives and Trade-Offs

Single-request upload has the simplest state and restarts fully after interruption. Resumable sequential upload keeps one ordered offset and limited parallelism. Numbered multipart enables out-of-order parallelism and a larger manifest.

Fixed-size parts simplify mapping and resource estimates. Adaptive/variable parts respond to network or source boundaries and complicate resume and offset reasoning. Larger parts save requests; smaller parts save retry bytes.

Client-side parallelism uses source/client capacity directly. Server-side compose can reuse existing objects and adds component limits, source preconditions, and cleanup. Managed transfer tools reduce implementation burden and can hide operational state.

Full-object checksum gives direct logical integrity and may require a complete source pass. Composite checksums parallelize efficiently and depend on part order/algorithm details. Use both where consequence and provider support justify them.

Upload directly to the final shared key is simple and needs a commit-time precondition. Unique staging keys avoid writer collision and require later manifest/pointer or copy publication plus cleanup.

Persisting every part acknowledgement maximizes crash recovery and local I/O. Batching local manifest updates reduces overhead and increases reconciliation after crash. A journal balances durability and throughput.

Aggressive abort/lifecycle expiry controls cost and can destroy recoverable long-running work. Long expiry aids resume and retains sensitive candidates. Use workflow ownership and policy rather than age alone.

High concurrency shortens ideal waves and raises memory, sockets, throttling, and tail contention. Dynamic concurrency adapts to feedback and needs stable bounds and fairness.

## Failure Modes and Misconceptions

- **“Multipart/form-data is object multipart upload.”** They are different protocols unless explicitly connected.
- **“The upload ID is harmless metadata.”** It can be a write capability and must be protected.
- **“A stable filename means stable source bytes.”** Bind an immutable snapshot or source version.
- **“Successful workers mean the object exists.”** Only successful completion publishes the final object.
- **“Parts concatenate in upload completion order.”** Logical part numbering/manifest defines byte order.
- **“Part numbers sort like strings.”** Numeric 10 must not precede numeric 2.
- **“Retrying a part is always harmless.”** Reusing identity with changed bytes can replace accepted state.
- **“An ETag is the part's portable hash.”** Treat it as an opaque provider validator.
- **“Part checksums prove full-object order.”** Verify concatenated length and end-to-end digest.
- **“Eight workers means bounded memory.”** Bound bytes and hidden buffers too.
- **“Local progress is authoritative.”** Reconcile with server session state after crash or timeout.
- **“Checking destination at initiation prevents overwrite.”** The race remains until completion.
- **“A completion timeout means no object.”** Commit may have succeeded with a lost response.
- **“Starting another session resolves ambiguity.”** It can create duplicates, versions, and conflict.
- **“Abort rolls back a committed object.”** Session candidates and final object versions are distinct.
- **“Abort instantly stops in-flight part requests.”** Coordinate workers and verify provider behavior.
- **“Ordinary object LIST finds incomplete uploads.”** Use dedicated multipart/session inventory.
- **“Completion immediately frees every candidate byte.”** Verify cleanup and billing behavior.
- **“Encryption is transparent to resume.”** Nonces, tags, keys, and deterministic part bytes matter.
- **“SDK success replaces independent verification.”** Validate final identity, length, metadata, and digest.

## Worked Examples

### Example 1

**Situation:** A 25-GiB object uses 128-MiB parts. **Reasoning:** It divides exactly into 200 parts. Eight workers make 25 ideal waves and can hold 1 GiB payload before SDK/socket overhead.

### Example 2

**Situation:** Parts finish in order 3, 1, 2. **Reasoning:** Persist each under its part number and validator; complete with logical order 1, 2, 3. Completion time does not define object order.

### Example 3

**Situation:** Part 7 times out after the server may accept it. **Reasoning:** List/query session state or retry identical bytes under part 7 as the API permits. Validate the returned/current checksum before marking local progress.

### Example 4

**Situation:** The source file grows during upload. **Reasoning:** Stop unless an append-aware protocol was designed. A stable initial size alone does not prove earlier/later parts belong to one source version; upload from a snapshot.

### Example 5

**Situation:** A completion response is lost. **Reasoning:** Query exact destination version, length, metadata, and digest plus session status. Record success if intended object committed; otherwise retry the identical manifest only when destination precondition remains valid.

### Example 6

**Situation:** Another client writes the destination during a two-hour upload. **Reasoning:** A commit-time expected-generation/absence condition prevents silent overwrite. Otherwise publish a unique staged object and conditionally update a pointer.

### Example 7

**Situation:** A client aborts while workers still upload parts. **Reasoning:** Stop scheduling, cancel/drain workers, abort, then query/abort again if provider semantics permit late successes. Lifecycle cleanup is a backstop.

### Example 8

**Situation:** Every part checksum validates but final digest differs. **Reasoning:** Suspect wrong order, wrong selected part/version, source mutation, metadata/encoding transformation, or digest scope. Do not publish downstream until the logical digest matches.

### Example 9

**Situation:** Millions of old sessions incur unexplained storage cost. **Reasoning:** Inventory incomplete uploads/uncommitted blocks, join to workflow ownership, expire abandoned sessions with canaries, and monitor candidate bytes and cleanup lag.

### Example 10

**Situation:** A browser uploads regulated records through a delegated session URL. **Reasoning:** Scope destination/origin/size/content/expiry, protect the URI, require checksum and final server-side validation, conditionally publish, audit principal/request/version, clean candidates, and obtain records/privacy/security/accessibility review.

## Cross-Program Connections

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies idempotency, resumable workflows, status resources, preconditions, pagination, errors, deadlines, and delegated clients. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies transactions, ambiguous outcomes, retries, leases, fencing, and garbage collection.

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies throughput, latency, congestion, parallel streams, loss, retry, and bandwidth-delay reasoning. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies stable file snapshots, buffer/cache memory, file mutation, checksums, and local I/O.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies capability URLs, scoped delegation, encryption/nonces, checksums, keys, audit, and sensitive metadata. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies quotas, lifecycle, cost, observability, cleanup, and operational automation.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes large-object upload, manifests, immutable publication, checksums, and retries. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns authoritative identity, provenance, lifecycle, retention, and recovery evidence.

Amazon S3 documents numbered multipart initiation, part upload, listing, completion, abort, checksum modes, and limits. Google Cloud Storage documents resumable sessions, XML multipart, and compose. Azure Blob documents named uncommitted blocks and atomic block-list commit. Their common concepts do not erase their distinct contracts.

## References

- Amazon Web Services, [*Uploading and Copying Objects Using Multipart Upload*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html), checked 2026-09-03. Official current initiation, upload ID, part number, validator, completion, abort, cost, and checksum overview.
- Amazon Web Services, [*CompleteMultipartUpload API*](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CompleteMultipartUpload.html), checked 2026-09-03. Official current completion manifest, conditional headers, checksum, errors, and response behavior.
- Amazon Web Services, [*Checking Object Integrity for Data Uploads*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity-upload.html), checked 2026-09-03. Official current full-object and composite multipart checksum semantics.
- Amazon Web Services, [*Aborting a Multipart Upload*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/abort-mpu.html), checked 2026-09-03. Official current abort, in-flight part, listing, permissions, and cleanup guidance.
- Amazon Web Services, [*Amazon S3 Multipart Upload Limits*](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html), checked 2026-09-03. Official current object, part, count, size, and listing limits.
- Google Cloud, [*Resumable Uploads*](https://cloud.google.com/storage/docs/resumable-uploads), checked 2026-09-03. Official current session URI, resume, completion visibility, expiry, metadata, and client buffer guidance.
- Google Cloud, [*XML API Multipart Uploads*](https://cloud.google.com/storage/docs/multipart-uploads), checked 2026-09-03. Official current initiate, upload part, complete, abort, and list protocol.
- Google Cloud, [*Compose Objects*](https://cloud.google.com/storage/docs/composing-objects), checked 2026-09-03. Official current source generation/precondition, composition, limits, metadata, and integrity behavior.
- Microsoft, [*Put Block*](https://learn.microsoft.com/en-us/rest/api/storageservices/put-block), checked 2026-09-03. Official current uncommitted block ID, checksum, encryption, authorization, and size semantics.
- Microsoft, [*Put Block List*](https://learn.microsoft.com/en-us/rest/api/storageservices/put-block-list), checked 2026-09-03. Official current committed/uncommitted block selection, ordering, atomic blob commit, conditions, and garbage collection.

## Exercises

### Exercise 1

Choose part size and calculate count, ideal waves, and payload buffer for a 4.5-TiB object, maximum 10,000 parts, concurrency 12, and a 768-MiB payload-buffer budget. State other constraints.

### Exercise 2

Design a durable local upload record and reconciliation algorithm for restart after some part acknowledgements were lost.

### Exercise 3

Design safe completion when the destination must remain unchanged from generation 27 and another client may write during upload.

### Exercise 4

Handle an ambiguous completion followed by an expired or unknown session. Give evidence that distinguishes success, conflict, and loss.

### Exercise 5

Specify security, cleanup, and named review for delegated multipart upload of sensitive research data from unreliable browsers.

## Answers to the Exercises

### Answer 1

The count limit requires part size at least `ceil(4.5 TiB/10000)`, about 471.86 MiB, subject to provider min/max. A practical 512-MiB part yields `4.5*1024*1024/512=9,216` exact parts and 768 ideal waves at concurrency 12. Twelve full buffers would be 6 GiB, violating the 768-MiB budget; at 512 MiB only one full payload buffer fits, or the implementation needs streaming/sub-buffers that prove lower residency. With 64-MiB memory per worker, 12 workers fit 768 MiB but part bytes must stream without full buffering. Also evaluate request limits, source I/O, checksums/encryption, retry cost, sockets, bandwidth, expiry, last-part rule, SDK hidden buffers, and completion manifest size.

### Answer 2

Persist operation ID, immutable source identity/length/full digest, destination and commit precondition, session, metadata/encryption/retention, part plan, and per-part expected offset/length/digest plus returned validator/checksum/request ID. Journal state changes atomically. On restart, verify the source fingerprint, query every server part page or committed offset, and compare. Accept matching remote progress even if its local acknowledgement was lost; reupload missing parts identically; quarantine unexpected lengths/digests/parts. Quiesce workers and reconcile again before creating the ordered completion manifest. Protect the record because it contains session capability and sensitive metadata.

### Answer 3

Record expected generation 27 in the upload intent and apply the provider's match-generation/ETag condition at completion, not only initiation. Upload parts to one session and validate their ordered manifest and full digest. If completion sees generation 27, it atomically publishes the new version and returns its identity. If another client changed the key, completion fails with a conflict/precondition result; preserve or abort the session according to policy and never overwrite blindly. If native completion cannot express the condition, complete at a unique staging key and conditionally update a small manifest/pointer from generation 27.

### Answer 4

Query destination versions/current state for the intended operation metadata, expected length, full digest, encryption/retention, and destination precondition result. If a matching new version exists after generation 27, record success even though the session is gone. If a different version exists, report conflict and retain audit/candidate evidence. If no matching destination exists and the session expired, the upload did not yield a recoverable visible object through that session; create a new session only after confirming the source and current destination precondition and record a new attempt identity. Provider request logs can strengthen evidence; absence from ordinary LIST alone is insufficient.

### Answer 5

Create a narrowly scoped server-side intent for exact bucket/key prefix, size/content type, origin, checksum, encryption key, retention, expiry, and single application operation. Treat session URLs as bearer capabilities: keep them out of logs/referrers/analytics, transmit over protected channels, revoke/expire promptly, and rate-limit parts/bytes. Browsers upload stable numbered parts with checksums; the trusted service reconciles, verifies full digest and schema, completes under a destination precondition, and publishes only after policy checks. Monitor/abort abandoned sessions and lifecycle-clean candidates after a justified recovery window. Named review includes investigators/data stewards, participant/community representatives, research ethics/IRB, privacy/legal/records, security/key management, browser/accessibility specialists, platform/storage operators, incident recovery, and independent assurance. Internal part verification is not ethical or legal approval.
