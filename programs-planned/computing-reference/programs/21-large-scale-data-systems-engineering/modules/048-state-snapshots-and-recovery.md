---
module_id: LSDS-048
program: Large-Scale Data Systems Engineering
level: 1
module_number: 48
title: State Snapshots and Recovery
status: complete
last_verified: 2026-09-04
---

# State Snapshots and Recovery

## One-Page Review

### Governing question

How can a large-scale stateful dataflow turn a consistent checkpoint cut into durable, compatible, integrity-checked state and then restore service within declared data-loss, correctness, latency, capacity, security, and regional objectives?

### Essential definitions

- A **logical snapshot** is an immutable view of state, timers, source positions, and required channel/effect metadata at one consistent cut.
- A **snapshot manifest** is the atomically published root that names checkpoint identity, topology/code/schema versions, component handles, sizes, hashes, encryption metadata, and dependencies.
- A **full snapshot** materializes a self-contained representation of all required state for its scope.
- An **incremental snapshot** stores changed/new objects and references objects shared with earlier snapshots; it is complete only through its dependency closure.
- A **changelog snapshot** combines a materialized base with an ordered durable mutation log that is replayed to the cut.
- **local recovery state** is a performance copy near a prior task placement; the fault-independent primary remains recovery truth.
- A **standby/warm replica** continuously or periodically restores state to reduce activation time at additional resource cost.
- **recovery point objective (RPO)** bounds acceptable lost durable progress; replayable inputs may reduce logical data loss even when the snapshot is older.
- **recovery time objective (RTO)** bounds time to restore the service/contract, including detection, scheduling, state load, replay, catch-up, and effect reconciliation.
- A **restore drill** actually reconstructs and validates a job from retained artifacts; successful snapshot creation alone is not restore evidence.

### Central model, mechanism, or theorem

Let completed snapshot $n$ have manifest

$$M_n=(id_n,top_n,code_n,schema_n,P_n,S_n,T_n,Q_n,E_n,D_n),$$

where $P$ are source positions, $S$ operator state handles, $T$ timers, $Q$ channel state, $E$ effect/transaction metadata, and $D$ the transitive object-dependency graph. Restore is admissible only if the manifest is completed, authentic, integrity-valid, policy-allowed, and compatible with the target code/topology—or an explicit migration exists.

End-to-end recovery time is approximately

$$RTO_{actual}=t_{detect}+t_{coordinate}+t_{schedule}+t_{fetch}+t_{verify}+t_{decode}+t_{replay}+t_{catchup}+t_{reconcile},$$

with critical-path/tail behavior rather than sum of averages. An incremental snapshot that writes few bytes can still restore slowly if it reads a long dependency chain or replays a large changelog. Garbage collection is safe only for objects unreachable from every retained/claimed snapshot and active restore.

### Critical invariants

- Only atomically completed manifests are eligible for normal recovery; directory presence and task-local success are insufficient.
- Every referenced object is immutable or content-addressed, length/hash verified, decryptable, and reachable for the retention horizon.
- Incremental dependency closure is retained and reference/liveness accounting includes active creation, restore, legal hold, fork, and rollback.
- Restore uses source positions, operator state, timers, channel state, and effect metadata from one checkpoint identity.
- Operator UID, state name, key/namespace encoding, serializer/schema, key-group mapping, code/time semantics, and runtime format are compatible or migrated.
- Every state shard/key group has exactly one eligible restored owner before processing/effects resume.
- Local state and caches may accelerate restore but never replace a complete fault-independent primary unless their durability is explicitly sufficient.
- Corrupt or unavailable newest snapshots fall back only to verified compatible older points, with added replay/RPO/RTO assessed.
- Restore/catch-up has reserved CPU, memory, disk, network, storage-request, source-retention, and sink capacity.
- Secrets and governed data remain protected through snapshot, replica, backup, restore, inspection, export, and deletion.

### Common failures

Common failures include treating a successful upload as a completed snapshot; choosing the newest directory rather than newest valid compatible manifest; deleting a shared base referenced by incremental descendants; validating only manifest hashes but not object bytes; retaining encrypted state after losing keys; assuming local SSD is durable primary; measuring snapshot write time as RTO; sizing restore from average throughput; restoring state with different source positions; ignoring timer/channel/sink metadata; changing operator/state IDs or key encoding; letting rescale omit or duplicate key groups; restoring corrupt newest state without fallback testing; starting sources before fencing old owners; underprovisioning catch-up; and never performing a production-scale restore drill.

### Compact example

Completed snapshot C1 references 120 MB base object. An incomplete C2 references the base plus a 30 MB delta. Completed C3 references the base plus a distinct 20 MB delta. Recovery selects C3, reads 140 MB, and never infers C2 from its files. If retention keeps C1 and C3, the base and C3 delta remain live; C2's unreferenced delta can be reclaimed only after confirming no active writer/restore/hold uses it. A 20 MB incremental write therefore does not imply a 20 MB restore.

### Connections

[LSDS-047](047-checkpoint-barriers.md) proves the consistent cut; [LSDS-043](043-stateful-operators.md) defines the state being preserved. [LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md) supply replay positions/ownership. [LSDS-049](../ROADMAP.md) explains backpressure/catch-up, and [LSDS-050](../ROADMAP.md) completes effect-safe reprocessing.

## Governing Question

A correct checkpoint barrier identifies which state belongs together, but recovery still depends on physical artifacts. State may be split across millions of objects, encrypted with rotating keys, incrementally shared across checkpoints, stored in a remote region, cached locally, and encoded by a serializer that the new binary no longer understands. A manifest can exist while one referenced object is missing or corrupt.

Restore is also a workload, not a file copy. Workers must be scheduled, state mapped to new owners, objects fetched and verified, databases opened or heap graphs decoded, channel/timer state reconstructed, sources rewound, changelogs replayed, and accumulated input caught up. External transactions and ambiguous effects must be reconciled before visible service is correct.

The fastest snapshot can be the slowest recovery. Incremental checkpoints reduce write traffic but may create dependency chains and many small reads. Local copies accelerate process failures but disappear with a node. Standbys reduce activation latency while consuming near-live resources. Cross-region durability improves disaster tolerance but adds cost, lag, residency, and key-management obligations.

The governing question is how to select representations and retention from recovery evidence, preserve compatibility and integrity throughout the dependency graph, and rehearse the complete restore until actual tail behavior satisfies the contract.

## Why This Matters

Recovery artifacts are the last defense when a worker, cluster, zone, region, deployment, or operator action fails. If snapshots cannot be restored, every upstream durability promise becomes irrelevant. If restore takes longer than source retention, replayable data expires before catch-up and a recoverable incident becomes data loss.

Large state magnifies tails. One slow object store prefix, hot key-group, corrupt block, missing encryption key, or memory-heavy decoder controls the critical path. Aggregate read bandwidth can look excellent while one task takes an hour. Scheduling may place all restore traffic behind production workloads exactly when spare capacity is most needed.

State also accumulates sensitive history. Snapshots outlive local TTL cleanup, replicate across regions, and can preserve deleted values in shared incremental objects. A backup retention policy must align recovery, legal hold, privacy deletion, key destruction, and dependency safety.

Operational confidence comes from drills. Listing “five recent checkpoints” does not show that their manifests are complete, dependencies reachable, binaries compatible, credentials valid, capacity available, outputs fenced, or recovered results correct.

## Prerequisites and Retrieval

Review checkpoint identities, aligned/unaligned cuts, completion publication, channel state, and sink coordination in [LSDS-047](047-checkpoint-barriers.md). Retrieve state scopes, backends, TTL, rescaling, and migration from [LSDS-043](043-stateful-operators.md); storage replication/integrity/lifecycle from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md); and source replay/assignment from [LSDS-041](041-logs-as-distributed-input.md) and [LSDS-042](042-partitioned-consumption.md).

You should understand immutable manifests, content hashes, dependency DAGs, reference counting/mark-and-sweep, full/incremental snapshots, WAL/changelogs, serializers, key groups, epochs/fencing, RPO/RTO, tail latency, source retention, transactions, encryption keys, and failure domains.

## Learning Objectives

After this module, you should be able to:

1. distinguish logical checkpoint cut, snapshot representation, primary/local copy, manifest completion, and restore;
2. design a self-describing immutable manifest with transitive dependency and integrity metadata;
3. compare full, incremental, changelog, local, standby, and disaggregated recovery strategies;
4. select the newest valid compatible recovery point and fall back safely on corruption/unavailability;
5. validate compatibility across operator/state identity, schemas/serializers, keys, topology, runtime, time, and effect semantics;
6. redistribute state shards/key groups exactly once during rescale or topology replacement;
7. estimate RPO and end-to-end RTO including detection, scheduling, load, replay, catch-up, and reconciliation;
8. retain and garbage-collect snapshot objects without breaking shared dependencies, active restores, forks, or holds;
9. protect credentials and governed state across failure domains, regions, exports, deletion, and incident access; and
10. execute restore drills that verify state/results, performance, rollback, and downstream effects.

## Core Exposition

### Separate logical and physical snapshots

The barrier protocol freezes a logical version. The backend encodes it into files, objects, changelog ranges, pages, or database handles. Logical equivalence does not require byte-identical encoding, but every physical representation must restore the same qualified state.

Document live backend, primary checkpoint storage, optional local copy, incremental base objects, changelog, standby, and archive roles. “RocksDB state,” for example, may mean a live local database, native checkpoint files, remotely uploaded SSTs, or a restored copy; these have different durability.

Snapshot format is an API between old writers and future readers. Version and test it.

### Publish a self-describing manifest

The manifest records checkpoint/job/materialization ID; creation/completion times; source positions; topology and stable operator/state IDs; key groups/parallelism; schema, serializer, code/runtime, time and configuration versions; state/timer/channel/effect handles; object length/hash/compression/encryption/key ID; dependencies; region; and retention/ownership.

Keep the root small enough to validate before allocating massive restore resources. Sign or authenticate it and make completion publication atomic. Component files without the root are candidates/orphans, not automatically a checkpoint.

Use immutable or content-addressed objects so a retained manifest cannot silently point to mutated bytes.

### Validate dependency closure

An incremental manifest can reference prior immutable base files plus new deltas. Restore traverses a DAG, not necessarily a simple parent chain. Validate acyclicity where required, object uniqueness, lengths/hashes, encryption keys, and reachability before declaring ready.

Reference counts are easy to race with snapshot creation, restore, fork, and deletion. A mark-and-sweep design can mark from every completed retained/claimed manifest plus active operation roots, then delete only unmarked objects after a safety grace and recheck.

One missing shared object can invalidate many descendants. Track blast radius and periodically compact/materialize independent bases.

### Choose full snapshots deliberately

A full snapshot contains the entire logical state for its scope without relying on prior checkpoint objects. It simplifies restore dependencies, portability, retention, and forensic copying. It moves all state on every creation and can saturate CPU, network, storage, and request quotas.

Full does not mean one file or instantly restorable. It may contain many shards, and all still need integrity, compatible decoders, key-group mapping, and source/effect metadata. Compression trades bytes for CPU and may increase time-to-first-restored shard.

Schedule occasional independent full bases if incremental chain risk exceeds write savings.

### Choose incremental snapshots deliberately

Incremental snapshots reuse unchanged immutable backend files/pages and upload only new content. They reduce steady write bytes when churn is low relative to total state. High compaction or broad rewrites can make deltas approach full size.

Restore bytes are the union of referenced objects needed for assigned shards, not the last delta size. Many small objects add listing/request/connection overhead; long dependency chains complicate retention and verification. Backend-native formats can constrain runtime/backend downgrade.

Measure logical state, newly uploaded bytes, total referenced bytes, unique retained bytes, object count, sharing factor, and restore read set separately.

### Use changelogs with bounded replay

A changelog persists state mutations continuously or between materializations. Recovery loads a base and replays ordered changes to a recorded position. Frequent bases reduce replay; sparse bases reduce snapshot writes.

The changelog needs durable ordering, integrity, compaction/tombstone semantics, schema compatibility, and alignment with source/state positions. Replaying a mutation twice or skipping one corrupts state unless operations are idempotent and identity-preserving.

Bound log bytes and replay time from update rate and materialization interval. A fast checkpoint that merely records a log position can shift cost into recovery.

### Treat local recovery as a cache

Keeping snapshot files on the former worker can avoid remote reads when a task is rescheduled there. It is valuable for process/container failures and large keyed state. Node/disk/zone loss removes the copy, and rescaling may move ownership.

The primary fault-independent snapshot must be complete before global acknowledgment under this model. Validate local copy identity/hash and fall back transparently to primary on mismatch. Do not let local success mask primary failure.

Budget local disk, cleanup, security, multi-tenant isolation, and scheduling affinity without making recovery depend on best-case placement.

### Evaluate standby and disaggregated state

Standbys continuously restore changelog/snapshot updates so activation reads little. They improve predictable failover if lag is bounded and placement avoids correlated failure. They consume compute, storage, network, and coordination even when idle.

Disaggregated/remote state can make compute replacement lighter because authoritative state is already remote, but live access, cache warming, network failure, service quotas, consistency, and cost become central. A cache must be rebuilt or validated.

Choose by failure frequency, RTO tail, state size/churn, network/storage characteristics, tenancy, and cost—not by architecture fashion.

### Select a recovery point safely

Enumerate only atomically completed manifests. Filter by job/materialization, topology/application compatibility or approved migration, policy/region, available keys, and required source/sink reachability. Verify manifest authentication and dependency closure before selecting the newest candidate.

If validation fails, quarantine the candidate and try the next older compatible completed point. Quantify added replay and whether source retention still covers it. Never silently skip incompatible state or corrupt channel data to achieve a green restart.

Manual selection requires two-person/high-risk controls where financial, safety, or regulated state is involved.

### Restore in controlled stages

Fence old attempts and pause/coordinate sources and effects. Allocate target resources, map state shards, fetch primary/local objects, verify/authenticate/decrypt/decompress, decode/migrate, open live backends, restore timers/channel data, and load source/effect metadata.

Run structural and semantic validation before exposure: counts, key-group coverage, hashes, invariants, sampled records, state versions, transaction status, and source positions. Then resume replay, reconcile ambiguous effects, catch up, and gradually restore traffic.

Keep rollback artifacts and the old deployment until cutover evidence is sufficient. A process reaching “RUNNING” is not recovery completion.

### Preserve exactly-one state ownership

Map stable key groups/shards rather than arbitrary serialized files to target tasks. Every required group maps to exactly one eligible owner; none is omitted or duplicated. Validate total counts/bytes/checksums and tenant/region placement before source consumption.

Operator/list/union/broadcast state has redistribution rules distinct from keyed state. Timers and window namespaces follow their keyed ownership. Channel state may impose topology/parallelism compatibility constraints.

Fence stale owners and effect writers with epochs. Two successfully restored owners are worse than none if both emit.

### Prove compatibility

Compatibility includes operator UID and state name, serializer snapshot and old-byte readability, state schema/business semantics, key/namespace encoding, partitioner/max parallelism/key groups, timer/window/watermark rules, code/runtime/backend format, and sink transaction/effect identity.

A field addition can be serializer-compatible but semantically wrong if its default is ambiguous. A key change can merge/split identities and requires export/rekey/merge or source replay. Operator rename can orphan state. Backend or runtime downgrade may not read newer files.

Test production-derived bytes in both upgrade and rollback directions. Record explicit migration and loss/skip decisions.

### Restore timers, watermarks, and channel state

Timers belong to keyed/namespace state and may be overdue at restore. Processing timers can bunch immediately; event timers depend on restored/regenerated watermarks. Callbacks and panes need stable effect identity.

Unaligned channel state must be restored in correct input/output order and topology without duplication. Ignoring corrupt channel state is an explicit data-loss/semantic action, not routine repair.

Watermarks are not interchangeable with checkpoint positions. Test runtime-specific recovery ordering for operators that depend on current watermark.

### Reconcile sources and sinks

Rewind each replayable source to the position in the chosen manifest. Verify retention, topic/file/table identity, partition epochs, permissions, and that offsets still name the same data. If inputs were compacted/deleted, snapshot validity may have expired despite intact state files.

Resolve prepared/committed/aborted sink transactions for the checkpoint. Fence old producers. Idempotent sinks retain dedup keys through the maximum replay horizon. Ambiguous external calls require query, ledger, compensation, or manual review.

Resume sources only after state ownership and output fencing are established.

### Model RPO precisely

Snapshot age is not automatically data loss. With durable replayable input and deterministic state, records after the checkpoint can be recomputed, so logical RPO may be zero while recovery work grows. Nonreplayable input or uncoordinated external decisions can be lost.

Define RPO separately for managed state, source availability, emitted results, external effects, and operational telemetry. Include the last successfully completed—not merely triggered—checkpoint and replication lag for regional failures.

Retention horizon must exceed detection, restore, replay/catch-up, investigation, and safety margin.

### Model end-to-end RTO

Measure detection, coordinator election, resource scheduling/image pull, credential/key access, manifest/dependency validation, bytes fetched, verification/decryption/decompression, backend open/deserialize, channel/timer reconstruction, source/sink reconciliation, replay, catch-up, validation, and traffic cutover.

Use critical-path p95/p99/max by shard, not total bytes divided by aggregate peak bandwidth. Storage request limits, hot objects, skewed groups, memory/compaction, and source/sink throttles control tails.

Recovery completes when service meets its correctness and freshness contract, not when processes start.

### Provision catch-up headroom

If input arrives at rate $\lambda$ and recovered processing capacity is $\mu>\lambda$, a backlog $N$ has ideal catch-up time $N/(\mu-\lambda)$. At $\mu\le\lambda$, catch-up never converges without throttling, dropping, or added capacity.

Include restore I/O and cache/compaction warming, which reduce effective $\mu$. Coordinate upstream retention and downstream write quotas. Prioritize critical tenants/partitions only under an explicit fairness/correctness policy.

Autoscaling itself may trigger state movement; reserve capacity and stable maximum-parallelism/key-group plans before an incident.

### Retain and garbage-collect safely

Retention keeps multiple recent compatible checkpoints, independent bases, pre-upgrade rollback points, and disaster-recovery copies according to RPO/RTO, audit, legal hold, and source retention. More snapshots do not help if all share one corrupt base or key.

Garbage collection starts from retained manifests, active jobs/restores, forks, claims, and holds; computes transitive reachability; applies grace; rechecks; and deletes with audit. Snapshot ownership/claim mode decides whether a restored job may later delete its source artifacts.

Test deletion on dependency graphs and concurrent operations. Monitor orphan and unreachable bytes without blindly deleting unknown objects.

### Engineer regional disaster recovery

Place the primary outside the worker/node failure domain. For zone/region failure objectives, replicate manifests, objects, encryption keys, code/images, configuration, schemas, source access, and sink coordination to an allowed destination.

Replication completion must be manifest-consistent; copying the root before all dependencies creates a remote phantom. Measure lag and select only region-complete points. Validate DNS/control-plane/identity dependencies that share the failed region.

Residency may forbid cross-region state. Then document a different failure objective rather than silently violating policy.

### Secure snapshots and recovery

Encrypt in transit/at rest; rotate keys without making retained checkpoints unreadable; separate backup keys/roles; use short-lived restore credentials; sign manifests; verify hashes before decoding; and sandbox parsers/migrations for untrusted/corrupt bytes.

Least privilege covers create, list, read, restore, export, inspect, retain, claim, and delete. Restores can expose historical deleted data, so authorize purpose and destination and audit access.

Redact secrets from state where possible. Secure local copies, standbys, temporary downloads, crash dumps, metrics, and deletion workflows, not only remote objects.

### Observe recovery readiness

Track completed snapshot age, logical/full/incremental/unique/referenced bytes, objects/dependency depth, shared-object fan-out, upload/read throughput, hash/key validation, local-copy coverage, standby/changelog lag, retention/GC/orphans, and source-retention margin.

For drills/incidents track every RTO phase, per-shard critical path, fallbacks, corrupt/missing objects, bytes/requests, decode/open time, key-group placement, replay backlog/rate, catch-up ETA, timer bursts, sink reconciliation, freshness, and semantic validation.

Alert on absence of recent restore-tested compatible points, not only failed checkpoint creation.

### Drill recovery and rollback

Regularly restore a production-scale recent checkpoint and an older independent fallback into isolated infrastructure using the actual binary, credentials, keys, topology, source/sink controls, and regional constraints. Prevent the drill from emitting real effects.

Verify counts, hashes, domain invariants, key-group coverage, timers, sampled state, deterministic replay, output diffs, performance, cleanup, and rollback. Inject missing/corrupt objects, unavailable local state, lost keys/credentials, cold capacity, throttling, schema changes, and regional dependency loss.

Record measured RPO/RTO and remediate gaps. A runbook read-through is not a restore drill.

## Definitions and Notation

For completed checkpoint $n$, $M_n$ is the manifest root; $P_n,S_n,T_n,Q_n,E_n$ are source, operator, timer, channel, and effect components; $D_n$ is the object dependency graph. Let $Reach(R)$ be the transitive object set reachable from manifest roots/active-operation roots $R$.

An object is garbage-collection eligible only if it is outside $Reach(R)$ after grace/recheck and no external ownership/hold applies. A snapshot's incremental write bytes $\Delta_n$ can be much smaller than restore read set $|Reach(\{M_n\})|$.

Let $t_d,t_c,t_s,t_f,t_v,t_x,t_r,t_u,t_e$ denote detection, coordination, scheduling, fetch, verify, decode, replay, catch-up, and reconciliation durations. Actual RTO is their dependency-aware critical path, approximated additively only when stages are serial.

If failure occurs $A$ seconds after the last completed snapshot at input rate $\lambda$, replay backlog begins near $N=\lambda A$ records (plus queued/channel/source effects). With sustainable catch-up capacity $\mu>\lambda$, ideal catch-up is $N/(\mu-\lambda)$.

## Mechanisms, Invariants, or Proof Structure

Audit state recovery in this order:

1. **Cut identity:** confirm source/state/timer/channel/effect components belong to one completed checkpoint.
2. **Manifest:** verify atomic completion, authentication, immutable handles, lengths/hashes, formats, encryption keys, region, and ownership.
3. **Closure:** traverse incremental/changelog dependencies and prove every object/range is reachable, ordered, durable, and retained.
4. **Compatibility:** test operator/state IDs, old bytes, schemas, keys, partitioning, timers/time, topology/runtime, and sink semantics.
5. **Placement:** map every keyed/operator/broadcast/channel shard exactly once with fencing and policy-compliant location.
6. **Restore:** fetch/local-fallback, verify, decode/migrate, open, and structurally/semantically validate before resuming.
7. **Reconciliation:** restore matching source positions, timers/watermarks, channel order, and sink/external-effect status.
8. **Capacity:** prove tail RTO, replay/catch-up convergence, source retention, storage requests, memory/disk/network, and headroom.
9. **Lifecycle/security:** retain independent fallbacks, mark dependencies, honor holds/deletion/keys/regions, audit access, and safely collect.
10. **Evidence:** restore and fault-inject recent/old/regional/upgrade/rollback points; compare results to authoritative invariants.

Manifest integrity proof composes only if the authenticated root binds every referenced component and each immutable object's verified bytes bind its expected hash/length. A valid manifest with an unverified dependency is not a verified snapshot.

Restore completeness requires every required shard exactly once plus source/effect metadata from the same cut. Starting before this predicate holds can expose partial or split-brain state.

GC safety is graph reachability under a stable root set. Concurrent root creation/claim/restore requires transactional marking, leases, or grace/recheck so a newly live object is not deleted between observations.

## Alternatives and Trade-Offs

**Full snapshots** simplify independence/restore but maximize write bytes. **Incremental snapshots** reduce steady writes but share failure/retention dependencies. **Changelogs** spread write work and shorten snapshot pauses while adding ordered replay/compaction. **Disaggregated state** moves durability remote while making network/cache/service performance central.

**Remote primary** survives worker loss and supports reassignment but adds fetch latency/cost. **Local secondary** accelerates same-node recovery but is correlated and needs disk. **Standbys** reduce activation latency at continuous resource cost.

**Newest snapshot** minimizes replay only if complete, compatible, and valid. **Older independent base** increases replay but can survive new-format corruption. **Rebuild from source** avoids state-format dependence when retention/determinism/cost allow it.

**Many retained snapshots** improve fallback choice but cost storage/key/attack surface and may share bases. **Periodic compaction/full bases** reduce dependency depth/blast radius but cause write spikes.

**Claimed restore ownership** can reuse and later manage objects efficiently. **No-claim/copy-on-first-checkpoint** preserves the source snapshot for forks/rollback but duplicates bytes. Runtime-specific semantics must be pinned.

**In-place upgrade restore** is fast when compatibility is proven. **Blue/green restore and shadow replay** isolate risk and compare results at double capacity. **Export/rekey/rebuild** handles identity changes at high migration cost.

## Failure Modes and Misconceptions

1. **“Checkpoint complete means files uploaded.”** One atomic valid manifest must bind all required components.
2. **“Newest path is newest recovery point.”** Listings can contain partial, orphaned, incompatible, or corrupt artifacts.
3. **“Incremental delta equals restore size.”** restore follows the dependency closure.
4. **“Delete the old base after a new delta.”** descendants may still reference it.
5. **“Reference count cannot race.”** creation, restore, forks, and holds change liveness concurrently.
6. **“A full snapshot is one self-validating file.”** shards, metadata, keys, and decoders remain.
7. **“Local SSD is the checkpoint.”** correlated node loss removes it.
8. **“Standby lag is harmless.”** activation can expose stale state unless catch-up/fencing completes.
9. **“Snapshot duration is RTO.”** detection through replay/catch-up/reconciliation dominates recovery.
10. **“Aggregate bandwidth predicts restore.”** slow shards, requests, compaction, and skew control the tail.
11. **“Replayable source makes RPO automatically zero.”** source retention and external decisions/effects can fail.
12. **“A running process is recovered.”** correctness/freshness and effects must be validated.
13. **“Schema-compatible means state-compatible.”** keys, serializers, names, timers, and semantics differ.
14. **“Changing key normalization is a decoder change.”** it changes identity/ownership and needs migration.
15. **“Rescaling just downloads files.”** every state shard must map exactly once.
16. **“Ignore corrupt channel state to recover.”** that is an explicit possible-data-loss action.
17. **“Encryption guarantees availability.”** a lost/unauthorized key makes valid bytes unusable.
18. **“More backups always improve resilience.”** shared bases, keys, regions, or bugs correlate failure.
19. **“Retention and deletion are separate.”** snapshots preserve governed historical values.
20. **“Successful snapshot tests recovery.”** only a restore drill does.

## Worked Examples

### Example 1

C1 references base A; C2 references A plus delta B; C3 references A plus delta C. Retaining C1 and C3 keeps A and C. B is collectible only if C2 is incomplete/unretained and no active operation or hold references it.

### Example 2

A 12 GB state writes a 400 MB incremental delta. Restore still reads a 12 GB dependency closure. At 300 MB/s ideal sequential throughput, transfer alone is 40 seconds, not 1.33 seconds.

### Example 3

Ten shards each restore in 20 seconds except one skewed shard at 180 seconds. Parallel aggregate throughput looks high, but fetch/decode critical path is at least 180 seconds before replay/catch-up.

### Example 4

The newest manifest has one hash mismatch. Recovery quarantines it and selects the previous verified point, adding 25 minutes of replay. If source retention has only 10 minutes remaining, fallback is not operationally safe despite valid old state.

### Example 5

Failure is detected after 30 seconds, scheduling takes 45, fetch/verify/decode takes 120, replay 60, catch-up 90, and reconciliation 15 serial seconds. Approximate RTO is 360 seconds (6 minutes); overlap must be measured rather than assumed.

### Example 6

Input continues at 8,000 records/s; recovered capacity is 10,000/s; backlog is 3.6 million. Ideal catch-up is $3.6M/(10k-8k)=1{,}800$ seconds, or 30 minutes. At capacity 8,000/s, it never converges.

### Example 7

An operator UID changes while its state name/schema remain identical. Automatic restore cannot map the old handle reliably. A stable explicit UID or governed remapping/rebuild is required; guessing by topology order risks attaching state to the wrong operator.

### Example 8

A secondary local copy restores seven of eight shards; one checksum fails. The task fetches that shard from the complete remote primary. Local failure degrades speed, not checkpoint validity.

### Example 9

A cross-region replica copies the manifest before its last shared object. A disaster immediately after produces a visible but unrestorable root. Replication publishes the regional root only after every transitive dependency and key is verified there.

### Example 10

This fixture selects the newest complete compatible manifest and computes live versus orphan snapshot objects.

<!-- bijux-verify: {"id":"snapshot-selection-and-reachability","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected=c3 restore_mb=140\nlive=('base', 'delta3') orphan=('delta2',)\n","stderr":""}} -->
```python
objects_mb = {"base": 120, "delta2": 30, "delta3": 20}
manifests = {
    "c1": ("base",),
    "c2": ("base", "delta2"),
    "c3": ("base", "delta3"),
}
complete = {"c1": True, "c2": False, "c3": True}
compatible = {"c1": True, "c2": True, "c3": True}

selected = "c1"
for candidate in ("c3", "c2", "c1"):
    if complete[candidate] and compatible[candidate]:
        selected = candidate
        break

restore_mb = sum(objects_mb[name] for name in manifests[selected])
retained = ("c1", "c3")
live = tuple(sorted({
    name
    for checkpoint in retained
    for name in manifests[checkpoint]
}))
orphan = tuple(sorted(name for name in objects_mb if name not in live))

print(f"selected={selected} restore_mb={restore_mb}")
print(f"live={live} orphan={orphan}")
```

The fixture validates one finite manifest selection and direct dependency set. It does not verify hashes, transitive DAGs, races, encryption, compatibility, distributed placement, restore performance, replay, or effects.

## Cross-Program Connections

- **Distributed Systems:** consistent cuts, epochs, fencing, replication, failure domains, consensus metadata, replay, and split-brain prevention underpin recovery.
- **Database Systems:** checkpoints, WAL, MVCC, page/SST snapshots, manifests, compaction, point-in-time recovery, and transactions recur directly.
- **Data Structures:** persistent trees, content-addressed DAGs, hashes, reference counts, reachability, logs, and key-group maps shape representation.
- **Data Engineering:** source retention, CDC positions, state stores, backfills, sink transactions, reconciliation, and schema evolution determine viability.
- **Reliability Engineering:** RPO/RTO, tail latency, cold capacity, catch-up, drills, fallback, and disaster recovery make artifacts useful.
- **Security Engineering:** encryption/key lifecycle, signatures, least privilege, tenant/region boundaries, deletion, legal hold, and audit protect snapshots.
- **Platform Engineering:** storage classes, schedulers, state backends, standbys, autoscaling, manifests, telemetry, and runbooks provide shared mechanisms.
- **Systems Engineering:** steady overhead, failure coverage, restore latency, correctness, cost, compatibility, governance, and human operations are coupled.

## References

1. Apache Flink. [Fault Tolerance via State Snapshots.](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) Current definitions of state backends, checkpoint storage, snapshots, checkpoints, savepoints, replay, and delivery guarantees.
2. Apache Flink. [Checkpoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints/) Current persistent checkpoint storage, retention, directory structure, and retained-checkpoint resume documentation.
3. Apache Flink. [Savepoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/savepoints/) Current manifest/files, stable operator IDs, restore, rescale, ownership, disposal, and portability behavior.
4. Apache Flink. [Checkpoints versus Savepoints.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints_vs_savepoints/) Current distinctions in purpose, format, ownership, retention, lifecycle, and operational use.
5. Apache Flink. [State Backends.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/state_backends/) Current heap, embedded/disaggregated, full/incremental, changelog, checkpoint, and recovery characteristics.
6. Apache Flink. [Tuning Checkpoints and Large State.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/) Current incremental snapshot, task-local recovery, primary/secondary roles, compression, restore, and capacity guidance.
7. Apache Flink. [Upgrading Applications and Flink Versions.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/upgrading/) Current savepoint-driven restart, application-state compatibility, stable IDs, serializer/schema, and rollback guidance.
8. Apache Flink. [State Schema Evolution.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/) Current serializer snapshot, supported schema changes, compatibility, and key-schema limitations.
9. Apache Flink. [Configuration: State Recovery.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/) Current claim/no-claim, local recovery, ignored unclaimed state, recovery path, and channel-state recovery controls.
10. Apache Kafka. [Processor API: Fault-Tolerant State Stores.](https://kafka.apache.org/43/streams/developer-guide/processor-api/) Current compacted changelog-backed state-store restoration and migration behavior.
11. Apache Kafka. [Configuring a Streams Application.](https://kafka.apache.org/43/streams/developer-guide/config-streams/) Current acceptable recovery lag, standby/warmup assignment, local state, and high-availability configuration.
12. Apache Beam. [Runner Authoring Guide.](https://beam.apache.org/contribute/runner-guide/) Primary source checkpoint, bundle atomicity, state/timer, retry, and runner consistency contract.
13. Akidau, T., et al. [“MillWheel: Fault-Tolerant Stream Processing at Internet Scale.”](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) PVLDB, 2013. Persistent state, checkpoints, low-watermarks, record production, deduplication, and recovery mechanisms.

## Exercises

### Exercise 1

Retained manifests are C1=`(A,B)`, C3=`(A,D)`, and C4=`(E,D)`; incomplete C2=`(A,C)`. Object sizes are A=100, B=20, C=15, D=30, E=80 MB. Compute live objects, orphan candidates, unique retained bytes, and restore bytes for C4.

### Exercise 2

Detection is 25 seconds, coordination/scheduling 50, fetch/verify/decode 210, replay 80, catch-up 120, and reconciliation/cutover 15, all conservatively serial. Compute RTO. State why snapshot upload duration and process-start time cannot substitute for it.

### Exercise 3

Input rate is 12,000 records/s. Failure and restore produce 4.8 million backlog records. Compute ideal catch-up time at sustainable capacities 15,000/s and 12,000/s. Give missing real-world factors.

### Exercise 4

The newest completed snapshot uses old operator UID `orders-v1`, 2,048 key groups, serializer version 3, a deprecated zone-rule version, and a prepared sink transaction. The new job renames the operator, changes key normalization, uses serializer version 4, and runs at different parallelism. Produce a compatibility/migration decision, not merely a decode check.

### Exercise 5

Design a regional recovery drill for a 30 TB stateful stream with incremental shared objects, local copies, changelog, transaction sink, 45-minute source retention, encryption-key rotation, and a 20-minute RTO. Include selection, security, capacity, verification, fallback, cleanup, and evidence.

## Answers to the Exercises

### Answer 1

Roots C1, C3, and C4 reach A, B, D, and E. C is referenced only by incomplete/unretained C2, so it is an orphan candidate subject to active-operation/hold/grace recheck. Unique retained bytes are $100+20+30+80=230$ MB. C4 restore reads E+D=$80+30=110$ MB. Shared A remains because C1/C3 need it even though C4 does not.

### Answer 2

Conservative serial RTO is $25+50+210+80+120+15=500$ seconds, or 8 minutes 20 seconds. Upload duration measures creation, not detection/scheduling/read/decode/replay/catch-up/effects. Process start excludes restored correctness and freshness. Real stages may overlap, but only measured critical-path evidence can reduce the estimate.

### Answer 3

At 15,000/s, net catch-up is 3,000/s, so $4.8M/3000=1{,}600$ seconds, or 26 minutes 40 seconds. At 12,000/s, net capacity is zero and catch-up never converges. Real estimates include skew, cache/compaction warming, restore I/O contention, source/sink quotas, retries, window/timer bursts, autoscaling delay, checkpoint overhead, and changing arrival rate.

### Answer 4

Preserve/map the old UID or explicitly export/remap its state; a rename alone can orphan it. Different parallelism is supportable only if all 2,048 key groups map exactly once and maximum-parallelism/key encoding are compatible. Serializer v4 must read production v3 bytes or perform a verified rewrite with rollback. Changed key normalization is a semantic rekey that may merge/split accounts, so use export/rekey/merge policy or deterministic replay into a new job; do not restore keyed bytes in place. Pin or intentionally migrate zone rules with output diffs. Resolve the prepared sink transaction against the selected checkpoint before effects resume and fence old producers. Blue/green shadow/reconciliation is safer than claiming compatibility from deserialization.

### Answer 5

Replicate only region-complete authenticated manifests after all transitive objects, changelog ranges, code/config/schema, source/sink access, and required key versions are verified. Select the newest compatible point whose 45-minute source margin covers detection/restore/catch-up; keep an independent older base fallback. Provision remote request/bandwidth, 30 TB fetch/decode or disaggregated access, per-shard memory/disk, sink/source throughput, and net catch-up to meet 20 minutes; local copies are assumed unavailable in regional loss. Fence old region/tasks, restore every shard exactly once, verify hashes/decrypt/schema/invariants/timers/channel state, resolve sink transactions, replay and reconcile before cutover. Test lost rotated keys, missing/corrupt shared bases, throttling, skew, stale standby/changelog, fallback, and rollback. Prevent real drill effects. Record phase/critical-path RTO, source margin, bytes/requests, state/result diffs, and recovery outcome; then validate reachability-aware cleanup without deleting held/fallback objects.
