---
module_id: DBE-077
program: Database Engineering
level: 2
module_number: 77
title: Group Commit
status: complete
last_verified: 2026-09-05
---

# Group Commit

## One-Page Review

### Governing question

How can concurrent transactions share one durable log flush while preserving each transaction's exact durability contract, bounded latency, failure semantics, and fair progress?

### Essential definitions

**Group commit** batches multiple commit waiters behind one persistence operation. A transaction's **commit LSN** is the log endpoint that must be durable before its synchronous commit can be acknowledged. The **flush frontier** is the greatest contiguous log endpoint proven durable under the declared storage contract. A **leader** performs or coordinates a flush; **followers** wait for a frontier. A **batch cut** is the set of published commit positions included in a flush target. A **grouping window** intentionally waits for peers; **natural grouping** uses requests already accumulated. **Commit latency** runs from the transaction's commit request to its result; **flush latency** covers the persistence operation. **Asynchronous commit** acknowledges before the required durable frontier and is a different durability policy, not faster group commit.

### Central model, mechanism, or theorem

For synchronous waiter i with required endpoint `c_i`, acknowledgement is safe only if

$$
F_{durable} \ge c_i,
$$

where `F_durable` is a verified contiguous durable frontier in the same log history. A leader may choose target `T=max(c_i)` over a batch, persist through T once, publish the frontier with correct synchronization, and wake every waiter whose requirement is at most T. Batching amortizes a fixed flush cost, but it does not change WAL ordering, storage truth, commit authority, or the response ambiguity created by connection failure.

### Critical invariants

- Publish a commit record completely before it becomes eligible for the flush target.
- Never advance the durable frontier across a reservation hole, partial record, failed flush, wrong history, or unverified persistence result.
- A synchronous waiter returns success only after its commit endpoint is covered by the durable frontier.
- Wake predicates are rechecked in a loop; a notification is not durability evidence.
- Leader cancellation, timeout, or death transfers ownership without losing waiters or duplicating unsafe acknowledgement.
- Batch policy bounds delay and starvation and distinguishes latency objectives by workload class.
- Flush errors become explicit transaction/system outcomes; they never advance the frontier.
- Metrics distinguish queueing, grouping delay, flush, replication wait, and client delivery.

### Common failures

Failures include acknowledging every queued transaction when the flush covered only an earlier prefix; selecting a target beyond a log-publication hole; treating `write` completion as durable flush; using sleep as the correctness mechanism; losing followers when a leader exits; waking without rechecking; holding a global mutex during slow I/O; starving sparse workloads behind a minimum batch size; confusing group commit with asynchronous commit; double-counting a transaction after retry; hiding flush errors; and claiming the client knows the outcome when commit became durable but the response was lost.

### Compact example

The durable frontier is 100. Three published transactions require endpoints 120, 150, and 170. One leader chooses target 170, performs one successful durable flush, publishes frontier 170, and wakes all three; each predicate `frontier >= commitLSN` holds. A fourth transaction at 210 arrives after the batch cut and is not acknowledged by the 170 flush. If the leader instead receives an I/O error, frontier remains 100 and none of the three synchronous transactions receives success, even if some bytes may have reached an unverified cache.

### Connections

Retrieve [Life of a Transactional Write](010-life-of-a-transactional-write.md), [Failure Models](071-failure-models.md), [Write-Ahead Logging](072-write-ahead-logging.md), and [Log Sequence Numbers](073-log-sequence-numbers.md). Continue through [the program roadmap](../ROADMAP.md) to crash recovery, backup, restore, and replication.

## Governing Question

A persistence barrier often has a fixed cost much larger than copying one small commit record. Flushing separately for every transaction preserves a simple mental model but wastes opportunities: one flush through LSN 170 also covers complete records ending at 120 and 150. How should concurrent callers coordinate that shared operation without weakening any caller's promise or adding unbounded delay?

The mechanism is small; the contract is not. Log insertion may have holes, storage may lie or fail, leaders may be cancelled, replication may add another acknowledgement frontier, and clients may disconnect after durability but before observing success. Group commit is therefore a concurrent frontier protocol, not merely “sleep briefly, then fsync.”

## Why This Matters

At high transaction rates, per-transaction synchronization can serialize work around storage latency. Group commit amortizes the fixed part of log synchronization over several commits, increasing throughput and sometimes reducing queueing. It can also increase latency at low load if the system waits for a batch that never arrives. The right policy depends on arrival rate, flush distribution, storage parallelism, log-buffer pressure, transaction class, and durability mode.

Group commit preserves durability only when all waiters are tied to exact log endpoints and the storage operation proves a contiguous prefix. A leader cannot infer that a later reserved position is complete. Nor can an operating-system `write` or device queue completion substitute for the configured durable boundary. DBE-071 and DBE-072 established those assumptions; batching merely shares their cost.

Current PostgreSQL documentation exposes `commit_delay` and `commit_siblings` for optional group-commit delay and distinguishes `synchronous_commit` durability policies. MySQL documents binary-log group commit stages and InnoDB redo durability settings. Product controls differ and interact with replication and logging layers. Durable engineering starts from the promise and measured environment rather than copying a vendor knob.

## Prerequisites and Retrieval

Retrieve these concepts:

- a log record occupies a complete published interval with a known end LSN;
- reserved, published, written, and durable frontiers are distinct and ordered;
- WAL-before-data and commit acknowledgement depend on the actual persistence contract;
- condition variables, atomics, mutexes, queues, cancellation, and spurious wakeups have explicit semantics;
- a transaction can be locally durable while its client observes an unknown outcome;
- synchronous replication can add remote receive, flush, replay, or quorum requirements;
- latency percentiles, throughput, queue depth, batch size, and service time require distributions, not averages alone;
- idempotency keys and authoritative transaction lookup handle ambiguous retry outcomes.

DBE-076 completed recovery pass mechanics. This module focuses on commit-path batching; DBE-078 will integrate the complete crash-recovery lifecycle.

## Learning Objectives

After completing this module, you should be able to:

1. derive safe acknowledgement from per-transaction commit LSNs and a durable frontier;
2. design leader/follower, flusher-thread, and epoch-based batching protocols;
3. separate log publication, local write, local flush, remote flush, replay, and client delivery;
4. reason about batch cuts, holes, arrivals during flush, failures, cancellation, and leader handoff;
5. quantify batching's throughput/latency trade-off without promising a universal optimum;
6. design fairness, backpressure, capacity, and overload policy;
7. diagnose ambiguous commit outcomes and safe retries;
8. validate group commit with schedules, crash cuts, storage faults, and frontier oracles.

## Core Exposition

**Derive the shared opportunity.** Suppose transactions require durable endpoints `c_1 <= ... <= c_k`, all within the contiguous published prefix. A flush through `T=c_k` covers every earlier endpoint. If the fixed persistence cost is S and record-copy cost is small, k individual flushes cost roughly kS of serialized service while one group costs roughly S. This is an amortization model, not a latency guarantee: each transaction also pays queueing and optional grouping delay.

**Keep four frontiers distinct.** A concurrent logger may reserve space ahead of records that are not yet complete. The published frontier advances only through a contiguous prefix of finished, checksummed records. The written frontier describes bytes submitted below the log buffer. The durable frontier describes the prefix verified persistent. Safe ordering is

$$
F_{durable} \le F_{written} \le F_{published} \le F_{reserved}.
$$

A group target cannot safely exceed `F_published`. A later transaction may finish inserting before an earlier reservation; that later LSN cannot be acknowledged until the hole is filled or validly cancelled by the logger protocol.

**Bind every waiter to a predicate.** On commit, the transaction publishes its complete commit record, obtains its required end LSN, and checks the durable frontier. If already covered, it can return without another flush. Otherwise it joins a wait structure keyed by that endpoint. On wake, it loops: success only if the current durable frontier covers the endpoint; error only if a recorded terminal condition applies. Notifications can be spurious, coalesced, or intended for another frontier.

**Leader/follower protocol.** The first waiter can become leader, choose a target from the current published requests, release coordination locks, flush through that target, then reacquire/publish the result and notify followers. Requests arriving during I/O either join the next generation or are covered opportunistically if the actual durable frontier reaches them. The batch-generation rule must prevent a follower from being stranded between leader selection and notification.

Never hold a broad transaction-manager lock over storage I/O. Use a small ownership state plus generation counter or a dedicated flusher queue. If the leader thread is cancelled, crashes, or times out, ownership must transfer or a durable error must reach all affected waiters. Cancellation of a client request cannot cancel a shared flush already needed by others.

**Dedicated flusher protocol.** Producers enqueue required endpoints and signal one flusher. The flusher snapshots a batch cut, chooses the greatest eligible endpoint, performs the write/flush, advances the frontier, and wakes covered waiters. This centralizes I/O and failure handling, but the queue and worker become availability-critical. Bound queue memory, define shutdown and fork/process-crash behavior, and ensure producers can detect a dead flusher.

**Choose delay as policy.** Natural batching often arises under load because several commits queue during one flush. An intentional grouping window can increase batch size when arrivals are sparse enough not to queue naturally. If arrival rate is lambda transactions per second and delay is w seconds, the expected additional arrivals under a simple stationary model are approximately `lambda*w`; real arrivals and flush times are bursty, so this is a calibration hint, not a guarantee.

A fixed sleep is usually crude. Cap delay by each request's deadline, skip delay when a flush is already busy or log pressure is high, and treat priority classes explicitly. Measure whether extra delay actually reduces flushes per commit without damaging tail latency. At low load, immediate flush may be best.

**Publish durability with concurrency semantics.** After storage confirms the configured flush, update the durable frontier with release semantics or under the required mutex; waiters load it with matching synchronization before returning. The frontier must be monotone within a log history and wide enough for the LSN. Do not publish before checking the exact syscall/device result. Partial writes, short writes, asynchronous errors, filesystem remounts, and device-cache behavior belong to the storage contract.

**Handle flush failure as state.** A failed or ambiguous flush does not advance the durable frontier. Record the error generation and affected range, wake waiters, and usually transition the database into a controlled failure state because continuing writes can compound uncertainty. A retry is safe only if the logger knows which complete bytes remain and the storage API permits a sound retry. Never return success because “the next flush will probably include it.”

**Distinguish durability policies.** Synchronous local commit waits for local durable log. Asynchronous local commit may return after record publication or write and explicitly permits recent acknowledged loss under crash. Synchronous replication may require local durability plus remote receive, remote flush, replay, or quorum evidence. Grouping can occur at each layer, but one frontier cannot masquerade as another.

A configuration change affects future and in-flight waiters according to a specified linearization point. Do not silently downgrade an existing synchronous waiter because an operator toggled a mode. Record the applied policy with the transaction/result evidence.

**Explain ambiguous client outcomes.** If the server makes commit durable and then the connection fails before the success response arrives, the transaction is committed but the client observes unknown. Re-executing a payment blindly can duplicate it. Use a stable operation key, unique constraint or deduplication record within the transaction, and an authoritative status query. Group commit changes neither this epistemic boundary nor exactly-once external effects.

**Integrate admission and backpressure.** Waiters consume memory, connections, log-buffer slots, and deadlines. Under overload, batch size may grow while tail latency explodes. Bound queues and transaction concurrency, reject before accepting work when possible, and avoid dropping a request after its commit outcome becomes ambiguous. Separate admission failure from commit failure.

**Measure the decomposition.** Record transaction endpoint, enqueue time, leader generation, batch target/size, publication wait, grouping delay, write time, flush time, frontier publication, remote wait, wake time, and response delivery. Aggregate without leaking sensitive transaction identities. Useful ratios include transactions per flush and bytes per flush; distributions include commit latency, flush duration, batch size, and waiters by age.

**Validate schedules and persistent cuts.** A model checker or deterministic scheduler should explore simultaneous arrivals, holes, spurious wakes, leader loss, request cancellation, timeouts, wrap/history changes, and configuration transitions. Fault injection should cut power or process execution before/after record publication, write, flush, frontier store, wake, and response. On restart, compare acknowledged transactions to durable commit records and the recovered database.

The executable model below checks one batch and one late arrival. It assumes published endpoints and a truthful flush result; it does not model threads, syscalls, device persistence, replication, or client networks.

<!-- bijux-verify: {"id":"finite-group-commit-frontier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_frontier=100\nbatch_target=170\nbatch_members=T1,T2,T3\nflush_count=1\nacknowledged=T1,T2,T3\nlate_waiter=T4\nlate_acknowledged=false\nfailed_flush_frontier=100\nfailed_flush_ack_count=0\nall_ack_predicates_hold=true\nevidence=finite_group_commit_frontier\n","stderr":""}} -->
```python
initial_frontier = 100
published = {"T1": 120, "T2": 150, "T3": 170}
batch_target = max(published.values())
durable_frontier = batch_target  # one modeled successful flush
acknowledged = sorted(tx for tx, end in published.items() if end <= durable_frontier)

late = {"T4": 210}  # arrived after the batch cut
failed_flush_frontier = initial_frontier
failed_ack = [tx for tx, end in published.items() if end <= failed_flush_frontier]

print(f"initial_frontier={initial_frontier}")
print(f"batch_target={batch_target}")
print("batch_members=" + ",".join(sorted(published)))
print("flush_count=1")
print("acknowledged=" + ",".join(acknowledged))
print("late_waiter=T4")
print(f"late_acknowledged={str(late['T4'] <= durable_frontier).lower()}")
print(f"failed_flush_frontier={failed_flush_frontier}")
print(f"failed_flush_ack_count={len(failed_ack)}")
print(f"all_ack_predicates_hold={str(all(published[t] <= durable_frontier for t in acknowledged)).lower()}")
print("evidence=finite_group_commit_frontier")
```

## Definitions and Notation

- `c_i`: complete commit-record endpoint required by transaction i.
- `T`: selected batch flush target.
- `F_published`: greatest contiguous endpoint containing complete visible log records.
- `F_written`: greatest contiguous endpoint submitted to the storage layer.
- `F_durable`: greatest contiguous endpoint proven durable.
- **Batch generation:** ownership interval tying a leader, target, result, and waiter set together.
- **Natural batching:** grouping caused by arrivals accumulating during existing work.
- **Intentional delay:** policy-controlled wait to seek more batch members.
- **Spurious wakeup:** return from a wait without establishment of its predicate.
- **Ambiguous outcome:** client cannot determine whether an authoritative commit occurred.
- **Durability class:** named local/remote frontier requirements for acknowledgement.
- **Frontier oracle:** independent mapping of durable log bytes/records to the maximum safely acknowledged endpoint.

## Mechanisms, Invariants, or Proof Structure

**Batch safety.** Assume all endpoints in batch B are complete in the contiguous published prefix and a successful persistence operation proves every byte through `T=max(c_i for i in B)` durable. Then for every member i, `F_durable >= T >= c_i`, so acknowledgement satisfies its predicate. The proof does not apply across holes, different histories, failed flushes, or stronger remote policies.

**No-false-ack invariant.** Every synchronous success event records a prior or synchronized observation of a durable frontier covering its exact commit endpoint. Wake events, leader completion flags, elapsed time, buffer emptiness, or batch membership cannot substitute for that comparison.

**Leader handoff invariant.** At most one owner publishes the result for a generation, while every uncompleted waiter belongs to either the current or a discoverable next generation. Owner failure changes generation state atomically and wakes or transfers followers.

**Monotonicity invariant.** Within one log incarnation, the durable frontier never decreases and never exceeds published complete history. Restart, restore, or promotion creates an explicit new history rather than comparing bare numbers.

**Latency model.** A transaction sees queueing plus optional grouping delay plus residual/own flush plus any remote wait and response delivery. Batching reduces flushes per transaction but can add grouping delay; it does not mathematically guarantee lower latency.

## Alternatives and Trade-Offs

| Design | Advantage | Risk or cost | Evidence needed |
| --- | --- | --- | --- |
| Per-transaction flush | simple mapping | poor amortization | baseline latency/throughput |
| Leader/follower | low extra infrastructure | handoff and cancellation races | schedule exploration |
| Dedicated flusher | centralized batching/errors | worker and queue dependency | failure and overload tests |
| Fixed grouping window | predictable maximum added delay | weak across changing load | percentile comparison |
| Adaptive window | follows observed load | unstable feedback and complexity | transition/control tests |
| Synchronous local | clear local crash promise | local flush latency | power-loss recovery |
| Asynchronous local | low acknowledgement latency | acknowledged-loss window | explicit product contract |
| Remote-flush quorum | broader failure tolerance | network/quorum tail | failure-domain evidence |

## Failure Modes and Misconceptions

1. **“One write covers one transaction.”** Durability requires the configured flush boundary, not buffer copying.
2. **“The largest reserved LSN is a valid target.”** Publication holes can make the prefix incomplete.
3. **“Every notified waiter can return.”** Each waiter rechecks its own endpoint predicate.
4. **“Sleep creates correctness.”** Ordering and frontiers do; delay only influences batch formation.
5. **“A larger batch always wins.”** It may increase queueing, tail latency, and unfairness.
6. **“Leader timeout cancels the flush.”** Other followers may still require it; ownership is shared state.
7. **“A failed flush probably persisted.”** Unverified bytes cannot advance the durable frontier.
8. **“Async commit is group commit.”** It weakens the acknowledgement contract; grouping need not.
9. **“Local flush means replicated durability.”** Remote receive, flush, replay, and quorum are separate.
10. **“A durable commit means the client knows.”** Response loss creates an unknown outcome.
11. **“Retrying an unknown commit is harmless.”** Stable operation identity and status lookup are required.
12. **“Average latency shows success.”** Tail, overload, sparse load, and error paths matter.
13. **“One mutex around fsync is sufficient.”** It may serialize unrelated work and complicate cancellation.
14. **“Frontiers are plain integers.”** History, endpoint convention, width, and memory synchronization matter.
15. **“Flush errors affect one transaction.”** Shared log uncertainty can require a database-wide controlled failure.
16. **“Benchmark success proves storage truth.”** Power-loss and platform-specific persistence evidence remain necessary.

## Worked Examples

### Example 1

**Situation.** Waiters require 120, 150, and 170; durable frontier is 100.

**Reasoning.** All records are in the published prefix. A leader flushes through target 170 once. After verified persistence it publishes frontier 170. Each endpoint is at most 170, so all three predicates hold. Three individual flushes were unnecessary.

**Conclusion.** One truthful contiguous flush can safely acknowledge every covered synchronous waiter.

### Example 2

**Situation.** Records ending 120 and 170 are complete, but an earlier reservation ending 150 is unfinished.

**Reasoning.** The contiguous published frontier cannot leap from 120 to 170. Choosing target 170 would expose a malformed prefix or let recovery encounter a hole. The batch can flush/acknowledge through 120; the 170 waiter remains until the 150 range is completed or validly resolved.

**Conclusion.** Completion of a later record does not make a noncontiguous prefix publishable or durable.

### Example 3

**Situation.** A follower receives a condition-variable notification while frontier remains below its commit LSN.

**Reasoning.** Notifications may be spurious or cover an earlier waiter. The follower reacquires synchronization and loops on `frontier >= required` or a terminal error. Returning because it woke would confuse scheduling with evidence.

**Conclusion.** The durable-frontier predicate, not wakeup, authorizes success.

### Example 4

**Situation.** A leader is cancelled after issuing a shared flush but before publishing its result.

**Reasoning.** Cancellation cannot abandon followers. A protected generation records ownership and in-flight target. Another coordinator joins/completes the operation or retries only under the storage protocol, then publishes one verified result. The cancelled client may still have an ambiguous committed outcome.

**Conclusion.** Leader lifetime and batch durability are decoupled through recoverable ownership state.

### Example 5

**Situation.** The flush syscall returns an I/O error after some device-cache activity.

**Reasoning.** The system lacks evidence that the required prefix is durable. It leaves the frontier unchanged, records the error, wakes waiters with failure/unknown according to the API, and normally prevents unsafe continued commits. Guessing that bytes “probably landed” violates the contract.

**Conclusion.** Partial or ambiguous persistence never advances a synchronous durable frontier.

### Example 6

**Situation.** Arrival rate is 4,000 commits/s and an intentional window is 250 microseconds.

**Reasoning.** Under a simple stationary model, expected additional arrivals are `4000 * 0.00025 = 1`. Bursts, deadlines, and ongoing flushes can change the actual batch. Measure the distribution; do not claim every batch gains one member or that latency improves.

**Conclusion.** Arrival-rate arithmetic calibrates a window but does not replace workload measurement.

### Example 7

**Situation.** T1 requires local durable flush; T2 requires local plus remote quorum flush.

**Reasoning.** One local group flush can satisfy T1 and the local component of T2. T2 must remain waiting until the required remote frontier/quorum covers its endpoint. Waking both on local completion silently weakens T2's policy.

**Conclusion.** Batch membership may be shared while acknowledgement remains durability-class specific.

### Example 8

**Situation.** A payment commit becomes durable, but the connection drops before success reaches the client.

**Reasoning.** Server recovery finds a winner; client knowledge is unknown. The client queries by stable payment operation ID. A unique transactional record returns the existing outcome instead of executing a second debit. Transport retry alone cannot create exactly-once semantics.

**Conclusion.** Group commit preserves the database outcome but cannot remove response ambiguity.

### Example 9

**Situation.** At low load, a policy waits for at least eight transactions before flushing.

**Reasoning.** If only one transaction arrives, it can wait forever. Add a maximum deadline, flush immediately when the oldest request reaches it, and permit natural batches smaller than eight. Priority classes need explicit maximum delay so bulk traffic cannot starve interactive commits.

**Conclusion.** Minimum batch size without a time/progress bound violates liveness.

### Example 10

**Situation.** Throughput rises 40%, but p99 commit latency triples after batching is enabled.

**Reasoning.** Decompose enqueue wait, grouping delay, flush, remote wait, and response delivery by batch generation and load. Large queues or a fixed delay may explain the tail; storage flush distribution or lock contention may also. Compare sparse, steady, burst, and overload workloads and enforce SLO-based caps.

**Conclusion.** Higher throughput is not sufficient evidence; batching policy must satisfy the declared latency envelope.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** leader election, condition predicates, generations, cancellation, and memory ordering determine safety.
- **Operating Systems:** write, fsync, barriers, device caches, scheduling, and I/O errors define the persistence boundary.
- **Distributed Systems:** quorum acknowledgement and replicated-log frontiers extend grouping across failure domains.
- **API and Service Engineering:** timeouts, idempotency keys, retries, and status lookup handle ambiguous outcomes.
- **Platform Engineering:** storage qualification, telemetry, overload control, canarying, and incident response make the policy operable.
- **Software Testing and Quality Engineering:** deterministic scheduling, model checking, crash injection, and frontier oracles test rare races.
- **Security Engineering:** queue exhaustion, forged metrics, log integrity, and operation-identity abuse belong in the threat model.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems* 17(1), 1992. Primary WAL, commit record, and recovery foundation; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
2. Hector Garcia-Molina and Kenneth Salem, “Sagas,” *ACM SIGMOD*, 1987. Primary transaction-compensation context distinguishing local commit from broader workflows.
3. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Commit, logging, group commit, recovery, and transaction-processing performance foundations.
4. Philip A. Bernstein and Eric Newcomer, *Principles of Transaction Processing*, 2nd ed., Morgan Kaufmann, 2009. Commit protocols, recovery, and distributed durability context.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Write Ahead Log Settings](https://www.postgresql.org/docs/18/runtime-config-wal.html), reviewed 2026-09-05. Official current `synchronous_commit`, `commit_delay`, `commit_siblings`, WAL synchronization, and durability behavior.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/18/wal-reliability.html), reviewed 2026-09-05. Official persistence and storage-cache assumptions.
7. Oracle, [MySQL 8.4 Reference Manual: Binary Log Group Commit](https://dev.mysql.com/doc/refman/8.4/en/binary-log.html), reviewed 2026-09-05. Official current group-commit staging and configuration context.
8. Oracle, [MySQL 8.4 Reference Manual: InnoDB Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html), reviewed 2026-09-05. Official current redo durability and capacity context.
9. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), reviewed 2026-09-05. Official storage flush and commit-boundary analysis for contrast.

## Exercises

### Exercise 1

Define reserved, published, written, and durable log frontiers. State the safe ordering and the exact synchronous acknowledgement predicate.

### Exercise 2

With frontier 80, published waiters `{A:100,B:140,C:160}`, a hole covering 121–130, and late waiter `{D:190}`, derive the first safe target and acknowledgements before and after the hole is completed.

### Exercise 3

Design a leader/follower group-commit state machine covering spurious wakes, arrivals during flush, leader cancellation, timeout, I/O failure, shutdown, and history change.

### Exercise 4

Compare immediate, fixed-window, adaptive-window, and dedicated-flusher policies for sparse, steady, burst, and overload workloads. Define selection evidence.

### Exercise 5

Design an unfamiliar multi-region payment service's commit contract and validation campaign, including local/remote frontiers, batching, unknown outcomes, fault injection, capacity, security, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Reserved is space allocated to producers and may contain holes. Published is the greatest contiguous prefix of complete, integrity-finalized records. Written is the greatest contiguous prefix submitted below the log buffer. Durable is the greatest contiguous prefix proven persistent under the storage contract. The safe relation is `durable <= written <= published <= reserved`. A synchronous transaction with complete commit endpoint c returns success only after observing a compatible durable frontier F with `F >= c`; notification, elapsed time, or membership is insufficient.

### Answer 2

The hole prevents the contiguous published frontier from passing 120 even though B and C may have finished later ranges. The first safe target is 120 or the last complete boundary before the hole; only A at 100 is acknowledged by a successful flush through that target. After 121–130 is completed and all intervening records through 160 are published, one flush through 160 can acknowledge B and C (and A if still waiting). D arrived after the batch cut and requires a later flush through at least 190. Full credit requires explicit record-boundary and same-history assumptions.

### Answer 3

Use states idle, collecting generation g, flushing(g,target), and failed/stopping, protected by a narrow mutex plus a monotone generation. A waiter publishes its record, enqueues `(endpoint,deadline,class)`, then loops on frontier coverage or terminal error. One leader snapshots only contiguous published endpoints, marks flushing, releases the lock for I/O, then publishes either the verified frontier or error under the lock and broadcasts. New arrivals remain discoverable for g or g+1 by a precise cut rule. Cancellation removes only an uncommitted request; it does not abandon shared I/O. Leader loss permits atomic ownership transfer. Timeout changes the caller observation, not an already authoritative commit. I/O failure leaves frontier unchanged; shutdown drains or rejects before acceptance; history change invalidates bare endpoint comparison and rebinds/fails waiters.

### Answer 4

Immediate flush minimizes intentional delay and suits sparse/deadline-sensitive work but wastes amortization. A fixed window is simple and bounded but mismatches changing rate. Adaptive delay can exploit load and storage observations but needs stable control, caps, and explainability. A dedicated flusher centralizes grouping and errors but adds queue/worker dependency. Evaluate commit-latency and flush distributions, transactions/bytes per flush, queue age/depth, sparse/burst/overload behavior, CPU/lock cost, error recovery, deadline misses, fairness, and storage endurance in the actual durability class. Select against SLO and capacity margins, not mean throughput alone.

### Answer 5

Name local published/written/durable and each replica receive/flush/replay frontier, then define acknowledgement as local durable plus a fenced quorum of remote durable endpoints in the same term/history. Batch compatible endpoints at local and remote layers while preserving per-payment requirements. Store a stable payment operation ID and authoritative outcome transactionally; after response loss, query rather than re-execute. Inject process, network, region, leader, quorum, storage-full, short-write, fsync-error, reorder, timeout, and response-loss faults at every frontier transition. Verify every acknowledged payment after recovery/failover and ensure no duplicate operation ID. Bound queues/WAL/reserves, protect identifiers/logs, expose delay/flush/quorum components, batch generations and ambiguity. Canary with reversible compatible configuration/builds; roll back batching without weakening already accepted waiters, and fail closed or reconcile if frontier evidence diverges.
