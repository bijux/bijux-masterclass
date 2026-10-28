# Worked answers — Data Lifetimes, Durability, and Storage Responsibility

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Classify the Atlas data

`run-state` is authoritative transactional data: one database authority writes it, and Node or zone loss must not destroy the acknowledged state. Immutable artifacts are authoritative after publication, but their writer can be a single publication workflow rather than a database transaction; deletion belongs to the retention owner. Worker scratch is non-authoritative and may die with the Pod, although it still needs quota. A read cache must be reconstructible and must not outlive authorization or source versions. Backup manifests are recovery authority: they must survive the source cluster and must be deleted only by the retention/recovery owner. The important result is not a storage product choice. It is a table that prevents one lifecycle or operator from silently owning every kind of byte.

## 2. Separate five different guarantees

The volume is persistent across container and Pod replacement because its lifetime is independent of those objects. Its durability depends on the backend’s acknowledgement and replication contract; a PVC alone proves none of that. Availability may be lost when the zone or attachment path fails even if every byte survives. Consistency is primarily the database engine’s responsibility: the volume cannot decide transaction order or prevent logical corruption. Recoverability depends on independently retained backups, keys, manifests, compatible software, and a tested restore path. A design review should therefore produce five distinct claims with separate failure domains and evidence. Collapsing them into “reliable storage” hides the exact condition under which the service fails.

## 3. Choose a lifetime deliberately

`emptyDir` is the best default when the data is Pod-scoped, reconstructible, and useful only while the worker runs. It avoids the provisioning, attachment, retention, and cleanup burden of a PV while allowing an explicit size limit. The container writable layer is harder to budget and observe, and its semantics are coupled to individual containers. A local or network PV extends lifetime without creating business value and can leave abandoned claims after retries. Object storage is appropriate for durable inputs and final outputs, not transient decompression work. The decision changes if recomputation is prohibitively expensive or the work must resume after Pod replacement; in that case the job protocol, not habit, should define a resumable durable checkpoint.

## 4. Explain why access mode is not writer authority

`ReadWriteOncePod` constrains Kubernetes-side use of a CSI volume so that one Pod is allowed to mount it read-write when the driver and cluster support the mode. It is valuable because it narrows one attachment/mount path. It does not revoke an old process that still has backend access, fence a stale VM, guarantee that a force-detach completed, serialize database transactions, or detect storage-system split brain. Writer authority still needs an application or infrastructure generation that every write path validates. The decisive test is to start a replacement writer, advance the fence generation, and prove that the old generation cannot commit even if it can still reach bytes. Access mode and fencing are complementary controls.

## 5. Define the acknowledgement boundary

The process must write all content, flush its user-space buffers, synchronize the file so the filesystem has accepted the data at the intended durability boundary, perform an atomic publication transition such as rename on the same filesystem, and synchronize the containing directory so the name transition is durable. It must also ensure that referenced artifacts are already durable and that the generation or transaction record tying them together is committed. These steps still establish only the local-filesystem evidence lane; host power-loss survival depends on filesystem, mount, device-cache, and storage-backend contracts. The response must not precede the last required transition. Otherwise a successful API result can refer to a name or bytes that disappear after crash.

## 6. Design deletion authority

Application retirement may remove the workload automatically, but it should not automatically destroy the authoritative claim or recovery chain. The PVC and PV should enter a retained, inventoried state. Snapshot deletion must account for dependent clones and the recovery window; retained snapshot content should require data-owner approval. Backup expiration may be policy-driven, but only after the repository proves that no retained manifest references the objects and that legal or incident holds are absent. Encryption-key destruction is an irreversible deletion event and requires separate authority. The evidence dossier should contain request identity, logical dataset, physical copies, dependency graph, approval, and post-deletion restore status. Separating authorities limits the blast radius of namespace deletion or a compromised delivery controller.

## 7. Evaluate a shared filesystem proposal

The design couples unrelated retention policies, so deleting scratch or pruning artifacts can threaten database or recovery data. It creates one performance and capacity failure domain: a snapshot chain, inode storm, or runaway scratch job can affect transactional latency. It erases authority boundaries because many Pods receive a path-shaped interface to data they should not mutate. It also weakens disaster recovery: a backup stored on the same filesystem shares the source’s administrative and storage failures. Finally, access modes do not provide transaction isolation or safe concurrent file semantics. Operational simplicity at the mount layer becomes ambiguity everywhere else. A better design separates data classes, then standardizes their interfaces, evidence, and lifecycle rather than forcing them onto one medium.

## 8. Decide whether local storage is acceptable

Local NVMe is defensible when the application or database owns replication across independent Nodes or zones, detects and repairs failed replicas, fences stale members, and can rebuild capacity without manual byte copying. The scheduler must preserve data locality, maintenance must respect quorum, backups must leave the Node, and the team must operate disk replacement and rebalancing. For a singleton database with no native replication, local storage turns Node loss into a recovery event and is usually a poor default despite excellent latency. The correct comparison is not local versus network as products; it is the complete data-service contract, including acknowledgement, failure domains, repair, RPO/RTO, capacity, and operator skill.

## 9. Turn requirements into a platform API

The request should identify the data class and authority, access pattern, writer model, consistency profile, failure-domain target, RPO, RTO, retention, deletion authority, encryption/residency constraints, expected growth, performance shape, and whether the engine manages replication. These fields let the platform select a StorageClass, managed data service, backup profile, quota, and review gate. `size` says nothing about write ordering, recovery, location, or who may destroy data. `fast=true` is worse: it encourages a tier label without workload evidence and can trade durability for latency invisibly. The API should offer curated profiles while keeping the underlying guarantees inspectable and refusing combinations the platform cannot honestly support.

## 10. Diagnose the disappearing result

Start with the application publication protocol. Determine whether the writer completed the artifact, verified its digest, synchronized it, atomically published the final name, and committed the result generation before reporting success. Then determine where the path lived: container layer, `emptyDir`, local volume, or durable store. A healthy replacement Pod says only that scheduling and startup succeeded. If the job record was on a different authority from the artifact, the system may have committed one side of a dual write. Kubernetes events become relevant after the data transition is understood: they can show Pod replacement or mount history, but not whether the application’s final bytes were complete. The earliest missing durable transition is the primary defect.

## 11. Build an evidence ladder

A semantic test rejects writes carrying a generation lower than the current fence. A local mechanism test persists the generation, restarts the process, and proves that the stale token remains rejected. A cluster test kills the active Pod, schedules a replacement, advances the generation, and attempts a stale write from a deliberately delayed old process. A storage-system test exercises real attach/detach or lease revocation under Node failure and verifies the backend’s observed writer. Operated proof includes repeated maintenance and failure drills, alerting on dual-writer indicators, and incident evidence over time. Each layer catches different defects; passing the semantic model does not prove a CSI driver or database deployment implements the same boundary.

## 12. Defend the Atlas data catalogue

Course 7 may reconcile desired resources, but it must preserve the distinction among authoritative state, immutable artifacts, disposable scratch, caches, and recovery evidence. It must not prune retained PVs, snapshots, backup manifests, or keys simply because they disappear from an application directory. Release ordering must preserve writer fencing, compatible readers, backfill identity, restore gates, and rollback windows. A Git commit is not deletion authority and a successful sync is not data correctness. The handoff therefore carries protected-resource rules, recovery gates, storage profiles, and explicit `not-executed` evidence. Automation is acceptable only when it makes those policies repeatable without silently broadening its authority.
