---
module_id: LSDS-062
program: Large-Scale Data Systems Engineering
level: 2
module_number: 62
title: Coordinator and Worker Architecture
status: complete
last_verified: 2026-09-04
---

# Coordinator and Worker Architecture

## One-Page Review

### Governing question

How should a distributed query engine divide authority between coordinators and workers so query planning, admission, task assignment, exchange, failure recovery, security, and upgrades remain correct and scalable when messages duplicate, nodes restart, and control-plane state changes concurrently?

### Essential definitions

- A **coordinator** accepts and authenticates queries, binds metadata, plans work, admits resources, creates task graphs, tracks state, and assembles completion or results.
- A **worker** executes assigned tasks, scans sources, runs operators, exchanges pages, manages local resources, and reports attempt state and metrics.
- The **control plane** carries desired state, assignments, leases, heartbeats, status, cancellation, and policy; the **data plane** carries source and exchange data.
- A **query epoch** fences messages from an obsolete coordinator or recovery generation.
- A **worker incarnation** distinguishes a restarted process from the prior process using the same address or stable node name.
- A **task attempt** is one execution of a logical task; retries and speculative attempts share lineage but not identity.
- **desired-state reconciliation** repeatedly compares authoritative desired work with observed worker state and issues idempotent corrections.
- A **lease** grants time-bounded authority that expires unless renewed; it is not equivalent to proof of failure.
- **failure domain** is the set of components whose loss can jointly remove a responsibility or state copy.
- **fault-tolerant execution** persists or reconstructs enough intermediate state to retry work beyond a transient worker loss.

### Central model, mechanism, or theorem

Model each query as a monotone state machine under generation $g$: accepted, analyzed, admitted, planned, running, finishing, and terminal, with explicit cancellation and failure substates. A control command is identified by $(query, g, task, attempt, sequence)$ and is accepted only when its epoch is current and its idempotency key has not already been applied. Workers publish observations tagged with worker incarnation and query epoch; coordinators reconcile them against durable or reconstructible desired state. Data flows directly among workers or storage whenever possible, so coordinator work grows with control metadata rather than all processed bytes. Safety comes from epochs, idempotency, atomic state transitions, attempt-commit rules, and compatible protocol versions; availability depends on which coordinator state is durable, replicated, or replayable.

### Critical invariants

- Every query, stage, task, attempt, command, worker incarnation, coordinator epoch, policy generation, and catalog snapshot has stable identity.
- Exactly one current authority may commit query/task outcomes for an epoch; stale coordinators and workers are fenced.
- Retried control messages are idempotent, and status transitions cannot move a terminal task back to running.
- Worker liveness suspicion does not immediately authorize unsafe duplicate external effects.
- Data-plane exchange does not transit the coordinator unless result semantics explicitly require it and capacity is bounded.
- Task placement respects source locality, partition ownership, resource requests, tenant policy, and failure-domain constraints.
- Backpressure propagates across exchange and split assignment so workers, coordinators, and metadata stores remain bounded.
- Cancellation and timeout reach queued, running, blocked, exchanging, spilling, and output-committing work.
- Result or sink commit chooses compatible successful attempts exactly once at the declared visibility boundary.
- Rolling upgrades preserve wire, state, catalog, exchange, and worker/coordinator compatibility or drain incompatible work first.

### Common failures

Common failures include sending all data through the coordinator; treating a heartbeat timeout as certain death; identifying a restarted worker only by hostname; replaying an old coordinator's assignments; creating duplicate tasks on request retry; allowing terminal state regression; retaining every split and metric indefinitely in coordinator memory; assigning faster than exchange or storage can drain; retrying side-effecting output without commit fencing; losing security context between planning and worker access; mixing catalog snapshots across fragments; placing all replicas or recovery state in one failure domain; and performing a rolling upgrade whose workers and coordinator disagree on plan or exchange protocol.

### Compact example

A worker has accepted coordinator epoch 4, command `q7-1`, and target parallelism 8. It rejects a delayed epoch-3 command and a duplicate `q7-1`, then accepts epoch 5 command `q7-2` with target 12. Epoch fencing prevents obsolete authority from overwriting recovered state; command identity prevents a network retry from applying the same operation twice.

### Connections

[LSDS-054](054-data-local-task-placement.md) defines placement, [LSDS-055](055-work-stealing-and-speculation.md) governs attempts, [LSDS-058](058-multi-tenant-queueing.md) supplies admission policy, [LSDS-059](059-autoscaling-data-clusters.md) separates desired from effective capacity, [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) traces control-plane delay, and [LSDS-061](061-distributed-logical-and-physical-plans.md) provides the fragment graph this architecture executes.

## Governing Question

Distributed query engines commonly present a coordinator/worker shape: one role understands the query as a whole, while many workers execute fragments over partitions. The boundary seems simple until failures arrive. A client retries submission after losing a response. A coordinator pauses and a replacement takes over. A worker restarts at the same address. Two attempts produce exchange output. A catalog changes during planning. Cancellation races with final commit. A rolling upgrade changes a task descriptor.

The coordinator is both valuable and dangerous. Central knowledge simplifies global planning, admission, and query state, but mutable per-query state, scheduling work, heartbeat processing, metrics, and result traffic can exhaust it. Replicating the process does not automatically replicate or fence authority. Sharding coordinators improves scale but introduces routing, ownership, failover, and cross-query resource coordination.

The governing question is how to draw the control/data boundary, define durable state machines and protocols, bound every queue, separate suspicion from authority transfer, and prove that failures or upgrades cannot create conflicting execution or visible duplication.

## Why This Matters

Coordinator failure can terminate thousands of otherwise healthy worker tasks, while a slow coordinator can delay every query despite idle compute. Worker failure is expected at scale and should usually have a bounded blast radius. Architecture determines whether the engine retries a task, stage, or whole query; whether intermediate data survives; and whether interactive latency or large batch recovery dominates design.

Control-plane correctness is also data correctness. Duplicate task assignment may be harmless for a pure scan but dangerous for an external sink. A stale cancellation can kill replacement work. A lost catalog or security context can read the wrong snapshot or exceed privilege. A result marked complete before exchange manifests or output commits are durable can disappear after failover.

Finally, the boundary determines operability. Query state, task lineage, worker membership, scheduler decisions, exchange pressure, and failure causes must correlate. Without explicit identities and generations, metrics from an old attempt contaminate a new one, and operators cannot distinguish worker shortage from coordinator saturation or downstream backpressure.

## Prerequisites and Retrieval

Review consensus and leases from the distributed-systems portion of the program, partition ownership in [LSDS-031](031-shuffle-architecture.md), placement in [LSDS-054](054-data-local-task-placement.md), speculation in [LSDS-055](055-work-stealing-and-speculation.md), preemption in [LSDS-056](056-preemption.md), queue policy in [LSDS-058](058-multi-tenant-queueing.md), autoscaling in [LSDS-059](059-autoscaling-data-clusters.md), scheduler diagnosis in [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md), and distributed plans in [LSDS-061](061-distributed-logical-and-physical-plans.md).

You should understand state machines, epochs and fencing, idempotency, heartbeats, leases, backpressure, task DAGs, exchange, resource admission, retries, atomic commit, snapshots, authentication, authorization, and rolling deployment.

## Learning Objectives

After this module, you should be able to:

1. assign planning, admission, scheduling, execution, exchange, and commit responsibilities to explicit owners;
2. distinguish control-plane metadata from data-plane bytes and keep both bounded;
3. design query, stage, task, attempt, worker-incarnation, and coordinator-epoch identities;
4. specify idempotent desired-state and status protocols under duplication and reordering;
5. choose which coordinator state is durable, replicated, reconstructible, or intentionally ephemeral;
6. design membership, heartbeat, lease, fencing, and worker-drain behavior;
7. constrain retries and speculation with exchange and external-effect commit rules;
8. evaluate singleton, standby, replicated, and sharded coordinator topologies;
9. instrument coordinator and worker saturation, recovery, fairness, and security; and
10. validate failure, partition, overload, cancellation, and mixed-version behavior.

## Core Exposition

### Draw responsibility boundaries

List responsibilities before choosing processes. Ingress authenticates clients and establishes request identity. Analysis binds catalogs and security. Planning produces fragments. Admission reserves policy and capacity. Scheduling assigns tasks and splits. Workers execute operators. Exchange moves intermediate data. A commit owner publishes result or sink outcome.

Each responsibility needs authoritative state, failure semantics, and an interface. Co-locating them in one coordinator process can be reasonable, but ownership must remain explicit so components can be measured, recovered, or separated later.

### Separate control and data planes

Control messages contain query/plan references, split descriptors, desired task state, leases, status deltas, cancellation, and small metrics. Data-plane paths move source pages, shuffle partitions, spills, and results. Workers should exchange large data directly or through a dedicated exchange/storage service.

Avoid proxying worker-to-worker bytes through the coordinator. It creates bandwidth, memory, copy, and failure bottlenecks. Final result traffic may pass through a coordinator or gateway, but use flow control, spooling, size limits, cancellation, and client backpressure.

### Give queries an idempotent ingress identity

A client may retry because it did not receive the submission response. Accept a client-generated or server-issued idempotency key scoped to authenticated tenant and request semantics. The same key returns the existing query; conflicting content is rejected.

Separate query identity from connection identity. Disconnect need not cancel unless policy says so. Record session, parameters, catalog/security snapshots, priority, resource group, and submission policy generation so recovery does not silently reinterpret the request.

### Model query state explicitly

Define legal transitions from accepted through terminal states. Failure, cancellation, timeout, and preemption have causes and ownership. Make terminal states absorbing. Use compare-and-set or transactional event application so concurrent completion and cancellation choose one documented outcome.

Stage and task states form related but separate machines. Aggregate query state from committed child evidence rather than arbitrary last-writer status. A task attempt finishing does not mean its output was selected or consumed.

### Fence coordinator authority

When a coordinator can be replaced, give ownership an epoch obtained from a durable authority. Commands and commits carry that epoch. Workers and state stores reject lower epochs after seeing a newer one. A lease alone is insufficient if an isolated former owner can still reach workers or sinks.

Failover must recover or reconstruct desired state before acting. A new epoch fences old commands, but it does not deduplicate client submissions, recover missing plan artifacts, or resolve partially committed output by itself.

### Identify worker incarnations

Use stable worker identity plus a unique process incarnation. A restart at the same hostname or address loses tasks, memory, exchange buffers, and local files unless explicitly recovered. Status from the old incarnation must not update the new worker.

Registration publishes capabilities, resources, topology, protocol versions, and health. The coordinator admits the worker only after compatibility and authorization checks. Inventory changes are generation-stamped and reconciled rather than inferred from address reuse.

### Treat heartbeats as observations

Heartbeats report liveness, load, task summaries, and protocol progress. Missing heartbeats create suspicion under a declared timeout; pauses, partitions, or coordinator overload can cause false suspicion. Do not equate timeout with proof that the worker cannot still perform external actions.

Lease/fencing rules constrain authority during ambiguity. Use scalable aggregation or delta reporting and bound payloads. A worker with thousands of tasks must not make every heartbeat grow without limit.

### Reconcile desired task state

The coordinator publishes desired task/attempt descriptors with immutable plan fragment, inputs, output contract, resource limits, query epoch, and sequence. Workers apply commands idempotently and report observed state with incarnation. Reconciliation repairs lost messages and restarts.

Commands such as start, add splits, no-more-splits, cancel, and release output need monotone or explicitly versioned semantics. Reordering must not reopen closed input or revive a terminal attempt. Acknowledge durable application, not mere receipt, where recovery depends on it.

### Bound split discovery and assignment

Large scans may contain millions of splits. Eagerly materializing all descriptors in coordinator memory creates a scale cliff. Enumerate lazily, page metadata, and maintain bounded assignment windows. Persist or reconstruct enumeration position consistently with the source snapshot.

Workers advertise demand or available slots; coordinators do not flood them. Balance locality, fairness, skew, and startup latency. “No more splits” is a terminal input signal that must be ordered after all accepted assignments.

### Apply admission before expensive planning or execution

Authenticate and perform cheap validation first, then place queries into resource groups or queues before consuming unbounded planning, metadata, worker, or memory resources. Some analysis is needed to estimate demand, so bound that phase separately.

Admission controls running queries, queued queries, CPU/memory, scan bytes, worker slots, and coordinator-heavy operations. Preserve tenant priority and fairness. A coordinator protected from worker overload can still fail under unlimited queued plan objects.

### Schedule fragments with explicit constraints

Translate physical fragments into tasks using source partitions, exchange partition count, resource vectors, topology, catalog capabilities, and failure domains. Placement may favor locality but must obey isolation and availability. Record why a worker was selected or rejected.

Do not assume all workers are interchangeable. Connector access, architecture, accelerators, memory, spill disks, network paths, and protocol versions differ. Mixed-version placement must respect the plan features each worker understands.

### Design exchange away from coordinator memory

Workers produce partitioned output for downstream workers, directly or through an exchange service. The coordinator tracks compact manifests and completion, not every data page. Backpressure limits producer output when consumers, network, memory, or storage lag.

Define buffers, spill, retries, speculative attempts, checksums, encryption, ownership, retention, and garbage collection. A coordinator restart must rediscover committed exchange state or restart at a safe boundary.

### Commit task and exchange attempts

Multiple attempts of one logical task may run, but only compatible winning output becomes visible. Select a complete attempt atomically in a manifest or equivalent authority. Consumers read committed attempts and ignore losers.

For pipelined exchange, consumers may observe an attempt before final selection, coupling recovery. Either restart dependent work on producer loss or use a protocol that preserves stream identity and completeness. Never merge two attempts merely because both reported success.

### Handle worker loss by recovery boundary

On confirmed or fenced worker loss, classify lost state: recomputable scan work, pipelined exchange, durable exchange, local spill, operator state, and external effects. Retry the narrowest safe unit. Durable shuffle may permit task/stage retry; pure pipelining may require a larger query restart.

Bound retry count, time, and resource amplification. Preserve original tenant accounting and deadline. Correlated worker failures should not trigger an unbounded storm that overwhelms the coordinator or source.

### Handle coordinator loss deliberately

A non-resilient coordinator can fail all owned queries and rely on client retry. This is simple and sometimes acceptable for short interactive work. Longer queries may require durable query descriptors, plan artifacts, admission state, task desired state, exchange manifests, and output commit records.

Classify state as authoritative durable, replicated cache, worker-reported/reconstructible, or disposable. Recovery scans and reconciles rather than trusting one stale view. Measure recovery-point and recovery-time objectives per query class.

### Choose coordinator topology

A singleton is simple but a failure and capacity boundary. An active/standby pair improves restart time only if state and fencing are correct. Multiple active coordinators can own disjoint queries behind stable routing; shared admission and worker membership still need coordination.

Sharding by query avoids per-query distributed consensus in the fast path, but hot tenants or giant queries can skew coordinators. Rebalancing ownership must transfer state and epoch safely. Separate discovery/router availability from query ownership.

### Protect metadata and catalog consistency

Planning resolves tables, schemas, partitions, functions, and access policy under catalog snapshots or connector-defined consistency. Workers receive enough identity to read the intended version. Schema changes after planning must either remain compatible, fail explicitly, or trigger reanalysis—not produce mixed interpretation.

Cache metadata with version and invalidation rules. Bound catalog calls and isolate slow connectors so one source cannot exhaust coordinator threads. Security decisions must not outlive their permitted snapshot or session without revalidation policy.

### Propagate identity and authorization

Workers need authenticated, least-privilege authority for assigned sources, exchange, spill, and sinks. Use scoped credentials tied to query, tenant, resources, and expiry rather than forwarding broad coordinator credentials. Protect control messages against forgery and replay.

Record delegation lineage without logging secrets. Cancellation, debug, and plan/metric access require authorization too. A compromised worker should not assign itself new splits or impersonate another query.

### Propagate cancellation and deadlines

Cancellation is desired state with an epoch and reason. Stop new admission and split assignment, notify tasks, interrupt blocked I/O where safe, abort output commits, and collect exchange/spill after recovery rules allow. A client disconnect is only one possible trigger.

Use deadlines at each layer so an expired query does not remain blocked in catalog, scheduler, exchange, or sink calls. Report incomplete cancellation and forceful termination separately; cleanup must be idempotent.

### Control backpressure end to end

Consumer congestion should reduce exchange reads, producer output, split assignment, and ultimately source admission. Bound every queue: client results, planning jobs, scheduling operations, unacknowledged splits, worker input, exchange buffers, status updates, and metrics.

Avoid positive feedback in which slow consumers create more buffered state, larger heartbeats, slower coordination, false worker suspicion, and retries. Shed optional telemetry before correctness messages, but retain counters that reveal loss.

### Isolate noisy workers and queries

Workers enforce CPU, memory, spill, network, and connector concurrency per task/query/tenant. Coordinator admission is not runtime isolation. A single query with many tiny tasks can overload scheduling/status channels even within byte limits.

Use per-query and per-worker task/split/status rate bounds. Quarantine unhealthy workers and stop new assignment before draining. Preserve enough headroom for cancellation, heartbeat, and recovery traffic during saturation.

### Observe control and data paths

Correlate client request, query epoch, coordinator, plan/fragment, stage, logical task, attempt, worker/incarnation, exchange partition, and commit ID. Measure queue/admission/planning/scheduling latency, RPC rate/size/retry, heartbeat age, reconciliation lag, task startup, exchange buffer/spill, blocked time, worker loss, and recovery.

Use bounded-cardinality labels and sampled traces while retaining exact per-query diagnostic records under policy. Separate coordinator CPU/memory/GC/thread/API/catalog saturation from worker resource and data-plane saturation.

### Roll upgrades and configuration safely

Declare compatibility matrices for task descriptors, plan operators, exchange protocol, serialization, metrics, catalogs, state stores, and security delegation. Coordinators schedule only features understood by selected workers. Drain queries if compatibility cannot bridge versions.

Canary coordinators and workers in bounded pools. Preserve query ownership and epochs during coordinator replacement; preserve incarnation distinction during worker restart. Rollback must understand state written by the new version or prevent it from becoming authoritative.

### Validate distributed failure behavior

Test duplicate, lost, delayed, and reordered control messages; coordinator pause/partition/restart; worker pause/restart/address reuse; catalog slowness; exchange corruption; sink timeout; client retry; and cancellation races. Inject failures at each state transition and commit boundary.

Load-test many small queries, one enormous split graph, skewed coordinators, status storms, slow consumers, and mass worker loss. Assert result correctness, no unauthorized access, bounded memory/queues/retries, terminal-state monotonicity, fair admission, recoverability, and explainable evidence.

## Definitions and Notation

Let query $q$ have coordinator epoch $g_q$, desired-state sequence $s_q$, policy generation $p_q$, catalog snapshot $c_q$, and state $Q_q$ in a declared state machine. Logical task $t$ has attempts $a\in A_t$, each with unique attempt ID and at most one committed output.

Worker $w$ has stable identity $i_w$, process incarnation $r_w$, capability set $K_w$, resource vector $C_w$, and last observed heartbeat event time $h_w$. Suspicion at time $T$ may be $T-h_w>\tau$, but suspicion does not prove the old process has lost access to external systems.

A command identity is $(q,g_q,t,a,s)$ and applies only if its epoch is not stale, its sequence is legal for current state, and its idempotency key is new. An observation is accepted only for matching query epoch, task attempt, and worker incarnation.

Let control load be driven by query rate $\lambda_q$, task rate $\lambda_t$, status rate $\lambda_s$, and mean message costs. Data-plane rate $B_d$ should normally bypass coordinator bandwidth $B_c$. Each queue $x$ has capacity $L_x$ and a declared reject, delay, spill, or backpressure behavior at its bound.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Define ingress, analysis, admission, planning, scheduling, execution, exchange, result, and commit owners.
2. Assign stable query/stage/task/attempt/command, worker-incarnation, coordinator-epoch, policy, catalog, and protocol identities.
3. Specify legal state transitions, durable versus reconstructible state, idempotency, fencing, and terminal commit boundaries.
4. Separate bounded control metadata from direct or dedicated data paths with end-to-end backpressure.
5. Register authenticated compatible workers, treat heartbeats as observations, and reconcile desired versus observed tasks.
6. Assign bounded split windows and fragments under resource, locality, capability, tenant, and failure-domain constraints.
7. Commit one compatible exchange/result attempt and define recovery for worker, coordinator, network, catalog, and sink failure.
8. Enforce admission, runtime isolation, delegation, cancellation, deadlines, and cleanup across every component.
9. Observe correlated state, saturation, retries, recovery, fairness, security, and data-plane outcomes with bounded telemetry.
10. Fault-inject message anomalies, partitions, restarts, overload, and mixed versions before canary and rollback.

Epoch fencing prevents a lower-epoch command from mutating a worker or commit store after a higher epoch is observed. It assumes all effectful endpoints enforce the check; fencing only worker RPC while a stale coordinator can still commit a sink is incomplete.

Idempotent command identity makes duplicate delivery observationally equivalent to one accepted application. It does not make two semantically distinct attempts identical or make non-idempotent external effects safe; those require attempt selection and commit protocols.

Keeping bulk exchange off the coordinator removes processed bytes from its normal bandwidth scaling term, but coordinator work still grows with queries, tasks, splits, status, and manifests. Lazy enumeration, deltas, aggregation, and bounds remain required.

## Alternatives and Trade-Offs

- **Single coordinator:** simple global reasoning; one capacity and failure boundary.
- **Active/standby:** faster service restoration; durable state and fencing remain difficult.
- **Multiple query-owning coordinators:** horizontal control scale; routing, shared admission, and ownership transfer add complexity.
- **Stateless coordinator with external state:** easier replacement; external store latency/load enters the control path.
- **In-memory query state:** fast and simple; long-running work usually dies with the owner.
- **Durable query/task state:** supports recovery; write volume, schema evolution, and reconciliation grow.
- **Push assignment:** low worker polling latency; can overload workers and stale placements.
- **Pull/credit assignment:** natural backpressure; may sacrifice locality or add request chatter.
- **Pipelined exchange:** low latency and storage; couples producer/consumer failures.
- **Materialized exchange:** narrow retries and resilient execution; adds I/O, retention, and commit metadata.
- **Direct client results:** bypass coordinator bandwidth; complicates ordering, security, retry, and client protocol.
- **Coordinator-streamed results:** centralizes semantics; slow clients can consume coordinator resources.
- **Frequent heartbeats:** rapid suspicion and load detail; high control cost and false positives under pauses.
- **Long leases:** tolerate jitter; slow genuine failure detection and reassignment.
- **Shared worker pool:** high utilization; weaker blast-radius and noisy-neighbor isolation.
- **Dedicated pools:** predictable capability/isolation; fragmented idle capacity and more fleet management.

## Failure Modes and Misconceptions

- **“The coordinator is just a router.”** it commonly owns semantics, plans, admission, state, and commits.
- **“Replicas make the coordinator highly available.”** authority, durable state, fencing, and routing must also work.
- **“A heartbeat timeout proves death.”** pauses and partitions create ambiguous liveness.
- **“Hostname identifies a worker.”** a restarted process has lost incarnation-local tasks and buffers.
- **“At-least-once RPC is enough.”** state transitions and external effects need idempotency or commit fencing.
- **“Terminal status can be overwritten by newer time.”** state-machine legality matters more than arrival order.
- **“Workers are interchangeable.”** capabilities, topology, data access, protocol, and resources differ.
- **“The coordinator can relay exchange.”** bulk data makes it a bandwidth and memory choke point.
- **“Small control messages cannot overload.”** task, split, status, metric, and retry cardinality can explode.
- **“Every split should be known up front.”** eager enumeration can exhaust coordinator memory.
- **“Cancellation is one RPC.”** queued, blocked, spilling, exchanging, and committing work must converge.
- **“A successful attempt is visible output.”** selection, manifest, and external commit are separate states.
- **“Worker retry is always transparent.”** pipelined dependents or side effects can widen recovery.
- **“Failover resumes automatically.”** plans, desired state, exchange, admission, and commits need recovery evidence.
- **“Security ends at admission.”** worker data and sink access need scoped delegated authority.
- **“Backpressure belongs only to exchange.”** assignment, status, results, metadata, and sources must participate.
- **“More coordinators fix every bottleneck.”** shared catalogs, admission, discovery, state stores, or giant queries may dominate.
- **“Rolling means compatible.”** mixed plan, exchange, state, and protocol versions require explicit proof.

## Worked Examples

### Example 1

A client times out after submission and retries with the same tenant-scoped key. The ingress returns query `q17` instead of creating `q18`. If the SQL or session digest differs, it rejects the conflicting reuse rather than guessing which request the key means.

### Example 2

Coordinator epoch 8 pauses, epoch 9 takes ownership, and workers observe 9. A delayed epoch-8 cancel is rejected. Without fencing, the old owner could kill replacement tasks even though leader election appeared successful.

### Example 3

Worker `node-4` restarts at the same address. Its incarnation changes from `r12` to `r13`; old task status and exchange buffers are invalid. The coordinator reconciles desired tasks instead of treating the fresh process as continuous with its predecessor.

### Example 4

A table exposes ten million splits. Eager coordinator enumeration consumes memory before scheduling begins. Lazy paged discovery maintains a bounded window per query, advances a snapshot-bound cursor, and stops when worker credits or tenant admission are exhausted.

### Example 5

A slow client stops reading a large result. Result buffers reach their bound, downstream consumption slows, exchange credits close, producers pause, and split assignment contracts. The coordinator retains enough capacity for cancellation and heartbeat rather than buffering the whole result.

### Example 6

Two speculative attempts produce exchange partition 3. A manifest atomically selects one complete checksummed attempt. Consumers never concatenate both, and the loser is collected after the recovery retention window.

### Example 7

A worker disappears during pipelined exchange. Downstream tasks consumed partial pages that cannot be replayed compatibly, so the engine restarts the dependent stage set. With durable committed exchange, it could retry only missing producers or consumers.

### Example 8

A catalog call blocks planner threads for one source. Other catalogs' queries also queue. Per-connector concurrency/timeouts and isolated planning pools contain the fault; adding workers cannot repair coordinator-side metadata saturation.

### Example 9

A new worker version understands operator encoding 6, but the current coordinator can emit only encoding 5. Registration publishes compatibility, and scheduling uses 5. A later coordinator requiring 6 drains old workers before selecting the new encoding.

### Example 10

The fixture demonstrates epoch fencing plus idempotent command application at a worker.

<!-- bijux-verify: {"id":"coordinator-epoch-fencing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=(True, False, False, True)\ncoordinator_epoch=5\ntarget_parallelism=12\n","stderr":""}} -->
```python
current_epoch = 0
applied = set()
target_parallelism = 0

def apply(epoch, command_id, target):
    global current_epoch, target_parallelism
    if epoch < current_epoch or (epoch, command_id) in applied:
        return False
    current_epoch = epoch
    applied.add((epoch, command_id))
    target_parallelism = target
    return True

decisions = (
    apply(4, "q7-1", 8),
    apply(3, "q7-old", 99),
    apply(4, "q7-1", 8),
    apply(5, "q7-2", 12),
)
print(f"accepted={decisions}")
print(f"coordinator_epoch={current_epoch}")
print(f"target_parallelism={target_parallelism}")
```

A real protocol also validates query/task state, sequence legality, worker incarnation, authenticated sender, durable acknowledgment, and fencing at every external effect or commit endpoint.

## Cross-Program Connections

- **Distributed systems:** epochs, leases, fencing, state machines, idempotency, membership, partial failure, and reconciliation define safety.
- **Database systems:** catalogs, snapshots, planning, fragments, exchange, query state, and result commit define semantics.
- **Data engineering:** splits, partitions, connectors, shuffle, skew, spills, and retry boundaries determine execution.
- **Platform engineering:** service discovery, resource groups, placement, autoscaling, isolation, deployment, and observability host the engine.
- **Reliability engineering:** blast radius, recovery point/time, bounded queues, overload, canaries, and rollback constrain architecture.
- **Security:** ingress identity, delegation, least privilege, replay resistance, encrypted channels, redaction, and audit span both planes.
- **Performance engineering:** coordinator throughput, worker utilization, critical path, exchange, backpressure, and cardinality explain scale.
- **Software architecture:** responsibility boundaries, protocol compatibility, durable state ownership, and sharding govern evolution.

## References

1. Trino. [Concepts.](https://trino.io/docs/current/overview/concepts.html) Current server, coordinator, worker, query, stage, task, split, driver, operator, and exchange terminology.
2. Trino. [Deployment.](https://trino.io/docs/current/installation/deployment.html) Current coordinator/worker discovery, configuration, and production deployment guidance.
3. Trino. [Fault-Tolerant Execution.](https://trino.io/docs/current/admin/fault-tolerant-execution.html) Current task retry, exchange manager, spooling, partitioning, and memory behavior.
4. Trino. [Resource Groups.](https://trino.io/docs/current/admin/resource-groups.html) Current query admission, queueing, concurrency, memory, CPU, selection, and distributed resource-group behavior.
5. Trino. [General Properties.](https://trino.io/docs/current/admin/properties-general.html) Current coordinator scheduling, query limits, retry, query-state, and worker-management properties.
6. Apache Spark. [Cluster Mode Overview.](https://spark.apache.org/docs/latest/cluster-overview.html) Current driver, executor, cluster-manager, application, job, stage, task, and deployment concepts.
7. Apache Spark. [Job Scheduling.](https://spark.apache.org/docs/latest/job-scheduling.html) Current application isolation, within-application scheduling, fair pools, dynamic allocation, and executor removal behavior.
8. Apache Spark. [Monitoring and Instrumentation.](https://spark.apache.org/docs/latest/monitoring.html) Current application, job, stage, task, executor, event-log, metric, and history evidence surfaces.
9. Apache Flink. [Flink Architecture.](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/flink-architecture/) Current JobManager, TaskManager, slots, operators, tasks, and deployment architecture.
10. Apache Drill. [Drill Query Execution.](https://drill.apache.org/docs/drill-query-execution/) Current foreman, fragments, exchanges, workers, parallelization, and execution overview.
11. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary account of serving trees, execution dispatch, aggregation, and interactive distributed analysis.
12. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of query coordinator, workers, plan distribution, operators, and production execution.
13. Meta Engineering. [Presto: Interacting with Petabytes of Data at Facebook.](https://engineering.fb.com/2013/11/06/core-infra/presto-interacting-with-petabytes-of-data-at-facebook/) Primary architecture account of coordinators, workers, stages, tasks, splits, operators, and pipelined data flow.

## Exercises

### Exercise 1

Design query, stage, task, attempt, command, coordinator-epoch, and worker-incarnation identifiers for a recoverable engine. State acceptance and deduplication rules for every control message.

### Exercise 2

Classify coordinator state for a one-hour query as durable authoritative, replicated cache, reconstructible from workers/storage, or disposable. Cover plan, admission, split cursor, task desire/status, exchange, metrics, cancellation, and result commit.

### Exercise 3

Design backpressure for a scan-to-exchange-to-slow-client pipeline. Specify bounds, credits, propagation, cancellation reserve, observability, and failure behavior.

### Exercise 4

Compare a singleton coordinator, active/standby, and query-sharded active coordinators for interactive and long-running workloads. Include fencing, routing, state, fairness, overload, and upgrade trade-offs.

### Exercise 5

Design a validation campaign for coordinator/worker protocol changes. Include message anomalies, partitions, pauses, restarts, duplicate effects, overload, security, mixed versions, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Use immutable tenant-scoped query ID, plan generation, stage ID, logical task ID, unique attempt ID, and command sequence/idempotency key. Coordinator ownership obtains monotonically increasing epoch; worker registration uses stable node ID plus random process incarnation. A command carries authenticated sender, query/epoch, task/attempt, sequence, desired transition, and payload digest. Reject lower epochs, wrong incarnations, incompatible plan/protocol generations, duplicate keys with conflicting digests, and illegal state transitions; return the prior result for exact duplicates. Observations must match current query epoch, attempt, and incarnation. Sink/exchange commit keys include attempt and are selected once by fenced authority.

### Answer 2

Persist the query request/idempotency key, session/security/catalog snapshot, plan artifact/version, terminal state, coordinator epoch, admission ownership, cancellation/deadline, selected exchange attempts, and result/sink commit. The split cursor may be durable or reconstructible only if enumeration is deterministic under the same source snapshot; otherwise persist checkpoints. Desired task state must be durable or derivable from the plan plus committed progress. Worker status is a replicated/reconstructible observation reconciled with exchange manifests and live workers. Detailed metrics may be disposable after bounded aggregation, but completion/error and accounting evidence are durable. In-memory scheduling caches are rebuildable. Document the loss and recovery objective for each class.

### Answer 3

Give the client-result queue a byte/page bound and acknowledgments. When full, coordinator or result gateway stops exchange credits. Consumers stop fetching; exchange buffers spill within quota or close producer credits; producers block; split-assignment credits shrink; source reads pause. Bound every edge and reserve control capacity for heartbeat, cancellation, failure, and cleanup. Emit queue occupancy, blocked duration/reason, credits, spill, unacknowledged bytes, client age, and propagation latency. On client timeout or cancel, atomically stop publication, cancel tasks, abort uncommitted result state, and collect after retry retention. Never respond to slow consumption by unbounded coordinator buffering or additional split assignment.

### Answer 4

A singleton gives simple global admission and low state complexity but bounds throughput and loses queries unless clients retry. Active/standby reduces outage only with durable query state, atomic epoch ownership, fenced workers/sinks, and compatible routing; standby capacity is partly idle. Query-sharded active coordinators scale planning/scheduling and isolate many failures, but require stable query routing, shared or coordinated tenant admission, membership, skew handling, state transfer, and per-query fencing. Short interactive workloads may accept singleton query loss behind fast client retry; one-hour queries favor durable state or fault-tolerant exchange. For every topology, bound giant-query state, preserve global fairness, canary mixed versions, drain incompatible plans, and make rollback understand written state.

### Answer 5

Model legal state transitions and protocol compatibility first. Inject duplicate, dropped, delayed, corrupted, and reordered start/split/close/cancel/status/commit messages; coordinator pause, partition, crash, stale return, and failover; worker pause, crash, address reuse, and incarnation change; exchange/sink partial commit; catalog and state-store slowness; client submission retry; and cancellation/completion races. Load many small queries, a huge split graph, slow clients, status storms, and mass worker loss while asserting bounded queues/retries/memory, terminal monotonicity, one selected output, fair admission, and recovery objectives. Test forged/replayed commands and credential expiry. Exercise every supported coordinator/worker version pair, canary a bounded pool, freeze on correctness/security/bound violations, and roll back by compatible state/protocol generation with in-flight reconciliation.
