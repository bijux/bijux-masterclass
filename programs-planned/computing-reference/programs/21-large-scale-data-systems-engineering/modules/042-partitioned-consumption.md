---
module_id: LSDS-042
program: Large-Scale Data Systems Engineering
level: 1
module_number: 42
title: Partitioned Consumption
status: complete
last_verified: 2026-09-03
---

# Partitioned Consumption

## One-Page Review

### Governing question

How can a consumer fleet divide partitioned input, transfer ownership safely, advance progress, and scale under failures and skew without skipping records, double-applying effects, violating order, or allowing obsolete owners to continue?

### Essential definitions

- A **consumer group** is a named coordination and progress domain in which source partitions or splits are assigned among active members.
- An **assignment** maps each eligible partition to at most one active owner for an ownership generation; delivery systems with message-level sharing use a different contract.
- A **generation**, **member epoch**, or **lease epoch** qualifies ownership so work from revoked or expired owners can be fenced.
- A **rebalance** changes membership or partition assignment after join, leave, failure detection, subscription change, or partition discovery.
- The **fetch position** $F_p$ is the next position the client will request; the **safe processed frontier** $P_p$ is the lowest not-yet-durably-incorporated position; the **checkpoint/committed position** $C_p$ is the durable recovery position.
- The **log end** $H_p$ is the exclusive current upper boundary under a named visibility rule; positional lag is commonly $H_p-C_p$ or $H_p-P_p$.
- A **contiguous completed prefix** contains every required record before its frontier; completing later records does not authorize advancing across an earlier hole.
- **eager rebalance** may revoke broad ownership before reassignment; **incremental/cooperative rebalance** transfers only changed partitions over multiple coordinated updates.
- **static membership** gives a process instance stable identity to reduce avoidable assignment churn, but still requires liveness and fencing.
- **pause/resume** stops fetching or delivery for selected partitions without necessarily relinquishing ownership; it is flow control, not a durable checkpoint.

### Central model, mechanism, or theorem

For partition $p$ in ownership generation $g$, maintain qualified state $(g,C_p,P_p,F_p,H_p)$. In a simple ordered source with buffered fetch, the safety relation is

$$L_p\le C_p\le P_p\le F_p\le H_p,$$

where every position below $P_p$ has been durably incorporated according to the processing contract. An asynchronous worker may finish offsets 100, 101, 103, and 104, but the safe next frontier remains 102 until offset 102 finishes or is resolved by an explicit policy. Committing 105 would skip 102 after recovery.

Assignment safety requires no two effect-capable members to act as current owner of the same partition in the same logical group generation. Coordinators, leases, heartbeats, revocation handshakes, and sink fencing reduce overlap, but timeouts alone cannot prove the old process stopped. Effects therefore carry generation/lease/transaction identity or are idempotent.

Capacity is partition-constrained. If partition $p$ arrives at rate $\lambda_p$ and its owner serves $\mu_p$, backlog grows at approximately $\max(0,\lambda_p-\mu_p)$. Adding group members beyond the number of assignable partitions creates idle members; it does not increase one hot partition's service rate unless the source or operator can be repartitioned safely.

### Critical invariants

- Group, subscription, cluster/topic, partition/split, member, and generation identities are explicit and authenticated.
- Each partition has at most one current effect-capable owner per assignment contract; stale owners are fenced at state and sink boundaries.
- Revocation stops new fetch, resolves in-flight work, records a safe contiguous frontier, and releases resources before or through a proven handoff.
- Assignment initializes from checkpointed state or an explicit start/reset policy; no local cached cursor silently overrides it.
- Checkpoints never advance beyond the contiguous durably processed prefix and remain coordinated with operator state/effects.
- Per-partition source order is preserved wherever promised; parallel processing has a reorder/commit discipline and bounded buffers.
- Heartbeat/session/poll/lease timeouts exceed legitimate pauses with margin but still detect failures within the recovery objective.
- Partition discovery, split/merge ancestry, assignment strategy, and compatibility version are deterministic or recorded.
- Records, bytes, CPU, state, event-time progress, lag, in-flight work, and failure risk—not partition count alone—drive balance.
- Memory, fetch bytes, queued records, workers, connections, checkpoint metadata, retries, and rebalance churn are bounded.

### Common failures

Common failures include equating consumer count with throughput; running more consumers than partitions and expecting speedup; assigning a hot partition as one unit forever; committing fetched rather than processed positions; committing the maximum completed offset despite holes; enabling auto-commit around slow effects; continuing after revocation; trusting process death after a timeout without fencing; doing blocking work so heartbeats/polls expire; treating pause as checkpoint; seeking without clearing buffered records; mixing manual assignment with group coordination assumptions; using partition-count balancing under unequal workloads; rebalancing on every brief restart; introducing static identities that collide; discovering child shards before parents are complete when order requires ancestry; failing to checkpoint on clean handoff; and placing raw group/member/topic data in unbounded metrics.

### Compact example

Six partitions have work rates `(90,70,50,30,20,10)` units/s. Round-robin assignment to three equal consumers yields loads 120, 90, and 60; a deterministic greedy load-aware assignment can yield 90 each. This is planning evidence, not a universal optimal algorithm. If partition 0 alone arrives at 130 units/s and one consumer can serve 100, the backlog grows 30 units/s even with ten idle consumers because ownership is indivisible. Inside that owner, offsets 100, 101, 103, and 104 can complete concurrently, but the safe next checkpoint stays 102.

### Connections

[LSDS-041](041-logs-as-distributed-input.md) defines partition positions, visibility, and replay bounds. [LSDS-043](../ROADMAP.md) adds operator state, [LSDS-044](../ROADMAP.md) and [LSDS-045](../ROADMAP.md) add event-time progress, and [LSDS-047](../ROADMAP.md) through [LSDS-050](../ROADMAP.md) connect assignment with barriers, snapshots, backpressure, and effect-safe replay.

## Governing Question

A partitioned source exposes parallelism, but somebody must decide which worker owns which partition, from which position, for how long, and what happens when membership changes. That decision is both a scheduling problem and a correctness protocol. A coordinator can assign quickly; it cannot instantaneously stop a paused or partitioned old owner.

Consumers also have several notions of progress. A client can fetch records into memory, dispatch them to asynchronous workers, update state, write an external system, and periodically commit a source position. These events occur at different times. Collapsing them into one “offset” creates losses or duplicates after crash.

Rebalances are normal: deployments, autoscaling, failures, subscription changes, and new partitions cause them. An eager protocol may stop the whole group; an incremental protocol limits movement but creates a multi-step transition. Static membership can preserve placement across short restarts but does not eliminate fencing, expiry, or software bugs.

The governing question is how to combine assignment, liveness, ownership epochs, contiguous progress, checkpoint/effect protocols, flow control, and load-aware capacity so partitioned consumption remains correct and operable during constant change.

## Why This Matters

Consumer groups let many workers process one logical input without every worker reading everything. They provide horizontal scale up to the source partitioning, automatic failover, and independent progress for separate applications. Correctly operated, a worker loss moves only its partitions and replay starts from durable state.

The failure modes are subtle. If a consumer commits after fetch but before effect, a crash loses work. If it commits after effect, a crash can repeat work. If two generations write the same sink, both can be individually well-behaved yet collectively corrupt results. If one slow callback misses its poll deadline, the coordinator may reassign while it still runs.

Balance by partition count can be misleading. One partition may carry most bytes or expensive keys. More instances may sit idle while a hot partition accumulates lag. Reassigning stateful partitions can itself cost minutes of restore and cold-cache time, so minimizing maximum load competes with minimizing movement.

Operational choices affect latency and cost. Large fetches improve throughput but expand recovery and memory. Frequent commits reduce replay but load coordination storage. Short timeouts detect failures quickly but cause false suspicions during GC, checkpoints, or deployment. Long timeouts delay recovery.

Ownership metadata, lag, and payloads cross security boundaries. Group IDs can collide across environments; credentials can outlive leases; reassignment can move regulated state across zones. Assignment and checkpoint design must enforce tenant, region, authorization, retention, and audit constraints.

## Prerequisites and Retrieval

Review partitioning, locality, task graphs, failures, and scale accounting in [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve metadata identity, leases, and consistency from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review task attempts/speculation in [LSDS-027](027-task-retry-and-speculation.md), skew in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), and log partitions/offsets/retention in [LSDS-041](041-logs-as-distributed-input.md). You should understand half-open ranges, failure detectors, leases/epochs, idempotency, transactions, backpressure, hashing, bipartite assignment, queueing rates, checkpoints, and source visibility.

## Learning Objectives

After this module, you should be able to:

1. distinguish subscription, group, member, partition, assignment, generation, lease, and checkpoint identity;
2. model committed, safe-processed, fetched, and end positions without skipping incomplete holes;
3. compare direct/manual assignment, coordinated eager assignment, incremental/cooperative transfer, static membership, and message-level sharing;
4. design revocation and assignment callbacks that stop, drain, snapshot, commit, restore, and fence safely;
5. tune heartbeat, session, poll, lease, acknowledgement, and checkpoint timing from failure and work distributions;
6. preserve per-partition order under batching and asynchronous processing with bounded reorder state;
7. select assignment using load, locality, state-movement, failure-domain, and regulatory constraints;
8. diagnose lag from arrival/service rates, skew, downstream blocking, rebalances, restore, and retention headroom;
9. handle partition discovery, split/merge ancestry, deletion, and bounded versus continuous membership; and
10. validate recovery and protect group metadata, source data, checkpoints, credentials, diagnostics, and derived effects.

## Core Exposition

### Define the coordination domain

A group identifier determines which consumers share assignment and usually which durable positions they observe. Qualify it by environment, tenant, application, source, and semantic version. Reusing a production group ID in a test can steal partitions or overwrite progress.

Membership identity may be ephemeral per process session or stable across restarts. An instance ID can reduce churn and preserve locality, but duplicates must be rejected. Deployment systems need unique, durable instance naming and explicit retirement.

Pin the subscription: topics/streams, pattern semantics, visibility, partition discovery, authorization, and reset policy. A group is not a data contract unless its source set and decoding/processing semantics are versioned.

### Separate assignment from delivery

Partition assignment gives one member responsibility for a whole ordered shard/split. It enables ordered sequential positions and compact checkpoints. Message-level shared delivery may send different records of one source shard to multiple consumers and track individual acknowledgements; ordering and cumulative progress differ.

Manual/direct assignment avoids group rebalances and gives the application deterministic placement, but it must discover partitions, elect owners, detect failure, checkpoint, and prevent overlap itself. Coordinated subscription delegates these tasks to a broker/coordinator protocol.

Choose the abstraction that matches state and ordering. Do not assume a shared subscription has Kafka-style partition exclusivity, or that a partition group can parallelize one hot partition without application-level subsharding.

### Qualify ownership with generations

An assignment record should include group generation/member epoch or lease version. When ownership changes from A to B, effects from A's old epoch must fail or deduplicate even if A is paused by a network partition and believes it still owns the work.

Heartbeats prove recent contact, not immediate death of an old process. Session expiry authorizes reassignment but does not cancel threads or remote requests. Sink transactions, conditional writes, per-partition fencing tokens, or idempotency keys close this gap.

Lease clocks require careful assumptions. Prefer coordinator-issued monotone versions and server-side expiry over comparing unsynchronized client wall clocks. Persist enough identity to audit which generation produced an effect.

### Track four progress frontiers

For each partition, $F_p$ advances as fetch requests/buffers receive data. Processing may finish in or out of order. $P_p$ is the next position whose required record is not durably incorporated—the completed prefix frontier. $C_p$ is the recovery position committed to checkpoint/group storage. $H_p$ is the current source end under one visibility.

Normally $C_p\le P_p\le F_p\le H_p$. A synchronous consumer often has $P_p$ near $F_p$; prefetch can make the gap large. Checkpoint barriers may temporarily leave $C_p<P_p$. Lag metrics must name which frontier they use.

On recovery, start from coordinated state $C_p$, not a stale local $F_p$. Recreate decoder/operator state before emitting. If retention moved log start beyond $C_p$, invoke the explicit gap procedure from LSDS-041.

### Commit only a contiguous completed prefix

Concurrent work improves throughput, but completion order no longer equals source order. Maintain a bounded set/bitmap of completed positions and advance $P_p$ only while the current frontier is complete. Do not commit `max(completed)+1`.

If effects must preserve partition order, serialize them or buffer results until the prefix closes. One slow record creates head-of-line blocking; timeout/dead-letter policy changes semantics and must be explicit. A poison record cannot be skipped merely to improve lag.

Bound in-flight records/bytes and reorder distance. On revocation, stop new dispatch, wait within a deadline for a prefix, cancel/fence remainder, checkpoint only the prefix, and allow unfinished suffix to replay.

### Coordinate positions with state and effects

Auto-commit commonly records positions on a timer relative to poll/fetch, not proof that arbitrary downstream work is durable. Use it only when its exact semantics match tolerated loss/duplication. Otherwise checkpoint explicitly.

At-least-once processing checkpoints after effects/state; crash can repeat effects, so sinks need idempotency/deduplication. At-most-once checkpoints before effects; crash can lose them. Exactly-once state requires atomic or coordinated source positions plus operator state, and end-to-end effects require a compatible sink protocol.

External group commits may be useful for monitoring while framework checkpoints remain authoritative. Record that distinction. A failed broker offset commit need not invalidate a framework snapshot if restore uses the snapshot's positions.

### Execute revocation safely

Revocation begins a handoff. Mark partitions revoking and stop new fetch/dispatch. Resolve in-flight work to a safe prefix, flush or snapshot partition state, commit through the chosen protocol, close partition resources, and publish no further old-generation effects.

Callbacks often run in a poll/event thread with deadlines. Slow remote flushes can extend group instability. Design bounded asynchronous handoff or rely on framework checkpoints rather than doing arbitrary blocking work inside callbacks.

If graceful revocation fails, the successor starts from the last durable checkpoint and duplicates the uncheckpointed suffix. Correctness comes from replay/effect semantics and fencing, not assuming graceful callbacks always execute.

### Initialize newly assigned partitions

On assignment, validate the generation, source incarnation, partition, and retained bounds. Load the matching partition state/checkpoint, establish sink fencing, seek to the next unread position, then permit fetch/effects.

Do not fetch with default reset while state restoration is pending. Do not reuse cache from a prior partition epoch without validation. If no checkpoint exists, apply a recorded earliest/latest/timestamp/snapshot policy; absence is not permission to guess.

Warm state transfer, standby replicas, and sticky assignment reduce recovery time, but their freshness/integrity must be checked. A stale standby resumes from its own checkpoint and replays the difference.

### Compare eager and incremental transfer

An eager rebalance broadly revokes ownership, establishes a new assignment, and restarts. Its global barrier is easy to reason about but causes stop-the-world pauses and cache loss.

Incremental/cooperative protocols communicate additions and revocations over successive updates so unaffected partitions continue. They reduce movement and pause time but require clients/assignors to respect intermediate states; a partition is not assigned to its new owner until the old ownership is relinquished under protocol rules.

Mixed client versions and incompatible assignors can defeat assumptions. Roll out protocol changes with compatibility matrices, metrics, canaries, and rollback. Name the actual protocol rather than saying “rebalance” generically.

### Tune liveness without confusing it with work

Heartbeat/session or lease timing determines failure detection. Poll/process interval limits may separately detect an application that remains network-alive but is not making progress. Long GC pauses, blocking callbacks, overloaded coordinators, checkpoints, and network loss can cause false expiry.

Set timeouts above observed legitimate p99/p99.9 pauses plus margin and below the recovery objective where possible. Reduce record batch/in-flight work or isolate heartbeat threads rather than simply making every timeout huge. Static membership may delay reassignment after a poll violation until session expiry.

Measure heartbeat latency/failures, poll gaps, lease renewals, coordinator load, false rebalances, and recovery time. Liveness tuning is empirical and version-specific.

### Choose assignment objectives explicitly

Count-balanced assignment gives each consumer similar partition counts. Range assignment may preserve topic/range locality but imbalance when topics have different partition counts. Round-robin spreads counts. Sticky strategies reduce movement. Load-aware strategies use estimated records, bytes, CPU, state, or lag.

Assignment is multi-objective: minimize maximum load, state transfer, cross-zone traffic, cold cache, unavailable partitions, and policy violations while respecting capacity and affinity/anti-affinity. Estimates become stale, and moving a hot stateful partition can temporarily worsen lag.

Version assignor algorithm and inputs. Deterministic tie-breaking prevents oscillation. Apply hysteresis/minimum residence/cost thresholds so small estimate changes do not rebalance continuously.

### Respect the partition parallelism ceiling

With $P$ assignable partitions and $M$ members, at most $\min(P,M)$ members own work under exclusive partition assignment. Extra members are standby/idle. Scaling consumers helps only when overloaded partitions can be distributed or when per-owner downstream concurrency is safe.

For each partition compare $\lambda_p$ with sustainable $\mu_p$. If $\lambda_p>\mu_p$, backlog grows even if fleet aggregate capacity exceeds aggregate arrival. Diagnose record width, CPU/state cost, downstream latency, throttling, and hot keys.

Remedies include increasing per-owner resources, optimizing processing, batching, asynchronously overlapping safe I/O, changing upstream key/shard distribution, or repartitioning downstream after reading. Splitting source partitions is a source migration with ordering/checkpoint implications.

### Handle pause, resume, and backpressure

Pause selected partitions when downstream capacity, reorder buffers, rate limits, or state restore require it. Continue group liveness according to client contract. Pause does not release assignment or checkpoint buffered data.

On resume, validate generation and positions. A seek must discard or reconcile prefetched records; otherwise old buffered data can appear after the cursor moves. Bound total and per-partition queues so hot partitions do not starve cold ones.

Credits, maximum fetch bytes/records, per-partition limits, and fair scheduling propagate backpressure. LSDS-049 develops end-to-end control; here the ownership layer must not hide unbounded buffers behind stable heartbeats.

### Discover partitions and preserve ancestry

Continuous sources may add partitions. An enumerator/coordinator discovers them and assigns new splits exactly once under its checkpointed metadata. A finite run generally freezes membership and stopping positions.

Some systems split or merge shards with parent/child lineage. To preserve hash-range order, children may need to wait until parents reach their end. Lease tables must cover all open shards and recover missing entries without assigning descendants prematurely.

Partition deletion/recreation with the same display name needs an incarnation ID. Pattern subscriptions can unintentionally include sensitive/new topics; authorize and audit discovery, and pin regex/version semantics.

### Observe lag as a vector

Record per partition $C_p,P_p,F_p,H_p$, source start, records/bytes/time lag estimates, arrival/service rates, oldest event time, watermark, in-flight count/bytes, processing latency, retries, and retention headroom. Report maximum and tail, not only sum.

Correlate lag with assignment/member/generation, heartbeat/poll gaps, rebalance reason/duration, restore bytes/time, downstream waits, pauses, throttling, GC, and failures. A growing $F-P$ means fetched work is not completing; growing $H-F$ means fetch/source service is behind; $P-C$ can be checkpoint delay.

Offset span may not equal records after compaction/filtering. Estimate time-to-catch-up from net service $\mu-\lambda$ only while positive and stable. Show uncertainty rather than a false exact ETA.

### Secure coordination and lifecycle

Authorize subscription, fetch, group join, offset commit, and administrative reset separately. Bind members to workload identity and environment. Encrypt transport/checkpoints, protect coordinator/lease tables, rotate credentials without accidental duplicate membership, and audit resets/reassignments.

Partition state may have residency constraints; assign only to eligible workers/zones. Group/member IDs, topic names, lag, keys, and state sizes can expose business activity. Bound metric cardinality and restrict raw diagnostics.

Retire static member IDs, group offsets, lease rows, checkpoints, local caches, credentials, and dead-letter data when retention/replay/hold obligations end. Deleting group state can change the next start policy, so require intent and evidence.

### Validate churn and adversarial schedules

Test joins/leaves, rolling restarts, crashes, network partitions, coordinator failover, GC pauses, poll stalls, lease expiry, overlapping old/new owners, callback failure, state-restore failure, offset-commit failure, and sink fencing.

Generate skewed rates/costs, poison records, out-of-order completions, holes, bounded reorder overflow, hot partitions, more members than partitions, partition discovery, split/merge ancestry, deletion/recreation, retention gaps, and schema errors.

Differentially compare effects with a single-owner reference using record IDs and per-partition order. Assert every required record is reflected according to the delivery contract, no stale generation commits, checkpoints stay at completed prefixes, resources remain bounded, and recovery converges.

## Definitions and Notation

- $A_g(p)$: member assigned partition $p$ in ownership generation $g$, or unassigned.
- $L_p,H_p$: source start and exclusive log-end positions for partition $p$ under one visibility.
- $C_p$: durable checkpoint/committed next position.
- $P_p$: safe processed next position; every required earlier record is durably incorporated.
- $F_p$: next fetch position after client buffering.
- $\lambda_p,\mu_p$: arrival and sustainable service rates for partition $p$ in the same work unit/time.
- **contiguous completed prefix**: all required records before $P_p$, regardless of later out-of-order completion.
- **generation/fencing token**: coordinator-issued identity that rejects obsolete owners at state/effect boundaries.
- **rebalance churn**: assignment changes, moved state/partitions, and unavailable time over a declared interval.
- **retention headroom**: time/position/bytes before the oldest required checkpoint becomes unavailable.

## Mechanisms, Invariants, or Proof Structure

1. Pin group/subscription/source identities, assignment protocol/version, member identity, and start/reset policy.
2. Discover an authorized partition set and establish assignment $A_g$ with at most one current effect-capable owner per partition.
3. Fence prior generations before the new owner writes state/effects; treat timeout as suspicion, not physical termination.
4. Restore partition state and $C_p$, then fetch while tracking $C_p\le P_p\le F_p\le H_p$.
5. Advance $P_p$ only across the contiguous durably completed prefix; coordinate $C_p$ with state/effects.
6. On revocation, stop new work, resolve a bounded prefix, checkpoint safely, fence/cancel suffix, and release resources.
7. Balance by measured load/state/locality/policy with deterministic tie-breaking and movement hysteresis.
8. Bound fetch, concurrency, reorder, pause, retry, checkpoint, connections, and coordination metadata.
9. Observe frontier gaps, rates, tails, churn, restore, retention, and security events per partition/generation.
10. Fault-test adversarial schedules and retire membership/checkpoint/state artifacts only under explicit lifecycle policy.

The ownership proof requires both coordinator agreement and effect fencing. Coordinator generation $g+1$ authorizes B, but delayed A may still execute. If every state/effect write includes a token accepted only for the current generation (or is idempotently keyed), A cannot corrupt the new history.

The progress proof is prefix-based. Let $D$ be completed positions. Starting at $P$, advance while $P\in D$. Any commit $C\le P$ replays at worst a suffix already completed; a commit above $P$ can skip the first missing position. This reasoning must incorporate filtered/control positions according to connector visibility.

## Alternatives and Trade-Offs

**Manual assignment** gives placement control without group churn but makes the application own discovery/failover/checkpoints. **Coordinated groups** automate recovery but add protocol and rebalance dependencies.

**Eager rebalance** is a clear global transition with broad pause. **Incremental/cooperative rebalance** limits movement but adds intermediate ownership states and compatibility constraints.

**Ephemeral membership** replaces failed sessions quickly. **Static membership** preserves assignment across short restarts but requires unique identities and can delay reassignment.

**Count-balanced assignment** is simple. **Load-aware assignment** handles skew but needs trustworthy estimates and hysteresis. **Sticky/locality-aware assignment** reduces restore/network cost but may tolerate imbalance.

**Serial partition processing** preserves order simply. **Async processing** improves utilization but needs bounded reorder state, prefix commits, and ordered effects where required.

**Frequent checkpoints** reduce replay and handoff work but consume coordinator/state-store resources. **Infrequent checkpoints** improve steady throughput while increasing recovery duplicates and retention exposure.

**Short liveness timeouts** reduce failure recovery delay but cause false rebalances. **Long timeouts** tolerate pauses while extending unavailability. **Pause** retains ownership; **revoke** transfers it.

## Failure Modes and Misconceptions

1. **“Ten consumers make one partition ten times faster.”** Exclusive assignment leaves nine idle.
2. **“Equal partition counts mean equal work.”** Rates, bytes, CPU, state, and downstream latency differ.
3. **“A timeout stops the old consumer.”** It only lets coordination move on; fence effects.
4. **“Heartbeats prove processing progress.”** A live client can be stuck or buffering indefinitely.
5. **“Fetched means processed.”** $F_p$ can be far ahead of $P_p$.
6. **“Commit the largest completed offset.”** Earlier holes would be skipped.
7. **“Auto-commit gives exactly-once.”** It does not coordinate arbitrary state or effects.
8. **“Pause is durable.”** It neither checkpoints nor relinquishes ownership.
9. **“Seek changes all buffered work.”** Prefetched records must be cleared/reconciled.
10. **“Revocation callback always finishes.”** Crash and deadlines require replay-safe fallback.
11. **“Static membership eliminates rebalances.”** Failure, collision, subscription, and topology changes remain.
12. **“Incremental means no overlap risk.”** Old owners still need protocol compliance and fencing.
13. **“Offset commit is the framework checkpoint.”** Some frameworks use checkpoint state as authority and broker commits only for visibility.
14. **“Lag sum explains latency.”** The maximum hot partition and frontier gaps often dominate.
15. **“More prefetch always improves throughput.”** It increases memory, recovery, and reorder exposure.
16. **“New child shards can start immediately.”** Parent lineage/order may constrain them.
17. **“Pattern discovery is harmless.”** It changes input and can cross authorization boundaries.
18. **“Deleting a group only removes metadata.”** It also removes recovery position and changes restart behavior.

## Worked Examples

### Example 1

Four partitions and six consumers under exclusive assignment use at most four consumers. The other two can be standby but add no current source throughput.

### Example 2

Three consumers receive six partition rates `(90,70,50,30,20,10)`. Round-robin by partition ID yields 120, 90, and 60 units/s. A load-aware arrangement can yield 90 each, at possible movement/state cost.

### Example 3

One partition receives 130 MB/s while its owner processes 100 MB/s. Backlog grows about 30 MB/s, or 108 GB/hour in decimal units, even if other consumers are idle.

### Example 4

The client has $C=400$, $P=430$, $F=500$, and $H=900$. Recovery replays from 400 unless a newer coordinated checkpoint exists. Committing 500 would risk skipping 70 positions not safely processed.

### Example 5

Offsets 100, 101, 103, and 104 finish. `max+1` is 105, but safe next is 102. When 102 completes, the frontier can jump through 105.

### Example 6

Consumer A's lease epoch 8 expires and B receives epoch 9. A later submits a database write tagged 8. A conditional sink accepting only current epoch 9 rejects the zombie effect.

### Example 7

A rebalance revokes a partition with 1,000 prefetched records. The consumer stops dispatch, completes a prefix through next offset 4,250, checkpoints 4,250, and cancels the suffix. The successor replays from 4,250.

### Example 8

A five-minute maximum poll gap protects against a stuck application. A handler occasionally blocks for eight minutes; heartbeats may remain healthy in some client designs, yet the processing-progress deadline triggers reassignment. Reduce/bound work or redesign concurrency before merely enlarging the threshold.

### Example 9

A shard splits into children C1 and C2. If the source contract requires parent-before-child order for each hash range, the assignor records ancestry and waits for parent P's ending checkpoint before activating its children.

### Example 10

This fixture computes a deterministic load-aware assignment and the safe completed-prefix frontier for out-of-order work.

<!-- bijux-verify: {"id":"partition-assignment-frontier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignments={'m0': [0], 'm1': [1, 4], 'm2': [2, 3, 5]} loads={'m0': 90, 'm1': 90, 'm2': 90}\ncompleted_max=104 safe_next=102 unsafe_next=105\n","stderr":""}} -->
```python
partition_load = {0: 90, 1: 70, 2: 50, 3: 30, 4: 20, 5: 10}
members = ("m0", "m1", "m2")
assignments = {member: [] for member in members}
loads = {member: 0 for member in members}

for partition, load in sorted(partition_load.items(), key=lambda item: (-item[1], item[0])):
    member = min(members, key=lambda name: (loads[name], name))
    assignments[member].append(partition)
    loads[member] += load

completed = {100, 101, 103, 104}
safe_next = 100
while safe_next in completed:
    safe_next += 1
unsafe_next = max(completed) + 1

print(f"assignments={assignments} loads={loads}")
print(
    f"completed_max={max(completed)} safe_next={safe_next} "
    f"unsafe_next={unsafe_next}"
)
```

The fixture validates one greedy heuristic and prefix arithmetic. It does not prove optimal assignment, simulate a coordinator, establish distributed fencing, or benchmark consumer throughput.

## Cross-Program Connections

- **Distributed Systems:** failure detection, leases, epochs, fencing, membership, consensus, and partial synchrony define safe ownership transfer.
- **Data Engineering:** connector checkpoints, CDC partitions, schema handling, dead letters, and backfills depend on source assignment and replay semantics.
- **Algorithms:** scheduling on unrelated loads, consistent/rendezvous hashing, matching, bin packing, reorder buffers, and prefix tracking inform assignors.
- **Database Systems:** transactional offsets, conditional writes, snapshot restore, and idempotency connect consumption to durable effects.
- **Reliability Engineering:** lag/headroom SLOs, rebalance churn, restore time, hot partitions, and chaos tests make group behavior operable.
- **Platform Engineering:** deployment identity, autoscaling, zones, quotas, workload credentials, and observability shape fleet membership.
- **Security Engineering:** least-privilege group operations, authenticated generations, tenant/residency constraints, audit, and lifecycle protect data/control planes.
- **Systems Engineering:** throughput, recovery time, state movement, availability, cost, and correctness are coupled objectives with feedback and hysteresis.

## References

1. Apache Kafka. [Consumer Rebalance Protocol.](https://kafka.apache.org/43/operations/consumer-rebalance-protocol/) Current primary documentation for classic versus next-generation consumer protocols, incremental assignment, server/client settings, and metrics.
2. Apache Kafka. [Consumer Configurations.](https://kafka.apache.org/43/configuration/consumer-configs/) Current configuration contract for group protocol, instance ID, session/poll timing, assignment, fetch limits, reset, auto-commit, and isolation.
3. Apache Kafka. [Group Configurations.](https://kafka.apache.org/43/configuration/group-configs/) Current server-side group assignment, heartbeat, and session configuration.
4. Apache Kafka. [Distribution: Consumer Offset Tracking.](https://kafka.apache.org/43/implementation/distribution/) Primary design documentation for per-partition positions, group coordinators, and offset commit/fetch.
5. Apache Kafka. [Consumer API.](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/Consumer.html) Current API contract for subscription, assignment, position, committed offsets, seek, pause/resume, and lifecycle.
6. Apache Kafka. [ConsumerRebalanceListener API.](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/ConsumerRebalanceListener.html) Current callback contract for partition revocation, assignment, and loss.
7. Apache Kafka. [Basic Kafka Operations.](https://kafka.apache.org/43/operations/basic-kafka-operations/) Current operational documentation for group state, members, assignment strategy, position, lag, and explicit reset.
8. Apache Flink. [Apache Kafka Connector.](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/) Current source documentation for partition splits, start/stop positions, discovery, checkpointed offsets, monitoring, idleness, and security.
9. Apache Flink. [Dynamic Kafka Source.](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/dynamic-kafka/) Current source/split identity and enumerator documentation across clusters.
10. Apache Pulsar. [Messaging Concepts.](https://pulsar.apache.org/docs/4.1.x/concepts-messaging/) Primary documentation for exclusive, failover, shared, and key-shared subscriptions, acknowledgements, redelivery, and ordering.
11. Amazon Web Services. [Kinesis Client Library Consumer and Lease Synchronization.](https://docs.aws.amazon.com/streams/latest/dev/shared-throughput-kcl-consumers.html) Primary documentation for shard leases, workers, lease-table capacity, discovery, and reshard ancestry.
12. Google Cloud. [Pub/Sub Exactly-Once Delivery.](https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery) Primary documentation for acknowledgement deadlines/IDs, redelivery, regional scope, ordering interaction, and quotas.
13. Google Cloud. [Pub/Sub Message Ordering.](https://docs.cloud.google.com/pubsub/docs/ordering) Primary documentation for ordering-key scope, publisher region, subscriber behavior, throughput, and latency trade-offs.

## Exercises

### Exercise 1

Eight partitions have rates `(80,70,60,50,40,30,20,10)` MB/s and four consumers each sustain 100 MB/s. Give a balanced assignment, determine whether all consumers remain within capacity, and explain why partition-count round-robin may differ.

### Exercise 2

A partition has $C=1{,}000$, $P=1{,}080$, $F=1{,}250$, and $H=2{,}000$. Compute the checkpoint-to-end, processed-to-end, fetched-to-end, fetched-but-not-safely-processed, and processed-but-not-checkpointed spans. State recovery implications.

### Exercise 3

Offsets 200, 201, 203, 204, and 206 complete asynchronously; 202 and 205 are still running. Starting at 200, compute safe next frontier. Then update it after 202 completes and after 205 completes. Explain why max-completed is unsafe.

### Exercise 4

A consumer in epoch 12 is isolated. The coordinator assigns its partition to another member in epoch 13. The old process later finishes a payment side effect. Design a fencing/idempotency key and the checks needed at the sink.

### Exercise 5

Design a rebalance test matrix for a stateful partition consumer. Cover eager/incremental transfer, graceful/crash paths, in-flight work, checkpoint failure, sink fencing, hot partitions, static identities, new partitions, and retention. State the authoritative assertions.

## Answers to the Exercises

### Answer 1

One balanced arrangement is `(80+10)`, `(70+20)`, `(60+30)`, and `(50+40)`, producing 90 MB/s per consumer, so all are below 100 MB/s with 10 MB/s nominal headroom. Round-robin by partition ID could yield `(80+40)=120`, `(70+30)=100`, `(60+20)=80`, `(50+10)=60`; equal counts do not equal load. Real assignment also includes variability, state, CPU, downstream latency, and movement cost.

### Answer 2

$H-C=1{,}000$, $H-P=920$, $H-F=750$, $F-P=170$, and $P-C=80$ positions. A crash restores from 1,000 unless a coordinated newer checkpoint exists, replaying up to 80 safely processed positions. The 170 fetched positions are not all safe; committing F could skip them. Current source-fetch lag begins at 1,250, while processing lag begins at 1,080.

### Answer 3

Initially safe next is 202 because 200 and 201 form the prefix. After 202 completes, it advances through completed 203 and 204 to 205. After 205 completes, it advances through 206 to 207. `max(completed)+1` would initially be 207 and would skip unfinished 202/205 on recovery.

### Answer 4

Use a stable business operation ID such as `(payment_id,event_version)` for idempotency and a fencing tuple `(group,source_partition,assignment_epoch)`. The sink atomically verifies epoch 13 is current for that ownership scope and inserts/updates the business operation only if its idempotency key has not been applied. Epoch 12 fails even if its work is logically valid. Authenticate the caller, prevent epoch rollback, retain dedupe state for the replay horizon, and coordinate result/checkpoint semantics.

### Answer 5

Cross protocol (eager/incremental), termination (leave/crash/network isolation), work state (empty/fetched/out-of-order/poison), checkpoint (success/timeout/failure), sink (idempotent/transactional/fence rejection), distribution (uniform/hot), membership (ephemeral/static collision), topology (add/delete/split), and retention (ample/gap). Assert at most one current effect-capable epoch, every required record appears according to delivery contract, partition order where promised, no commit beyond completed prefix, replay begins at authoritative checkpoint, stale effects fail/deduplicate, state restores correctly, child/topology rules hold, gaps fail visibly, resource bounds hold, and assignments converge.
