---
module_id: DBE-084
program: Database Engineering
level: 2
module_number: 84
title: Replication Lag and Stale Reads
status: complete
last_verified: 2026-09-05
---

# Replication Lag and Stale Reads

## One-Page Review

### Governing question

How can a database quantify where replication is behind, determine what a replica read is allowed to observe, and route or wait for reads without mistaking one lag metric for a consistency guarantee?

### Essential definitions

**Replication lag** is a difference between two typed progress observations, not one universal scalar. **Transport lag** separates the source/sent and received frontiers; **durability lag** separates source and remote durable frontiers; **apply lag** separates durable receipt and replay/apply; **visibility lag** separates apply and the newest snapshot eligible for a read contract. **Position staleness** is an offset/transaction gap within one history. **Time staleness** is elapsed time since a relevant source commit became visible, conditional on trustworthy timestamp semantics. **Version staleness** counts missed committed versions. **Business staleness** asks whether an application fact is sufficiently current. A **session token** carries a minimum required causal/frontier observation. **Read-your-writes** ensures a session can observe its completed writes; **monotonic reads** prevent it from going backward. A **delayed replica** intentionally withholds apply for a recovery or testing purpose.

### Central model, mechanism, or theorem

For one history with source, receive, flush, replay, and visible frontiers,

$$
F_v \le F_a \le F_f \le F_r \le F_s.
$$

A read requiring token $q$ is eligible only if the selected replica can serve a safe snapshot with $F_v\ge q$ under the relevant schema, tenant, and consistency scope. If backlog $B$ is measured in one work unit, source arrival rate is $\lambda$, and sustained apply service rate is $\mu$, an idealized catch-up estimate is $B/(\mu-\lambda)$ only when $\mu>\lambda$ and rates remain stable. A small byte gap does not prove low time, version, causal, or business staleness.

### Critical invariants

- Every lag value names two compatible frontiers, one source history, a unit, observation time, and uncertainty.
- A replica advances visible progress only after replay/apply and snapshot rules make that progress readable.
- A read token is compared only with the frontier type and scope that created it.
- Read routing never substitutes connectivity, receive, or flush progress for query visibility.
- Session guarantees maintain per-session dependencies across replica changes and retries.
- Idle sources, clock changes, long transactions, parallel apply, and filters are handled explicitly in time metrics.
- Intentional delay is separated from fault-induced lag in alerts and routing.
- Catch-up estimates state rate units and require positive sustained spare capacity.
- Promotion, failover, and client retries do not reset causal/session requirements silently.

### Common failures

Failures include treating “seconds behind” as exact; reporting zero when the receiver is disconnected and its local relay queue is empty; comparing offsets across histories; converting bytes to seconds without workload rate; using source wall-clock timestamps despite skew; alerting on an idle replica because the last commit is old; routing read-after-write to a merely flushed replica; losing the session token on a load-balanced request; calling one row current while related rows are from older transactions; ignoring parallel-apply gaps; hiding an intentionally delayed replica among normal readers; and estimating catch-up when apply capacity does not exceed arrival rate.

### Compact example

Source frontier is 1,200; a replica has received 1,160, durably flushed 1,140, replayed 1,050, and can expose 1,020. The typed gaps are 40 transport, 60 durability, 90 apply-after-flush, and 180 visible-to-source positions. A session token requiring 1,000 may read there; a token requiring 1,100 may not. With backlog 180 transactions, sustained arrival 30/s, and apply 50/s, the idealized catch-up time is $180/(50-30)=9$ seconds. At apply 25/s it never catches up under steady input.

### Connections

Retrieve [Log Sequence Numbers](073-log-sequence-numbers.md), [Physical Replication](081-physical-replication.md), [Logical Replication](082-logical-replication.md), and [Synchronous and Asynchronous Replication](083-synchronous-and-asynchronous-replication.md). Continue through [the program roadmap](../ROADMAP.md) to leader election/failover, sharding, distributed transactions, consensus-backed replication, and consistency/latency/availability evaluation.

## Governing Question

“The replica is five seconds behind” sounds precise but leaves crucial questions unanswered. Behind which source observation? Is the network receiver late, is durable log queued, is replay stalled, or is the query using an old snapshot? Does five seconds mean wall-clock age, measured acknowledgement delay, transaction timestamp, or an estimate? Does the relevant order even have a total position across shards or sources?

A useful lag model decomposes the pipeline and connects it to a read contract. The read contract may permit eventual convergence, require a maximum version/time bound, require causal/session guarantees, or require the latest authoritative state. Monitoring tells the router whether evidence satisfies that contract; it does not manufacture the guarantee.

## Why This Matters

Read replicas reduce primary load and place data near users, but stale results can violate user expectations and business invariants. A customer who updates an address and immediately sees the old value may retry. An authorization revocation served stale can be a security incident. An analytical dashboard may tolerate minutes, while a settlement decision may require an authoritative transactional read.

Lag also drives recoverability and capacity. Receive lag can indicate network or sender problems. Durable lag changes asynchronous loss exposure. Apply lag can make failover slow or unsafe. Visibility lag governs read eligibility. Retention grows when a consumer cannot advance its required frontier. Collapsing them into one number prevents correct diagnosis.

Current PostgreSQL 18 documentation states that `pg_stat_replication` write/flush/replay lag values measure recent acknowledgement delay and are not predictions of catch-up time; on an idle caught-up system they can retain a recent value briefly and then become `NULL`. Current MySQL 8.4 documentation explains that `Seconds_Behind_Source` can show zero when the applier has consumed the relay log even if a slow receiver is behind the source, and that clock changes reduce reliability. Current product behavior is therefore evidence for decomposed metrics, not justification for a universal “seconds behind” gauge.

## Prerequisites and Retrieval

Retrieve these ideas:

- positions such as LSNs, GTIDs, and offsets are typed by history, channel, source, and representation;
- receive, write, flush, replay/apply, transaction commit, and query visibility are distinct stages;
- synchronous acknowledgement can wait for a remote stage but does not make every replica current;
- MVCC snapshots can intentionally remain older than the latest replayed commit;
- a logical consumer can be blocked by schema or constraint conflicts after receiving events;
- parallel apply can complete later independent transactions while an earlier transaction remains a low-water-mark gap;
- throughput is meaningful only with a work unit; bytes, records, transactions, and apply cost are not interchangeable;
- latency and queue length are distributions that change under load and failure;
- client retries and load balancing can move a session between replicas;
- election, promotion, and fencing determine write authority but do not automatically preserve session context.

This module assumes the replication mechanisms of DBE-081 through DBE-083 and develops measurement and read policy. It does not replace general causal-consistency theory or the later failover protocol.

## Learning Objectives

After completing this module, you should be able to:

1. decompose transport, durable, apply, and visibility lag using typed frontiers;
2. distinguish position, byte, transaction, version, time, causal, and business staleness;
3. explain the limitations of timestamp- and last-event-based lag metrics;
4. derive conditional backlog growth and catch-up estimates with correct units;
5. implement read-your-writes and monotonic reads using scoped session tokens;
6. route, wait, fall back, or reject reads according to explicit consistency policy;
7. diagnose lag across sender, network, storage, apply, conflicts, snapshots, and workload;
8. validate lag monitors and stale-read behavior with deterministic histories and failure cuts.

## Core Exposition

**Name each frontier.** For one source history define $F_s$ as the source comparison frontier, $F_r$ as complete received history, $F_f$ as remote durable history, $F_a$ as applied/replayed history, and $F_v$ as the newest safe query-visible frontier for a stated isolation/snapshot contract. Products may add sent, write, decoded, staged, indexed, or acknowledged frontiers.

The differences answer different questions:

- $F_s-F_r$: transport backlog, if the position admits subtraction;
- $F_s-F_f$: remote durability exposure relative to that replica;
- $F_f-F_a$: durable apply backlog;
- $F_a-F_v$: visibility/snapshot delay;
- $F_s-F_v$: end-to-end read frontier gap.

Subtraction is legal only inside the same ordered history and unit. A byte LSN gap can include transactions of wildly different costs; a GTID set may require set difference rather than scalar subtraction; multiple shards have a vector of frontiers.

**Choose a staleness dimension.** Position staleness is precise for replay continuity but not human time. Byte staleness measures retained work volume but not transaction count. Version staleness counts committed versions missed by a key/read. Time staleness measures elapsed time between relevant commit and observation. Causal staleness asks whether dependencies are visible. Business staleness applies a domain predicate: “authorization revocation no older than 2 seconds” or “inventory at least as new as reservation token q.”

No dimension dominates. One 2 GiB bulk load can create a large byte gap but one transaction. Ten thousand tiny security changes can create a small byte gap with serious business impact. An idle source has an old last-commit timestamp while a replica is perfectly current. Publish separate metrics and connect each SLO to its consequence.

**Interpret clocks cautiously.** A source commit timestamp and replica wall clock can estimate time staleness when clocks have bounded error, timestamps preserve original source meaning, and the selected event actually describes the latest source frontier. Clock steps, time zones, upstream cascades, transaction duration, and idle periods complicate it.

Attach uncertainty: if source and replica clocks each have bounded error $\epsilon_s$ and $\epsilon_r$, a measured difference has at least their combined uncertainty. Prefer monotonic local durations for pipeline stages and position correlations for exact coverage. Never replace “unknown” with zero merely to make dashboards green.

**Model the queue.** Let source work arrive at sustained rate $\lambda$ units/s and the replica apply at $\mu$ units/s. Backlog evolves approximately as

$$
B(t+\Delta)=\max(0,B(t)+(\lambda-\mu)\Delta).
$$

If $\mu>\lambda$ and both remain stable, idealized drain time is $B/(\mu-\lambda)$. If $\mu\le\lambda$, there is no finite steady-input catch-up time. State the unit: transactions/s can hide variable transaction cost; bytes/s can hide DDL, index, and conflict work. Use measured service curves and confidence intervals for production predictions.

Long transactions can create misleading shapes. A decoder may retain large history until commit. A parallel applier may finish many later transactions while a conflict holds the low-water mark. A single global backlog should be accompanied by oldest blocked transaction, worker queues, dependency gaps, retry/conflict counts, and resource saturation.

**Separate observed lag from desired delay.** A delayed replica intentionally postpones apply to protect against operator mistakes or test stale-read behavior. Its transport/durable frontiers can remain current while apply/visible frontiers trail by policy. Label configured delay and actual excess delay separately. Never place it in ordinary read or failover pools without an explicit role.

Current MySQL 8.4 delayed replication uses per-transaction commit timestamps and reports desired/remaining delay through Performance Schema/replica status. That is a product mechanism. A delayed copy is not a replacement for backup because it remains online, filtered by its replication scope, and vulnerable to shared faults or accidental reconfiguration.

**Define the read contract.** Common contracts include:

- **eventual:** a read may observe any valid replica state, with convergence expected once writes stop and faults recover;
- **bounded staleness:** a read requires a declared maximum version/time/frontier gap;
- **read-your-writes:** a session read observes its completed writes;
- **monotonic reads:** once a session observes frontier q, later reads do not return a state before q;
- **writes-follow-reads:** a session write is ordered after the state on which it depended;
- **causal:** dependencies such as read-then-write are not observed out of order;
- **strong/latest:** the read is coordinated with current authoritative order under a specified consistency model.

These can be scoped per key, partition, database, transaction, or global history. A global token from one shard cannot be compared to another shard's scalar position. Use a vector or a coordination service when dependencies span authorities.

**Carry session tokens.** After a write, return a token containing history/epoch, scope, and minimum visibility frontier. After each read, raise the session's observed token. On a later read, select a replica whose safe visible frontier covers the token, wait within a budget, route to the source/strong path, or return an explicit unavailable/staleness response. Never silently route to an older replica.

Tokens must be authenticated or server-bound if clients can alter them. They need versioning, size bounds, and topology-change translation. A promoted history may extend the old one; validate ancestry. If a write was lost during failover, pretending the new history covers its token violates read-your-writes—surface the recovery outcome.

**Protect multi-row meaning.** A replica snapshot can be transactionally consistent yet stale. That is often preferable to mixing rows from incompatible points. Read an order and its lines under one snapshot. Logical filters can omit related tables, making the target incapable of the invariant regardless of lag. Business readiness may require a watermark across several tables or streams, not only the database replay LSN.

Parallel apply needs a **consistent cut**. A high maximum-applied position does not mean all prior dependencies are applied. Use the contiguous commit frontier or a vector/dependency representation. For analytical sinks, publish a batch/generation watermark only after all partitions for that cut are complete.

**Route with eligibility, not one threshold.** A replica is eligible when it has the right history/schema/tenant data, is healthy, can serve the isolation level, has a visible frontier covering the request token/bound, and meets security/residency policy. Lag is one predicate. Load, query capability, maintenance state, and intentional delay also matter.

Hedged reads can reduce latency but must send the same token and accept only an eligible response. Caches need equivalent version metadata; otherwise a fresh database response can be overwritten by a stale cache fill. Negative results and authorization checks deserve explicit freshness policy.

**Diagnose the pipeline.** Start by comparing all frontiers at one observation time. If $F_s-F_r$ grows, inspect sender capacity, network, receiver, authentication, and source retention. If receive is current but flush trails, inspect replica storage, fsync, writeback, and disk-full conditions. If flush is current but apply trails, inspect replay CPU/I/O, locks, conflicts, long queries, DDL, schema errors, retries, and worker skew. If apply is current but visible trails, inspect snapshots, safe-time computation, indexes/materialization, and read-router data.

Correlate with input rate, transaction sizes, resource saturation, checkpoints, compaction/vacuum, maintenance, deployment, and topology events. A falling lag can still predict failure if retained log reaches disk limits first. Measure retained bytes and time to capacity alongside catch-up time.

**Understand product gauges.** PostgreSQL's `pg_stat_replication` exposes sent/write/flush/replay LSNs and recent write/flush/replay acknowledgement delays. Its documentation explicitly says lag intervals reflect recent synchronous-commit delay and are not catch-up estimates. Query functions on a standby expose last received/replayed WAL and last replayed transaction time, each with narrower meaning.

MySQL's `Seconds_Behind_Source` is based on event timestamps and applier/receiver state. Documentation warns that a slow network can let the applier be caught up with a receiver that is itself late, producing zero relative to the relay stream, and that clock changes reduce reliability. Performance Schema transaction/worker timestamps and GTIDs provide more diagnostic detail. Treat `NULL`, zero, and no-new-events as distinct states.

**Validate reads and monitors together.** Generate transactions with unique IDs, commit positions/timestamps, dependencies, key changes, multi-row invariants, long/large transactions, and controlled idle periods. Pause sender, network, receiver, storage flush, replay, one parallel worker, visibility publication, and read-router refresh independently. Step clocks in a test environment. Create cascades and intentional delay.

Assert every metric against ground truth. Ask reads with and without tokens at exact boundaries. Move sessions between replicas, fail over histories, restart components, exhaust retention, and restore. Verify that stale responses are either within the declared bound or rejected/fallback-routed; do not infer correctness from a smoothly moving dashboard.

The executable finite model below calculates typed gaps, conditional drain time, and token eligibility. Positions are abstract transaction units in one history. It does not simulate clocks, concurrency, MVCC snapshots, network/storage, failure, or production workload distributions.

<!-- bijux-verify: {"id":"replica-lag-and-read-token","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source=1200\nreceive=1160\nflush=1140\napply=1050\nvisible=1020\ntransport_gap=40\ndurability_gap=60\napply_after_flush_gap=90\nvisible_gap=180\ncatchup_seconds=9.0\ntoken_1000_eligible=true\ntoken_1100_eligible=false\nslow_apply_catches_up=false\nevidence=finite_replica_lag_model\n","stderr":""}} -->
```python
frontier = {"source": 1200, "receive": 1160, "flush": 1140,
            "apply": 1050, "visible": 1020}
arrival_rate = 30
apply_rate = 50
backlog = frontier["source"] - frontier["visible"]

def eligible(required):
    return frontier["visible"] >= required

catchup = backlog / (apply_rate - arrival_rate) if apply_rate > arrival_rate else None
print(f"source={frontier['source']}")
print(f"receive={frontier['receive']}")
print(f"flush={frontier['flush']}")
print(f"apply={frontier['apply']}")
print(f"visible={frontier['visible']}")
print(f"transport_gap={frontier['source'] - frontier['receive']}")
print(f"durability_gap={frontier['source'] - frontier['flush']}")
print(f"apply_after_flush_gap={frontier['flush'] - frontier['apply']}")
print(f"visible_gap={backlog}")
print(f"catchup_seconds={catchup:.1f}")
print(f"token_1000_eligible={str(eligible(1000)).lower()}")
print(f"token_1100_eligible={str(eligible(1100)).lower()}")
print(f"slow_apply_catches_up={str(25 > arrival_rate).lower()}")
print("evidence=finite_replica_lag_model")
```

## Definitions and Notation

- $H$: one replication history/epoch in which positions are comparable.
- $F_s$: selected source frontier at an observation time.
- $F_r$: complete receive frontier for the replica.
- $F_f$: remote durable flush/staging frontier.
- $F_a$: contiguous applied or replayed commit frontier.
- $F_v$: newest frontier safe for the declared query visibility contract.
- $q$: session/read token specifying a minimum required visible frontier and scope.
- $B$: backlog in a declared work unit.
- $\lambda$: sustained source arrival rate in that unit per second.
- $\mu$: sustained replica service/apply rate in the same unit per second.
- **Consistent cut:** selected progress across transactions/partitions with no missing required predecessor.
- **Low-water mark:** greatest position below which all required work is complete.
- **Intentional delay:** configured minimum postponement of apply or visibility.
- **Business staleness:** domain-specific insufficiency of observed state, possibly stricter than technical lag.
- **Read eligibility:** conjunction of frontier, history, scope, schema, isolation, health, and policy predicates.

## Mechanisms, Invariants, or Proof Structure

**Frontier ordering.** In one correctly reported pipeline, safe visibility cannot cover work not applied, applied work cannot exceed durable available history when replay depends on it, durable history cannot exceed complete receipt, and receipt cannot exceed the selected source endpoint. Hence $F_v\le F_a\le F_f\le F_r\le F_s$. Engines with different staging must define an equivalent causal graph rather than reuse the symbols blindly.

**Token safety.** If token q names a committed dependency in history H and a replica serves a snapshot with compatible history and $F_v\ge q$, then that snapshot includes q under the declared contiguous-visibility semantics. If history differs, scope is partial, or $F_v$ is a maximum with gaps, the scalar comparison is insufficient.

**Queue derivation.** Over interval $\Delta$, arrivals add $\lambda\Delta$ units and service removes at most $\mu\Delta$, bounded below by zero. Stable positive spare capacity $\mu-\lambda$ drains backlog B in ideal time $B/(\mu-\lambda)$. Variable cost, bursts, dependencies, failures, and saturation violate the constant-rate assumptions, so production estimates need empirical bounds.

**Idle-time counterexample.** If no source transaction commits for one hour and the replica is fully caught up, `now - last_visible_commit_time` is one hour although frontier staleness is zero. Therefore age of the last event is not, by itself, replication lag.

**Session monotonicity.** Maintain token $q_{next}=\max(q_{prior},q_{observed},q_{written})$ within one ordered scope. Routing only to replicas covering $q_{next}$ prevents read regression and supplies read-your-writes. Cross-shard/source scopes need a vector or dependency graph because scalar maximum may be undefined.

## Alternatives and Trade-Offs

| Measure or policy | What it answers | Advantage | Limitation |
| --- | --- | --- | --- |
| Position/LSN gap | ordered history distance | exact continuity signal | unit may not predict time/cost |
| Byte gap | retained volume | capacity relevance | transactions have variable work |
| Transaction/version gap | missed commits/versions | closer to logical meaning | expensive or ambiguous across keys |
| Commit-time age | wall-clock freshness estimate | intuitive SLO unit | skew, idle, cascade, timestamp semantics |
| Recent acknowledgement lag | foreground wait cost | useful for sync policy | not total backlog/catch-up time |
| Queue drain model | conditional recovery time | exposes spare-capacity requirement | assumes stable comparable rates |
| Eventual replica read | low latency/high availability | simple scaling | no per-read bound |
| Bounded-staleness routing | explicit freshness | aligns with some business SLOs | needs trustworthy frontier/time evidence |
| Session token | read-your-writes/monotonicity | precise client dependency | token propagation and topology complexity |
| Source fallback | strongest current authority | simple correctness path | source load and regional latency |
| Wait at replica | preserves placement | can meet token soon | consumes latency/budget; may never succeed |
| Intentional delayed replica | recovery/testing window | protects against rapid mistakes | unsuitable for normal current reads/failover |

## Failure Modes and Misconceptions

- **“Lag is a number.”** It is a relation between typed frontiers and a unit at an observation time.
- **“Zero seconds means current.”** The receiver may be disconnected or behind while the applier has consumed its local queue.
- **“NULL means zero.”** It can mean unknown, idle/no recent sample, stopped component, or unsupported tracking.
- **“Last commit age is lag.”** An idle caught-up source is a counterexample.
- **“A byte gap converts directly to time.”** Apply cost and input rate vary.
- **“Positive apply throughput guarantees catch-up.”** Catch-up requires sustained service greater than arrivals.
- **“Maximum applied position is a safe watermark.”** Parallel gaps require a contiguous low-water mark.
- **“Remote flush makes reads fresh.”** Apply and visibility can trail.
- **“Synchronous replica means this replica acknowledged.”** Another eligible member may have satisfied the commit.
- **“Read-your-writes follows the user automatically.”** Load balancing loses it without a token or sticky authoritative path.
- **“One token works across every shard.”** Independent histories need vectors/dependencies or coordination.
- **“Transactionally consistent means current.”** A replica can expose a self-consistent old snapshot.
- **“Delayed replica is broken.”** Delay can be intentional, but it must have a distinct role.
- **“Row counts detect stale state.”** Equal counts can hide missing deletes, wrong values, gaps, and broken dependencies.

## Worked Examples

### Example 1

**Situation.** Source/receive/flush/apply/visible frontiers are 1,200/1,160/1,140/1,050/1,020.

**Reasoning.** Transport gap is 40, source-to-durable gap 60, durable apply backlog 90, and end-to-end visible gap 180 positions. Calling the replica “180 behind” hides the pipeline cause; each difference answers a distinct operational question.

**Conclusion.** Report typed frontier gaps together rather than one unlabeled lag value.

### Example 2

**Situation.** A caught-up replica's last replayed transaction committed one hour ago because the source has been idle.

**Reasoning.** `now - last_commit_time` is one hour, but source and visible frontiers are equal. There is no missed source work. Pair commit-age gauges with a current source heartbeat/frontier or explicit idle state.

**Conclusion.** Age since last event is not replication staleness during source idleness.

### Example 3

**Situation.** Backlog is 600 MiB, source produces 40 MiB/s, and replica replays 55 MiB/s at current load.

**Reasoning.** Spare capacity is 15 MiB/s, so the constant-rate ideal is $600/15=40$ seconds. If source rate rises to 60 MiB/s, spare capacity becomes negative and no finite steady-input catch-up exists. Transaction cost changes can invalidate byte-rate estimates.

**Conclusion.** Catch-up time is conditional on sustained positive spare capacity in a common unit.

### Example 4

**Situation.** A write returns token `(history=7, tenant=A, visible>=900)`. Replica r1 is healthy at 940 for tenant A; r2 is at 880; r3 is at 950 but lacks tenant A.

**Reasoning.** r1 is eligible. r2 violates the frontier requirement. r3 violates scope even with a higher scalar frontier. The router may wait for r2 or use the source, but cannot silently choose r2/r3.

**Conclusion.** Read eligibility is a conjunction of history, scope, visibility, and policy—not “largest number wins.”

### Example 5

**Situation.** A session reads version 120 on r1, then load balancing sends it to r2 at version 110.

**Reasoning.** Without a session token, the second read regresses. Raise the session's required frontier to at least 120 after the first observation; r2 must catch up, another eligible replica must serve, or the request must use an explicit fallback.

**Conclusion.** Monotonic reads require preserving the client's observed dependency across routing changes.

### Example 6

**Situation.** A parallel applier has completed transactions 101–109 except transaction 103, which is blocked by a conflict.

**Reasoning.** Maximum completed position 109 is not a safe contiguous watermark. A read depending on 103 may be wrong even if unrelated effects from 109 are present. The low-water mark remains 102 until 103 and required predecessors complete; advanced systems may expose per-key/dependency vectors instead.

**Conclusion.** Parallel completion needs gap-aware progress, not a maximum offset.

### Example 7

**Situation.** The receiver's network is slow. The applier consumes every event already in the relay log and a “seconds behind” gauge reports zero.

**Reasoning.** Applier-to-receiver lag is zero, while receiver-to-source transport lag can be large. Compare source/sent and received transaction frontiers plus connection state. MySQL 8.4 documents this limitation for `Seconds_Behind_Source` on slow networks.

**Conclusion.** A downstream-relative time gauge can be zero while end-to-end replication is behind.

### Example 8

**Situation.** An order header and three lines commit together, but a logical replica publishes only headers and two line partitions have different watermarks.

**Reasoning.** Header freshness does not establish complete order visibility. Define a consistent batch/transaction cut across all required partitions or keep the read on a transactional source. If the publication excludes one line table entirely, no amount of catch-up satisfies the business projection.

**Conclusion.** Business freshness can require multi-object completeness beyond one database frontier.

### Example 9

**Situation.** A replica is configured to delay apply by 3,600 seconds. It has received and durably stored the newest log but exposes state from an hour ago.

**Reasoning.** Transport/durability health can be current while apply/visibility lag is intentional. Exclude it from current-read and normal failover pools, report configured delay separately from excess delay, and protect its configuration/retention role.

**Conclusion.** Intentional delay is a policy state, not evidence of a broken receiver.

### Example 10

**Situation.** After failover to a history that ends at 990, a client presents a read-your-writes token for acknowledged transaction 1,000 from the old history.

**Reasoning.** The new primary cannot honestly claim coverage. Validate ancestry and recovery records; if transactions 991–1,000 were lost, return an explicit uncertain/lost-write outcome and reconcile by transaction ID. Mapping token 1,000 to “current” on the new history fabricates causality.

**Conclusion.** Session guarantees must survive topology change honestly or surface the broken dependency.

## Cross-Program Connections

- Distributed Systems owns eventual, causal, session, quorum, and strong consistency models; this module maps database replication frontiers and reads to those contracts.
- API and Service Engineering owns propagation of consistency/session tokens and explicit stale/unavailable responses across request boundaries.
- Data Engineering owns pipeline watermarks and cross-partition completeness for downstream data products; database replica watermarks are a related but narrower mechanism.
- Platform Engineering owns service discovery and traffic routing; a replica endpoint is eligible only after database-specific history, scope, visibility, and health predicates pass.
- Software Delivery and Reliability Engineering owns SLOs, alerting, capacity forecasting, fault injection, and incident modes; lag dashboards must preserve unknown and intentional states.
- Security Engineering owns freshness requirements for revocation, authorization, secrets, and policy; some stale reads are safety violations rather than usability defects.

## References

1. PostgreSQL Global Development Group. [PostgreSQL 18: Cumulative Statistics System](https://www.postgresql.org/docs/18/monitoring-stats.html), especially `pg_stat_replication` LSN and lag semantics. Current documentation checked 2026-09-05.
2. PostgreSQL Global Development Group. [PostgreSQL 18: System Administration Functions](https://www.postgresql.org/docs/18/functions-admin.html), including WAL receive/replay positions and last replayed transaction timestamp. Current documentation checked 2026-09-05.
3. PostgreSQL Global Development Group. [PostgreSQL 18: Hot Standby](https://www.postgresql.org/docs/18/hot-standby.html). Current read visibility, snapshot, and recovery-conflict behavior checked 2026-09-05.
4. Oracle. [MySQL 8.4 Reference Manual: `SHOW REPLICA STATUS`](https://dev.mysql.com/doc/refman/8.4/en/show-replica-status.html). Current `Seconds_Behind_Source`, receiver, clock, and null-state limitations checked 2026-09-05.
5. Oracle. [MySQL 8.4 Reference Manual: Delayed Replication](https://dev.mysql.com/doc/refman/8.4/en/replication-delayed.html). Current transaction timestamp and Performance Schema delay behavior checked 2026-09-05.
6. Douglas B. Terry, Alan J. Demers, Karin Petersen, Mike Spreitzer, Marvin Theimer, and Brent Welch. “Session Guarantees for Weakly Consistent Replicated Data.” IEEE ICDCS, 1994. Read-your-writes, monotonic-read/write, and writes-follow-reads foundations.
7. Peter Bailis, Shivaram Venkataraman, Michael J. Franklin, Joseph M. Hellerstein, and Ion Stoica. [Probabilistically Bounded Staleness for Practical Partial Quorums](https://www.vldb.org/pvldb/vol5/p776_peterbailis_vldb2012.pdf). PVLDB 5(8), 2012. Version/time staleness analysis.
8. Werner Vogels. [Eventually Consistent](https://dl.acm.org/doi/10.1145/1466443.1466448). *Communications of the ACM* 52(1), 2009. Eventual consistency and client-observed consistency perspective.
9. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Transaction, recovery, replication, and measurement foundations.
10. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly, 2017. Replication lag, read-after-write, monotonic-read, and prefix-consistency explanations.

## Exercises

### Exercise 1

Distinguish transport, durability, apply, and visibility lag. Give one operational consequence and one suitable frontier pair for each.

### Exercise 2

A replica has 900 transactions of visible backlog. New transactions arrive at 70/s. It can apply 100/s normally, but every fifth minute maintenance lowers it to 50/s for one minute. Compute the ideal normal catch-up time, then explain why that value is insufficient for a production promise.

### Exercise 3

A dashboard reports `lag_seconds=0` whenever the applier queue is empty and `NULL` as zero. The receiver can disconnect independently. Diagnose the false states and redesign the telemetry.

### Exercise 4

Compare sticky-primary reads, session-token routing, and waiting for synchronous remote apply for an application requiring read-your-writes across two regions. State strengths, costs, and failure behavior.

### Exercise 5

Design stale-read policy for an authorization system in which grants may be 30 seconds stale but revocations must be visible within 2 seconds. Replicas span histories and regions, clocks have bounded uncertainty, and failover can lose asynchronous writes. Include write tokens, routing, time/position evidence, caching, failure responses, monitoring, and tests.

## Answers to the Exercises

### Answer 1

**Transport lag** is source/sent minus complete receive; it predicts retained-log pressure and indicates sender/network/receiver trouble. **Durability lag** is source durable or comparison frontier minus remote flush/staging; it bounds that replica's durable-copy gap under the stated failure model. **Apply lag** is remote durable minus contiguous replay/apply; it predicts failover catch-up and points to CPU/I/O/lock/conflict/worker problems. **Visibility lag** is applied minus safe query-visible frontier, or source minus visible for end-to-end reads; it governs replica read eligibility. Each pair must share history and compatible units. A good answer does not call socket receipt durable or replay automatically visible.

### Answer 2

During normal operation spare capacity is $100-70=30$ transactions/s, so the constant-rate ideal is $900/30=30$ seconds. That estimate ignores the maintenance cycle because it predicts catch-up before the next minute only if maintenance is not already active and rates remain stable. During maintenance, $\mu=50<70$, so backlog grows by 20/s or 1,200 transactions in that minute. Over a five-minute cycle, four normal minutes drain $4\times60\times30=7,200$, while one maintenance minute adds 1,200, for net 6,000 transactions per cycle when backlog exists. Production prediction needs the current phase, bursts, variable transaction cost, conflicts, saturation, and confidence bounds; it must use the same work unit and cap at zero. Report the 30-second value only as a conditional ideal.

### Answer 3

An empty applier queue proves only that apply caught up with what the receiver supplied. If the receiver is disconnected or slow, end-to-end source lag can be positive while the dashboard says zero. Mapping `NULL` to zero also turns unknown, stopped, unsupported, or idle/no-recent-sample states into a false success.

Expose source/sent, receive, durable, contiguous apply, and visible frontiers with source history, sample time, connection/worker states, and units. Derive each gap only when endpoints are comparable. Represent `unknown`, `idle-and-frontiers-equal`, `stopped`, `disconnected`, and `unsupported` separately. Add a source heartbeat/frontier observation, oldest pending transaction, worker gaps, retained bytes/time to capacity, and measured input/apply rates. Alert on state and consequence, not merely a numeric threshold.

### Answer 4

Sticky-primary reads are simplest and use the current authority, but increase primary/regional latency and load; failover still needs transaction identity and history handling. Session-token routing returns a history/scope/minimum-visible token after writes, allows any covering replica to serve, and falls back/waits explicitly. It scales better but requires trustworthy per-replica visible frontiers, token propagation, and topology translation. Waiting for synchronous remote apply can make a selected replica ready earlier and reduce per-read waits, but adds network/apply tails and standby conflicts to every protected write; it still needs routing to the acknowledging/covering replica and correct snapshot semantics.

A practical design uses session tokens with a bounded wait and source/strong fallback, optionally remote apply for a narrow latency-critical class. On partition, either preserve read-your-writes by using a covering authority or return unavailable; silently using an older regional replica violates the contract.

### Answer 5

Every grant/revocation write receives an immutable transaction ID and token containing authority history, policy partition/tenant, commit position, commit-time evidence, and operation class. Revocations use a durable acknowledgement policy consistent with the 2-second objective; grants may use the ordinary path. A read authorizing access must carry the maximum dependency token and route only to a replica/cache whose compatible visible frontier covers it. For unrelated revocations, require both a position heartbeat proving coverage and a conservative time bound adjusted for maximum clock uncertainty; a bare old last-event timestamp is insufficient during idle periods.

Caches store policy version/token with positive and negative decisions. A revocation invalidation is not trusted until cache instances acknowledge or their entries expire inside the 2-second bound; when evidence is missing, fail closed or query the strong authority. Grants older than 30 seconds may similarly route strong or return an explicit unavailable/pending result rather than invent freshness.

On failover, validate token ancestry. If the new history does not include an acknowledged revocation, mark the outcome as a safety incident and fail closed until reconciled by transaction ID; never map the lost token to current. Monitor source/receive/flush/apply/visible frontiers, heartbeat age and uncertainty, per-class SLO violations, cache versions, routing rejections/fallbacks, history changes, and lost-write reconciliation. Tests pause every pipeline stage, skew clocks within/outside bounds, idle the source, move sessions, partition regions, replay stale cache fills, introduce parallel gaps, and fail over before/after revocations. The oracle verifies that no authorization succeeds after the declared 2-second revocation bound under the covered failure model, while grant behavior matches the documented 30-second policy.
