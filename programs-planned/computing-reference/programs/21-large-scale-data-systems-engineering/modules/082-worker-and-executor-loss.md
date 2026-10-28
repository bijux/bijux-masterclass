---
module_id: LSDS-082
program: Large-Scale Data Systems Engineering
level: 2
module_number: 82
title: Worker and Executor Loss
status: complete
last_verified: 2026-09-04
---

# Worker and Executor Loss

## One-Page Review

### Governing question

When a worker process, executor, container, virtual machine, or physical node disappears—or merely appears unreachable—how can the platform fence its old incarnation, reconstruct every lost task and local artifact, replace capacity without a retry storm, and preserve correctness across planned decommissioning, preemption, partitions, and correlated failure domains?

### Essential definitions

- A **worker** is a schedulable execution agent that owns slots/resources and runs task attempts.
- An **executor** is a job/runtime-specific worker process, often one of several processes or containers on a node.
- A **worker incarnation** is a stable worker identity plus a monotonically changing registration epoch.
- **failure suspicion** is evidence such as heartbeat timeout; it is not proof that the process stopped.
- **fencing** rejects messages, output, and resource mutations from an obsolete incarnation.
- **abrupt loss** gives no reliable drain window; **decommissioning** announces planned removal and attempts graceful handoff.
- **local artifact inventory** records shuffle blocks, cache, spill, state, logs, and credentials tied to a worker.
- A **replacement deficit** is the resource/slot capacity needed after invalidating lost work and artifacts.
- A **failure domain** groups resources likely to fail together, such as process, host, rack, zone, image, or account.
- **blast radius** is affected tasks, state, blocks, jobs, tenants, bytes, and recovery time—not simply dead-worker count.

### Central model, mechanism, or theorem

Let worker incarnation $w=(id,e)$ own running attempts $A_w$, local artifacts $B_w$, state copies $S_w$, and resources $R_w$. When the coordinator advances accepted epoch to $e'>e$, all messages and commits carrying $e$ are rejected. The effective loss set is

$$L(w)=A_w\cup\{b\in B_w:availableOwners(b)\setminus\{w\}=\varnothing\}\cup\{s\in S_w:noDurablePrimary(s)\}.$$

Recovery invalidates running attempts, recomputes only artifacts without valid surviving owners or lineage boundaries, restores state from durable checkpoints, and requests capacity for the resulting runnable region. Graceful decommission can shrink $L(w)$ by stopping new assignments, migrating/replicating artifacts, checkpointing, and confirming handoff before termination; it cannot assume best-effort copying completed.

### Critical invariants

- Worker ID and incarnation epoch identify one registration; reconnecting processes never inherit authority accidentally.
- Heartbeat timeout triggers suspicion and duplicate-safe recovery, while fencing prevents a partitioned old worker from publishing.
- The coordinator maintains an exact worker-to-attempt/artifact/resource inventory at a durable enough authority boundary.
- Losing a local copy does not invalidate an artifact with a verified surviving durable owner; losing the last copy does.
- Local state/cache is an accelerator unless a separately documented replicated protocol makes it authoritative.
- Replacement tasks use new attempt IDs/epochs and winner-only output commit.
- Decommission stops new assignments before handoff and validates migrated blocks/state before declaring completion.
- Capacity replacement respects quotas, priorities, locality, anti-affinity, and recovery concurrency limits.
- Correlated failures are attributed by host/rack/zone/image/version/provider event rather than counted as independent samples.
- Credentials, volumes, ports, temporary objects, and logs are revoked or retained under explicit lifecycle policy.

### Common failures

Common failures include treating heartbeat loss as proof of death; reusing a worker ID after restart; accepting a late executor result after replacement; forgetting that one node hosts many executors; invalidating every replicated block when one owner disappears; assuming local checkpoint copies survive host loss; killing a decommissioning worker before block migration completes; draining all nodes in one failure domain together; autoscaling down executors that hold active shuffle; requesting unlimited replacements during a regional outage; rescheduling onto the same broken image or storage path; force-detaching volumes from a worker that may still write; revoking credentials before diagnostic/state upload; and measuring only executor count instead of lost work and recovery.

### Compact example

Worker `w1` runs three attempts and holds shuffle blocks `b1`, `b2`, and `b4`. `b1` also exists on `w2`, `b4` on `w3`, but `b2` has no other owner. On loss, the three running attempts receive new attempt IDs, only `b2` is invalidated and recomputed, and replacement demand begins at three slots plus any downstream work unlocked by `b2`. If `w1` later reconnects with its old epoch, its heartbeats and output commits are rejected. A graceful drain could have copied `b2` and reduced the block-loss portion to zero.

### Connections

[LSDS-031](031-shuffle-architecture.md) supplies block ownership, [LSDS-043](043-stateful-operators.md) supplies local/durable state, [LSDS-052](052-static-and-dynamic-allocation.md) supplies capacity control, [LSDS-055](055-work-stealing-and-speculation.md) supplies duplicate attempts, and [LSDS-081](081-task-level-failure-recovery.md) supplies recovery regions and winner commit.

## Governing Question

“Executor lost” compresses many events: clean process exit, OOM kill, container eviction, node reboot, preemption, network partition, disk failure, authentication expiry, scheduler removal, or deliberate scale-down. The coordinator may observe only missed heartbeats and a resource-manager event. Meanwhile the worker can still be running and capable of sending stale output.

Loss consequences are also heterogeneous. Running attempts disappear; cached inputs are performance-only; shuffle blocks may be last copies; local state may have durable primaries; attached volumes may be unsafe to move; logs may hold the only diagnosis; credentials may remain valid. Treating all local artifacts identically either wastes work or risks correctness.

The governing question is how to turn ambiguous liveness into safe membership, compute a precise loss inventory, recover capacity and data under bounded load, and make planned removal materially safer than abrupt failure.

## Why This Matters

At fleet scale, worker churn is normal. Autoscaling, spot/preemptible capacity, upgrades, kernel reboots, runtime crashes, memory pressure, and network maintenance continually replace executors. A system designed only for rare crashes will live in permanent degraded recovery.

Worker loss can cascade. Missing shuffle blocks cause upstream recompute; replacements cold-read checkpoints and object storage; simultaneous cache misses saturate services; retries consume spare capacity; speculative duplicates add load; and a coarse exclusion policy shrinks the fleet further. Recovery needs admission and dependency-aware prioritization.

Planned decommissioning is a powerful control surface. It can finish or cancel tasks, migrate shuffle/cache, persist diagnostics, checkpoint state, relinquish leases, and confirm zero critical ownership. But deadlines and provider termination notices are finite, so correctness cannot depend on graceful completion.

## Prerequisites and Retrieval

Review shuffle architecture in [LSDS-031](031-shuffle-architecture.md), stateful operators in [LSDS-043](043-stateful-operators.md), allocation in [LSDS-052](052-static-and-dynamic-allocation.md), speculation in [LSDS-055](055-work-stealing-and-speculation.md), and task recovery in [LSDS-081](081-task-level-failure-recovery.md).

You should understand heartbeats, leases, membership epochs, fencing, attempt IDs, shuffle lineage, replication, checkpoints, local disks, volumes, cgroups/OOM, signals, schedulers, autoscaling, taints/drains, preemption, anti-affinity, quotas, backpressure, and failure domains.

For diagnosis retain worker ID/epoch, process/container/node/provider IDs, registration/heartbeat timeline, exit reason/code/signal, task and artifact inventories, block owners/checksums, checkpoint handles, resource requests/usage/limits, pressure/eviction events, decommission notice/progress, placement topology, replacement requests, fencing decisions, logs, and correlated fleet changes.

## Learning Objectives

After this module, you should be able to:

1. Distinguish process, executor, container, VM, node, and failure-domain loss.
2. Explain why failure suspicion requires epoch fencing and duplicate-safe recovery.
3. Compute lost attempts, last-copy artifacts, state impact, and capacity deficit.
4. Separate authoritative durable state from local recovery accelerators.
5. Design graceful decommissioning with validated handoff and a hard deadline.
6. Recover shuffle/cache/state without unnecessary invalidation or silent reuse.
7. Replace capacity under quotas, priorities, topology, and bounded concurrency.
8. Diagnose OOM, disk, network, image, dependency, eviction, and provider failures.
9. Test partitions, late workers, abrupt shutdown, failed migration, and correlated loss.
10. Measure blast radius, recovery amplification, preservation, and decommission success.

## Core Exposition

### Identity, registration, and incarnation

Assign a durable logical worker ID only where needed; every process registration receives a new incarnation/epoch and authenticated session. The coordinator records runtime/version, resources, topology, addresses, artifact services, credential scope, and start time. Task leases and output authorizations bind that incarnation.

A restarted process on the same hostname is not the same executor. IPs, pod names, and local paths can be reused. Reject messages whose epoch is below current registration, whose session identity mismatches, or whose assigned attempt is no longer current.

### Detection, suspicion, and fencing

Heartbeats carry monotonic progress and inventory summaries. Timeout, closed control stream, resource-manager removal, process exit, and node event contribute evidence. Choose timeouts against pause, load, and network distributions; too short creates false suspicion, too long extends recovery.

Once recovery duplicates work, assume the old worker may return. Advance epoch or revoke its leases, and make coordinators, shuffle services, sinks, and output commit reject stale authority. A “kill” request is not fencing because a partition can prevent delivery.

### Loss inventory and propagation

Snapshot the worker's running attempts, committed/uncommitted outputs, shuffle/cache blocks, state copies, local disks/volumes, broadcasts, service endpoints, credentials, and diagnostic streams. For each artifact compute surviving valid owners and lineage. Invalidate last copies, not every copy.

Feed lost attempts and artifacts to LSDS-081 recovery-region logic. A missing shuffle partition may rerun one producer and affected consumers; loss of a nonreplayable source shard is terminal; loss of cache causes cold reads only. Deduplicate simultaneous worker and block-loss reports.

### Shuffle, cache, and local disk

Worker-owned shuffle couples executor lifetime to downstream tasks. External/reliable shuffle, block replication, decommission migration, or shuffle tracking can decouple them. Each mechanism needs exact block identity, producer attempt/epoch, checksum, completeness, ownership, and retention.

Cache loss changes performance, not logical state, if the origin is durable and pinned. Spill and temporary files are generally attempt-private. Never promote surviving path names without identity checks. Monitor disk pressure, corruption, and inode exhaustion before they become process loss.

### Stateful workloads and local recovery

Local checkpoint/state copies reduce restore latency when the same storage survives and compatible placement returns. The complete distributed checkpoint is primary. If a task manager or node is lost, restore affected keys/operators from the durable checkpoint and replay matching sources.

Persistent volumes can preserve bytes across pod restart, but attachment identity, fencing, filesystem integrity, and single-writer rules matter. Force-detaching a volume while an isolated node still writes risks corruption. Treat storage recovery separately from compute membership.

### Abrupt loss workflow

Classify and fence the incarnation; freeze its inventory; invalidate running attempts and last-copy artifacts; derive recovery regions; request bounded replacement capacity; restore/recompute in dependency order; verify winners and state progress; then retire credentials/resources and reconcile artifacts.

Prioritize work that unlocks many consumers or restores service-level state, subject to tenant fairness. Coalesce recovery for multiple workers in one domain. Preserve diagnostics before cleanup where available, but do not delay correctness on a dead worker's cooperation.

### Graceful decommissioning

Mark draining and stop new tasks. Let short safe attempts finish or cancel them under deadline. Replicate/migrate critical shuffle and cached blocks, complete or abort output commits, checkpoint state when useful, upload diagnostics, release service registrations, and validate the destination inventory.

Declare drain complete only when critical ownership is zero or policy accepts recomputation. Best-effort transfer needs checksums and acknowledgements. If deadline expires, switch to abrupt-loss recovery. Batch drains across zones/racks conservatively and maintain disruption/spare-capacity budgets.

### Replacement scheduling and locality

Capacity deficit begins with lost slots/resources but recovery demand may expand through recomputation. Request by CPU, memory, accelerator, disk/network, architecture, image/runtime, zone, and data locality. Keep headroom for churn and avoid placing every replacement in the failed domain.

Allocation-preserving scheduling can reuse local state on surviving hosts without evicting other tasks from their former slots. When a host is gone, relax locality after a bounded wait. Recovery concurrency is limited independently from normal scheduling so it does not starve production.

### Autoscaling, preemption, and maintenance

Scale-down chooses workers with no running commitments and minimal critical artifact ownership. Shuffle tracking or migration prevents deleting executors that look CPU-idle but hold active blocks. Include startup latency and cache/state warming in scaling economics.

Preemption notices trigger the same drain state machine with a shorter deadline. Node upgrades use cordon/drain or runtime decommission integrations and respect disruption budgets. Chaos and real maintenance should exercise the identical recovery path.

### Correlated failures and containment

Group incidents by physical host, rack, zone, network, storage service, image, runtime, dependency endpoint, deployment, credential issuer, and time window. Ten workers lost to one bad image are one correlated cause with ten effects, not ten independent reliability samples.

Pause rollouts or scale-outs that reproduce the cause. Spread durable replicas and coordinators across relevant domains. Avoid retrying all affected tasks simultaneously against the same degraded dependency. Use circuit breakers and global recovery budgets while preserving priority work.

### Security and resource lifecycle

Workers use short-lived scoped credentials and authenticated channels. On loss, revoke sessions and leases where possible; fencing remains necessary because revocation propagates imperfectly. A returning worker cannot regain tasks from cached credentials.

Release IPs, ports, volumes, accelerators, service registrations, and quota exactly once. Retain logs, cores, profiles, and attempt artifacts under privacy and incident policy. Scrub reused local disks and prevent cross-tenant cache exposure.

### Observability and verification

Measure registrations/incarnations, heartbeat age, suspected/confirmed/drained workers, causes, affected attempts/jobs/tenants, lost/preserved/recomputed blocks and bytes, state restored local/remote, replacement latency/capacity, fencing rejects, recovery concurrency, cold-cache impact, drain duration/success, and resource leaks. Segment by runtime/version, image, node pool, zone, provider event, workload, and artifact type.

Inject process kill, OOM, container eviction, node reboot, network partition, disk loss/corruption, control-plane delay, preemption notice, failed migration, volume attachment delay, stale-worker return, and zonal loss. Compare results with a reference, verify one winner, exact state, no unavailable last-copy artifacts, bounded recovery load, and cleaned resources.

## Definitions and Notation

Let:

- $w=(id,e)$ be worker identity and incarnation epoch;
- $A_w$ be running task attempts on $w$;
- $B_w$ be local shuffle/cache blocks and $S_w$ local state copies;
- $owners(b)$ be validated owners of block $b$;
- $L_B(w)=\{b\in B_w:owners(b)\setminus\{w\}=\varnothing\}$ be last-copy blocks lost;
- $C_w$ be slot/resource capacity removed with $w$;
- $C_r$ be replacement capacity requested;
- $T_d$ be detection time and $T_r$ restored-progress time;
- $P$ be prior useful work and $X$ recomputed work;
- $z_w$ be greatest accepted worker fencing epoch;
- $D(w)$ be correlated failure-domain labels;
- $p_d$ be fraction of planned drains completing critical handoff.

Recovery latency is $T_r-T_d$ only under a stated detection boundary. Preservation ratio $P/(P+X)$ needs work units such as bytes or compute-seconds. Executor-loss rate requires executor-time exposure. Drain success must state deadline and required artifact classes.

## Mechanisms, Invariants, or Proof Structure

### Incarnation-fencing proof

Coordinator atomically advances accepted epoch for worker ID from $e$ to $e'>e$. Every task lease, block registration, and output commit checks the accepted epoch. A delayed message from old process carries $e$ and is rejected, so duplicate recovery cannot be overwritten by a partitioned stale incarnation.

### Artifact-availability proof

For each required block $b$, accept reuse only if at least one surviving owner provides matching logical producer, attempt/epoch, length, checksum, completeness, and retention. Removing $w$ preserves $b$ when this set remains nonempty; otherwise lineage schedules reconstruction before consumers commit. Thus replicated availability is not discarded and last-copy loss is not hidden.

### Decommission-handoff proof

Draining stops new ownership. For every critical artifact on $w$, the protocol obtains a verified destination or records intentional recomputation. Running attempts reach winner commit or are invalidated. Only after the inventory reaches zero unresolved critical items does termination preserve recoverability. Timeout falls back to abrupt loss rather than asserting completion.

### Capacity-containment argument

If replacement/recompute admission is bounded by reserve, tenant quota, and dependency capacity, one loss wave cannot schedule unbounded concurrent recovery. Priority and dependency-unlocking order preserve useful progress. This is a liveness policy, not a guarantee against a failure larger than durable-state or capacity assumptions.

### Adversarial verification

Test false heartbeat suspicion, late reconnect, duplicate registration, process/node/zonal loss, replicated/last-copy blocks, partial migration, local/primary checkpoint combinations, force-detach risk, OOM, disk pressure, bad image rollout, preemption deadline, exhausted quota, cold start, cleanup duplication, and credential revocation delay. Require fencing, exact results, bounded recovery, or explicit terminal failure.

## Alternatives and Trade-Offs

**Long heartbeat timeout** avoids false suspicion but delays recovery. **Short timeout** restores faster but creates duplicate work and fencing traffic. Adaptive evidence can help but must remain explainable.

**Worker-owned shuffle** is local and cheap but couples block life to executors. **External/reliable shuffle** preserves work but adds a stateful service. **Replication** spends steady-state bytes; **lineage** spends failure-time compute; **decommission migration** helps planned loss only.

**Local state** accelerates same-host recovery. **Remote primary checkpoints** survive host loss and rescaling. Keeping both costs disk/write traffic but improves common recovery latency.

**Immediate replacement** restores capacity quickly but can stampede dependencies. **Admission-limited replacement** protects the fleet but lengthens individual recovery. **Warm spare capacity** costs money while reducing tail recovery.

**Aggressive scale-down** improves utilization but loses caches/shuffle and increases churn. **artifact-aware scale-down** preserves work but may retain apparently idle workers.

## Failure Modes and Misconceptions

1. **Missed heartbeat means dead.** It means suspected; fence before duplicating safely.
2. **Same hostname means same worker.** Incarnation identity must change.
3. **Kill request fences a worker.** Network partitions can hide it.
4. **Executor loss equals one task loss.** It may remove many attempts and artifacts.
5. **Every local block is lost data.** Replicas and durable origins may survive.
6. **One surviving filename proves a block.** Identity, completeness, and checksum matter.
7. **Cache loss changes results.** Correct caches are derived; it changes performance.
8. **Local checkpoint is primary.** Host loss disproves that assumption.
9. **Persistent volume solves membership.** Stale writers still require fencing.
10. **Decommission signal means migrated.** Verify every critical handoff.
11. **CPU-idle executor is removable.** It may own active shuffle/state.
12. **Replacement slots equal recovery work.** Dependency recompute can expand demand.
13. **Retry in the same zone is locality.** It can repeat a domain failure.
14. **Ten executor failures are independent.** One rollout may cause all ten.
15. **More recovery concurrency is faster.** Shared services can collapse.
16. **Force detach is always safe.** An isolated old node may still write.
17. **Credential revocation is instantaneous fencing.** Propagation can lag.
18. **Removing the process cleans resources.** Volumes, registrations, and objects remain.

## Worked Examples

### Example 1

Executor `e7` times out and replacement launches. `e7` reconnects with epoch 12 after accepted epoch becomes 13; all late output and block registrations are rejected.

### Example 2

Worker owns blocks `b1,b2`; `b1` has another checksummed replica, `b2` does not. Loss preserves `b1` and follows lineage only for `b2`.

### Example 3

An OOM-killed executor used 14 GiB RSS under a 12-GiB container limit. Identical replacement is likely to fail; inspect heap/off-heap/native and partition skew before retry.

### Example 4

Local keyed-state copy survives a process restart on the same node, shortening restore. Node loss removes it, so the task restores from the durable distributed checkpoint.

### Example 5

A two-minute preemption notice stops assignments, finishes short tasks, copies last-copy shuffle blocks, checkpoints state, and validates destinations. Anything unfinished at deadline enters abrupt recovery.

### Example 6

Autoscaler sees no running tasks on an executor, but shuffle tracking shows 800 GiB needed by active reducers. It keeps the executor or migrates blocks before scale-down.

### Example 7

Twenty workers running one new image crash together. Scheduler pauses that rollout and avoids using the same image for replacements instead of excluding twenty unrelated hosts.

### Example 8

A partitioned node still mounts a volume. Force attachment elsewhere without storage fencing risks two writers. Recovery waits for verified power-off/fencing or uses a protocol-safe detach.

### Example 9

Replacement demand is 200 slots, but object storage is throttled. Admission allows 40 restore-heavy slots at once while latency-sensitive unaffected work retains quota.

### Example 10

The executable fixture classifies running-attempt and replicated-shuffle consequences of one worker loss.

<!-- bijux-verify: {"id":"worker-loss-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lost_worker=w1\nrunning_tasks_lost=3\nshuffle_blocks_lost=b2\nshuffle_blocks_surviving=b1,b3,b4\nreplacement_slots=3\n","stderr":""}} -->
```python
lost_worker = "w1"
running_attempts = {"w1": ["t1", "t2", "t3"], "w2": ["t4"]}
owners = {
    "b1": {"w1", "w2"},
    "b2": {"w1"},
    "b3": {"w2"},
    "b4": {"w1", "w3"},
}

lost_blocks = sorted(block for block, hosts in owners.items() if hosts == {lost_worker})
surviving = sorted(block for block, hosts in owners.items() if hosts - {lost_worker})
lost_attempts = running_attempts[lost_worker]

print(f"lost_worker={lost_worker}")
print(f"running_tasks_lost={len(lost_attempts)}")
print(f"shuffle_blocks_lost={','.join(lost_blocks)}")
print(f"shuffle_blocks_surviving={','.join(surviving)}")
print(f"replacement_slots={len(lost_attempts)}")
```

## Cross-Program Connections

- **Distributed systems:** failure detectors, leases, epochs, fencing, replication, and correlated failure govern membership.
- **Operating systems:** processes, signals, OOM, cgroups, filesystems, and shutdown expose causes and resources.
- **Cloud infrastructure:** preemption, instance lifecycle, zones, autoscaling, images, and attached volumes shape churn.
- **Storage:** shuffle ownership, checksums, replicas, local disks, checkpoints, and volume fencing determine preservation.
- **Scheduling:** locality, quotas, priority, anti-affinity, disruption budgets, and admission contain recovery.
- **Security:** sessions, scoped credentials, revocation, disk scrubbing, and audit protect stale and replacement workers.
- **Reliability engineering:** blast radius, fault injection, SLOs, headroom, and incident correlation verify resilience.
- **Economics:** warm capacity, replication, remote shuffle, migration, and recomputation trade steady cost for recovery tails.

## References

1. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents executor failure, heartbeat, decommissioning, block migration, exclusion, and dynamic allocation controls.
2. Apache Spark, [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Current. Covers executor allocation, shuffle preservation prerequisites, pools, and cancellation.
3. Apache Spark, [Monitoring](https://spark.apache.org/docs/latest/monitoring.html). Current. Documents executor, stage, event-log, metrics, and status evidence.
4. Apache Spark, [Running on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html). Current. Documents executor pods, allocation, decommissioning, and pod lifecycle integration.
5. Apache Flink, [Task Failure Recovery](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/task_failure_recovery/). Version 2.3. Defines restart/failover scope after task-manager effects.
6. Apache Flink, [Tuning Checkpoints and Large State](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/large_state_tuning/). Current. Defines local recovery as secondary to durable primary state.
7. Apache Flink, [TaskManager Memory](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/memory/mem_setup_tm/). Current. Documents worker heap, managed, off-heap, network, and process memory.
8. Kubernetes, [Node Shutdowns](https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/). Current. Documents graceful/non-graceful node shutdown and storage-detach cautions.
9. Kubernetes, [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/). Current. Defines voluntary/involuntary disruption and disruption budgets.
10. Kubernetes, [Node-Pressure Eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/). Current. Documents memory, disk, inode, and PID pressure responses.
11. Kubernetes, [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/). Current. Defines phases, container restarts, termination, and node-loss behavior.
12. AWS EC2, [Spot Instance Interruptions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html). Current. Documents interruption notices and rebalance signals.
13. Apache Hadoop YARN, [NodeManager](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/NodeManager.html). Current. Documents worker-node services, health, recovery, and resource management.

## Exercises

### Exercise 1

Worker W runs five attempts and owns blocks x, y, z. Owners are x={W,A}, y={W}, z={W,B,C}. Compute immediate attempt retries and block invalidations after W is fenced. What additional evidence is required to reuse x and z?

### Exercise 2

Design a 90-second executor decommission protocol for a worker with running tasks, last-copy shuffle, local checkpoint state, credentials, and an attached volume.

### Exercise 3

Thirty workers in one zone time out within ten seconds. Describe detection, correlated attribution, replacement admission, placement, and service protection.

### Exercise 4

A node is network-partitioned but may still write its attached volume. Explain why heartbeat timeout and force detach are insufficient and design a safe recovery decision.

### Exercise 5

Design a chaos experiment and dashboard comparing abrupt worker loss with graceful decommission, including correctness, preserved work, capacity, and tail recovery.

## Answers to the Exercises

### Answer 1

All five running attempts need new attempt identities according to their recovery regions. Only y loses its last recorded owner and is invalidated; x and z still have candidate owners. Reuse requires each surviving owner to return the correct logical block and producer attempt/epoch, complete length, checksum, partition/serialization contract, and retention/accessibility. A stale inventory entry alone is insufficient.

### Answer 2

At notice, advance W to draining and stop assignments. Fence new ownership changes, inventory tasks/artifacts/state/resources, finish only tasks whose commit fits the deadline, and cancel others into normal retry. Replicate last-copy shuffle with checksum acknowledgements, ensure durable checkpoint primary exists, upload diagnostics, and prepare credential/session revocation. Quiesce and safely detach the volume under storage fencing. Declare success only when critical inventory is zero and destinations validate; otherwise at a safety cutoff transition remaining items to abrupt recovery, request bounded replacements, and never delay provider termination assumptions beyond the notice.

### Answer 3

Correlate by zone and time before treating thirty samples independently. Fence each incarnation, coalesce lost attempts/blocks/state into dependency recovery, and preserve evidence of network/provider events. Request replacements in healthy zones subject to anti-affinity, quotas, startup capacity, and data egress constraints. Limit restore/recompute concurrency against checkpoint, shuffle, catalog, and object-storage budgets; prioritize dependency-unlocking and high-SLO jobs fairly. Suppress retries into the failed zone until authoritative health returns, while avoiding a total freeze if cross-zone durable state is intact.

### Answer 4

Timeout proves only that the coordinator cannot communicate; the node may still execute cached instructions and write the volume. Force attaching it elsewhere can create concurrent writers and corruption. First fence at a storage/controller layer the old node cannot bypass—verified power-off, provider instance fencing, lease/token enforcement by the volume service, or protocol-defined safe detach. Only after authoritative fencing/detach confirmation attach to the replacement. If no enforceable fence exists, prefer delayed recovery or restore a separate durable replica rather than assert single-writer safety.

### Answer 5

Run matched workloads with deterministic outputs and inject process kill, node loss, partition, and scheduled drain at read/compute/shuffle/state/commit points. For drain vary notice length and fail one migration. Assert exact final rows/state, one attempt winner, stale-epoch rejection, valid surviving blocks, and no leaked volume/session. Graph detection, drain, replacement, and restored-progress percentiles; lost/preserved/recomputed tasks and bytes; local/remote state restore; migration throughput/failure; cold-cache penalty; dependency throttling; capacity deficit; and affected jobs/tenants by domain. Graceful removal is better only where verified handoff raises preservation or lowers recovery tails without violating deadlines or correctness.
