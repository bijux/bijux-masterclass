---
module_id: SARCH-045
program: Software Engineering: Software Architecture
level: 1
module_number: 45
title: Batch and File-Based Integration
status: complete
last_verified: 2026-09-06
---

# Batch and File-Based Integration

## One-Page Review

### Governing question

When should systems exchange bounded data sets as files or batches, and how should the architecture make completeness, identity, schema, integrity, reconciliation, restart, security, and time semantics explicit?

### Essential definitions

- A **batch** is a bounded set of work processed under one declared run or cutoff; a **file** is one transport artifact and need not equal one batch.
- A **snapshot** represents state for a declared scope and as-of point; a **delta** represents changes relative to a named predecessor or range.
- A **manifest** is control metadata describing an exchange: identity, producer, schema, parts, sizes, checksums, counts, ranges, and completion.
- A **part** is one immutable data artifact within a logical delivery; a **completion marker** states that the producer has finished publishing the declared set.
- A **cutoff** defines which source facts qualify; **watermark** states event-time progress under explicit lateness assumptions.
- **reconciliation** compares independent control totals, identities, and outcomes to detect loss, duplication, corruption, or semantic mismatch.
- **restartability** allows failed work to resume or repeat without corrupting the result.
- **quarantine** isolates an invalid artifact or record with evidence and ownership; it is unresolved work, not success.
- A **checksum** detects accidental change relative to supplied digest; authenticity additionally requires a trusted signature, MAC, or protected channel and key.
- **atomic publication** ensures consumers observe either no declared delivery or a complete immutable delivery, not a producer's intermediate writes.

### Central model, mechanism, or theorem

Model delivery $D=(id,schema,mode,scope,cutoff,parts,control)$, where every part $p_i$ has immutable name, byte length $b_i$, record count $n_i$, digest $h_i$, and key or time range. Producer publishes parts, then a manifest or completion marker referencing exactly those versions. Consumer validates control evidence before applying data and records delivery identity with its result.

For $N$ records averaging $r$ bytes, raw size is $S=Nr$. A transfer or scan at sustained rate $v$ has lower bound $T\ge S/v$ before parsing, validation, decompression, storage, contention, and retries. For window $W$, necessary average capacity is $S/W$; production headroom must cover variance and recovery.

### Critical invariants

- define batch identity, scope, cutoff, authority, snapshot or delta semantics, and expected outcome;
- keep data parts immutable and publish a manifest only after all referenced parts are durable;
- never infer completeness from silence, directory listing, filename order, or a fixed delay;
- validate schema, encoding, size, digest, count, ranges, uniqueness, and semantic control totals before commit;
- authenticate producer and consumer and protect artifact integrity, confidentiality, keys, and administrative operations;
- record source delivery identity, part identity, consumer run, code/schema version, and applied result separately;
- make import idempotent or stage into an isolated version before atomic cutover;
- define delta predecessor, sequence, overlap, gap, correction, late-arrival, and snapshot recovery policy;
- bound part size, parallelism, memory, disk, transfer, retries, quarantine, retention, and recovery rate;
- reconcile source, transfer, staging, target, reject, and published totals independently;
- test truncation, duplicate parts, missing parts, mutation, schema drift, clock boundaries, restart, rollback, and disaster recovery.

### Common failures

Common failures include treating a filename as a contract; reading a file while it is still being written; assuming successful transfer means complete business data; publishing mutable files; trusting checksums supplied over an unauthenticated path; using row count as the only reconciliation; applying a delta after a missing predecessor; loading directly into live tables; retrying non-idempotent inserts; dropping malformed records silently; using local time without zone or cutoff convention; putting secrets in filenames; retaining raw personal data indefinitely; and sizing only the happy-path window.

### Compact example

A nightly snapshot has 180 million rows averaging 240 bytes: $43.2$ GB raw. At sustained 200 MB/s, transfer or scan alone needs at least $216$ seconds. Compression may reduce bytes but adds CPU; validation, staging, indexes, and cutover add time. The producer publishes immutable parts, then a signed manifest with schema, as-of time, counts, byte sizes, digests, and control sums. The consumer stages by delivery ID, validates every part and total, then atomically switches the visible version.

### Connections

[SARCH-041](041-system-of-record-boundaries.md) defines authority; [SARCH-042](042-shared-database-versus-database-per-service.md) defines storage ownership; [SARCH-044](044-asynchronous-messaging-integration.md) provides streaming handoff and replay. [SARCH-046](../ROADMAP.md) next examines edge mediation. Data Engineering owns pipeline implementation; Data Architecture owns lineage and data contracts.

## Governing Question

Files remain one of the most durable integration mechanisms. They cross organizational, network, platform, and technology boundaries; support large sequential transfer; can be retained, inspected, signed, and replayed; and fit periodic settlement, catalog exchange, regulated submission, scientific acquisition, backup, and bulk migration.

Their danger is apparent simplicity. A file does not state whether it is complete, authoritative, current, unique, immutable, or safe to reprocess. Directory visibility can race with writing. Partial transfer can look valid. A syntactically valid row can carry the wrong currency or time convention. A successful job can omit rejected records. The architecture must provide a control protocol around the bytes.

## Why This Matters

Batch changes the unit of failure from one request or message to a set. A corrupt part can block millions of records. A missed daily delta can invalidate every later delta. A retry can duplicate an entire settlement. Slow processing can exceed the next cutoff and create overlapping runs.

Batch also offers useful boundaries. Immutable snapshots support reproducible reads. Manifests enable deterministic completeness checks. Staging makes validation possible before publication. Control totals expose silent loss that per-record acknowledgments may miss. An exchange can work while organizations are not simultaneously online.

The architectural goal is not to replace files with services reflexively. It is to make a file delivery behave like a well-specified protocol with authority, state, evidence, and recovery.

## Prerequisites and Retrieval

Retrieve file, record, byte, encoding, schema, snapshot, delta, transaction, immutable, identifier, checksum, signature, encryption, compression, partition, sequence, cutoff, time zone, watermark, staging, idempotency, reconciliation, atomicity, retention, lineage, backpressure, and recovery.

From SARCH-017 retrieve interoperability; SARCH-018 supplies evidence; SARCH-024 supplies runtime views; SARCH-041 supplies system-of-record boundaries; SARCH-042 supplies transaction placement; and SARCH-044 supplies delivery identity, duplicate handling, backlog, and replay reasoning.

## Learning Objectives

After completing this module, you should be able to:

1. choose file or batch integration from data-volume, latency, autonomy, and audit forces;
2. distinguish snapshots, deltas, parts, manifests, runs, and published versions;
3. design an atomic immutable publication protocol;
4. validate structural integrity, authenticity, and semantic completeness separately;
5. design restartable idempotent staging and atomic target publication;
6. specify cutoff, sequence, lateness, correction, and time-zone semantics;
7. reconcile counts, values, keys, rejects, and outcomes independently;
8. size transfer, storage, processing window, parallelism, and recovery headroom;
9. evolve schemas and formats across producers, consumers, retained history, and rollback;
10. secure and operate cross-boundary file exchange under failure.

## Core Exposition

**Choose batch for bounded-set forces.** Batch is appropriate when consumers need a complete periodic set, data volume rewards sequential transfer, organizations cannot remain online together, audit requires immutable submissions, or latency tolerates a window. A nightly settlement or monthly regulatory return is naturally a bounded artifact.

It is weak when each decision needs current authority, when one urgent item must wait behind a huge set, or when continuous updates and fine-grained outcomes matter. A file every second is often a message protocol with poor observability. A service call for billions of records is often a file transfer disguised as pagination.

**Define the logical delivery.** One delivery can contain many files, and one file can contain several logical groups. Assign immutable delivery ID, producer, authority, purpose, snapshot or delta mode, scope, cutoff, schema version, predecessor, creation time, expiry, and expected parts.

Do not overload filename parsing with the entire contract. Human-readable names help operations, but authoritative metadata belongs in a manifest and persisted control state. Object-store listing order, modification time, and directory presence are not reliable completion evidence.

**Distinguish snapshot and delta.** A snapshot states the complete representation of a declared scope as of a point. Replacement is simple, but large transfer and long production windows can make the “as of” meaning subtle. Is it one transactionally consistent view, a scan whose rows have different observation times, or an export from a replica?

A delta states changes since a named predecessor, source sequence, or half-open interval. It is smaller but creates chain dependency. Consumers must detect missing, duplicate, overlapping, and out-of-order intervals. Periodic snapshots bound recovery and allow the delta chain to restart.

**Define cutoffs mathematically.** Use an interval convention such as $[t_0,t_1)$ and one named time scale and zone. State whether qualification uses business-effective time, source commit time, ingestion time, or event time. Daylight-saving changes make “local midnight plus 24 hours” unsafe.

Late facts need policy: include in the next delta with original event time, issue a correction, reopen the period, or reject after finality. Watermarks are claims about observed progress under assumptions, not proof that no earlier event can arrive.

**Publish immutably and atomically.** A producer writes each part under a unique delivery version, closes and durably stores it, computes metadata, then publishes a manifest referencing exact immutable object versions. Consumers discover manifests, not arbitrary data objects.

On a filesystem with suitable same-filesystem rename semantics, write under a nonvisible name, synchronize as required, then rename. On object storage, use unique keys and publish a small completion manifest after parts; do not assume rename exists or that copying a large object is atomic. The exact storage guarantee must be verified for the chosen platform.

Never overwrite an accepted delivery in place. Corrections receive new identity and relationship to the superseded artifact. Immutability preserves audit, caching, retry, and forensic evidence.

**Use a manifest as the control plane.** Include format and schema identity, producer, delivery and predecessor IDs, purpose, scope, cutoff, parts in deterministic order, object versions, bytes, digests, record counts, key/time ranges, encoding, compression, encryption metadata, control totals, and signature information where required.

The manifest itself needs canonical representation or a precisely defined signature input. Avoid self-referential digest ambiguity. Version it independently from the data schema so control protocol can evolve.

**Separate integrity from authenticity.** A cryptographic digest detects changed bytes relative to the expected digest. If attacker can replace both file and digest, it proves nothing about origin. Protect the manifest through authenticated transport, a MAC, or a digital signature rooted in trusted key management.

CRC can detect common accidental errors but is not an authenticity mechanism. Encryption protects confidentiality under its threat model; authenticated encryption can also protect integrity, but key identity, rotation, replay, and metadata remain.

**Validate in layers.** First validate delivery and part identity, allowlist location, size, digest, and decompression limits. Then validate encoding, delimiter or container structure, schema, types, required fields, ranges, and uniqueness. Finally validate semantic constraints and control totals.

Defend against zip bombs, path traversal, formula injection, oversized fields, malformed Unicode, ambiguous quoting, and resource exhaustion. Parse untrusted input in a constrained environment. A familiar extension such as `.csv` does not make content safe.

**Stage before publication.** Load into an isolated delivery-scoped staging area. Record part and record progress so restart does not repeat committed work. Validate totals and domain rules before making the result visible. Publish by atomic pointer/version switch, metadata transaction, or another mechanism with explicit reader semantics.

Direct append into live tables makes partial failure visible. Deleting “today's rows” and retrying can erase concurrent corrections. Define target identity and replacement scope; make either per-record effects idempotent or the entire staged version disposable and repeatable.

**Reconcile independently.** Counts detect some omissions but not value changes, duplicates that replace omissions, or wrong units. Use several controls: total records, distinct keys, bytes, sums by currency, debit/credit balance, minimum/maximum sequence, category subtotals, reject counts, and expected scope.

The producer, transfer layer, staging layer, and published target should each report controls. Comparing values copied from one corrupted manifest is not independent evidence. Business owners must decide tolerance and terminal disposition.

**Treat rejects as first-class outcomes.** Record-level quarantine can preserve valid progress only if the business contract permits partial acceptance. Store delivery, part, record locator, safe error class, schema/code version, and redacted evidence. Never silently drop invalid rows.

Some batches are all-or-nothing: a financial settlement cannot publish while debits and credits disagree. Others allow bounded rejection with a correction file. State thresholds, ownership, notification, repair, replay, and final reconciliation.

**Design restart and duplicate handling.** A transfer can retry a part; an orchestrator can restart a run; an operator can resubmit a delivery. Persist stable identities and state transitions. Re-reading an immutable part should either reproduce staging or be recognized as complete.

Avoid using filename plus date as the sole key: partners resend corrected bytes under the same name. Bind identity to producer, declared delivery ID, semantic scope, and digest. Reject identity reuse with different content unless the correction protocol explicitly permits it.

**Plan capacity from the window.** Compute raw and compressed bytes, record count, file count, transfer, decompression, validation, transformation, storage, indexing, and publication work. Sustained throughput is lower than peak device or network rate. Concurrency may overload databases or create small-file overhead.

If a two-hour job normally uses 110 minutes, it has little recovery margin. Size for late arrival, retry, slower dependencies, and overlap with the next delivery. Apply admission and priority so a huge backfill cannot starve current required work.

**Choose part size deliberately.** Large parts improve sequential efficiency but increase retry cost and reduce parallelism. Tiny parts amplify listing, open, metadata, transaction, and scheduling overhead. Partition by stable processing and recovery units without embedding sensitive data in names.

Skew matters: equal record counts may not mean equal bytes or work. Record part statistics and rebalance future deliveries rather than mutating accepted artifacts.

**Evolve formats and semantics.** CSV needs explicit delimiter, quoting, header, newline, null, encoding, decimal, date, and escaping rules. Self-describing containers still need logical schema and semantic contracts. Compression and container versions are separate from record schema.

Additive fields may be safe for tolerant consumers; changing unit, timezone, identifier meaning, default, precision, or snapshot scope is semantic change. Producers must support mixed consumers, retained old files, replay, and rollback. Test new readers on old data and old supported readers on new data.

**Secure the full lifecycle.** Authenticate producer, transfer service, consumer, and operator. Authorize create, read, list, overwrite, delete, quarantine, replay, and key use separately. Use least privilege and unique delivery locations; prevent path or key injection.

Protect data in transit and at rest where required. Secrets and personal identifiers can leak through filenames, manifests, logs, temporary disk, backups, rejected rows, and support exports. Define retention, legal hold, deletion, residency, and disposal for every copy.

Signing keys need rotation, revocation, timestamp policy, algorithm agility, and audit. A valid signature proves control of a trusted key over exact bytes, not business truth or authorization for every consumer action.

**Observe the business exchange.** Track expected, arrived, validated, staged, rejected, published, acknowledged, reconciled, expired, and superseded deliveries. Measure age at each boundary, bytes, records, throughput, retries, part skew, checksum failures, schema failures, control differences, and storage pressure.

Alerts should distinguish “nothing expected” from “expected but absent.” Successful scheduling is not successful delivery. A green transfer dashboard can coexist with a missing business period or a target that never published.

**Test the failure matrix.** Interrupt during part creation, upload, manifest publication, download, decompression, staging, validation, target commit, acknowledgment, and cleanup. Repeat parts and deliveries. Remove, truncate, reorder, mutate, and corrupt them. Change schemas, encodings, time zones, and key versions.

Test disk full, quota, network retry, expired credentials, quarantine saturation, late delivery, overlapping runs, backfill contention, consumer rollback, restore, and resubmission after disaster. Verify source-to-target reconciliation and reader visibility, not just process exit codes.

**Define acknowledgment and deletion.** Consumer acknowledgment might mean received, validated, staged, published, or reconciled. Name it. The producer must not delete its only recoverable copy when the consumer merely downloaded bytes.

Retention and deletion depend on recovery, audit, privacy, and contractual evidence. Preserve manifests and reconciliation longer than raw data when lawful and sufficient. Test restore before treating retained artifacts as recoverable.

**Know the hybrid options.** A message can announce a manifest; the data remains in immutable object storage. A synchronous API can request an export and return an operation ID. A stream can produce hourly compacted snapshots. Batch control messages should carry references and identities rather than huge payloads.

The integration remains batch if correctness is defined over the bounded set. Combining transports does not remove the need for one authority, completeness protocol, and outcome model.

## Definitions and Notation

Let delivery $D$ contain identity $id_D$, producer $P$, schema $v$, mode $m\in\{snapshot,delta\}$, scope $S$, cutoff interval $I$, predecessor $pred(D)$ where applicable, ordered part set $F(D)$, and controls $C(D)$.

For part $f_i$, define immutable object version $o_i$, bytes $b_i$, records $n_i$, digest $h_i$, and key/time range $R_i$. Manifest completeness requires every declared exact object to exist and validate; existence of undeclared objects does not extend delivery.

Raw size estimate is $B=Nr$. With sustained rate $q$, lower-bound transfer or scan time is $T\ge B/q$. Necessary average window throughput is $q_{min}=B/W$. These omit fixed per-file cost, compression, parsing, validation, transforms, storage, contention, and retries.

Reconciliation vector can include $(N,N_{distinct},\sum amount,\sum debit,\sum credit,min(seq),max(seq),rejects)$ partitioned by relevant dimensions. Equality proves only those controls, not universal semantic equivalence.

## Mechanisms, Invariants, or Proof Structure

**Identity invariant.** Delivery, correction, part, producer run, consumer run, schema, source state, and published target version have distinct stable identities.

**Completeness argument.** A consumer that discovers arbitrary parts cannot distinguish a slow producer from a completed smaller delivery. A terminal manifest referencing immutable exact versions provides an explicit completion claim that can be validated.

**Publication invariant.** Referenced parts become immutable and durable before manifest visibility; target readers see either the prior accepted version or the new validated version.

**Integrity invariant.** Byte digest, authenticated origin, authorization, schema validity, and business correctness are separate checks.

**Delta invariant.** Every delta names predecessor or unambiguous interval/sequence, and the consumer detects gaps, duplicates, overlaps, late facts, and corrections before publication.

**Restart invariant.** Retrying any interrupted stage under the same identities cannot create additional visible business effect; incompatible identity reuse is rejected.

**Reconciliation invariant.** Source accepted, transferred, staged, rejected, published, and consumer-acknowledged controls balance under declared tolerances.

**Capacity invariant.** Bytes, records, parts, parallelism, disk, memory, transfer, processing window, retries, quarantine, retention, and backfill rate remain bounded.

**Security invariant.** Every artifact and operation retains authenticated producer, authorized purpose, integrity, confidentiality, provenance, retention, and key state.

**Evidence invariant.** Scheduler, transfer, validation, publication, acknowledgment, and business reconciliation are observed as different outcomes.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Full snapshot | simple replacement and bounded recovery | high volume and as-of ambiguity | complete periodic view is valuable |
| Delta chain | low transfer and focused change | gap, order, and long-chain recovery | change volume is small and sequencing strong |
| Snapshot plus deltas | bounded recovery with efficient updates | two protocols and cutover | sustained exchange needs reset points |
| One large file | sequential efficiency | retry cost and weak parallelism | size and window are modest |
| Partitioned parts | parallelism and localized retry | skew and metadata overhead | large sets need bounded work units |
| CSV/text | broad interoperability and inspectability | ambiguous types and escaping | contract specifies every textual convention |
| Typed columnar container | compact analytics and typed schema | tooling and version complexity | large analytical exchange dominates |
| Transactional staging | atomic visible result | extra storage and publication work | partial visibility is unacceptable |
| Per-record apply | early progress and localized rejection | partial state and idempotency burden | domain permits independent records |
| Message/stream | low-latency incremental processing | backlog and per-event complexity | bounded complete set is not required |
| Synchronous API | immediate authoritative response | temporal coupling and pagination | interactive bounded result is required |

## Failure Modes and Misconceptions

1. **“A file is a contract.”** Bytes need authority, schema, scope, and outcome semantics.
2. **“Visible means complete.”** Consumers can observe intermediate writes.
3. **“Transfer success means import success.”** Validation and business publication are later states.
4. **“Row count proves equality.”** Substitution and value corruption can preserve count.
5. **“Checksum proves origin.”** An attacker may replace both data and untrusted digest.
6. **“Encryption proves correctness.”** It protects confidentiality, not business truth.
7. **“Snapshots are consistent.”** Export observation semantics must be stated.
8. **“Deltas can be applied whenever they arrive.”** Missing or overlapping history can corrupt state.
9. **“Retrying a load is safe.”** Non-idempotent target effects can duplicate.
10. **“Rejecting bad rows is graceful.”** Partial acceptance may violate the batch invariant.
11. **“Timestamps define the business day.”** Zone, scale, cutoff, and lateness matter.
12. **“More files mean more speed.”** Per-file overhead and downstream contention can dominate.
13. **“Schema validation proves meaning.”** Units, authority, and scope may still be wrong.
14. **“A signed file is authorized truth.”** Signature scope and business authority differ.
15. **“No alert means no expected file.”** Absence detection requires an expectation model.
16. **“Batch is obsolete.”** It remains strong where bounded sets and audit dominate.

## Worked Examples

### Example 1

**Situation.** An export contains 180 million records averaging 240 bytes and a sustained transfer rate of 200 MB/s.

**Reasoning.** Raw size is $180{,}000{,}000\times240=43.2$ GB. The lower-bound transfer time is $43{,}200/200=216$ seconds using decimal units. Parsing, compression, validation, indexing, replication, and contention add time. Measure each stage and reserve retry headroom.

**Conclusion.** Raw byte arithmetic is a necessary lower bound, not a batch-window guarantee.

### Example 2

**Situation.** A producer uploads twelve parts, and a consumer starts after seeing the tenth.

**Reasoning.** Directory listing cannot distinguish incomplete publication from a ten-part delivery. Producer uses immutable delivery keys, uploads all twelve, verifies metadata, then publishes a manifest listing exact object versions. Consumer begins only from that manifest and rejects missing, additional, or mismatched declared parts.

**Conclusion.** A terminal manifest turns timing inference into a verifiable completeness claim.

### Example 3

**Situation.** A payroll file and its SHA-256 text file arrive through the same unauthenticated writable location.

**Reasoning.** An attacker can replace both. Protect a canonical manifest with a trusted signature or authenticated channel, validate signer authority and key state, then verify each part digest. Encryption is added for confidentiality, and replayed old delivery IDs are rejected.

**Conclusion.** Digest, authenticity, confidentiality, authorization, and freshness solve different problems.

### Example 4

**Situation.** Delta sequence 104 arrives after 102; 103 is absent.

**Reasoning.** Applying 104 could make deletes, balances, or versions wrong. Stage 104 but do not publish it. Request or recover 103, validate predecessor and overlapping key/time ranges, then apply in source order. If recovery fails, load a later authoritative snapshot and restart the chain.

**Conclusion.** Delta gaps are correctness failures, not merely late files.

### Example 5

**Situation.** A four-million-row settlement matches expected row count but debit and credit totals differ by €8,300.

**Reasoning.** Count alone misses value change or substitution. Compare distinct transaction IDs, sums by currency and legal entity, debit/credit balance, sequence range, duplicate and reject counts, and producer controls. Quarantine the entire settlement if its invariant requires balance; do not publish “mostly complete.”

**Conclusion.** Reconciliation must encode business invariants in addition to structural completeness.

### Example 6

**Situation.** A loader commits two of five parts, crashes, and restarts.

**Reasoning.** Direct live inserts could expose partial state and duplicate the first two parts. Load into delivery-scoped staging with part digest and status. Repeat or skip a part only after confirming its exact digest and transaction outcome. Validate the complete delivery, then atomically switch the target version. Failed staging is disposable.

**Conclusion.** Stable identities plus isolated staging make restart safe and reader visibility atomic.

### Example 7

**Situation.** Eight hundred 256 MB parts must finish within two hours.

**Reasoning.** Raw volume is $800\times256=204{,}800$ MB. Necessary average throughput is about $204{,}800/7{,}200=28.44$ MB/s. Planning for twice that rate gives about 56.89 MB/s before decompression, validation, storage, skew, and retry. Parallelism is capped by target capacity and tested with worst-size parts.

**Conclusion.** Window design combines byte rate, per-part overhead, downstream capacity, and recovery reserve.

### Example 8

**Situation.** A CSV producer changes empty fields from “missing” to numeric zero without a schema version change.

**Reasoning.** Both files parse, but meaning changes balances and completeness. The contract defines null token, empty-string meaning, decimal syntax, currency, timezone, header, encoding, and quoting. Semantic change receives a new version and coexistence plan; consumers test mixed deliveries and rollback.

**Conclusion.** Syntactic readability does not provide semantic compatibility.

### Example 9

**Situation.** Rejected medical rows are copied to a shared support bucket indefinitely.

**Reasoning.** Quarantine creates another sensitive data store. Store only necessary redacted evidence or encrypt tightly scoped records; authorize repair separately, audit access, set retention and deletion, prevent identifiers in object names, and reconcile repaired rows back to original delivery. Capacity limits stop quarantine exhaustion.

**Conclusion.** Reject handling must preserve privacy, provenance, capacity, and terminal ownership.

### Example 10

**Situation.** A wildfire resource snapshot is generated while roads close and crews move.

**Reasoning.** The manifest states authority, geographic scope, per-source observation time, export completion time, and consistency limitations. Consumers never interpret absence as current unavailability. Urgent closures travel through a lower-latency authoritative channel, while later deltas correct the snapshot. Field decisions record which version and local observations were used.

**Conclusion.** A complete file can still be stale or temporally mixed; high-consequence use needs freshness and override semantics.

## Cross-Program Connections

- **Data Engineering:** owns extraction, partitioning, formats, orchestration, incremental processing, and pipeline recovery in depth.
- **Data Architecture Engineering:** owns data contracts, authority, lineage, quality, retention, privacy, and consumer purpose.
- **Database Engineering:** owns consistent export, bulk load, staging transactions, indexes, logs, and target publication.
- **API and Service Engineering:** owns export-job APIs, operation status, partner contracts, and protocol error semantics.
- **Distributed Systems Engineering:** owns visibility, failure, replication, ordering, clocks, and atomicity limits.
- **Security Engineering:** owns signatures, key management, authenticated transfer, sandboxed parsing, access, and sensitive-data lifecycle.
- **Software Delivery and Reliability Engineering:** owns schedules, SLOs, capacity, alerts, incident response, restore, and reconciliation operations.
- **Platform Engineering:** provides governed object storage, transfer, schema, secrets, observability, quarantine, and replay facilities.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*, Addison-Wesley, 2003. <https://www.enterpriseintegrationpatterns.com/>
2. Leonard Richardson, Sam Ruby, and Mike Amundsen, *RESTful Web APIs*, O'Reilly Media, 2013.
3. Y. Shafranovich, *RFC 4180: Common Format and MIME Type for Comma-Separated Values (CSV) Files*, IETF, October 2005. <https://www.rfc-editor.org/rfc/rfc4180>
4. NIST, *FIPS PUB 180-4: Secure Hash Standard*, August 2015. <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>
5. Apache Software Foundation, *Apache Parquet Format Specification*. <https://github.com/apache/parquet-format>
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
7. Ralph Kimball and Margy Ross, *The Data Warehouse Toolkit*, 3rd ed., Wiley, 2013.
8. NIST, *SP 800-92: Guide to Computer Security Log Management*, September 2006. <https://csrc.nist.gov/pubs/sp/800/92/final>

## Exercises

### Exercise 1

Define batch, file, snapshot, delta, manifest, part, completion marker, cutoff, watermark, reconciliation, restartability, quarantine, checksum, authenticity, and atomic publication. Explain why one file need not equal one batch.

### Exercise 2

A delivery has 600 parts of 384 MB and a 90-minute window. Compute raw volume and necessary average throughput in MB/s. At measured sustained end-to-end throughput of 70 MB/s, compute ideal processing time and nominal margin. Explain why neither result proves the window.

### Exercise 3

Design an immutable snapshot-plus-delta exchange for customer account status. Include identities, manifest, snapshot consistency, delta predecessor, cutoff, late corrections, staging, idempotency, atomic publication, reconciliation, and recovery.

### Exercise 4

Compare CSV, a typed columnar format, synchronous pagination, asynchronous per-record messages, and partitioned snapshot files for exchanging 500 million analytical records with three partners. Address compatibility, throughput, audit, partial failure, privacy, and partner autonomy.

### Exercise 5

Design a cross-border disaster-relief supply exchange between intermittently connected agencies. Cover authority, part and delivery identities, signatures and encryption, key rotation, cutoff, units, duplicates, missing parts, corrections, quarantine, capacity, offline use, reconciliation, retention, and facts that a later file cannot undo.

## Answers to the Exercises

### Answer 1

A **batch** is bounded work under one run or cutoff; a **file** is one artifact, so a batch can have many parts and one file can contain multiple groups. A **snapshot** is state for scope and as-of point; a **delta** is change relative to a predecessor or range. A **manifest** describes delivery control metadata; a **part** is one immutable artifact; a **completion marker** declares publication complete. A **cutoff** selects facts; a **watermark** claims time progress under lateness assumptions. **Reconciliation** compares independent controls. **Restartability** permits safe resume or repeat. **Quarantine** isolates unresolved invalid input. A **checksum** detects change relative to a digest; **authenticity** requires trusted origin evidence. **Atomic publication** prevents intermediate delivery or target state from appearing complete.

### Answer 2

Raw volume is $600\times384=230{,}400$ MB. Ninety minutes is 5,400 seconds, so necessary average throughput is $230{,}400/5{,}400\approx42.67$ MB/s. At 70 MB/s, ideal time is $230{,}400/70\approx3{,}291.43$ seconds, about 54.86 minutes, leaving about 35.14 minutes. These calculations omit per-file overhead, compression CPU, parsing, schema and semantic validation, staging writes, indexing, replication, contention, skew, retries, publication, reconciliation, and late arrival. Sustained end-to-end failure and recovery tests must validate the window.

### Answer 3

Account authority assigns immutable delivery and part identities. A snapshot manifest states scope, source-consistency mechanism, as-of point, schema, exact object versions, bytes, digests, counts, key range, and status totals. Deltas name predecessor and half-open source commit sequence or interval. Producer publishes immutable parts before a protected terminal manifest. Consumer stages by delivery ID, validates authenticity, parts, schema, unique accounts, counts, and status subtotals, then atomically switches a version pointer. Reprocessing the same identities is idempotent; different bytes under one identity are rejected. Gaps stop delta publication, duplicates are recognized, and late facts appear as versioned corrections under original effective time. Periodic snapshots bound chain recovery, and source-to-target reconciliation plus retained manifests proves only declared controls.

### Answer 4

Synchronous pagination couples partners for a long transfer and makes consistent completion and restart difficult. Per-record messages suit continuous low-latency change but impose 500-million-message backlog, ordering, retention, and replay cost. Partitioned immutable files with a signed manifest fit the bounded analytical set and independent partner schedules. CSV maximizes basic tooling but requires exhaustive textual and type conventions and is bulky; a typed columnar format improves compression, projection, and schema fidelity but requires compatible readers and format governance. Offer governed format versions or produce both from one authoritative staged snapshot, reconcile them independently, partition into retryable units, and publish atomically. Partners stage and acknowledge named outcomes. Minimize partner-specific fields, encrypt and authorize separately, define retention and deletion, and test old/new reader combinations and partial transfer.

### Answer 5

Each agency retains authority for its inventory and commitments; the exchange does not convert an observation into allocation authority. A delivery has agency, jurisdiction, purpose, cutoff, schema, unit system, predecessor, and immutable part identities. A signed canonical manifest authenticates exact encrypted objects and key version; rotation accepts governed overlapping keys and rejects revoked or replayed identities. Counts, distinct supply IDs, quantities by item and unit, source sequence, and rejects reconcile. Missing or corrupt parts prevent complete publication; duplicates are idempotent; corrections supersede by new identity. Quarantine is encrypted, bounded, audited, and owned. Offline consumers display source, observation time, completeness, and local overrides and never infer current availability from absence. Admission and part sizing protect scarce links; retention follows recovery, legal, and privacy needs. Later files cannot undo supplies already issued, routes already taken, or treatment already delivered; they create new facts and reconciliation actions. Full credit requires unit conversion authority, human conflict resolution, and honest unknown state.
