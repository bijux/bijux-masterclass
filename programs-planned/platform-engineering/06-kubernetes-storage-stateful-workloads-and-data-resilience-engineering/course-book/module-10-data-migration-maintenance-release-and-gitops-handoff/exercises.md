# Exercises — Data Migration, Maintenance, Release, and GitOps Handoff

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Order an expand-and-contract migration

Atlas adds a new storage layout and schema while old readers remain. Give the safe phase order.

## 2. Choose a volume-migration strategy

Compare storage-native clone, snapshot restore, application replication, and offline copy for moving a database to a new class.

## 3. Cut over writer authority

What exact sequence prevents old and new database deployments from writing concurrently during migration?

## 4. Change a StorageClass safely

Why can’t an existing PVC simply switch `storageClassName`, and how should the change be represented?

## 5. Protect against GitOps pruning

A retained PV and snapshot are no longer referenced by the application directory. Why must GitOps not prune them automatically?

## 6. Define rollback after format change

A new database version writes an on-disk format the old version cannot read. What rollback remains possible?

## 7. Drain a stateful Node

Describe a safe maintenance drain for a Node hosting the current Atlas database writer.

## 8. Classify release evidence

Static manifests and semantic tests pass, but no CSI driver or restore drill ran. Can the data-plane release be accepted?

## 9. Handle a partial migration failure

Backfill reaches 80%, then the target backend becomes unavailable. What should the system do?

## 10. Make maintenance observable

Which events and metrics should a data migration publish without exposing sensitive data?

## 11. Write the Course 7 contract

What should the GitOps course receive from Course 6 as immutable handoff facts?

## 12. Defend Atlas Data Plane 1.0

Summarize the non-compensable gates for the final Course 6 release.
