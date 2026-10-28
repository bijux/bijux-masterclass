# Module 08 — Backup, Restore, RPO, RTO, and Disaster Recovery

> **Governing question:** How can the platform prove that authoritative data can be reconstructed in a clean environment within an agreed loss and time budget?

## Why this module exists

Daily backup jobs have been green for six months. During an incident, the team discovers that the backup contains volume data but not the database encryption key or the schema migration record. The most recent restorable copy is three weeks old. Backup completion had been measured; recoverability had not.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- distinguish snapshot, replication, backup, archive, and disaster recovery
- derive backup frequency and log retention from RPO
- derive restoration workflow and staffing from RTO
- create content-verified backup manifests
- restore into an empty destination and validate application invariants
- design regional and account-level failure exercises

## Snapshots, replication, backup, and archive solve different problems

A snapshot is a point-in-time storage copy, often in the same backend and administrative domain. Replication maintains additional copies and may reproduce deletion or corruption quickly. A backup is a governed recovery copy with inventory, retention, integrity, and restoration procedure. An archive prioritizes long-term retention and retrieval. Disaster recovery combines data, infrastructure, identity, configuration, procedure, and people to restore a capability after a defined disaster.

A mature design layers these mechanisms. Fast snapshots may support operational rollback, log shipping may reduce RPO, object-store backups may survive cluster loss, and cross-account copies may survive credential compromise.
## RPO is a property of the whole write path

An hourly snapshot does not guarantee a one-hour RPO if the snapshot cannot be restored, if logs required for recovery are missing, or if the application acknowledges writes before they are durable. RPO is measured from the latest business operation that can be reconstructed in the recovery environment.

Atlas records a monotonic transaction generation in backup manifests. Restore verification compares the recovered generation with the declared objective. The course also distinguishes time-based RPO from operation-count or event-sequence objectives.
## RTO includes decision and preparation time

RTO is not only data transfer duration. It includes incident recognition, authority to declare recovery, environment provisioning, identity and key restoration, data retrieval, verification, DNS or routing changes, client recovery, and operator decision points. A technically fast restore can miss RTO because no one knows who may initiate it.

Course 6 runbooks name roles, prerequisites, commands, abort conditions, and expected evidence. Course 7 will automate delivery, but automation cannot invent missing authority or recovery policy.
## A backup manifest makes a copy intelligible

Atlas backup manifests include source identity, data class, application version, schema version, snapshot or checkpoint identity, content digests, object sizes, encryption context reference, creation time, retention class, and predecessor chain. The manifest itself is checksummed and stored separately from the source volume.

Content-addressed chunks reduce duplicate transfer, but deduplication creates shared dependencies: deleting one chunk can invalidate many backups. Garbage collection must prove reachability from retained manifests before deletion.
## Restore into emptiness is the decisive test

Restoring over the original volume can accidentally depend on surviving files, credentials, network paths, or metadata. Atlas restores into an empty directory and a newly created logical environment. The drill verifies digests, file inventory, schema, transaction generation, artifact references, and application startup. It records elapsed time by phase.

A successful file copy is not the final oracle. The recovered application must answer domain queries and preserve expected invariants. For a database, that can include constraint checks, transaction-log position, row counts, and known sentinel records.
## Disaster boundaries must be larger than the source

A backup stored in the same cluster, zone, account, credentials, and encryption-key hierarchy as the source may not survive the intended disaster. Cross-zone, cross-region, or cross-account copies increase resilience but also create data-sovereignty, key-management, cost, and transfer concerns.

Atlas maps each recovery copy to failure domains and administrative authorities. It refuses to claim regional recovery from a backup that has never left the source region or from a restore process requiring the failed cluster’s control plane.

## Incremental chains trade transfer for dependency

Incremental backups reduce copied data but create a dependency chain. Losing one base or delta can invalidate later recovery points. Retention and garbage collection must reason over the graph, not individual object age. Synthetic full backups can shorten restore chains while consuming additional compute and storage.

Atlas manifests record parent identity and verify chain completeness before declaring a recovery point restorable.


## Encryption recovery is part of the backup

Encrypted bytes without recoverable key authority are not a usable backup. Storing the key beside the backup can collapse the failure boundary. A recovery design records key identifiers, restoration authority, rotation history, and an independent procedure for obtaining or recreating access.

Restore drills should exercise the actual key path. A test that reuses live process credentials may hide a missing disaster procedure.


## Restore verification should query meaning

Checksums prove byte integrity, not application correctness. A database restore should verify schema version, constraints, known records, transaction generation, and application queries. An artifact restore should verify object digests and metadata references. A queue restore should verify deduplication and lease state.

Atlas’s domain oracle checks a sentinel run and artifact relationship after file verification. This prevents a structurally complete but logically inconsistent restore from passing.


## Disaster exercises must protect the source

A DR drill should not require destructive action against the authoritative environment. Restore into isolated names, networks, credentials, and storage. Prevent the recovered system from sending real webhooks, processing production queues, or accepting public writes.

Course 5’s network controls and Course 3’s runtime identity become safeguards during recovery. The course handoff marks drill environments as non-authoritative.

## Worked semantic example

```python
from atlas_data.backup import BackupRepository

repo = BackupRepository("./backup-target")
manifest = repo.backup_directory(
    source="./atlas-state",
    logical_name="atlas-run-state",
    generation=8842,
)
result = repo.restore(manifest.id, destination="./empty-restore")
assert result.verified
assert result.generation == 8842
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: atlas-backup
  namespace: atlas-system
spec:
  schedule: "17 * * * *"
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| green backup | restore lacks keys or metadata | empty-destination drill |
| RPO miss | latest restorable generation too old | generation and time evidence |
| same-account loss | source and backup share authority | failure-domain map |

## Atlas capstone increment

A content-addressed backup repository, manifest chain, empty-destination restore, domain verification, and measured RPO/RTO report form the Atlas recovery dossier.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 9 tests whether the storage design remains measurable and supportable under latency, capacity, attachment, filesystem, and backend failure.

## Advanced design review — recovery is a second deployment path

A disaster restore exercises infrastructure, identity, keys, storage, networking, software artefacts, schema, application validation, traffic, and human authority. It should be designed as a maintained product path rather than an emergency script. Every production dependency needed for restore must either exist independently or be reproducible from retained artefacts.

Measure RPO by the last restorable generation, not the last backup schedule. Measure RTO until clients receive a correct service, not until bytes copy. Break both into phases so improvements target the real bottleneck. A backup repository can be fast while key retrieval or application validation dominates recovery.

## Recovery copies need independent control

Immutability and cross-account retention reduce ransomware and operator blast radius, but they also require governed recovery identities. Test the identity from the target environment. A privileged source account session that can read the backup during a drill hides the exact failure the copy is meant to survive.

## Restore certification should sample history

Always restoring the newest backup can miss defects in incremental chains, retention, old encryption keys, and software compatibility. A mature program samples recovery points across the advertised window: recent, middle, oldest retained, and a point after a key or schema rotation. It also restores after deliberately removing a required object to prove the system fails closed.

Certification frequency should follow change and risk. Database upgrades, backup-tool changes, key rotation, repository migration, and new data size can invalidate previous evidence. Record the software and infrastructure versions used for each restore so a passing drill is not generalized indefinitely.

## RPO and RTO are negotiated service properties

A lower RPO can require continuous log shipping, more durable acknowledgement, or synchronous replication. A lower RTO can require preprovisioned capacity, warm credentials, automated infrastructure, and practiced decision authority. Both increase cost and complexity. Service owners should choose them based on business impact rather than inherit an arbitrary platform default.

The platform can offer profiles, but each profile states what disasters it covers and what it costs. If a requested objective is impossible with the selected architecture, the correct platform behavior is to reject or escalate the request, not publish a hopeful number.
## Recovery objectives are service decisions

RPO and RTO are not storage product features. They are service-level decisions that determine architecture, cost, and operating practice.

- **Recovery Point Objective (RPO)** is the maximum acceptable amount of recent history that may be lost, measured from the failure back to the selected recovery point.
- **Recovery Time Objective (RTO)** is the maximum acceptable time to restore the service to the defined usable state.

A backup every 24 hours cannot satisfy a one-hour RPO unless another mechanism, such as continuous log shipping, closes the gap. A storage snapshot that restores in five minutes may not satisfy a fifteen-minute RTO if key retrieval, database recovery, schema validation, DNS change, and client reconnection take an hour.

### Decompose RTO into owned phases

A practical RTO budget is the sum of several phases:

```text
detect and declare incident
+ select recovery point
+ provision destination
+ retrieve data and keys
+ restore bytes
+ recover application state
+ validate integrity and semantics
+ redirect traffic
+ verify clients and close incident
```

Assign an owner and expected duration to each phase. A storage team can optimize restore throughput while the overall RTO remains dominated by manual approval or missing application validation. Course 6 treats the complete critical journey as the objective.

### Backup architecture requires independent failure domains

A backup that shares the same credentials, account, cluster, region, deletion policy, and key as the primary is vulnerable to the same administrative or security failure. Independence is a spectrum, but the dossier must state it honestly.

Possible boundaries include:

- separate bucket or repository;
- separate account or project;
- separate region;
- independent immutable retention;
- separate deletion authority;
- separately recoverable encryption keys;
- offline or logically air-gapped copies;
- independent catalogue and monitoring.

The stronger the disaster claim, the more independent the recovery plane must be.

### A backup set is a graph, not a file

Point-in-time recovery may depend on a base backup, incremental chunks, write-ahead logs, manifests, checksums, schema metadata, and encryption keys. Deleting one node in this graph can invalidate later recovery points. Backup catalogues should track dependency chains and prevent retention policies from removing required ancestors.

Atlas’s dependency-light repository stores content-addressed objects and a manifest. The proof verifies every referenced object and restores into an empty directory. A production database adds engine-specific logs and metadata, but the same principle holds: the catalogue must prove that the selected recovery point is complete.

### Integrity has several layers

A successful checksum proves that bytes match the recorded digest. It does not prove the bytes represent the intended service state. Validation should proceed through layers:

1. repository object integrity;
2. manifest and identity integrity;
3. decryption and decompression;
4. filesystem or database structural checks;
5. schema compatibility;
6. application invariants;
7. tenant and authorization boundaries;
8. end-to-end business workflow.

The restored service remains isolated until required layers pass. “Database process started” is not the final oracle.

### Restore into a new destination

Restoring over the existing primary destroys comparison evidence and can combine old and restored state. A safer procedure creates a new destination with a new identity, restores the chosen point, validates it, and only then performs a controlled cutover. This supports rollback and makes data lineage visible.

The destination must be empty unless the restore tool explicitly supports and verifies incremental application. Atlas rejects non-empty destinations by default. The restore records source manifest, target identity, tool version, start and completion times, checksums, and validation results.

### Encryption keys are part of the backup

A retained encrypted backup is useless if its key is destroyed, access policy no longer works, or the key is bound to an unavailable account. Conversely, giving the workload broad key authority undermines separation. The recovery plan names:

- key identity and version;
- recovery principals;
- escrow or independent account boundary;
- rotation policy;
- historical decryption availability;
- key-loss test;
- audit evidence;
- emergency access controls.

A backup drill should include obtaining the key through the real recovery path, not a conveniently preloaded development secret.

### Disaster tiers and truthful claims

Define failure tiers explicitly:

| Tier | Example | Typical mechanism |
|---|---|---|
| process/Pod | crash or restart | durable primary storage and application recovery |
| Node | machine loss | reattachment or replicated data service |
| zone | zonal outage | multi-zone service or cross-zone recovery |
| cluster | control-plane or cluster loss | external backup plus new-cluster restoration |
| region | regional failure | cross-region recovery copies and independent foundation |
| account/security | credential compromise | isolated recovery account, keys, and deletion authority |

Passing a Node-loss test does not justify a regional DR claim. Each tier needs its own executed evidence or a visible `not-executed` status.

### Drill design

A good restore drill starts from a clean destination, uses production-shaped sizes, follows the real authorization path, measures each RTO phase, and produces a decision. It also tests failure branches: missing object, corrupt manifest, unavailable key, incompatible schema, insufficient capacity, and stale DNS.

The drill is complete only when the service performs a meaningful user journey and the team records lessons, remediation owners, and the next rehearsal date. Backups are inventory; restore drills create confidence.
