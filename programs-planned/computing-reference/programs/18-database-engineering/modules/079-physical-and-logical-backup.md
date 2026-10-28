---
module_id: DBE-079
program: Database Engineering
level: 2
module_number: 79
title: Physical and Logical Backup
status: complete
last_verified: 2026-09-05
---

# Physical and Logical Backup

## One-Page Review

### Governing question

How can a database capture a self-describing, integrity-protected, restorable history while writes continue, and how should engineers choose between physical and logical representations without mistaking file copies, replicas, or successful jobs for verified backups?

### Essential definitions

A **physical backup** captures engine storage structures—pages, files, tablespaces, and usually the log range required to make them consistent. A **logical backup** serializes schema and data as logical objects, rows, or commands through database semantics. A **base backup** is a restorable physical starting point. A **consistent cut** is a set of data and metadata corresponding to one valid database state or to a state recoverable through a declared log interval. A **backup manifest** binds identity, format, objects/files, sizes, digests, log history/ranges, dependencies, encryption/compression, and completion evidence. A **snapshot** is a point-in-time view supplied by a database, filesystem, volume, or storage system; its consistency scope must be proven. **RPO** is the maximum tolerated data loss under a named failure; **RTO** is the tolerated time to restore service. **Backup isolation** separates failure, credentials, and retention from the primary system.

### Central model, mechanism, or theorem

A backup artifact B is acceptable only when it forms a recoverable chain:

$$
B=(I,V,S,H,[L_s,L_e],M,K,P),
$$

where I identifies the database/incarnation, V the storage/schema format, S the captured snapshot or logical cut, H the log history, the interval covers every recovery record required from start to end, M is the integrity manifest, K names available cryptographic/key dependencies, and P records capture/publication provenance. Existence or checksum validity alone is insufficient; restore and semantic verification establish recoverability in DBE-080.

### Critical invariants

- Capture all files/objects and metadata required by the selected backup contract from one compatible database history.
- For online physical copies, retain and verify the exact WAL/redo interval needed to reconcile pages copied at different times.
- For logical copies, use a supported snapshot/locking protocol and capture schema, data, ownership, privileges, dependencies, and engine objects within declared scope.
- Publish the backup as complete only after payload, manifest, ending position, integrity metadata, and required log are durable in the backup authority.
- Bind every artifact to database ID, history/timeline, version/format, timestamps only as labels, and stable content identities.
- Encrypt sensitive backups, protect and test key recovery separately, and use least-privilege credentials plus isolated retention.
- Treat partial, cancelled, stale, or unverifiable captures as non-restorable until explicitly repaired and revalidated.
- Never recycle required log or delete the previous good generation before the new backup and its dependencies are proven complete.

### Common failures

Failures include copying live database files without a supported protocol; snapshotting data and WAL volumes at unrelated cuts; trusting filesystem crash consistency as transaction consistency; omitting tablespaces, large objects, extensions, users, privileges, sequences, or encryption metadata; taking a logical dump with DDL races; recording only wall-clock time instead of log history and endpoints; declaring success before uploads and manifests are durable; using mutable object names; storing backups under primary credentials; retaining ciphertext without recoverable keys; restoring only the easiest table in tests; and equating replicas, RAID, export completion, checksums, or catalog rows with a usable backup.

### Compact example

An online physical backup begins at LSN 1,000 and copies pages while transactions continue. One page is copied before update 1,120 and another after update 1,260. The engine ends the backup at 1,400. The artifact is not a point-in-time byte image, but it is recoverable when it includes the supported backup metadata plus complete compatible WAL from the engine-defined start through end. Its manifest records system ID, timeline, file digests, versions, encryption key ID, and log range. A logical dump at snapshot X instead emits schema and rows visible at X, but separately captures global roles and excludes post-X changes. Neither is accepted until a clean restore proves the declared scope.

### Connections

Retrieve [Checksums and Page Corruption](029-checksums-and-page-corruption.md), [Transactions](041-acid-and-transaction-boundaries.md), [Snapshot Visibility](047-snapshot-visibility.md), [Log Sequence Numbers](073-log-sequence-numbers.md), and [Crash Recovery](078-crash-recovery.md). Continue through [the program roadmap](../ROADMAP.md) to point-in-time recovery and restore verification.

## Governing Question

What exactly is being protected: the bytes of one server, a database cluster, selected schemas, tenant rows, roles and privileges, logical history, or the ability to restore an application service? A backup method cannot be judged without this scope. A physical copy may preserve engine-private objects yet be version/platform constrained. A logical dump may be portable and selective yet omit global or non-relational state and take far longer to reload.

The fundamental problem is concurrent capture. Database pages, indexes, catalogs, and log advance while the backup reads them. Either the capture mechanism supplies a transaction-consistent snapshot, or it records enough recovery history to reconcile the mixed page times. Arbitrary file copying supplies neither.

## Why This Matters

Replication optimizes availability and often propagates deletion, corruption, compromise, and operator error. RAID protects against selected device failures without independent history. A backup provides recoverable historical state only when its failure domain, retention, credentials, keys, catalog, and restore path are sufficiently independent.

Physical and logical methods fail differently. Physical backup is usually faster for large same-engine restoration and preserves internal structures, but depends on engine format, page size, tablespace layout, and log continuity. Logical backup exercises database reads and emits durable semantics, supports selective migration, and can cross some versions, but can be slow, expand data, stress locks/snapshots, omit globals/extensions, and reproduce logically corrupt data faithfully.

Current PostgreSQL documentation defines supported base backup and continuous-archiving protocols, provides backup manifests and verification tooling, and documents consistent logical dumps and parallel dump constraints. MySQL 8.4 distinguishes physical and logical methods and documents consistency/locking requirements. SQLite provides an online backup API and a `VACUUM INTO` path rather than endorsing arbitrary live multi-file copying. The product-specific protocol is part of correctness.

## Prerequisites and Retrieval

Retrieve these concepts:

- crash consistency, transaction consistency, and application consistency are different guarantees;
- WAL/redo positions require database and history identity plus exact endpoint semantics;
- MVCC snapshots determine row visibility but may not automatically freeze every schema or global object;
- pages can be copied before or after concurrent changes and require recovery to reach a consistent state;
- filesystems and storage snapshots have atomicity scopes that may not cover multiple volumes or external keys;
- content digests detect accidental or adversarial changes only under protected algorithms/manifests and trustworthy verification;
- compression, encryption, deduplication, chunking, and transport each add format and key dependencies;
- RPO/RTO are measured under named failures and include catalog, credential, key, network, verification, and traffic-restoration time;
- data classification, retention, legal hold, deletion, residency, and access logging apply to historical copies.

DBE-078 established the recovery lifecycle. This module produces valid backup inputs; DBE-080 proves restoration, target selection, and semantic readiness.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical, logical, full, incremental, differential, snapshot, and log-archive artifacts;
2. derive online physical-backup correctness from a supported start/copy/end/log protocol;
3. define logical snapshot, schema, dependency, and global-object coverage;
4. design immutable manifests and atomic backup publication;
5. analyze version, platform, tablespace, extension, encryption, and key dependencies;
6. engineer retention, isolation, deduplication, deletion, and capacity policies safely;
7. choose physical, logical, or combined strategies from recovery and migration requirements;
8. validate capture using fault injection, catalog reconciliation, integrity checks, and restore evidence.

## Core Exposition

**Define the protected unit.** A PostgreSQL cluster-level physical base backup, a MySQL instance snapshot, a logical schema dump, and a tenant export protect different things. Inventory databases, schemas, tables, partitions, indexes, large objects, sequences, views, routines, extensions/plugins, roles, grants, tablespaces, configuration, encryption metadata, and application-external dependencies. Mark each included, reconstructed, separately protected, or excluded.

The unit also has time semantics. A logical dump may represent one MVCC snapshot. A physical online backup may contain page images from many moments but be recoverable to a consistent endpoint using WAL. A storage snapshot may freeze one volume atomically while another continues. “Taken at 02:00” does not define a consistent cut.

**Physical online backup is a protocol.** A typical supported flow establishes a backup start position and mode, ensures required metadata/full-page protection, copies all owned physical files using the engine's rules, obtains an ending position and backup-completion metadata, retains the required log interval, then publishes the artifact. WAL reconciles pages copied before and after concurrent updates during restore.

The exact inclusive/exclusive interval and checkpoint relationship are engine-specific. Record start/end, timeline changes, and archive completion must be preserved. Copying the data directory first and later “finding some WAL” is not equivalent because the required start, history, and mode may be unknown.

**Coordinate multiple storage domains.** Tablespaces, separate WAL devices, object stores, and external catalogs can cross snapshot boundaries. A storage snapshot is usable only if its consistency group covers every relevant volume or the database protocol supplies log reconciliation. Freeze hooks must be bounded, failure-safe, and always unfreeze. Snapshot creation success does not prove upload/copy completion or future readability.

**Logical backup is also a protocol.** Obtain a supported consistent snapshot and decide how DDL is controlled. Enumerate objects from a catalog view compatible with that snapshot, serialize definitions in dependency order or preserve a dependency graph, emit data with unambiguous encoding and null/binary semantics, record ownership/privileges/security labels, and capture global objects separately where required. Parallel workers must share the intended snapshot or declare weaker cross-table consistency.

Logical dumps commonly omit physical indexes and rebuild them, which can detect some corruption but adds time and resource needs. They may preserve bad logical values and omit engine-private objects. Generated columns, collations, extensions, functions, triggers, sequences, row-level security, partition attachment, and large objects require explicit handling.

**Handle DDL and object identity.** A table can be renamed, dropped, recreated, or repartitioned while a dump enumerates and reads it. Names are not stable identity. A supported database snapshot plus appropriate catalog/DDL locking or dependency protocol must ensure each serialized object corresponds to the intended version. Otherwise a manifest can claim table A while containing rows from a recreated A.

**Build an immutable manifest.** Record backup ID, parent ID for incremental chains, database/system ID, history/timeline, capture method/tool and version, database version, platform/architecture constraints, start/end positions, snapshot ID, object/file inventory, byte sizes, content digests, chunking/compression/encryption formats, key ID, required log ranges, tablespaces, exclusions, timestamps, creator identity, storage locations, retention class, and completion state.

Protect the manifest itself with authenticated integrity and immutable versioning. Object-store checksums or ETags may not be end-to-end content digests and can change semantics with multipart upload or encryption. Compute and verify a declared cryptographic digest over the exact stored representation or clearly defined plaintext/ciphertext layer.

**Publish atomically.** Upload payload under immutable candidate names, verify sizes/digests and required log availability, write the final manifest, durably publish a small catalog pointer/status, then allow retention automation to consider older generations. A failed or cancelled candidate remains incomplete and cannot replace the last verified generation. Readers never infer completeness from directory presence.

**Design incremental chains conservatively.** An incremental backup records changes since a parent/base according to a change-tracking mechanism. A differential records changes since a fixed base. Chains reduce transfer/storage but add dependencies and restore steps. Validate parent identity, bitmap/LSN coverage, page generations, and chain continuity. Losing one middle incremental can invalidate later descendants.

Synthetic full construction rewrites or composes artifacts; it requires the same integrity and atomic publication as a live backup. Deduplication creates shared chunks whose deletion reference counts become correctness-critical. Retention operates on dependency graphs, not filenames or creation age alone.

**Protect keys and credentials.** Encrypt in transit and at rest, but decide whether digests cover plaintext, ciphertext, or both. Store key identifiers and algorithm/version metadata without embedding secrets. Key backup, escrow, rotation, revocation, and disaster access must survive loss of the primary identity provider under controlled dual authorization.

Separate backup-writer, verifier, restore, and deletion privileges. Use immutable or object-lock retention where appropriate, separate accounts/projects/regions, and test compromise scenarios. A backup encrypted with an irrecoverable key is durable ciphertext, not recoverable data.

**Treat retention as policy plus graph safety.** Retain generations to meet time-based and event-based recovery needs, legal holds, audit, and disaster separation. Before deletion, prove no retained incremental, restore point, replica seed, or investigation depends on the artifact. Expiration of personal data in backups needs a documented delayed-deletion or cryptographic-erasure model consistent with law and restoration procedures.

Retention must include required WAL/log. A base backup without the log needed to reach consistency is incomplete. Conversely, log without a compatible base may not be usable. Catalog the pair as a recoverable chain and continuously audit gaps before primary log recycling.

**Choose from restore objectives.** Physical backup usually minimizes bytes transformed and restore CPU for large same-engine recovery. Logical backup can select tenants/tables, inspect semantics, and migrate across supported versions/platforms. A combined strategy uses frequent physical bases plus continuous WAL for disaster recovery and periodic logical exports for selective recovery/migration. Neither replaces application-level export of external objects.

**Measure capture without claiming restore.** Observe snapshot establishment, bytes/files/objects/chunks, read and upload rate, dirty/WAL generation, retained log, checksum failures, retries, compression ratio, key access, catalog publication, and primary workload effects. “Backup successful” should mean capture contract complete; a separate latest-verified-restore metric records stronger evidence.

**Test capture failures.** Kill workers before/after snapshot, file copy, upload, manifest write, log archive, and publication. Inject short reads, changed files, stale listings, truncated objects, checksum mismatch, DDL races, tablespace omission, expired credentials, missing keys, ENOSPC, network partitions, and object-store inconsistency. Verify candidates never become complete and previous good generations remain protected.

The executable fixture below validates a tiny immutable manifest against payload digests and a required object set. It does not implement snapshot consistency, database backup, encryption, object storage, or restoration.

<!-- bijux-verify: {"id":"finite-backup-manifest-verifier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"backup_id=base-0042\nobject_count=3\nrequired_coverage=true\ndigests_valid=true\nlog_range=1000..1400\nhistory=timeline-7\npublishable=true\nmissing_object_publishable=false\ntampered_publishable=false\nevidence=finite_backup_manifest_verifier\n","stderr":""}} -->
```python
from hashlib import sha256

payloads = {
    "control": b"system=alpha;checkpoint=1000",
    "data/users": b"page-set-users-v4",
    "data/orders": b"page-set-orders-v9",
}
required = {"control", "data/users", "data/orders"}
manifest = {
    "backup_id": "base-0042",
    "history": "timeline-7",
    "log_start": 1000,
    "log_end": 1400,
    "objects": {name: sha256(body).hexdigest() for name, body in payloads.items()},
}

def publishable(candidate: dict[str, bytes]) -> bool:
    if set(candidate) != required:
        return False
    return all(
        sha256(candidate[name]).hexdigest() == manifest["objects"].get(name)
        for name in required
    )

missing = {name: body for name, body in payloads.items() if name != "data/orders"}
tampered = dict(payloads)
tampered["data/orders"] += b"!"

print(f"backup_id={manifest['backup_id']}")
print(f"object_count={len(manifest['objects'])}")
print(f"required_coverage={str(set(payloads) == required).lower()}")
print(f"digests_valid={str(publishable(payloads)).lower()}")
print(f"log_range={manifest['log_start']}..{manifest['log_end']}")
print(f"history={manifest['history']}")
print(f"publishable={str(publishable(payloads)).lower()}")
print(f"missing_object_publishable={str(publishable(missing)).lower()}")
print(f"tampered_publishable={str(publishable(tampered)).lower()}")
print("evidence=finite_backup_manifest_verifier")
```

## Definitions and Notation

- `I`: database/system incarnation identifier.
- `V`: database, page, schema, tool, and artifact format versions.
- `S`: physical capture interval or logical snapshot/cut.
- `H`: log timeline/history and ancestry.
- `[L_s,L_e]`: engine-defined required recovery-log interval with explicit endpoint semantics.
- `M`: protected manifest of exact artifact coverage and digests.
- `K`: encryption/key identifiers and recovery dependencies.
- `P`: capture, upload, verification, and publication provenance.
- **Full backup:** self-contained payload except declared log/runtime dependencies.
- **Incremental backup:** changes since a named parent artifact or position.
- **Differential backup:** changes since a fixed base.
- **Synthetic full:** new full artifact constructed from existing backup components.
- **Recovery chain:** compatible base, increments, logs, manifests, keys, and tools needed for a target.
- **Capture complete:** all declared artifacts and dependencies are durably published and integrity-verified; restore remains unproven.

## Mechanisms, Invariants, or Proof Structure

**Physical-cut argument.** Assume the engine's online-backup protocol establishes start L_s, copies every required physical object, records end L_e, and retains a complete compatible log range sufficient to reconcile every page image. Then the mixed-time copy can be transformed by the engine's recovery algorithm into the protocol's declared consistent state. Arbitrary copies fail because these coverage and metadata premises are absent.

**Logical-cut argument.** Assume every worker uses the same supported transaction snapshot, DDL/object identity is stabilized, and every declared logical/global dependency is captured. Then emitted rows and definitions represent the declared snapshot scope. The result says nothing about excluded globals, external objects, nondeterministic code, or reload compatibility unless separately proven.

**Publication invariant.** A catalog marks generation G complete only after every required payload, manifest, digest, log interval, and key dependency is durably referencable. A crash before publication leaves G incomplete and the prior complete generation intact.

**Chain-retention invariant.** Deletion is permitted only when no retained recovery target has a dependency path through the artifact/chunk/log/key. Reference and legal-hold updates are atomic with deletion authorization.

**Integrity boundary.** A content digest supports equality of the defined byte representation under cryptographic assumptions. It does not prove snapshot consistency, completeness, provenance, semantic correctness, confidentiality, or restorability.

## Alternatives and Trade-Offs

| Method | Strength | Limitation | Best-fit evidence |
| --- | --- | --- | --- |
| Physical base + WAL | fast large same-engine recovery, internal coverage | version/platform and log dependency | protocol trace and full restore |
| Logical dump | selective, inspectable, migration-friendly | slow reload and scope omissions | snapshot/object inventory and reload |
| Storage snapshot | fast copy boundary | consistency group and provider dependency | multi-volume crash/restore test |
| Incremental physical | reduced transfer/storage | chain and tracking complexity | parent/change-map verification |
| Differential | bounded base dependency | growing artifact size | base identity and merge restore |
| Synthetic full | shorter future restore chain | composition/dedup correctness | atomic construction and independent verify |
| Combined physical/logical | complementary disaster/selective paths | cost and operational complexity | separate objectives and drills |

## Failure Modes and Misconceptions

1. **“A file copy is a physical backup.”** Live files require the supported database/snapshot protocol and recovery log.
2. **“A storage snapshot is transaction-consistent.”** Its atomicity scope and database coordination must be proven.
3. **“Logical means complete.”** Globals, privileges, extensions, large objects, and external state may be absent.
4. **“One worker snapshot covers parallel dump workers.”** Snapshot sharing must be explicit and supported.
5. **“Names identify objects.”** Rename/drop/recreate races require stable catalog identity and DDL control.
6. **“Checksums prove recoverability.”** They prove only defined-byte equality/integrity assumptions.
7. **“The job exited zero, so publication is complete.”** Payload, log, manifest, catalog, and remote durability must all pass.
8. **“Latest timestamp selects the right backup.”** Identity, history, generation, completion, and target coverage govern selection.
9. **“Replication is backup.”** Replicas commonly propagate deletion/corruption and share credentials/failure domains.
10. **“Encryption guarantees safety.”** Key loss destroys recovery; key compromise exposes every retained copy.
11. **“Deduplication only saves space.”** Shared-chunk reference/deletion correctness becomes critical.
12. **“Incrementals can be deleted by age.”** Descendant and target dependencies must be traversed.
13. **“A base backup needs no WAL.”** Online mixed-time pages often require a declared recovery interval.
14. **“Logical restore is cross-version by definition.”** syntax, types, extensions, collations, and semantics still constrain it.
15. **“RPO equals schedule interval.”** Failed captures and unverified chains can make the recoverable point older.
16. **“Backup completion proves data correctness.”** Restore and semantic verification remain separate.

## Worked Examples

### Example 1

**Situation.** An operator copies a live data directory over 40 minutes without telling the engine.

**Reasoning.** Pages and control/catalog files come from different transaction times; a page split or file create/drop can cross the copy. There is no supported start/end metadata or guaranteed WAL range. Even if every file checksum matches its copied bytes, the set need not be a recoverable history.

**Conclusion.** Byte-copy integrity cannot replace an online physical-backup protocol.

### Example 2

**Situation.** Data is on volume A and WAL on volume B; snapshots occur five seconds apart.

**Reasoning.** Unless a consistency group atomically covers both or the database protocol records a recoverable interval and retains matching WAL, the cuts may disagree. A newer data page can require log absent from B's older snapshot. Coordinate snapshots or use a supported backup mode with archived WAL.

**Conclusion.** Multi-volume atomicity or log reconciliation is an explicit premise.

### Example 3

**Situation.** A parallel logical dump uses independent default snapshots while transfers overlap active writes.

**Reasoning.** Orders worker may see a newly committed order while customers worker sees the earlier snapshot without its customer, creating a cross-table state never authorized at one instant. Export/share one supported snapshot among workers or lock to the declared consistency level.

**Conclusion.** Parallel speed must preserve one declared logical cut.

### Example 4

**Situation.** Table `accounts` is dropped and recreated after enumeration but before row copy.

**Reasoning.** The name remains, but object identity, schema, ownership, and rows changed. A dump that binds work only by name can pair old metadata with new contents. Supported snapshot/catalog semantics plus DDL locking or identity validation must reject or serialize the race.

**Conclusion.** Backup objects need stable identity, not merely stable names.

### Example 5

**Situation.** Every backup object exists, but one multipart upload was truncated and its provider ETag still looks plausible.

**Reasoning.** Compare expected size and a declared end-to-end digest computed over the exact stored layer. The manifest must remain incomplete on mismatch. Provider-specific ETag semantics are not silently treated as SHA-256 or as proof of plaintext identity.

**Conclusion.** Publication requires explicit end-to-end integrity, not object presence or an ambiguous storage tag.

### Example 6

**Situation.** A base backup is valid, but WAL segment 37 inside its required range is missing.

**Reasoning.** Later segments cannot reconstruct the gap. Mark the chain non-restorable for targets requiring segment 37, retrieve the exact compatible segment from another archive/replica, or select an older/newer complete base and range. Do not recycle primary WAL until archive continuity is verified.

**Conclusion.** A single required-log gap invalidates the affected recovery chain.

### Example 7

**Situation.** Encrypted backups survive a regional disaster, but the only key service and administrator credentials were in that region.

**Reasoning.** Artifact durability exists but decryptability does not. Key escrow/recovery must occupy an independent failure domain with audited emergency authorization, tested rotation/version support, and no dependency on the failed primary identity path.

**Conclusion.** Recoverable key custody is part of backup completeness.

### Example 8

**Situation.** Retention wants to delete incremental I2; retained synthetic full S claims to include it.

**Reasoning.** Verify S's atomic completion, independent content manifest, parent/chunk materialization, and successful restore evidence before severing I2. If S shares deduplicated chunks with I2, delete only the logical reference and preserve reachable chunks transactionally.

**Conclusion.** Retention follows verified dependency graphs, not artifact labels.

### Example 9

**Situation.** A physical backup restores 20 TB quickly, while a logical dump can recover one accidentally deleted tenant.

**Reasoning.** The physical path fits whole-service disaster recovery and preserves engine internals. The logical path provides selective semantics but may require dependency filtering and reconciliation. Keeping both can be justified when disaster and tenant-recovery objectives differ, with independent schedules and tests.

**Conclusion.** Representation choice follows recovery units and objectives rather than a universal ranking.

### Example 10

**Situation.** Hourly jobs are green, but the two newest generations reference missing tablespace objects.

**Reasoning.** The last complete recoverable capture is three hours old. Nominal schedule suggests one-hour RPO, but evidence shows a three-hour current recoverable point before restore testing. Alert on manifest coverage and latest verified restore, not job count alone.

**Conclusion.** Observed recoverable history—not schedule—is the current RPO evidence.

## Cross-Program Connections

- **Data Architecture Engineering:** recovery objectives, lineage, retention, sovereignty, legal hold, and semantic inventories govern backup policy.
- **Operating Systems:** snapshots, freeze/thaw, filesystem ordering, sparse files, and device failure define physical capture.
- **Distributed Systems:** consistent cuts, object-store durability, quorum catalogs, epochs, and multi-region independence support publication.
- **Security Engineering:** encryption, key custody, immutability, least privilege, deletion, and ransomware separation protect history.
- **Platform Engineering:** scheduling, capacity, bandwidth, monitoring, credentials, failure injection, and restore environments operationalize backups.
- **Data Engineering:** exports, schema evolution, partitioning, CDC/log archives, and external object dependencies shape logical scope.
- **Software Testing and Quality Engineering:** fault matrices, manifest oracles, mutation tests, and restore drills distinguish evidence levels.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18: Continuous Archiving and Point-in-Time Recovery](https://www.postgresql.org/docs/18/continuous-archiving.html), reviewed 2026-09-05. Official base-backup, WAL archive, backup history, recovery, and timeline protocol.
2. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_basebackup`](https://www.postgresql.org/docs/18/app-pgbasebackup.html), reviewed 2026-09-05. Official online base-backup behavior, targets, manifests, compression, and WAL methods.
3. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_verifybackup`](https://www.postgresql.org/docs/18/app-pgverifybackup.html), reviewed 2026-09-05. Official manifest and required-WAL verification boundaries.
4. PostgreSQL Global Development Group, [PostgreSQL 18: SQL Dump](https://www.postgresql.org/docs/18/backup-dump.html), reviewed 2026-09-05. Official logical dump, consistency, global-object, and restore behavior.
5. Oracle, [MySQL 8.4 Reference Manual: Database Backup Methods](https://dev.mysql.com/doc/refman/8.4/en/backup-methods.html), reviewed 2026-09-05. Official physical/logical method and consistency overview.
6. Oracle, [MySQL 8.4 Reference Manual: `mysqldump`](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html), reviewed 2026-09-05. Official logical dump options, transactional consistency, object coverage, and limitations.
7. SQLite Project, [Online Backup API](https://www.sqlite.org/backup.html), reviewed 2026-09-05. Official online copy semantics under concurrent access.
8. SQLite Project, [`VACUUM INTO`](https://www.sqlite.org/lang_vacuum.html#vacuuminto), reviewed 2026-09-05. Official alternative consistent backup-file behavior and limitations.
9. NIST, [SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems](https://csrc.nist.gov/pubs/sp/800/34/r1/final), 2010, reviewed 2026-09-05. Authoritative contingency, recovery, testing, and plan-maintenance guidance.
10. Google, [Site Reliability Engineering: Data Integrity—What You Read Is What You Wrote](https://sre.google/sre-book/data-integrity/), reviewed 2026-09-05. Operational backup, restore, corruption, and human-error lessons.

## Exercises

### Exercise 1

Define physical backup, logical backup, consistent cut, recovery log interval, manifest, capture completion, and restore verification. Explain which concepts are not interchangeable.

### Exercise 2

An online physical backup starts at LSN 2,000, copies data across two volumes, ends at 3,200, and has archived WAL 2,000–2,700 plus 2,900–3,400. Determine its status and the smallest repair.

### Exercise 3

Design a logical backup protocol for a database with active DDL, parallel workers, roles, grants, sequences, large objects, extensions, and tenant selection. State consistency and exclusion evidence.

### Exercise 4

Compare physical base plus WAL, full logical dump, storage snapshot, and incremental physical backup for whole-region loss, one-tenant deletion, major-version migration, and 30 TB restore.

### Exercise 5

Design an immutable multi-region backup system and capture-validation campaign. Include manifests, keys, credentials, deduplication, retention/legal deletion, failures, monitoring, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Physical backup captures engine storage representations and normally depends on compatible recovery log and software. Logical backup captures declared schema/data semantics through database APIs. A consistent cut is the valid state represented directly or reconstructable by a protocol. The recovery interval supplies records needed to reconcile mixed-time physical capture. A manifest binds exact identity, coverage, formats, digests, dependencies, keys, and publication. Capture completion proves those declared artifacts were durably published and checked; it does not prove they restore or satisfy semantics. Restore verification executes the recovery path and evaluates independent oracles. Files, snapshots, manifests, and checksums each support only part of that chain.

### Answer 2

The required interval has a gap from 2,700 to 2,900, so the backup is incomplete/non-restorable for its declared online physical protocol even though WAL extends beyond the end. Copying two volumes is also valid only if the engine protocol or a consistency group covers their relation. The smallest repair is to retrieve the exact compatible missing WAL 2,700–2,900 (respecting record/segment endpoint conventions) from primary retention, another archive, or replica and verify continuity, history, and integrity. If unavailable, discard the candidate or use another complete base/range; do not publish it as complete.

### Answer 3

Open one supported exported/shared snapshot and bind every parallel worker to it. Stabilize object identity and schema with supported DDL locking or a catalog protocol so drop/recreate/alter races cannot mix versions. Inventory tenant tables/partitions, dependency objects, sequences, large objects, views/functions/triggers, collations, extensions, roles, grants, ownership, row-security policy, and global configuration; mark included, reconstructed, separate, or excluded. Filter tenant rows through authoritative keys and include cross-tenant/shared dependencies explicitly. Record snapshot ID, database/tool versions, object IDs and definitions, row/chunk counts/digests, encodings, null/binary semantics, exclusions, and DDL observations. Test concurrent DDL and mutations and reconcile referential/business totals.

### Answer 4

Physical base plus continuous WAL is normally strongest for whole-region loss and a 30 TB same-engine restore because it minimizes logical transformation; it needs isolated bases, log continuity, compatible infrastructure, and full drills. Logical dump is strongest for selective tenant recovery and can aid major-version migration, but dependency filtering/reload and 30 TB rebuild time may be prohibitive. A storage snapshot can seed rapid large restore when its consistency group and regional independence are proven, but provider/volume coupling remains. Incremental physical reduces routine transfer yet adds chain and merge dependencies. A combined portfolio is reasonable: physical/snapshot plus WAL for disaster scale, logical tenant exports for selection/migration, and verified chain/restoration evidence for each objective.

### Answer 5

Use isolated accounts/regions and immutable content-addressed payloads. Candidate uploads record sizes and plaintext/ciphertext digests, then publish an authenticated manifest containing backup/parent IDs, database/history/version, snapshot and WAL endpoints, inventory, chunk graph, compression/encryption/key IDs, provenance, exclusions, retention, and legal holds. A quorum or strongly consistent catalog marks complete only after payload/log verification. Split writer, verifier, restore, key-recovery, and deletion privileges; escrow keys and emergency identity independently. Retention traverses parent/chunk/log/key dependencies and applies legal deletion atomically. Inject worker death, DDL, short reads/uploads, missing objects/log, stale listings, corruption, region/network loss, expired credentials, unavailable keys, ENOSPC, and catalog crash. Monitor latest complete and latest restored point, gaps, coverage, age, bytes, failures, keys, capacity, and restore results. Canary new readers before writers emit new formats; rollback preserves compatible tools and never deletes the prior good generation until the new chain is restored and verified.
