---
module_id: DE-054
program: Data Engineering
level: 2
module_number: 54
title: Consumer Groups
status: complete
last_verified: 2026-09-03
---

# Consumer Groups

## One-Page Review

### Governing question

How should a set of consumer processes coordinate exclusive partition ownership, liveness, assignment, checkpoint handoff, state transfer, scaling, and failure recovery without allowing stale owners or rebalance churn to corrupt results?

### Essential definitions

- A **consumer group** is one logical consuming application whose live members coordinate to divide a subscribed work set while sharing one progress namespace.
- A **group identifier** names that logical application's subscription/progress state; different group IDs commonly create independent fan-out, while members of one group share work.
- A **member** is one current participant with a protocol identity; a process, host, pod, client ID, and stable instance identity are related but distinct.
- A **subscription** declares the topics/patterns or work domains the group wants; an **assignment** declares which member currently owns each partition/shard.
- An **assignor** computes or helps compute the mapping from eligible partitions and members to owners subject to protocol and balance/locality constraints.
- A **group generation** or **assignment epoch** versions membership and assignment state. Work, progress, state, and effects must be bound to it when stale owners are dangerous.
- A **heartbeat** is protocol evidence that a member session remains participating; it is not evidence that records are being processed correctly or that sinks are healthy.
- A **session timeout** bounds coordinator failure detection; a **processing/poll timeout** bounds how long a member may fail to make required client progress before reassignment.
- A **rebalance** changes ownership because membership, subscription, topology, metadata, or protocol state changed.
- **Eager rebalancing** revokes broad or complete assignments before redistributing; **cooperative/incremental rebalancing** transfers only affected partitions over one or more steps.
- **Static membership** gives a restarting instance a stable group identity to reduce avoidable reassignment under its documented timeout/protocol; it does not grant permanent ownership.
- **Revocation** is a planned request to relinquish ownership; **loss** means ownership may already have moved, so the old member cannot safely publish or commit as owner.
- A **lease** is time/version-bounded authority to process a shard or partition; renewal suggests liveness, while a monotonically changing token/counter can fence stale holders.
- A **handoff checkpoint** binds the last accepted progress/state/effect boundary of an old owner to the starting boundary of a new owner.
- **Assignment stickiness** minimizes movement across rebalances; **balance** distributes work. They are objectives, not correctness, and can conflict with locality or heterogeneous capacity.

### Central model, mechanism, or theorem

For group $G$ in assignment epoch $g$, let eligible partitions be $P_g$ and live members $M_g$. An assignment is a partial function

$$
A_g:P_g\to M_g.
$$

Correct active ownership requires complete exclusive coverage for partitions intended to run:

$$
\forall p\in P_g:\quad |\{m:A_g(p)=m\}|=1.
$$

When $p$ moves from $m$ in epoch $g$ to $m'$ in $g+1$, safe handoff requires the old owner to stop/fence, a durable checkpoint/state/effect boundary $c_p$ to be selected, and the new owner to restore from that boundary before publishing. Because failure can prevent graceful revocation, correctness cannot depend solely on the old process cooperating. Every ownership-sensitive write must prove a current epoch/lease token or be idempotent/reconcilable under the delivery contract.

### Critical invariants

- Group ID means one durable logical consumer purpose; deployments that should fan out use separate progress identities, while replicas sharing work use the same intended group.
- Topic generation, subscription, complete partition set, member identities, protocol type/version, assignor, group generation, assignment, and checkpoint schema are recorded together.
- At most one current owner may publish ownership-sensitive state/effects for a partition epoch; stale owners are fenced at the state/sink boundary, not merely removed from coordinator metadata.
- Every assigned partition has an initialization boundary and every revoked partition has a bounded stop/checkpoint/flush policy; lost partitions do not perform unsafe final commits.
- Checkpoints never advance beyond accepted state/effects and include group/application generation, topic/partition identity, code/schema/state version, and ownership token where required.
- Heartbeats and polling remain timely without masking wedged processing; application progress, oldest work, state/checkpoint health, and sink acceptance are monitored separately.
- Rebalance triggers, protocol, callbacks, timeouts, retries, and failure paths are understood; correctness never assumes graceful callback execution after crash, pause, partition, or process kill.
- Eager versus cooperative behavior is not mixed incompatibly during rollout; protocol/assignor migration follows a supported staged path with rollback evidence.
- Stickiness does not retain an invalid/stale owner, and balance does not split an ordered partition or overload a weaker member; assignment objectives are capacity-aware where necessary.
- Scaling is bounded by partitions/order domains and by the slowest state/sink/resource path; more members than assignable partitions may legitimately be idle.
- State follows the partition through verified checkpoint/changelog/snapshot restoration; in-memory caches never silently disappear or overlap at handoff.
- Rolling deploys, autoscaling, host drains, topology changes, credential expiry, long pauses, oversized records, and downstream outages do not create unbounded rebalance loops.
- Group metadata and administrative operations are least-privileged and audited; group IDs, member identities, host details, subscriptions, and lag can reveal sensitive topology.
- Drills verify join, planned leave, crash/loss, network pause, slow processing, coordinator failure, partition expansion, protocol migration, state restore, and stale-owner rejection.

### Common failures

Common failures include giving every replica a unique group ID and accidentally broadcasting every record; reusing one group ID for unrelated applications and accidentally load-balancing between them; confusing client ID with group ID; treating heartbeat success as healthy processing; blocking the poll/event loop on slow work; setting timeouts without measuring processing and pauses; committing fetched rather than accepted progress; assuming revocation callbacks always run; performing a final write after ownership is already lost; restoring from a stale checkpoint while the old owner still writes; choosing eager assignment for huge state without accounting for stop-the-world movement; enabling cooperative assignment on only part of a group; expecting static membership to prevent failure reassignments; autoscaling on aggregate lag until rebalances dominate; and assuming equal partition counts imply equal work.

### Compact example

Generation 8 assigns six partitions evenly to workers A, B, and C. B leaves. A cooperative generation 9 retains A's partitions 0 and 3 and C's 2 and 5, moving only B's partitions 1 and 4—two moves instead of six eager revocations. A and C each own three partitions, complete exclusive coverage holds, and the new owners restore partitions 1 and 4 from durable next offsets 80 and 40. Any write carrying generation 8 after assignment 9 is rejected. This finite model proves assignment arithmetic only, not broker coordination, state correctness, delivery semantics, or production capacity.

### Connections

[DE-052](052-topics-partitions-and-offsets.md) defines partition identities, offset vectors, lag, and topology epochs. [DE-053](053-producer-keys-and-ordering.md) establishes local order and producer fencing. [DE-044](044-retries-timeouts-and-idempotency.md) supplies attempt/effect discipline; [DE-049](049-run-metadata-and-operational-state.md) supplies authoritative state. DE-055 and DE-056 will couple group progress to delivery and effects; DE-059 will develop stateful stream restoration.

## Governing Question

A single consumer can read one or several partitions, but it offers limited throughput and becomes an availability bottleneck. Running replicas helps only when they agree which partitions each owns, where each should resume, and when an old owner must stop. Consumer groups provide this coordination, but the group protocol itself does not complete the application's correctness proof.

At any moment a coordinator has some view of group membership and assignment. Networks are delayed, processes pause, hosts fail, deployments overlap, and workers can keep executing after their session expires. Therefore two processes can temporarily believe they own the same partition. The coordinator's new assignment establishes current protocol authority; external state and sinks must reject or safely tolerate the stale process.

Rebalancing is the transition between assignments. It can improve balance, recover from failure, add capacity, or reflect new partitions. It also interrupts work, moves state, changes caches/connections, and creates a progress boundary. A high-throughput group can spend most of its time rebalancing if membership is unstable or processing blocks liveness.

The group ID is data architecture, not a deployment label. Members using the same group divide one logical subscription and checkpoint namespace. Different groups independently consume the stream. A mistaken ID can turn intended fan-out into work sharing or intended work sharing into duplicate fan-out.

This chapter treats groups generically through membership, assignment, leases, epochs, and handoffs, then uses Kafka, Pulsar, Kinesis, and Pub/Sub as concrete but different mechanisms. It does not pretend their subscription and delivery models are interchangeable.

## Why This Matters

Consumer groups allow horizontal consumption without splitting source topics per replica. They recover partition work when a member fails, rebalance as instances scale, and retain logical progress across process lifetimes. This is foundational for continuously operating transformations, projections, CDC sinks, alerts, and integrations.

The parallelism is bounded. Six partitions offer at most six independently assigned ordered domains in the common partition-owner model. Ten replicas may leave four idle. One hot partition can still dominate. Downstream database locks, state stores, APIs, or checkpoints can constrain useful concurrency below the partition count.

Membership changes have real cost. Eager protocols may revoke all partitions for a rebalance. Stateful consumers must flush or checkpoint, release resources, and restore elsewhere. Cooperative protocols reduce movement but introduce incremental transitions that applications must implement correctly. Sticky placement reduces warmup but can preserve load imbalance.

Failure detection trades availability against false suspicion. Short sessions move work quickly after a crash but evict members during garbage collection, CPU starvation, network jitter, or slow processing. Long sessions reduce churn but delay recovery. Separating heartbeat/control activity from data processing helps, but can leave a member “alive” while application progress is stuck.

Exactly one current assignment is not exactly-once processing. A worker can produce an effect and die before checkpointing; the next owner repeats the record. A stale owner can write after reassignment. A checkpoint can advance before a sink commits. Consumer groups distribute and recover work; delivery/effect correctness needs the protocols in DE-055 and DE-056.

State makes handoff harder. A stateless filter can restart cheaply. A keyed aggregation may restore gigabytes before catching up. Moving many partitions simultaneously can overwhelm changelog storage, object storage, network, or sinks. Assignment should account for state locality and recovery capacity, not only partition counts.

Groups are an operational control plane. Group descriptions reveal applications, members, hosts, assignments, lag, and topics. Resetting offsets changes data outcomes. Deleting group state can make consumers replay or skip. Access, audit, guarded commands, privacy, retention, and incident procedure belong in the design.

## Prerequisites and Retrieval

Retrieve the consumer product contract: logical application purpose; input topic generations; expected outputs/effects; fan-out versus work sharing; ordering domain; freshness/availability; state; delivery/effect semantics; replay; degraded mode; owner/on-call; and recovery objectives.

Retrieve group identity: group/subscription/application name; immutable generation if names can be reused; environment/tenant/region; protocol type/version; coordinator or lease store; authorization; offset/checkpoint store; retention; and creation/deletion/reset history.

Retrieve membership: dynamic member ID; stable instance ID if used; client ID; process/pod/host; deployment/code/config/schema/state version; start/session epoch; subscription; rack/zone/locality; capacity class; heartbeat and poll/progress state; credentials; and shutdown lifecycle.

Retrieve assignment semantics: eligible topics/partitions/shards; discovery timing; assignor and configuration; eager/cooperative/incremental behavior; stickiness/balance/locality objectives; heterogeneous capacity; maximum ownership; standby/warm state; and assignment/generation tokens.

Retrieve liveness: heartbeat thread/event loop; interval; session/failover timeout; poll/processing interval; request timeout; coordinator reachability; clock behavior; GC/runtime pauses; CPU/memory pressure; network failure; container termination grace; and library-specific ownership-loss signals.

Retrieve processing lifecycle: assignment initialization; start position; state restore; cache/connection setup; pause/resume; fetch/in-flight limits; batch duration; checkpoint cadence; sink acceptance; revocation callback; lost-ownership callback; shutdown; and cleanup. Determine which actions require current ownership.

Retrieve state and progress: beginning/head/read/processed/state-durable/sink-accepted/committed/published frontiers per partition; checkpoint schema and next-offset convention; state snapshot/changelog identity; ownership epoch; conditional-write support; recovery time; corruption response; and external effect receipts.

Retrieve change triggers: member join/leave/crash; rolling deploy; autoscaler; orchestration restart; subscription/pattern match change; partition expansion; credential/ACL change; coordinator migration; protocol/assignor upgrade; state incompatibility; and manual rebalance/reset.

Retrieve operational evidence: active members, assigned/unassigned/duplicated partitions, group state/generation, rebalance count/rate/latency/failures/reasons, assignment movement, heartbeat/session failures, processing/poll interval, lag/freshness, oldest work, state restore time/bytes, checkpoint errors, lost ownership, stale write rejection, and sink capacity.

Retrieve governance: who may join/read/commit/reset/delete/describe groups; topic and group ACL interaction; tenant isolation; sensitive member host/client metadata; TLS/credentials; offset/checkpoint retention; audit; break-glass; and incident approvals.

Distinguish group from member; logical application from deployment; group ID from client/instance ID; subscription from assignment; eligible partition from owned partition; leader election from consumer rebalance; liveness from progress; heartbeat from health; session expiration from graceful leave; revocation from loss; assignment generation from code release; lease expiry from fencing; fetch position from durable checkpoint; checkpoint from state/effect acceptance; eager from cooperative; sticky from static; balance by count from balance by work; active owner from standby state; pause from leave; fan-out from load balancing; and reset from repair.

Create a group contract:

| Concern | Required decision and evidence |
|---|---|
| Purpose | One logical consumer/output contract and intended fan-out/work sharing |
| Identity | Group/subscription generation, member/dynamic/stable/client identities |
| Inputs | Exact topic generations, subscription/pattern, complete partition set |
| Protocol | Coordinator/lease store, version, heartbeats, sessions, join/leave |
| Assignment | Assignor, exclusive scope, balance/stickiness/locality/capacity objectives |
| Handoff | Revoke/lost/assign lifecycle, stop, checkpoint, state, resources, fencing |
| Progress | Read/process/state/sink/commit/publish frontiers and boundary convention |
| State | Snapshot/changelog, restore time, compatibility, standby/locality, corruption |
| Scale | Partition/work limits, heterogeneous members, downstream and recovery capacity |
| Operations | Rebalance SLO, metrics, deployment/autoscale policy, reset and drills |
| Security | Join/read/commit/admin rights, tenant isolation, secrets and audit |
| Recovery | Crash, stale owner, expired session, coordinator/store loss, archive/replay |

Write a testable claim: “For group generation $g$, every eligible partition has one current owner with assignment token $(G,g,p)$; the owner restores from the last accepted handoff checkpoint before publishing, checkpoints only accepted state/effects, stops or is fenced when revoked/lost, and the new owner cannot overlap unsafe writes. Membership change moves only the partitions required by the selected protocol/objectives, completes within the freshness budget, and preserves replay margin.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish group, subscription, member, client, instance, assignment, lease, coordinator, and checkpoint identities;
2. explain fan-out versus work sharing and predict the consequences of group-ID reuse or proliferation;
3. model assignment as exclusive partition ownership versioned by group generation or lease token;
4. compare eager, sticky, cooperative/incremental, static-membership, and lease-based coordination;
5. design safe assignment, revocation, lost-ownership, state restore, checkpoint handoff, and stale-owner fencing;
6. tune and test heartbeat, session, poll/processing, graceful-shutdown, and failover boundaries using measured pauses and objectives;
7. reason about partition-limited parallelism, skew, heterogeneous capacity, state locality, restore storms, and downstream limits;
8. design rolling deployments, autoscaling, partition changes, protocol migrations, and regional recovery without rebalance storms;
9. specify monitoring, security, privacy, administrative, test, and incident controls for groups; and
10. state precisely what consumer-group coordination does not prove about delivery, exactly-once effects, domain correctness, or end-to-end freshness.

## Core Exposition

### Decide fan-out versus shared work

One logical application typically uses one progress namespace. Its replicas share the group/subscription so each partition or message work item is assigned to one member according to the service model. A separate application with independent outputs uses a separate group/subscription so it sees its own logical copy of the stream.

If analytics and fraud detection accidentally share `orders-consumer`, each receives only part of the input. If five replicas accidentally use pod-specific group IDs, all five may consume the full stream and multiply effects. Encode stable domain purpose and environment in group identity, not replica name or deployment sequence.

Some services allocate partitions exclusively; others load-balance individual messages under acknowledgement leases; some offer subscription modes such as exclusive, failover, shared, or key-shared. State the work unit and order guarantee. Do not use “consumer group” to erase material differences.

Group creation and deletion are governed lifecycle events. Names can outlive deployments, checkpoint history can expire, and a recreated name may resume unexpectedly or start anew. Catalog owner, purpose, topics, progress, retention, and generation.

### Separate member identities

A dynamic member ID identifies one protocol session. It can change on restart or rejoin. A client ID identifies telemetry/client configuration and need not be unique enough for ownership. A pod/host/process ID describes infrastructure. A stable instance ID can let a protocol recognize a restarting logical instance. None alone is a universal fencing token.

Bind runtime metadata: deployment/code/state schema, region/zone/rack, capacity, and startup epoch. This supports diagnosis and assignment locality. Avoid putting secrets or unnecessary personal host/operator data in IDs because group metadata may be widely describable.

Static membership can reduce churn when a process restarts within the applicable session behavior, but a truly failed instance must still lose work. Duplicate stable IDs must fail safely. Static identity is operational continuity, not permanent partition ownership or proof that local state is current.

Authenticate every member and authorize its topic/group operations. A compromised member can read data, commit progress, trigger churn, or hold assignments while doing no useful work.

### Model assignment as epoch-scoped authority

For each group epoch, assignment maps partitions to current members. A valid assignment covers all intended partitions exactly once; temporarily unassigned partitions may be part of a transition but must be visible. Assignment is not merely a scheduling hint when state or effects depend on exclusive ownership.

Carry a generation/epoch or monotone lease counter into ownership-sensitive writes. A state row or publication pointer can condition updates on `(group generation, partition)`. When a new owner receives generation 12, writes from generation 11 fail even if the old process resumes.

Coordinator membership alone cannot fence external databases or APIs. If the sink lacks conditional fencing, make effects idempotent by stable occurrence/output identity, write through a fenced transactional state store, publish isolated generations, or reconcile. The exact delivery/effect strategies follow in DE-055 and DE-056.

Assignment metadata should include topic generation and partition topology. Partition number 3 in a recreated topic is not the old work domain. New or retired partitions require explicit initialization/terminal checkpoints.

### Understand why rebalances occur

Expected causes include first member join, additional capacity, graceful leave, crash/session expiry, subscription change, new topic matching a pattern, partition expansion, assignor/protocol change, and coordinator recovery. Unexpected causes include liveness starvation, network churn, credential failure, duplicate instance identity, client bugs, or automation oscillation.

Each rebalance has a reason, previous/new generation, old/new membership, old/new assignment, moved partitions, duration, callbacks, lost owners, and state/checkpoint work. Retain these as operational events. A raw counter without cause is hard to improve.

Avoid using a rebalance as a general refresh mechanism. Frequent membership scaling can cost more than it saves. Batch deployments, apply stabilization/cooldown, use minimum healthy duration, and scale from sustained per-partition work/freshness rather than noisy aggregate lag.

Topic-pattern subscriptions can change when topics appear. This makes topic creation a workload/assignment event. Constrain patterns and test authorization, schema compatibility, topology, and state initialization.

### Compare eager and cooperative handoff

In eager rebalancing, members revoke their full or broad assignment, the group computes a new mapping, and partitions restart. This offers a simple no-overlap phase but pauses unaffected work and can cause large state restore/cache churn.

Cooperative or incremental protocols retain unaffected assignments and transfer only partitions that must move. This reduces disruption and preserves warm state, especially for large groups. Ownership transfer can require multiple protocol steps: revoke from old owner, then assign to new owner after release is known.

Cooperation does not remove failure. An old owner may crash before revocation or lose its session without receiving a callback. The new owner must still be safe. Treat `revoked` as a graceful chance to checkpoint and `lost` as already non-authoritative.

All members must use a compatible protocol/assignor during migration. Apache Kafka documents distinct classic and newer consumer protocols and a supported migration path; its classic cooperative assignor also requires coordinated rollout. Do not flip one instance and hope negotiation is harmless.

### Choose assignment objectives

Balance by partition count minimizes count difference but ignores work. One partition may contain most bytes, state, or sink calls. Capacity-aware assignment needs trusted per-partition costs and member capacities, but those measurements change and can cause movement.

Stickiness minimizes partition movement and preserves caches/state locality. It can retain skew or unhealthy placement. Rack/zone affinity reduces restore/network cost but may conflict with failure-domain spread or data residency. Define priorities and constraint violations.

Range-style assignment can cluster contiguous partitions by topic and leave imbalance when members subscribe to several topics. Round-robin/uniform approaches can improve counts but increase movement or cross-topic distribution. Product/protocol details vary; test actual assignments on representative topologies.

Standby/warm replicas can reduce restore time for stateful tasks but consume storage, network, and compute. They need freshness and promotion/fencing semantics and are not active owners.

### Treat liveness as a failure detector

Heartbeats tell the coordinator a member session is responsive under the protocol. They cannot prove that application logic advances, checkpoints succeed, outputs are correct, or downstream systems accept writes. Monitor control-plane liveness and data-plane progress separately.

Session timeout determines how long missing liveness evidence is tolerated before work moves. Detection plus assignment plus restore plus catch-up form recovery time. A short timeout reduces detection delay but raises false eviction under network/CPU/runtime pauses.

Some consumer protocols couple polling/application calls to membership. A member that does not poll within a maximum interval may be considered failed even if background heartbeats continue. This protects the group from a live process that holds partitions without processing. Retrieve the exact client/protocol threading model.

Bound per-record/batch execution below the processing/poll budget with margin. Move long work to controlled executors, pause fetch while retaining required liveness, split oversized work, checkpoint safely, and cap in-flight records. Do not merely raise timeouts until failure detection becomes useless.

### Design planned revocation

On graceful revocation, stop accepting new work for affected partitions, drain or cancel bounded in-flight work according to effect semantics, persist accepted state/checkpoint, release partition-scoped resources, and acknowledge handoff. Enforce a deadline shorter than termination grace/session behavior.

Do not block forever flushing a failed sink. Choose a durable checkpoint before uncertain effects, persist receipts for reconciliation, or abandon candidate work safely. The group must regain availability without lying about completion.

Kafka's `ConsumerRebalanceListener` distinguishes assigned, revoked, and lost callbacks. Its documentation notes that lost partitions may already belong to another member and therefore unsafe commits should not be attempted. Callbacks are notifications; exceptions do not veto assignment. Application code must honor these semantics.

Log old/new owner, generation, partition, last fetched/processed/state/sink/committed positions, in-flight count, and cleanup outcome. Avoid payloads and sensitive keys.

### Survive ungraceful loss

A crash, kill, host loss, long pause, or network partition may prevent revocation. The coordinator eventually assigns the partition elsewhere. The old process can later resume. Therefore safety must not depend on `finally` blocks or graceful callbacks.

The new owner restores from the last accepted checkpoint and may repeat uncheckpointed work. State/effects must tolerate that according to the delivery contract. The old owner, once it learns of loss, stops and performs only cleanup that cannot overwrite current state.

External writes include the ownership token in a conditional update when possible. A monotone group generation, lease counter, or application fencing epoch prevents stale updates. Beware protocols whose group generation is not stable/exposed for direct sink fencing; create an application-owned monotone token at assignment.

If fencing is impossible, isolate candidate output per run/epoch and publish conditionally, or use stable idempotency keys and reconciliation. Document residual overlap risk.

### Couple checkpoints to ownership

DE-052 defined next-offset checkpoints. A group adds ownership context. Checkpoint record should identify application/group generation, topic generation, partition, next offset, code/config/schema/state version, state snapshot/changelog, sink receipt boundary, and ownership token.

Only the current owner advances it, using compare-and-set on the previous token/version where possible. A stale owner must not overwrite a newer checkpoint with a lower or incompatible position. Monotonic offset alone is insufficient if code/state generations differ or corrections permit nonmonotone repair.

On assignment, load and validate the checkpoint before fetching/publishing. Confirm it is within retention, matches state, and belongs to the expected topic/topology. Restore state, replay to an accepted boundary, warm dependencies, then mark readiness. Assignment callback completion alone is not application readiness.

Automatic periodic commits can be convenient for stateless, duplicate-tolerant consumers but may decouple progress from effects. Never let fetch position advance the durable claim accidentally. DE-055 compares delivery placements.

### Move state deliberately

Stateful ownership includes local database files, caches, timers, changelog positions, external locks, and publication identity. Inventory which state is authoritative, reconstructible, or merely a cache. Verify compatible serializers and code.

Restore time depends on state bytes, storage throughput, partition count, locality, checkpoint age, changelog tail, and concurrent restores. A rebalance that moves many partitions can create a restore storm and breach freshness even when steady processing has headroom.

Sticky assignment and planned drains reduce movement. Warm standbys or shared remote state reduce recovery time with cost/consistency tradeoffs. Snapshot less frequently to reduce write load only if longer replay remains within recovery/retention objectives.

Do not allow old local state to masquerade as current merely because the same static instance returns. Validate checkpoint/state generation and reconcile with the group assignment. Delete or quarantine incompatible/corrupt state safely.

### Scale within real parallelism

For $|P|$ exclusively assigned partitions and $|M|$ homogeneous members, active useful owners are at most $\min(|P|,|M|)$. More members can improve failover standby but not active partition concurrency. One member may own several partitions.

Count balance target is approximately $\lfloor |P|/|M|\rfloor$ or $\lceil |P|/|M|\rceil$, but work can be uneven. Track maximum member CPU/memory/state/sink demand and slowest partition. Heterogeneous instances need capacity-aware constraints or separate groups/workloads.

Scale-out benefit must exceed rebalance and restore cost. If adding one member moves two 500 GiB state partitions and saves little throughput, it can worsen freshness for hours. Forecast assignment movement before applying autoscaling.

Scale in uses planned draining: mark member non-ready for new ownership, trigger/await cooperative revocation where supported, checkpoint/transfer state, verify new owners, then terminate. Orchestrator termination grace must cover the bounded handoff, with crash-safe fallback.

### Prevent rebalance storms

Symptoms include high rebalance rate/latency, constantly changing members, repeated state restore, low useful throughput, volatile lag, coordinator errors, and deployments that never settle. Find triggers rather than raising timeouts blindly.

Common causes are processing beyond poll interval, long GC, CPU throttling, memory kills, flaky network/DNS, credentials, duplicate stable IDs, autoscaler oscillation, health probes killing warmup, pattern-discovered topics, partition changes, incompatible assignors, and shutdown shorter than revocation.

Stabilize resources and work bounds; separate startup/liveness/readiness probes; use disruption budgets; batch rollouts; add cooldown and minimum membership duration; pause autoscaling during incidents/migrations; use cooperative/sticky behavior where appropriate; and provision coordinator/checkpoint stores.

Readiness should remain false until assignment and required state restore complete. Liveness should not kill a healthy long restore if progress is observable, but must detect a genuinely wedged member. Startup probes can protect initialization.

### Compare other subscription and lease models

Apache Pulsar subscription modes illustrate different allocation scopes: exclusive/failover choose active consumers differently, shared distributes messages without general ordering, and key-shared keeps a key with one consumer under documented routing conditions. These are not identical to one-owner-per-partition Kafka groups.

Amazon Kinesis Client Library coordinates workers with shard leases stored alongside checkpoints in a DynamoDB lease table. One worker holds a shard lease at a time, and lease/state metadata supports reassignment. Reshard lineage adds parent/child lifecycle. Lease-store throughput and availability become part of the consumer control plane.

Google Pub/Sub permits multiple subscribers on one subscription to receive load-balanced subsets and uses per-message acknowledgement deadlines/lease extensions rather than exposing a Kafka-style partition assignment to the application. A missed deadline can cause redelivery. The shared concept is bounded ownership of work; the unit and guarantees differ.

Design portable abstractions around logical application, work identity, authority token/lease, progress/effect boundary, handoff, and retry—not around method names that imply false equivalence.

### Deploy and migrate group protocols safely

A rolling code release changes members and can trigger assignments while old/new schemas coexist. Verify state backward/forward compatibility, output compatibility, checkpoint format, and rollback. Canary by partitions only when outputs/state remain separable and the assignor can preserve the boundary.

Use static identity carefully with orchestration: two pods must not claim the same instance ID during overlap. Ensure termination and replacement ordering or rely on protocol rejection/fencing. Do not derive stable identity from ephemeral addresses.

Protocol or assignor migration follows vendor-supported sequencing. Test mixed-version negotiation, callbacks, movement, group metadata, lag, rollback, and operational tooling. Apache Kafka 4.3 documents classic and newer consumer protocols with different ownership of heartbeat/session and assignment configuration; inventory which one is active before tuning.

When input partitions expand, the group must discover and assign new partitions with explicit initial offsets/state. Capacity increases only if members/sinks can process them. Old state routing and producer key changes remain separate migrations.

### Observe the ownership state machine

Expose group state/protocol/generation, coordinator health, member count/identity/version/capacity, subscription, full assignment, unassigned/duplicate ownership, and partition movement. Correlate every partition with read, processed, state, sink, commit, and publication frontiers.

Measure rebalance count/rate/reason, join/assignment/revoke/lost timing, moved partitions and state bytes, restore/catch-up duration, heartbeat latency/failure, time since useful progress, poll/processing maxima, checkpoint errors, and stale-write rejections.

Separate expected deployment rebalances from pathological churn. Alert on sustained instability, not every membership event, but record each event for audit. Page when freshness/replay margin, duplicated/unassigned ownership, state corruption, or fencing failures threaten correctness.

Kafka exposes rebalance count/rate/latency and other coordinator metrics; service tools can describe members and assignments. Treat tool output as control-plane evidence, not proof of output correctness.

### Secure administrative operations

Least privilege separates topic read, group join/describe, progress commit, offset reset, group deletion, and coordinator/lease-table administration. A read-only observer should not reset production. A consumer should not join another tenant's group or overwrite its checkpoints.

Reset and deletion commands identify exact group generation, topic generation, partitions, old/new vectors, state/effect implications, replay/skip estimate, approval, dry run, reconciliation, and rollback. Pause/fence members before mutation and verify after restart.

Protect lease/checkpoint stores from broad writes. Conditional/versioned updates and audit logs are correctness controls. Backup/restore group metadata with topic/state coordinate mapping and exercise recovery.

Member hostnames, client IDs, subscriptions, lag, and error samples may reveal sensitive operations. Restrict describe APIs and telemetry, minimize labels, and avoid payload/business keys in group metadata.

### Test transitions, not just steady state

Unit/model tests generate membership sets and assert complete exclusive assignment, allowed imbalance, minimal movement objectives, stable tie-breaking, and capacity constraints. Property tests ensure no partition has two current assignment tokens.

Integration tests cover first join, second join, graceful leave, abrupt kill, long pause, network partition, lost callback, stale owner resume, coordinator failover, checkpoint-store timeout, assignment callback error, and incompatible state. Assert external stale writes are rejected.

Load tests measure steady capacity plus rebalance/restore cost under realistic state and skew. Inject rolling deployments, autoscaler changes, large batches, GC/CPU throttle, sink slowdown, and partition expansion. Measure useful accepted throughput, not fetch rate.

Recovery tests corrupt/delete checkpoints, expire source retention, restore lease/group metadata, replay from archive, and reconcile sinks. Protocol migration tests follow the exact staged path and roll back.

### Review the complete handoff argument

A group review should establish identity, eligible work, membership, assignment, liveness, handoff, progress, state, capacity, fencing, operations, and governance as one system. A green “stable group” status only says the coordinator is not currently transitioning.

For each partition ask: who owns it now, under which generation/token, where did ownership begin, which state is loaded, what work is in flight, what checkpoint/effects are accepted, how will revocation/loss behave, and how will the sink reject stale ownership?

For the group ask: why is this one logical consumer, which applications fan out separately, what triggers movement, what is the measured rebalance/restore budget, how does deployment/autoscaling avoid churn, and what recovery exists after coordinator/checkpoint corruption?

State limitations explicitly: consumer coordination can assign one worker, yet duplicates, omissions, stale business versions, late data, or incorrect effects can still occur. The next modules build those semantic guarantees.

## Definitions and Notation

Let $G$ be a logical group/application generation, $g$ its current assignment epoch, $M_g$ live eligible members, and $P_g$ eligible partitions. Assignment

$$
A_g:P_g\to M_g
$$

has exclusive complete coverage when every active $p$ maps to exactly one member. Let owned set of member $m$ be $O_g(m)=\{p:A_g(p)=m\}$.

Movement from $g$ to $g+1$ is

$$
\Delta_g=\{p\in P_g\cap P_{g+1}:A_g(p)\ne A_{g+1}(p)\},
$$

plus newly eligible and retired partitions. Stickiness minimizes $|\Delta_g|$ subject to membership, balance, capacity, locality, and protocol constraints.

Count load is $n_m=|O_g(m)|$. For homogeneous members, count imbalance can be

$$
B_g=\max_m n_m-\min_m n_m.
$$

Real work load uses weights $w_p$ and member capacity $C_m$:

$$
W_m=\sum_{p\in O_g(m)}w_p,\qquad W_m\le C_m.
$$

Let $h$ be heartbeat interval, $s$ session/failover timeout, $q$ maximum processing/poll interval where applicable, $d$ failure-detection delay, $a$ assignment delay, $r_p$ restore duration, and $c_p$ catch-up duration. Recovery for partition $p$ is approximately

$$
T_p=d+a+r_p+c_p,
$$

subject to coordinator/store/network and workload assumptions.

Let checkpoint $K_{G,g,p}$ contain next source position, state identity, accepted-effect boundary, code/schema/config generation, and ownership token $f_{G,g,p}$. A write is ownership-valid only if its token is accepted as current. Revoked ownership may finalize under the old token within protocol ordering; lost ownership cannot assume that privilege.

## Mechanisms, Invariants, or Proof Structure

Use this group review chain:

1. **Establish logical purpose.** Prove the group represents one consumer/output contract and that independent applications use independent progress identities.
2. **Establish identities.** Bind group generation, topic generations, dynamic/stable/client/runtime members, protocol, assignor, and checkpoint schema.
3. **Establish eligible work.** Enumerate subscribed partitions/shards/messages and their topology/retention boundaries.
4. **Establish exclusive assignment.** Verify complete coverage, no duplicate current owner, explicit transition gaps, and documented balance/stickiness/locality constraints.
5. **Establish liveness.** Show heartbeat/session/poll behavior survives measured pauses but detects failed or wedged members within the recovery objective.
6. **Establish handoff.** Bound stop/drain/checkpoint/state release on revocation and fail safely when callbacks are missed or ownership is already lost.
7. **Establish progress/state.** Couple checkpoint to accepted state/effects and restore/validate before the new owner publishes.
8. **Establish fencing.** Reject old generations/lease counters at every ownership-sensitive state/publication/effect boundary or prove idempotent reconciliation.
9. **Establish capacity.** Test skewed steady load, failure, restore storms, catch-up, downstream limits, scaling movement, and replay margin.
10. **Establish operations/governance.** Monitor transitions, control deploy/autoscale/reset/delete, protect metadata, audit authority, and drill recovery.

The ownership invariant is:

> For each partition and assignment epoch, at most one current token can authorize ownership-sensitive state or effects; coordinator reassignment invalidates stale authority even if the process still runs.

The handoff invariant is:

> A new owner begins from a validated accepted checkpoint/state boundary, while the old owner has either relinquished work gracefully or is fenced; callback success is an optimization, not a safety premise.

The progress invariant is:

> Group commits never exceed accepted state/effects and cannot be overwritten by stale owners or confused across topic, group, code, state, or topology generations.

The operability invariant is:

> Membership, rebalance, restore, and catch-up complete within freshness/retention budgets under measured failure and skew, without unstable automation causing repeated movement.

This executable compares one cooperative handoff with a full eager revocation. It models assignments and tokens, not a real coordinator.

<!-- bijux-verify: {"id":"consumer-group-handoff","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"generation_before=8\ngeneration_after=9\nassignment_before=(('worker-a', (0, 3)), ('worker-b', (1, 4)), ('worker-c', (2, 5)))\nassignment_after=(('worker-a', (0, 1, 3)), ('worker-c', (2, 4, 5)))\nrevoked_from_worker_b=(1, 4)\nretained_by_survivors=(0, 2, 3, 5)\ncooperative_moves=2\neager_revocations=6\nexclusive_assignment=True\ncomplete_coverage=True\nbalance_gap=0\nhandoff_starts=((1, 80), (4, 40))\nstale_generation_fenced=True\n","stderr":""}} -->
```python
generation_before = 8
generation_after = 9
partitions = tuple(range(6))

before = {
    "worker-a": (0, 3),
    "worker-b": (1, 4),
    "worker-c": (2, 5),
}
after = {
    "worker-a": (0, 1, 3),
    "worker-c": (2, 4, 5),
}
checkpoints = {0: 120, 1: 80, 2: 50, 3: 90, 4: 40, 5: 70}


def owner_map(assignment):
    return {
        partition: member
        for member, owned in assignment.items()
        for partition in owned
    }


before_owner = owner_map(before)
after_owner = owner_map(after)
moved = tuple(
    partition
    for partition in partitions
    if before_owner[partition] != after_owner[partition]
)
retained = tuple(
    partition
    for partition in partitions
    if before_owner[partition] == after_owner[partition]
)
all_after = tuple(partition for owned in after.values() for partition in owned)
handoff_starts = tuple((partition, checkpoints[partition]) for partition in moved)
load_counts = tuple(len(owned) for owned in after.values())

print(f"generation_before={generation_before}")
print(f"generation_after={generation_after}")
print(f"assignment_before={tuple(sorted(before.items()))}")
print(f"assignment_after={tuple(sorted(after.items()))}")
print(f"revoked_from_worker_b={moved}")
print(f"retained_by_survivors={retained}")
print(f"cooperative_moves={len(moved)}")
print(f"eager_revocations={len(partitions)}")
print(f"exclusive_assignment={len(all_after) == len(set(all_after))}")
print(f"complete_coverage={tuple(sorted(all_after)) == partitions}")
print(f"balance_gap={max(load_counts) - min(load_counts)}")
print(f"handoff_starts={handoff_starts}")
print(f"stale_generation_fenced={generation_before < generation_after}")
```

The model assumes a known graceful departure and valid checkpoints. It does not cover missed callbacks, state/effect coupling, heterogeneous work, network partitions, coordinator correctness, or crash recovery.

## Alternatives and Trade-Offs

**Independent groups versus one shared group.** Independent groups provide fan-out and isolated progress/failure but multiply reads, state, outputs, and cost. One group shares work efficiently but members must implement the same logical application and compatible state/effects.

**Manual assignment versus coordinator subscription.** Manual assignment gives deterministic ownership and avoids group rebalances, useful for fixed/sharded jobs. It requires external failover, membership, checkpoint, topology-change, and fencing logic. Coordinated groups provide dynamic recovery at transition cost.

**Dynamic versus static membership.** Dynamic IDs recover naturally but restart churn can move work. Static IDs can preserve assignments across short restarts yet require unique lifecycle control and still expire/fail over. Neither replaces sink fencing.

**Eager versus cooperative rebalancing.** Eager transfer is conceptually simple and broadly stops old work but disrupts unaffected partitions. Cooperative transfer minimizes movement and state restoration but needs compatible members and correct incremental revoke/assign handling.

**Sticky versus work-balanced assignment.** Stickiness keeps warm state and reduces movement. Work balance responds to skew but can chase noisy estimates. Combine constraints with hysteresis and measured migration cost.

**Short versus long session timeout.** Short detects crashes quickly but falsely evicts paused or network-delayed members. Long tolerates pauses but delays recovery. Improve resource isolation and bounded processing before stretching timeouts.

**Background heartbeat versus poll-coupled liveness.** Background control traffic tolerates processing work but can keep a wedged application assigned. Poll/progress coupling detects stalled consumers but requires careful work offloading and pause semantics. Monitor both liveness and useful progress.

**Local state versus remote/shared state.** Local state offers fast processing but expensive movement and rebuild. Remote state reduces transfer but adds latency, concurrency control, cost, and dependency. Changelog/snapshots balance these with restore complexity.

**Cold restore versus warm standby.** Cold restore saves steady resources but increases recovery time and load. Warm standby improves failover when fresh and correctly fenced but duplicates storage/compute and complicates assignment.

**Partition-count balance versus weighted assignment.** Count balance is stable/simple. Weighted assignment better represents skew and heterogeneous members but needs accurate measurements and can oscillate. Hard locality/residency constraints may dominate both.

**Autoscaling versus reserved headroom.** Autoscaling adapts cost but triggers rebalances/state movement and may lag bursts. Reserved capacity recovers quickly but costs more. Combine stable baselines, cooldown, and objective-aware scale decisions.

**Broker-managed offsets versus external checkpoint store.** Broker storage integrates with group tooling. External storage can atomically couple progress with application state/effects but must implement generation fencing, availability, backup, and tooling. Dual sources of truth are dangerous.

## Failure Modes and Misconceptions

**“Same topic means same group.”** Group identity determines work sharing. Different groups independently consume; same group divides one logical subscription.

**“Unique group ID per pod gives scale.”** It broadcasts work to every pod and duplicates output. Replicas of one application share the intended group.

**“Client ID is group ID.”** Client ID labels/identifies a client for telemetry; group ID owns shared progress and coordination.

**“One partition has one consumer forever.”** Ownership changes across generations. Persist state/progress and fence stale owners.

**“Stable group means healthy product.”** Coordinator stability says nothing about progress, output correctness, freshness, or sink health.

**“Heartbeat means processing.”** A background thread can heartbeat while application work is wedged. Measure accepted progress and oldest obligation.

**“Short timeouts improve reliability.”** False evictions can create churn and overlap. Tune from measured pauses and total recovery objectives.

**“Long timeouts stop rebalances.”** They mask symptoms and slow real failover. Fix work bounds/resources/network and deployment behavior.

**“Revocation always happens.”** Crashes and session loss can skip graceful callbacks. Safety requires fencing/idempotency/reconciliation.

**“Lost is the same as revoked.”** Ownership may already have moved; the old member cannot safely make final ownership-sensitive commits.

**“Callback failure rejects assignment.”** Some APIs treat callbacks as notification and propagate errors without veto/retry. Design explicit failure handling.

**“Committed offset is processing truth.”** It can be early, late, stale, or detached from state/effects. Bind the checkpoint contract.

**“Cooperative means no pause.”** Affected partitions still transfer and failures can cause loss events. It minimizes movement, not all disruption.

**“Enable cooperative on one replica.”** Mixed incompatible strategies can fail or behave unexpectedly. Follow a supported group-wide migration.

**“Static membership prevents failover.”** The member remains subject to session/protocol rules and duplicate IDs; it mainly reduces avoidable restart churn.

**“Equal partitions means equal load.”** Keys, bytes, state, computation, and sinks skew. Measure weighted demand.

**“More consumers always catch up.”** Parallelism is partition- and downstream-bounded; rebalances/restores can reduce throughput.

**“Autoscale on lag immediately.”** Noisy scale changes can cause continuous rebalances. Include sustain, capacity, restore cost, cooldown, and partitions.

**“Local state is safe with stable pods.”** pods fail and assignments move. Validate and restore state from durable evidence.

**“Resetting a group is harmless administration.”** It redefines processed input and can duplicate or omit effects. Govern it as a data change.

## Worked Examples

### Example 1

Three fraud replicas use `fraud-decisions-prod`; six order partitions are divided among them. A separate warehouse projection uses `warehouse-orders-prod` and independently reads all six. When one fraud pod accidentally deploys with a unique group ID, it receives a full independent stream and duplicates decisions. Admission policy restricts allowed group IDs per service identity.

### Example 2

Generation 20 assigns partitions 0–3 to A and 4–7 to B. C joins. A sticky cooperative assignment moves only 2 and 6 to C while unaffected partitions continue. State for the moved partitions is checkpointed/restored; all sink writes carry new fencing tokens. Count movement is two, but state bytes and restore time determine actual cost.

### Example 3

A member heartbeats on a background thread while its worker pool deadlocks. Coordinator status remains stable and lag grows. A progress watchdog detects no accepted checkpoints for ten minutes, pauses admission, captures diagnostics, and restarts under a new epoch. Heartbeat is retained as membership evidence, not health.

### Example 4

A 30-second session timeout encounters a 45-second stop-the-world pause. The coordinator reassigns partition 2 to B. A resumes without receiving graceful revocation. B writes with fencing token 18; A's token 17 is rejected. A treats the partition as lost, discards candidate state, and does not perform a final checkpoint.

### Example 5

A consumer processes 1,000 records and commits their next offset before a database transaction completes. It crashes; the new owner resumes after them, omitting effects. Group ownership worked correctly but checkpoint semantics failed. The design couples checkpoint and output transactionally or retains effect identities/receipts for idempotent replay and reconciliation.

### Example 6

Eight partitions are count-balanced across four members, two each. One partition contains 70% of state and input. Its member is saturated while others idle. Weighted assignment can move cold partitions away but cannot split the hot ordered partition; producer key/domain or serial capacity must change.

### Example 7

A rolling deployment replaces every pod at once. Eager rebalancing revokes all 200 partitions, then every new pod restores state simultaneously and overloads object storage. The team adopts bounded surge/drain, compatible cooperative transfer, restore concurrency limits, readiness after restoration, and rollout pauses based on freshness.

### Example 8

A static member ID derives from StatefulSet ordinal. A misconfigured surge creates two pods with ordinal-equivalent identity. The protocol rejects overlap; the deployment controller does not delete the old pod until it confirms shutdown. State/sink fencing remains generation-based because stable identity alone cannot prove current ownership.

### Example 9

KCL workers coordinate ten shards through leases/checkpoints. Worker A loses a lease after a network fault, and worker B acquires it. The lease counter and conditional state writes reject A when it resumes. B restores from the persisted shard checkpoint. DynamoDB lease-table throttling is monitored because coordination itself can become the bottleneck.

### Example 10

An operator needs to replay two partitions from yesterday. They stop/fence the production group, snapshot its current vector/state, create an isolated recovery group and sink generation, process the selected cut, compare outputs, then conditionally repair/publish. They do not reset the live group in place while members continue committing.

## Cross-Program Connections

Distributed systems contributes leases, epochs, fencing tokens, failure detectors, leader election, consensus, partial synchrony, split brain, and safe handoff. A group coordinator is a specialized distributed control plane.

Operating systems contributes process/thread liveness, scheduling, signals, graceful termination, stop-the-world pauses, resource limits, and readiness/liveness separation. Runtime behavior directly affects membership.

Database systems contributes compare-and-set, transactions, durable checkpoints, write-ahead/changelog recovery, locks, MVCC versions, and externalized state. Group progress is useful only when coordinated with state/effects.

Algorithms contributes assignment/matching, load balancing, bin packing, weighted scheduling, stickiness/minimum movement, graph locality, and online optimization under changing demand.

Control theory contributes feedback delay, hysteresis, cooldown, oscillation, and stability. Autoscaling membership based on lag is a delayed feedback loop with rebalance cost.

Platform engineering contributes orchestration identity, rolling updates, disruption budgets, autoscaling, probes, secret rotation, rack/zone topology, guarded admin tools, and self-service policy.

API and service engineering contributes leases, idempotency keys, conditional requests, retry/timeout semantics, authentication/authorization, pagination/cursors, and versioned administrative resources.

Security engineering contributes member authentication, group/topic authorization, checkpoint integrity, least privilege, tenant isolation, audit, stale-token rejection, and denial-of-service resistance.

Site reliability engineering contributes membership/rebalance/restore SLIs, freshness and replay margin, capacity, incident diagnosis, safe change, chaos testing, and recovery drills.

Formal methods contributes assignment invariants, epoch state machines, refinement, temporal properties, model checking, and adversarial schedules that expose overlap or lost progress.

## References

1. Apache Kafka. [Consumer Rebalance Protocol, Apache Kafka 4.3](https://kafka.apache.org/43/operations/consumer-rebalance-protocol/). Accessed 2026-09-03. Primary documentation for classic/new consumer protocols, incremental assignment, server-side assignors, timeouts, and migration.
2. Apache Kafka. [Consumer Configuration, Apache Kafka 4.3](https://kafka.apache.org/43/generated/consumer_config.html). Accessed 2026-09-03. Primary configuration reference for group identity/protocol, heartbeats, sessions, static membership, polling, assignment, and commits.
3. Apache Kafka. [KafkaConsumer API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html). Accessed 2026-09-03. Primary client documentation for subscriptions, assignments, group management, polling, positions, commits, and threading.
4. Apache Kafka. [ConsumerRebalanceListener API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/ConsumerRebalanceListener.html). Accessed 2026-09-03. Primary API documentation for assigned, revoked, and lost partition lifecycle.
5. Apache Kafka. [CooperativeStickyAssignor API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/CooperativeStickyAssignor.html). Accessed 2026-09-03. Primary API documentation for cooperative sticky assignment and migration requirements.
6. Apache Kafka. [Monitoring, Apache Kafka 4.3](https://kafka.apache.org/43/operations/monitoring/). Accessed 2026-09-03. Primary documentation for rebalance, coordinator, fetch, lag, and consumer metrics.
7. Apache Pulsar. [Messaging Concepts, Apache Pulsar 4.2](https://pulsar.apache.org/docs/4.2.x/concepts-messaging/). Accessed 2026-09-03. Primary documentation for exclusive, failover, shared, and key-shared subscription models, acknowledgements, and redelivery.
8. Amazon Web Services. [Kinesis Client Library Concepts](https://docs.aws.amazon.com/streams/latest/dev/kcl-concepts.html). Accessed 2026-09-03. Primary documentation for KCL applications, workers, shard leases, lease tables, record processors, and checkpoints.
9. Amazon Web Services. [Kinesis Client Library Configuration](https://docs.aws.amazon.com/streams/latest/dev/kcl-configuration.html). Accessed 2026-09-03. Primary configuration reference for worker IDs, failover, lease assignment, throughput, graceful handoff, and checkpoint-related behavior.
10. Google Cloud. [Pub/Sub Service Overview](https://cloud.google.com/pubsub/docs/pubsub-basics). Accessed 2026-09-03. Primary documentation for subscriptions, load-balanced subscribers, acknowledgement state, deadlines, and redelivery.
11. Google Cloud. [Pub/Sub Lease Management](https://cloud.google.com/pubsub/docs/lease-management). Accessed 2026-09-03. Primary documentation for acknowledgement-deadline extension and subscriber processing leases.

## Exercises

### Exercise 1

For each deployment, choose group IDs and explain work sharing/fan-out: four replicas of fraud scoring; two replicas of a warehouse projection; an independent audit archive; a canary that must see the same records without publishing; and a backfill over a fixed cut. Identify the failure caused by pod-specific IDs and by reusing one ID across fraud and warehouse.

### Exercise 2

Generation 31 assigns eight partitions as A:`(0,3,6)`, B:`(1,4,7)`, C:`(2,5)`. B leaves and cooperative generation 32 assigns A:`(0,1,3,6)`, C:`(2,4,5,7)`. Compute moved and retained partitions, cooperative movements, eager revocations, count imbalance, and the handoff evidence needed for each moved partition.

### Exercise 3

A group uses a 30-second session timeout. Crash detection takes the full timeout, assignment takes 8 seconds, state restore 95 seconds, and catch-up 47 seconds. Compute recovery time. The freshness objective is 150 seconds and source replay margin is 4 minutes. Assess both margins and propose changes without simply lowering the session timeout.

### Exercise 4

Twelve partitions have work weights `(9,8,7,6,5,4,3,2,2,1,1,1)` and three equal members each with safe capacity 18. Produce a feasible assignment by weight, report loads and count imbalance, and compare it with naive contiguous count balance. Explain what additional state/locality/movement evidence an assignor needs.

### Exercise 5

Design a rolling migration from an eager group protocol to cooperative/incremental assignment for a stateful 120-partition application. Include identity, supported version path, old/new configuration, mixed-member safety, deployment/drain, callbacks, lost ownership, state/checkpoints, fencing, observability, abort/rollback, capacity, retention, and verification.

## Answers to the Exercises

### Answer 1

Fraud's four replicas share one `fraud-scoring-prod` group; warehouse's two share a distinct `warehouse-projection-prod`; audit uses its own group; the nonpublishing canary uses a separate isolated group; and a fixed-cut backfill uses a distinct recovery identity/output generation so it cannot alter live progress. Pod-specific group IDs create four independent fraud subscriptions and multiply processing/effects. Reusing one group for fraud and warehouse makes them divide records, so neither application sees a complete stream. Identities should be authorized to their declared group/topic purpose and generation.

### Answer 2

Before owners are 0/3/6→A, 1/4/7→B, and 2/5→C. Afterward partitions 1 moves to A and 4/7 move to C; moved set is `(1,4,7)`, while `(0,2,3,5,6)` is retained. Cooperative movement is three; eager revocation would stop all eight. New counts are four and four, so imbalance is zero. For each moved partition record old/new group generations and owners/tokens, stop/drain outcome, last fetched/processed/state/sink/committed positions, durable checkpoint and state snapshot/changelog identity, in-flight/uncertain effects, schema/code/config, restore verification, and stale-owner fencing. Loss must not assume a final old-owner commit.

### Answer 3

Recovery is $30+8+95+47=180$ seconds. It exceeds the 150-second freshness objective by 30 seconds but remains inside the 240-second replay margin by 60 seconds under this simple estimate. Improve state snapshot freshness/restore throughput, warm standbys/locality, assignment latency, catch-up capacity, work/state size, or objective/retention; reserve resources and limit concurrent restores. Lowering session timeout alone saves at most part of 30 seconds and can cause false evictions unless measured pauses/network support it. Extend retention or archive coverage because the 60-second recovery margin is fragile under variance and live load.

### Answer 4

One feasible weighted allocation is A:`(9,6,2,1)` with load 18, B:`(8,5,3,1)` with load 17, and C:`(7,4,2,1)` with load 14. This consumes all twelve weights with counts 4/4/4 and count imbalance zero; work-load spread is four. Naive contiguous chunks of four produce loads 30, 14, and 5, so the first member exceeds safe capacity badly despite perfect count balance. Real assignment also needs per-partition identities, state bytes/locality, restore cost, rack/residency, sink demand, prior owners/stickiness, measurement confidence, failure headroom, and migration rate; weights are estimates, not timeless truth.

### Answer 5

Inventory immutable group/topic generations, current protocol/assignor, all client versions/configs, assignments, state/checkpoints, output fencing, and vendor-supported migration path. Upgrade clients to a version supporting both behaviors while retaining eager-compatible configuration, verify state/offset formats, then stage the documented assignor/protocol negotiation so no member advertises an incompatible-only mode prematurely. Roll with bounded surge and planned drains; `revoked` stops work and persists accepted state/checkpoints, while `lost` performs no unsafe final commit. Every sink/state write carries an application ownership epoch so missed callbacks cannot overlap. Monitor membership/generation, protocol, moved partitions/state bytes, rebalance failures/latency/rate, restore/catch-up, lag/freshness, replay margin, and stale-write rejection. Abort by halting rollout and returning through the supported compatible configuration—not mixing arbitrary modes—while preserved checkpoints/state remain readable. Test join/leave/crash, coordinator loss, long pause, rolling deploy, state restore, and output reconciliation over exact cuts before completing rollout; retain capacity and source history for rollback.
