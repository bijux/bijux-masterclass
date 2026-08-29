---
module_id: CONPAR-017
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 17
title: Thread-Safe Queues
status: complete
last_verified: 2026-08-29
---

# Thread-Safe Queues

## One-Page Review

### Governing question

What must a concurrent queue guarantee about ordering, ownership, capacity, blocking, closure, visibility, progress, and reclamation so that producers and consumers can exchange work without loss, duplication, unbounded overload, or shutdown deadlock?

### Essential definitions

- A **queue** is an abstract sequence supporting insertion and removal under a declared order such as FIFO or priority.
- **thread-safe** means concurrent operations satisfy a stated consistency and progress contract, not merely avoid memory corruption.
- **linearizability** lets each completed operation appear to take effect atomically between invocation and response while respecting real-time precedence.
- **SPSC**, **MPSC**, **SPMC**, and **MPMC** name single/multiple producer and consumer topologies.
- A **bounded queue** has finite admitted capacity; an **unbounded queue** has no intrinsic application bound.
- **backpressure** couples producer progress to downstream capacity.
- A **linearization point** is the abstract instant an enqueue, dequeue, close, or failure takes effect.
- **ownership transfer** moves responsibility for an accepted item from producer to queue, then from queue to one consumer.
- **close** forbids future insertion and defines how buffered items and waiters terminate.
- **drain** removes accepted items before final closure; **abort** may discard according to an explicit policy.
- **work completion** means processing reached a terminal outcome, which is later than dequeue.
- **memory reclamation** proves removed nodes are not freed while another participant can still access them.

### Central model, mechanism, or theorem

For a bounded FIFO queue with capacity (K), sequence (Q), and lifecycle (L), maintain:

(0 <= |Q| <= K).

A successful enqueue atomically appends one item only when insertion is permitted and creates queue ownership. A successful dequeue atomically removes exactly the head and transfers ownership to one consumer. Empty/full attempts block, time out, fail, or return a special result according to the selected operation. Close is a linearized lifecycle transition, not a sentinel value.

Linearizability plus the representation invariant proves a legal abstract history. It does not prove fairness, bounded response, item processing success, durability, or distributed delivery semantics.

### Critical invariants

Each accepted item is represented exactly once in queue storage until one successful dequeue. Failed insertion retains producer ownership. Successful dequeue gives exactly one consumer ownership. FIFO follows the documented scope—often one global enqueue order, not wall-clock creation order. Head, tail, count, and slots agree. Full/empty predicates are checked under the synchronization protocol. Capacity covers the intended scarce units, including bytes where item sizes vary. Close wakes blocked producers and consumers with unambiguous outcomes. Accepted-item and terminal-outcome accounting reconcile at shutdown. Removed storage is reclaimed only after no possible observer remains.

### Common failures

Teams call an effectively unbounded queue “thread-safe”; bound slots but not payload bytes or waiting producers; inspect size before acting; use if instead of predicate loops; notify before mutation; treat dequeue as completion; lose ownership when a timed insertion races with success; accept after close; use one poison pill for many consumers; confuse empty-open with closed-drained; let workers recursively submit to the same full queue; assume priority queues are FIFO among ties; mutate enqueued objects; hold a blocking queue call across async execution; or generalize an SPSC ring to MPMC without a new ordering and reclamation proof.

### Compact example

A capacity-two FIFO contains [A]. Producer P successfully appends B, so [A,B] is full and P transfers ownership of B. Producer R waits. Consumer C removes A, takes ownership, and creates one free slot; R may now append C. If shutdown closes before R succeeds, R must retain C and receive “closed.” Consumers remove B and then report closed-and-drained. None may interpret transient empty as end-of-stream.

### Connections

[Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) defines endpoint and item custody; [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md) supplies not-empty/not-full loops; [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md) supplies capacity conservation. The [program roadmap](../ROADMAP.md) next covers lock ordering, bounded worker pools, thread-local state, and thread cancellation.

## Governing Question

How can an engineer refine “put work in a queue” into a complete concurrent protocol whose abstract history, bounds, ownership, wait behavior, closure, completion, memory visibility, and reclamation remain correct under every interleaving and terminal path?

The queue is not just a container. It is the admission and ownership boundary between components with potentially different rates and lifetimes.

## Why This Matters

Producer-consumer queues decouple when work is created from when it is processed. They underpin worker pools, logging, event loops, network pipelines, schedulers, device drivers, actors, and background maintenance. A correct queue can remove ad hoc shared-state coordination and make ownership explicit.

Decoupling can conceal overload. If producers sustain rate (lambda) above consumer service rate (mu), backlog grows. An unbounded queue converts overload into memory growth and increasingly stale work. A bounded queue forces a deliberate policy: block, time out, reject, shed, coalesce, spill durably, or reduce upstream demand.

Thread safety alone is incomplete. A queue may be linearizable but unfair; bounded by item count but not bytes; safe for MPSC but not MPMC; FIFO per producer but not across producers; nonblocking but unable to wake a shutdown waiter; or correct while live but unsafe during node reclamation. Every product requirement must map to a supported guarantee.

Current APIs expose these differences. Java SE 26 `BlockingQueue` offers exception, special-value, blocking, and timed operation families, optional bounded capacity, atomic individual operations, memory-consistency effects, and no intrinsic close. Python 3.14 `queue.Queue` provides synchronized MPMC operations, approximate inspection, task tracking, and shutdown behavior introduced in 3.13. Rust 1.98 `std::sync::mpsc` distinguishes asynchronous and synchronous channels and closes through endpoint disconnection. Go channels define typed capacity, close, receive results, and memory-model edges. Use the actual selected contract.

## Prerequisites and Retrieval

Retrieve:

- ownership transfer, endpoint topology, backpressure, close, and terminal accounting from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- shared-state representation invariants from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- atomic wait loops and close/cancellation predicates from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- capacity conservation from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- lifecycle and joining from [Creating and Joining Threads](011-creating-and-joining-threads.md); and
- sequences, ring arithmetic, partial orders, linearizability, queueing theory, memory models, and exception-safe ownership.

Retrieval prompt: capacity is two and queue is empty. Trace enqueue A, enqueue B, failed nonblocking enqueue C, dequeue A, successful enqueue C, close, dequeue B, dequeue C, and one final take. Mark ownership and lifecycle after every step.

## Learning Objectives

After completing this module, a learner can:

1. specify queue topology, abstract order, operation variants, and progress guarantees;
2. prove bounded sequence or ring-buffer representation invariants;
3. identify enqueue, dequeue, and close linearization points;
4. design not-empty and not-full predicate loops without lost wakeups;
5. track ownership across success, timeout, cancellation, close, and processing failure;
6. distinguish queue occupancy, in-flight work, and terminal completion;
7. choose item, byte, time, and waiter bounds plus an overload policy;
8. explain why MPMC lock-free reclamation requires a new proof; and
9. identify safety-critical delivery claims requiring named human review.

## Core Exposition

### Specify topology and abstract order

First choose endpoint multiplicity. An SPSC ring can assign head exclusively to the consumer and tail to the producer. MPSC needs producer arbitration. SPMC needs consumer arbitration. MPMC requires both. Cloning an endpoint changes the topology and invalidates any proof tied to uniqueness.

Then define order. FIFO means dequeue follows successful enqueue linearization order, not necessarily request creation or method invocation time. Concurrent enqueues overlap and may linearize in either order. A priority queue follows its comparator; ties need an explicit stable sequence if FIFO among equal priorities matters. Work stealing often provides local LIFO and remote stealing rather than global FIFO.

Do not demand ordering the workload does not need. Relaxed order can improve scalability, but each relaxation must remain visible to callers.

### Sequence representation and transitions

For an abstract bounded queue, state is (Q,K,L), where (Q) is an ordered finite sequence, (K>0), and lifecycle (L) is open, closing/draining, closed-drained, or aborted.

- enqueue(x) in open state with (|Q|<K) changes (Q) to (Q followed by x);
- dequeue in nonempty state changes (x followed by Q') to (Q') and returns x;
- close changes open to closing without modifying accepted items;
- when closing and (Q) becomes empty, lifecycle becomes closed-drained;
- abort follows its stated disposition for buffered items.

Empty-open means “no item now; future insertion possible.” Closed-drained means “no item now or later.” The return type must distinguish them.

### Ring-buffer representation

A fixed array ring typically stores head (h), tail (t), and count (n), with (0<=h,t<K) and (0<=n<=K). Occupied logical position (i) maps to slot ((h+i) mod K). Enqueue writes slot (t), advances (t=(t+1) mod K), and increments (n). Dequeue reads/clears slot (h), advances (h=(h+1) mod K), and decrements (n).

If only head and tail are stored, equal indices can mean empty or full; reserve one slot or add a count/generation bit. Every mutation must preserve correspondence among count, slots, and ownership. Clear removed references so storage can be reclaimed.

### Lock-based bounded MPMC protocol

A reviewable implementation uses one mutex protecting buffer, indices/count, and closed state; a not-empty condition; and a not-full condition. Producer loops while full and open, atomically waits, rejects if closed, appends, then signals not-empty. Consumer loops while empty and open, waits, returns closed when empty-and-closed, removes, then signals not-full.

<!-- bijux-verify: {"id":"bounded-queue-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral monitor pseudocode states queue predicates and ownership boundaries; exact locking, cancellation, and error APIs are platform-specific."} -->
```text
put(item):
    lock
    while size == capacity and state == open: wait(not_full)
    if state != open: unlock; return closed_with_item
    append(item)              # ownership transfers here
    signal(not_empty)
    unlock; return accepted

take():
    lock
    while size == 0 and state == open: wait(not_empty)
    if size == 0: unlock; return closed_and_drained
    item = remove_head()      # ownership transfers here
    signal(not_full)
    unlock; return item
```

State changes occur before notifications. Loops cover spurious returns and competing participants. Close under the mutex changes lifecycle and broadcasts both conditions so blocked producers reject and consumers drain or terminate.

### Ownership and completion accounting

Before successful enqueue, producer owns the item. At the enqueue linearization point, queue owns it. At successful dequeue, one consumer owns it. A failed, timed-out, cancelled, or closed enqueue retains producer ownership unless the API explicitly reports success.

Dequeue is not work completion. Track accepted, dequeued/started, and terminal outcomes separately. A consumer exception must still record failed/cancelled/panicked disposition. Python-style task tracking makes each successful get create one task-done obligation; too many or missing acknowledgements corrupt join semantics.

At graceful shutdown:

(accepted = buffered + in_flight + terminal),

and after drain/join:

(accepted = terminal).

Retries require identities and policy: a retry may be a new accepted attempt while the logical job remains one. Avoid silently counting duplicates as success.

### Bounds and overload policy

An item bound is inadequate when payloads range from bytes to gigabytes. Bound queued items, queued bytes, in-flight work, per-tenant share, waiting producers, and lifetime where relevant. A bounded internal buffer plus an unbounded executor submission list is still unbounded.

Capacity is a service decision tied to measured saturation, latency budget, and memory. Little's relation (L=lambda W) explains that large average queue length implies waiting at a given throughput; it does not choose capacity by itself.

When full, define one of:

- block with cancellation and a monotonic deadline;
- reject immediately with ownership retained;
- shed by priority or tenant;
- coalesce replaceable state updates;
- drop newest/oldest only with explicit loss semantics;
- spill to durable storage with its own quota; or
- propagate demand reduction upstream.

Blocking is backpressure only if the producer cannot relocate work into another unbounded buffer or task set. Recursive submission from workers to their own full queue can deadlock when all consumers are blocked producing.

### Operation families and deadline semantics

Insertion/removal commonly offer throwing, special-result, blocking, and timed variants. Select them from caller policy. Immediate offer supports load shedding. Blocking put fits trusted backpressure when shutdown can wake it. Timed operations bound admission delay but need one absolute monotonic deadline across spurious wakes and retries.

An inspection such as size, empty, full, or remaining capacity is a racy observation. It can drive metrics but not a later decision. Use the atomic operation and handle its result. Peek has its own linearization point; the item can be removed immediately afterward.

Bulk operations require explicit atomicity. Java's `BlockingQueue` does not promise all bulk collection operations are atomic, and drain-to can have partial effects if the destination rejects an item. Transactional batch enqueue/dequeue needs a separate contract and rollback/ownership proof.

### Closure, draining, abort, and poison pills

Closure is shared lifecycle state. Once close linearizes, future insertion fails and waiting producers wake with their items. Consumers may drain items accepted earlier, then receive an unambiguous terminal result. Close should be idempotent or return a documented repeated-call outcome.

Abort differs: decide whether buffered items are returned to an owner, reported cancelled, dead-lettered, or destroyed. Never silently discard owned work. A shutdown timeout can escalate drain to abort, but the transition and accounting must be observable.

Poison pills are ordinary queue items masquerading as lifecycle. One pill wakes only one of several competing consumers unless it is re-enqueued or one pill per consumer is accounted. Pills compete for bounded capacity, can appear before later submissions if close is not serialized, and can collide with domain values. Endpoint closure or explicit lifecycle state is usually clearer. Java `BlockingQueue` itself defines no intrinsic close, so applications using it must own this protocol.

Endpoint-counted channels close when all senders disappear or an authorized endpoint closes. That design still requires a rule for buffered drain and receiver cancellation.

### Publication and item mutability

A successful transfer must publish item initialization to the consumer according to the API's memory model. Java documents a happens-before edge from actions before placement to actions after access/removal. Go defines send/receive and close synchronization rules. Rust channel safety and ownership prevent unsynchronized use of moved non-shared values.

Transfer does not freeze aliases. If producer retains a mutable reference and changes the object after enqueue, consumer access can race. Move ownership, enqueue an immutable value, copy a snapshot, or separately synchronize shared internals.

Queue visibility covers the transferred item and specified lifecycle state, not unrelated memory accessed without a valid edge. Do not rely on approximate metrics as publication.

### Fairness and scheduling

FIFO item order does not imply FIFO waiter service. A newly arriving producer or consumer may barge ahead of a long waiter. Some implementations offer fairness policies with throughput costs; many do not promise bounded bypass.

Measure maximum producer/consumer wait, not just mean queue delay. Priority queues can starve low-priority items; add aging, classes, quotas, or deadlines when the service contract requires them. A single slow consumer can cause head-of-line blocking if item order forbids parallel selection.

### Lock-free boundaries and reclamation

Lock-free means system-wide progress despite a delayed participant; it does not mean wait-free, fair, allocation-free, or automatically faster. The Michael-Scott MPMC queue uses linked nodes and compare-and-swap, but a production implementation also needs a memory-model mapping, safe reclamation, allocator behavior, ABA analysis, shutdown, and endpoint lifecycle.

An SPSC ring is much simpler because roles exclusively own indices and fixed storage avoids node reclamation. Adding a second producer or consumer changes reservation and publication. A local extra compare-and-swap does not create an MPMC proof.

Hazard pointers, epochs, tagged pointers, reference counting, or garbage collection address different reclamation assumptions. Choose a mature implementation whose topology and progress contract match the product rather than improvising unsafe machinery.

### Async and cross-process boundaries

A blocking thread queue call can park an executor thread. Async code needs an async-aware queue whose waits yield tasks and whose cancellation removes waiter registrations safely. Never hold unrelated locks across await, and bound the number of suspended producers as well as buffered items.

A process-local queue does not provide durable delivery or coordinate machine failure. Cross-process queues require serialization, permissions, lifecycle, and crash semantics. Distributed brokers add acknowledgement, redelivery, ordering partitions, persistence, and consumer-group contracts; “exactly once” requires end-to-end idempotency or transactions beyond an in-memory dequeue.

### Observability and testing

Record accepted/rejected/timed-out/closed insertions; dequeue and terminal outcomes; item and byte occupancy; high-water marks; producer/consumer wait and item age; in-flight work; close/drain/abort times; duplicates; and invariant violations. Queue size alone cannot show throughput, saturation cause, or completion.

Test empty/full boundaries, wraparound, competing producers/consumers, close while each class waits, timeout-success races, cancellation, item-constructor/consumer exceptions, duplicate completion, drain escalation, recursive submission, large payloads, fairness, and destruction. Linearizability histories need invocation/response intervals and returned values. Stress and race detection complement, not replace, an abstract oracle.

## Definitions and Notation

Let queue sequence be (Q=<q_0,...,q_{n-1}>), capacity (K), lifecycle (L), accepted count (A), in-flight count (F), and terminal count (T). Maintain (0<=n<=K) and ownership partition (A=n+F+T) for one non-retrying batch.

For a ring, head (h), tail (t), and (n) satisfy index bounds and occupied-slot mapping ((h+i) mod K). Invocation and response times (inv(op),res(op)) constrain a linearization point (lin(op)) between them. Real-time precedence requires completed earlier operations precede later invocations in the abstract history.

Arrival rate is (lambda), service capacity (mu), waiting time (W), and average queued work (L_q). These are measured workload quantities, not correctness invariants.

## Mechanisms, Invariants, or Proof Structure

Apply:

1. **Declare topology and order.** Name producer/consumer multiplicity and ordering scope.
2. **Define ownership.** Locate transfer points for success and every failure.
3. **Prove representation.** Relate sequence or ring slots, indices, and count.
4. **Bound the system.** Include items, bytes, waiters, in-flight work, and time.
5. **Specify operations.** Immediate, blocking, timed, bulk, and cancellation outcomes.
6. **Linearize lifecycle.** Define close, drain, abort, and repeated calls.
7. **Separate completion.** Reconcile accepted, buffered, in-flight, and terminal work.
8. **Map visibility.** Use the chosen memory-model edges and prevent mutable aliases.
9. **Own progress/reclamation.** Do not generalize topology or lock-free claims.
10. **Measure and test.** Use histories, invariants, overload, and shutdown oracles.

The executable model enumerates the twenty relative schedules of three ordered puts and three ordered takes. A capacity-two blocking FIFO admits only schedules whose abstract count never falls below zero or exceeds two.

<!-- bijux-verify: {"id":"bounded-fifo-operation-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=20\ncapacity_safe_histories=4\nunderflow_histories=15\noverflow_histories=1\n","stderr":""}} -->
```python
histories = []


def extend(puts, takes, events):
    if puts == 3 and takes == 3:
        histories.append(events)
        return
    if puts < 3:
        extend(puts + 1, takes, events + "P")
    if takes < 3:
        extend(puts, takes + 1, events + "T")


extend(0, 0, "")
safe = 0
underflow = 0
overflow = 0
for history in histories:
    count = 0
    went_below = False
    went_above = False
    for event in history:
        count += 1 if event == "P" else -1
        went_below = went_below or count < 0
        went_above = went_above or count > 2
    underflow += int(went_below)
    overflow += int(went_above)
    safe += int(not went_below and not went_above)

print(f"candidate_histories={len(histories)}")
print(f"capacity_safe_histories={safe}")
print(f"underflow_histories={underflow}")
print(f"overflow_histories={overflow}")
```

Limitations: this finite sequential event model treats blocked attempts as rejected histories. It does not store values, run threads, prove FIFO linearizability, model wakeups, close, cancellation, weak memory, fairness, or reclamation.

## Alternatives and Trade-Offs

**Lock-based bounded queues** provide blocking, close-and-wake, and straightforward invariant review. Mutex contention and convoying may limit scaling.

**SPSC rings** offer fixed storage and simple role ownership, but cannot be safely widened to multiple endpoints without redesign.

**Lock-free queues** can provide system-wide progress and reduce blocking, while adding memory-order, reclamation, lifecycle, and debugging complexity.

**Unbounded queues** simplify producer progress but convert sustained overload into memory and latency growth. “Unbounded” is not infinite and is rarely a responsible service default.

**Synchronous/rendezvous channels** have zero buffer, directly coupling producer and consumer. They minimize queued age but can reduce burst tolerance and create dependency cycles.

**Priority or deadline queues** align selection with urgency but weaken FIFO, can starve low classes, and require stable tie and expiration policy.

**Per-worker deques and work stealing** reduce central contention and improve locality. They expose different ordering, balancing, and shutdown semantics.

**Actors and async channels** package endpoint ownership and task-aware waiting. Their mailbox bounds, cancellation, and supervision contracts still need review.

**Durable brokers** survive process failure and add acknowledgement/redelivery. They cost serialization, storage, network coordination, and end-to-end duplicate handling.

## Failure Modes and Misconceptions

- **“Thread-safe means production-safe.”** Ordering, bounds, close, progress, and accounting may still be wrong.
- **“FIFO means invocation order.”** Overlapping operations may linearize in either order.
- **“Capacity 1,000 bounds memory.”** Payload bytes, waiters, tasks, and in-flight work may remain unbounded.
- **“Size then put is safe.”** Inspection races; use atomic offer/put.
- **“Empty means finished.”** Empty-open permits future insertion; completion requires lifecycle and in-flight accounting.
- **“Dequeued means done.”** Processing may fail, cancel, retry, or panic.
- **“A sentinel closes the queue.”** Multiple consumers, ordering, and capacity complicate pills.
- **“Timeout means no transfer.”** Trust the operation result and ownership contract at the race boundary.
- **“Bulk means atomic.”** Many collection-style bulk operations permit partial effects.
- **“Lock-free means wait-free and faster.”** Progress class, reclamation, allocation, and workload matter.
- **“SPSC plus CAS becomes MPMC.”** Endpoint multiplicity changes the proof.
- **“A bounded queue always backpressures.”** Producers may relocate backlog elsewhere.
- **“One queue fits all tenants.”** Hot producers can monopolize space and service.
- **“Close can destroy immediately.”** Holders, waiters, buffered items, and endpoint references must reach quiescence.

## Worked Examples

### Example 1

**Question:** Queue capacity is two; A and B are buffered and offer(C) is immediate.

**Reasoning:** The full predicate holds at offer's linearization attempt. C never enters queue ownership.

**Conclusion:** Offer fails and the producer retains C.

### Example 2

**Question:** Producers P and R concurrently enqueue A and B.

**Reasoning:** Their invocation intervals overlap, so a linearizable FIFO may order either enqueue first. Later dequeues must follow the selected order.

**Conclusion:** FIFO respects enqueue linearization, not wall-clock intent.

### Example 3

**Question:** A consumer observes size one, then calls take.

**Reasoning:** Another consumer can remove the item between operations, making take block.

**Conclusion:** Size is diagnostic; poll/take supplies the atomic outcome.

### Example 4

**Question:** A capacity-100 queue admits 100 objects of 500 MiB each.

**Reasoning:** The item invariant holds while memory demand approaches 50 GiB plus overhead.

**Conclusion:** Bound bytes and validate payload size, not only slots.

### Example 5

**Question:** Four consumers share one poison pill.

**Reasoning:** One consumer removes it; three may remain blocked. Re-enqueueing changes order and can fail on lifecycle/capacity.

**Conclusion:** Prefer explicit close broadcast or account one terminal item per consumer under serialized submission.

### Example 6

**Question:** Every worker dequeues a task and synchronously enqueues two children to the same full queue.

**Reasoning:** All consumers become blocked producers; no thread remains to free capacity.

**Conclusion:** Use coordinator submission, nonblocking overflow policy, reserved capacity, or a proven work-stealing design.

### Example 7

**Question:** Close occurs while one producer waits on full and one consumer waits after drain.

**Reasoning:** Both predicates changed. Producer must wake and recover its item; consumer must wake and receive closed-drained.

**Conclusion:** Close broadcasts producer and consumer wait sets with distinct outcomes.

### Example 8

**Question:** What does the executable enumeration establish?

**Reasoning:** Of twenty ordered put/take schedules, four keep occupancy within zero and two; fifteen underflow and one exceeds capacity.

**Conclusion:** It recomputes a bounded-count condition, not a queue implementation.

### Example 9

**Question:** A linearizable queue shows one writer waiting for seconds.

**Reasoning:** Safety and abstract order hold, but scheduler/waiter policy provides no bounded fairness.

**Conclusion:** Measure wait-age tails and select a supported fairness or sharding policy.

### Example 10

**Question:** Can a priority queue alone safely schedule commands for autonomous train braking?

**Reasoning:** Queue order cannot establish sensor validity, stopping physics, deadline feasibility, fail-safe behavior, redundancy, hardware faults, or certification.

**Conclusion:** No. Named authorized railway signaling, controls, real-time, hardware, functional-safety, verification, cybersecurity, human-factors, and regulatory reviewers must approve the actual system. No external review is claimed.

## Cross-Program Connections

- **Data structures:** rings, linked lists, heaps, deques, and reclamation determine representation.
- **Programming languages:** ownership, exceptions, memory models, async suspension, and endpoint types define transfer.
- **Operating systems:** scheduling, parking, wakeups, pipes, and process sharing affect progress.
- **Distributed systems:** brokers add durability, redelivery, partitions, and consumer-group coordination.
- **Cloud engineering:** admission control, worker pools, load shedding, tenant quotas, and metrics depend on queue bounds.
- **Formal methods:** linearizability, refinement histories, invariants, and temporal progress supply verification.

## References

1. Leslie Lamport, “Specifying Concurrent Program Modules,” *ACM TOPLAS* 5(2), 1983, [doi:10.1145/69624.357214](https://doi.org/10.1145/69624.357214).
2. Maurice Herlihy and Jeannette Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” *ACM TOPLAS* 12(3), 1990, [doi:10.1145/78969.78972](https://doi.org/10.1145/78969.78972).
3. Maged M. Michael and Michael L. Scott, “Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms,” PODC 1996, [doi:10.1145/248052.248106](https://doi.org/10.1145/248052.248106).
4. Oracle, “BlockingQueue,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/BlockingQueue.html) (retrieved 2026-08-29).
5. Oracle, “ArrayBlockingQueue,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ArrayBlockingQueue.html) (retrieved 2026-08-29).
6. Python Software Foundation, “queue — A synchronized queue class,” Python 3.14.7, [official documentation](https://docs.python.org/3/library/queue.html) (retrieved 2026-08-29).
7. Rust Project, “std::sync::mpsc,” Rust 1.98 standard library, [official API](https://doc.rust-lang.org/std/sync/mpsc/) (retrieved 2026-08-29).
8. The Go Authors, “Channel types,” *Go Language Specification*, [official specification](https://go.dev/ref/spec#Channel_types) (retrieved 2026-08-29).
9. The Go Authors, “The Go Memory Model,” version of 2022-06-06, [official specification](https://go.dev/ref/mem) (retrieved 2026-08-29).
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

Define queue topology, FIFO linearization order, ownership transitions, and full/empty/closed outcomes for a bounded MPMC queue.

### Exercise 2

Prove the abstract capacity invariant across successful put, failed offer, take, close, and closed-drained take. State what remains unproved.

### Exercise 3

Diagnose a worker pool with 1,000 slots, unlimited payload bytes, blocking recursive submission, poison-pill shutdown, and final counts taken at dequeue.

### Exercise 4

Compare a mutex/condition MPMC queue, SPSC ring, lock-free MPMC queue, per-worker stealing deques, and durable broker for a bounded job engine.

### Exercise 5

A medical alarm service uses a priority queue. State what chapter evidence can establish and what requires named authorized human review.

## Answers to the Exercises

### Answer 1

Multiple producers and consumers may call operations. Each successful enqueue linearizes between invocation and response and transfers one item to the queue; FIFO dequeues follow that abstract enqueue order. Successful dequeue transfers the unique head to one consumer. Immediate full returns failure with producer ownership; blocking/timed variants wait or return their documented outcome. Empty-open waits/fails transiently, while closed-drained is terminal. Close linearizes once, rejects future insertions, wakes both waiter classes, and permits the declared drain policy.

### Answer 2

Initially (Q) is empty and (0<=|Q|<=K). Successful put requires open and (|Q|<K), so appending yields at most (K). Failed offer changes nothing. Successful take requires nonempty, so removing the head leaves a nonnegative length. Close changes only lifecycle; draining takes preserve the bound. Closed-drained take changes nothing. The proof does not establish FIFO implementation, linearizability, visibility, fairness, ownership accounting, byte bounds, completion, or reclamation; those need their stated assumptions and evidence.

### Answer 3

The slot bound does not constrain memory, so add per-item validation and queued/in-flight byte budgets. Recursive blocking submission can deadlock when every worker waits for capacity; centralize child scheduling, use nonblocking policy, or adopt proven work stealing. Poison pills do not broadcast reliable lifecycle to an unknown/multiple consumer set; close under the queue protocol and wake all. Dequeue counts only starts. Record one terminal outcome for every accepted identity, including failure/cancellation/panic, join workers, then reconcile accepted equals terminal. Bound producers, deadlines, retries, and shutdown escalation too.

### Answer 4

The lock-based MPMC queue best fits simple blocking backpressure, close-and-wake, and auditability, at contention cost. An SPSC ring is excellent only when exactly one endpoint exists on each side. Lock-free MPMC can improve progress under stalls but demands memory-order, reclamation, and lifecycle expertise; use a mature implementation. Work-stealing deques improve locality and balancing but relax global FIFO and complicate termination. A durable broker is justified for process failure, persistence, and redelivery, but introduces serialization, network partitions, acknowledgement, duplicates, and operational cost. Choose from actual topology, failure domain, ordering, latency, and ownership requirements.

### Answer 5

Internal evidence can validate abstract capacity histories, representation and lifecycle reasoning, ownership transitions, source currency, snippet output, local links, and exercise correspondence. It cannot establish alarm clinical priority, physiological deadlines, sensor validity, delivery infrastructure, device hazards, human response, fail-safe behavior, cybersecurity controls, regulatory compliance, or deployment fitness. Named authorized clinical, medical-device systems, real-time, controls, hardware, functional-safety, verification, cybersecurity, human-factors, quality, and regulatory reviewers must approve the real requirements, implementation, evidence, and operation. This chapter claims no external review.
