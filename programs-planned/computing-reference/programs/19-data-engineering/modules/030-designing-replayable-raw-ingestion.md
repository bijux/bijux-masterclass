---
module_id: DE-030
program: Data Engineering
level: 1
module_number: 30
title: Designing Replayable Raw Ingestion
status: complete
last_verified: 2026-09-02
---

# Designing Replayable Raw Ingestion

## One-Page Review

### Governing question

How can an ingestion boundary preserve every intended source occurrence and its interpretation context so trusted datasets can be reproduced or deliberately recomputed after defects, schema changes, retention loss, platform migration, or disaster—without rereading a source that may no longer contain the same history?

### Essential definitions

- **Raw ingestion** captures the highest-fidelity source representation and source context available under a declared contract before lossy business transformation.
- An **authoritative raw layer** is the governed recovery source whose completeness, immutability, identity, retention, access, and restore behavior support declared replay claims.
- A **logical occurrence identity** names one source file/object version, API item/page at a source cut, database change, transaction, message, or record across delivery retries.
- A **source coordinate** is a source-scoped position such as object version/path, manifest member, cursor/snapshot token, LSN, topic/partition/offset, sequence, or transaction ordinal.
- A **landing receipt** atomically binds occurrence identity and source coordinate to payload digest, stored object/version, metadata, and outcome.
- A **raw manifest** lists the expected and landed units for one immutable generation/range, with counts, sizes, digests, schema/envelope identities, controls, and publication state.
- An **interpretation bundle** identifies writer schema, serialization/framing, compression, encryption/key context, code/configuration, and reference data needed to decode and transform raw evidence.
- **reproduction** reruns the original transformation contract to obtain the same governed output; **recomputation** intentionally runs a new contract and creates a new output generation.
- A **trusted pointer** selects a complete immutable manifest/snapshot for readers; staging paths are never treated as published data.
- A **replay horizon** is the interval for which raw payloads, manifests, identities, schemas, code, keys, dependencies, and target correction mechanisms all remain usable.
- **immutability** means prior accepted object versions and manifests cannot be silently changed under the stated storage, identity, permission, and retention controls; a reused path name alone is insufficient.

### Central model, mechanism, or theorem

Let $I_b$ be the exact ordered/partitioned set of in-scope source occurrences through boundary $b$, and let $R_b$ be their immutable raw representations plus interpretation/lineage metadata. If capture is complete and injective by occurrence identity, then

$$
decode(R_b)=I_b.
$$

For deterministic transformation contract $T_v$ whose code, configuration, schemas, reference snapshots, time/randomness inputs, and execution semantics are preserved,

$$
T_v(R_b)=O_{b,v}
$$

on every supported replay. A new contract $T_w$ may intentionally produce $O_{b,w}$; it must not overwrite or masquerade as reproduction of $O_{b,v}$.

Source checkpoint $C$ may advance only through the greatest boundary $D_R$ represented by a complete durable raw receipt/manifest:

$$
C\preceq D_R.
$$

### Critical invariants

- Source identity/epoch, scope, coordinate domain, ordering/transaction boundary, and expected input set are explicit.
- One occurrence identity binds to one original payload digest and landing receipt; equal identity with unequal payload fails closed.
- Raw capture preserves original bytes/envelope where available and records every unavoidable acquisition-time transformation or source limitation.
- Data objects, sidecar metadata, schema/decoder material, and expected manifest become durable before source acknowledgement/checkpoint.
- Manifests prove expected-set completeness and exact membership; directory listing, latest timestamps, and row counts alone do not.
- Staging writes are invisible to trusted readers; a complete validated manifest is published with an atomic conditional metadata/pointer transition.
- Reproduction pins code, configuration, writer/reader schemas, libraries/runtime, reference snapshots, time/random seeds, and target semantics required by $T_v$.
- Replay preserves occurrence/effect identity and writes a new idempotent output generation; it never appends blindly or mutates raw evidence.
- Checksums are verified at capture, rest, retrieval, copy/migration, and restore while remaining separate from source correctness/completeness claims.
- Replay horizon is bounded by the earliest expiry of every required payload, manifest, schema, key, code, dependency, identity, and correction capability.
- Security, privacy, deletion, legal hold, and tenant isolation apply to raw and replay because raw data maximizes fidelity and risk.

### Common failures

Calling a mutable landing bucket “raw”; overwriting `latest.csv`; using path or ingestion timestamp as identity; keeping decoded JSON but discarding original framed bytes; stripping unknown fields; losing writer schemas or compression dictionaries; acknowledging a broker before durable raw commit; discovering a manifest by storage listing; publishing partial partitions; using ETag as an assumed universal content hash; relying on object versioning without recording the version; claiming WORM while privileged deletion/lifecycle remains unexamined; replaying against today's mutable lookup; reading current time/random/network during reproduction; assigning new event IDs; appending replay output beside old output; expiring raw before receipts; retaining encrypted bytes after deleting needed keys; hand-editing bad raw; or asserting replayability without a restore-and-rebuild exercise.

### Compact example

Positions 101–103 arrive with one repeated delivery of 102. The landing service binds each source coordinate to a byte digest, writes three content-addressed raw objects and metadata, validates the expected position set, publishes one manifest, then checkpoints 103. Replay with transformation `v1` deterministically totals 6; deliberate `v2` recomputation totals 60 in a new generation. A missing 102 leaves the manifest unpublished and checkpoint at 100. Reusing 102 with different bytes is an identity conflict, not a new raw version.

### Connections

[DE-021](021-full-and-incremental-extraction.md) defines source scope, [DE-022](022-watermarks-and-high-water-marks.md) constrains progress, [DE-023](023-file-arrival-and-manifest-processing.md) supplies manifest publication, [DE-024](024-api-based-ingestion.md) and [DE-025](025-database-snapshot-extraction.md) define source cuts, [DE-026](026-database-change-data-capture.md) supplies change positions, and [DE-027](027-idempotent-loads.md) through [DE-029](029-quarantine-and-dead-letter-data.md) provide replay-safe effects, identity, and containment.

## Governing Question

What current evidence would let a different operator, in a restored environment months later, reconstruct the same intended input population and either reproduce the original output or run an explicitly new transformation—without trusting mutable source state, directory listings, process memory, or folklore?

Replay begins before storage. An API may expose only current state; a transaction log may recycle; a queue may expire acknowledged messages; a file can be replaced at the same path; a database snapshot token can become invalid. If ingestion discards the highest-fidelity evidence or advances source progress too early, no later lake layout can restore the lost history.

“Raw” is not a color or folder name. It is a bounded evidentiary claim about source scope, occurrence identity, payload fidelity, ordering, schema, lineage, completeness, immutability, and retention. A CSV produced by a lossy API client might be the highest accessible representation, but it is not the original server database. The contract must state that limitation.

Replay is also more than reading old files. The transformation may depend on a writer schema, library behavior, time zone database, reference dimension, feature flag, current time, random sampling, network lookup, or target merge semantics. Retaining bytes while losing their interpretation or deterministic dependencies creates archaeological storage, not reliable replay.

Finally, a replay must correct outputs safely. It should preserve source occurrence identity, avoid duplicate effects, publish a distinct generation, reconcile scope and controls, and retain lineage between superseded and replacement outputs. Otherwise recovery can compound the original defect.

## Why This Matters

Sources are often less replayable than pipelines assume. Broker retention is finite, API cursors expire, CDC log slots can fall behind, SaaS objects mutate, and operational databases delete or update history. An authoritative raw layer decouples downstream recovery from those source windows after one complete durable capture.

Raw replay enables defect repair. A parsing bug that shifted decimals, a schema reader that ignored a field, a timezone mistake, an incorrect identity rule, or a corrupted reference join can be recomputed from preserved evidence. Without raw, teams must request a new source extract that may represent a different point in time or may be impossible.

It enables platform evolution. Data can be reserialized, repartitioned, re-encrypted, compacted, or migrated while the original generation remains verifiable. A new query engine or table format can be validated against the same source population instead of comparing moving inputs.

It strengthens audits. Manifests and receipts connect source coordinates and object digests to transformations, schemas, quarantine decisions, and output generations. An output row can be traced back without assuming that current source state still contains it.

Replayability also limits blast radius. Downstream consumers can rebuild independently from durable raw rather than couple source log retention to every sink. The raw layer becomes critical infrastructure, however: corruption, credential compromise, silent lifecycle expiry, unavailable keys, or incomplete backups can break many recovery paths at once.

High fidelity increases risk and cost. Raw can include deleted personal data, secrets accidentally emitted by producers, unknown binary content, or fields never meant for broad analysis. Strong access, minimization at source where lawful, retention/deletion workflows, safe tooling, and tenant separation are part of the replay design—not later housekeeping.

## Prerequisites and Retrieval

Retrieve the data product/source owner; business purpose; source system/cluster/account/tenant/epoch; source topology/failover; extraction/capture mechanism; source retention and replay limits; object path/version/manifest, API cut/cursor/request, snapshot/log/LSN, topic/partition/offset, transaction and record ordinal; source ordering and commit boundaries; expected populations and exclusions; delivery/redelivery semantics; payload bytes and envelope; headers/properties; content type; encoding; framing; compression and dictionaries; encryption and key version; signatures/authentication; writer schema ID/content; source types/time zones/collation; deletes/tombstones; code/config/library/runtime/connector versions; canonical occurrence identity; object naming and content addressing; checksum algorithm/type/scope; multipart behavior; storage version/generation; write preconditions; immutability/Object Lock/WORM/legal hold; staging and publication; raw manifest schema; landing receipts; acknowledgement/checkpoint transaction; quarantine; late/gap behavior; partitioning; target formats; reference-data snapshots; deterministic time/random/environment; replay code and infrastructure; idempotent target receipts; output versioning/supersession; retention and lifecycle; privacy classification/consent/deletion; tenant/IAM/network/encryption; restore/DR; observability; reconciliation; capacity/cost; and replay exercise history.

Distinguish source truth from captured representation; original source bytes from client-serialized values; payload from transport envelope; object name from immutable object version; checksum from authenticity, validity, or completeness; compression checksum from application content digest; ETag from a guaranteed universal hash; occurrence identity from payload digest; event time from capture time; source coordinate from wall-clock; ordered partition from global order; transaction envelope from row events; write success from manifest publication; durable object from durably discoverable receipt; storage listing from expected manifest; staging from trusted generation; replayable raw from recoverable backup alone; reproduction from recomputation; same code label from same runtime/dependencies; current lookup from historical reference snapshot; idempotent effect from exactly one delivery; logical deletion from physical erasure; and retained ciphertext from usable data if keys are gone.

Write a replay contract before capture:

| Concern | Required evidence |
|---|---|
| Source boundary | Source/epoch/scope, cut or coordinate domain, expected population, exclusions |
| Occurrence | Stable identity, transaction/order, payload binding, duplicate/conflict behavior |
| Fidelity | Original/highest-fidelity bytes, envelope, acquisition transformations/limitations |
| Interpretation | Encoding/framing/compression/encryption, writer schema, type/time semantics |
| Storage | Object version/generation, content digest, size, write precondition, immutable retention |
| Completeness | Expected manifest members/ranges, gaps, counts/bytes/controls, quarantine disposition |
| Publication | Staging rules, validated manifest, atomic conditional trusted pointer |
| Transformation | Code/config/runtime/library/reference/time/random inputs and output contract |
| Replay | Selection manifest, isolated execution, stable IDs, target generation, reconciliation |
| Lifecycle | Retention horizon, key/schema/code preservation, privacy deletion, migration, restore test |

State the claim as a testable sentence: “For source cluster epoch `e4`, committed partitions 0–15 through offsets recorded in manifest `m`, every occurrence envelope and writer schema is preserved under immutable object versions; transformation bundle `v7` reproduces output snapshot `o`, and bundle `v8` recomputes a separately published successor.”

## Learning Objectives

After completing this module, you should be able to:

1. define an authoritative raw boundary and state its source-fidelity limitations;
2. model source coordinates, occurrence identities, payload digests, landing receipts, and manifests separately;
3. couple source acknowledgement/checkpoint to durable raw evidence without silent loss;
4. preserve transport envelopes, writer schemas, encoding, framing, compression, encryption, ordering, and transaction context;
5. use immutable versions, content addressing, checksums, and conditional publication without overstating any one control;
6. prove expected-set completeness and publish only validated raw generations;
7. distinguish deterministic reproduction from intentional recomputation under a new contract;
8. replay through stable identities into idempotent versioned targets with quarantine and rollback;
9. calculate the effective replay horizon across payload, metadata, schema, key, code, dependency, and correction retention; and
10. validate security, deletion, migration, restore, reconciliation, and end-to-end replay through exercises.

## Core Exposition

### Begin with recovery questions

List the failures raw replay must address: lost target, transformation bug, corrupted derived partition, schema-reader defect, incomplete deployment, source retention expiry, region loss, storage migration, privacy correction, and deliberate business-rule restatement. Different cases require different evidence.

For each case state recovery point, recovery time, source range, output granularity, and whether the goal is byte-for-byte reproduction, semantic reproduction, or new recomputation. A floating-point engine change may prevent byte identity while preserving declared decimal semantics; an audit may require the original exact artifact.

Do not claim arbitrary replay if operations only support last seven days or if transformations depend on current reference data. Publish the proven horizon and exercise it.

### Define “raw” relative to the accessible source

Capture the earliest, highest-fidelity representation the source contract permits. For a file feed, that may be exact received compressed bytes plus transport metadata. For a broker, it may be key, value bytes, headers, timestamp type/value, topic/partition/offset, producer metadata, and transaction context. For an API, it may be HTTP response bytes/headers and request/cursor at a documented source cut. For database CDC, it may be connector envelopes rather than physical WAL bytes.

Record transformations that necessarily occur before capture: TLS termination, SDK decompression, character decoding, API field projection, driver type conversion, logical decoding, connector single-message transformation, or gateway redaction. “Raw” then means raw at that declared boundary, not unmodified source internals.

Where feasible preserve both original object/envelope bytes and a validated query-friendly landing representation, linked by a manifest. The query-friendly copy is a derivative; it never substitutes silently for evidence.

### Freeze source identity, epoch, and scope

An offset `42` is meaningless without topic, partition, cluster/logical source, and epoch. Object path `daily.csv` is mutable without bucket/account and version/generation. API page 5 is unstable without query, source snapshot/cursor, ordering, and response identity.

Define source tuple

$$
S=(provider,account,system,instance,epoch,scope).
$$

Every occurrence coordinate is interpreted inside $S$. Failover, restore, topic recreation, connector reset, table replacement, or producer-key reuse can create a new epoch. Never compare or concatenate positions across epochs without an explicit continuity proof.

Scope includes filters, tenant/security context, tables/topics/endpoints, fields, deleted records, transaction status, time/partition ranges, and exclusions. Preserve the contract version with each manifest.

### Derive stable occurrence identity

Prefer source-native immutable coordinates when their domain guarantees one logical occurrence: object version plus member/record ordinal; cluster/topic/partition/offset; database/topology/transaction/row ordinal; API resource version within a snapshot; or producer event ID with source epoch.

If no stable ID exists, construct one from the strongest source coordinates and canonical framing, record uncertainty, and detect payload conflicts. Content digest alone cannot distinguish two legitimate equal-payload events. Ingestion attempt UUID cannot recognize redelivery.

Bind identity $O(u)$ to payload digest $h(u)$ and envelope digest/version. Equal identity/equal digest is replay. Equal identity/unequal digest is a source or lineage conflict requiring containment, not overwrite.

### Preserve bytes, boundaries, and framing

Exact bytes matter when parsing or serialization may be defective. Preserve byte order, length, framing boundaries, compression container, archive member names/order, and record delimiter behavior. A text reader that normalizes line endings or replaces invalid characters has already lost evidence.

For messages, retain key/value separately and all interpretation-relevant headers. For files, preserve original object plus provider version/generation, size, modification/server timestamps, checksum metadata, multipart/composite context, encryption metadata, and transfer receipt. For API responses, retain status, selected response/request headers, pagination/snapshot tokens, body bytes, request fingerprint, and safe rate-limit evidence.

Bound payload sizes and hostile formats as [DE-029](029-quarantine-and-dead-letter-data.md) requires. High fidelity does not mean unsafe automatic decompression or deserialization.

### Treat checksums as scoped evidence

Compute a strong application content digest over precisely specified bytes as close to acquisition as possible. Store algorithm/version, scope (compressed object, decompressed stream, record, envelope), multipart combination semantics, and expected source checksum where trustworthy.

Amazon S3 documents multiple full-object and composite checksum algorithms/types and integrity validation during upload/download. That makes checksum metadata useful, but the pipeline must not assume every ETag is the raw content MD5 or compare checksums computed over different byte scopes.

A matching digest shows that two observed byte sequences match under the algorithm's assumptions. It does not prove the producer sent every intended record, that bytes are authentic without a trust/signature mechanism, that parsing is correct, or that a manifest is complete.

Verify at initial transfer, durable commit, read/replay, replication/copy, storage-class restore, migration, and backup restore. Periodically scrub retained objects and treat mismatch as corruption requiring replica/source recovery and incident evidence.

### Use immutable object identities

Never make `raw/source/date/latest.json` the only identity. Record provider-specific immutable version/generation plus digest and size. Content-addressed object names can make accidental overwrites visible, but permissions and metadata still matter.

Amazon S3 Object Lock uses a WORM model, works with versioning, and protects specified object versions under retention/legal holds; it does not prevent creating a new version or adding a delete marker. Therefore readers must resolve the recorded locked version, not merely the current path.

Immutability claims include retention mode, privileged bypass/delete behavior, bucket/account controls, replication, lifecycle, legal holds, encryption-key availability, audit, and restore. Test them in the deployed configuration.

### Make writes conditional

Race-safe landing must prevent two writers from silently replacing the same logical object or publication pointer. Use create-if-absent, generation/version match, ETag/compare-and-set under documented semantics, unique database constraints, or transactional metadata commits.

Google Cloud Storage documents generation/metageneration preconditions for conditional operations and preventing race conditions. A failed precondition is not a nuisance to retry blindly; it signals that another state exists and must be compared by identity/digest.

Write large objects to unique staging identities, verify close/size/digest, then create the immutable landing receipt conditionally. Avoid list-then-put as the correctness arbiter because another writer can race between calls.

### Couple durable raw to source progress

For source checkpoint/acknowledgement $C$ and greatest position $D_R$ whose required raw data, envelope, schema reference/content, receipt, and complete manifest are durable, require

$$
C\preceq D_R.
$$

If raw commits and acknowledgement is lost, source replay occurs; idempotent occurrence binding makes it a no-op. If acknowledgement advances before raw durability, source retention can erase the only copy.

Where source and raw store lack one transaction, use an idempotent two-step protocol: write immutable content; conditionally bind receipt/manifest; only then acknowledge. On restart query the receipt by source coordinate/digest before writing. Never infer outcome solely from a timeout.

If capture acknowledges after durable per-record raw but before parent manifest publication, the raw store must retain enough expected-set/source-range metadata to complete or diagnose the manifest. Distinguish “durably landed” from “published complete generation.”

### Build manifests from expectations, not listings

A storage listing reports what is visible under a prefix at observation time. It does not reveal expected missing objects, concurrent uploads, wrong versions, extras, or source scope. Construct the expected set from a source manifest, bounded offsets, exported snapshot partition plan, API cut/page protocol, or other authoritative control.

A raw manifest records generation/source scope, expected and landed occurrence/range membership, object versions/digests/sizes, encoding/schema/envelope, transactions/order, counts/bytes/control totals, empty partitions, quarantine states, capture software/configuration, acquisition times, validation results, and predecessor/successor continuity.

Require exact set equality where enumeration is possible:

$$
E_b=L_b,
$$

not merely $|E_b|=|L_b|$. Equal counts can hide one missing and one unexpected object.

### Publish manifests atomically

Stages are untrusted. After all expected members and controls validate, write an immutable manifest and conditionally update a trusted pointer/catalog entry from expected predecessor to new generation. Loss of acknowledgement is resolved by reading the pointer and comparing manifest identity.

Apache Iceberg's specification illustrates a metadata architecture in which table-state changes create new metadata and replace old metadata with an atomic swap; snapshots track complete data-file sets through manifests. A raw-ingestion design can use analogous immutable-generation publication without claiming that every raw store is an Iceberg table.

Never let readers infer completeness from the newest directory or file modification time. Preserve prior manifests for rollback/audit and prevent cleanup of any generation referenced by active/published snapshots or replay plans.

### Preserve writer schemas and decoding rules

Serialized bytes are not self-explanatory. Store writer schema ID and immutable schema content or a content-addressed registry reference whose retention/availability is proven. Record format/spec version, codec, logical types, defaults, aliases, union/tag conventions, and relevant library behavior.

Apache Avro's specification defines writer/reader schema resolution, including promotion, defaults, aliases, and incompatible cases. Replaying Avro with today's reader schema can be intentional recomputation, but reproducing the original interpretation needs the original writer schema and reader contract.

Unknown writer schema must not be guessed. Preserve bytes and quarantine/stop the semantic stage while raw capture continues only if envelope framing, security, and source acknowledgement remain safe.

### Preserve file-level interpretation

Columnar files include structural metadata beyond rows. Apache Parquet documents file metadata after column chunks, row groups, schema/encoding information, metadata length, and magic markers. A valid header/footer does not prove every logical row is correct, but losing/truncating the footer can make data undecodable.

Record file format/version, writer, schema, row groups, codecs, page/index/checksum features, time/logical-type conventions, and encryption/footer settings. Validate with independent readers where risk warrants. Preserve the original file even if a derived normalization rewrites it.

Do not concatenate or edit binary files as if they were line streams. Compaction creates a new derived generation with its own manifest and lineage.

### Preserve transport and transaction context

For ordered streams store topic/partition/offset (or equivalent), key, headers, broker timestamp and type, producer/schema identity, transaction/commit status, and sequence metadata. “Arrival time” cannot reconstruct source order.

For CDC preserve source engine/topology epoch, database/table identity, log position, transaction ID/ordinal/count/boundary, operation, before/after availability, schema position, snapshot flag, and connector envelope/configuration. PostgreSQL logical-decoding documentation describes slots, WAL retention, confirmed positions, and crash/replay considerations; retrieve engine-specific semantics rather than treat LSN as a generic integer.

Do not publish aborted/uncommitted transaction fragments into a trusted raw transaction manifest when the contract is committed changes. It may be reasonable to preserve lower-level bytes for forensic purposes, but label that boundary separately.

### Model time without replacing order

Keep source event/valid/commit time, broker time, source-observed time, capture time, landing-commit time, and publication time separately with time zone/precision/origin. Replay should not substitute capture time for event time or use “now” as an unstated default.

Clock order cannot replace partition/log/source version order. Equal timestamps are common; clocks skew; API timestamps can be updated retroactively. Store the source coordinate domain that actually governs progress and per-key versions.

If transformation uses calendar rules or time-zone databases, preserve their version or materialize the resolved business date as governed input. Historical timezone/rule changes can alter recomputation.

### Record provenance as queryable lineage

W3C PROV-O defines concepts for representing/interchanging provenance of entities, activities, and agents. Whether or not the ontology is adopted, raw ingestion should answer: which source occurrence/entity produced this object; which capture activity/code/config/schema created it; which agent/service authorized it; which manifest published it; and which output/replay derived from it?

Store lineage in durable metadata, not only ephemeral logs. Link raw objects to landing receipts, manifests, quarantine decisions, transformation runs, output snapshots, supersession, and deletion. Ensure lineage metadata itself is backed up, versioned, access-controlled, and reconciled.

Avoid putting secrets or full sensitive payloads into lineage fields. References should be immutable and resolvable by authorized tools without widening access.

### Make transformations deterministic by contract

For reproduction, transformation $T_v$ must receive explicit inputs: raw manifest; code commit/artifact digest; configuration; schema readers; library/runtime/container/architecture where relevant; locale/collation/time zone; reference-data snapshots; feature flags; fixed time; random seeds/algorithm; partitioning/order; numeric precision/rounding; and target write semantics.

Eliminate or capture network lookups, current database state, environment defaults, filesystem/listing order, nondeterministic SQL peers, process hash seeds, concurrency races, and floating-point aggregation order where they affect output. “Same source code” is insufficient when dependencies float.

Define comparison: byte digest, exact typed row multiset, ordered events, decimal control totals, or domain invariants with allowed physical differences. Reproduction evidence follows that declared equivalence.

### Distinguish reproduction from recomputation

Reproduction runs original $T_v$ on $R_b$ to obtain output equivalent to $O_{b,v}$. Recomputation runs $T_w$—perhaps fixed parsing, new business logic, or new schema—and creates $O_{b,w}$. Both are useful; only the first tests original reproducibility.

Never mutate old output or reuse its generation identity for $T_w$. Record supersession link, changed contract/reason, affected raw range, validation, approval, and downstream migration. Consumers choose old/new through atomic versioned publication.

If original code is unsafe or unavailable, mark reproduction unsupported and preserve enough evidence for controlled semantic reconstruction. Do not silently call a best-effort rebuild “identical replay.”

### Replay through an immutable selection manifest

Select exact raw manifest(s), occurrence IDs, object versions/digests, source ranges, schemas, and quarantine states. Snapshot the selection; do not let a live prefix query change membership during replay.

Provision isolated compute and output namespace. Verify all inputs and interpretation dependencies before expensive work. Canary representative partitions, compare to expected original or corrected controls, then expand within capacity. Record run attempts and failures.

Preserve original occurrence/effect IDs. Use [DE-027](027-idempotent-loads.md) receipts so retry or overlap creates one output effect. Publish only a complete validated new generation; never append corrected duplicates beside trusted old rows.

### Reconcile replay end to end

For the selected raw generation verify input object set/digests, decode counts/errors, occurrence identities, transaction/order coverage, quarantine/exclusion, transformation artifact/config/reference digests, output partitions/keys/counts/control totals, and lineage edges.

For reproduction, compare against original output under declared equivalence and investigate every difference. For recomputation, compare expected semantic deltas and prove unaffected domains remain stable. Validate downstream aggregates, permissions, deletions, and contracts before pointer transition.

Record replay completion only after output manifest publication and downstream obligations are durable. Failed/cancelled output remains untrusted and garbage-collectable after retention/debug windows.

### Compute the real replay horizon

Let retention horizons from capture time be $T_{payload}$, $T_{manifest}$, $T_{schema}$, $T_{key}$, $T_{code}$, $T_{reference}$, $T_{identity}$, and $T_{target}$. The effective replay horizon is bounded by

$$
T_{replay}\le\min(T_{payload},T_{manifest},T_{schema},T_{key},T_{code},T_{reference},T_{identity},T_{target}).
$$

Keeping raw ciphertext for seven years does not enable replay if decryption keys expire in one. Keeping code without its container/package repository may not reproduce it. Keeping payloads without source identity/tombstone receipts can make reapplication unsafe.

Align lifecycle policies and test restoration before the shortest horizon. If privacy/legal policy requires earlier deletion, narrow the replay claim and use new source baselines or irreversible aggregate evidence where authorized.

### Apply security and privacy at maximum fidelity

Raw often contains more fields and longer history than curated outputs, including malformed or unexpected secrets. Default-deny access, separate tenant/security domains, encrypt in transit/at rest, govern key rotation/restore, audit access, scan hazardous formats safely, and provide bounded redacted inspection tools.

Minimize collection at the source contract where data is unnecessary; “raw” is not permission to retain everything. Enforce purpose, residency, retention, legal hold, consent, and subject deletion across payloads, copies, manifests, backups, caches, and derived replay outputs.

Deletion can conflict with reproducibility. Record a deletion/tombstone event and create a new compliant generation; physically erase required data and keys under policy; preserve only permitted non-sensitive proof. Historical output may become intentionally non-reproducible, and documentation must say so.

### Migrate and compact without erasing lineage

Raw object layouts may accumulate tiny files or obsolete formats. Treat compaction, reserialization, repartitioning, recompression, re-encryption, and region/provider copy as derivations. Verify source and destination manifests/digests and preserve mapping between old and new objects.

Do not delete original generation until the new representation's equivalence, interpretation bundle, access, retention, restore, and replay have been tested and policy authorizes supersession. Content-level equivalence may differ from byte identity; state which was proven.

Keep manifest/catalog history stable across path moves. A redirect that depends on a mutable database with no backup is not durable lineage.

### Back up the metadata and restore path

Object durability is not a complete disaster-recovery plan. Back up manifests, receipts, schemas, code artifacts, registry mappings, encryption/key metadata, catalog pointers, IAM/policy configuration, and replay runbooks. Protect against account compromise and correlated region/provider failure according to risk.

Exercise restore into an isolated environment. Verify digests, versions, schemas, keys, pointer reconstruction, access boundaries, expected-set reconciliation, transformation execution, output publication, and measured recovery time. A storage replication status alone does not prove usability.

### Observe capture and replay continuously

Measure source-to-raw lag, oldest recoverable source position, landed/duplicate/conflicting/missing occurrences, object/byte counts, checksum failures, manifest publication latency, pending/quarantine age, schema/key/dependency horizon, storage/cost growth, lifecycle deletions, scrub/restore results, and replay outcomes.

Alert on checkpoint ahead of raw, gaps/overlaps, same-ID/different-digest, unknown schema/envelope, unversioned object reference, manifest mismatch, conditional-write conflict, checksum corruption, shortest-horizon breach, unauthorized access, key expiry, unexpected lifecycle action, restore failure, and nondeterministic replay.

An idle source can legitimately produce no data. Heartbeats/control records should establish connector liveness and source position without being counted as business occurrences. A running connector alone does not prove completeness.

### Test the whole recovery claim

Inject failure before/after object write, receipt, manifest member, manifest validation, pointer commit, source checkpoint, and acknowledgement. Repeat delivery, change payload under same occurrence identity, omit/duplicate/replace a member, corrupt bytes/metadata, lose publication acknowledgement, and race writers.

Test empty/full/large transactions, source failover epoch, out-of-order partition delivery, schema unavailable/incompatible, compression truncation/dictionary loss, encoding errors, multipart checksums, writer/reader upgrades, key rotation/loss, hostile payload, and quarantine paths.

Replay with original bundle twice for deterministic comparison; replay with deliberate new bundle into a separate generation; inject mutable current lookup/time/randomness; overlap backfill/live capture; fail output midway; retry; publish/rollback; and verify downstream supersession.

Expire/restore payload, manifest, schema, code package, reference snapshot, receipt, key, and backup independently. Measure actual replay horizon and recovery time rather than infer them from configured retention.

## Definitions and Notation

Let:

- $S$ be the fully scoped source identity/epoch;
- $b$ be a source boundary in a documented position domain;
- $I_b$ be exact intended source occurrences through $b$;
- $O(u)$ be logical occurrence identity of source unit $u$;
- $p(u)$ be the highest-fidelity captured payload/envelope;
- $h(u)$ be digest of explicitly scoped bytes;
- $R_b$ be immutable raw objects, receipts, manifest, and interpretation metadata for $I_b$;
- $E_b$ and $L_b$ be expected and durably landed occurrence sets;
- $C$ be source checkpoint/acknowledgement position;
- $D_R$ be greatest source boundary durably represented in authoritative raw;
- $T_v$ be deterministic transformation contract/version $v$;
- $O_{b,v}$ be output generation from $R_b$ under $T_v$;
- $P$ be trusted publication pointer; and
- $T_{replay}$ be effective replay horizon.

Occurrence binding requires

$$
O(u)=O(v)\implies
\begin{cases}
replay, & h(u)=h(v),\\
conflict, & h(u)\ne h(v).
\end{cases}
$$

Manifest completeness requires exact membership

$$
E_b=L_b
$$

plus per-member digest/schema/metadata and cross-member controls. Count equality is necessary but not sufficient.

Capture progress safety is

$$
C\preceq D_R.
$$

Conditional reproduction requires

$$
decode(R_b)=I_b,\qquad T_v(R_b)=O_{b,v}.
$$

The equality relation for output must be declared: byte-identical, ordered records, typed row multiset, or domain semantic equivalence. A new transformation $T_w$ yields a distinct generation $O_{b,w}$ even if some values happen to match.

## Mechanisms, Invariants, or Proof Structure

**Conditional replay theorem.** Suppose (1) $E_b$ exactly defines in-scope source occurrences; (2) each occurrence is captured once by identity with immutable payload/envelope and complete interpretation metadata; (3) $E_b=L_b$ and manifests/receipts remain durable; (4) $T_v$ is deterministic with every semantic dependency preserved; and (5) target application/publication is idempotent and versioned. Then replaying manifest $R_b$ under $T_v$ produces output equivalent to original $O_{b,v}$ under the declared comparison, independent of delivery repetition.

**Proof sketch.** Exact set equality and occurrence binding provide the same logical input population despite duplicate physical deliveries. Payload digests/immutable versions plus decoding metadata provide the same decoded inputs. Preserved deterministic $T_v$ and dependencies map equal inputs to equivalent outputs. Idempotent application removes physical retry multiplicity, and atomic manifest publication exposes only the complete generation. Missing source occurrences, lossy capture, changed schemas/dependencies, nondeterminism, or unmodeled external effects invalidate the corresponding step.

**Source-domain invariant.** Coordinates are compared only within compatible source/epoch/scope domains. Failover or recreation requires continuity proof or new epoch.

**Occurrence-binding invariant.** One $O(u)$ binds to one scoped $h(u)$ plus envelope/metadata. Equal/equal is replay; equal/unequal is conflict.

**Fidelity invariant.** Highest-available source representation is immutable; every acquisition transformation and omission is explicit. A derivative never silently replaces original evidence.

**Raw-progress invariant.** $C\preceq D_R$. Raw object, envelope, schema reference/content, receipt, and recoverable manifest boundary precede source acknowledgement.

**Expected-set invariant.** $E_b=L_b$ with no missing, extra, duplicated, wrong-version, or wrong-digest member and with all required controls/empty partitions represented.

**Publication invariant.** Trusted pointer changes only through conditional atomic commit to a complete immutable manifest; staging and failed generations remain untrusted.

**Interpretation invariant.** Writer schema, framing, encoding, compression, encryption/key, types/time, connector/reader contract, and versions remain resolvable for the replay horizon.

**Determinism invariant.** $T_v$ pins code, configuration, runtime/library, reference snapshots, time/randomness, order/partitioning, numeric semantics, and target behavior necessary for declared output equivalence.

**Replay-effect invariant.** Replay preserves source occurrence/effect IDs, writes a new output generation, uses idempotent receipts, and never commingles corrected and superseded effects invisibly.

**Horizon invariant.** $T_{replay}$ does not exceed the earliest expiry of payload, manifests, schemas, decryption keys, code/runtime, references, identity/tombstone evidence, and target correction capability.

**Governance invariant.** Access, purpose, residency, deletion, legal hold, audit, and tenant separation cover raw, metadata, backups, replay compute, and replacement outputs.

**Evidence boundary.** Successful replay proves the checked manifest/bundle/environment under declared equivalence. It does not prove source truth, universality across engines, or future replay after an untested dependency expires.

<!-- bijux-verify: {"id":"raw-manifest-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=4\nunique_occurrences=3\nduplicate_deliveries=1\nraw_objects=3\nmanifest_complete=True\ncheckpoint=103\nreplay_v1_total=6\nreplay_v2_total=60\ndeterministic_replay=True\ngap_unpublished=True\nidentity_conflict=True\n","stderr":""}} -->
```python
from hashlib import sha256

source = {
    101: b"001",
    102: b"002",
    103: b"003",
}
deliveries = (101, 102, 103, 102)

def capture(delivered, expected=(101, 102, 103)):
    objects = {}
    receipts = {}
    duplicates = 0
    for position in delivered:
        payload = source[position]
        digest = sha256(payload).hexdigest()
        if position in receipts:
            if receipts[position]["digest"] != digest:
                raise ValueError("source identity conflict")
            duplicates += 1
            continue
        objects[digest] = payload
        receipts[position] = {"digest": digest, "bytes": len(payload)}

    complete = set(receipts) == set(expected)
    manifest = tuple((position, receipts[position]["digest"]) for position in expected) if complete else None
    checkpoint = expected[-1] if manifest is not None else expected[0] - 1
    return objects, receipts, duplicates, manifest, checkpoint

def replay(objects, manifest, contract):
    assert manifest is not None
    values = []
    for _, digest in manifest:
        payload = objects[digest]
        assert sha256(payload).hexdigest() == digest
        value = int(payload)
        values.append(value if contract == "v1" else value * 10)
    return tuple(values)

objects, receipts, duplicates, manifest, checkpoint = capture(deliveries)
v1 = replay(objects, manifest, "v1")
v1_again = replay(objects, manifest, "v1")
v2 = replay(objects, manifest, "v2")
gap = capture((101, 103))

identity_conflict = False
conflicting_digest = sha256(b"999").hexdigest()
if receipts[102]["digest"] != conflicting_digest:
    identity_conflict = True

print(f"deliveries={len(deliveries)}")
print(f"unique_occurrences={len(receipts)}")
print(f"duplicate_deliveries={duplicates}")
print(f"raw_objects={len(objects)}")
print(f"manifest_complete={manifest is not None}")
print(f"checkpoint={checkpoint}")
print(f"replay_v1_total={sum(v1)}")
print(f"replay_v2_total={sum(v2)}")
print(f"deterministic_replay={v1 == v1_again}")
print(f"gap_unpublished={gap[3] is None and gap[4] == 100}")
print(f"identity_conflict={identity_conflict}")
```

The executable fixture models byte-preserving content-addressed objects, position receipts, duplicate delivery, exact expected-set manifest publication, checkpoint-after-manifest, deterministic reproduction, explicit new-contract recomputation, gap blocking, and changed-payload conflict. It uses in-memory integer positions and cannot prove durable storage, real source continuity, atomic provider operations, schema/key preservation, security, or production determinism.

## Alternatives and Trade-Offs

**Original bytes versus parsed canonical raw.** Original bytes maximize forensic/reparse fidelity but can be hard to query and risky. Parsed canonical raw improves usability but embeds parser/type decisions. Preserve both when justified and link them as original and derivative.

**Per-event objects versus batched immutable files.** Event objects simplify individual identity but create cost/listing scale. Batched files improve throughput/compression but need internal offsets/indexes, atomic manifests, and transaction/order boundaries. Hierarchical manifests combine them.

**Content-addressed names versus source-coordinate paths.** Content addressing exposes equal bytes and overwrite conflict; source paths aid operations/order. Store both digest and namespaced source coordinate rather than overload either as identity.

**Object versioning versus WORM/Object Lock.** Versioning preserves prior versions when used/retained correctly. WORM controls add deletion/overwrite protection for selected versions but increase operational/legal complexity. Neither replaces manifests, checksums, IAM, or restore tests.

**Per-record receipt versus range/file receipt.** Fine receipts support precise dedup/gap diagnosis but increase metadata. Coarse receipts reduce cost but need strong immutable membership/index evidence and can enlarge replay. Use parent/child manifests at scale.

**Acknowledge after each raw object versus after parent manifest.** Per-object acknowledgement reduces source retention if raw is authoritative and expected-set metadata survives. Waiting for full manifest simplifies source-range atomicity but couples lag to large batches. State which boundary raw guarantees.

**Raw files versus transactional table format.** Simple immutable objects minimize dependencies and preserve source artifacts. Table formats add snapshots, schema/partition metadata, pruning, and atomic commits but require catalog/protocol operation. Original artifacts can coexist with a queryable raw table derivative.

**Schema registry reference versus embedded schema content.** Registry IDs reduce duplication but can become unresolved after deletion/migration. Embedding/content-addressing improves autonomy at storage/privacy cost. Preserve at least an immutable resolvable schema artifact for the horizon.

**Reproduction container versus rebuildable environment.** Frozen images ease near-term replay but can become un-runnable/insecure. Reproducible builds preserve provenance and patchability but require retained sources/dependencies/toolchains. Test both restoration and policy exceptions.

**Long raw retention versus privacy minimization.** Long retention expands recovery/audit but also exposure, cost, and legal duties. Minimize scope, tier storage, restrict access, and make the replay claim conform to authorized retention rather than retain by default.

**Replay in place versus new generation.** In-place mutation is cheap but destroys rollback and can mix versions. A new generation costs space/compute but makes validation, supersession, and atomic publication explicit.

**Central raw fan-out versus direct source per consumer.** Central raw decouples source retention and standardizes evidence but becomes shared critical infrastructure. Direct consumers isolate ownership but multiply source load/slots and make cross-consumer recovery inconsistent.

## Failure Modes and Misconceptions

**“Raw means untouched source truth.”** Capture occurs at a boundary after possible source/API/connector transformations. State highest fidelity and limitations.

**“Files in a raw prefix are replayable.”** Without expected manifests, immutable versions, schemas, code/dependencies, identities, and tested publication, they may be incomplete or uninterpretable.

**“Object storage is immutable.”** Objects/versions can be overwritten, superseded, deleted, lifecycle-expired, or rendered unreadable by key/policy loss. Configure, record, and test controls.

**“Versioning is enough.”** A path without recorded version still resolves to mutable latest state. Lifecycle may remove versions. Bind receipts to explicit version/generation and digest.

**“Object Lock prevents every change.”** It protects specified versions under documented modes; new versions/delete markers and privileged/configuration behaviors still require analysis.

**“ETag is always MD5.”** Provider/multipart/encryption semantics vary. Use documented checksum fields and application digests with explicit scope.

**“Matching checksum proves completeness.”** It proves observed bytes matched, not that expected occurrences all arrived. Compare exact expected and landed sets.

**“Directory listing is a manifest.”** It lacks intended membership, source boundary, empty partitions, controls, and concurrency state. Manifests derive from expectations.

**“Keep decoded rows; original bytes add no value.”** Parser defects, unknown fields, invalid encodings, framing, signatures, and future readers may require original evidence.

**“Schema ID will always resolve.”** Registries have retention, migration, IAM, and disaster boundaries. Preserve immutable schema content/reference for the replay horizon.

**“Current reader schema reproduces old interpretation.”** Schema resolution/default/type behavior can change. Pin writer and original reader contracts for reproduction.

**“Checkpoint means raw is durable.”** It is a claim to verify. If $C>D_R$, crash/source expiry can lose history.

**“Write completed means generation published.”** Member objects can be durable while the expected set is incomplete. Publish only a validated immutable manifest.

**“Same code commit means same output.”** Floating dependencies, runtime, references, time, randomness, ordering, and target semantics can differ.

**“Replay and recompute are synonyms.”** Original contract reproduction and new corrected-contract computation need distinct identities/evidence.

**“Replay can reuse new event IDs.”** It defeats deduplication and duplicates effects. Preserve occurrence identity and create new run/output generation IDs separately.

**“Append corrected rows and let consumers choose latest.”** This mixes truth versions and pushes ambiguous precedence downstream. Publish a complete superseding generation.

**“Raw retention alone defines replay horizon.”** The shortest required schema/key/code/reference/identity/target horizon wins.

**“Encrypted old bytes are usable forever.”** Deleted/expired/unrestorable keys make them unreadable. Test key backup/rotation under policy.

**“Successful one-record replay proves recovery.”** Full manifests, gaps, transactions, scale, dependencies, output publication, security, and restore need exercises.

## Worked Examples

### Example 1

A vendor replaces `daily/orders.csv` at the same path after correction. The landing receipt records bucket/account, provider object version, size, application SHA-256 of received compressed bytes, source manifest ID, and capture time. Both versions remain immutable. The correction is a new source occurrence/generation linked to the superseded one; “latest path” never defines history.

### Example 2

A broker consumer writes offset 500 to raw and then crashes before acknowledging. Restart receives 500 again, queries `(cluster,topic,partition,offset)`, verifies the same payload/envelope digest, and returns the existing receipt. Only then does it acknowledge. If digest differs, it quarantines an identity/epoch conflict and does not overwrite raw.

### Example 3

An API returns JSON after server-side field projection and gzip transfer. The client library automatically decompresses. The team captures response bytes after decompression, request fingerprint, response headers, cursor/source snapshot, and explicitly records that compressed wire bytes are unavailable. Its raw claim begins at client body delivery; it does not pretend to preserve server database rows or TLS packets.

### Example 4

An Avro event references writer schema 37. Years later the registry has schema 52 only. Retaining payload bytes and integer ID 37 is insufficient. The landing manifest content-addresses schema 37 and records the reader/config used originally. Original replay uses those contracts; a new reader is a recomputation whose schema/default differences are compared before publication.

### Example 5

Expected file partitions are 0–15, including empty partition 9. Storage listing shows 15 files and all checksums pass. The manifest expects 16 receipts and detects missing partition 9; it cannot infer whether empty output or absent work occurred. A zero-row signed receipt for 9 completes exact membership and permits publication.

### Example 6

A CDC transaction spans positions 700–702 across three tables. Raw capture stores all row envelopes plus transaction ID, ordinals, expected count, commit boundary, source epoch, schemas, and position. It publishes the raw transaction manifest only when complete. A downstream replay applies the transaction atomically rather than expose two rows while the third is quarantined.

### Example 7

Transformation `v4` joins tax rates by current database lookup. Replaying 2024 raw in 2026 changes results because rates were corrected. The team snapshots/version-controls the reference table and rewrites the contract: reproduction uses the 2024 reference snapshot; deliberate restatement uses the corrected reference snapshot and publishes a superseding output generation.

### Example 8

Small raw records are compacted into Parquet. Original objects and their manifest remain until the derived file's membership, typed values, null/time semantics, row count, schema, codec, checksums, and replay behavior validate. The compaction manifest maps every source occurrence to file/row group. Only policy-approved cleanup later removes the original generation.

### Example 9

Raw ciphertext retention is seven years, manifests five, writer schemas three, decryption keys two, code artifacts four, reference snapshots one, identity receipts three, and target correction history two. The supported reproduction horizon is at most one year because the reference dependency expires first. Dashboards and policy must state one year, not seven.

### Example 10

A disaster exercise restores objects to another account but omits catalog pointers, schema artifacts, and key permissions. Checksums of copied ciphertext pass, yet replay fails. The team expands backup scope to manifests, receipts, schemas, catalog history, keys/policies, code artifacts, and runbooks, then repeats a full raw-to-output rebuild and measures recovery time.

## Cross-Program Connections

**Database Engineering.** WAL/log positions, MVCC snapshots, transactions, constraints, backups, isolation, and recovery define database-source cuts and raw receipt durability.

**Distributed Systems.** At-least-once delivery, idempotence, ambiguous commit, conditional writes, consensus metadata, ordering, epochs, replication, and retention shape capture/publication protocols.

**Storage Systems.** Object versions, checksums, erasure coding, WORM, lifecycle, tiering, compaction, catalogs, and restore behavior determine evidence durability and cost.

**Programming Languages.** Serialization, deterministic builds, dependency locking, numeric/time semantics, randomness, concurrency, and undefined/environment behavior affect reproduction.

**Security Engineering.** Source authenticity, least privilege, encryption/key recovery, hostile formats, tenant isolation, access audit, retention, deletion, and supply-chain integrity protect raw and replay.

**Platform Engineering.** Landing services, catalogs, schema registries, artifact stores, key management, observability, quotas, DR, and self-service replay environments operationalize the design.

**Data Architecture and Governance.** Ownership, lineage, authoritative boundaries, classification, legal purpose, retention, deletion, quality, and versioning define what raw may preserve and publish.

**Systems Engineering.** Hazard analysis treats source loss, silent gap, corruption, key/schema expiry, nondeterminism, and failed correction as end-to-end system risks rather than storage details.

## References

1. Amazon Web Services, [Checking Object Integrity for Data Uploads in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity-upload.html). Documents supported checksum algorithms/types, upload/download validation, multipart behavior, and ETag-related cases.
2. Amazon Web Services, [Locking Objects with S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html). Documents WORM behavior, versioning requirements, retention modes, legal holds, protected version scope, new versions, and delete markers.
3. Google Cloud, [Cloud Storage Request Preconditions](https://cloud.google.com/storage/docs/request-preconditions). Documents generation/metageneration conditions, conditional operations, race prevention, and failure responses.
4. Apache Avro, [Apache Avro 1.12.0 Specification](https://avro.apache.org/docs/1.12.0/specification/). Defines binary/container encoding, codecs, writer/reader schema resolution, parsing canonical form, and logical types.
5. Apache Parquet, [Parquet File Format](https://parquet.apache.org/docs/file-format/). Documents file layout, row groups, column chunks, file metadata, metadata length, magic values, and format components.
6. Apache Iceberg, [Iceberg Table Specification](https://iceberg.apache.org/spec/). Defines metadata files, atomic table-state replacement, snapshots, manifests, data-file membership, and optimistic concurrency requirements.
7. PostgreSQL Global Development Group, [Logical Decoding Concepts](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html). Documents logical slots, WAL retention, confirmed positions, crash behavior, and replay considerations for a database change source.
8. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Defines concepts and properties for representing and interchanging provenance about entities, activities, and agents.

## Exercises

### Exercise 1

A pipeline stores API responses as parsed JSON rows, records only request time, and acknowledges pages immediately. The API mutates records, returns expiring cursors, and sometimes omits unknown fields from the SDK model. Redesign the raw boundary, identity, source cut/pagination evidence, payload fidelity, receipt/acknowledgement order, manifest, schema/SDK metadata, and replay limitations.

### Exercise 2

Expected stream positions are 101–105. Landed receipts contain 101, 102, 104, 105, and an unexpected 106; all five payload checksums pass and the landed count equals the expected count. Determine whether the manifest can publish, what the exact set difference is, how checkpointing should behave, and why counts/checksums are insufficient.

### Exercise 3

Raw payload retention is 2,555 days, manifests 1,825 days, writer schemas 1,460 days, decryption keys 1,095 days, code/runtime artifacts 730 days, reference snapshots 365 days, identity/tombstone receipts 1,825 days, and target correction snapshots 1,460 days. Compute the maximum supported replay horizon. Propose two different remedies depending on whether seven-year exact reproduction or only two-year governed recomputation is required.

### Exercise 4

A transformation reads current exchange rates, current time, an unseeded random sampler, and unordered distributed input, then appends to an existing target. Identify every replay defect. Design a reproduction contract and a corrected recomputation/publication plan with stable source/effect identity, reference snapshots, deterministic order/randomness/time, and output comparison.

### Exercise 5

Design a disaster exercise for a raw platform using versioned object storage, immutable manifests, schema registry, encryption keys, code artifacts, quarantine, and an analytical target. Specify failures to inject, restored artifacts, integrity/completeness checks, replay steps, security boundaries, output verification, evidence, and criteria for claiming the documented recovery point/time objectives.

## Answers to the Exercises

### Answer 1

Define raw at the earliest body/envelope interface the client can actually observe. Preserve response bytes before SDK field projection if possible, selected request/response headers, content encoding, status, endpoint/query/tenant/security scope, server snapshot/version token, cursor/page request and response tokens, ordering, item/resource versions, and capture/landing times. Bind logical page/items to source snapshot/cursor and immutable payload digest; if stable item IDs/versions exist, record them separately from page delivery. Write immutable raw object version/generation, digest, size, schema/content type, SDK/library/config version, and landing receipt before advancing/acknowledging the cursor. Build an expected manifest from the API's documented pagination/cut contract, recording page/item IDs, counts, controls, and exclusions; directory listing is insufficient. If only parsed SDK objects are available, explicitly state that unknown fields and original bytes are irrecoverably lost and do not claim reparse fidelity. Retain cursors only as lineage if they expire; durable raw becomes the replay source after complete capture.

### Answer 2

No. Expected set is $E=\{101,102,103,104,105\}$ and landed set is $L=\{101,102,104,105,106\}$. $E-L=\{103\}$ is missing and $L-E=\{106\}$ is unexpected. Equal cardinality five hides replacement of one expected member by one extra; per-object checksum validates each observed payload but says nothing about membership. The manifest remains unpublished, 106 is contained/investigated under its source/epoch scope, and position 103 must be recovered. A contiguous checkpoint for this range cannot advance through 103 until authoritative raw contains the missing occurrence; depending on protocol it remains at 102 or an earlier already-published boundary, while 104–105 can remain durably staged but not claimed as a complete ordered range.

### Answer 3

The horizon is bounded by the minimum: 365 days from reference snapshots. Seven-year exact reproduction requires retaining every required component for at least 2,555 days, including manifests, schemas, keys with tested recovery, code/runtime dependencies, reference snapshots, identities/tombstones, and target correction/version evidence; it also needs policy authorization, migrations, scrubbing, and full replay exercises. If only two-year governed recomputation is required, preserve raw, manifests, schemas, keys, identities, code capable of the new contract, and an explicit two-year reference strategy for at least 730 days; original reference snapshots may still be absent, so label the result recomputation, not exact reproduction. Publish new output generations with recorded current/new reference snapshots and semantic delta validation. In either case, changing one payload TTL alone does not extend the horizon.

### Answer 4

Current exchange rates make an external mutable input; current time changes output; unseeded random selection changes membership; unordered input can change order-sensitive or floating aggregation; append repeats effects and mixes generations. For reproduction, pin the exact raw selection manifest and occurrence IDs, exchange-rate snapshot/digest, fixed logical evaluation time, random algorithm/seed (or materialized selection), deterministic total input/aggregation order and numeric rules, code/config/runtime/library versions, writer/reader schemas, and target schema/semantics. Write a fresh isolated generation with stable effect IDs, compare it with the original under declared byte/typed/domain equivalence, and publish conditionally only after controls. For a corrected contract, use a new transformation/version and reference snapshot, record the reason and expected deltas, preserve old output, publish a superseding generation atomically, and migrate downstream consumers. Never append replay rows into the old trusted table.

### Answer 5

Simulate loss of the primary account/region plus one corrupt object, one missing manifest member, unavailable schema, stale catalog pointer, denied key permission, and quarantined source unit. Restore explicit object versions and locked-generation metadata, manifests/receipts/catalog history, writer schemas, decryption keys/policies, code/runtime artifacts, reference snapshots, identity/tombstone registries, quarantine/history, configuration, IAM/network controls, and runbooks into an isolated tenant-safe environment. Verify object/version/size/digests, expected-versus-landed exact sets, transaction/order ranges, schema/key resolvability, manifest signatures/lineage, and least-privilege access; recover corruption/missing data from the approved replica or fail the exercise. Select a published raw manifest, reproduce with pinned bundle, use idempotent effect receipts, quarantine failures, validate typed key sets/counts/control totals and original output equivalence, then conditionally publish a test target generation and verify downstream lineage/access. Record start, boundary, every recovery action, checks, failures, output snapshot, and end time. Claim recovery point/time objectives only if the restored boundary meets the documented source position/time, the full usable output becomes available inside the time objective, security controls remain intact, and independent reconciliation passes—not merely because objects copied successfully.
