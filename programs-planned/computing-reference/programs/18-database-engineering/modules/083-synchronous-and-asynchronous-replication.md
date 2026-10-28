---
module_id: DBE-083
program: Database Engineering
level: 2
module_number: 83
title: Synchronous and Asynchronous Replication
status: complete
last_verified: 2026-09-05
---

# Synchronous and Asynchronous Replication

## One-Page Review

### Governing question

Which replication event must occur before a database reports commit success, and how does that choice change latency, loss exposure, read visibility, availability, and behavior under uncertain failure?

### Essential definitions

**Asynchronous replication** allows a source to acknowledge commit without waiting for a remote replica event. **Synchronous replication** places at least one declared remote condition on the commit-success path. **Semisynchronous replication** is a product term whose exact acknowledgement point and timeout/fallback policy must be read literally. An **acknowledgement point** may be remote receipt, operating-system write, durable flush, replay, or query visibility. An **acknowledgement set** declares which replicas may satisfy a policy; a **threshold** $k$ requires enough qualifying acknowledgements. **Commit latency** is client-observed response time, not replica lag. **Loss exposure** is committed work that can disappear under a stated failure and failover model. **Commit ambiguity** occurs when the client cannot tell whether a timed-out operation committed. **Degraded mode** is an explicit policy used when the acknowledgement condition cannot be met.

### Central model, mechanism, or theorem

For local durable time $T_L$ and qualifying remote acknowledgement times $T_1,\ldots,T_n$, a threshold-$k$ policy returns no earlier than

$$
T_{success}=\max(T_L,T_{(k)}),
$$

where $T_{(k)}$ is the $k$th-smallest qualifying remote time. The formula states a latency lower bound, not a safety theorem. Safety additionally depends on what each acknowledgement proves, replica independence, membership, history, promotion eligibility, and fencing. An asynchronous acknowledgement reduces response dependence on replicas but permits a nonempty loss window. A remote receive acknowledgement is weaker than durable flush; flush is weaker than replay/visibility.

### Critical invariants

- A successful commit records exactly which local and remote events the configured policy required.
- An acknowledgement never represents a stronger stage than the replica actually completed.
- Replica identities, failure domains, histories, and eligibility are verified before their acknowledgements count.
- The threshold is evaluated over distinct eligible replicas; duplicate connections cannot impersonate independent copies.
- A timeout or disconnect cannot retroactively prove abort; ambiguous client outcomes use transaction identity and status lookup.
- Switching from synchronous to asynchronous behavior is an observable durability-policy change, not a routine retry.
- Promotion considers the acknowledged durability frontier, not merely the nearest reachable replica.
- Read routing uses replay/visibility evidence rather than inferring freshness from the write acknowledgement mode.

### Common failures

Failures include calling socket receipt durable; treating “sync” as one universal guarantee; waiting for a remote write while promising query visibility; counting two replicas in one failure domain as two independent copies; hiding automatic timeout fallback; acknowledging locally before the durable record required by the advertised contract; confusing quorum acknowledgement with leader election; promoting a replica below an acknowledged frontier; retrying an ambiguous transaction without idempotency; letting one slow priority replica block despite healthy alternatives; and using average latency when tail order statistics determine commits.

### Compact example

A source durably logs at 4 ms. Three eligible remote replicas durably flush at 8, 23, and 60 ms. An asynchronous/local-durable policy can answer at 4 ms. An `ANY 1` remote-flush policy answers at 8 ms; `ANY 2` at 23 ms; `ANY 3` at 60 ms. If the policy requires remote apply and apply times are 18, 40, and 95 ms, `ANY 2` answers no earlier than 40 ms. These times do not prove safe failover unless the selected replicas share the correct history and the old writer can be fenced.

### Connections

Retrieve [Failure Models](071-failure-models.md), [Group Commit](077-group-commit.md), [Physical Replication](081-physical-replication.md), and [Logical Replication](082-logical-replication.md). Continue through [the program roadmap](../ROADMAP.md) to lag and stale reads, leader election/failover, consensus-backed replication, and consistency/latency/availability evaluation.

## Governing Question

Calling replication synchronous or asynchronous is shorthand for a precise placement of a remote event relative to the client-visible commit response. The label alone says neither what was acknowledged nor what happens when the acknowledgement cannot arrive. A replica may have received bytes into memory, written them through an operating-system cache, durably flushed them, replayed them, or exposed them to queries. Those states survive different failures and enable different reads.

The governing design question is therefore: for this transaction class and failure model, which evidence must exist before success, which replicas can provide it, how many are required, and what policy applies when they cannot? That answer must connect storage semantics to client retry behavior, topology, promotion, and operations.

## Why This Matters

Asynchronous replication keeps the foreground write path independent of remote latency and outages. It suits distant disaster-recovery copies, analytical replicas, and workloads that accept a bounded or measured recovery-point objective. It also creates a window in which locally acknowledged commits may not exist on any promotable replica.

Synchronous replication can place acknowledged transactions in additional failure domains before success, reducing defined loss exposure. It adds the chosen network, queueing, storage, and perhaps replay tail to client latency, and can make writes unavailable when too few eligible replicas respond. “Zero data loss” remains conditional: simultaneous failures, shared storage faults, corrupted records, configuration errors, wrong-history promotion, and failed fencing can invalidate it.

Current PostgreSQL 18 supports priority (`FIRST`) and quorum (`ANY`) selection of synchronous standbys and distinguishes local, remote-write, remote-flush, and remote-apply commit settings. Current MySQL 8.4 replication is asynchronous by default and offers semisynchronous plugins that wait for a configurable number of replica receipt/log acknowledgements, with a timeout that can revert operation to asynchronous behavior. These product terms and defaults are version-sensitive and were checked on 2026-09-05.

## Prerequisites and Retrieval

Retrieve these concepts:

- source commit, WAL/binlog publication, network send/receive, remote write, durable flush, replay, and visibility are distinct events;
- group commit amortizes flush cost but does not itself add a remote durable copy;
- an LSN, GTID, or offset is comparable only within its typed history and protocol;
- physical and logical replication expose different compatibility, apply, and conflict conditions;
- failure domains include process, host, disk, rack, zone, region, control plane, credentials, and operator/configuration faults;
- a recovery-point objective is a policy target under a declared failure model, not a guarantee inferred from average lag;
- election chooses authority, eligibility checks state, and fencing excludes stale writers;
- timeouts create uncertainty and do not reveal whether a remote or source event occurred just before the deadline;
- idempotency and transaction-status lookup resolve client retries more safely than assuming timeout means abort;
- latency percentiles and correlated failures matter more than independent averages for production tails.

[Physical Replication](081-physical-replication.md) defined receive/write/flush/replay/visible frontiers. [Logical Replication](082-logical-replication.md) added transaction envelopes, identity, apply, and checkpoint frontiers. This module decides which of those events participates in commit success.

## Learning Objectives

After completing this module, you should be able to:

1. define synchronous, asynchronous, and semisynchronous behavior by exact acknowledgement points;
2. distinguish source durability, remote receipt, write, flush, replay, and visibility guarantees;
3. derive latency for priority and threshold acknowledgement policies;
4. connect acknowledgement sets and replica placement to explicit failure domains;
5. reason about commit ambiguity, timeout, fallback, cancellation, and retry;
6. design degraded modes without silently weakening durability promises;
7. separate commit acknowledgement from replica-read freshness, election, promotion, and fencing;
8. validate replication policies with deterministic failure cuts and independent durability/read oracles.

## Core Exposition

**Write the commit contract first.** A useful contract has the form: “success means the source has durably recorded transaction x and at least $k$ distinct eligible replicas from set E have completed event A for the same history and transaction.” Define transaction classes, A, $k$, E, failure domains, timeout, degraded behavior, and required client evidence. Without those terms, “synchronous” is marketing vocabulary.

The source may expose per-transaction choices. Critical ledger writes might require two remote durable flushes; reconstructible telemetry might use local durability; a read-after-write workflow might wait for apply/visibility on a chosen read replica. This flexibility needs authorization and observability so an application cannot accidentally downgrade durable classes.

**Distinguish acknowledgement points.** A common pipeline is:

1. source transaction commits and produces an ordered record;
2. source writes and durably flushes the record;
3. sender transmits it;
4. replica receives it;
5. replica writes it to its storage path;
6. replica durably flushes it;
7. replica replays/applies it;
8. replica exposes a safe read snapshot containing it.

A receive acknowledgement can survive a source process failure if replica memory survives, but not replica process/host loss. A remote write can survive some process failures but perhaps not operating-system or power loss. A durable flush is evidence about replica storage under the tested stack. Replay is needed for immediate service after promotion or read visibility, but waiting for it adds apply queueing and conflicts. Each engine defines its named modes; map them to tested events rather than assuming names.

**Choose priority or threshold membership.** A priority policy selects particular synchronous replicas, often preferring local low-latency candidates and substituting standbys in order. It is predictable but can let one chosen slow member dominate even when another healthy replica could satisfy the failure objective. A threshold policy waits for any $k$ members from an eligible set, reducing straggler sensitivity.

Thresholds must count distinct identities and match failure placement. Two acknowledgements from virtual machines backed by one host or storage system may not protect against that shared failure. A regional objective might require one acknowledgement in a named remote region rather than any one of three local nodes. Use topology predicates, not only a scalar $k$.

**Derive foreground latency.** Let local durable completion be $T_L$. For `ANY k`, sort qualifying remote acknowledgement times; success occurs after $\max(T_L,T_{(k)})$. Queueing and batching couple these values across requests. For priority `FIRST k`, the selected members determine the maximum even if a lower-priority member is faster. Network round trip, remote flush batch interval, apply queue, lock/conflict delay, and scheduling contribute to the tail.

Do not add independent averages and call the result a percentile. Measure end-to-end distributions under load and failure. Group commit can amortize source and replica flushes but can produce bursty acknowledgements. Synchronous apply can couple foreground latency to long-running standby queries or DDL conflicts.

**State loss exposure precisely.** Under asynchronous acknowledgement, the loss window includes locally successful transactions beyond the greatest position durable on the chosen failover candidate. Under a one-remote-flush policy, those successful transactions should exist on the source plus at least one qualifying remote copy—provided acknowledgements are truthful and promotion selects a copy at or beyond that frontier.

That is not an unlimited zero-loss theorem. A shared power/storage fault may destroy both. Corrupt log can be durably copied. A remote copy may be incompatible, unavailable, or on the wrong history. The control plane may promote an older replica. The old primary may keep serving writes. Name the covered failures and residual risks.

**Treat timeout as a policy transition.** When too few acknowledgements arrive, choices include blocking, rejecting new commits before they begin, returning an ambiguous timeout, or changing to a weaker mode under explicit authority. Automatic fallback improves write availability by weakening remote evidence. It must emit a durable state/alert and produce an auditable interval of transactions acknowledged under the weaker contract.

Product behavior varies. MySQL 8.4 semisynchronous replication can time out and revert to asynchronous replication. A design that promises remote durability cannot simply inherit that default without detecting and governing it. Conversely, indefinite blocking can exhaust connection pools and cause retry storms. Apply admission control before accepting work when the required mode is known unavailable.

**Model commit ambiguity.** Suppose the source commits locally, a replica flushes, and success is sent, but the response is lost. The client times out. Retrying a non-idempotent transaction can duplicate it, while assuming abort can omit required work. Give each business command a stable idempotency/transaction identity and provide authoritative status lookup. A cancellation request is not proof that commit stopped.

The same uncertainty exists when a synchronous wait times out just before a late acknowledgement. Product APIs may return an error after the source transaction has committed. Document error classes and test exact cut points.

**Separate reads from write acknowledgement.** Remote durable flush says the transaction can later be replayed; it does not say a current query can see it. Read-after-write on a replica requires a visibility token or session frontier and routing to a replica whose visible/replay frontier covers it. Waiting for remote apply may provide a stronger basis, but long-lived snapshots can still return older data under the database's isolation semantics.

Do not infer replica freshness from synchronous membership alone. A replica can cease being synchronous, reconnect, or lag in replay while another member provides acknowledgements. Route based on current typed frontiers and the read contract.

**Coordinate topology changes.** Adding a replica to the acknowledgement set requires base/history validation, catch-up, compatibility, durability tests, and failure-domain classification. Removing one may reduce the tolerated failure set. Changing $k$, membership, or acknowledgement stage is a safety change and should be versioned, reviewed, and rolled out with a rollback condition.

Membership configuration is not consensus. If different nodes use inconsistent acknowledgement sets or epochs, they can make incompatible claims. A leader/election protocol must bind authority and membership; this module evaluates the commit policy only after authority is established. Promotion must choose an eligible replica covering the required acknowledged frontier and fence old writers.

**Account for logical apply.** With logical replication, remote receipt or durable staging can protect the change envelope without proving it applied under target schema, constraints, conflicts, and transformations. Remote apply may fail later on a poison event. If the contract requires a usable target projection at success, the acknowledgement must include successful compatible target commit, not mere queue receipt.

Cross-system synchronous apply creates distributed-transaction-like coupling without automatically providing atomic rollback. If the source commits but a downstream index or service fails, waiting longer does not make the source and sink one transaction. Use explicit distributed coordination or design for asynchronous convergence.

**Engineer degraded operation.** Define states such as `normal-remote-flush`, `blocked`, `authorized-local-only`, and `recovering`. Specify who can transition, which transaction classes remain allowed, how clients learn the active guarantee, how weakened intervals are recorded, and what evidence restores normal mode. Do not oscillate automatically on single heartbeats; use health criteria and stabilization.

During degradation, preserve enough log for lagging replicas, cap source disk use, and understand backlog catch-up load. Restoring the configuration string is insufficient; qualifying replicas must cover the current frontier and pass integrity/eligibility checks.

**Validate acknowledgement truth.** Instrument source local durable, send, replica receive/write/flush/replay/visible, acknowledgement emission, threshold satisfaction, client response, timeout/fallback, and mode epoch. Correlate them by transaction identity and history.

Cut power/process/network before and after every stage. Delay or forge acknowledgements in a test harness, duplicate replica identities, isolate zones, fill disks, pause replay, change membership, rotate credentials, and lose client responses. For every reported success, prove the required artifacts survive the declared failure and are present on every candidate the promotion policy may choose. For every error, query transaction status before retry.

The executable model below evaluates one finite acknowledgement set. It orders remote durable-flush and apply times, reports threshold latency, and rejects duplicate replica identities. It does not run a database, network, storage flush, failure detector, election, or fence.

<!-- bijux-verify: {"id":"replication-ack-thresholds","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"local_durable_ms=4\nasync_success_ms=4\nany1_flush_ms=8\nany2_flush_ms=23\nany3_flush_ms=60\nany2_apply_ms=40\npriority_r2_r3_flush_ms=60\ndistinct_replicas=true\nduplicate_identity_rejected=true\nevidence=finite_acknowledgement_thresholds\n","stderr":""}} -->
```python
local_durable_ms = 4
replicas = [
    {"id": "r1", "flush": 8, "apply": 18},
    {"id": "r2", "flush": 23, "apply": 40},
    {"id": "r3", "flush": 60, "apply": 95},
]

def any_k(stage, k):
    times = sorted(replica[stage] for replica in replicas)
    return max(local_durable_ms, times[k - 1])

def priority(stage, selected):
    by_id = {replica["id"]: replica for replica in replicas}
    return max(local_durable_ms, *(by_id[name][stage] for name in selected))

distinct = len({replica["id"] for replica in replicas}) == len(replicas)
duplicate = replicas + [{"id": "r1", "flush": 7, "apply": 17}]
duplicate_rejected = len({replica["id"] for replica in duplicate}) != len(duplicate)

print(f"local_durable_ms={local_durable_ms}")
print(f"async_success_ms={local_durable_ms}")
print(f"any1_flush_ms={any_k('flush', 1)}")
print(f"any2_flush_ms={any_k('flush', 2)}")
print(f"any3_flush_ms={any_k('flush', 3)}")
print(f"any2_apply_ms={any_k('apply', 2)}")
print(f"priority_r2_r3_flush_ms={priority('flush', ['r2', 'r3'])}")
print(f"distinct_replicas={str(distinct).lower()}")
print(f"duplicate_identity_rejected={str(duplicate_rejected).lower()}")
print("evidence=finite_acknowledgement_thresholds")
```

## Definitions and Notation

- $T_L$: time at which the required source-local durability event completes.
- $T_i^A$: time at which eligible replica $i$ completes acknowledgement stage A.
- $T_{(k)}^A$: $k$th order statistic among qualifying remote acknowledgement times.
- $E$: eligible acknowledgement set, including identity, history, role, and topology predicates.
- $k$: required count of distinct qualifying acknowledgements.
- $F_{ack}$: greatest source frontier known to satisfy the configured acknowledgement policy.
- **Remote receive:** complete transaction record accepted into receiver ownership; durability unspecified.
- **Remote write:** record handed to a remote storage path; power-loss durability depends on definition.
- **Remote flush:** record reported durable by the remote storage stack under its tested contract.
- **Remote apply:** record effects committed/replayed on the replica; visibility may require an additional condition.
- **Priority policy:** waits for selected replicas according to an ordered membership rule.
- **Threshold policy:** waits for any $k$ distinct eligible members.
- **Degraded mode:** explicit operation under a weaker or unavailable acknowledgement contract.
- **Commit ambiguity:** client cannot infer committed/aborted outcome from its observation.

## Mechanisms, Invariants, or Proof Structure

**Latency derivation.** Success requires local event L and $k$ qualifying remote events A. The earliest time all predicates can hold is the later of $T_L$ and the $k$th-fastest qualifying remote completion: $T_{success}=\max(T_L,T_{(k)}^A)$. For fixed priority members, replace the order statistic with the maximum selected completion. Queueing, batching, eligibility changes, and response transmission add latency; the expression is a lower-bound model.

**Acknowledgement monotonicity.** For one replica and history, receive precedes write, write precedes durable flush, flush normally precedes or supports replay, and replay precedes declared visibility. An acknowledgement can safely imply only its completed stage and weaker stages whose definitions are proven by the engine. Product naming does not replace this causal proof.

**Loss-exposure argument.** If success requires truthful durable flush on $k$ independent eligible replicas plus the source, then every successful transaction has at least those durable copies at response time. Surviving a failure requires at least one such copy to remain available and be selected without history divergence. Thus remote flush reduces the stated loss window but promotion, common-mode failures, corruption, and fencing remain separate premises.

**Availability trade-off.** A strict threshold policy cannot acknowledge new commits when fewer than $k$ qualifying replicas can complete A. Lowering $k$ or falling back changes the safety predicate; it does not preserve the original guarantee by another name. The system can remain readable while writes block, so availability must identify operation and consistency class.

**Ambiguity argument.** A client timeout observes absence of a response, not absence of commit. Because commit and response are distinct events, there exists a cut after commit and before response with the same client observation as a pre-commit failure. Transaction identity and status lookup are therefore required to distinguish the cases.

## Alternatives and Trade-Offs

| Policy | Foreground dependency | Strength under stated assumptions | Cost or risk |
| --- | --- | --- | --- |
| Source local durable only | source flush | no remote copy required at success | nonempty failover loss window |
| Remote receive | one or more receiver acknowledgements | protects against narrower source failures | volatile remote state may vanish |
| Remote write | remote OS/storage-path write | stronger than receipt under some stacks | power-loss semantics may be weak |
| Remote durable flush | remote persistence evidence | durable remote copy under tested storage model | network and remote-flush tail |
| Remote apply | remote target/replay completion | smaller promotion/read catch-up gap | apply conflicts and queueing on write path |
| Priority `FIRST k` | named preferred members | explicit placement preference | selected straggler can block |
| Quorum-style `ANY k` | any $k$ eligible members | tolerates some stragglers | must enforce identity/topology predicates |
| Strict blocking | never weakens success contract | clear safety | write unavailability and pileups |
| Explicit local-only degradation | authorized weaker mode | continued writes with known exposure | recovery interval and failover risk |
| Automatic timeout fallback | quick liveness recovery | product-specific weaker contract | hidden durability downgrade |
| Per-transaction mode | workload-aligned trade-off | precise criticality | misuse and observability complexity |

## Failure Modes and Misconceptions

- **“Synchronous means no data loss.”** Only a defined remote event and failure model are covered.
- **“Semisynchronous is halfway durable.”** It is a product protocol; inspect the exact acknowledgement and fallback semantics.
- **“Received means persisted.”** Receiver memory and storage cache can disappear.
- **“Flushed means visible.”** Apply/replay and snapshot visibility can lag.
- **“Two acknowledgements mean two failure domains.”** Distinct process IDs can share host, rack, storage, power, region, or operator faults.
- **“Any quorum implies consensus.”** A commit acknowledgement threshold does not establish unique leadership or safe membership changes.
- **“Timeout means rollback.”** The transaction may have committed and the response may have been lost.
- **“Retry is safe because transactions are atomic.”** Atomicity does not deduplicate a second transaction.
- **“Fallback only affects performance.”** Moving from remote flush to local-only changes loss exposure.
- **“A synchronous member is current for reads.”** Another member may satisfy commits while this replica's replay stalls.
- **“Average RTT predicts commit latency.”** Tail order statistics, flush batching, queueing, and correlated stalls drive percentiles.
- **“The nearest replica is the safest failover.”** It may lack the greatest acknowledged frontier or share the failed domain.
- **“Restoring connectivity restores safety.”** The member must catch up, validate history/integrity, and re-enter the eligible epoch.
- **“Remote apply makes an external sink atomic.”** Source and sink commits still need a coordination protocol or compensating design.

## Worked Examples

### Example 1

**Situation.** Local durable completion is 4 ms; three remote durable flushes finish at 8, 23, and 60 ms.

**Reasoning.** Sort qualifying remote times. `ANY 1` uses the first order statistic, so $\max(4,8)=8$ ms. `ANY 2` uses 23 ms; `ANY 3` uses 60 ms. Local-only success is 4 ms. These are lower bounds before response transmission and other overhead.

**Conclusion.** Raising $k$ increases covered remote copies and exposes later tail members to the foreground path.

### Example 2

**Situation.** Replica R receives transaction x at 10 ms, writes at 12 ms, flushes at 18 ms, and applies at 45 ms.

**Reasoning.** A receive policy can answer after 10 ms but R may lose x with its process/host. A remote-write policy at 12 ms depends on storage-cache semantics. Remote-flush at 18 ms provides the tested durable-copy evidence. Remote-apply at 45 ms additionally reduces replay delay, but read visibility still follows the engine's snapshot contract.

**Conclusion.** The same replica yields four materially different commit contracts.

### Example 3

**Situation.** `ANY 2` is satisfied by replicas r1 and r2, but both are virtual machines on one storage array and power domain.

**Reasoning.** The count predicate holds, yet one array/power failure can remove both copies. If the requirement is survival of one zone failure, eligibility must encode different zones and independent durable storage, perhaps requiring one local-zone and one remote-zone acknowledgement.

**Conclusion.** Replica count is not failure independence; topology belongs in the acknowledgement predicate.

### Example 4

**Situation.** A semisynchronous source waits ten seconds, times out, then acknowledges subsequent commits asynchronously without clients changing requests.

**Reasoning.** Availability resumes but the remote-copy premise no longer holds. Record the exact transition time/frontier, alert clients/operators, restrict transaction classes if required, preserve source log, and make failover policy account for the weaker interval. MySQL 8.4 documents timeout-based fallback to normal replication for its semisynchronous plugin.

**Conclusion.** Automatic fallback is a durability-mode transition and must be observable and governed.

### Example 5

**Situation.** Payment command `pay-77` times out after 2 seconds. The source log and one remote replica contain its commit.

**Reasoning.** Reissuing a new payment can double charge. Query authoritative status by `pay-77`; if committed, return the stored result; if known aborted/not accepted, execute once; if unresolved, keep the command pending rather than guessing. The database response loss is independent of replication success.

**Conclusion.** Stable command identity and outcome lookup turn timeout uncertainty into a recoverable protocol state.

### Example 6

**Situation.** Priority members r1 and r2 flush at 8 and 60 ms; spare r3 flushes at 12 ms. A two-ack policy is required.

**Reasoning.** `FIRST 2` over r1,r2,r3 waits for selected r1 and r2, so no earlier than 60 ms. `ANY 2` can use r1 and r3 at 12 ms if both meet the same eligibility and placement objective. Priority may deliberately prefer a remote disaster-recovery site; `ANY` is not automatically better.

**Conclusion.** Membership semantics determine whether healthy alternatives reduce the tail.

### Example 7

**Situation.** The write waits for remote flush through position 900 on r1, then the application immediately reads from r1, whose visible frontier is 870.

**Reasoning.** Durability at 900 does not make transaction 900 query-visible. Pass a session token requiring visible frontier at least 900 and wait/route accordingly, or configure/test a remote-apply/visibility acknowledgement. Even then, an older explicit snapshot can intentionally omit it.

**Conclusion.** Synchronous durability does not by itself provide replica read-your-writes.

### Example 8

**Situation.** The source has acknowledged commits through 1,000 locally. Candidate r1 has durably flushed through 992; r2 through 997. The source is permanently lost.

**Reasoning.** If r2 is compatible, intact, and safely promotable, commits 998–1,000 are outside its durable frontier and may be lost: three positions under this simplified contiguous model. Promoting r1 would expose eight. Byte/position count does not equal business impact; inspect transaction identities.

**Conclusion.** Candidate selection determines realized loss within the asynchronous exposure window.

### Example 9

**Situation.** Two connections both advertise standby name `r1` and the threshold is two.

**Reasoning.** Counting connections can let one replica or misconfiguration satisfy two slots. Bind acknowledgement identity to authenticated instance identity and membership epoch, enforce uniqueness, and count one qualifying frontier per member. PostgreSQL documentation warns that standby names are not mechanically unique in its synchronous-standby configuration.

**Conclusion.** Threshold arithmetic is sound only over distinct authenticated members.

### Example 10

**Situation.** During a regional outage, authorized policy moved from one remote flush to local-only and acknowledged through 1,500. After connectivity returns, the remote replica is at 1,200.

**Reasoning.** Changing the setting back immediately would not place the weakened interval remotely. Retain and stream 1,201–1,500, verify continuous history and integrity, wait for durable remote coverage through the current source frontier, validate eligibility, then enter a new normal-mode epoch. Until then, failover can lose the degraded interval.

**Conclusion.** Restoring a durability promise requires frontier coverage, not merely configuration convergence.

## Cross-Program Connections

- Distributed Systems owns quorum intersection, leader election, consensus, membership, and network-partition theory; a database acknowledgement policy consumes those foundations but is not equivalent to them.
- Systems Engineering owns end-to-end failure-domain and assurance reasoning; replication membership must map process counts to real power, storage, network, regional, and operator dependencies.
- Software Delivery and Reliability Engineering owns safe configuration rollout, incident modes, SLOs, and rollback; acknowledgement-stage and threshold changes are production safety changes.
- API and Service Engineering owns idempotency and client retry contracts; commit ambiguity must surface as an API protocol rather than an undocumented database error.
- Operating Systems owns writeback, flush, storage ordering, process, and power-failure semantics beneath “remote write” and “remote flush.”
- Network Engineering owns latency, loss, partitions, and transport behavior; synchronous replication converts their tail behavior into foreground database latency.

## References

1. PostgreSQL Global Development Group. [PostgreSQL 18: Replication Configuration](https://www.postgresql.org/docs/18/runtime-config-replication.html), including `synchronous_commit` and priority/quorum synchronous standbys. Current documentation checked 2026-09-05.
2. PostgreSQL Global Development Group. [PostgreSQL 18: Synchronous Replication](https://www.postgresql.org/docs/18/warm-standby.html#SYNCHRONOUS-REPLICATION). Current write, flush, apply, and transaction-level behavior checked 2026-09-05.
3. PostgreSQL Global Development Group. [PostgreSQL 18: Replication Statistics](https://www.postgresql.org/docs/18/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW). Current acknowledgement-frontier monitoring checked 2026-09-05.
4. Oracle. [MySQL 8.4 Reference Manual: Replication](https://dev.mysql.com/doc/refman/8.4/en/replication.html). Current asynchronous default and semisynchronous overview checked 2026-09-05.
5. Oracle. [MySQL 8.4 Reference Manual: Configuring Semisynchronous Replication](https://dev.mysql.com/doc/refman/8.4/en/replication-semisync-interface.html). Current wait point, replica-count, timeout, and fallback semantics checked 2026-09-05.
6. Oracle. [MySQL 8.4 Reference Manual: Replication Threads](https://dev.mysql.com/doc/refman/8.4/en/replication-threads.html). Current receiver, relay-log, coordinator, and apply-worker behavior checked 2026-09-05.
7. Jim Gray and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1993. Commit, durability, logging, and distributed recovery foundations.
8. Philip A. Bernstein and Eric Newcomer. *Principles of Transaction Processing*, 2nd ed. Morgan Kaufmann, 2009. Commit protocols, failures, and recovery foundations.
9. Navin Budhiraja, Keith Marzullo, Fred B. Schneider, and Sam Toueg. “The Primary-Backup Approach.” In *Distributed Systems*, 2nd ed., ACM Press/Addison-Wesley, 1993. Primary-backup failure and replication foundations.
10. Diego Ongaro and John Ousterhout. [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf). USENIX ATC, 2014. Used only to distinguish quorum-backed replicated-state-machine commitment and leadership from a database's configurable remote acknowledgement path.

## Exercises

### Exercise 1

Explain why “two synchronous replicas” is not a complete durability contract. List the minimum information needed to make it testable.

### Exercise 2

Local durable time is 6 ms. Four eligible replicas have durable-flush times 10, 14, 31, and 90 ms and apply times 20, 28, 70, and 140 ms. Compute local-only, `ANY 1` flush, `ANY 3` flush, `ANY 2` apply, and priority flush for selected replicas 2 and 4.

### Exercise 3

A service promises every successful order is durably present in another zone. Its database automatically falls back to local-only after a five-second synchronous timeout, and the service does not expose the active mode. Diagnose the contract violation and design an operational correction.

### Exercise 4

Compare remote receive, durable flush, and apply for a cross-region database supporting rapid failover and replica read-after-write. Recommend a default and any transaction-specific overrides.

### Exercise 5

Design an acknowledgement policy for three local-zone replicas and two remote-region replicas. The business requires survival of any one zone loss for ordinary writes and survival of complete regional loss for settlement writes. Include thresholds, topology predicates, latency/degradation behavior, ambiguity handling, observability, and promotion constraints.

## Answers to the Exercises

### Answer 1

The phrase omits what event each replica acknowledges, whether the source is locally durable, which identities can count, whether they are distinct and in independent failure domains, which history/membership epoch applies, what happens on timeout, and how promotion uses the evidence. A testable contract names the transaction class; source-local requirement; acknowledgement stage (receive/write/flush/apply/visible); eligible authenticated set and topology; threshold or priority rule; timeout and degraded mode; client result semantics; covered failure model; and required promotion/fencing frontier. It also specifies monitoring and evidence retention.

### Answer 2

Sort flush times: 10, 14, 31, 90. Local-only is 6 ms. `ANY 1` flush is $\max(6,10)=10$ ms. `ANY 3` flush is 31 ms. Sort apply times: 20, 28, 70, 140; `ANY 2` apply is 28 ms. Priority flush for replicas 2 and 4 waits for both selected values 14 and 90, so it is $\max(6,14,90)=90$ ms. These are earliest modeled completion times; response transmission, batching, and queueing can add latency.

### Answer 3

The service's success claim is false during automatic fallback because success no longer requires another-zone durable evidence. Five-second waiting does not preserve the contract. Either disable fallback and reject/block protected writes when the remote condition is unavailable, or expose an explicitly authorized weaker service mode in which protected orders are rejected while less critical classes may continue. Record the mode epoch and first/last affected transaction frontiers, alert immediately, preserve log, bound source capacity, and require remote catch-up/integrity/eligibility through the current frontier before restoring the promise. Clients need stable order IDs and status lookup because timeouts can be ambiguous.

### Answer 4

Remote receive has the lowest remote stage latency but can lose acknowledged data with the remote process/host. Durable flush is the appropriate default when the main promise is recoverable remote state under the tested storage and failure model. Apply reduces promotion catch-up and can support a visibility-token path, but makes foreground writes depend on replay load, conflicts, and long standby queries. For rapid failover, pair remote flush with measured/bounded replay lag and promotion eligibility; for a small class requiring immediate replica reads, wait for a documented remote-apply/visible frontier or route reads to the source until the token is covered. Never infer query visibility from flush alone.

### Answer 5

For ordinary writes, require source-local durability plus one durable-flush acknowledgement from an eligible replica in a different local zone; encode distinct authenticated identity and zone, not merely `ANY 1` among all nodes. This survives loss of the source zone if the other-zone replica and control plane remain intact. For settlement writes, additionally require one durable-flush acknowledgement in the remote region; if regional independence requires two sites within that region, state that separately rather than assuming one replica survives all remote faults.

Use topology-aware predicates such as `one-of-local-other-zones AND one-of-remote-region` for settlement, not a scalar quorum that two local replicas can satisfy. Measure both tails and apply admission control when required members are unavailable. Ordinary writes may enter a recorded authorized local-only degraded mode if business policy permits; settlement writes should reject before execution or block within bounded resource limits rather than silently downgrade. Every command has an idempotency key and outcome lookup for ambiguous timeouts. Observe per-stage/per-member frontiers, mode epoch, failure domain, threshold satisfaction, latency percentiles, backlog, and retained log. Promotion must select a compatible intact candidate at or beyond the greatest frontier acknowledged for the transaction class, establish authority, and fence the old writer; a reachable but older replica is ineligible.
