---
module_id: DBE-081
program: Database Engineering
level: 2
module_number: 81
title: Physical Replication
status: complete
last_verified: 2026-09-05
---

# Physical Replication

## One-Page Review

### Governing question

How can a database reproduce one physical history on compatible replicas while preserving log order, durability and replay frontiers, page identity, version compatibility, bounded retention, and safe ownership under failure?

### Essential definitions

**Physical replication** transfers storage-level changes—commonly WAL/redo records, pages, blocks, or files—so a replica reconstructs a compatible physical database. A **base image** seeds the replica at a known position. **Log shipping** transports retained log segments; **streaming replication** sends records continuously. **Receive**, **write**, **flush**, **replay**, and **visible** frontiers describe increasingly stronger but not universally equivalent states. A **timeline**, **term**, or **history** identifies an ordered branch after promotion. A **replication slot** or retention lease records a consumer's required log frontier. A **cascading replica** receives history through another replica. A **hot standby** serves reads during replay under product-specific visibility and conflict rules. **Fencing** prevents a stale former primary from accepting authoritative writes.

### Central model, mechanism, or theorem

For one compatible history H, a replica's frontiers normally satisfy

$$
F_{visible} \le F_{replay} \le F_{flush} \le F_{write} \le F_{receive} \le F_{source},
$$

with meanings defined by the engine. A physical replica is eligible for a claimed role only when its base identity, log ancestry, formats, required frontier, integrity, transaction visibility, and ownership policy all pass. Byte receipt is not durability; durable flush is not replay; replay is not necessarily query visibility or safe promotion.

### Critical invariants

- The replica base and every applied record belong to the same database incarnation and a valid history ancestry.
- Transport preserves complete record bytes and ordering; duplicates are handled idempotently, while gaps block replay.
- The replica never advances write/flush/replay/visible frontiers beyond their actual completed evidence.
- Page identity, generation, format, and integrity validate before a physical record or page image is trusted.
- Source log is retained until every protected replica/slot has durably passed its required restart frontier or is explicitly invalidated.
- Mixed-version replication is allowed only across a tested physical-format and protocol compatibility matrix.
- Read service exposes only snapshots safe under replay/conflict semantics.
- Promotion requires authoritative election plus enforceable fencing and creates a new history/epoch.

### Common failures

Failures include calling received bytes durable; calling flushed WAL applied; choosing a failover candidate by bare numeric LSN; streaming from a base on another timeline; ignoring a missing middle segment; letting a stale slot fill the primary disk; deleting a slot without acknowledging reseed/data-loss consequences; assuming replicas repair primary corruption; serving reads before visibility/index/catalog state is safe; replaying new physical formats with old binaries; promoting without fencing; measuring byte lag as time or business staleness; and treating an online replica as an independent historical backup.

### Compact example

The source has durable WAL through 1,000. Replica R has received 950, written 930, flushed 900, replayed 820, and exposed a safe snapshot through 800. Under these declared frontiers it can survive a replica process crash through 900, but its pages represent history only through 820 and its queries only promise visibility through 800. It is not eligible for a zero-loss failover requiring source commit 1,000. Byte gaps are receive 50, flush 100, replay 180, and visible 200; none alone is a time-lag guarantee.

### Connections

Retrieve [Write-Ahead Logging](072-write-ahead-logging.md), [Log Sequence Numbers](073-log-sequence-numbers.md), [Crash Recovery](078-crash-recovery.md), and [Point-in-Time Recovery and Restore Verification](080-point-in-time-recovery-and-restore-verification.md). Continue through [the program roadmap](../ROADMAP.md) to logical replication, acknowledgement modes, lag/stale reads, election/failover, sharding, distributed transactions, and consensus-backed replication.

## Governing Question

A physical replica promises to become another copy of the same database without re-executing SQL or translating every row. That apparent simplicity hides a strict coupling: the replica must understand the primary's page and WAL formats, start from a compatible base, follow one history, apply physical changes in order, and reproduce transaction visibility and structural state.

What exactly does “caught up” mean? The network receiver can hold bytes the kernel has not persisted. Persisted WAL can await replay. Replayed changes can await a safe query snapshot. A replica can match an LSN yet belong to a divergent timeline. A correct design exposes typed frontiers and bases every acknowledgement, read, retention, and failover decision on the relevant one.

## Why This Matters

Physical replication is efficient because recovery-oriented records already encode storage changes. It can reproduce indexes, catalogs, and engine-private structures without logical decoding, and it supports read scaling, rapid failover candidates, backup seeding, and disaster recovery. Its cost is tight compatibility and faithful propagation: destructive transactions, many corruptions, and physical bloat are replicated too.

Replication is a pipeline across failure domains. Source logging, sender, network, receiver, durable storage, replay workers, visibility, feedback, retention, and orchestration can each stall or fail. A single “replica lag” metric collapses distinct risks: primary-disk exhaustion, loss exposure, stale queries, failover readiness, or replay CPU debt.

Current PostgreSQL documentation distinguishes sent, written, flushed, and replayed WAL positions and supports asynchronous/synchronous streaming, replication slots, timelines, cascading, and hot standby. MySQL 8.4 uses binary-log replication primarily at logical/row or statement event levels rather than being a direct analogue to PostgreSQL physical WAL shipping; InnoDB Cluster/replica technologies have different protocols. This module owns the storage-level physical model and uses product examples without relabeling every vendor replication stream as physical.

## Prerequisites and Retrieval

Retrieve these concepts:

- a base backup is valid only with matching database/system ID, history, formats, manifest, and required log;
- WAL records form a complete ordered history with defined start/end positions;
- receive, publish, write, flush, apply, transaction visibility, and acknowledgement are separate events;
- checkpoints/restartpoints bound recovery but do not authorize skipping an unreceived record;
- pageLSN comparisons require page identity, generation, format, and integrity;
- promotion forks history and must fence stale writers;
- MVCC snapshots and recovery conflicts determine which standby reads are safe;
- retention frontiers from replicas, archives, backups, recovery, and decoders share finite log capacity;
- network security, authentication, authorization, encryption, and traffic limits apply to the replication channel.

DBE-080 established backup/log lineage and promotion verification. This module develops physical propagation; DBE-082 contrasts logical change streams.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical log shipping, streaming, page shipping, and logical replication;
2. design replica bootstrap with identity, history, format, and start-position validation;
3. reason independently about receive, write, flush, replay, visibility, and feedback frontiers;
4. enforce complete ordered replay under duplicates, gaps, reconnects, corruption, and restart;
5. operate retention slots, cascading topologies, read replicas, and rebuilds safely;
6. evaluate physical compatibility across versions, platforms, page sizes, encryption, and extensions;
7. derive promotion eligibility without conflating it with election or fencing;
8. validate replication using deterministic cuts, failover drills, oracles, security checks, and capacity tests.

## Core Exposition

**Choose the replicated representation.** WAL/redo shipping transfers recovery records; page/block shipping transfers resulting physical images; file/snapshot refresh transfers larger immutable units. WAL is incremental and ordered but coupled to record readers and retained history. Page shipping can repair or seed efficiently but needs page identity/generation and consistency metadata. Snapshot refresh reduces replay distance but transfers more data.

Physical replication differs from logical replication because it preserves engine storage semantics rather than a selected committed data model. It usually reproduces all databases and internal objects in the physical authority, though products can have tablespace or filtering exceptions. It cannot casually transform schema, collation, page size, or storage engine during replay.

**Bootstrap from a proven base.** Create or select a base through the supported online-backup/snapshot protocol. Record system/database ID, timeline/history, checkpoint/start position, page/log formats, block size, checksum/encryption settings, tablespaces, extensions, architecture constraints, and manifest digests. Copy into isolation and verify before registering the replica.

The source must retain log from the base's required start until the replica confirms the appropriate durable restart frontier. If the log is gone, a numerically close replica cannot fill the gap; reseed from a newer compatible base or retrieve the exact archive history.

**Separate pipeline frontiers.** Define:

- sent/receive: complete bytes transferred into receiver ownership;
- write: bytes passed to the replica's storage path;
- flush: contiguous prefix proven durable on the replica;
- replay: records whose effects have been applied under recovery semantics;
- visible: latest transaction/snapshot boundary safe for the declared query API.

Products can combine or name these differently. Preserve their exact semantics. A synchronous policy might wait for remote write, flush, or replay; each survives different failures and adds different latency.

**Maintain contiguous history.** Sequence records or segments by typed history positions. Validate lengths, checksums/authentication, previous links where applicable, system ID, timeline, and format. Duplicates after reconnect are safe only when identity and replay guards establish idempotence. A gap stops advancement even if later segments arrive. Feedback cannot jump across a missing range.

Use bounded reordering buffers if transport can reorder, then advance only the contiguous prefix. Protect against a malicious or corrupt sender advertising enormous lengths or far-future positions. Persist enough receiver metadata to resume after process/host crash without falsely reporting a volatile frontier.

**Replay as recovery.** Replay validates records/pages and applies physical effects in history order, using pageLSN or engine-specific guards. It must reproduce transaction status, catalogs, indexes, allocation, and structural actions. Parallel replay requires per-page and cross-object dependency proofs; a later pageLSN cannot be published before its prerequisites.

The replica can create local restartpoints after safely flushing replayed state, but it cannot invent source history. On crash it restarts from its durable receive/replay evidence. Record replay errors, corrupt pages, missing keys, and unsupported formats explicitly rather than skipping them.

**Define standby visibility.** A hot standby normally exposes snapshots consistent with a replay frontier. Long queries can conflict with replay that removes old versions, drops objects, or changes locks. Policies can delay replay, cancel conflicting queries, retain upstream history, or feed back horizons that increase primary bloat. None is free.

Report snapshot/transaction visibility, not only replay LSN. A query can remain on an older snapshot while the replica replays later commits. Clock-based freshness estimates need correlated commit metadata and uncertainty; bytes do not equal seconds or business events.

**Operate feedback and retention.** A replica reports restart/receive/flush/replay frontiers to the source. A retention slot protects the oldest log it may still need. Durable slots survive source restart but can pin unbounded storage if the consumer disappears. Track owner, purpose, last heartbeat/advance, retained bytes, safe capacity, and invalidation/reseed policy.

Deleting or advancing a slot is not cleanup when the replica still depends on it. It explicitly abandons incremental continuity. Preserve an alternative archive or schedule a new base, then invalidate under authority. At capacity limits, backpressure or controlled consumer loss is safer than silent required-log deletion.

**Design cascading topologies.** A downstream replica can receive from an intermediate, reducing source fan-out and crossing regions efficiently. Its maximum history is bounded by every upstream link and retention decision. Failure of the intermediate can require reparenting, but the new source must share compatible ancestry and retain the downstream's needed position.

Track end-to-end and hop frontiers. A downstream may be connected and current relative to a lagging intermediate while far behind the primary. Promotion of an intermediate changes histories and requires downstream validation/reconfiguration.

**Respect compatibility.** Physical formats can change across major versions, builds, architectures, storage engines, encryption keys, checksums, page sizes, or extensions. Support only documented matrices plus direct tests. Rolling upgrades require an overlap in which senders and replay binaries understand emitted records. Once a writer emits an incompatible durable format, binary rollback can become impossible.

Canary new replay binaries on disposable/reseedable replicas, compare page/log and query oracles, then upgrade candidates before primaries where the vendor protocol recommends it. Preserve a verified base and log path for rollback/rebuild.

**Treat corruption propagation honestly.** Physical replication can copy corrupt log records, logical destructive transactions, and some page corruption. Checksums can detect but not automatically correct. A replica may provide a repair source only when its page identity, generation, history, and integrity prove compatibility. Replication is not a historical backup because it converges toward current history.

**Separate eligibility, election, and fencing.** Eligibility asks whether a candidate covers the required durable history, has applied/validated enough state, supports formats, and can meet role invariants. Election selects one candidate under membership rules. Fencing prevents old writers. Promotion records a new term/timeline and publishes it durably. DBE-085 develops the full failover protocol; physical replication supplies evidence but not authority by itself.

**Secure the channel and files.** Authenticate both endpoints, authorize the exact replication identity, encrypt sensitive transport, rotate credentials without losing connectivity, and prevent downgrade/replay across histories. Treat WAL as sensitive: it can contain row images, credentials accidentally stored in data, and deleted values. Apply least privilege, retention, audit, rate limits, and protected at-rest keys.

**Validate every boundary.** Generate histories with commits, aborts, page splits, checkpoints, large records, DDL, prepared work, and full-page images. Cut connections/processes/power before and after source publication, send, receive, write, flush, replay, feedback, slot persistence, restartpoint, and promotion. Inject duplicate/out-of-order/missing/corrupt segments, stale timelines, wrong bases, full disks, slow replay, key loss, mixed versions, and query conflicts.

Oracles compare acknowledged commits, rows, visibility, indexes, catalogs, allocations, checksums, sequence promises, and history ancestry. Measure each frontier, gap, rate, stall duration, retained bytes, estimated exhaustion, conflicts, replay errors, rebuild time, and failover readiness without claiming more than the tested failure model.

The executable model below checks typed frontier ordering and candidate eligibility for one finite replica. It does not perform network, storage, replay, visibility, election, or fencing work.

<!-- bijux-verify: {"id":"finite-physical-replica-frontiers","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source=1000\nreceive=950\nwrite=930\nflush=900\nreplay=820\nvisible=800\nfrontiers_ordered=true\nreceive_gap=50\nflush_gap=100\nreplay_gap=180\nvisible_gap=200\nzero_loss_candidate=false\nread_bound_satisfied=true\ndifferent_history_comparable=false\nevidence=finite_physical_replica_frontiers\n","stderr":""}} -->
```python
frontier = {
    "source": 1000,
    "receive": 950,
    "write": 930,
    "flush": 900,
    "replay": 820,
    "visible": 800,
}
ordered = (
    frontier["visible"] <= frontier["replay"] <= frontier["flush"]
    <= frontier["write"] <= frontier["receive"] <= frontier["source"]
)
required_zero_loss = 1000
required_read_bound = 780

for name in ("source", "receive", "write", "flush", "replay", "visible"):
    print(f"{name}={frontier[name]}")
print(f"frontiers_ordered={str(ordered).lower()}")
print(f"receive_gap={frontier['source'] - frontier['receive']}")
print(f"flush_gap={frontier['source'] - frontier['flush']}")
print(f"replay_gap={frontier['source'] - frontier['replay']}")
print(f"visible_gap={frontier['source'] - frontier['visible']}")
print(f"zero_loss_candidate={str(frontier['flush'] >= required_zero_loss).lower()}")
print(f"read_bound_satisfied={str(frontier['visible'] >= required_read_bound).lower()}")
print("different_history_comparable=false")
print("evidence=finite_physical_replica_frontiers")
```

## Definitions and Notation

- `H`: database log history/timeline/term with ancestry.
- `B`: compatible verified base image and its required start.
- `F_source`: source's declared comparison frontier, normally a durable or sent endpoint.
- `F_receive`, `F_write`, `F_flush`: replica transport and persistence frontiers.
- `F_replay`: greatest source position whose physical effects are applied under recovery semantics.
- `F_visible`: greatest transaction/snapshot boundary safe for the declared read contract.
- **Restart frontier:** oldest log the replica might still require after restart.
- **Retention slot:** durable source-side ownership of a consumer's retained history.
- **Replica eligibility:** predicate over history, durability/replay, integrity, formats, resources, and role requirements.
- **Reparenting:** changing a replica's upstream while preserving compatible history continuity.
- **Reseed:** replace/reconstruct a replica from a new verified base when incremental continuity is unavailable.
- **Physical oracle:** independent check of pages/log/catalog/index/allocation and committed logical results.

## Mechanisms, Invariants, or Proof Structure

**Frontier monotonicity.** Within one history, each frontier advances only after its named event completes over a contiguous prefix. The partial order follows from pipeline causality. Products can define visible differently, so its relation must be justified rather than assumed universally.

**Replay safety.** Given a compatible base, complete validated history, and correct recovery algorithm, ordered record application with page identity/integrity and LSN guards reconstructs the source physical history through the replay frontier. The conclusion excludes corrupt source truth, external effects, and unsupported formats.

**Retention safety.** If a replica can restart from position R and no independent exact source exists below R, source recycling must remain before R. Advancing/deleting that obligation destroys incremental recoverability and requires explicit invalidation/reseed.

**Eligibility implication.** A candidate safe for requirement Q must satisfy the frontier named by Q, compatible history ancestry, integrity/format/resource gates, and fencing/election prerequisites. Equal bare offsets or low receive lag cannot imply the conjunction.

**Cascading bound.** A downstream's end-to-end progress cannot exceed the minimum available contiguous frontier across its upstream path. Local hop health does not prove proximity to the root primary.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or risk | Evidence |
| --- | --- | --- | --- |
| Segment log shipping | simple immutable transfer/archive reuse | coarse latency | segment continuity and restore |
| Streaming WAL | low propagation latency | persistent connection/backpressure | cut-point and restart tests |
| Page/block shipping | direct repair/seed potential | identity/generation complexity | checksums and history proof |
| Direct source fan-out | simple topology | primary network/CPU load | capacity and failure tests |
| Cascading | reduces root fan-out, regional hierarchy | compounded lag/reparenting | end-to-end frontiers |
| Async physical replica | low primary commit cost | acknowledged-loss window | explicit RPO and drills |
| Sync remote flush | stronger failover durability | network/quorum tail latency | failure-domain tests |
| Hot standby reads | uses replica capacity | stale/conflicting snapshots | visibility and conflict evidence |

## Failure Modes and Misconceptions

1. **“Received means durable.”** It may exist only in process/kernel memory.
2. **“Flushed means replayed.”** Durable WAL can await page application.
3. **“Replayed means every query sees it.”** snapshot visibility and conflicts can lag.
4. **“Equal LSN means equal state.”** history/system identity and integrity must match.
5. **“Later segments bridge a gap.”** required middle history is not reconstructable in general.
6. **“Replication slots are harmless metadata.”** stale slots can exhaust source storage.
7. **“Deleting a slot frees space safely.”** it can force reseed or lose the replica.
8. **“Physical replicas are backups.”** they converge and often share corruption/credentials/failure domains.
9. **“Replicas repair corruption automatically.”** faithful replay may propagate it.
10. **“Byte lag is seconds.”** rate and apply work vary.
11. **“Hot standby is current.”** its query snapshot can be behind replay/source.
12. **“Cascading child health means root currency.”** every upstream frontier bounds it.
13. **“Old binaries can replay new WAL.”** physical compatibility must be documented/tested.
14. **“Most advanced replica should promote.”** eligibility, election, and fencing are distinct.
15. **“TLS alone secures replication.”** identities, authorization, files, keys, retention, and audit also matter.
16. **“One failover test proves durability.”** failure domain, cut, load, version, and history bound the evidence.

## Worked Examples

### Example 1

**Situation.** A replica is seeded from base history H4 at 500 but configured to consume sibling H5 records after a fork at 450.

**Reasoning.** The base already contains H4-specific history past the fork. H5 is not its descendant, so physical replay can apply incompatible state despite plausible LSNs. Reseed from a base on H5 or a common ancestor no later than the fork with the exact H5 path.

**Conclusion.** Physical replay requires ancestry compatibility, not numeric position proximity.

### Example 2

**Situation.** Source is 1,000; replica receive 950, flush 900, replay 820, visible 800.

**Reasoning.** Transport backlog is 50, remote durable gap 100, physical apply gap 180, and declared read gap 200 position units. A source crash can lose source-only 901–1,000 if promotion requires remote flush and no other copy exists. Queries promise only 800.

**Conclusion.** Each frontier answers a different durability, replay, or freshness question.

### Example 3

**Situation.** Segments 10 and 12 arrive before 11.

**Reasoning.** Verify and buffer 12 within bounded capacity, but advance receive-contiguous/replay only through 10. Request 11. If unavailable, stop and reseed/repair; replaying 12 can depend on missing transaction/page state from 11.

**Conclusion.** Out-of-order arrival never permits a frontier to cross a gap.

### Example 4

**Situation.** The network duplicates record 700 after reconnect; the replica page already has validated pageLSN 700.

**Reasoning.** Identity, history, record checksum, page identity/generation, and pageLSN validate. The recovery guard skips physical reapplication. If the record described a non-idempotent external effect, physical WAL replay would not be a sufficient protocol—but such effects are outside this page operation.

**Conclusion.** Duplicate transport is safe only through typed recovery idempotence, not because duplication is harmless generally.

### Example 5

**Situation.** A slot has not advanced for two days and retains 4 TB with only 500 GB free.

**Reasoning.** Estimate exhaustion, page the owner, diagnose reachability/replay, throttle or expand capacity, and confirm an archive/new base path. Deleting the slot abandons its restart frontier and normally requires reseeding. Make that decision explicit before the primary reaches ENOSPC.

**Conclusion.** Slot retention couples replica availability to primary capacity and needs an invalidation policy.

### Example 6

**Situation.** A downstream is zero bytes behind its regional cascading source, which is 600 GB behind the primary.

**Reasoning.** Local hop lag is zero, end-to-end lag is at least 600 GB. Report both path frontiers. Reparenting directly to primary is possible only if ancestry matches and primary/archive retains the downstream's required start.

**Conclusion.** Cascading health is path-relative; root currency requires end-to-end evidence.

### Example 7

**Situation.** A six-hour standby query needs old row versions that replay would remove.

**Reasoning.** The engine can cancel the query, delay replay, or retain upstream cleanup horizons through feedback. Delay increases stale-read/failover lag; feedback can bloat the primary. Route analytical work elsewhere or bound query duration based on explicit priorities.

**Conclusion.** Hot-standby availability trades against replay currency and primary version retention.

### Example 8

**Situation.** A replica detects a checksum failure in a page whose source counterpart also fails.

**Reasoning.** Replication faithfully propagated or shared the defect. Stop using either as a repair oracle. Locate a validated backup/full-page image or reconstruct logically, inspect adjacent pages/history, and expand corruption sampling.

**Conclusion.** Redundant current copies do not provide independent historical integrity.

### Example 9

**Situation.** A new primary emits WAL record version 9 while one failover replica understands through 8.

**Reasoning.** That replica can no longer replay or serve as a safe rollback target. Upgrade/verify readers before writers emit version 9, or maintain a protocol compatibility mode. Once incompatible history is durable, rollback requires a version-9 reader or reseed/migration.

**Conclusion.** Physical format rollout is a reader-before-writer protocol migration.

### Example 10

**Situation.** Replica R has the greatest replay LSN but its old primary remains writable after promotion.

**Reasoning.** R may be most current yet promotion is unsafe without fencing. Obtain a new authoritative term/epoch, make storage/clients reject the old term, validate required durability and history, then promote and record a new timeline. Eligibility does not confer authority.

**Conclusion.** Physical currency, election, and fencing are separate prerequisites for safe failover.

## Cross-Program Connections

- **Distributed Systems:** logs, epochs, ancestry, failure detection, quorum acknowledgement, and fencing define safe replication authority.
- **Operating Systems:** socket buffers, page cache, fsync, storage errors, checksums, and scheduling separate receive/write/flush/replay.
- **Concurrent and Parallel Programming:** sender publication, receiver queues, parallel replay, feedback, and cancellation require happens-before proofs.
- **Platform Engineering:** topology, slots, capacity, TLS identities, monitoring, upgrades, rebuilds, and drills operationalize replicas.
- **Security Engineering:** WAL confidentiality, mutual authentication, authorization, key rotation, and corruption handling protect the channel.
- **Data Architecture Engineering:** RPO/RTO, region placement, lineage, backup independence, and read-staleness policy govern use.
- **API and Service Engineering:** routing and read-your-writes/session guarantees must select a replica frontier appropriate to the request.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18: Log-Shipping Standby Servers](https://www.postgresql.org/docs/18/warm-standby.html), reviewed 2026-09-05. Official physical WAL shipping, streaming, cascading, slots, synchronous modes, and failover foundations.
2. PostgreSQL Global Development Group, [PostgreSQL 18: Monitoring Database Activity](https://www.postgresql.org/docs/18/monitoring-stats.html), reviewed 2026-09-05. Official sender/receiver write, flush, replay, and lag observability.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Hot Standby](https://www.postgresql.org/docs/18/hot-standby.html), reviewed 2026-09-05. Official standby query, snapshot, conflict, and feedback behavior.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Replication Slots](https://www.postgresql.org/docs/18/warm-standby.html#STREAMING-REPLICATION-SLOTS), reviewed 2026-09-05. Official retention semantics and operational cautions.
5. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_rewind`](https://www.postgresql.org/docs/18/app-pgrewind.html), reviewed 2026-09-05. Official divergent-timeline resynchronization scope and prerequisites.
6. Oracle, [MySQL 8.4 Reference Manual: Replication Formats](https://dev.mysql.com/doc/refman/8.4/en/replication-formats.html), reviewed 2026-09-05. Official statement/row/mixed binary-log semantics used to distinguish logical event replication from physical WAL.
7. C. Mohan et al., “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM TODS* 17(1), 1992. Primary physical recovery-record, pageLSN, and replay foundations; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
8. Jim Gray, Pat Helland, Patrick O'Neil, and Dennis Shasha, “The Dangers of Replication and a Solution,” *ACM SIGMOD*, 1996. Primary analysis of replication scale/conflict concerns.
9. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable logging, recovery, and replicated transaction foundations.

## Exercises

### Exercise 1

Define physical replication, base, history, receive/write/flush/replay/visible frontiers, restart frontier, retention slot, eligibility, promotion, and fencing.

### Exercise 2

Source durable is 2,000. Replica A has receive/write/flush/replay/visible `1980/1960/1900/1850/1800`; replica B has `1950/1950/1940/1700/1680`. Compare process-crash durability, replay/read currency, and zero-loss failover eligibility for required commit 1,920.

### Exercise 3

Design a physical replication receiver and persistent state machine covering base validation, record framing, duplicates, gaps, checksums, reconnect, flush, replay, feedback, restart, and history change.

### Exercise 4

Compare direct streaming, segment shipping, cascading, and periodic snapshot reseeding across latency, source load, retention, region failure, compatibility, and recovery objectives.

### Exercise 5

Design a mixed-version physical-replication rollout and validation campaign with security, corruption, capacity, hot reads, promotion, canarying, and rollback/reseed.

## Answers to the Exercises

### Answer 1

Physical replication transfers storage-level records/pages so a compatible replica reconstructs one database history. A base is the verified starting image and position. History names the timeline/term ancestry. Receive owns transferred bytes; write submits them to storage; flush proves a contiguous durable prefix; replay applies effects; visible bounds the read contract. Restart is the oldest log still needed after failure. A retention slot protects that need at the source. Eligibility proves a candidate satisfies a role's history/frontier/integrity/format/resource requirements. Promotion assigns authoritative writable history; election chooses the candidate; fencing excludes stale writers. None of the frontiers, election, or promotion terms are interchangeable.

### Answer 2

A's durable remote flush is 1,900 and B's is 1,940, so B retains required commit 1,920 across a replica process/host crash under the stated storage model while A does not. A is more replayed/visible (1,850/1,800 versus 1,700/1,680), so it is more current for immediate pages/reads but lacks the required durable commit. B can potentially replay from 1,700 to at least 1,920 and become eligible, subject to compatible history, integrity, transaction state, formats, resources, election, and fencing. Neither current state alone proves zero-loss promotion: B needs replay/verification policy, and both need history/authority checks.

### Answer 3

Persist system ID, timeline/history, base/checkpoint/start, format versions, and last durable receiver frontier. Frame each record with bounded overflow-safe length, position/history, type/version, and checksum/authentication. Accept duplicates only when exact identity matches; buffer bounded reordering but advance contiguous receive/write/flush only across no gaps. Flush metadata/frontier after actual storage synchronization. Replay through the recovery engine with page identity/generation/integrity and ordered dependencies, recording restartpoints. Feedback reports typed durable/replay/restart positions and never exceeds local evidence. After crash, revalidate base/control/log and resume from durable state. Reconnect authenticates peer/history and requests the first missing endpoint. Promotion/history mismatch pauses and requires ancestry-aware reparenting or reseed.

### Answer 4

Direct streaming minimizes hops and latency but consumes root connections/network. Segment shipping is immutable/archive-friendly and robust to disconnects but coarser. Cascading reduces root load and supports regional distribution but compounds lag and makes reparenting/retention path-dependent. Snapshot reseeding bounds old-log retention and repairs lost continuity but transfers large bases and creates periodic currency gaps. Compare per-hop and end-to-end durability/replay, source capacity, maximum outage/retention, archive availability, region independence, base transfer/rebuild time, format compatibility, and RPO/RTO drills. A hybrid commonly streams normally, archives segments independently, cascades regionally, and periodically reseeds.

### Answer 5

Inventory WAL/page/control/protocol/encryption/extension compatibility for every source, replica, backup, and recovery binary. Upgrade and canary replay readers before any primary emits new mandatory format. Feed production-like copies through commits, aborts, DDL, page splits, checkpoints, full-page images, and query conflicts; compare logical/structural/checksum oracles. Inject duplicate/gap/corrupt WAL, wrong timeline/base, slow network/replay, ENOSPC from slots, key/credential rotation, worker/host/power loss, and promotion with stale-writer attempts. Observe every frontier, conflicts, retained bytes/exhaustion, errors, read staleness, and rebuild/failover time. Promote only fenced eligible candidates. Rollback before new emission may restore old writers; afterward retain compatible new readers or reseed/migrate—never let an old binary ignore unknown physical records.
