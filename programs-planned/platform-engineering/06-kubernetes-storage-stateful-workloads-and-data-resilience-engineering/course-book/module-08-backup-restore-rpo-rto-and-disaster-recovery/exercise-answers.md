# Worked answers — Backup, Restore, RPO, RTO, and Disaster Recovery

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Calculate effective RPO

The schedule alone does not determine RPO. If the backup is 75 minutes old and only the next 20 minutes of logs are available, the recoverable point is roughly 55 minutes behind now, assuming the logs are complete, ordered, compatible, and restorable. If the log chain has a gap, loss may be 75 minutes or more. The drill must identify the last restorable generation, not the last Job timestamp. Effective RPO also includes detection and backup failure: repeated failed schedules can age the recovery point silently. Report the data generation or transaction position alongside wall-clock age.

## 2. Decompose RTO

RTO includes incident detection, decision and authority, environment provisioning, credential/key recovery, backup selection, data transfer, volume or service creation, restore, log replay, schema/application startup, domain validation, DNS/traffic cutover, and client recovery. A fast object copy may be a small fraction. Waiting for approval or discovering a missing key can dominate. Measure each phase during drills and define parallelizable work. The final clock stops when the service meets its agreed functionality and correctness, not when bytes finish copying. Course 7 automation can reduce provisioning and deployment phases, but it cannot invent missing recovery authority or verify domain correctness automatically without explicit oracles.

## 3. Design the backup manifest

Include logical dataset and tenant, source system/version, schema version, checkpoint or transaction generation, creation time, consistency type, file/object inventory, sizes and cryptographic digests, compression, encryption context or key reference, backup tool/version, predecessor/base chain, retention class, storage locations, and required restore procedure. Store the manifest in an independent catalogue and protect its integrity. Avoid embedding raw secrets. The manifest must be sufficient to detect missing or corrupt objects and choose compatible software. A collection of anonymous blobs is not a recoverable backup, even when every blob is durable.

## 4. Why restore into an empty destination?

An in-place restore can reuse surviving configuration, files, database pages, credentials, DNS, mounts, or metadata, allowing a broken backup to appear successful. It also risks overwriting the only source and makes rollback harder. An empty destination proves that the manifest and retained objects are complete and that provisioning, keys, software, and startup instructions work independently. The target should use a new volume or service identity and side effects should be disabled until validation. After restore, verify content digests and domain invariants. In-place recovery may be necessary during an incident, but periodic certification should use emptiness to expose hidden dependencies.

## 5. Include encryption keys in recovery design

The copy does not meet cross-account recovery because its decryption authority shares the source account failure domain. The bytes may survive yet remain unusable. Recovery design must retain or replicate key material and policy through a separately governed mechanism, with least privilege, rotation, revocation, and audit. The recovery principal should be tested without relying on source-account sessions. Key escrow or multi-region keys introduce their own security trade-offs and must follow organizational policy. The backup manifest references the encryption context but should not contain the key. A restore drill must prove the recovery identity can decrypt in the target environment.

## 6. Place copies across failure domains

Use local storage snapshots for fast rollback and clone within the source system, accepting that they share backend and administrative failures. Export backups to a repository independent of the source cluster and preferably a different zone or service boundary for routine recovery. For account compromise or regional disaster objectives, maintain an immutable or separately administered copy in another account and, when required, another region, with independent keys and catalogue access. Data residency, transfer cost, and restore time may constrain the design. Each copy should name the disaster it covers; “three copies” is meaningless if all share one credential or control plane.

## 7. Protect a point-in-time recovery chain

The chain cannot replay beyond the gap unless the engine provides another consistent base or branch. The recovery point is therefore before the missing segment, regardless of later logs. Monitoring should verify continuity and backup manifests should record sequence ranges and digests. Retention must keep a complete chain for every advertised recovery window. Garbage collection cannot consider objects independently; it must prove reachability from retained bases and targets. Drills should choose random points, not only the latest backup, and intentionally remove a segment to prove failure is detected rather than silently producing a partial database.

## 8. Garbage-collect deduplicated backup objects

One object may be referenced by many manifests. Deleting it because the newest backup no longer needs it can corrupt older retained backups. Garbage collection must begin from every retained manifest and traverse base, incremental, and object references, then delete only unreachable objects after a safety window. Holds, replication lag, and incomplete manifests must be considered. The reachability calculation and deletion plan should be versioned and reviewable. Content identity reduces storage and detects corruption, but it turns retention into a graph problem. A simple age-based lifecycle rule on shared objects is unsafe unless the repository guarantees reference-aware deletion.

## 9. Define domain validation after restore

Verify the recorded generation, schema version, constraints, sentinel records, row counts or object inventory, artifact references and digests, tenant boundaries, and a representative end-to-end workflow. Confirm no outbound webhooks, emails, or destructive jobs run in the isolated restore environment. Compare expected checkpoint/log position and ensure the current writer fence is new. File hashes prove transfer integrity but not logical consistency. The service owner defines these oracles because the platform cannot infer business truth from mounted bytes. The recovery report should retain both storage verification and domain verification results.

## 10. Assign drill authority

Those are separate authorities. An incident commander or designated recovery owner may initiate the drill; the data/service owner confirms the chosen recovery point and may accept loss within policy; security controls access to keys and target accounts; platform operators provision infrastructure; application owners validate correctness; traffic owners execute cutover after gates pass. Break-glass roles and approvals should be documented and tested. Automation can execute steps but should not silently choose a recovery point or accept data loss. The runbook records who made each irreversible decision and which evidence was available.

## 11. Reject backup-job success as proof

The job may omit objects, upload corrupt or truncated content, reference the wrong source generation, fail to persist the manifest, use an expiring key, or produce an application-inconsistent snapshot. The repository may share the source failure domain, and no compatible software or restore instructions may exist. Exit zero proves only the program’s own success criterion. The backup gate requires object digests, complete manifest, checkpoint/log identity, independent retention, key recoverability, and empty-destination restore with domain validation. Operational monitoring should alert on backup age and restore certification, not just Job failure count.

## 12. Design a regional disaster exercise

Use a target region and account that do not depend on the source region’s control plane. Recover identity, keys, network, DNS, compute, storage, backup catalogue, and application versions from independently retained artifacts. Restore a selected recovery point, verify domain invariants, test clients, measure each phase, and perform controlled traffic cutover or a non-production equivalent. Demonstrate that source-region unavailability is not bypassed by hidden API calls. Record actual RPO/RTO, cost, operator actions, and residual risks. A diagram or copy in another region is documentation evidence; executed classification requires the full usable service path.
