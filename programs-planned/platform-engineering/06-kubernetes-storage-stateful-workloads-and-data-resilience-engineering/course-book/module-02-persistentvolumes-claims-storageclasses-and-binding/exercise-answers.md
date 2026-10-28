# Worked answers — PersistentVolumes, Claims, StorageClasses, and Binding

These are complete reference solutions. A different design is valid only when it preserves the same authority, failure, recovery, and evidence boundaries.

## 1. Name the authoritative records in binding

The PVC owns namespaced demand: capacity, modes, class, and sometimes data source. The PV owns the cluster-visible allocation identity and its one-to-one claim relationship. The StorageClass is policy and provisioner selection; it does not represent an individual allocation. The CSI backend volume is the physical or virtual effect identified by a stable handle. The application data remains business truth and may be valid or corrupt independently of every Kubernetes object. Diagnosis should trace the mapping PVC → PV → volume handle → backend object → filesystem/application state. A `Bound` PVC proves that the control plane associated objects; it does not prove attachability, mount success, freshness, consistency, or recoverability.

## 2. Explain delayed binding with a concrete conflict

A zonal volume is only accessible within its topology. Immediate binding chooses storage before the scheduler has selected a feasible Node, so the PV adds a hard zone-A affinity while the Pod has a hard zone-B requirement. The intersection is empty. Global free capacity is irrelevant because feasibility is per topology segment and per workload constraints. Manually prebinding another volume can make the state harder to unwind and may violate data identity. `WaitForFirstConsumer` lets scheduling constraints identify a feasible zone first, then provisioning occurs in that topology. The proof should preserve per-Node rejection reasons and the selected topology annotation, not merely observe that a later Pod happened to run.

## 3. Treat a StorageClass as a service contract

The class can promise a provisioner, delayed binding mode, reclaim policy, expansion permission, allowed topologies, volume mode expectations, and a documented service profile such as encryption or performance parameters. It should also state supported CSI capabilities and evidence status. It cannot promise application consistency, database replication, regional durability, restore success, or safe concurrent writers. Those depend on the engine, backend, backup system, and operational process. The name must not overclaim: “durable” requires a defined fault boundary. A mature platform publishes the class as a versioned service contract with capacity, cost, recovery, and deprecation rules rather than exposing an unreviewed bag of provider parameters.

## 4. Compare static and dynamic provisioning

Static provisioning is appropriate because the physical volume already exists and its identity must not be replaced by a new allocation. Create a PV with the exact backend handle, capacity, access mode, topology, and `Retain` policy, then bind through deliberate claim references or selectors. Verify that no other PV or claim can reference the same backend and that import does not format or initialize it. Dynamic provisioning is safer for ordinary new allocations because it standardizes naming and policy, but it is the wrong tool for adoption unless the driver provides an explicit import path. The migration must record source identity, pre-import backup, rollback, and post-bind application verification.

## 5. Analyze an idempotent provision retry

The retry must use the same stable request identity and parameters. The driver should discover or return the existing backend volume rather than allocate another. If the name exists with compatible capacity, topology, and capabilities, it returns the same volume handle. If the existing effect conflicts with the request, it fails explicitly rather than silently repurposing it. The controller then records one PV for that handle. Evidence includes the driver request name, backend object identity, repeated RPC result, and absence of a second allocation. Cleanup must distinguish an orphaned volume from a still-pending operation. “Retry the call” is not a complete strategy unless request identity and conflict semantics are specified.

## 6. Design claim deletion safely

The workload deletion and claim deletion are separate transitions. With `Retain`, the PV becomes released but the backend bytes remain; the platform inventories the logical owner, handle, snapshots, encryption context, and recovery status before any reuse or destruction. Rebinding requires deliberate cleanup and identity checks. With `Delete`, the provisioner may remove the backend after claim release; this is suitable only when the data class and environment authorize automatic destruction. Finalizers should prevent removal while controllers still need to finish cleanup, but they are not retention policy by themselves. StatefulSet claim-retention settings add another owner. The release design must define which deletion source is authoritative and how accidental namespace or GitOps deletion is contained.

## 7. Diagnose a Pending PVC without guessing

First identify the StorageClass and binding mode. If it is `WaitForFirstConsumer`, inspect whether a consuming Pod exists and whether the scheduler can select a topology. Read PVC and Pod events, selected-node annotations, class allowed topologies, and CSIStorageCapacity for the relevant segments. Verify provisioner registration and controller health, then inspect driver logs and backend quotas, volume-count limits, and API errors. Check selectors, data sources, access modes, volume mode, and requested size. Free bytes alone do not prove a compatible zone, class, attach slot, quota, or driver capability. Avoid deleting or prebinding until the earliest missing transition is known and retained data identity is protected.

## 8. Explain protection finalizers

Protection finalizers delay object deletion while a PVC is in use or while a PV remains bound, allowing controllers to complete safe lifecycle transitions. They prevent a Kubernetes object from vanishing before dependent use is resolved. They do not create backups, guarantee backend retention, validate application consistency, or stop an administrator from removing the finalizer or deleting the backend directly. A stuck finalizer is evidence that some owner has not completed its work, not an invitation to patch metadata immediately. Diagnosis should identify the responsible controller, current attachment/mount state, reclaim policy, backend object, and recovery consequences. Force removal is a break-glass action with an explicit data-owner decision.

## 9. Review access and volume modes

The workload contract and admission checks should reject it before scheduling. `Block` presents a raw device and requires the application to understand block semantics or format/mount it deliberately; it does not provide a filesystem path. `ReadWriteMany` is an accessibility request that the driver and backend must support, but it still says nothing about application concurrency. The StorageClass capability catalogue should make unsupported combinations impossible or review-gated. If the request reaches provisioning, the CSI driver must also reject incompatible capabilities rather than silently changing them. Evidence should show the requested volume capabilities, driver response, and application interface. Defaulting to “whatever the provider supports” produces hidden runtime mismatches.

## 10. Prevent unsafe prebinding

Confirm the PV’s backend handle maps to the intended logical dataset and no other active claim or process uses it. Verify capacity, volume mode, access modes, StorageClass, topology, filesystem, encryption key, and application/schema version. Confirm reclaim policy and claim reference state, remove stale claim references only through an audited import procedure, and restore or snapshot before mutation. Ensure the target Pod can schedule in the PV topology and that stale writers are fenced. The claim name alone is not data identity. A safe prebind is an adoption or recovery migration with evidence and rollback; it is not a generic cure for a Pending PVC.

## 11. Model multi-claim scheduling

Neither zone is feasible. Zone A lacks aggregate compatible capacity for both claims. Zone B has bytes but cannot attach two additional volumes to the candidate Node. The scheduler and binder must evaluate the claims as one workload placement problem rather than provisioning each independently in arbitrary zones. Partial provisioning can leave orphaned volumes and still fail the Pod. A stronger system reserves or serializes capacity transitions with stable operation identity and records which constraints rejected each Node. The correct response is not to provision one claim and hope; it is to preserve the all-required-volumes feasibility oracle and either choose another Node/topology or reject admission before creating physical effects.

## 12. Defend the Course 7 handoff

GitOps must preserve class identity, binding mode, topology constraints, claim names, data-source identity, access and volume modes, reclaim policy, StatefulSet claim-retention policy, and protected-resource lists. It must not recreate PVCs to “fix drift,” change a class on an existing claim as though it were ordinary configuration, or prune released retained PVs. Changes that require migration must use an explicit staged workflow rather than declarative replacement. The handoff should also carry unresolved native evidence: a manifest that says `WaitForFirstConsumer` does not prove the chosen driver publishes capacity correctly. Delivery automation can reconcile intent, but data owners retain authority over destructive transitions and migration cutover.
