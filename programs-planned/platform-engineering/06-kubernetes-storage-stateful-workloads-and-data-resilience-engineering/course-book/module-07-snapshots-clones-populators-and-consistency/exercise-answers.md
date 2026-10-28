# Worked answers — Snapshots, Clones, Populators, and Consistency

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Distinguish crash and application consistency

A crash-consistent snapshot captures storage state as though power stopped at an arbitrary instant. A journaling filesystem or database may recover it by replaying logs, but transactions across files or volumes may not align. Application consistency adds a coordinated recovery point: flush buffers, checkpoint, pause or sequence writes, snapshot the relevant volumes, then resume. It is required when the application’s own recovery protocol cannot guarantee a valid state from arbitrary storage timing or when multiple volumes must represent one transaction point. The snapshot record must label the achieved consistency honestly. “ReadyToUse” says the storage snapshot exists, not that the application can restore from it.

## 2. Design a group snapshot protocol

Acquire an application-level snapshot operation identity, confirm no conflicting backup or migration, request the database to checkpoint and quiesce writes, and record the resulting log/generation position. Create a VolumeGroupSnapshot covering both PVCs through a driver that supports the operation. Wait for all group content to become ready, record handles and deletion policy, then resume writes even if later export fails. If snapshot creation partially fails, preserve evidence and clean up through the controller. Restore into new claims, start the engine, and validate the recorded checkpoint. The group API coordinates storage operations; the application protocol establishes semantic consistency.

## 3. Interpret `readyToUse` correctly

It proves that the snapshot controller and CSI driver report a snapshot content object usable as a data source according to their API. It does not prove the source application was quiesced, all related volumes share one recovery point, the snapshot is independent of source failure domains, encryption keys are retained, a clone or restore will succeed, or the application can open the restored data. It may also be a thin copy dependent on source blocks. Required follow-up evidence includes consistency label, backend identity, restore into a new PVC, filesystem/engine recovery, domain validation, retention, and failure-domain mapping.

## 4. Choose clone, snapshot restore, or populator

A PVC clone can be fast and preserve storage-native efficiency but usually requires same driver/namespace constraints and copies sensitive data unless sanitization occurs later. A snapshot restore provides a retained recovery point and can create multiple claims, but shares snapshot failure and privacy concerns. A volume populator can build a new claim from an external data source through a controlled import/sanitization process, making provenance explicit, but adds a controller and lifecycle. The best path is a sanitized export/populator or separately produced sanitized snapshot, not direct cloning of production. The decision must include identity, access, deletion, cost, consistency, and proof that sensitive fields are removed.

## 5. Protect snapshot deletion

The namespaced VolumeSnapshot is a request/reference. VolumeSnapshotContent represents the cluster-scoped snapshot binding and backend handle. The snapshot class deletion policy determines whether deleting the request also deletes backend content or retains it. With `Retain`, the content and bytes can outlive the namespaced object and require inventory and later disposition. Finalizers protect in-use transitions but do not define retention. Operators must understand clones or backups that depend on the snapshot. GitOps pruning a request must not silently become data destruction. Deletion evidence should track logical source, physical handle, policy, dependents, key, and restore status.

## 6. Handle quiesce failure safely

It must prioritize resuming the application within a bounded freeze budget, even if snapshot status is uncertain. Record the operation identity and checkpoint, query the snapshot controller/backend for existing effects, and reconcile idempotently. If a snapshot exists, classify it and verify all members; if not, clean up partial content according to policy. Never leave the application frozen while retrying indefinitely. The runbook needs an abort timer, ownership for resume, and alerting. A later retry should create a new recovery point unless the original operation can be proven complete. Availability and data consistency are both part of the protocol.

## 7. Evaluate snapshot chains

The backend may preserve old blocks on every source write, increasing metadata work, latency, and capacity consumption. Deep chains can slow snapshot creation, clone, restore, deletion, or merge operations. If the pool fills, source writes can fail. The effect depends on the backend, so native metrics and tests are required. Retention should account for delta growth and flatten/export policies. Performance alerts should correlate snapshot age/count with source latency and queue depth. Read-only describes the consumer interface, not the absence of write-path cost or shared failure domains.

## 8. Preserve historical truth

Do not rewrite historical evidence to imply a stronger guarantee. Correct the catalogue with an append-only amendment that records the original claim, discovered limitation, affected snapshots, and current usability. If labels drive automation, block unsafe restores or require review. Create new application-consistent snapshots under the corrected protocol. Historical integrity matters during incident analysis and release decisions. Changing a record in place can make it impossible to know which recovery choices were made with which assumptions. A snapshot’s bytes are immutable; its interpretation can evolve, but that evolution must be auditable.

## 9. Secure snapshot access

A snapshot is a copy of storage, not a filtered API. Creating a PVC from it can expose all rows, deleted remnants, indexes, secrets, and historical data visible at that point. Read-only access is still confidentiality authority. Snapshot APIs, content objects, backend handles, KMS keys, and restore namespaces require least privilege and tenant isolation. Test environments need sanitization and distinct keys. Logs should not leak handles or signed URLs. Deletion and retention must respect legal requirements. Treat snapshot creation and restore as privileged data export operations, not ordinary developer convenience.

## 10. Design a restore test

Restore into a new PVC and new application identity, not over the source. Verify the restored volume’s handle, capacity, filesystem, and checksum or engine recovery. Start the application with outbound side effects disabled, confirm schema/version, replay logs, query sentinel data, and compare the recorded recovery point. Exercise a real read and, when safe, a write under a new generation. Measure elapsed phases and delete through the test retention policy. A successful PVC bind or Pod start is only an intermediate observation. The test should fail if it accidentally relies on source files, credentials, DNS, or network paths.

## 11. Explain why snapshots are not backups

It may share the source backend, account, region, credentials, and encryption-key hierarchy, so the same outage or compromise destroys both. Thin snapshots may depend on source blocks. Retention or garbage collection can remove them with the source. Application consistency may be absent, and restore may never have been tested. Snapshots are excellent for fast local rollback, clone, and backup staging, but a backup should export content and metadata into a failure domain chosen for the recovery objective. The recovery design should use both when appropriate and name which disaster each survives.

## 12. Decide if VolumeGroupSnapshot is required

Independent snapshots can be sufficient when volumes contain unrelated data, the application can reconstruct consistency from a transaction log or external checkpoint, or one volume is immutable. Group coordination is needed when a transaction spans volumes and recovery cannot tolerate arbitrary skew, such as separate data and WAL devices without a protocol that re-establishes one point. Even a group snapshot does not create semantic consistency unless the driver and application coordinate. The design should start from the recovery model, not the availability of an API. Record the exact Kubernetes and driver support because group snapshot APIs and implementations can differ by version.
