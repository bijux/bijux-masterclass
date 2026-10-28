# Module 10 — Data Migration, Maintenance, Release, and GitOps Handoff

> **Governing question:** How can storage classes, data formats, volumes, databases, and recovery systems change without losing authority, rollback options, or auditability?

## Why this module exists

A team changes StorageClass, database version, schema, and application image in one pull request. The workload rolls forward, the migration partially commits, and rollback starts an old binary against the new schema. Every individual artifact was valid; the release choreography was not.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- design online and offline data migrations
- separate schema, data, storage, and workload release ordering
- evaluate volume migration, clone, restore, and replication strategies
- perform maintenance without creating two writers
- define categorical release gates for the data plane
- produce an exact GitOps handoff with safe ordering and rollback boundaries

## Data changes have direction and irreversibility

Application binaries are often easy to replace; data transformations may not be. Adding a nullable column is usually more reversible than dropping a populated column. Rewriting a volume into a new format may require a full copy. Changing encryption or storage class can create a point after which the old volume is stale. Release planning identifies expansion, dual-read or dual-write, backfill, cutover, verification, and contraction phases.

The course uses explicit compatibility windows. Old and new application versions may coexist only when both understand the intermediate schema and data contract.
## Volume migration strategies

Common strategies include snapshot-and-restore, clone-and-cutover, application-level replication, backup-and-restore, filesystem copy, database logical replication, and storage-system migration. Each has different downtime, consistency, topology, cost, and rollback behavior. Kubernetes does not provide a universal “change StorageClass” operation for an existing PVC.

Atlas selects migration by data meaning. Immutable artifacts can be copied and verified by digest. Transactional state requires a quiesced or replicated cutover with a known commit point. Recovery copies must remain readable until the new path is proven.
## Maintenance needs authority and fencing

Node drain, volume detach, filesystem repair, snapshot rollback, database failover, and storage upgrade can all produce stale actors. The maintenance procedure must acquire authority, stop or fence writers, verify no outstanding mutation, perform the change, validate storage and application state, then release authority.

PodDisruptionBudgets limit voluntary disruption but do not make data maintenance safe. A force delete can bypass graceful shutdown. Atlas maintenance records the active fencing generation before and after the operation.
## Release gates are categorical

Atlas Data Plane releases must pass: predecessor integrity, manifest validity, storage-class policy, data-authority review, CSI capability evidence, snapshot and backup policy, empty-destination restore, migration compatibility, performance and capacity budget, security and network flows, and honest evidence classification. A strong average score cannot compensate for a failed restore or ambiguous writer authority.

Candidates can be accepted, rejected, review-required, or not-executed. Missing environment-backed evidence is not converted into a pass.
## Rollback stops at the data boundary

Application rollback is safe only while the data format and schema remain compatible. Storage rollback by replacing a volume with an older snapshot intentionally loses newer writes and must be treated as recovery, not deployment rollback. A failed migration may require forward repair rather than reversal.

The GitOps system in Course 7 must therefore consume rollback boundaries from Course 6. It may reconcile resources, but it cannot infer that an old desired state is data-safe.
## Course 7 handoff

The outgoing handoff includes immutable workload subjects, storage classes and service profiles, PVC and StatefulSet contracts, migration phases, backup and restore gates, maintenance authority, data SLOs, and evidence boundaries. It also names resources that GitOps must not prune automatically, including retained PVs, snapshot content, recovery manifests, and protected backups.

This makes delivery automation accountable to data reality. Git history becomes the desired-state record, not a magical undo log for bytes.

## Dual writes create a temporary distributed system

During migration, writing old and new stores appears to provide safety. It introduces partial failure, ordering, retry, and reconciliation problems. The application must define which store is authoritative, how divergence is detected, and how replay works. Without that design, dual writes make rollback less clear rather than more.

Atlas prefers source-controlled replication or an outbox-style change stream when possible. If dual write is unavoidable, each logical mutation has one identity and reconciliation report.


## Storage-class migration changes topology and operations

Moving from one storage class to another can change zone placement, attach behavior, encryption, snapshots, performance, and reclaim policy. A byte-identical copy is only one part of the migration. The new volume must satisfy the workload contract and the old recovery path must remain available until verification completes.

The migration dossier compares both classes and records the exact cutover generation.


## GitOps must distinguish apply from data action

A GitOps controller is good at reconciling declarative resources. Some data actions—backup validation, schema backfill, cutover, restore, and destructive cleanup—require one-time or externally observed procedures. Representing them as Jobs can make them visible, but retry and pruning semantics must be explicit.

Course 7 receives a list of ordinary reconcilable resources, protected retained resources, ordered migration actions, and manual approval boundaries.


## Final defense uses recovery, not screenshots

The final proof is an empty-destination restore and a defended release, not a collection of green object statuses. The learner must show where bytes came from, which generation was recovered, how stale writers were excluded, which evidence is local or native, and which risks remain.

A reviewer should be able to reproduce the decision from the dossier without access to the original terminal session.

## Worked semantic example

```python
from atlas_data.release import ReleaseEvaluator

result = ReleaseEvaluator().evaluate({
    "predecessor": "pass",
    "single_writer": "pass",
    "restore_drill": "pass",
    "migration_compatibility": "pass",
    "native_csi": "not-executed",
})
assert result.decision == "review-required"
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: atlas-schema-expand-2026-08
  namespace: atlas-system
spec:
  backoffLimit: 1
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrator
          image: registry.example.invalid/atlas/migrator@sha256:REPLACE
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| all-at-once release | schema and binary become incompatible | expand/backfill/cutover/contract |
| unsafe rollback | old binary reads new data format | rollback boundary |
| GitOps prune | retained recovery asset deleted | protected-resource policy |

## Atlas capstone increment

Atlas Data Plane 1.0 is released with a migration ledger, restore dossier, categorical evidence, retained recovery assets, and an exact delivery-plane handoff.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Course 7 begins by turning this safe ordering and evidence contract into reviewed GitOps reconciliation.

## Advanced design review — delivery state and data state evolve at different speeds

Git can declare a new workload immediately; authoritative data may require hours of backfill, catch-up, verification, and observation before writer cutover. Model the release as a durable process with phases and evidence rather than one atomic manifest sync. The Git revision can identify desired phase, but the data controller or operator owns progress and status.

Rollback also has several meanings. Reverting YAML can restore a previous Pod template while leaving schema, volume attributes, or on-disk format changed. The release dossier must say which phases support binary rollback, traffic rollback, writer rollback, or only restore from backup. A later course must not imply that Git history is data history.

## Final architecture defense

The final defense should walk one write from application acknowledgement through database generation, volume, snapshot, backup object, manifest, restore, and new writer fence. Then walk one destructive action and show why it cannot erase every recovery copy. Finally, identify every claim that remains environment-backed. This establishes a data plane that automation can safely consume without pretending that automation owns the data.

## Data changes require a control plane of their own

A declarative delivery controller is excellent at converging Kubernetes objects. Long-running data operations need richer progress, retry, pause, and verification state. Model them as custom resources, operator workflows, migration records, or external jobs with durable status rather than encoding every phase as manual comments in Git.

The delivery system can create the operation and observe its status. It should not repeatedly rerun a non-idempotent migration whenever reconciliation occurs. The data controller owns stable operation identity and knows whether a request is new, replayed, complete, failed, or conflicting. This separation lets Git remain the source of desired release intent without pretending that Git is the transaction log for the data.

## Decommissioning is part of migration

After cutover, old volumes, snapshots, routes, identities, and keys remain intentionally for a rollback window. Decommissioning needs its own inventory and evidence: no old readers or writers, recovery coverage on the new system, retained incident requirements, and data-owner approval. Resources should not linger forever, but cleanup should be a deliberate final phase rather than an accidental side effect of pruning.

Course 7 will automate promotion and cleanup. Its design quality depends on the precision of this handoff. A vague “do not delete data” rule is less useful than named protected resources, conditions for release, expiry, and the owner of irreversible action.
## Data migrations are ownership transfers

A migration changes more than bytes. It can transfer authority from one volume, database, storage class, region, or service to another. The central safety property is that exactly one history remains authoritative at every point—or, during a deliberately controlled overlap, that conflict resolution is explicit and tested.

A migration plan identifies:

- source and target identities;
- current authoritative generation;
- copy or replication mechanism;
- catch-up and verification method;
- write-freeze or dual-write policy;
- cutover condition;
- rollback boundary;
- old-copy retention;
- deletion authority;
- user-visible impact.

“Copy data, update PVC, restart” is not a complete plan.

### Common migration patterns

**Offline copy** stops writers, copies data, verifies it, and starts the target. It is conceptually simple and provides a clean cutover at the cost of downtime.

**Snapshot and catch-up** takes a base snapshot, restores it to the target, then applies logs or incremental changes until cutover. It reduces downtime but requires ordered change capture and replay.

**Replication and switchover** runs source and target together, catches up the target, fences the old writer, and promotes the new one. It requires protocol compatibility and strong authority controls.

**Application dual write** writes to both systems. It is often the most dangerous option because partial failure creates divergent histories. Use only with an explicit reconciliation model and durable operation identity.

**Read shadowing** sends reads to both systems and compares results while the source remains authoritative. This is useful evidence but does not validate target writes or failure recovery by itself.

### Verification must be semantic

Byte counts and checksums are valuable but insufficient for many data stores. Verification can include:

- object or row counts by tenant and partition;
- checksums or Merkle summaries;
- schema and collation;
- transaction or log position;
- referential integrity;
- application invariants;
- permissions and ownership;
- encryption and key access;
- representative read/write workflows;
- backup and restore from the new target.

The verification method should detect the failure modes of the migration mechanism. A logical export/import needs semantic checks; a block copy needs filesystem and database recovery checks.

### Cutover and rollback are asymmetric

Before cutover, rollback usually means discarding the target and continuing on the source. After the target accepts writes, rollback requires returning those writes to the source or declaring the target authoritative. The rollback boundary should be a named event, not a vague “we can switch back.”

A safe switchover often follows:

```text
copy and catch up
→ verify target
→ stop or fence source writes
→ confirm final position
→ promote target generation
→ redirect clients
→ verify critical journeys
→ retain source read-only
→ close rollback window
→ retire source deliberately
```

If any step is not observable, automation can continue through an unsafe state.

### Maintenance and storage-stack change

Course 6 also covers non-data migrations: CSI driver upgrades, sidecar updates, StorageClass evolution, volume-attribute changes, filesystem repair, Node maintenance, and backend migration. These changes can interact with in-flight provisioning, attachments, expansion, snapshots, and restores.

Maintenance policy defines:

- allowed concurrent operations;
- quiesce or drain requirements;
- disruption and quorum limits;
- mixed-version compatibility;
- evidence collected before and after;
- rollback capability;
- emergency stop conditions;
- communication and ownership.

A green DaemonSet rollout is not enough. Run representative lifecycle operations and verify existing mounted volumes remain correct.

### GitOps does not own irreversible data transitions automatically

GitOps is effective for declarative, convergent resources. Data deletion, restore, migration, and key retirement often require external evidence and human authorization. A controller that prunes a PVC or snapshot because it disappeared from Git may perform a technically correct reconciliation and a disastrous business transition.

Course 7 receives a handoff that distinguishes:

- resources safe for ordinary reconciliation;
- resources requiring retain or orphan semantics;
- one-shot migration intents;
- recovery actions that must never be auto-replayed;
- status and evidence needed before promotion;
- manual approval boundaries;
- rollback limits.

Git records desired state; it does not by itself prove data safety.

### Release gates are categorical

Atlas Data Plane 1.0 uses non-compensable gates. The release is rejected when any of these are missing:

1. data-class ownership and deletion authority;
2. compatible binding and topology;
3. verified CSI capabilities;
4. single-writer fencing where required;
5. application-consistent recovery strategy;
6. executed empty-destination restore at the claimed evidence level;
7. capacity and performance headroom;
8. migration and rollback boundaries;
9. monitoring and runbooks;
10. exact handoff to delivery automation.

A high average score cannot compensate for an untested restore or a possible stale writer.

### Final architecture defense

The learner’s final defense should walk one Atlas transaction through:

```text
application acknowledgement
→ authoritative storage mutation
→ CSI and volume lifecycle
→ snapshot or backup capture
→ loss of the primary environment
→ restoration into an empty destination
→ fencing and authority selection
→ application validation
→ traffic return
```

For each arrow, name the owner, durable identity, failure modes, evidence, and rollback limit. The defense should also identify what remains unproven without native cluster, driver, backend, cloud, or production evidence.

### Course 7 handoff

The outgoing handoff includes exact workload and data contracts, immutable identities, retention policy, migration boundaries, network dependencies, recovery gates, and resources that GitOps may or may not prune. Course 7 can then automate delivery without inventing data semantics or treating every Kubernetes object as safely disposable.
