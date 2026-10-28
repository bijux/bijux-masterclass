# Worked answers — Databases, Object Storage, and Operator Boundaries

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Choose managed service or in-cluster operator

A managed PostgreSQL service is the more defensible default if it can meet networking, identity, data residency, recovery, and cost requirements. Cross-region recovery and engine lifecycle demand expertise beyond Kubernetes object management. A managed service can reduce the team’s ownership of replication, patching, backup infrastructure, and failover, though it does not remove schema, query, access, or restore responsibilities. The decision should compare actual service contracts and exit paths, not assume “managed” means safe. An in-cluster operator is justified when control, portability, custom extensions, or disconnected operation outweigh the operational burden and the team can prove those capabilities.

## 2. Draw the responsibility boundary

Kubernetes owns generic object persistence, scheduling, and controller execution. The storage platform and CSI driver own volume lifecycle. The database operator owns engine-specific members, replication orchestration, backup hooks, failover, upgrade, and status according to its contract. The service team owns schema, transactions, query behavior, data meaning, and application-level recovery validation. The platform team owns supported operator versions, classes, security baselines, and cluster capacity. Backup storage and key owners have separate authority. Overlap must be explicit: an operator saying “backup completed” is one input, while the service owner validates a restored database. No layer should inherit responsibility merely because another team lacks access.

## 3. Choose object storage for artifacts

Artifacts have content identity, large sequential transfer, independent retention, and many readers. Object storage provides immutable-key patterns, checksum metadata, lifecycle rules, scalable reads, and a natural separation from transactional database I/O. Storing them on the database volume couples capacity, backup, restore time, and performance; a large artifact can delay database recovery. The database should store authoritative metadata and content digest, while publication writes the object and commits the reference through a safe workflow. Object storage is not automatically consistent or secure in every provider configuration, so the contract still defines overwrite policy, encryption, tenant authorization, deletion, replication, and verification.

## 4. Evaluate an operator status condition

Not for the service contract that requires that RPO. Operator conditions express the controller’s own model and may use a threshold different from the application. Read the condition reason, observed generation, member roles, lag metrics, backup status, and application readiness policy. The platform may add a service-level gate that requires operator readiness plus bounded lag, current fence, and recent restore evidence. Do not patch the operator’s status or duplicate its reconciliation logic; compose its observations into a separate service decision. A generic `Ready` condition is useful only when its semantics are documented and match the consumer’s requirement.

## 5. Keep database credentials out of the storage layer

Application workloads receive database credentials or workload identity limited to their schema and operations. The database/operator receives engine and backup authority appropriate to replication and export. The backup component can read a consistent backup stream and write to a dedicated repository but should not provision volumes. CSI controller and node components receive backend storage authority without database credentials. KMS access is split so runtime decryption, backup encryption, and recovery can be governed separately. Operators and GitOps controllers should not receive all credentials by convenience. This separation prevents a compromised workload or delivery system from deleting volumes, decrypting every backup, and altering database state through one identity.

## 6. Plan an operator upgrade

Record the current CRDs, stored versions, conversion behavior, operator image, engine versions, custom resources, backups, and active operations. Verify the upgrade path and version skew, test CRD conversion and rollback in a disposable environment, and confirm that the old operator can still understand stored objects during the rollback window. Pause conflicting maintenance, take and restore a current backup, and protect finalizers and child resources. Observe reconciliation after upgrade without forcing ownership of fields managed by another controller. The release is not complete when the Deployment is Available; it is complete when database membership, replication, backup, restore, and application queries remain correct.

## 7. Reject a false HA claim

The Pods may not replicate, may all be writable, may share one Node or zone, and may have independent data. No leader election, quorum, fencing, synchronous commit, failover, or client routing behavior has been established. Even with replication, storage and backups may share a failure domain, and recovery might require manual action beyond the target RTO. The chart must identify an engine or operator protocol, membership, failure-domain placement, readiness, PDB, capacity, backup/restore, and tested failover. Replica count is an input, not an availability result. The honest label for three unmanaged Pods is “three processes,” not an HA database.

## 8. Compare filesystem and object semantics

Not without an adaptation layer whose semantics and failure modes are explicit. Object stores generally expose keys rather than directories, may implement rename as copy-plus-delete, and do not provide POSIX advisory locking. Listing and overwrite consistency depend on the service contract, and multipart upload introduces incomplete-object lifecycle. A filesystem gateway can emulate some behavior but becomes a stateful component and may not preserve atomicity. The application should be changed to immutable object publication and metadata-based coordination when possible. If compatibility requires RWX, treat it as a bounded legacy profile and avoid claiming object-store durability or scale automatically transfers through the gateway.

## 9. Design a database backup oracle

Verify the backup manifest, source database identity, checkpoint or log position, schema/version, object inventory, encryption context, and retention. Restore into a fresh database and storage identity without reusing surviving files or credentials. Start the target engine, replay logs, run consistency checks, query sentinel records, compare expected counts/generations, and exercise a representative application workflow. Record elapsed phases and whether RPO/RTO were met. A completed Job proves only that the backup process exited successfully under its own criteria; it cannot prove every object was retained, keys will be available during disaster, or the restored application is correct.

## 10. Plan service exit and portability

Maintain an engine/version inventory, schema migrations, logical and physical export options, backup formats, key ownership, network dependencies, extension use, size and transfer estimates, and a tested restore into an independent environment. Avoid provider-specific features unless their value and exit cost are explicit. Document DNS and credential cutover, writer fencing, replication or downtime strategy, and rollback boundaries. Portability does not mean lowest-common-denominator design; it means the consequences of dependency are measurable and an exit path exists. A migration that has never been tested is not an exit plan.

## 11. Handle an operator outage

Existing engine processes may continue serving because the operator is a control plane, not the data path. Reconciliation, failover, backup scheduling, certificate rotation, scaling, and status updates may stop. Do not restart healthy database Pods merely to “make the operator notice”; that can convert a control-plane outage into data unavailability. Restore the operator, inspect its queue and observed generation, and verify no conflicting human changes occurred. Alerting should distinguish operator unavailable from database unavailable while still treating prolonged loss as risk. The recovery oracle includes resumed reconciliation and backup/failover capability, not only an Available operator Deployment.

## 12. Produce a data-service decision record

It should state workload and data semantics, availability and recovery objectives, regions, identity and network boundaries, encryption and key control, backup/restore evidence, engine features, performance/capacity, maintenance, upgrades, observability, cost, support, compliance, exit path, and residual risks. Compare alternatives against the same criteria. Name responsibility after the decision: managed service does not own schema or application correctness, and the platform still owns connectivity and access. Record evidence class for each claim and conditions that would reopen the decision. The document should enable later Course 7 automation without hiding provider-specific manual steps or broadening delivery authority.
