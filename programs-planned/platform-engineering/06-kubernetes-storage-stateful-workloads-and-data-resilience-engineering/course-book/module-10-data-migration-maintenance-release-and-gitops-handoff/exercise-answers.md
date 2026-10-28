# Worked answers — Data Migration, Maintenance, Release, and GitOps Handoff

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Order an expand-and-contract migration

First expand interfaces: create new classes/claims or schema fields without removing old ones. Deploy readers and writers that understand both representations, with writes carrying stable operation identity. Backfill historical data idempotently and verify counts, digests, generations, and lag. Establish replication or dual-read comparison before changing authority. Fence old writers, cut over one authoritative write path, and observe. Keep rollback possible while both formats remain readable. Only after old versions are gone and the rollback window closes should the system contract old schema, volumes, routes, or keys. Every phase has a named oracle and explicit stop condition.

## 2. Choose a volume-migration strategy

Clone or snapshot restore can be fast and preserve block-level state, but support, topology, consistency, and source dependencies must be verified. Application replication provides online catch-up and transaction-aware cutover but is engine-specific and operationally complex. Offline copy is simple and auditable but incurs downtime proportional to data size and verification. Choose based on RPO/RTO, engine semantics, volume size, topology, native capabilities, and rollback. Regardless of method, restore or copy into a new identity, validate content, fence writers, and preserve the source until the recovery window closes. A PVC spec edit is not a data migration.

## 3. Cut over writer authority

Establish a durable generation or lease authority shared by both paths. Prepare the target and catch it up while it is read-only. Quiesce or stop new writes briefly, record the final source generation, complete replication, advance the fence to the target, and verify the source rejects further writes. Then route write traffic to the target and validate. Keep the source retained but fenced for rollback. DNS or Service changes alone do not revoke existing connections. The cutover evidence includes source/target generations, fence transition, rejected stale write, routing change, and domain checks. If the fence cannot be enforced at the write path, the migration requires downtime and confirmed shutdown.

## 4. Change a StorageClass safely

The class participated in provisioning one backend volume with specific parameters and topology. Changing the field does not transform those bytes, and many PVC fields are immutable. Represent the change as a new class/profile and a data migration to a new claim or managed service. Record source and target identities, capability differences, copy/replication method, verification, cutover, rollback, and old-volume retention. If VolumeAttributesClass supports an in-place mutable attribute, treat that as a separately gated operation, not a class replacement. Desired-state tools must not delete and recreate a claim to force convergence.

## 5. Protect against GitOps pruning

Their absence from workload configuration does not mean the data owner authorized destruction. Retained PVs, snapshot contents, backup manifests, and recovery keys have lifecycles independent of the application release. GitOps controllers commonly treat absence as desired deletion, so protected-resource policies and separate repositories or ownership boundaries are required. Pruning may delete a namespaced snapshot whose class then deletes backend content, or remove a claim needed for rollback. Course 7 must encode retention and approval as platform policy, with inventory and eventual cleanup workflows. Convergence is subordinate to data authority.

## 6. Define rollback after format change

Application binary rollback is no longer safe once authoritative data crosses the format boundary. Recovery may require restoring a pre-upgrade backup or snapshot, accepting data loss after that point, or using a vendor-supported downgrade/export path. The release plan must mark the exact irreversible transition and require current restore evidence before crossing it. Keep old readers/writers out once incompatible data appears. A Deployment rollback command cannot reverse storage format. The decision belongs to the data/service owner and should be visible in Course 7 promotion gates.

## 7. Drain a stateful Node

Confirm service health, quorum or planned downtime, current backup, replacement capacity, storage topology, attachment slots, and PDB. Initiate engine/operator switchover or quiesce according to the data-service protocol, advance or preserve writer fencing, then evict. Observe endpoint withdrawal, detach/unstage, replacement attach/stage, recovery, membership, and readiness. Do not force the drain merely because a PDB blocks it; that may be correctly protecting availability. If the volume cannot move across zones or no replacement exists, maintenance becomes a scheduled outage or requires prior migration. The completion oracle includes one writer and correct data, not an empty Node.

## 8. Classify release evidence

Not as a production-supported storage profile. Static and semantic evidence can reject many unsafe designs and show intended transitions, but they cannot prove native provisioning, attachment, snapshots, expansion, backend durability, or restoration. The release may be `review-required` for a teaching or development lane with explicit limitations, or rejected if production depends on those capabilities. Record each unexecuted gate rather than replacing it with a mock pass. Acceptance requires the evidence class declared by the profile: native driver tests, backend evidence, and empty-destination restore for authoritative data.

## 9. Handle a partial migration failure

Stop or pause the backfill under its stable operation identity, preserve completed progress and checksums, and keep source writer authority unchanged. Do not cut over or delete partial target data. Diagnose target capacity/service, then resume idempotently or abandon through a documented cleanup that inventories target effects. If dual writes were enabled, verify divergence and rollback rules; ideally the source remained authoritative until final cutover. The migration plan should have predicted this state and defined whether target cleanup is reversible. Evidence includes last completed range, target objects, source generation, and absence of unauthorized target writes.

## 10. Make maintenance observable

Publish migration ID, source/target logical identities, phase, ranges or counts, bytes, lag, retry/failure class, current writer generation, verification result, and elapsed time. Use bounded labels such as migration type, service, phase, and result; keep raw object paths or tenant data in restricted logs. Emit durable phase transitions so operator restart does not erase progress. Correlate storage, application, and routing events. Avoid logging credentials, raw rows, backup URLs, or encryption material. The telemetry should answer whether the migration is progressing, safe to pause, ready to cut over, or needs rollback—not merely show process activity.

## 11. Write the Course 7 contract

It should receive version ledger, data catalogue, storage profiles, stateful workload identities, protected resources, release ordering, migration gates, restore requirements, network/security obligations, native evidence status, and known risks. It must know which resources may be reconciled normally and which require data-owner approval or staged workflow. The handoff preserves exact writer fencing and rollback boundaries. It should also identify mutable configuration versus immutable data identity and which resources are generated by operators. Without this contract, GitOps may fight controllers, recreate claims, prune recovery assets, or promote before restore evidence exists.

## 12. Defend Atlas Data Plane 1.0

The Course 5 handoff must verify exactly. Every data class must have authority, lifetime, deletion, RPO/RTO, and writer model. Storage binding and CSI lifecycle must be compatible with topology and workload. Authoritative writers require fencing; stale writes must be rejected after restart. Snapshots must state consistency honestly. Backups require complete manifests, independent retention appropriate to the target failure, and verified empty-destination restore with domain checks. Migration and class changes need ordered compatibility and rollback boundaries. Protected resources must survive GitOps pruning. Missing native or regional evidence is recorded, not implied. Performance and convenience cannot compensate for failed safety or recovery gates.
