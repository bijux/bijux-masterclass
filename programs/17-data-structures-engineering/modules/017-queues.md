---
module_id: DSE-017
program: Data Structures Engineering
level: 1
module_number: 17
title: Queues
status: complete
last_verified: 2026-08-29
---

# Queues

## One-Page Review

### Governing question

How can a first-in-first-out abstraction preserve admission order while making empty/full policy, backpressure, cancellation, fairness, lifecycle, representation, and concurrent publication explicit?

### Essential definitions

- A **queue** is a finite sequence with removal at the **front/head** and insertion at the **back/tail**.
- **Enqueue/offer** appends an element at the back; **dequeue/poll** removes and returns the front; **peek** observes the front.
- **FIFO** means that if accepted element `x` precedes accepted element `y` and neither is removed otherwise, `x` is dequeued before `y`.
- **Underflow/empty** is a removal or observation request with no element available.
- **Full/overflow** is an admission request that cannot succeed under a capacity/resource policy.
- **Backpressure** is a mechanism by which insufficient downstream capacity affects producers; a finite buffer alone does not define it.
- **Admission order** is the abstract order of successful enqueue operations. It need not equal request-arrival, waiter-wakeup, completion, or service-finish order.
- A **bounded queue** has an explicit item/byte capacity and a full policy such as reject, block, time out, drop, or coalesce.
- **Close/shutdown** defines whether new elements are accepted, whether buffered elements drain, and how waiting producers/consumers terminate.
- A **linearization point** is the instant a concurrent enqueue/dequeue takes effect in one legal FIFO history.

### Central model, mechanism, or theorem

Write the abstract queue front-to-back as

\[
Q=\langle q_0,\ldots,q_{n-1}\rangle.
\]

Successful `enqueue(x)` maps Q to `Q·<x>`; successful `dequeue()` for `n>0` returns `q_0` and leaves `<q_1,...,q_(n-1)>`; `peek()` returns `q_0` unchanged. For accepted enqueues `x_1,...,x_k` with no other operation removing them, successive dequeues return `x_1,...,x_k`. The proof follows by induction from append-back/remove-front.

A linked representation uses head and tail; a ring representation uses bounded or growable circular indexing; a segmented deque supplies front/back operations. A plain contiguous array that shifts the suffix on every dequeue is correct but performs linear movement. Core FIFO semantics do not select one representation or full/empty API.

### Critical invariants

1. The representation encodes exactly the abstract front-to-back sequence.
2. Empty is exactly depth zero; head/tail or indices agree with it.
3. A successful enqueue publishes exactly one constructed element at the back.
4. A successful dequeue removes exactly one front element and returns it under the ownership/failure contract.
5. Rejected/timed-out/cancelled admission has the stated no-effect or partial-effect behavior.
6. Count, item/byte capacity, head/tail indices, generation, and arithmetic remain valid.
7. Waiting, wakeup, close, cancellation, and shutdown cannot strand accepted work silently.
8. Concurrent visibility, ordering, progress, and reclamation follow a specific algorithm and memory model.

### Common failures

- Calling any container with `append` and `pop` a FIFO queue without checking ends.
- Shifting an array on every dequeue and claiming constant-time operations.
- Keeping a head offset forever and retaining consumed objects or unbounded dead space.
- Forgetting to clear tail when the last linked node is removed.
- Treating “unbounded” as infinite rather than resource/policy-limited.
- Adding a capacity without defining reject, block, timeout, drop, or coalesce semantics.
- Claiming FIFO fairness for threads, tasks, priorities, or service completion from FIFO element order alone.
- Using a poison value that can collide with real data or be consumed by only one of several consumers.
- Ignoring close, cancellation, interrupted waits, producer failure, or consumer abandonment.
- Treating atomic head/tail fields as a complete concurrent queue or reclamation proof.

### Compact example

A capacity-three linked queue accepts A and B, dequeues A, then accepts C and D. It rejects E while full. Dequeuing until empty yields B, C, D, so the total removal order is A, B, C, D. Both head and tail become empty, and another dequeue reports underflow. The trace checks finite FIFO and metadata, not blocking, timing, allocation failure, or concurrency.

### Connections

[DSE-014](014-singly-linked-lists.md) supplies head/tail ownership; [DSE-016](016-stacks.md) supplies the contrasting LIFO law and bounded-policy vocabulary; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supplies capacity growth. The [program roadmap](../ROADMAP.md) next develops deques and ring buffers as richer or more specialized endpoint structures.

## Governing Question

What abstract FIFO law, representation invariant, admission policy, lifecycle protocol, and concurrency proof allow a queue to transfer work without loss, duplication, reordering, unbounded retention, or stranded waiters?

## Why This Matters

Queues decouple producers from consumers in schedulers, services, device pipelines, event loops, storage engines, networks, and parallel programs. FIFO is often desirable because it preserves a simple admission order and supports reproducible reasoning. Yet a correct data-structure order is only one part of a useful work-transfer contract.

If producers can outrun consumers, the queue grows until resources fail unless capacity and admission semantics intervene. Blocking introduces cancellation and shutdown problems. Dropping changes delivery guarantees. Multiple consumers can finish out of order. Priorities and deadlines may intentionally override FIFO. Durable messaging adds persistence, acknowledgement, replay, and deduplication far beyond an in-memory queue.

The engineering task is to keep those layers separate: prove queue order, choose a representation, define bounded behavior, specify lifecycle, and add concurrency or durability only with their own evidence.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction functions, representation invariants, and transition proofs from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- failure guarantees, ownership, callbacks, cancellation, and observability from [DSE-003](003-operation-contracts.md);
- worst-case, amortized, allocation, memory, and latency costs from [DSE-004](004-time-space-and-allocation-cost.md);
- generic element and iterator contracts from [DSE-007](007-genericity-and-type-constraints.md) and [DSE-008](008-iterators-and-traversal-protocols.md);
- model testing and representative benchmarking from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- dynamic arrays, singly linked head/tail invariants, intrusive lifecycle, and bounded-stack policy from [DSE-012](012-dynamic-arrays-and-geometric-growth.md), [DSE-014](014-singly-linked-lists.md), [DSE-015](015-doubly-and-intrusive-linked-lists.md), and [DSE-016](016-stacks.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify enqueue, dequeue, peek, empty, and size as sequence transitions;
2. prove FIFO order for arbitrary successful enqueue histories;
3. distinguish accepted order from arrival, wakeup, scheduling, and completion order;
4. implement linked, array-offset, ring, segmented, and persistent queue representations;
5. design explicit empty/full, capacity, byte-budget, and backpressure contracts;
6. specify blocking, timeout, cancellation, close, drain, and shutdown behavior;
7. analyze lifetime, retention, iterator, bulk, and serialization consequences;
8. test order, exact boundaries, failures, waiters, and overload with a model oracle;
9. measure throughput, latency, memory, fairness, and queue-depth dynamics honestly;
10. identify linearization, memory-ordering, ABA, helping, and reclamation obligations for concurrent queues.

## Core Exposition

**Define front and back once.** The abstract sequence is written in dequeue order. Enqueue appends at back; dequeue removes index zero. C++ `queue` adapts an underlying container supporting `front`, `back`, `push_back`, and `pop_front`. Rust documents the ordinary `VecDeque` queue pattern as `push_back` plus `pop_front`. Naming endpoints avoids a common implementation bug: appending at one end and removing from that same end implements a stack.

The minimal Queue ADT need not expose random access, arbitrary removal, iteration, or the underlying container. Restricting those operations protects FIFO reasoning and permits representation changes. If cancellation-by-identity or inspection is required, add it explicitly with complexity and ordering effects.

**Empty results are an API decision.** Dequeue and peek have no value at depth zero. Option/result types preserve the element domain; exception/precondition forms are also possible. A special null result is unambiguous only if null elements are prohibited. Java `Queue` and `BlockingQueue` deliberately pair exception and special-value forms and prohibit null in blocking queues.

C++ adaptor `pop` does not return the element, so callers inspect front before removal under the exact precondition. Rust `VecDeque::pop_front` returns an option. A portable explanation must not merge these into a universal operation signature.

**Linked queues need both endpoints.** State `(head,tail,n)` reaches an acyclic chain whose values equal Q. Empty requires `head=tail=null` and n zero. Enqueue constructs a detached node. If empty, publish it as both head and tail; otherwise set old tail's next then move tail. Dequeue saves head's value and successor, advances head, decrements n, and clears tail when the removed node was last before reclamation.

The link work is constant, but allocation, element construction/return, reclamation, and callbacks are separate. A missing tail makes enqueue linear. Forgetting to clear tail at the singleton boundary leaves a dangling/stale endpoint. Publication order and failure rollback follow the same ownership principles as earlier linked modules.

**Naive array dequeue shifts too much.** Storing Q in a dynamic array and erasing index zero moves all remaining elements, so each dequeue is linear. Maintaining a head offset avoids shifts: dequeue increments head, and enqueue appends. But consumed prefix storage can retain references and grow dead space. Periodic compaction moves live elements and creates latency; thresholds need amortized and retention analysis.

A circular buffer reuses prefix capacity by wrapping head/tail indices, giving bounded constant index work. It introduces full-versus-empty disambiguation, modular arithmetic, wraparound, live-slot lifetime, and contiguous-span issues developed in DSE-019. A segmented deque offers endpoint operations while distributing allocation. Representation choice depends on capacity, growth, locality, stability, and failure needs.

**FIFO is an accepted-history theorem.** For one accepted enqueue x, it becomes the only newest back element; earlier existing elements remain before it. Inductively, enqueue `x_(k+1)` places it after every previously accepted remaining element. Dequeues remove from front, so the accepted sequence is returned in order unless another defined operation removes elements.

Concurrent FIFO applies to a legal linearization of overlapping operations. Two enqueues that do not overlap have real-time order; overlapping enqueues may be linearized in either order if the API permits. Request timestamp, lock arrival, thread wakeup, and method return order do not automatically define the abstract order.

Multiple consumers can dequeue A then B but finish processing B first. A FIFO queue does not imply FIFO completion, equal service, starvation freedom, deadline ordering, or fair scheduling. Those require separate dispatcher and workload contracts.

**Capacity is product semantics.** A capacity can constrain element count, retained bytes, cost/weight, or multiple dimensions. Ten queued 20 MB buffers differ from ten integers. Every enqueue must use checked accounting and define when reserved/in-flight memory counts.

Full behavior can:

- reject immediately with no effect;
- wait until space is available;
- wait up to a deadline;
- drop newest or oldest;
- coalesce equivalent work;
- spill to a governed durable tier;
- fail/close the stream.

Only the first three preserve every accepted element without replacing another; even then producer retry can duplicate unless identity semantics exist. Drop/coalesce policies create different abstract structures and must surface metrics and caller-visible outcomes.

“Unbounded” library queues mean no intrinsic small capacity, not infinite resources. Heap, integer, process, cgroup, and system limits remain. Production admission needs a deliberate maximum or a justified external bound.

**Backpressure requires a path to the producer.** A blocking or awaited enqueue can slow an upstream producer. A synchronous event callback that cannot wait cannot magically propagate backpressure; it must reject, drop, coalesce, detach, or accumulate elsewhere. The contract should identify who waits, which scheduler/thread is blocked, how cancellation interrupts, and whether holding other locks can deadlock.

Timeout distinguishes no admission from unknown admission only if the operation's linearization/cancellation semantics are precise. If cancellation races with newly available space, define which outcome wins and whether the element can still appear. Retrying after an ambiguous result needs an idempotency key or duplicate tolerance.

**Close is not an empty marker.** A queue can be open-empty, open-nonempty, closed-with-buffered-elements, or closed-drained. A robust close contract answers:

1. are new enqueues rejected;
2. do buffered elements remain dequeuable;
3. what does dequeue return once drained;
4. how are waiting producers and consumers awakened;
5. is close idempotent and who owns it;
6. what happens on producer crash or consumer abandonment?

A poison-pill element collides with data unless typed separately, requires enough pills or rebroadcast behavior for multiple consumers, can sit behind ordinary work, and can be lost with dropping policies. Java `BlockingQueue` explicitly does not intrinsically define close/shutdown. Build lifecycle above it rather than assuming a sentinel solves termination.

**Bulk operations expand failure surfaces.** Enqueueing a range can be atomic, all-or-nothing, or accept a prefix; order must match repeated enqueue. Dequeue/drain can return up to k in FIFO order and must define output allocation failure and concurrent arrivals. Java notes that bulk collection operations need not be atomic across implementations.

Draining can reduce synchronization overhead but let one consumer monopolize work. Batch size affects latency and fairness. Moving values into an output container can fail after queue removal in some models; a transaction or result protocol must state ownership at each point.

**Retention follows physical storage.** Dequeue should release or clear the physical reference when required so consumed objects do not remain reachable. Array-offset and ring representations must clear vacated slots. Linked queues retire nodes. Persistent queues can retain old versions. Metrics, traces, dead-letter storage, retries, and in-flight consumers create additional copies.

Logical dequeue is not secure erasure. Sensitive payloads may persist in allocator blocks, old buffers, logs, swap, dumps, or durable tiers. Capacity and retention policies should classify payloads and use platform-appropriate erasure where required.

**Iteration is a snapshot contract, not FIFO proof.** A sequential read-only iterator can yield front-to-back current elements. Mutation may invalidate it, expose a snapshot, or produce weakly consistent results. Concurrent collection iterators often do not freeze one instant. Do not use iteration to infer a dequeue history unless the library guarantees that relation.

Serialization chooses front-to-back order, validates declared counts/bytes, and records version/type. Restoring a linked queue by repeated head insertion reverses order; use tail append or reverse once. Persistence adds atomic file/database commit, acknowledgement, replay, and crash recovery—separate from in-memory FIFO.

**Concurrency needs algorithm-specific proof.** A single mutex can make enqueue/dequeue linearizable, with condition variables for not-empty/not-full. Correct waiting uses a predicate loop because wakeups can be spurious or another waiter can win. Shutdown/cancellation must wake and recheck. Holding application locks while blocking can create cycles.

Michael and Scott's classic work presents a nonblocking linked queue and a two-lock queue where enqueue and dequeue can proceed concurrently. The algorithms use a dummy node and exact atomic/helping/reclamation premises. Copying a diagram without memory-order and safe-reuse reasoning is not an implementation.

Lock-free does not mean wait-free or starvation-free. Compare-and-swap retries can starve one operation while system-wide progress continues. ABA and reclaimed node reuse threaten correctness. Garbage collection can simplify reclamation but not ordering, publication, capacity accounting, or shutdown.

**Evidence includes dynamics, not only operation speed.** Model-test sequential transitions against a simple list. Generate empty/singleton/full/wrap boundaries, repeated values, capacity bytes, allocation/return failure, bulk partial acceptance, cancelled/expired offers, close states, multiple producers/consumers, and stale iterators.

For blocking queues, use controlled waiters and prove wakeup predicates, interruption, timeout races, and close. For concurrent queues, collect histories and check linearizability where practical; use race/memory tools, forced node reuse, stress, stalled participants, and overload. Finite stress is evidence, not a proof of all schedules.

Measure queue-depth distribution, arrival and service rates, offered/accepted/rejected/dropped counts, enqueue wait, time-in-queue, service completion, throughput, latency tails, memory/bytes, allocation, contention, retries, and shutdown drain. A fast empty-queue microbenchmark does not characterize overload or fairness.

The following standard-library Python model uses a capacity-three linked queue with explicit offer and underflow results. Python manages memory, so it validates FIFO topology and metadata only.

<!-- bijux-verify: {"id":"bounded-linked-queue-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dequeue_order=A,B,C,D\ncapacity=3\noverflow_rejected=True\nunderflow_rejected=True\nhead_tail_cleared=True\ninvariant=True\nevidence=finite_bounded_queue_trace\n","stderr":""}} -->
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class BoundedQueue:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("negative capacity")
        self.capacity = capacity
        self.head = None
        self.tail = None
        self.size = 0

    def offer(self, value):
        if self.size == self.capacity:
            return False
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1
        return True

    def poll(self):
        if self.head is None:
            return (False, None)
        node = self.head
        self.head = node.next
        self.size -= 1
        if self.head is None:
            self.tail = None
        node.next = None
        return (True, node.value)

    def invariant(self):
        count = 0
        current = self.head
        last = None
        while current is not None:
            count += 1
            last = current
            current = current.next
            if count > self.capacity:
                return False
        return (
            count == self.size
            and 0 <= self.size <= self.capacity
            and ((self.size == 0) == (self.head is None and self.tail is None))
            and (self.size == 0 or (last is self.tail and self.tail.next is None))
        )


queue = BoundedQueue(3)
assert queue.offer("A") and queue.offer("B")
ok, first = queue.poll()
assert ok and first == "A"
assert queue.offer("C") and queue.offer("D")
overflow_rejected = not queue.offer("E")

removed = [first]
while True:
    ok, value = queue.poll()
    if not ok:
        break
    removed.append(value)
underflow_rejected, _ = queue.poll()
underflow_rejected = not underflow_rejected

print(f"dequeue_order={','.join(removed)}")
print(f"capacity={queue.capacity}")
print(f"overflow_rejected={overflow_rejected}")
print(f"underflow_rejected={underflow_rejected}")
print(f"head_tail_cleared={queue.head is None and queue.tail is None}")
print(f"invariant={queue.invariant()}")
print("evidence=finite_bounded_queue_trace")
```

## Definitions and Notation

| Term or symbol | Meaning |
|---|---|
| `Q` | Abstract front-to-back sequence. |
| front/head | End from which dequeue removes. |
| back/tail | End at which enqueue inserts. |
| accepted enqueue | Admission that has taken effect in the abstract queue. |
| underflow | Dequeue/peek with no available element. |
| full | Admission cannot proceed under current capacity/resource state. |
| backpressure | Upstream-observable response to insufficient downstream capacity. |
| drain | Remove several available elements, usually in FIFO order. |
| close | Lifecycle transition restricting future admission and eventually terminating dequeue. |
| fairness | Property about participants/service, not implied by FIFO element order. |
| linearization point | Instant a concurrent operation takes abstract effect. |
| in flight | Removed from the queue but not yet completed/acknowledged by a consumer. |

Complexity counts core link/index work unless otherwise stated. Allocation, growth, callbacks, blocking, scheduling, retries, reclamation, persistence, and service time remain separate.

## Mechanisms, Invariants, or Proof Structure

**ADT proof.** Enqueue appends at back; dequeue removes front; peek leaves Q. Induction on accepted enqueues proves FIFO return order, subject to intervening removals and successful-operation premises.

**Linked proof.** Head reaches exactly n live nodes ending at tail; empty endpoints agree. Enqueue constructs before publication and updates both endpoints for empty. Dequeue advances head, clears tail on singleton, returns/reclaims under its failure/lifetime contract.

**Bounded proof.** Maintain `0<=n<=capacity` plus checked byte accounting. Full rejection leaves Q unchanged. Blocking admission does not become accepted until its defined linearization; timeout/cancellation races use explicit outcome precedence.

**Lifecycle proof.** State distinguishes open, closed-buffered, and closed-drained. Close rejects future admission, preserves or discards buffered work only as specified, wakes waiters, and yields one unambiguous terminal dequeue outcome.

**Cost conclusion.** Linked and ring representations can perform constant core enqueue/dequeue work; linked allocation and ring wrap/growth differ. Naive array front erase is linear; head-offset compaction is amortized with retention/latency consequences. Blocking/concurrent work includes scheduling and retry.

## Alternatives and Trade-Offs

- **Linked head/tail:** constant link work and stable nodes; per-node allocation/metadata and reclamation.
- **Naive contiguous array:** simplest storage; front dequeue shifts the suffix.
- **Head-offset array:** avoids per-dequeue shifts; consumed-prefix retention and periodic compaction.
- **Ring buffer:** bounded compact reuse and predictable index work; wrap/full/empty/lifetime invariants.
- **Segmented deque:** efficient endpoints with growth; block allocation and noncontiguous layout.
- **Unbounded versus bounded:** unbounded avoids immediate admission policy but risks resource exhaustion; bounded makes overload explicit.
- **Reject versus block/timeout:** reject preserves caller control and bounded wait; blocking provides backpressure with cancellation/deadlock/shutdown obligations.
- **Drop/coalesce/spill:** can control overload for appropriate domains; changes delivery/order/durability semantics.
- **Single lock versus two-lock/nonblocking:** single lock simplifies history; alternatives permit more concurrency with greater proof/reclamation complexity.
- **Strict FIFO versus priority/deadline/fair queue:** FIFO preserves admission order; other policies optimize domain goals and are different ADTs/schedulers.
- **In-memory versus durable messaging:** in-memory is low-latency/ephemeral; durable systems add persistence, acknowledgement, replay, deduplication, and distributed failure.

## Failure Modes and Misconceptions

1. **“Append and pop implement a queue.”** Removing from the appended end implements LIFO.
2. **“FIFO means first request wins.”** The contract orders accepted operations, especially under overlap.
3. **“FIFO means first completion.”** Consumers can execute at different speeds.
4. **“A capacity creates backpressure.”** Only a producer-visible reject/wait/drop/etc. policy does.
5. **“Unbounded means safe from full.”** Resource exhaustion remains.
6. **“Blocking is lossless.”** Cancellation, crash, shutdown, interruption, and retry semantics still matter.
7. **“Timeout proves non-admission.”** Only if the race/linearization contract says so.
8. **“One poison pill closes many consumers.”** It may terminate only one, collide with data, or be dropped.
9. **“Queue empty means processing complete.”** Elements can be in flight.
10. **“Head offset solves arrays completely.”** It can retain references/dead space and needs compaction.
11. **“Bulk drain is always fair.”** One consumer can monopolize batches.
12. **“Iteration shows one concurrent instant.”** Weakly consistent iterators may not.
13. **“Atomic endpoints make a queue lock-free.”** Publication, helping, ordering, ABA, and reclamation remain.
14. **“Lock-free means every operation finishes quickly.”** It usually guarantees system progress, not per-thread wait freedom.
15. **“Throughput proves overload safety.”** Depth, rejection, memory, and tail latency dynamics matter.
16. **“In-memory FIFO implies durable exactly-once delivery.”** Persistence and delivery protocols are separate systems.

## Worked Examples

### Example 1

Starting Q=`<A,B>`, enqueue C yields `<A,B,C>`; dequeue returns A and leaves `<B,C>`; peek returns B unchanged. Conclusion: front removal and back insertion define the orientation.

### Example 2

A linked singleton has head=tail=A. Dequeue saves A, sets head to null, and must also clear tail. Leaving tail=A creates an empty queue with a stale endpoint. Conclusion: singleton is the critical endpoint transition.

### Example 3

Repeatedly erasing index zero from a one-million-element dynamic array shifts nearly the entire suffix each time. A ring or head offset avoids those shifts. Conclusion: correctness does not establish constant dequeue cost.

### Example 4

A capacity-two queue holds A,B. Immediate offer C returns false and leaves A,B. A blocking put C waits; a drop-oldest policy would produce B,C. Conclusion: these policies have different abstract histories and caller outcomes.

### Example 5

Ten queued items can retain 200 MB if each payload is 20 MB. A count-only capacity of ten violates a 64 MB budget. Conclusion: resource admission can require both item and byte accounting.

### Example 6

Consumer 1 dequeues A, consumer 2 dequeues B, but B completes first. The queue is FIFO and the service is not FIFO-completion. Conclusion: order layers must be reported separately.

### Example 7

A timed offer races with a dequeue that frees space. If offer linearizes first, timeout means no C; if successful publication wins, the caller must learn success. An ambiguous timeout followed by retry can duplicate C. Conclusion: deadline races need exact outcomes and idempotency.

### Example 8

Closing with A,B buffered rejects C, wakes blocked producers, lets consumers receive A then B, and then returns closed-drained. Conclusion: close needs state beyond empty/nonempty.

### Example 9

A benchmark reports 10 million empty uncontended operations per second while production queues reach depth 100,000 and block producers. It omitted allocation, wait, depth, memory, and tail latency. Conclusion: queue dynamics are part of evidence.

### Example 10

A clinical work queue preserves FIFO in tests. That does not establish deadline prioritization, cancellation, duplicate/loss behavior, durable audit, failover, authorization, or clinical safety. Conclusion: a verified in-memory order is one component, not deployment certification.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns condition variables, linearizability, lock-free queues, memory ordering, ABA, and reclamation.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns allocation, ring indices, object lifetime, wait primitives, interrupts, and I/O buffering.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops BFS, worklists, amortized compaction, scheduling policies, and evidence design.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns durable logs/queues, acknowledgement, replay, deduplication, partitions, and delivery guarantees.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) connects admission control, overload, shutdown, observability, SLOs, and capacity planning.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects run queues, device queues, wakeups, scheduling, memory pressure, and kernel concurrency.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns exhaustion, malicious payload size, stale references, retention, poisoning, and cross-tenant isolation.

## References

1. ISO C++ working draft, [`queue`](https://eel.is/c%2B%2Bdraft/queue). Container-adaptor definition, required front/back operations, constructors, push/pop, size, and underlying-container policy.
2. ISO C++ working draft, [Container Adaptors: General](https://eel.is/c%2B%2Bdraft/container.adaptors.general). Adaptor ownership, underlying containers, allocators, and swap exception behavior.
3. Rust Project, [`VecDeque`](https://doc.rust-lang.org/std/collections/struct.VecDeque.html). Current growable ring representation, ordinary push-back/pop-front queue use, front-to-back iteration, and contiguous conversion.
4. Oracle, [Java SE 25 `Queue`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Queue.html). Paired exception/special-value operations, FIFO qualification, ordering, capacity, and null conventions.
5. Oracle, [Java SE 25 `BlockingQueue`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/BlockingQueue.html). Reject, special-value, block, timeout forms; capacity; atomicity; memory effects; and absence of intrinsic close.
6. Oracle, [Java SE 25 `ArrayBlockingQueue`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ArrayBlockingQueue.html). Bounded array queue, optional fairness policy, blocking operations, iteration, and bulk semantics.
7. Python Software Foundation, [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque). Endpoint operations, bounded `maxlen`, iteration, rotation, and documented thread-safe appends/pops.
8. Python Software Foundation, [`queue`](https://docs.python.org/3/library/queue.html). Thread-synchronized bounded/unbounded queue classes, blocking/timeouts, task tracking, shutdown, and non-reentrancy.
9. Maged M. Michael and Michael L. Scott, [Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms](https://www.cs.rochester.edu/~scott/papers/1996_PODC_queues.pdf). Primary PODC paper for nonblocking and two-lock linked queue algorithms and experimental context.
10. Go Project, [Go Language Specification: Channel Types](https://go.dev/ref/spec#Channel_types). FIFO channel communication, capacity, blocking, close, and receive semantics in its language-specific concurrent setting.

## Exercises

### Exercise 1

Specify the Queue ADT and prove FIFO for arbitrary successful enqueue operations and subsequent dequeues. State what the theorem does not order.

### Exercise 2

Design a linked head/tail queue and an array-offset queue. Prove endpoint/lifetime invariants and compare worst-case, amortized, retention, and allocation costs.

### Exercise 3

Specify a bounded blocking queue with timeout, cancellation, close, drain, item/byte capacity, and multiple consumers. Resolve every race outcome.

### Exercise 4

Design evidence comparing strict FIFO, priority, and deadline scheduling for a service where queued jobs have variable cost.

### Exercise 5

Prepare a verification plan for adopting a nonblocking linked queue with manual memory reclamation in a high-reliability runtime.

## Answers to the Exercises

### Answer 1

Q is a finite front-to-back sequence. Successful enqueue appends x; nonempty dequeue returns/removes first; nonempty peek returns first unchanged. By induction, each new accepted x is placed after all earlier accepted remaining elements, and front removals therefore return accepted elements in their abstract order. The theorem excludes failed/rejected/timed-out admissions, explicit cancellation/removal, and defines overlap only through the concurrent linearization contract. It does not imply request-arrival, thread wakeup, service start/completion, fairness, priority, deadlines, or durable delivery order.

### Answer 2

Linked state `(head,tail,n)` has an acyclic n-node chain ending at tail; empty iff both endpoints null. Enqueue constructs before linking and handles empty by setting both; dequeue safely establishes return, advances head, clears tail on singleton, and reclaims exactly the old head. Core links are constant but enqueue allocates and traversal/layout cost is noncontiguous. Array-offset state stores live `[h,len)`; dequeue clears h then increments it, enqueue appends. Core operations are constant until growth/compaction; growth and compaction are linear events, consumed prefixes can retain capacity/dead space, and observer invalidation must be stated. Ring/segmented alternatives avoid long-lived prefix at added invariant complexity.

### Answer 3

State open/closed plus ordered elements, item/byte usage, capacities, and wait sets. Offer rejects with no effect; put waits in a predicate loop for open-and-space; timed/cancelled offer succeeds only if publication linearizes before the winning timeout/cancel outcome. Close atomically rejects future admission, wakes all waiters, permits specified drain of existing elements, then returns one closed-drained result; it is idempotent. Take waits for nonempty-or-closed; interruption/cancellation removes waiter state without consuming unless dequeue already linearized. Drain preserves FIFO and defines maximum and atomicity. Multiple consumers receive FIFO elements but can finish out of order. Checked accounting releases bytes at the selected dequeue/in-flight/ack boundary.

### Answer 4

Specify goals: admission-order latency, deadline misses, starvation bounds, throughput, and cost weighting. Replay the same timestamped jobs with sizes/deadlines/priorities under each policy; include overload, long jobs ahead of short jobs, priority inversion, aging, cancellation, and burst/steady phases. Measure accepted/rejected/dropped counts, queue-time and completion tails by class, deadline misses, starvation, depth/bytes, CPU, and policy overhead. Validate each scheduler against a reference ordering and invariants. Strict FIFO is simplest/reproducible; priority or deadlines can improve target outcomes while requiring tie-breaking, aging, admission, and starvation policy. Select against declared service objectives, not one aggregate mean.

### Answer 5

Specify FIFO/overlap semantics, linearization points, progress, capacity, close, shutdown, and element ownership. Implement the exact published/derived algorithm under the target memory model; prove dummy-node transitions, helping, atomic ordering, ABA defense, and reclamation when threads stall. Keep the locked queue as a model. Use controlled history/linearizability checking, schedule exploration where feasible, forced node reuse, tag wrap, memory/race/undefined-behavior tools, allocation failure, empty contention, long stress, stalled reclamation, overload, cancellation, and shutdown. Measure retries, CPU, throughput, tails, memory retention, and fairness. Require named concurrency, runtime, allocator, reliability, security, safety, operations, and independent review; finite tests and the historical paper do not certify this implementation.
