---
module_id: DARCH-037
program: Data Architecture Engineering
level: 1
module_number: 37
title: Batch and File Exchange
status: complete
last_verified: 2026-09-03
---

# Batch and File Exchange

## One-Page Review

### Governing question

When is a bounded batch or file the most responsible way to exchange data, and how can producers and consumers prove completeness, integrity, atomic publication, semantic fitness, protection, recovery, correction, and retirement across schedules, storage, networks, and independently operated systems?

### Essential definitions

- A **batch** is a bounded set of work or data processed as one declared run, interval, population, or release rather than one interactive request at a time.
- A **file exchange** publishes one or more named objects and control records from a producer boundary to authorized consumers.
- A **snapshot** represents a population at a declared effective or extraction boundary; a **delta** represents changes since a declared prior boundary.
- A **manifest** is a control record listing expected files or parts, versions, sizes, counts, checksums, time boundaries, schema, and other evidence needed to validate a delivery.
- A **checksum** is a digest used to detect accidental or adversarial content changes under a declared algorithm and trust arrangement; it does not prove semantic correctness.
- **Atomic publication** prevents consumers from mistaking a partially written or incomplete file set for a complete release.
- A **ready marker** or committed manifest signals that all declared parts are durably available and validation can begin.
- An **arrival window** defines earliest, target, and latest delivery behavior using an explicit calendar, timezone, exception policy, and service objective.
- A **watermark** identifies the source-time boundary believed complete for the batch under declared lateness assumptions.
- A **rerun** repeats a planned interval or run; a **backfill** creates or corrects historical output for one or more prior intervals.
- **Quarantine** isolates invalid or suspicious input with evidence and access controls until correction or accountable disposition.
- **Consumer acknowledgement** records which declared delivery was received, validated, accepted, rejected, or applied under a named consumer contract.

### Central model, mechanism, or theorem

Represent a batch exchange as:

`B = (product, population, boundary, files, format, schema, manifest, transfer, publication, validation, service, protection, observability, ownership, correction, lifecycle)`

A file is a durable transport artifact, not a self-explaining contract. A trustworthy exchange names the represented population and time, publishes immutable versioned parts plus a committed manifest, verifies integrity and schema before exposure, records consumer acceptance, and preserves enough lineage to replay or correct the delivery. Batch remains valuable when coherent bulk state, offline processing, partner constraints, or cost efficiency matter more than per-record immediacy.

### Critical invariants

- Every batch identifies product, producer, consumers, purpose, population, keys, grain, time boundary, run identity, schema, version, and owner.
- Consumers never interpret an in-progress object or incomplete part set as committed output.
- The committed manifest unambiguously lists expected parts, sizes, counts, checksums, schema, boundaries, and prior dependency where applicable.
- Checksums, counts, and structural validation establish bounded integrity evidence but never stand in for semantic, quality, or authorization review.
- Snapshot, delta, correction, deletion, late-arrival, and backfill behavior preserve a reconstructable history or explicitly disclose limitations.
- Transfers, storage, compression, encryption, keys, temporary files, quarantine, logs, and backups obey purpose, access, residency, retention, records, deletion, and incident requirements.
- Reruns are idempotent or versioned, and consumers can distinguish identical retry, replacement, correction, and new business-effective data.
- Expected-arrival, freshness, completeness, validation, application, recovery, correction, and acknowledgement are observable at producer and consumer boundaries.
- Capacity planning covers source extraction, sorting, serialization, compression, encryption, network, storage, validation, loading, overlap, and recovery.
- Retirement closes schedules, accounts, keys, network rules, buckets, directories, files, manifests, copies, schemas, alerts, contracts, and support after verified consumer migration.

### Common failures

Common failures are treating CSV as self-describing; overwriting a file in place; using file modification time as business time; omitting stable run and part IDs; assuming row count proves completeness; publishing checksums through the same untrusted path without authentication; declaring success when upload finishes; using local calendars and daylight-saving behavior implicitly; letting partial files match production names; applying a delta without its predecessor; silently replacing corrected history; retrying loads that duplicate effects; keeping plaintext staging copies after encrypted transfer; quarantining protected files indefinitely; and stopping a schedule while credentials, copies, alerts, and partner obligations remain.

### Compact example

A producer publishes a daily Account snapshot as four immutable Parquet parts under a run ID. A manifest declares product and schema versions, UTC extraction boundary, source watermark, each object name, byte size, record count, SHA-256 digest, aggregate count, classification, and predecessor. Parts land under a staging prefix; the signed manifest is committed last. A consumer verifies identity, manifest, parts, checksums, schema, population rules, and counts before atomically exposing the new version and acknowledging it. A correction creates a new run rather than mutating yesterday's files.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md) supplies temporal modeling, [DARCH-019](019-model-versioning.md) governs change, and [DARCH-027](027-producer-and-consumer-contracts.md) defines obligations. [DARCH-034](034-api-led-data-access.md), [DARCH-035](035-event-driven-data-integration.md), and [DARCH-036](036-change-data-capture-architecture.md) provide interactive and incremental alternatives; this module prepares [DARCH-040](../ROADMAP.md) on integration-style choice.

## Governing Question

Files are sometimes dismissed as legacy integration, yet they remain efficient, portable, inspectable, and operationally decoupled for large populations and external exchanges. Their apparent simplicity hides coordination: a consumer must know when a release is complete, what it represents, how to validate it, and what to do when it is late or wrong.

The governing question is not “Can we send a file?” It is “Does a bounded release fit the consumer's time and workload, and can the organization govern its semantic boundary, atomicity, evidence, protection, correction, and full lifecycle?”

## Why This Matters

An API requiring a million paginated requests can be worse than one governed snapshot. An event stream can burden a consumer that only needs a daily population. Partners and regulators often require portable signed artifacts. Batch trades immediacy for coherent boundaries and efficient bulk processing.

[RFC 4180](https://www.rfc-editor.org/rfc/rfc4180) documents a common CSV format and MIME type, while the [Apache Parquet file-format documentation](https://parquet.apache.org/docs/file-format/) describes a column-oriented file structure. Formats solve encoding and layout concerns; they do not define business keys, grain, time, completeness, or authorization.

NIST [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final) specifies secure hash algorithms, and [RFC 4253](https://www.rfc-editor.org/rfc/rfc4253) specifies the SSH transport layer. A checksum can detect content differences and an encrypted channel can protect transfer, but neither proves source authenticity, semantic correctness, or safe downstream use by itself.

The W3C [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) covers formats, identifiers, metadata, access, versioning, provenance, quality, preservation, and reuse. W3C [PROV-O](https://www.w3.org/TR/prov-o/) supplies derivation concepts. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) informs bounded retries and recovery, while NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames protection across the system lifecycle.

## Prerequisites and Retrieval

You should understand data products, keys and grain, time, schemas, encodings, filesystems and object storage, checksums, encryption, batch processing, transactions, quality, lineage, provenance, service objectives, privacy, records, and lifecycle.

Retrieve batch, run, snapshot, delta, extract, partition, part, file, object, prefix, manifest, checksum, digest, signature, compression, encryption, staging, atomic rename, ready marker, watermark, arrival window, calendar, timezone, validation, acknowledgement, rerun, backfill, correction, quarantine, and retirement.

As a retrieval test, inspect “Customers.csv arrives nightly.” Ask which customer product, population, keys, grain, fields, schema, format dialect, character encoding, business and extraction time, timezone, schedule, run ID, parts, manifest, checksum, encryption, purpose, retention, validation, acknowledgement, correction, owner, and late behavior apply. The filename and cadence are not a contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish snapshots, deltas, append batches, correction releases, extracts, archives, and control files;
2. model batch products through population, time boundary, parts, format, schema, manifest, publication, validation, service, protection, ownership, and lifecycle;
3. design immutable names, run and part identities, staging, ready markers, committed manifests, and consumer activation;
4. use counts, sizes, checksums, signatures, schemas, and quality rules as bounded evidence with explicit limitations;
5. specify CSV, columnar, record-oriented, compression, character, null, decimal, timestamp, and partition conventions;
6. define snapshot, delta, watermark, deletion, late-data, rerun, backfill, restatement, and predecessor behavior;
7. engineer schedules, calendars, arrival windows, retries, idempotency, capacity, isolation, recovery, and acknowledgement;
8. protect transfer, storage, staging, keys, metadata, logs, quarantine, backups, and downstream copies;
9. observe producer extraction through consumer application and diagnose partial, late, corrupt, incompatible, or semantically wrong releases;
10. choose batch, API, event, CDC, replication, federation, or analytical serving from workload and semantic evidence.

## Core Exposition

**Begin with consumer need.** Identify purpose, population, assertions, history, volume, acceptable freshness, consistency, latency, protection, and lifetime. A daily snapshot and hourly delta solve different problems.

Do not choose a file merely because the source can export one. Confirm that bounded processing and delivery align with downstream decisions and recovery.

**Define the product.** Name the source-aligned, aggregate, or consumer-aligned product represented. Assign meaning, quality, service, correction, and lifecycle ownership.

A transfer team owns reliable movement, not the truth of Customer or Account. File storage does not become source authority merely because consumers read it.

**Define the population.** State inclusion and exclusion rules, filters, security scope, late records, deleted records, test data, and unknown values. A record count without a population definition is weak evidence.

Preserve population version and effective interval. If eligibility changes, publish impact and whether history is restated.

**Define keys and grain.** State what one record represents and which fields identify it. Composite, mutable, surrogate, and reused keys need explicit handling.

For multi-file products, ensure keys cannot appear unexpectedly across parts unless deduplication semantics permit it. Publish partition rules and changes.

**Define time boundaries.** Distinguish business-effective time, source observation, extraction start and end, source watermark, publication, availability, consumer validation, and application time.

“2026-09-03 file” is ambiguous without timezone and boundary. It may represent business date, UTC interval, local calendar, or publication date.

**Choose snapshot or delta.** A snapshot represents full state at a boundary and simplifies independent load. It increases transfer and can obscure intermediate changes.

A delta reduces volume and preserves changes but depends on a predecessor, ordered application, delete semantics, and gap-free boundaries. State which prior run it requires.

**Design snapshot consistency.** An extract spanning hours can contain mixed-time rows if the source changes during the scan. Use source snapshot isolation, versioned source copies, or an explicit mixed-time limitation plus reconciliation.

Record snapshot identifier, isolation, boundary, source position, extraction duration, and changes during extraction. Row counts cannot establish a single-time view.

**Design delta boundaries.** Define half-open or closed intervals precisely, using source positions or stable time plus tie-breakers. Overlap with deduplication may be safer than an unobserved gap.

Late-arriving source data complicates event-time boundaries. Use watermarks and correction batches. Never assume publication time equals business-effective time.

**Name runs immutably.** Each publication needs a stable unique run or release ID unrelated to a mutable filename such as `latest.csv`. Include product and contract version and meaningful time metadata separately.

Consumers should record the run ID they applied. A convenience pointer can identify the latest committed run but must not overwrite immutable history silently.

**Name parts deterministically.** Partition by a declared key range, date, region, hash, or workload unit. Include part identity and expected total or manifest membership.

Lexical filename order may not equal semantic order. Avoid relying on directory listing completeness or eventual discovery. The manifest is the authority for the file set.

**Choose format from workload.** CSV is widely interoperable and human-viewable but has dialect, quoting, escaping, header, type, null, newline, and encoding ambiguity.

Columnar formats support typed analytical scans, projection, compression, and statistics, while adding library compatibility and metadata concerns. Record exact format and version rather than file extension alone.

**Specify CSV completely.** Define character encoding, delimiter, quote, escape, header, line ending, embedded newlines, null token, empty string, decimal separator, thousands separator, dates, timestamps, booleans, and invalid records.

RFC 4180 documents common conventions but does not cover every dialect. Include adversarial examples: quotes, delimiters, newlines, Unicode, null, empty, and leading formula characters.

**Specify typed formats.** Declare logical and physical types, precision, scale, timestamp timezone and unit, nullability, nested structures, dictionary behavior, schema metadata, compression, writer version, and supported reader range.

Do not infer business units or authority from physical types. A 64-bit integer still needs meaning, and a timestamp needs its time concept.

**Choose compression deliberately.** Compression reduces storage and network but consumes CPU, affects splittability, changes corruption scope, and introduces library compatibility.

Record algorithm and version, validate decompression before load, and plan worst-case expansion. A small compressed input can expand beyond consumer storage limits.

**Design the manifest.** Include product, producer, run, contract and schema versions, population and time boundary, source watermark, predecessor, part names, sizes, counts, checksums, format, compression, classification, publication time, and contact.

The manifest can also include aggregate counts, quality evidence, signature, encryption key reference, and expiry. Version its schema. Keep it machine-readable and independently documented.

**Use checksums within a trust model.** A digest detects whether bytes differ from the expected digest. If attacker and digest share one untrusted path, both can be replaced.

Authenticate the manifest or delivery channel through signatures, protected metadata, or trusted transport. State algorithm and exact byte scope: compressed, encrypted, or plaintext.

**Separate integrity from semantics.** Matching SHA-256 shows the consumer received the bytes named by the manifest. It does not prove those bytes contain all intended customers, correct balances, or authorized fields.

Layer validation: identity, manifest, parts, sizes, digests, format, schema, structural rules, population, referential rules, quality, business reconciliation, and consumer fitness.

**Publish atomically.** Write to a staging name or prefix, verify producer-side artifacts, and expose a committed manifest or ready marker only after every immutable part is durable.

Filesystems may support atomic rename within one volume; object stores have different semantics. Design for the actual platform. Consumers must ignore uncommitted staging artifacts.

**Do not overwrite in place.** A reader can observe partial content or retain cached prior content. Publish a new immutable version and change a small pointer or manifest atomically where supported.

Corrections should produce a new run that references the superseded run. Preserve history under retention and records policies.

**Design transfer.** Choose managed file transfer, object storage, SFTP, shared filesystem, physical media, or provider exchange from size, frequency, trust boundaries, networking, identity, reliability, and partner capability.

Define authentication, authorization, encryption, host verification, network restrictions, retries, resume, multipart behavior, timeouts, acknowledgement, and support. A secure transport does not authorize downstream use.

**Protect data at rest and in transit.** Apply approved encryption, key ownership, rotation, separation of duties, region constraints, least privilege, access logging, and incident response.

Avoid shared partner accounts and permanent keys. Use workload identity or bounded credentials where possible. Test expired and rotated keys before critical runs.

**Minimize fields and metadata.** Include only assertions required for declared consumer purposes. Filenames, directory paths, manifests, counts, logs, and notifications can reveal protected subjects or business activity.

Classify control files as well as payloads. Use opaque IDs when names would disclose data. Separate metadata discovery from payload authorization.

**Define schedule and calendar.** State timezone, business calendar, weekends, holidays, daylight-saving transitions, maintenance, earliest availability, target, latest acceptable arrival, and exceptional runs.

Use UTC instants for system coordination while preserving relevant business dates. Test missing and repeated local clock hours. “Nightly” is not an objective.

**Define expected-arrival monitoring.** Detect missing deliveries, not only failed jobs. The last successful file can remain readable and make dashboards silently stale.

Monitor run creation, expected manifest, part completion, transfer, consumer retrieval, validation, application, acknowledgement, and data age. Alert from consumer consequence.

**Define consumer acknowledgement.** Distinguish received, integrity-checked, schema-valid, quality-valid, applied, and accepted. One status must not collapse these boundaries.

Record consumer, run ID, contract version, time, result, counts, errors, and owner. A producer upload is not end-to-end success.

**Make loads idempotent.** A rerun of the same immutable run should not duplicate rows or effects. Consumers can stage by run ID, validate, then atomically replace or merge under declared keys.

Append-only effects need deduplication or business idempotency. Upserts do not protect repeated notifications, increments, or external actions.

**Differentiate retry, rerun, replacement, and correction.** A transfer retry carries identical bytes and run ID. A rerun may reproduce an interval with new execution evidence. A replacement supersedes a broken artifact. A correction changes asserted data.

Assign distinct identities and links. Consumers need policy for which version is authoritative and whether prior decisions must be restated.

**Handle partial transfer.** Multipart upload, interrupted SFTP, disk exhaustion, and network failure can leave objects that appear named correctly. Use staging, size and checksum validation, immutable completion, and committed manifests.

Never infer completeness from file existence or age. Quarantine partial or mismatched artifacts and prevent downstream activation.

**Handle duplicate and missing parts.** Validate manifest uniqueness, exact membership, part numbering or partitions, and aggregate counts. Extra unexpected files may indicate stale output or disclosure.

Reject or isolate ambiguous sets. Do not simply load every matching wildcard. Preserve evidence for correction and incident review.

**Handle schema mismatch.** Validate before loading into production. Route incompatible runs to quarantine with schema, error, owner, retryability, retention, and notification.

Avoid auto-coercion that hides lost precision, invalid dates, truncated strings, or changed nulls. Compatibility requires semantics and consumer behavior, not only parsing.

**Handle quality failures.** Define blocking, warning, and informational checks based on consequence. Record thresholds, populations, versions, evidence, and owner.

A rejected batch creates a service incident if consumers miss their window. Provide correction, degraded use, prior-snapshot fallback, and communication paths.

**Bound quarantine.** Quarantine is protected temporary state with owner, purpose, access, encryption, location, retention, review, correction, deletion, and closure.

It must not become an indefinite shadow archive. Minimize payload copies; store protected references where sufficient. Monitor age and unresolved volume.

**Plan capacity end to end.** Include extraction reads, sorts, joins, serialization, compression, encryption, hashing, staging, transfer, storage, validation, decompression, parsing, loading, indexes, and downstream computation.

Model bytes and record distributions, peak overlap, reruns, backfills, retries, source contention, network windows, and consumer concurrency. Average daily size hides month-end peaks.

**Use partitioning to bound recovery.** Smaller parts can retry and validate independently and increase parallelism. Too many small files increase metadata, listing, open, scheduling, and bookkeeping cost.

Choose target sizes from storage and query engines, network, encryption, checksums, and consumer capacity. Manifest all parts regardless of partition strategy.

**Bound retries.** Use backoff, jitter, attempt limits, resumable transfer, concurrency controls, and budgets. A partner outage should not trigger thousands of simultaneous full-file uploads.

Preserve the same run and digest for identical retry. Escalate persistent failure and avoid overwriting evidence. Test recovery after partial success.

**Plan backfills.** Specify intervals, product and schema versions, source reconstruction, run identities, partitioning, capacity, priority, protection, consumer mode, validation, and rollback.

Historical sources may reflect corrected semantics or missing fields. Label limitations. Isolate backfill workloads so live schedules continue.

**Design correction.** Identify affected run, parts, keys, fields, time, population, consumers, cause, and corrected release. Consumers restate state and downstream decisions according to contract.

Do not silently edit an existing file. Preserve original evidence if records, audit, or completed decisions require it, while preventing accidental continued use.

**Maintain lineage and provenance.** Relate each file and record population to source products, queries, snapshots, transformations, executions, agents, schema, code, and prior runs.

Provenance supports reproduction and correction but does not prove quality. Store it at useful granularity without leaking protected data or creating unbounded metadata.

**Govern retention and deletion.** Set retention for staging, committed runs, manifests, checkpoints, quarantine, logs, backups, consumer copies, and derived data by purpose and records needs.

Deletion can conflict with reproducibility and holds. Record accountable resolution. Expiring producer objects does not delete downloaded partner or consumer copies.

**Design observability.** Track expected and actual runs, extraction and watermark, parts, bytes, counts, checksums, schemas, transfer, validation, load, acknowledgement, freshness, quality, retries, quarantine, cost, and correction.

Protect telemetry. Monitor missing observations. Correlate by product, run, part, consumer, and version so incident scope is reconstructable.

**Assign ownership.** Producers own source assertions and publication. Transfer platforms own movement capability. Consumers own validation for use and downstream effects. Security, privacy, records, and operations own their controls and response.

Name one incident coordinator and explicit handoffs. Partner contracts need support windows, escalation, correction, and termination terms.

**Choose batch without apology.** Batch is appropriate for coherent bulk state, low-frequency needs, offline operation, constrained partners, archival evidence, or cost-efficient analytical loading.

It is inappropriate when individual facts must trigger prompt action, interactive queries need variable selection, or a consumer cannot safely wait for a full interval.

**Combine patterns.** An API can initiate an export or retrieve its manifest. An event can notify that a batch committed. CDC can generate deltas. A snapshot can bootstrap an event consumer.

Define cross-pattern identity, time, authority, correction, and race behavior. Combining mechanisms does not remove their individual obligations.

**Plan migration.** Inventory file jobs, directories, accounts, fields, formats, schedules, consumers, reports, manual steps, retention, failures, and unknown use. Establish immutable runs, manifests, contracts, and telemetry before changing transport.

Migrate consumer cohorts with parallel semantic and operational validation. Compare populations, keys, values, nulls, time, counts, integrity, quality, protection, performance, and decisions. Preserve rollback.

**Retire completely.** Stop schedules and transfer jobs; revoke accounts, keys, and network rules; remove staging, directories, buckets, files, manifests, schemas, alerts, dashboards, scripts, provider resources, and manual procedures.

Update catalogs and lineage. Preserve required records, provenance, holds, and correction. Verify consumers and post-shutdown absence before closing support.

**Measure value.** Track on-time accepted runs, end-to-end freshness, integrity failures, schema and quality rejects, reruns, backfills, recovery, quarantine age, consumer effort, protection exceptions, cost, and retirement closure.

Number of files and transferred bytes are workload measures, not value. The outcome is a complete, intelligible, protected, and recoverable product at the consumer boundary.

## Definitions and Notation

Represent batch product $B=(P,U,T,F,S,M,X,A,Q,Z,O,C,L)$, where $P$ is product and population, $U$ run identity and predecessor, $T$ temporal boundary and watermark, $F$ file parts and format, $S$ schema, $M$ manifest and integrity evidence, $X$ transfer and publication, $A$ acknowledgement and application, $Q$ service and quality, $Z$ protection, $O$ observability and ownership, $C$ correction and recovery, and $L$ lifecycle.

For manifest expected part multiset $E$ and observed part multiset $O$, completeness requires exact identity and multiplicity equality after authorized resolution: $E=O$. Set equality alone can hide duplicate part names; counts alone can hide substitutions.

For parts $i=1,\ldots,n$, aggregate declared records are $R=\sum_i r_i$ and bytes $Y=\sum_i y_i$. These totals are reconciliation evidence only. They do not prove uniqueness, population completeness, field correctness, or authorization.

Let end-to-end freshness at consumer activation be $F_a=t_{activate}-t_{boundary}$ under declared clocks and time meanings. Transfer duration is only one component and cannot substitute for source-boundary age.

Define `JustifiedBatch(B,t)` as a review predicate requiring a bounded bulk need, explicit population and time, atomic immutable publication, complete manifest, suitable validation, achievable service, effective protection, recoverable consumers, accountable correction, compared alternatives, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material batch exchange.

**1. Product gate.** Define producer, consumers, purpose, assertions, population, keys, grain, time, quality, owner, limitations, and alternatives.

**2. Format gate.** Specify file and format versions, encoding, types, nulls, units, timestamps, compression, parts, names, examples, and reader compatibility.

**3. Manifest gate.** Declare run, predecessor, schema, boundary, watermark, expected unique parts, sizes, counts, checksums, aggregate evidence, classification, and contacts.

**4. Publication gate.** Enforce staging, immutable writes, producer validation, committed manifest or marker, atomic exposure, retry identity, and supersession.

**5. Transfer gate.** Govern authentication, authorization, encryption, keys, host and network trust, resume, multipart behavior, timeouts, retries, acknowledgement, and providers.

**6. Consumer gate.** Validate identity, membership, integrity, schema, structure, population, quality, idempotency, application, degraded behavior, correction, and acceptance.

**7. Service gate.** Define calendar, arrival window, freshness, capacity, isolation, missing detection, recovery, backfill, support, incident communication, and evidence.

**8. Protection gate.** Apply purpose, minimization, classification, metadata protection, staging, quarantine, copies, residency, retention, deletion, records, audit, and incidents.

**9. Evolution gate.** Govern schema, format, population, partitioning, semantics, versions, fixtures, parallel runs, consumer migration, rollback, correction, and deprecation.

**10. Lifecycle gate.** Discover, publish, transfer, validate, apply, acknowledge, correct, rerun, backfill, migrate, revoke, remove, archive, retire, and verify closure.

The executable example compares expected manifest parts with observed objects, preserving duplicate evidence.

<!-- bijux-verify: {"id":"batch-manifest-membership-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"expected_parts=5\nobserved_objects=5\nunique_observed_parts=4\nmissing_parts=part-003\nunexpected_parts=none\nduplicate_parts=part-002\nmanifest_complete=false\n","stderr":""}} -->
```python
from collections import Counter

expected = [f"part-{number:03d}" for number in range(1, 6)]
observed = ["part-001", "part-002", "part-002", "part-004", "part-005"]

expected_counts = Counter(expected)
observed_counts = Counter(observed)
missing = sorted(expected_counts.keys() - observed_counts.keys())
unexpected = sorted(observed_counts.keys() - expected_counts.keys())
duplicates = sorted(part for part, count in observed_counts.items() if count > 1)
complete = expected_counts == observed_counts

print(f"expected_parts={len(expected)}")
print(f"observed_objects={len(observed)}")
print(f"unique_observed_parts={len(observed_counts)}")
print(f"missing_parts={','.join(missing) or 'none'}")
print(f"unexpected_parts={','.join(unexpected) or 'none'}")
print(f"duplicate_parts={','.join(duplicates) or 'none'}")
print(f"manifest_complete={str(complete).lower()}")
```

The example proves only that the observed multiset repeats `part-002`, omits `part-003`, and therefore differs from the expected five-part manifest. It does not verify object identity, bytes, checksum, schema, record population, semantics, authorization, atomic publication, or consumer application. Production acceptance needs authenticated manifests, integrity checks, contract validation, quality evidence, and accountable acknowledgement.

## Alternatives and Trade-Offs

**Batch versus API.** Batch moves coherent bulk populations efficiently; APIs support selective interactive access. Crawling an API can be expensive and inconsistent, while files add schedule and storage latency.

**Batch versus events.** Batch simplifies bounded processing and complete snapshots. Events reduce reaction time and preserve changes but add ordered state, duplicates, lag, and replay.

**Snapshot versus delta.** Snapshots are independently loadable but large. Deltas are efficient but depend on predecessors, deletes, ordering, and gap-free boundaries.

**CSV versus typed columnar format.** CSV maximizes basic interoperability but leaves types and dialect ambiguous. Columnar formats improve analytical performance and typing while requiring compatible libraries and metadata governance.

**One large file versus many parts.** One file simplifies discovery and counts but limits parallelism and recovery. Many parts scale better while increasing metadata and completeness risks.

**Filesystem rename versus object-manifest commit.** Atomic rename can expose completed files on one filesystem. Object platforms often favor immutable parts plus a committed manifest; semantics must match the platform.

**Checksum versus digital signature.** A checksum detects byte differences against an expected value. A signature can authenticate origin and integrity under key trust, while adding key and verification lifecycle.

**Overwrite versus immutable correction.** Overwrite minimizes visible versions but destroys evidence and risks partial reads. Immutable superseding runs support audit and rollback with retention cost.

**Long retention versus reproducible regeneration.** Retention speeds replay and supports evidence but increases storage and exposure. Regeneration saves storage only if sources, code, schemas, and semantics remain reproducible.

**Shared transfer platform versus domain-owned exchange.** A platform reuses secure transport and telemetry. Domains retain product meaning and consumer contracts; central transport must not absorb semantic accountability.

## Failure Modes and Misconceptions

1. **Files are inherently legacy.** They remain appropriate for bounded bulk and offline exchange.
2. **CSV is self-describing.** Dialect, types, nulls, encoding, and semantics remain.
3. **A filename defines time.** Business, extraction, publication, and availability time differ.
4. **File existence means completion.** Partial writes and incomplete sets can exist.
5. **Directory listings are manifests.** They do not declare expected membership or semantics.
6. **Equal part counts prove completeness.** Duplicates can replace missing parts.
7. **A matching checksum proves correct data.** It proves bytes match one declared digest.
8. **Encrypted transfer authorizes use.** Purpose and downstream controls remain.
9. **Upload success means delivery success.** Consumer validation and application may fail.
10. **Offset dates are obvious.** Calendars, timezones, and daylight-saving transitions matter.
11. **Rerunning is always idempotent.** Append effects and changed bytes can duplicate or restate.
12. **A delta can be loaded independently.** It depends on predecessor and boundary semantics.
13. **Quarantine is safe permanent storage.** It needs protection, owner, retention, and closure.
14. **Compression only reduces cost.** CPU, memory, expansion, splittability, and corruption change.
15. **Prior snapshot is always a safe fallback.** Its freshness and semantics may be unacceptable.
16. **Changing an optional column is harmless.** Parsers, meaning, protection, and size can break.
17. **Stopping the schedule retires exchange.** Accounts, files, copies, alerts, contracts, and duties remain.

## Worked Examples

### Example 1

A daily directory contains five objects, but `part-002` appears twice and `part-003` is absent. Object count equals the manifest count. Multiset comparison rejects it. **Conclusion:** counts and set membership must preserve multiplicity and identity.

### Example 2

A producer overwrites `customers.csv` while a consumer reads it. The consumer receives half old and half new bytes. Immutable run paths plus a committed manifest published last prevent partial activation. **Conclusion:** naming and commit protocol provide atomic publication, not file extension.

### Example 3

A CSV field contains an embedded newline and an empty value. One parser splits a record; another treats empty as null. A declared RFC-style dialect, UTF-8 encoding, quoted examples, and explicit null token remove ambiguity. **Conclusion:** portable text still requires a complete format contract.

### Example 4

A SHA-256 digest matches every downloaded part, but the producer omitted all customers from one region. Population reconciliation rejects the run despite byte integrity. **Conclusion:** cryptographic integrity and semantic completeness are distinct evidence layers.

### Example 5

A local 02:30 schedule runs twice when daylight-saving time repeats. Two outputs share one business date and overwrite each other. UTC run instants, unique run IDs, explicit business date, and calendar rules preserve both identities. **Conclusion:** schedule time must be modeled, not inferred from filenames.

### Example 6

An hourly delta for interval `[10:00,11:00)` arrives before its predecessor. The consumer stages it and requests the missing run rather than applying out of sequence. **Conclusion:** deltas require a declared chain and gap handling.

### Example 7

A transfer succeeds on its second attempt with identical run ID and digest. The consumer's run table prevents a second append. A correction uses a new run ID and supersedes relation. **Conclusion:** retries and corrections need different identity semantics.

### Example 8

An encrypted medical file lands in a plaintext decompression directory retained for thirty days. The design uses encrypted temporary storage, restricted workload identity, immediate cleanup, monitored deletion, and minimized quarantine. **Conclusion:** secure transport does not protect intermediate copies automatically.

### Example 9

A month-end backfill is twenty times normal volume and starves the daily feed. Separate capacity, partitions, priority, network windows, and progress checkpoints isolate it. **Conclusion:** backfills are production workloads requiring explicit resource governance.

### Example 10

A partner stops downloading a file, so the producer disables the job. Live credentials, old objects, notification emails, and contractual retention remain. Closure revokes access, disposes of copies, updates the agreement and catalog, and preserves required evidence. **Conclusion:** inactivity is not complete retirement.

## Cross-Program Connections

- **Data engineering:** extraction, partitioning, formats, manifests, orchestration, validation, loading, backfills, quality, and lineage implement batch flows.
- **Database engineering:** snapshots, isolation, keys, transactions, query load, temporal boundaries, and source positions shape extracts.
- **Distributed systems:** partial failure, retries, idempotency, atomic publication, clocks, storage consistency, and recovery govern exchange.
- **Cybersecurity and privacy:** transfer trust, encryption, keys, purpose, minimization, metadata, residency, retention, deletion, and incidents constrain artifacts.
- **Platform engineering:** managed transfer, object storage, identity, secrets, schemas, observability, self-service, and capacity provide shared capability.
- **API and event engineering:** export APIs, completion events, CDC deltas, contracts, compatibility, and consumer evidence connect patterns.
- **Reliability engineering:** arrival objectives, missing-run detection, fault injection, backpressure, recovery, reconciliation, and runbooks provide assurance.
- **Records and governance:** manifests, signatures, provenance, preservation, holds, correction, partner agreements, and lifecycle determine evidence.

## References

1. Shafranovich, Y., *Common Format and MIME Type for Comma-Separated Values Files*, RFC 4180, 2005. <https://www.rfc-editor.org/rfc/rfc4180>
2. Apache Software Foundation, *Apache Parquet File Format*. <https://parquet.apache.org/docs/file-format/>
3. NIST, *Secure Hash Standard*, FIPS PUB 180-4, 2015. <https://csrc.nist.gov/pubs/fips/180-4/upd1/final>
4. Ylonen, T., and Lonvick, C., *The Secure Shell (SSH) Transport Layer Protocol*, RFC 4253, 2006. <https://www.rfc-editor.org/rfc/rfc4253>
5. W3C, *Data on the Web Best Practices*, W3C Recommendation, 2017. <https://www.w3.org/TR/dwbp/>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a complete daily Account snapshot contract, including population, grain, time, format, manifest, publication, validation, service, protection, correction, and lifecycle.

### Exercise 2

Design a manifest validator for a ten-part delivery. Explain identity, multiplicity, sizes, checksums, aggregate counts, schema, signatures, and limitations.

### Exercise 3

Design snapshot and delta products that support bootstrap, hourly change, late data, deletes, reruns, backfills, and consumer recovery.

### Exercise 4

Compare API pagination, event stream, CDC, daily Parquet snapshot, and CSV partner exchange for operational, analytical, and regulatory consumers.

### Exercise 5

Plan migration of fifty unmanaged file jobs to governed exchanges without disrupting unknown consumers. Include discovery, seams, validation, rollback, protection, and retirement.

## Answers to the Exercises

### Answer 1

Name the Account source-aligned product, producer, authorized consumers, purposes, population rules, exclusions, stable account key, one-record grain, field definitions, units, codes, nulls, classifications, quality, and owner. Declare business-effective boundary, source snapshot or watermark, extraction start and end, UTC publication, business calendar, and limitations. Use an immutable run ID and predecessor relation.

Specify Parquet or another exact format and version, logical and physical types, decimal precision, timestamp units, compression, partition rule, object names, and supported readers. The manifest lists product, run, contract and schema, boundary, watermark, parts, byte sizes, record counts, SHA-256 digests, aggregates, classification, and authenticated publication. Parts land in staging; the manifest commits last. Consumers validate identity, membership, checksums, schema, population, quality, and counts before atomic activation and acknowledgement. Service defines arrival, freshness, recovery, correction, support, and backfill. Protection covers identities, encryption, keys, regions, staging, logs, quarantine, retention, deletion, holds, and incidents. Corrections publish a new superseding run. Retirement revokes access and removes artifacts after consumer evidence.

### Answer 2

Parse a versioned authenticated manifest and verify product, producer, consumer authorization, run ID, expected ten unique part identities, format, schema, time boundary, and predecessor. Compare observed and expected multisets so a duplicate cannot replace a missing part. Reject unexpected objects. For each part verify exact byte size and checksum over the declared representation, then parse under the declared compression and format. Validate schema and structural rules. Sum part records and bytes and compare aggregates.

Then apply population, key uniqueness, referential, quality, and source reconciliation appropriate to the product. Verify the manifest signature or trusted delivery binding and record key identity and verification outcome. Keep parts quarantined until all blocking checks pass; publish one consumer acceptance record. Limitations are explicit: matching sizes and digests prove byte identity, signatures authenticate under key trust, schemas prove structure, and counts provide reconciliation. None alone proves semantic correctness, complete source population, authorized content, current time, or fitness for a consumer decision.

### Answer 3

Publish a consistent full snapshot with immutable run ID, population, source boundary, schema, manifest, parts, checksums, and source watermark or change position. Each hourly delta references its predecessor and defines a half-open source-position or time interval with stable tie-breaker, inserts, updates, deletes, and key changes. A new consumer loads snapshot `S`, then applies deltas after `S`'s watermark in order. It rejects gaps and stages out-of-order arrivals.

Late source records after a watermark create correction deltas linked to affected intervals. A transfer retry keeps run ID and bytes. A rerun records new execution identity and whether bytes are equivalent. A correction or restatement uses a new authoritative run and supersedes relation. Backfills declare historical interval, source reconstruction, schema versions, capacity, and limitations and are isolated from live work. Consumers stage and validate by run, apply state and run checkpoint atomically or idempotently, retain rollback, and reconcile final keys, values, deletes, counts, time, and quality. If delta history is missing, rebuild from a later snapshot under an explicit reset rather than guessing.

### Answer 4

Use an API for interactive selective lookup or commands with low latency, authorization, and current-state semantics. Use events for consumers that must react promptly to individual facts and can manage ordering, duplicates, lag, and local state. Use CDC internally for physical source changes feeding replication, search, or analytical ingestion, transforming it before cross-domain semantic use. Use a daily Parquet snapshot for analytical scans and coherent full populations, with manifest, schema, source boundary, and quality evidence. Use CSV only where a partner's capability requires it, defining the dialect, encoding, protection, manifest, and acknowledgement completely.

A regulator needing immutable evidence may receive a signed encrypted versioned file or archive rather than reconstructing state from an API. Patterns can combine: events announce committed snapshots, an API exposes manifest and status, CDC builds deltas, and snapshots bootstrap event consumers. Keep identities, authority, time, correction, protection, and consumer contracts aligned across mechanisms. Choice follows purpose, workload, consistency, latency, history, service, and constraints.

### Answer 5

Assign stable job, product, run, file, directory, credential, producer, and consumer identifiers. Discover from schedulers, scripts, repositories, file servers, object stores, network rules, accounts, transfer tools, email, spreadsheets, provider consoles, logs, reports, incidents, and interviews. Record population, fields, keys, format, schedule, timezone, source, consumers, purposes, transformations, protection, retention, failure behavior, manual steps, costs, and observed confidence. Monitor unknown access without treating it as authorization.

Group jobs by durable products and legitimate consumer variants. Add contracts, immutable run IDs, schemas, manifests, checksums, authenticated publication, staging, expected-arrival monitoring, acknowledgements, ownership, and correction to existing paths before transport changes. Move to shared transfer capability where it reduces repeated controls while retaining domain meaning. Migrate cohorts with parallel comparison of population, keys, values, nulls, time, integrity, schema, quality, protection, performance, and decisions. Define rollback and bound duplicate copies.

After acceptance and observed inactivity, stop schedules, revoke accounts, keys, and network rules, remove directories, buckets, files, manifests, scripts, alerts, providers, manual steps, and old schemas, update catalogs and lineage, dispose of copies under retention and holds, preserve necessary provenance, and verify closure. Measure known consumers, on-time acceptance, rejects, incidents, correction, migration, protection exceptions, costs, and retirement.
