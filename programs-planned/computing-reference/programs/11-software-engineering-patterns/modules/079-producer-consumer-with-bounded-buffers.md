---
module_id: SEPAT-079
program: Software Engineering: Patterns
level: 2
module_number: 79
title: Producer-Consumer with Bounded Buffers
status: complete
last_verified: 2026-08-29
---

# Producer-Consumer with Bounded Buffers

## One-Page Review

### Governing question

How can producers and consumers exchange owned items at different rates through finite storage while preserving no-loss/no-duplication semantics, memory visibility, ordering, backpressure, fairness, cancellation, drain/close behavior, and stable end-to-end capacity?

### Essential definitions

- A **producer** creates items and attempts to transfer ownership into a buffer.
- A **consumer** claims an available item, processes it, and owns its terminal result/release.
- A **bounded buffer** has finite slot and byte capacity, making overload an explicit wait, rejection, drop/coalesce, or upstream-demand decision.
- **enqueue linearization** is the instant an accepted item becomes buffer-owned and visible in queue order; **dequeue linearization** transfers it to one consumer.
- **backpressure** prevents production from outrunning finite consumption/resources; it may block allowed producer threads or use a nonblocking control channel.
- **work sharing** gives each item to one consumer; **broadcast/fan-out** requires independent per-consumer delivery/acknowledgement and is not an ordinary queue.
- **high/low watermarks** avoid rapidly toggling upstream admission around full capacity.
- A **poison pill/sentinel** is an in-band item interpreted as termination; it is hazardous with multiple producers/consumers and data-domain collisions.
- A **ring buffer** reuses a fixed array with monotonically advancing sequences or wrapped indices.
- **drain** stops new production while consumers process accepted items; **abort** terminally classifies queued/in-flight items under explicit policy.

### Central model, mechanism, or theorem

For capacity (K), FIFO ring state can satisfy

\[
0\le count\le K,\qquad tail-head=count
\]

when head/tail are logical monotonic sequences (or equivalent modulo invariants). Each successful enqueue consumes one free-slot permit and publishes exactly one owned item; each successful dequeue consumes one item permit and returns one slot. In a correct work-sharing queue,

\[
accepted = queued + in\_flight + terminal
\]

for a defined audit boundary, with disjoint item identities.

If accepted arrival rate is λ and aggregate sustainable consumer rate is μₜ, long-run stability requires λ < μₜ. Little's Law (L=\lambda W) checks stable averages. A finite (K) bounds queue entries but cannot make sustained overload disappear; it forces a full-buffer policy and bounds only declared payload memory (Kb_{max}), not producers, consumers, results or hidden downstream queues.

### Critical invariants

- Exactly one enqueue outcome wins: rejection retains producer ownership; acceptance transfers one immutable/exclusive item identity to the buffer.
- Queue count and owned bytes never exceed configured bounds; slot/item permits or sequence arithmetic remain conserved.
- Every accepted work-sharing item is claimed by at most one consumer and reaches one terminal/requeue/dead-letter classification.
- Producer writes happen-before consumer access under the exact queue/memory protocol; a slot is published only after initialization and reused only after all required consumers release it.
- FIFO/priority/partition ordering is precisely stated; concurrent completion order is not inferred from dequeue order.
- Blocking put is used only where blocking the producer is safe; event/UI/reactive producers use nonblocking demand/rejection/pause.
- Per-producer/tenant fairness and quotas prevent monopolization; priority cannot starve prerequisite or ordinary work indefinitely without policy.
- Cancellation, expiry, consumer failure, retry/requeue and poison/close cannot duplicate or silently lose effect identities.
- Close is out-of-band protected lifecycle state or a rigorously designed sentinel protocol; all producer/consumer waiters become terminal.
- Shutdown stops admission, drains/aborts, reaps in-flight outcomes, releases every item/slot, joins participants, then destroys storage/synchronization.

### Common failures

Common failures include calling an unbounded queue “backpressure,” bounding count but not payload bytes, blocking an event-loop producer, publishing a ring slot before initialization, overwriting before the slowest consumer advances, using non-atomic check-then-enqueue, duplicating work after consumer crash, retrying ambiguous effects with a new ID, assuming FIFO completion, one producer monopolizing slots, strict-priority starvation, batch consumers holding slots too long, poison pill consumed by only one of many consumers, producers adding work after the pill, data colliding with sentinel, close without waking full/empty waiters, and measuring queue depth while upstream/downstream buffers grow.

### Compact example

A capacity-three FIFO accepts `p1:a`, `p2:b`, and `p1:c`. `p2:d` is rejected while full and producer retains it. A consumer takes `a`, releasing one slot; `p2` retries the same item identity `d` and succeeds. Close stops new production but preserves drain. Consumers receive `b,c,d` exactly once, then end-of-stream. Accepted order and consumed order match, occupancy stays in `[0,3]`, and rejection never transferred ownership.

### Connections

[SEPAT-073](073-half-sync-half-async.md) uses a bounded queue between concurrency models; [SEPAT-075](075-thread-pool.md) schedules queued tasks; [SEPAT-077](077-monitor-object.md) supplies one blocking implementation. [SEPAT-080](../ROADMAP.md) selects among these patterns. Producer-Consumer also connects to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Data Engineering](../../19-data-engineering/ROADMAP.md), [Operating Systems](../../22-operating-systems/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When production and consumption are concurrent and temporarily mismatched, how should a finite buffer absorb bounded bursts and communicate pressure without losing ownership, correctness, ordering, fairness, or termination?

Producer-Consumer separates the pace and execution context of item creation from processing. A bounded buffer makes that decoupling finite. This is not just a data structure: it is a capacity, memory, latency, admission and lifecycle contract. The buffer can be implemented with monitors/semaphores, channels, blocking queues, lock-free rings or reactive demand, but the semantic obligations remain.

## Why This Matters

I/O pipelines, thread pools, log processors, telemetry, media, ETL, device drivers, schedulers and message brokers all use buffers between stages. Bounded buffers smooth short bursts and limit retained state while allowing producers/consumers to run efficiently.

Under sustained overload, the buffer fills. The next decision—block, pause, reject, shed, coalesce, spill durably or fail—is a system/API decision. Hiding it behind an unbounded queue eventually produces extreme latency, memory failure and stale work. Correct bounded design makes the pressure visible early and aligns it with item semantics.

## Prerequisites and Retrieval

You should understand queues/rings, threads, mutexes/conditions/semaphores, memory visibility, ownership, deadlines, idempotency, Little's Law and backpressure. Retrieve these facts:

1. A count bound does not bound bytes if item sizes/graphs are unbounded.
2. Blocking a producer communicates pressure only if that producer/thread can safely block.
3. Queue publication must order item initialization before consumer visibility.
4. Multiple consumers make dequeue order distinct from completion/effect order.
5. A consumer crash after effect but before acknowledgement creates ambiguity.
6. Work sharing and broadcast require different data structures/accounting.
7. Queue close is not intrinsic to every API; sentinel schemes have topology constraints.
8. A bounded stage cannot stabilize a pipeline whose accepted long-run input exceeds its bottleneck.

## Learning Objectives

After completing this module, you should be able to:

- identify producers, consumers, buffer, admission, slot/item synchronization, ownership and terminal accounting;
- state ring/FIFO invariants and enqueue/dequeue linearization points for SPSC and MPMC contexts;
- design count, byte, tenant, deadline, in-flight and downstream bounds as one capacity system;
- choose blocking, timed, nonblocking, watermark, explicit-demand, rejection, coalescing or durable spill policies;
- distinguish work-sharing, broadcast, partitioned ordering and completion semantics;
- reason about memory publication, preallocated slot reuse, sequence wrap, false sharing and wait strategies;
- design fairness, priority, batching, retry/requeue, poison/close and shutdown without loss/duplication;
- apply Little's Law and service constraints without treating averages as tail/correctness proofs;
- compare monitor/semaphore, concurrent queue, channel, reactive stream and ring-buffer implementations;
- verify finite models, real concurrency, saturation, crash ambiguity, memory ordering and recovery.

## Core Exposition

### Define the topology and delivery semantics

List producers and consumers, their threads/processes, item identity/schema/maximum bytes, and whether one or every consumer must see each item. A common MPMC queue is work sharing: one dequeue transfers an item to one consumer. If audit and indexing both need every event, use two subscriber positions/queues or a broadcast log—not two consumers racing one queue.

Define ordering: global FIFO by enqueue linearization, per-producer FIFO, partition-key order, priority, or none. MPMC global FIFO can serialize a hot point. Partitioning scales while preserving key order, but skew causes imbalance. Completion order across consumers is normally unconstrained.

### Make acceptance an ownership boundary

The producer builds a complete immutable item or obtains an exclusive lease, then attempts enqueue. Successful linearization transfers ownership. Failed/timed/cancelled enqueue retains producer ownership and must release/retry under policy. Do not mutate accepted payload or recycle its buffer.

Each item carries stable item/effect identity, producer/tenant/partition, sequence/schema, accepted/deadline time, authority/classification, payload lease and trace. A consumer claims once, validates current relevance/authority, performs bounded work and terminally acknowledges/requeues/dead-letters/reconciles.

In-process queue acceptance is not durable. A crash can lose queued items. If callers receive durable acceptance, write to a durable log/outbox before acknowledgement and use stable consumer effect identities.

### Bound slots and bytes

Capacity (K) bounds entries, not size. Enforce (b_i\le b_{max}), aggregate queued bytes (B_q\le B_{max}), in-flight bytes, per-tenant/partition shares, result/output and downstream work. Large-item classes may need separate queues/permits.

For fixed preallocated ring entries, storage is predictable but referenced external payload still counts. Clearing slots after consume may be needed to release references/sensitive data. Reuse only after every required consumer sequence passed; work-sharing one-consumer release differs from multicast slowest-consumer gating.

Capacity follows memory and useful-wait budgets. A 10-second queue for 100 ms-deadline requests is not useful burst absorption. Reserve operational headroom and test allocator/runtime overhead.

### Implement monitor/semaphore conservation

A monitor buffer protects array/deque, count/head/tail/closed and uses `not_empty`/`not_full` predicate loops. Enqueue waits while full/open, writes, increments, signals items. Dequeue waits while empty/open, reads/clears, decrements, signals slots. Close broadcasts.

A semaphore design initializes `slots=K`, `items=0`, plus a mutex for indices. Producer obtains a slot, writes under appropriate exclusion, publishes, then increments items. Consumer obtains an item, reads/claims, then returns a slot. Exception/cancellation between permit and publication must restore permits exactly once. The conservation relationship is not automatic if cleanup paths omit one step.

Avoid checking `remainingCapacity` then enqueueing: another producer can win. Use the atomic queue operation's return.

### Publish ring entries correctly

In a ring, producer claims sequence/slot, initializes all fields, then publishes availability with release semantics. Consumer observes published sequence with acquire semantics before reading. Consumer advances its gating sequence only after finished reading/releasing. Producer cannot wrap and overwrite a slot until relevant consumer sequences make it free.

SPSC algorithms exploit one writer per head/tail and are simpler than MPMC. Multiple producers need safe claim/publication, including holes when sequence N+1 finishes before N. Multiple consumers need exclusive work claims or independent broadcast cursors. Never transplant an SPSC algorithm into MPMC.

Sequence wrap/ABA and integer overflow require proof. Cache-line placement can reduce false sharing between hot producer/consumer counters but is hardware/runtime-specific. Busy spin lowers wake latency under continuous load while burning CPU; blocking/parking saves CPU with wake costs. Hybrid wait strategies need measurement.

### Define full-buffer behavior

Blocking `put` is appropriate for a dedicated bounded producer that may safely stop. Timed put constrains producer wait but needs one monotonic deadline. Nonblocking `offer` lets event/UI threads pause input, return overload or schedule later without freezing unrelated work.

High/low watermarks pause upstream at high occupancy and resume at lower occupancy to prevent oscillation. Explicit demand (reactive pull tokens/credits) prevents producers from emitting more than downstream requested capacity across a nonblocking boundary. Credits require overflow-safe accounting and terminal protocol.

Drop-new, drop-oldest, sample or coalesce only when item semantics permit loss. State snapshots may coalesce by key; commands/payments generally may not. Record dropped identities/counts/reasons, avoid cross-tenant replacement and maintain sequence/gap semantics.

Durable spill is a different storage/failure contract, not an unlimited escape. Bound disk/broker use and define replay/order/idempotency.

### Prevent unfair monopolization

One producer can fill all slots. Apply per-producer/tenant quotas, weighted fair admission, reserved critical capacity, partition queues or tickets. A consumer can similarly monopolize dequeue, though work completion may remain balanced by service time.

Strict priority can starve old ordinary items and let deadlines expire. Aging/weighted scheduling or separate pools helps. Priority queues often do not provide intrinsic finite capacity; wrap with permits/admission.

Fair synchronization may reduce throughput and still not guarantee end-to-end fairness if tasks differ. Measure accepted/rejected/wait/service by class/tenant.

### Batch carefully

Producers can claim/write batches and consumers drain batches to amortize locks/wakeups/cache transitions. Limit batch count/bytes/time. A large producer batch monopolizes slots; a consumer holding a batch delays slot return and cancellation, increasing tail latency.

Bulk queue APIs may not be atomic: partial enqueue/drain on exception can violate assumptions. Document all-or-nothing versus prefix acceptance and return exact accepted identities. Process batches under per-item terminal accounting when effects matter.

### Handle consumer failure and retry

An in-memory dequeue often removes before processing. If the consumer crashes, the item is lost unless an in-flight ledger/requeue owner exists. Alternatively peek/claim/ack retains it until ack, requiring visibility timeout/lease and duplicate handling.

If effect succeeds then consumer crashes before ack, re-delivery duplicates. Use stable effect identity, idempotent/conditional operations and reconciliation. Retry count/deadline/budget are bounded; poison items go to a governed dead-letter/quarantine path rather than cycling forever.

In-process threads may catch failures and complete item terminally, but process crash still erases volatile state. Align advertised guarantee with actual durability.

### Carry deadlines through the queue

Record acceptance time and monotonic deadline. Queue age consumes the budget. Before expensive consume, classify expired work and release/record it. For commands with possible effects, expiry may mean do-not-start; once started, actual result still needs reconciliation.

Earliest-deadline scheduling can reduce missed deadlines but sacrifices FIFO and can starve long-deadline work; it needs overload feasibility/admission. Dropping expired items does not restore health if input remains above capacity.

### Close without sentinel traps

Best is protected out-of-band state: close rejects producers; consumers drain queued items then receive end-of-stream; all full/empty waiters wake and inspect closed. Close is idempotent and generation-fenced.

Poison pills are in-band. With N consumers, one pill may stop only one; N pills may be consumed before late real items if producers remain; a consumer can crash holding a pill; priority can reorder; payload can collide; broadcast topology multiplies requirements. If used, stop/join producers first, reserve capacity, use an unforgeable control type, define one-per-consumer propagation and test every topology race.

Abort differs from drain. It terminally classifies/disposes queued items and cooperatively cancels/reconciles in-flight effects. Every lease/permit is returned exactly once.

### Analyze whole-pipeline stability

For stages, throughput is limited by the slowest sustainable consumer/downstream. If accepted λ exceeds μₜ, a finite buffer reaches full; the full policy is normal operation. Larger K delays pressure and increases memory/latency but not sustainable throughput.

Little's Law checks stable measured (L=\lambda W). Use distributions for bursts/tails. Correlated downstream outages invalidate stationary assumptions. Backpressure must propagate to the original admission point; otherwise hidden buffers accumulate upstream.

Observe every queue, kernel/socket/broker/client buffer and in-flight stage. Local low depth can coexist with downstream connection-pool saturation or upstream memory.

### Secure the buffer

Untrusted producers can fill capacity, submit maximal payloads, expensive items or high priority. Authenticate before costly acceptance, authorize operations, enforce tenant quotas/rate/bytes/deadlines and validate schemas. Do not let priority claims bypass policy.

Items/freed slots can retain secrets. Clear/preinitialize safely before cross-tenant reuse, protect traces/dead-letter content, and revalidate authority before delayed effect/delivery. Queue timing/depth may leak workload; limit observability access.

### Shut down and verify

Stop or fence producers, close admission, wake blocked producers/consumers, drain or abort by policy, stop retries, reap in-flight results/effects, release buffers/permits, join participants, verify conservation/accounting, then destroy storage/synchronization. A consumer cannot terminate merely because queue is momentarily empty.

Model identities and count conservation. Test empty/full, simultaneous enqueues/dequeues, wrap, producer failure between claim/publish, consumer failure before/after effect/ack, spurious wakes, cancellation, fairness, large items, batches, overload, downstream stall, priority, close with all waiter roles, poison races, drain/abort, process crash and restart. Use race/memory tools and target architecture/runtime tests for lock-free rings.

### A finite executable model

This deterministic FIFO demonstrates capacity, rejection ownership, slot reuse, close/drain and conservation. It does not execute threads, synchronization, memory ordering, blocking, retries, effects or crash recovery.

<!-- bijux-verify: {"id":"sepat-079-bounded-fifo","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"produce=p1:a,p2:b,p1:c accepted=3 count=3\nproduce=p2:d status=rejected owner=p2 count=3\nconsume=a count=2\nproduce=p2:d status=accepted count=3\nclose=true producers=stopped\nconsume=b,c,d count=0\nconsume=none status=end_of_stream\ninvariants=bounded:true fifo:true accepted:4 consumed:4\n","stderr":""}} -->
```python
class BoundedFifo:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.closed = False
        self.accepted = []
        self.consumed = []

    def produce(self, producer, item):
        if self.closed or len(self.items) >= self.capacity:
            return "rejected"
        record = (producer, item)
        self.items.append(record)
        self.accepted.append(item)
        return "accepted"

    def consume(self):
        if self.items:
            _, item = self.items.pop(0)
            self.consumed.append(item)
            return item, "ok"
        if self.closed:
            return None, "end_of_stream"
        return None, "would_wait"

    def close(self):
        self.closed = True


queue = BoundedFifo(capacity=3)
for producer, item in (("p1", "a"), ("p2", "b"), ("p1", "c")):
    queue.produce(producer, item)
print(f"produce=p1:a,p2:b,p1:c accepted={len(queue.accepted)} count={len(queue.items)}")

status = queue.produce("p2", "d")
print(f"produce=p2:d status={status} owner=p2 count={len(queue.items)}")
item, _ = queue.consume()
print(f"consume={item} count={len(queue.items)}")
status = queue.produce("p2", "d")
print(f"produce=p2:d status={status} count={len(queue.items)}")

queue.close()
print("close=true producers=stopped")
drained = []
while queue.items:
    item, _ = queue.consume()
    drained.append(item)
print(f"consume={','.join(drained)} count={len(queue.items)}")
item, status = queue.consume()
print(f"consume=none status={status}")

bounded = str(len(queue.items) <= queue.capacity).lower()
fifo = str(queue.accepted == queue.consumed).lower()
print(f"invariants=bounded:{bounded} fifo:{fifo} accepted:{len(queue.accepted)} consumed:{len(queue.consumed)}")
```

## Definitions and Notation

Let (K) be slot capacity, (B_{max}) queued-byte capacity, (b_i) item bytes, (h,t) logical dequeue/enqueue sequences, (count=t-h), λ effective accepted production rate, μₜ aggregate sustainable consume rate, and (W_q) queue residence.

Let item lifecycle be `created -> rejected | accepted -> queued -> claimed -> terminal/requeued/quarantined`. Let (A,Q,F,T) be accepted, queued, in-flight and terminal identity sets at an audit instant. Conservation requires (A=Q\uplus F\uplus T) under a defined recovery boundary.

For broadcast consumer j has sequence (c_j); producer wrap is safe only below (min_j c_j+K). For work sharing one claim sequence assigns each item to one consumer. Close generation (g) fences late producers/consumers.

## Mechanisms, Invariants, or Proof Structure

### Count/permit conservation

Assume capacity K, atomic slot acquisition before accepted publish, atomic item acquisition before dequeue, and every failure path restores the acquired permit exactly once. Then `free_slots + queued_items = K` for queue storage and (0\le count\le K). In-flight consumer work is outside slots if dequeue frees immediately and needs its own bound.

### Ownership/no-duplication argument

Assume enqueue success linearizes one unique identity and transfers ownership; dequeue claim linearizes once and excludes other work-sharing consumers; terminal/requeue transition is serialized under the same identity. Then no accepted identity is concurrently owned by two queue/consumer states in the modeled process. Crash/effect-before-ack requires durable lease/idempotency evidence beyond it.

### Publication argument

Assume producer fully initializes a claimed slot, publishes its sequence with release semantics, consumer observes availability with acquire semantics, and producer cannot reuse until consumer release. Consumer sees initialized data and no overwrite in the stated topology. Exact SPSC/MPMC algorithm and memory model must prove these assumptions.

### Stability limit

If long-run accepted λ exceeds sustainable μₜ, backlog has positive drift and any finite K eventually reaches full under continued operation. Capacity changes time-to-full, not throughput. Stationary average equations do not predict correlated outages or tails.

### Evidence boundaries

Finite models check count, order, ownership and close. Race/memory tests sample implementation schedules. Mathematical accounting checks capacity. Performance, fairness, backpressure effectiveness, durability and external-effect claims require system evidence.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Appropriate use |
| --- | --- | --- | --- |
| Monitor bounded FIFO | Clear predicates/close and portable reasoning | Lock contention/context switches | General MPMC moderate load |
| Semaphore ring | Explicit slot/item conservation | Exception/permit cleanup complexity | Fixed storage and clear topology |
| Concurrent BlockingQueue | Proven library semantics/options | Defaults/close/fairness vary | Standard in-process work sharing |
| SPSC lock-free ring | Low overhead/simple ownership | Only one producer/consumer topology | Dedicated pipeline stages |
| MPMC lock-free queue/ring | Scales contention when proven | Complex memory/reclamation/sequence proof | Measured hot path with expert support |
| Reactive demand | Nonblocking backpressure across async stages | Protocol/subscription complexity | Async streaming/event loops |
| Broadcast log/ring | Every subscriber can observe | Slowest consumer gates retention or misses by policy | Fan-out/event processing |
| Durable broker | Crash persistence and distributed consumers | Delivery duplicates, latency, operations | Durable cross-process pipeline |
| Rendezvous/direct handoff | No queue latency/storage | Producer/consumer must overlap; low burst absorption | Tight synchronous backpressure |

Preallocation reduces allocation variance but retains fixed memory. Busy spinning reduces wake latency but burns CPU. Batches increase throughput but hurt fairness/tails. Partitioning scales but creates skew and rebalancing semantics.

## Failure Modes and Misconceptions

- **“Bounded queue guarantees bounded system.”** Producers, in-flight work, outputs and downstream queues also need bounds.
- **“Capacity in items bounds memory.”** Item/object graphs need byte limits.
- **“Blocking put is always backpressure.”** On event/UI threads it blocks unrelated progress.
- **“Remaining capacity reserves a slot.”** Only atomic enqueue/permit acquisition does.
- **“Thread-safe queue makes payload safe.”** Continued mutation still races.
- **“FIFO queue means FIFO effects.”** Multiple consumers complete out of order.
- **“Two consumers provide broadcast.”** They split work; they do not each receive every item.
- **“Lock-free means wait-free and correct.”** Progress classes differ and memory/reclamation proof is hard.
- **“A ring cannot overflow.”** Sequence wrap/overwrite can corrupt slow consumers.
- **“Poison pill closes the queue.”** It is one item with topology/order/failure hazards.
- **“Empty means finished.”** Producers may still add unless closed/joined.
- **“Requeue is harmless.”** It can duplicate an already-applied effect.
- **“Bigger buffer raises throughput.”** It only absorbs longer bursts before pressure.
- **“Drop-oldest is neutral.”** It changes ordering/effect and may discard the closest-to-service item.
- **“Batch drain is atomic.”** Library bulk semantics may be partial.
- **“Low local depth means healthy pipeline.”** Hidden upstream/downstream buffers may be saturated.

## Worked Examples

### Example 1

**Situation.** An event loop uses blocking `put` into a full worker queue.

**Reasoning.** The loop stops serving every connection and may deadlock if workers need loop-driven results. Use nonblocking offer, pause read readiness at a high watermark, return overload or propagate explicit demand; resume below a low watermark.

**Conclusion.** Backpressure must respect producer execution context.

### Example 2

**Situation.** Queue capacity is 1,000, but items can retain 50 MiB buffers.

**Reasoning.** Count bound allows catastrophic memory. Enforce item and aggregate byte permits, lease/copy ownership, separate large classes, and include in-flight/results/allocator overhead. Reject before transfer when byte capacity is unavailable.

**Conclusion.** Production buffers need multidimensional capacity.

### Example 3

**Situation.** Two consumers dequeue FIFO items 1 and 2; item 2 finishes first.

**Reasoning.** Dequeue order is FIFO, completion is concurrent. If effects require key order, partition/serialize by key or use sequence/version conditional apply and bounded reorder. Do not globally serialize unrelated keys without need.

**Conclusion.** Queue order and effect order are different contracts.

### Example 4

**Situation.** A consumer writes a payment, crashes before acknowledgement, and the item is requeued.

**Reasoning.** The queue cannot know whether effect occurred. Reuse stable effect/idempotency ID, query/conditionally apply, reconcile then ack; bound retry/dead-letter policy. At-most-one dequeue is insufficient across crash.

**Conclusion.** Delivery and external-effect guarantees require separate protocols.

### Example 5

**Situation.** One producer fills every global slot with bulk work while urgent producers reject.

**Reasoning.** Add per-tenant/class quotas, reserved urgent capacity and weighted/aged admission. Ensure urgent work does not depend on starved bulk prerequisites. Test sustained adversarial mixes.

**Conclusion.** Global boundedness does not imply fair access.

### Example 6

**Situation.** An MPMC ring publishes sequence before the producer finishes writing payload.

**Reasoning.** A consumer observes availability and reads partial/stale data. Initialize first; publish with release; observe with acquire; never reuse before the consumer gating sequence. Use a proven implementation for target memory model.

**Conclusion.** Slot publication is a memory-order linearization boundary.

### Example 7

**Situation.** One poison pill is added for four consumers.

**Reasoning.** One exits and three may wait forever. Four pills still race with late producers/reordering/crash. Prefer out-of-band close+broadcast+drain. If sentinels are unavoidable, stop producers, use unforgeable control, reserve/order and prove propagation count.

**Conclusion.** In-band termination is topology-sensitive.

### Example 8

**Situation.** Consumer drains 10,000 items into a private batch before processing.

**Reasoning.** Queue depth falls but memory/in-flight ownership merely moved; producers refill and total backlog doubles. Bound batch count/bytes/time and include claimed work in pressure/accounting; release slots according to actual memory semantics.

**Conclusion.** Dequeue is not completion or resource release for the whole system.

### Example 9

**Situation.** Average λ is below μ but correlated five-minute dependency outages fill the buffer.

**Reasoning.** Stable means hide outage tails. Admission/circuit policy must reduce accepted rate, reject/spill within explicit capacity, expire stale work and recover without retry storm. Size only a useful burst, not the outage fantasy.

**Conclusion.** Queueing averages do not replace failure-distribution design.

### Example 10

**Situation.** A neonatal-monitor telemetry buffer approaches full while one consumer/storage path stalls.

**Reasoning.** Preserve critical alarms through reserved capacity and fail-safe direct escalation; sample/coalesce only clinically approved telemetry with explicit gaps; bound patient/device quotas, encrypt/clear data, use sequence/effect identity, and durably audit drops. Named clinical review defines allowable loss/latency.

**Conclusion.** High-stakes shedding and priority are domain safety decisions.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md): locks, semaphores, atomics, memory models and progress properties implement buffers.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): ingestion, partitioning, watermarking, batching, replay and schema/effect identity scale the pattern.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): scheduler, pipes/socket buffers, cache coherence and wait/wake affect throughput/latency.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): quota abuse, payload retention, tenant isolation, priority authorization and dead-letter protection constrain queues.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): durable brokers, leases, duplicates, idempotency and reconciliation extend in-memory delivery.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): resource limits, watermarks, telemetry, graceful drain and incident recovery operationalize buffers.
- [SEPAT-073](073-half-sync-half-async.md), [SEPAT-075](075-thread-pool.md) and [SEPAT-077](077-monitor-object.md) apply or implement the pattern; [SEPAT-080](../ROADMAP.md) selects the architecture.

## References

1. Oracle. “BlockingQueue,” Java SE 25 API. Capacity, atomic operations, close note and memory consistency. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/BlockingQueue.html>. Accessed 2026-08-29.
2. The Open Group. “pthread_cond_clockwait, pthread_cond_timedwait, pthread_cond_wait,” POSIX.1-2024. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html>. Accessed 2026-08-29.
3. Reactive Streams Initiative. “Reactive Streams JVM Specification,” version 1.0.4. <https://github.com/reactive-streams/reactive-streams-jvm>. Accessed 2026-08-29.
4. LMAX Exchange. “Disruptor User Guide.” <https://lmax-exchange.github.io/disruptor/user-guide/>. Accessed 2026-08-29.
5. LMAX Exchange. “Disruptor Technical Paper.” <https://lmax-exchange.github.io/disruptor/files/Disruptor-1.0.pdf>. Accessed 2026-08-29.
6. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Blocking queues, producer-consumer, task execution and cancellation.
7. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012. Concurrent queues and memory reclamation.
8. Butenhof, David R. *Programming with POSIX Threads*. Addison-Wesley, 1997.
9. Downey, Allen B. *The Little Book of Semaphores*, 2nd ed. Green Tea Press, 2016. Producer-consumer synchronization.
10. Little, John D. C. “A Proof for the Queuing Formula: L = λW.” *Operations Research* 9, no. 3 (1961): 383–387.
11. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020.

Queue capacity/fairness/close, memory ordering, lock-free progress, wait strategies, bulk operations, cancellation and reactive demand vary by runtime/library/hardware version. Current official sources were checked on 2026-08-29; verify exact deployed semantics.

## Exercises

### Exercise 1

Design an MPMC bounded work-sharing buffer with item and byte capacity. Specify lifecycle, ownership, enqueue/dequeue linearization, invariants, memory publication, fairness, cancellation, retry/effect identity, close/drain/abort and at least eight checks.

### Exercise 2

A buffer has (K=256), maximum item 48 KiB, accepted rate 1,200/s and stable mean queue residence 120 ms. Consumers number 12 and each sustains 110 items/s for this workload. Compute maximum queued payload, average queued items, aggregate nominal service, utilization and necessary stability inequality. Explain limitations.

### Exercise 3

Design a nonblocking backpressured pipeline from network event loop through CPU parsing and a 40-connection database. Include watermarks/demand, queue/byte/per-tenant capacities, ordering, deadlines, batches, cancellation, failures, close and observability.

### Exercise 4

Diagnose a pipeline using an unbounded queue, count-only limits, blocking event-loop puts, mutable payloads, an SPSC ring with multiple producers, strict priority, huge drain batches, requeue after ambiguous effects, one poison pill for eight consumers and empty-means-done shutdown. Provide remediation/testing.

### Exercise 5

Design bounded producer-consumer buffering for a safety-critical emergency telemetry system. Address identity, priority/loss policy, finite memory, backpressure, sequencing, consumer/effect failure, durability, fail-safe close/recovery, security, observability, testing and external review.

## Answers to the Exercises

### Answer 1

Use stable item/effect ID, producer/tenant/partition/sequence, schema, monotonic deadline, immutable payload/lease, byte size, authority/class and trace. Admission atomically reserves both one slot and bytes/per-tenant capacity; rejection returns ownership; successful enqueue publishes initialized data and transfers ownership. Dequeue atomically assigns one identity to one consumer/in-flight lease; terminal ack/requeue/quarantine is serialized under same identity.

Invariants include (0\le count\le K), (0\le bytes\le B_{max}), permit conservation, no duplicate queue/in-flight identity, initialized-before-visible memory order, no slot reuse before release, per-partition ordering policy, queue wait inside deadline, bounded in-flight/retry/result, effect-aware requeue, fair/quota admission, and all lifecycle paths returning permits/leases once. Cancellation before enqueue retains ownership; queued removes/marks; claimed/running reconciles actual effect.

Close is protected generation state: rejects production, wakes all, drains to EOS; abort terminally disposes queue and reconciles in-flight. Join before destruction. Tests cover simultaneous full/empty/byte races, producer failure between permits/publish, consumer failure before/after effect/ack, duplicates, wrap, large items, fairness, deadlines, close/abort and memory visibility on target runtime.

### Answer 2

Maximum declared queued payload is

\[
256\times48\text{ KiB}=12{,}288\text{ KiB}=12\text{ MiB}.
\]

Little's Law gives average queued items

\[
L_q=\lambda W_q=1200\times0.12=144.
\]

Aggregate nominal consumer service is (12\times110=1320) items/s, so (1200<1320) satisfies the necessary mean inequality and nominal utilization is (1200/1320\approx0.9091), about 90.9%.

The memory bound excludes in-flight/results/object graphs/producers/overhead. Means do not bound bursts/tails, and high utilization amplifies wait under variability. Consumers may contend for downstream resources; arrivals/service may correlate or be nonstationary; hidden queues invalidate the boundary. No arithmetic proves ordering, ownership, memory visibility, fairness, durability or adequate deadlines.

### Answer 3

The event loop validates frame/tenant/size cheaply and maintains global/per-tenant byte/count credits. It never blocks: nonblocking offers into a finite parse stage, pauses read readiness at high watermark and resumes below low, or returns overload. CPU parsing uses a bounded pool near measured CPU with immutable leases and per-connection/partition sequence. Parsed DB commands enter a finite dependency queue/concurrency limiter at or below a safe share of 40 connections; connection acquisition consumes the same monotonic deadline.

Carry request/owner generation, tenant, sequence, deadline and effect ID. Preserve per-key order by partition/one-in-flight where needed, not global FIFO. Batch only bounded count/bytes/time and count claimed memory in pressure. Queue expiry skips not-started work; cancellation reclaims queued work but running DB effects are reaped/reconciled. Typed failures/dead-letter use bounded governed paths.

Shutdown stops network admission, drains/aborts parse and DB queues by policy, keeps results/event loop alive, reconciles effects, releases all leases/credits and joins. Observe every stage count/bytes/oldest/slack, watermarks, credits, tenant fairness, pool/DB acquisition/service, batches, reject/drop/cancel/retry/effect, hidden socket/output buffers and residue. Test saturation, slow tenants, parser/DB stalls, disconnect/reuse, ordering, full queues, memory, cancellation races and rolling shutdown.

### Answer 4

Unbounded/count-only design hides latency/memory; event-loop block freezes progress; mutable payloads race; SPSC is invalid for multiple producers; strict priority starves; batches move hidden backlog; effect-ambiguous requeue duplicates; one pill stops one consumer; empty is transient.

Use finite slot+byte+tenant/in-flight/result limits and nonblocking watermarks/demand/rejection. Copy/transfer immutable payloads. Replace ring with proven MPSC/MPMC topology or partition one producer per SPSC ring and verify memory order/wrap. Add weighted aging/reservations. Bound batch count/bytes/time and retain claimed-work accounting. Requeue with stable effect identity/lease/idempotent reconciliation and bounded retry.

Use out-of-band closed generation: stop producers, reject late items, broadcast/wake, drain to EOS for every consumer, join, then destroy. Verify conservation/identity model, exact topology, producer claim/publish failure, consumer effect/ack crash, target memory/race tools, adversarial fairness, batch memory, overload, mutable sentinels, close at every state and process restart.

### Answer 5

Every record carries device/patient/incident/session/generation, monotonic sequence/time/deadline, authenticated source/authority, classification, payload hash/schema, effect/idempotency ID and audit trace. Enforce fixed slot and byte memory, per-device/tenant quotas and reserved alarm capacity. Only clinically/safety-approved telemetry classes may sample/coalesce/drop; commands/alarms follow fail-safe escalation or durable protected spill. Record explicit gaps/drops.

Use sequence-qualified immutable buffers and verified publication; preserve per-device order while processing independent devices concurrently. Backpressure propagates to device/protocol credits where possible; otherwise bounded rejection/fail-safe alarm. Consumers use leases/acks and stable effect IDs so crash after storage/dispatch is reconciled without duplicate unsafe action. Bound retries and quarantine corrupt input.

Persist required accepted data/effect ledger before durable acknowledgement. Close transfers to safe fallback, stops producers, drains critical work, terminally classifies lower work, reaps effects, verifies sequence gaps and joins; restart authenticates sources/storage and reconciles before reopening. Encrypt/minimize payload, protect keys/audit/dead letters, authorize priority, rate-limit abuse and clear reused slots.

Observe queue bytes/count/age/slack by criticality/device, gaps/drops, producer/consumer rates, storage/effect ack, duplicate/late/cancel, resource health, fail-safe and residue. Verification includes state/conservation models, target memory/concurrency tests, hardware-in-loop, burst/outage/power/process/network/storage failures, adversarial security, overload/loss policy, close/restart/recovery drills and worst-case timing. Production claims require named clinical/emergency/domain/safety, device/controls, concurrency/platform, security/privacy, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance evidence.
