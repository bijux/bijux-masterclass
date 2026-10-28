---
module_id: DE-023
program: Data Engineering
level: 1
module_number: 23
title: File Arrival and Manifest Processing
status: complete
last_verified: 2026-09-02
---

# File Arrival and Manifest Processing

## One-Page Review

### Governing question

How can a file-based ingestion boundary determine that an exact dataset generation—not merely some visible objects—has arrived intact, is authorized, is complete, can be processed once by effect, and can be replayed or repaired without ambiguity?

### Essential definitions

- A **data object identity** is path/key plus immutable version, generation or content digest; a pathname alone may be overwritten.
- A **manifest** is a versioned control record enumerating the objects and metadata that constitute one logical dataset generation.
- A **publication protocol** makes data objects durable first and exposes their manifest or snapshot pointer last.
- A **completion marker** is a producer-owned signal meaningful only under a documented protocol; an empty `_SUCCESS`-like object is not self-explanatory.
- A **notification** announces that an object event may have occurred; it is a discovery hint, not proof that all related files arrived.
- **Structural validation** checks manifest schema, required fields, uniqueness, bounds and references.
- **Integrity validation** checks object identity, size and cryptographic/content checksum under declared algorithms.
- A **consumer receipt** durably records that one manifest generation produced one committed downstream effect.
- A **quarantine** isolates invalid or ambiguous objects/manifests with evidence and controlled reprocessing.
- A **repair generation** supersedes an invalid or incomplete generation without mutating its forensic record.

### Central model, mechanism, or theorem

Let manifest $M$ declare a finite set of immutable object identities $F_M$. Let $V_M$ be the objects actually retrieved at those exact versions whose byte lengths and digests match the manifest. Object completeness requires

$$
V_M=F_M,
$$

not merely $|V_M|=|F_M|$. Equal counts can hide one missing and one extra object.

Let `effect(M,S)` apply manifest $M$ to downstream state $S$. Replay safety requires manifest-level idempotency:

$$
effect(M,effect(M,S))=effect(M,S).
$$

This does not require notifications to arrive once. It requires stable manifest identity, immutable inputs and a receipt/commit protocol that makes duplicate delivery produce one governed effect.

### Critical invariants

- Producers write unique immutable data objects before publishing the manifest that references them.
- Manifest identity, schema/contract version, producer, source interval, partition scope and publication time are explicit.
- Every object reference includes immutable version/generation where supported, byte size, checksum algorithm/value and expected format/compression.
- Manifest file identities are unique; referenced objects exist exactly at declared versions and pass size/digest validation.
- Manifest totals reconcile with file totals; exact key/file sets matter more than counts alone.
- Notifications may duplicate, arrive late or out of order; processing correctness does not depend on notification uniqueness/order.
- Consumers atomically relate manifest receipt, durable outputs and input progress; retries replay rather than skip.
- Unlisted staging objects, partial uploads and abandoned multipart parts are not admitted.
- Corrections publish a new version/supersession record rather than overwriting accepted evidence.
- Paths, archives, schemas, decompression, encryption and sensitive-data handling are validated before unsafe parsing or publication.

### Common failures

Treating the first file as the batch trigger; declaring completion after a quiet period; trusting a listing count; relying on lexicographic filename order; using path without object version; overwriting data under the same key; publishing manifest before all data; interpreting a storage event as exactly once or ordered; assuming `ETag` is always a whole-object MD5; validating checksum but not manifest authorization; parsing before size/decompression bounds; acknowledging the queue before durable receipt/output; deleting inputs immediately; editing a bad manifest in place; and letting a partial generation advance the extraction watermark.

### Compact example

A manifest declares two four-byte files with independent SHA-256 digests and total eight bytes. The consumer resolves exact object versions, verifies the two identities, sizes and digests, then commits one receipt. A missing file, an unlisted in-scope file or a one-byte mutation fails validation. Delivering the same manifest notification twice returns the prior receipt and does not duplicate output.

### Connections

[DE-003](003-csv-json-and-line-oriented-formats.md), [DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) and [DE-006](006-parquet-and-columnar-files.md) define file interpretation; [DE-010](010-designing-a-reproducible-data-boundary.md) defines immutable boundaries; [DE-022](022-watermarks-and-high-water-marks.md) defines safe progress. Planned DE-029 covers quarantine and DE-030 replayable raw ingestion; see the [Data Engineering roadmap](../ROADMAP.md).

## Governing Question

What evidence allows a consumer to say “this exact file dataset is complete and committed” when object events can duplicate, files can arrive in any order, names can be reused and a producer can fail halfway through publication?

File ingestion often begins with a folder and a schedule. That is not a protocol. A listing is an observation at a time; it does not reveal how many files the producer intended, whether uploads are final, whether two files came from the same source cut or whether a correction will replace one later. A notification says an object event was published, not that a multi-object dataset is complete.

A manifest turns implicit convention into an explicit commit object. It names a dataset generation and enumerates exact immutable inputs plus their integrity and semantic metadata. The producer writes data first, validates its own output, and publishes the manifest last. Consumers treat only a valid manifest as work, verify every referenced object independently, and record one durable receipt before advancing progress.

This protocol does not make object storage transactional across many objects. It creates a small atomic publication point—an immutable manifest or metadata pointer—from which a complete set can be resolved. Apache Iceberg's [specification](https://iceberg.apache.org/spec/) illustrates the pattern at table-format scale: immutable manifests list data/delete files, manifest lists group manifests for a snapshot, and table metadata changes through an atomic pointer swap.

The governing question is therefore about identity, closure and evidence, not how quickly a directory scanner notices a filename.

## Why This Matters

File boundaries connect systems with different transaction models. A producer may write many files over minutes, while a consumer scheduler sees individual objects immediately. Without a commit protocol, the consumer can publish partial data, double-process retries or combine generations.

Names are mutable in many stores. `orders/2026-09-02/part-000.parquet` can refer to different bytes after overwrite. A checkpoint containing only that path cannot reproduce what was read. Version, generation or digest must bind the reference.

Notifications deliberately favor delivery over uniqueness. Amazon S3 documents that event notifications are at least once and not guaranteed in event order; Google Cloud Storage documents at-least-once Pub/Sub notifications with possible duplicates and reordering. A robust consumer uses notifications to wake discovery, then relies on storage metadata, manifest identity and receipts.

Integrity also has layers. Successful upload/download, byte length and checksum are distinct. A cryptographic digest detects accidental or malicious byte differences within its assumptions, but does not prove the file belongs to the intended batch, follows the schema, contains the correct rows or was authorized by the producer.

Operational failures are normal: producer crashes, delayed parts, duplicate triggers, consumer crashes after output but before acknowledgement, schema changes, expired credentials and corrections. Explicit state transitions and immutable evidence make these diagnosable and replayable.

Finally, file ingestion can be a security boundary. Untrusted filenames, archives, compression, schemas and metadata can cause path traversal, resource exhaustion, code execution or disclosure. Validate identity and bounds before parsing; quarantine is safer than best-effort admission.

## Prerequisites and Retrieval

Retrieve producer/consumer owners; dataset and contract version; source interval/watermark; expected schedule and lateness; object store/filesystem semantics; bucket/container/prefix; versioning/generation behavior; read/list/write/delete consistency; overwrite and conditional-write support; multipart/compose semantics; notification guarantees and retention; object metadata; encryption/key references; checksum algorithms; producer upload/commit workflow; naming and partition conventions; manifest schema/canonicalization/signature; expected files, sizes, row counts and control totals; file format/compression/schema identifiers; column/partition statistics; delete/tombstone files; consumer discovery/checkpoint/receipt store; concurrency/lease model; downstream transaction/publication behavior; retry and acknowledgement ordering; quarantine; raw retention; correction/supersession policy; privacy/deletion obligations; maximum file/archive/decompressed sizes; parser limits; credentials/network boundaries; monitoring; recovery objectives; and historical incident evidence.

Distinguish path from immutable object identity; object creation from dataset completion; write success from durable/visible publication; storage listing consistency from producer semantic completeness; notification delivery from source of truth; event ID from manifest ID; manifest file from manifest contents; checksum from authentication and semantic validation; compressed size from expanded size; row count from key-set/content correctness; in-scope extra object from unrelated/staging object; producer retry from correction; duplicate delivery from duplicate effect; quarantine from silent skip; receipt from queue acknowledgement; batch commit from file deletion; raw retention from accepted publication; and version supersession from in-place overwrite.

Before implementation, define a manifest schema with these groups:

| Group | Required content |
|---|---|
| Identity | Dataset, producer, manifest ID/version, generation, predecessor/supersedes |
| Scope | Source interval/watermark, partitions, filters, timezone/calendar, contract/schema |
| Files | Path/key, object version/generation, role, format, compression, bytes, checksum algorithm/value, rows/statistics |
| Totals | Expected file count, bytes, rows, control sums and allowed tolerances |
| Security | Signature/key identity if used, encryption/key reference, classification and access scope |
| Publication | Created/published time, producer run, status and expiry/retention |
| Consumer evidence | Validation result, receipt ID, output generation, committed time and software version |

Use canonical serialization for signing or manifest digests. Reject duplicate JSON keys, ambiguous number/time encodings, path normalization surprises, unsupported algorithms and unknown required fields according to the compatibility policy.

## Learning Objectives

After completing this module, you should be able to:

1. explain why notification, listing and quiet time do not prove dataset completion;
2. design a versioned manifest and publication-last protocol;
3. bind filenames to immutable object versions, lengths and checksums;
4. validate exact file sets, totals, formats, schemas and source intervals;
5. process duplicate/out-of-order notifications with one manifest effect;
6. coordinate consumer receipts, downstream publication and watermark advancement;
7. quarantine invalid inputs while preserving evidence and replay paths;
8. publish corrections through immutable superseding generations;
9. defend file ingestion against path, archive, compression and metadata attacks; and
10. test producer/consumer failures and reconcile accepted generations.

## Core Exposition

### Treat arrival as a protocol

A dataset is not complete because one or all currently visible files arrived. Completion requires producer-declared scope and a publication event that cannot precede durable data.

Define producer and consumer state machines. The producer moves through `building`, `validating`, `publishing-data`, `publishing-manifest`, `committed` or `aborted`. The consumer moves through `discovered`, `validating`, `ready`, `claimed`, `processing`, `committed`, `quarantined` or `superseded`.

Record every transition with generation identity. Do not infer state solely from pathname suffix or elapsed time.

### Write data before the manifest

Use unique generation-scoped data keys. Upload/close each object, capture immutable version/generation, length and checksum, and validate producer totals. Only then write the immutable manifest.

If a mutable “current” pointer is needed, update it conditionally after the new manifest is durable. Consumers that already resolved the old pointer continue using its immutable generation.

Publishing the manifest first creates dangling references. Retrying by overwriting referenced paths can make a previously valid manifest resolve to new bytes.

### Use immutable object identity

Represent identity as store/bucket/key plus object version or generation where supported. Include digest as integrity evidence and potentially content identity; record checksum algorithm explicitly.

If the store does not version objects, use never-reused generation-scoped keys. Enforce create-if-absent/conditional writes so retries cannot silently replace accepted data.

Path normalization must be defined. Case sensitivity, Unicode normalization, repeated separators, dot segments and URL decoding can create duplicate or escaping identities.

### Design stable manifest identity

Give each manifest a globally or dataset-scope unique ID, generation, producer run and schema version. Include predecessor/supersession relation if generations form a chain.

The manifest's own immutable object identity and canonical digest distinguish duplicate notification of the same generation from conflicting bytes under one ID.

If the same manifest ID appears with a different digest, fail closed and escalate; do not choose the latest arrival.

### Enumerate exact expected objects

Each entry names path, immutable version, logical role/partition, format, compression, byte size, checksum type/value, schema and optional row/statistics controls.

Require unique entry identities. A duplicate path/version can double count totals or hide producer defects. Sort order in serialization may be canonical, but data semantics should not depend on listing order unless explicitly declared.

State whether unlisted objects under the generation prefix are forbidden, ignored staging debris or separately governed. Never accept them implicitly.

### Record semantic scope

Include source low/high watermark or snapshot ID, interval boundaries, timezone/calendar, filters, tenant, partition specification, schema/contract version and whether generation is full, incremental, correction or delete.

File bytes can be internally valid yet overlap a prior batch or leave a gap. Manifest intervals let the consumer reconcile continuity before advancing DE-022 watermarks.

If multiple producers share a dataset, define one serialization/coordination owner or explicit partition independence. Two “complete” manifests over overlapping scope can conflict.

### Record useful totals

Include file count and total bytes computed from entries. Row counts, min/max keys, null counts, column bounds and control sums can strengthen validation when producer calculates them independently.

Totals must reconcile exactly or under a predeclared tolerance. Never use total count alone: expected `{a,b}` and observed `{a,c}` both have two members.

Statistics can leak sensitive information. Classify and authorize manifest metadata like data.

### Validate manifest structure before access

Parse with bounded input size/depth and a strict schema. Reject duplicate fields, invalid encodings, unsupported versions, unknown required semantics, duplicate object identities, negative sizes/counts, overflow, impossible timestamps and inconsistent totals.

Validate paths against allowed bucket/prefix and disallow local path traversal, URI scheme changes and credentials embedded in URIs. Resolve references without string concatenation into a filesystem shell command.

Only after structural and authorization checks should the consumer fetch data objects.

### Authenticate producer intent

Storage permissions can establish who wrote an object only within the cloud/audit model. For higher assurance, sign a canonical manifest with a managed producer identity/key and verify trust, algorithm, key validity and revocation policy.

A checksum is not a signature. Anyone able to replace both file and manifest checksum can create a matching pair unless write controls or authentication prevent it.

Do not embed private keys or plaintext data-encryption keys in manifests. Reference governed key identities/versions as required for authorized decryption.

### Verify existence and exact version

Resolve every entry at its named version/generation and read authoritative metadata. “Latest object at path” is not equivalent if the key was overwritten.

Handle transient authorization/network errors as retryable observation failures, not missing files. A genuine not-found after publication is an invalid manifest or retention incident.

Cloud Storage's [consistency documentation](https://docs.cloud.google.com/storage/docs/consistency) documents strongly consistent object reads/listings and atomic individual-object uploads while noting multi-operation batches are not atomic. Strong listing makes observation clearer; it does not say which set the producer intended.

### Verify byte length

Compare declared and stored/downloaded byte length using integer bounds. Detect truncation, unexpected expansion and representation confusion.

Zero-byte data can be valid only if format/role permits it. A completion marker may intentionally be empty; a Parquet data file generally needs structural bytes.

Length equality does not establish content equality; pair it with digest and format validation.

### Verify checksums correctly

Use the exact declared algorithm and checksum type. Calculate over the agreed byte representation—stored compressed/encrypted object or decoded content—and say which.

Amazon S3's [object-integrity documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html) documents supported checksums; multipart/object APIs can distinguish composite from full-object values. Do not assume every `ETag` is a whole-object MD5.

Cryptographic hashes have collision assumptions and do not prove semantic correctness. For adversarial producer trust, authenticate the manifest and transport/storage identities too.

### Validate format and compression safely

Check magic/version/footer where applicable, schema identity, codec and complete parse. For splittable formats, validate every referenced range/row group as required.

Enforce compressed and expanded size, nesting, record length, column count and resource/time limits. Decompression bombs and malformed files must not exhaust shared workers.

Parse untrusted data in least-privileged isolated workers. Never execute embedded formulas, macros, object deserializers or external references by default.

### Validate schema and semantics

Resolve schema by immutable ID/version. Validate column names/IDs, types, nullability, logical types, encodings and compatibility. Preserve unknown fields under policy rather than silently dropping meaning.

Check partition values against actual row values when producer trust/risk warrants. Validate source interval, key ranges, duplicate keys and control totals.

File-format validity cannot prove the producer extracted the right rows. Reconcile against independent source controls where consequence demands it.

### Discover with notifications, verify with manifests

Use object notifications to trigger manifest lookup. Deduplicate by manifest identity/digest after retrieval, not notification message ID alone; two notification IDs can represent the same storage event.

AWS documents [S3 event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html) as at-least-once and not guaranteed in event order. Google Cloud documents similar [Cloud Storage Pub/Sub notification](https://docs.cloud.google.com/storage/docs/pubsub-notifications) behavior.

Poll/reconcile manifests periodically to recover lost, expired or misconfigured notifications. Event delivery is an optimization, not the sole catalog of committed work.

### Filter events precisely

Subscribe to manifest prefix/suffix or object metadata where supported, and ignore data/staging events. Validate event bucket/key/generation against the fetched manifest object.

Prevent recursive triggers when consumers write receipts or outputs into the same notification scope. Separate prefixes/buckets or filter producer/event type.

Treat delete/overwrite notifications as lifecycle events requiring policy, not as new complete datasets.

### Do not infer completion from quiet time

A “no new files for five minutes” heuristic confuses slow producer, network partition and completion. It can work only as an explicitly weak timeout policy with partial-output semantics and later correction.

Likewise, stable repeated listings prove only that two observations matched. They do not reveal intended count or future delayed files.

A producer-issued manifest/marker supplies closure because the protocol forbids issuing it early. Monitor producer conformance.

### Understand completion markers

An empty marker is useful when its path binds a unique generation and the producer contract says it is written last after validating all data. It should reference or accompany a rich manifest rather than replace it for critical ingestion.

Hadoop's [manifest committer documentation](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/manifest_committer.html) describes job commit metadata and a success marker in a concrete output-commit protocol.

A manually created marker or leftover marker from an older retry is unsafe. Bind it to generation/run identity.

### Claim work without duplicate effects

Multiple consumers may discover the same manifest. Acquire a lease/compare-and-set claim keyed by dataset and manifest ID/digest, or let all perform read validation while only one commits the receipt/output transaction.

Leases need owner, expiry, fencing token and heartbeat. An expired worker must not commit after a new worker takes ownership; compare fencing generation at commit.

Exactly-once notification is unnecessary. Manifest effect idempotency and transactional receipt publication are the target.

### Stage, validate and publish downstream

Write output into a generation-scoped staging/immutable location. Reconcile file/row/key/control totals and only then atomically publish a pointer/table snapshot/transaction.

Do not expose partial per-file results merely because some tasks succeeded. A manifest-level all-or-nothing consumer contract either commits the generation or records a deliberately partial product with different semantics.

Keep the last trusted output through rollback horizon.

### Coordinate receipt and acknowledgement

A consumer receipt includes manifest identity/digest, input object versions/digests, consumer code/configuration, validation results, output generation, counts/controls, commit time and predecessor receipt.

Persist receipt/output before acknowledging the notification or advancing the source interval watermark. A crash afterward may redeliver; lookup returns the committed receipt.

If receipt and output cannot be atomic, make outputs immutable/idempotent and use recovery reconciliation to finish or roll back the partially committed state.

### Handle file-level retries

Retry transient fetches with bounded exponential backoff/jitter and stable object version. Do not refetch “latest” after a failure because it can change bytes.

Parallel downloads can complete out of order. Aggregate status by manifest entry and commit only when every required entry passes.

Persist per-file validation evidence for large manifests so a worker restart can reuse proven immutable objects, subject to evidence/credential validity.

### Quarantine invalid arrivals

Quarantine by manifest/object immutable identity with reason category, safe diagnostics, detection time, producer/contact, retryability and evidence links. Restrict access because rejected data remains sensitive.

Do not advance the dataset watermark past an unresolved required generation. Independent partitions can proceed only if the contract makes them independent.

Reprocessing uses the same immutable input or a new repair generation; never edit evidence in place to force green status.

### Publish corrections and supersession

Corrections get a new manifest ID/generation stating which prior generation or partitions they supersede and why. Preserve old manifests/receipts under retention for reproducibility.

Define whether correction replaces a full snapshot, partitions or keyed records. Consumers apply version precedence idempotently and prevent an older delayed manifest from overwriting newer state.

If bytes were malicious or privacy-invalid, access/delete policy may require removal while retaining non-sensitive audit metadata and tombstones.

### Support delete files and withdrawals

Some datasets publish delete/tombstone files or manifests that remove prior file/data identities. Give them explicit roles and sequence semantics.

Apache Iceberg manifests illustrate tracking data and delete files plus snapshot sequence. A generic ingestion protocol can borrow the separation without claiming Iceberg semantics.

Never infer record deletion solely because a file is absent from an incremental manifest; determine whether manifests are full-state or delta.

### Manage schema evolution

Manifest schema version governs control parsing; data schema version governs row interpretation. Evolve each compatibly and independently.

Unknown optional fields can be preserved/ignored under policy; unknown required semantics must fail. A producer should not reuse a schema ID for different definitions.

Test mixed-schema batches if allowed. Otherwise require one schema per manifest or per entry with explicit normalization.

### Manage object lifecycle

Retain data, manifests, receipts and schemas through replay/audit horizon. Ensure lifecycle rules do not delete data while a valid manifest still references it.

Clean abandoned staging objects and incomplete multipart uploads using age/run state, never broad prefix deletion that might remove committed generations.

Verify restoration from archive includes exact versions and integrity metadata within recovery objectives.

### Protect sensitive metadata

Object names, partitions, min/max values and row counts can reveal customers, dates, diagnoses or business volume. Avoid sensitive plaintext in paths and minimize manifest statistics.

Use least-privileged producer write and consumer read identities. Separate ability to write data from ability to publish/sign manifests when risk warrants dual control.

Audit reads, signature verification, receipt commits, overrides, quarantine access and deletions.

### Monitor the boundary

Monitor expected-versus-arrived manifests, notification delay/duplicates, discovery reconciliation, manifest validation failures, missing/extra/version-mismatched objects, checksum/size/schema failures, time to ready/commit, stuck claims, retries, quarantine age, late/superseding generations, watermark gaps and retention headroom.

Alert differently for producer late, manifest early, object lost, permission denied, consumer stalled and invalid content. Each has a different owner/action.

Measure per dataset/producer/partition and preserve run-level evidence.

### Test the publication protocol

Inject producer crash before any data, during multipart upload, after some files, after all files but before manifest, during manifest write and after manifest before notification.

Inject duplicate/out-of-order/delayed/lost notifications, object overwrite/version mismatch, missing/extra/zero/truncated/corrupt files, duplicate manifest entries, invalid totals, decompression bomb, schema drift, signature failure, consumer claim race and crash around receipt/output/acknowledgement.

For each case, assert visibility, validation state, downstream effect, receipt, watermark, quarantine, alert and replay/repair path.

## Definitions and Notation

Let a manifest be

$$
M=(id,g,d,s,[a,b],F,T,\sigma),
$$

where $id$ is stable manifest identity, $g$ generation, $d$ dataset/producer scope, $s$ schema/contract identity, $[a,b]$ source interval, $F$ the finite ordered/canonical entry collection, $T$ declared totals and $\sigma$ optional authenticated signature.

Each file entry is

$$
f=(uri,version,role,format,codec,bytes,algorithm,digest,rows,stats).
$$

Define immutable object identity $I(f)=(uri,version)$, or a generation-scoped never-reused URI when versions are unavailable. Require uniqueness:

$$
|\{I(f)\mid f\in F\}|=|F|.
$$

Let $F_M=\{I(f)\mid f\in F\}$ and $V_M$ be exact identities retrieved and validated for length/digest. Object completeness requires $V_M=F_M$. If in-scope prefix exclusivity is part of the contract, observed committed set $O_M$ must also equal $F_M$; otherwise unlisted staging objects are classified separately.

Declared byte and row totals reconcile when

$$
T_{bytes}=\sum_{f\in F}bytes(f),\qquad T_{rows}=\sum_{f\in F}rows(f)
$$

for formats/semantics where row additivity applies.

Let canonical manifest bytes be $canon(M)$ and manifest digest $h_M=H(canon(M))$. The pair $(id,h_M)$ identifies a delivery; same $id$ with different $h_M$ is a conflict.

For downstream state $S$, idempotent generation application satisfies

$$
effect(M,effect(M,S))=effect(M,S).
$$

A receipt $R=(id,h_M,input\_versions,consumer\_version,output\_generation,controls,time)$ binds accepted input to one durable result.

## Mechanisms, Invariants, or Proof Structure

**Publication mechanism.** Create generation-scoped immutable data; validate producer outputs; publish immutable manifest last; optionally conditionally swap a current pointer; notify consumers; retain all referenced objects through recovery horizon.

**Exact-set theorem.** $V_M=F_M$ implies no declared identity is missing and no different identity substitutes within the validated set. Equality of cardinalities alone lacks this implication because distinct sets can have the same size.

**Publication-last invariant.** If the producer protocol publishes $M$ only after every $f\in F_M$ is durable and immutable, observing valid $M$ authorizes resolution of the full declared set. This depends on producer conformance and storage/object identity guarantees.

**Notification-independence invariant.** Duplicate, reordered or delayed notifications do not alter final effect because discovery retrieves immutable $M$ and the receipt key is $(id,h_M)$.

**Receipt safety invariant.** Acknowledgement and input-watermark advance occur only after output and receipt are durable. Failure before that point yields retry/replay, not silent skip.

**Checksum boundary.** Matching $H(bytes)$ establishes equality to the declared digest within algorithm/canonical-byte assumptions. It does not establish schema validity, semantic completeness, producer authorization or correctness of declared digest.

**Correction monotonicity.** Newer generation/supersession state can replace older state under declared ordering; delayed older manifests cannot overwrite a committed newer generation.

**Atomic-publication condition.** Multi-file storage need not be atomic if consumers resolve one immutable manifest/snapshot pointer and publish downstream only after all entries validate. The manifest becomes the logical commit object.

<!-- bijux-verify: {"id":"manifest-completeness-receipt","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"manifest_files=2\nmanifest_bytes=8\ncomplete=True\nmissing_detected=True\nextra_detected=True\nchecksum_mismatch_detected=True\nduplicate_manifest_idempotent=True\npublished_after_validation=True\n","stderr":""}} -->
```python
import hashlib

manifest = {
    "id": "orders-2026-09-02",
    "files": (
        ("part-000.csv", 4, "a763c2b572d8bdf96960a1511f6928ec35879ec98363a3e14e3c75ca1cbc8994"),
        ("part-001.csv", 4, "9fba86a2a7936f7c5ca5852c476b3d949fe8022d5e410c9e07477cdb906185a7"),
    ),
}
objects = {
    "part-000.csv": b"a,1\n",
    "part-001.csv": b"b,2\n",
}

def validates(specification, actual):
    expected_names = {entry[0] for entry in specification["files"]}
    if set(actual) != expected_names:
        return False
    for name, size, digest in specification["files"]:
        payload = actual[name]
        if len(payload) != size or hashlib.sha256(payload).hexdigest() != digest:
            return False
    return True

complete = validates(manifest, objects)
missing = {"part-000.csv": objects["part-000.csv"]}
extra = dict(objects, **{"part-002.csv": b"c,3\n"})
changed = dict(objects)
changed["part-001.csv"] = b"b,9\n"

receipts = {}
if complete:
    receipts.setdefault(manifest["id"], "output-generation-7")
first_receipt = receipts[manifest["id"]]
receipts.setdefault(manifest["id"], "output-generation-8")

print(f"manifest_files={len(manifest['files'])}")
print(f"manifest_bytes={sum(entry[1] for entry in manifest['files'])}")
print(f"complete={complete}")
print(f"missing_detected={not validates(manifest, missing)}")
print(f"extra_detected={not validates(manifest, extra)}")
print(f"checksum_mismatch_detected={not validates(manifest, changed)}")
print(f"duplicate_manifest_idempotent={receipts[manifest['id']] == first_receipt}")
print(f"published_after_validation={complete and manifest['id'] in receipts}")
```

The finite execution checks two known byte strings and a simple in-memory receipt. It does not prove storage durability, cryptographic authentication, schema correctness or production transactionality.

## Alternatives and Trade-Offs

**Manifest versus directory listing.** A manifest declares intended identity and totals; listing is convenient discovery. Strong listings still lack producer closure/semantics, so use them to find manifests or reconcile debris.

**Rich manifest versus completion marker.** A marker is small and simple under a strong naming protocol. A rich manifest supports exact integrity, lineage and repair. Critical/multi-file datasets benefit from both combined.

**Immutable generation keys versus mutable stable paths.** Immutable keys preserve reproducibility and simplify cache/retry. Stable paths are convenient but require object versions/preconditions and careful cache identity.

**One manifest versus hierarchical manifests.** One file is simple but large for millions of objects. Manifest lists/shards scale planning while adding another integrity/commit layer.

**Push notification versus polling.** Push lowers discovery latency but duplicates/reorders and can be misconfigured. Polling is simple/reconciling but costs listings and latency. Combine them.

**Full-object versus composite checksum.** Full-object values are direct byte identities under the algorithm. Composite checksums can validate multipart construction efficiently but require exact documented calculation/type.

**Checksum versus signature.** Checksums detect byte differences relative to a trusted value. Signatures authenticate canonical manifest intent but require key lifecycle and do not validate data semantics.

**Strict extra-file rejection versus manifest-only scope.** Rejection catches producer debris when the generation prefix is exclusive. Manifest-only reads coexist with staging/unrelated files but need clear namespaces/lifecycle.

**Per-file commit versus manifest-level commit.** Per-file output improves partial availability but complicates consistency. Manifest-level atomic publication gives a coherent dataset at higher completion latency.

**Delete after consume versus retain raw.** Early deletion saves storage but weakens replay/audit. Retention supports recovery but increases cost and privacy/security obligations.

**In-place correction versus superseding generation.** In-place edits appear simple but destroy reproducibility. Supersession preserves lineage and enables rollback at metadata cost.

**Fail-fast versus quarantine.** Fail-fast protects quality; quarantine preserves other independent work and diagnostics. Never let quarantine silently count as complete.

## Failure Modes and Misconceptions

- **“Visible means complete.”** One object says nothing about intended siblings.
- **“The directory stopped changing.”** Quiet time is not producer closure.
- **“Strong listing consistency solves batch completion.”** It reveals present objects, not intended future ones.
- **“Count equals expected, so set is complete.”** Missing and extra identities can cancel.
- **“Filenames uniquely identify bytes.”** Keys can be overwritten.
- **“Latest object is good enough.”** It breaks reproducibility and accepted-manifest integrity.
- **“Rename is atomic everywhere.”** Object-store rename may be copy/delete or unavailable.
- **“Write the manifest first so consumers prepare.”** It exposes dangling references.
- **“Notification means the upload is complete.”** Event semantics and multipart/object completion differ by source.
- **“Notifications arrive once.”** At-least-once systems can duplicate.
- **“Notifications preserve producer order.”** Many services explicitly do not guarantee it.
- **“Message ID is dataset identity.”** Retries can create distinct notification IDs for one object event.
- **“Polling is unnecessary with events.”** Reconciliation recovers lost/misconfigured notification paths.
- **“ETag is always MD5.”** Multipart/encryption/provider behavior can differ.
- **“Checksum proves correct data.”** It proves bytes match a declared digest under assumptions.
- **“Checksum authenticates the producer.”** An attacker who changes both needs separate trust controls.
- **“Length match is enough.”** Different content can have equal length.
- **“Valid Parquet/CSV means correct extraction.”** Format validity does not prove source scope.
- **“Zero-byte file is always corrupt.”** Role/format decides.
- **“Unknown schema fields can be dropped.”** They may contain required meaning.
- **“Extra objects should always be consumed.”** They may be staging, retries or attacks.
- **“Lexicographic file order is business order.”** Naming convention can change and parallelism is nondeterministic.
- **“A success marker explains itself.”** It needs generation/protocol binding.
- **“Lease expiry prevents stale commit.”** A fencing token must reject the old worker.
- **“Queue acknowledgement is a receipt.”** Downstream output may not be durable.
- **“Delete inputs after processing.”** Replay/rollback/receipt evidence may still require them.
- **“Fix the manifest in place.”** It invalidates prior digests and receipts.
- **“Partial batch is better than none.”** Only if consumers accept explicitly partial semantics.
- **“Archive paths are safe data.”** Traversal and decompression attacks require isolation/bounds.
- **“The watermark may advance past quarantine.”** Required unresolved input breaks completeness.

## Worked Examples

### Example 1

A producer uploads 99 of 100 files, pauses six minutes, then uploads the last. A consumer's five-minute quiet-period rule publishes a partial dataset.

The corrected producer publishes a 100-entry manifest only after all uploads and producer controls pass. Quiet time remains an alert signal, not completion evidence.

### Example 2

A manifest expects `{a,b}` and a listing contains `{a,c}`. Both counts are two, so a count-only check passes.

Exact identity set comparison reports missing `b` and extra `c`. Neither is silently substituted.

### Example 3

Two retries write different bytes to `part-000` under the same key. An earlier manifest contains only the path.

The consumer cannot reproduce the accepted generation. Versioned object identity or unique attempt/generation keys plus digest would bind the exact bytes.

### Example 4

An S3 notification is delivered twice and the second arrives after a newer manifest event. Two workers race.

Both retrieve immutable manifests. Conditional receipt/commit keyed by manifest ID/digest and fenced claims let each generation have one effect; generation ordering prevents the older one overwriting newer current state.

### Example 5

A multipart upload is abandoned after seven parts. A prefix lister sees no completed object but storage cost grows; a naive part-level event consumer might treat parts as data.

The pipeline subscribes only to committed object/manifest events and lifecycle-cleans abandoned multipart uploads after verifying they are not referenced.

### Example 6

A four-byte CSV file changes from `b,2\n` to `b,9\n`. Size validation passes.

The independently declared SHA-256 digest fails, so the generation is quarantined before parsing or watermark advance.

### Example 7

A malicious archive entry is named `../../credentials`. An extractor expands it using raw paths.

Safe processing rejects absolute/traversing normalized paths, enforces entry/expanded-size limits and parses in an isolated least-privileged workspace.

### Example 8

A consumer publishes a table, crashes before acknowledging the notification and receives it again.

Its durable receipt maps the same manifest digest to the already-published table generation. The retry verifies the receipt/output and acknowledges without duplicate append.

### Example 9

A producer discovers one partition was wrong and overwrites its manifest and file in place. Earlier reports can no longer be reproduced.

It instead publishes a new correction generation that supersedes the prior partition, retains immutable evidence and lets consumers apply version precedence with rollback.

### Example 10

Lifecycle rules delete data objects after seven days while manifests/receipts promise 30-day replay. A repair requested on day 10 fails.

Retention validation compares all referenced-object horizons. The policy retains or archives exact versions through the promised replay window and continuously alerts on dangling manifests.

## Cross-Program Connections

- [Database Engineering](../../18-database-engineering/ROADMAP.md): transactions, checksums, snapshot identity and atomic metadata publication inspire file-set commit protocols.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): contracts, ownership, lineage, retention and authoritative scope define manifest meaning.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): object storage, distributed commit, manifest scaling and parallel planning shape implementation.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): close, rename, sync, path normalization and filesystem semantics matter for local file drops.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): signatures, least privilege, path traversal, decompression bounds and sensitive metadata govern trust.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): at-least-once notifications, idempotency, fencing, immutable logs and partial failure explain receipts.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): event/webhook delivery contracts, idempotency keys and versioned resources parallel manifest processing.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): standardized producers, schema registries, quarantine, observability and repair tools make the boundary self-service.

## References

1. Amazon Web Services, [Amazon S3 Event Notification Types and Destinations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-event-types-and-destinations.html). Documents at-least-once notification delivery, possible duplicates and lack of event-order guarantee.
2. Amazon Web Services, [Checking Object Integrity in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html). Documents supported object checksum algorithms and integrity verification.
3. Google Cloud, [Pub/Sub Notifications for Cloud Storage](https://docs.cloud.google.com/storage/docs/pubsub-notifications). Documents object-event metadata, at-least-once delivery, duplicates and publication ordering limits.
4. Google Cloud, [Cloud Storage Consistency](https://docs.cloud.google.com/storage/docs/consistency). Documents object read/list consistency, individual-object atomicity and non-atomic batch operations.
5. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Defines immutable manifests, manifest lists, snapshots, file/delete entries, sequence metadata and atomic table-metadata pointer replacement.
6. Apache Hadoop, [Manifest Committer for Azure and Google Cloud Storage](https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/manifest_committer.html). Documents task manifests, job output commit and success-marker/report behavior.

## Exercises

### Exercise 1

Design a manifest for a daily three-part order extract. Include immutable identity, source interval, schema, per-file integrity, totals, encryption, publication, correction and consumer receipt fields. State which fields must be authenticated.

### Exercise 2

A manifest declares files `{a@v1,b@v4,c@v2}` with sizes 10, 20 and 30. Storage resolution returns `{a@v1,b@v5,d@v1}` with the same three-object count and total size 60. Determine missing, mismatched/extra identities and whether the batch is complete.

### Exercise 3

Design a producer/consumer failure-injection matrix for crashes before/during/after data upload, manifest publication, notification, downstream output, receipt and acknowledgement. State expected replay behavior.

### Exercise 4

An ingestion worker validates a ZIP object from an external producer. Define structural, integrity, authentication, archive-safety, schema, semantic and privacy controls before publication.

### Exercise 5

Plan a correction for an already accepted monthly manifest whose one partition omitted refunds. Include immutable supersession, version ordering, replay, downstream publication, watermark handling, communication, retention and reconciliation.

## Answers to the Exercises

### Answer 1

Use manifest ID/digest, generation, producer/run, predecessor, dataset/tenant scope, source interval/watermarks and full/incremental kind. Bind contract/data schema IDs and partition spec. Each of three entries records bucket/key/object version, role/partition, format/codec, stored bytes, full-object checksum algorithm/value, rows/control statistics, encryption algorithm and managed key-version reference. Totals give file count 3, bytes, rows and independent business controls. Publication metadata records producer validation and published time; correction fields identify superseded generation/partitions. Consumer receipt binds exact input versions/digests, validator/consumer version, output generation, controls and commit time.

Authenticate all semantics that authorize processing: identity/generation, scope/interval, schema, exact entries/integrity values, totals, encryption references, supersession and publication metadata. Sign a canonical representation with governed producer identity where threat/risk requires it; keep secrets out of the manifest.

### Answer 2

Expected identities are `a@v1`, `b@v4`, `c@v2`. Only `a@v1` matches. `b@v4` and `c@v2` are missing. `b@v5` is not a substitute for `b@v4`; it is an extra/mismatched version. `d@v1` is extra. Equal count three and total bytes 60 do not establish exact identity equality, so the batch is incomplete/invalid and must not publish or advance its watermark.

### Answer 3

Before/during data upload, no manifest exists and consumers publish nothing; abandoned objects/parts are later cleaned safely. After all data but before manifest, data remains uncommitted debris. During manifest write, individual-object atomicity or generation-scoped finalization must expose either no valid manifest or one complete immutable manifest. After manifest before notification, periodic manifest reconciliation discovers it.

Duplicate/delayed/out-of-order notifications retrieve immutable identity and converge through receipt deduplication. Crash during downstream staging leaves no published pointer. Crash after output publication but before receipt requires immutable output reconciliation to finish the receipt without duplicate effect; preferably output and receipt commit atomically. Crash after receipt but before acknowledgement causes redelivery, which returns the prior receipt. Every case preserves exact inputs, state evidence and alerts; none advances input progress before durable output/receipt.

### Answer 4

Bound manifest/archive/object sizes first; authorize bucket/key/version and verify declared length/full-object digest plus producer signature/trust. Reject unsupported encryption/codec/archive types, path traversal, absolute/device/symlink entries, duplicate normalized names, excessive entry count, nesting, compression ratio and expanded bytes. Expand in an isolated least-privileged filesystem with quotas/timeouts and no executable interpretation.

Validate every extracted file's expected identity/digest if enumerated, magic/version, parser completeness and schema ID/compatibility. Enforce row/field sizes, types, keys, partition/source interval, counts and control totals. Scan/classify sensitive/malicious content under policy, encrypt/quarantine evidence and restrict diagnostics. Only a complete manifest-level result can publish; checksum alone is insufficient.

### Answer 5

Freeze the bad manifest, receipt and output for evidence. Publish a new correction manifest/generation with a new ID/digest, predecessor/supersedes relation, exact affected partition and source interval, corrected immutable file versions, reason and approved contract/schema. Ensure its ordering is newer and old delayed delivery cannot overwrite it.

Validate refund keys/components against an independent control, replay the correction into a new output generation, reconcile unaffected and affected partitions, then atomically publish. Do not move the live extraction watermark backward or forward merely for correction; track repair state separately and preserve the source cut. Notify consumers of restatement/version, invalidate caches, retain both generations/receipts through audit policy, and confirm downstream reports use the corrected generation with rollback available.
