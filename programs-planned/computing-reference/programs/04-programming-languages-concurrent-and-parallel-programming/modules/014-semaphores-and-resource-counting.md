---
module_id: CONPAR-014
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 14
title: Semaphores and Resource Counting
status: complete
last_verified: 2026-08-29
---

# Semaphores and Resource Counting

## One-Page Review

### Governing question

What does a semaphore permit represent, how is its count conserved across acquisition, use, failure, cancellation, and release, and when is that protocol more appropriate than mutex ownership or condition-predicate waiting?

### Essential definitions

- A **semaphore** is a synchronization primitive with a nonnegative permit count and atomic acquire/wait and release/post operations.
- A **counting semaphore** represents zero or more interchangeable permits; a **binary semaphore** has a logical capacity of one.
- **Acquire/P/down/wait** atomically takes a permit when available or waits/fails/times out according to the API.
- **Release/V/up/post** returns or creates a permit and may make a waiter eligible.
- A **permit** is logical authorization to consume one unit of bounded concurrency or resource capacity; it is not necessarily a physical resource.
- **Permit conservation** relates configured capacity, available permits, checked-out permits, and any explicit resizing state.
- A **permit leak** occurs when successful acquisition lacks a matching release; **permit inflation** occurs when release has no corresponding acquisition or authorized capacity increase.
- **Admission control** bounds simultaneous admitted work before scarce resources are consumed.
- **Bulk acquisition** atomically requests several permits where supported; repeated single acquisitions can hold-and-wait.
- **Fairness** constrains acquisition order under API-specific assumptions; mutual exclusion or capacity safety alone does not imply it.
- A **named/process-shared semaphore** can coordinate eligible processes according to platform lifecycle and storage rules.

### Central model, mechanism, or theorem

For fixed capacity (K), available permits (S) and checked-out permits (U) satisfy:

(0 <= S <= K), (0 <= U <= K), and (S + U = K).

A successful one-permit acquire transitions (S,U) to (S-1,U+1). A matching release transitions to (S+1,U-1). Failed, timed-out, or cancelled acquisition leaves the permit with the semaphore. Every exception or cancellation after success must transfer or release the checked-out permit exactly once. This conservation proof is separate from correctness of the physical resource protected by the permit.

### Critical invariants

The initial count equals usable capacity, not desired demand. Each successful acquire has one owned release obligation. Failed acquisition creates none. Release occurs exactly once on every terminal path. Non-owner release is allowed only when the protocol intentionally transfers the obligation. Available plus checked-out equals capacity unless resizing is explicit. Bulk requests do not partially leak. Fairness claims follow the exact API. Permit availability does not prove a resource is healthy. Destruction occurs only after no waiter or user can access the semaphore.

### Common failures

Teams initialize to worker count instead of resource capacity; acquire after allocating the scarce object; forget release on exceptions; release in both normal and cleanup paths; treat a binary semaphore as an ownership-checking mutex; post from unrelated code and inflate capacity; read the current value as a reliable admission decision; acquire several permits one at a time and deadlock; retry timed waits without one deadline; use a concurrency semaphore as a rate limiter; assume FIFO fairness; resize by arbitrary posts; or destroy/unlink while participants still depend on it.

### Compact example

A database has eight usable connections. An admission semaphore starts at eight. A request acquires one permit before taking a connection, then returns both through a scoped cleanup path. At any stable boundary, available permits plus checked-out connections equals eight. If request code posts twice, nine requests may enter for eight connections; if it forgets to post, capacity shrinks until the service stalls.

### Connections

[Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md) distinguishes remembered state from notification; [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md) supplies owner-based exclusion; [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies capacity and cleanup authority. The [program roadmap](../ROADMAP.md) next covers read-write locks, barriers, queues, lock ordering, and thread pools.

## Governing Question

How can engineers translate a finite capacity or event-counting requirement into semaphore permits, prove that permits neither leak nor multiply, integrate cancellation and failure, and avoid mistaking a count for ownership, health, rate, or fairness?

The reliable abstraction is not “a semaphore blocks.” It is a conserved accounting protocol whose atomic operations coordinate admission. Every successful acquisition creates an obligation, and every release must discharge a real obligation or implement a separately authorized capacity change.

## Why This Matters

Semaphores elegantly bound concurrent use of interchangeable capacity: database connections, file descriptors, GPU command slots, parallel requests, memory-heavy jobs, or downstream calls. Unlike a mutex, capacity may exceed one. Unlike a condition notification, a posted permit persists until consumed.

That persistence makes semaphores powerful and dangerous. A stray release changes future behavior rather than failing immediately. A leak gradually reduces capacity. A too-large initial count lets callers pass admission and block later at the real resource, defeating the bound. The semaphore and physical pool must tell the same accounting story.

Semaphores also express event handoff. A producer posts when one unit of work becomes available and a consumer waits before consuming it. Yet complex predicates, closure, priorities, and multiple resource classes can become opaque when encoded as several counts. A mutex and explicit state may be easier to prove.

Modern APIs differ. POSIX.1-2024 defines a nonnegative shareable semaphore abstraction and process-oriented facilities. Java SE 26 `Semaphore` supports permits, optional fairness, bulk operations, timed/try acquisition, and specified memory-consistency effects. Go's memory model shows a buffered channel idiom for bounding concurrent use, with channel-specific synchronization rules. Use the selected mechanism's actual contract.

## Prerequisites and Retrieval

Retrieve:

- invariant and conservation reasoning from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- ownership transfer, bounded capacity, backpressure, and terminal accounting from [Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md);
- mutex ownership, fairness, timeouts, and destruction from [Mutexes and Mutual Exclusion](012-mutexes-and-mutual-exclusion.md);
- predicate loops and remembered-state distinctions from [Condition Variables and Predicate Waiting](013-condition-variables-and-predicate-waiting.md);
- nonnegative integers, induction, queueing, partial orders, and exception-safe resource management; and
- practical knowledge of pools, quotas, cancellation, process sharing, and monotonic deadlines.

Retrieval prompt: capacity is three. Draw states (available, checked-out) from (3,0) through three acquires and three releases. Add a failed fourth acquire, one leaked permit, and one double release. Identify which transitions preserve conservation.

## Learning Objectives

After completing this module, a learner can:

1. define binary and counting semaphore state transitions and prove permit conservation;
2. distinguish semaphore permits from mutex ownership and condition notifications;
3. initialize permits from authoritative capacity and align them with a physical pool;
4. structure release obligations across success, exception, cancellation, and transfer;
5. design bulk acquisition without partial hold-and-wait or leakage;
6. evaluate blocking, try, timed, fair, process-shared, and channel-based variants;
7. diagnose permit leaks, inflation, starvation, oversubscription, and misleading value inspection;
8. test bounded histories and instrument capacity without claiming universal correctness; and
9. recognize safety-critical resource admission requiring named authorized review.

## Core Exposition

### Define what one permit means

Write a sentence: “One permit authorizes exactly one ___ until ___.” Examples:

- one active database request until the connection and transaction are returned;
- one in-flight GPU buffer until completion cleanup;
- one memory-heavy job until its reserved bytes are released;
- one producer item until a consumer accepts ownership; or
- one outstanding call until a terminal response.

If the blank contains heterogeneous quantities, one uniform semaphore may be wrong. A job using 10 MiB and one using 10 GiB should not both consume one memory permit unless another bound covers bytes. Use weighted permits, separate classes, or a budget allocator.

The count represents logical permission, not physical health. Eight permits with only seven healthy connections is inconsistent. Health changes require coordinated capacity adjustment and treatment of checked-out resources, not an unreviewed extra release or permanent acquire.

### Atomic state transitions

With available (S):

- acquire when (S>0) atomically decrements and returns success;
- acquire when (S=0) blocks, fails, or times out according to variant;
- release atomically increments subject to the maximum and may wake a waiter.

The atomicity prevents two callers consuming the same last permit. Reading a count and later acquiring is not equivalent. POSIX `sem_getvalue`-style observation, where available, is diagnostic and races immediately with other operations. Make decisions through acquire/try-acquire.

Some implementations conceptually hand a released permit directly to a waiter without making a positive count externally visible. The conservation abstraction still holds if waiter custody is modeled. Do not depend on internal queue/count sequencing.

### Conservation proof and obligation ownership

Initialize (S=K,U=0). Successful acquire changes by (-1,+1); release by (+1,-1). Induction preserves (S+U=K). The difficult part is mapping (U) to application obligations.

Represent each acquired permit by a scoped token/guard where possible. Construction occurs only after successful acquire. Dropping or closing the guard releases once. Transfer moves the guard, not a Boolean copy. Explicit `disarm` is reserved for a deliberate handoff to another owner.

Failure before acquire has no release obligation. Failure after acquire has one. This boundary must be obvious:

<!-- bijux-verify: {"id":"permit-guard-schema","mode":"schematic","language":"text","toolchain":"none","reason":"Language-neutral cleanup pseudocode illustrates permit ownership and is not directly executable."} -->
```text
permit = acquire()
try:
    resource = checkout()
    use(resource)
finally:
    return resource if obtained
    release permit
```

Place admission before scarce allocation. If checkout can fail because the pool is inconsistent, release the permit and report the health defect. If a physical resource is transferred elsewhere, transfer the permit obligation with it or redesign accounting.

### Mutex versus binary semaphore

A binary semaphore with count one can exclude entrants, but it does not necessarily track an owner. Another thread or signal handler may release under some APIs. Double release may inflate or error. Recursive semantics, owner-death handling, and priority protocols differ.

Use a mutex for “the current owner exclusively protects this invariant.” Use a semaphore for “there are K interchangeable permissions” or intentional cross-participant handoff. Do not choose a binary semaphore merely to work around an invalid mutex release.

### Semaphore versus condition variable

A semaphore count remembers posts. A condition notification does not; the protected predicate remembers state. Semaphores work well when each post corresponds to one independently consumable unit. Condition variables work well for arbitrary predicates over several fields.

Encoding a bounded queue with semaphores commonly uses:

- empty slots initialized to capacity;
- filled slots initialized to zero; and
- a mutex for buffer indices and representation.

Producer waits for empty, locks, inserts, unlocks, then posts filled. Consumer waits for filled, locks, removes, unlocks, then posts empty. Every failure boundary must restore the consumed count. Closure and cancellation require additional explicit state; counts alone do not naturally encode end-of-stream.

### Multi-permit acquisition

Some workloads consume several capacity units. An atomic bulk acquire either obtains all requested permits or none. Repeating single acquires can create hold-and-wait: A holds two of four waiting for one more while B holds two waiting for one more.

If the API lacks atomic bulk acquisition, use one budget allocator under a mutex/condition, impose rollback without livelock, or redesign request sizes. Validate request (0 < n <= K); an impossible request must fail rather than wait forever.

Bulk release must match the owned amount. A release count taken from untrusted input can inflate capacity. Store quantity in the permit token.

### Blocking, try, and timed variants

Blocking acquire is appropriate when work must wait and cancellation/shutdown can wake or interrupt it. Try-acquire implements optional work, immediate overload rejection, or fallback. Timed acquire gives a policy bound.

Use one monotonic deadline across retries. On failure or timeout, no permit was acquired unless the API reports otherwise. Never run cleanup that releases an unowned permit. When cancellation races with success, define whether the permit is returned immediately or transferred into cancellation cleanup.

Repeated immediate try can spin and starve. Queue admission, backoff, useful alternative work, or explicit rejection is better. Timeouts do not repair leaked permits or prove resource failure.

### Fairness and starvation

Capacity safety says at most (K) permits are checked out. It does not say which waiter succeeds. Unfair admission may let newcomers barge, improving throughput while starving old requests.

Java's fair semaphore option orders certain blocking acquisition points under documented qualifications; untimed try-acquire can bypass fairness. Bulk requests complicate head-of-line behavior: a large request at the front can block smaller ones even when some permits are free.

Choose policy from the service contract. FIFO improves bounded bypass but can convoy. Size-aware scheduling improves utilization but may starve large requests. Aging or separate classes can help. State assumptions and measure wait distributions, not only utilization.

### Memory synchronization

Permit operations can supply memory-order edges, but exact guarantees are API-specific. Java documents that actions before release happen-before actions after successful acquire in another thread. Go channel operations have specific synchronized-before relationships. POSIX semaphore memory synchronization follows its standard definitions.

This does not make arbitrary shared state safe. If multiple permit holders mutate one object concurrently, a semaphore of capacity greater than one permits races. Use a mutex, partition ownership, atomics, or an independently thread-safe resource.

### Cancellation, exceptions, and permit transfer

Acquire can be a cancellation point in some systems. Distinguish cancellation before success from after success. Install cleanup atomically with ownership where the language permits; otherwise carefully mask/defer cancellation across the small acquisition-to-handler window.

Once acquired, every exit releases exactly once. Exceptions inside resource checkout, task cancellation, timeout of later work, process shutdown, and callback failure all count. A cleanup stack or scoped guard makes this reviewable.

Cross-thread release can be intentional: producer acquires capacity and consumer releases after processing. Then message ownership includes the permit token. If the message is dropped or dead-lettered, cleanup releases. A producer must not also release after successful transfer.

### Rate, concurrency, and queue bounds

A semaphore bounds simultaneous in-flight work, not starts per second. Ten permits with one-millisecond jobs can admit roughly far more operations per second than ten permits with one-second jobs. Use a token bucket or paced scheduler for rate, and a semaphore for concurrency if both constraints matter.

A semaphore around work does not bound the upstream queue if callers accumulate while waiting. Acquire before accepting or materializing expensive work, or bound the wait queue separately. Otherwise memory and latency remain unbounded although active concurrency is safe.

### Resizing and degraded capacity

Capacity change is a protocol. Increasing by (d) can add authorized permits. Decreasing cannot simply delete permits already checked out. Options:

- stop granting until checked-out falls below the new limit;
- acquire and retain administrative permits;
- mark resources retiring and remove on return; or
- create a new generation and drain the old pool.

Serialize resize with admission, record target/current/retiring counts, and preserve (available + checked-out + retiring adjustments = configured accounting). Avoid negative logical availability hidden inside an API that forbids it.

### Process sharing and lifecycle

POSIX named or process-shared semaphores have creation, open, close, unlink, initialization, and destruction rules. Name lifetime and object lifetime can differ. Crash persistence is not a portable assumption. Permissions and namespace security matter.

For unnamed process-shared use, storage and attributes must be suitable and outlive all processes. An ordinary thread semaphore in private memory does not coordinate other processes.

Destroy only after no waiter, owner of a permit obligation, or potential accessor remains. A zero count may mean all permits checked out or waiters blocked; it does not prove quiescence.

### Observability

Record:

- configured, available if safely observable, checked-out, and retiring capacity;
- acquire success, immediate failure, timeout, interruption, and cancellation;
- wait time and queue age distributions;
- release count and detected overflow/double release;
- resource checkout failures after permit success;
- permit ownership duration and logical operation;
- fairness/bypass indicators; and
- shutdown/drain terminal accounting.

Instrument permit tokens rather than trusting a racy raw count. Reconcile semaphore metrics with physical-pool inventory. A discrepancy is an invariant violation requiring investigation, not a dashboard adjustment.

## Definitions and Notation

Let fixed capacity be (K), available permits (S), and checked-out multiset (U) whose cardinality is (|U|). Conservation is (S+|U|=K) with (0<=S<=K).

Acquire (a_t) succeeds only when it atomically transfers one or (n) permits from (S) to an obligation owned by (t). Release transfers an owned obligation back. Fairness order (prec_F) and wake policy are defined by the API, not by count safety.

Physical resources (R) may have health subset (H subseteq R). Correct alignment requires configured permits match admissible usable capacity under the pool protocol; semaphore conservation alone says nothing about (H).

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Define one permit.** Name unit, capacity source, and terminal release point.
2. **Initialize from authority.** Align logical permits with usable physical capacity.
3. **Model conservation.** Cover acquire, fail, timeout, transfer, release, resize, and shutdown.
4. **Represent obligations.** Use scoped, move-only permit tokens where possible.
5. **Place admission early.** Bound work before scarce allocation and queue growth.
6. **Specify variants.** Bulk, try, timed, fair, process-shared, and cancellation semantics.
7. **Protect separate state.** Do not use K permits as mutual exclusion for one mutable object.
8. **Handle failure.** Prevent leaks and double release on every exit.
9. **Reconcile and observe.** Compare permits, resources, waits, and terminal outcomes.
10. **Test adversarially.** Exhaustion, cancellation races, overflow, resize, crash, and destruction.

Maintain these invariants:

- available plus checked-out permits equals authorized capacity;
- each successful acquire creates exactly one quantified release obligation;
- failed acquisition creates no obligation;
- every obligation is released or explicitly transferred once;
- semaphore capacity matches usable resource accounting;
- multi-permit requests are all-or-none or safely rolled back;
- fairness and visibility claims follow the selected API;
- upstream queued work is separately bounded;
- resizing preserves accounting across generations; and
- no user or waiter exists at destruction.

## Alternatives and Trade-Offs

**Counting semaphores** compactly represent interchangeable capacity and remember unused authorization. They expose little domain state, so diagnosing which logical operation owns a leaked permit requires application-level tokens and telemetry.

**Mutexes** encode exclusive ownership and protect arbitrary invariants. A mutex is preferable when exactly one owner mutates shared representation; a semaphore is preferable when up to (K) independent users may proceed.

**Condition variables with explicit counters** make closure, resizing, weighted requests, priorities, and several predicates visible under one lock. They require more code but can be easier to prove than a web of semaphores.

**Bounded channels or queues** combine capacity with item ownership. They are often clearer for producer-consumer work because a received value identifies what was transferred. A bare semaphore transfers permission but no payload.

**Resource pools** can make checkout and logical admission one operation, preventing divergence between permit and resource counts. Their correctness still depends on return, health eviction, cancellation, and shutdown semantics.

**Token buckets** bound average start rate and bursts; semaphores bound simultaneous occupancy. Production systems commonly need both, applied in a documented order.

**Fair admission** can bound bypass for eligible waiters but reduces barging opportunities and may convoy. Unfair admission can improve throughput. Neither choice repairs leaked permits, slow holders, or an unbounded waiting queue.

**Bulk permits** model weighted demand but risk head-of-line blocking and fragmentation. Separate capacity classes or a budget scheduler may yield more predictable service when request sizes vary widely.

## Failure Modes and Misconceptions

- **“The initial count is desired parallelism.”** It must derive from authoritative usable capacity.
- **“A permit is the resource.”** It is authorization; pool health and identity require separate state.
- **“Binary semaphore means mutex.”** Ownership checks, priority protocols, recursion, and failure behavior can differ.
- **“Release is harmless.”** An unmatched release inflates future capacity and can violate physical limits.
- **“Cleanup always releases.”** Cleanup releases only after confirmed acquisition and exactly once.
- **“The raw value supports check-then-act.”** Observation races; use an atomic acquisition operation.
- **“Acquiring before use is enough.”** Admission must occur before scarce allocation and unbounded queueing.
- **“One-at-a-time weighted acquisition composes.”** Partial holdings can create hold-and-wait deadlock.
- **“Fair means perfectly FIFO.”** API qualifications, cancellation, bulk requests, and scheduling intervene.
- **“Semaphore bounds throughput.”** It bounds occupancy, not starts per time interval.
- **“Zero means idle.”** It can mean full utilization with waiters; lifecycle needs explicit quiescence.
- **“Posting repairs a stuck service.”** It can hide a leak by creating unauthorized capacity.
- **“Cancellation before return means no acquisition.”** A success-cancellation race follows the API contract and cleanup protocol.
- **“A passing history enumeration proves the implementation.”** It validates only the stated finite model.

## Worked Examples

### Example 1

**Question:** A pool exposes five healthy connections and a semaphore starts at eight. What fails?

**Reasoning:** The first five admitted callers check out connections; three more hold logical authorization but block at the real pool. The semaphore no longer bounds the scarce resource and can amplify queueing.

**Conclusion:** Initialize from usable physical capacity and reconcile health changes.

### Example 2

**Question:** Capacity is three. Starting from (S,U)=(3,0), two acquires, one release, and another acquire occur.

**Reasoning:** The states are (2,1), (1,2), (2,1), and (1,2). Every transition preserves (S+U=3).

**Conclusion:** Conservation proves the count bound for this trace, provided each element of (U) represents a real obligation.

### Example 3

**Question:** A timed acquire fails, but a generic finally block posts.

**Reasoning:** No permit moved into caller custody, so the post changes (S,U) from (K,0) to an unauthorized logical (K+1,-1) or triggers an overflow error.

**Conclusion:** Construct cleanup ownership only after confirmed acquisition.

### Example 4

**Question:** Four permits exist. Two jobs each acquire two and then request a third.

**Reasoning:** Both hold partial allocations; neither can obtain the remaining unit because none remains. Every holder waits for the other to release.

**Conclusion:** Use atomic bulk acquisition, rollback, or a serialized budget allocator.

### Example 5

**Question:** A producer acquires before enqueueing, while the consumer releases after processing.

**Reasoning:** The enqueue transfers both the work item and permit obligation. A failed enqueue must release locally; a successful enqueue forbids producer release. Consumer cleanup releases once even when processing fails.

**Conclusion:** Cross-thread release is valid when obligation transfer is explicit and terminal.

### Example 6

**Question:** Ten permits protect one unsynchronized map, and each admitted job writes it.

**Reasoning:** Capacity remains at ten, yet two writers can race because the semaphore intentionally admits multiple holders.

**Conclusion:** Permit safety does not imply representation safety; add ownership partitioning, a mutex, atomics, or a thread-safe map.

### Example 7

**Question:** Operators reduce capacity from eight to five while six permits are checked out.

**Reasoning:** Revoking an active holder is unsafe. Stop new grants, mark a target of five, and let returns reduce checked-out occupancy. Only after occupancy falls below five may availability become positive.

**Conclusion:** Decrease through draining or retirement, not arbitrary negative accounting.

### Example 8

**Question:** What does the executable model enumerate?

**Reasoning:** It generates all 90 order-preserving acquire/release histories for three labeled tasks. With capacity two, 54 never exceed two checked-out permits and 36 would demand a third.

**Conclusion:** The model recomputes the finite capacity boundary; it does not model schedulers, memory ordering, cancellation, or a library semaphore.

### Example 9

**Question:** An unfair semaphore shows high utilization but one request waits minutes.

**Reasoning:** Capacity conservation is intact while repeated barging violates the service's progress goal. Average latency conceals tail starvation.

**Conclusion:** Specify an admission policy and observe maximum age, percentiles, and bypass—not only utilization.

### Example 10

**Question:** May a four-permit gate approve simultaneous commands to aircraft hydraulic actuators?

**Reasoning:** Permit conservation cannot establish actuator independence, physical load limits, timing, redundancy, fault containment, certification, or safe degraded modes.

**Conclusion:** No. Named authorized aerospace systems, controls, hardware, real-time, functional-safety, verification, cybersecurity, and certification reviewers must approve the actual system. No external review is claimed.

The following finite executable check supplies deterministic numerical evidence for Example 8.

<!-- bijux-verify: {"id":"counting-semaphore-capacity-histories","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate_histories=90\ncapacity_safe_histories=54\nrejected_over_capacity=36\nmaximum_checked_out=2\n","stderr":""}} -->
```python
tasks = ("A", "B", "C")
histories = []


def extend(prefix, progress):
    if len(prefix) == 2 * len(tasks):
        histories.append(tuple(prefix))
        return
    for task in tasks:
        step = progress[task]
        if step < 2:
            progress[task] += 1
            event = "acquire" if step == 0 else "release"
            extend(prefix + [(task, event)], progress)
            progress[task] -= 1


extend([], {task: 0 for task in tasks})
safe = 0
rejected = 0
maximum = 0
for history in histories:
    checked_out = 0
    valid = True
    for _, event in history:
        checked_out += 1 if event == "acquire" else -1
        maximum = max(maximum, min(checked_out, 2))
        if checked_out > 2:
            valid = False
    safe += int(valid)
    rejected += int(not valid)

print(f"candidate_histories={len(histories)}")
print(f"capacity_safe_histories={safe}")
print(f"rejected_over_capacity={rejected}")
print(f"maximum_checked_out={maximum}")
```

Limitations: the program enumerates a small sequential event model with per-task order. It does not execute concurrent threads, implement a semaphore, establish memory-order guarantees, explore cancellation, or prove arbitrary programs correct.

## Cross-Program Connections

- **Programming languages:** scoped cleanup, cancellation, ownership types, and memory models determine how permit obligations compose.
- **Operating systems:** wait queues, scheduling, process-shared objects, signals, and destruction implement blocking semantics.
- **Algorithms and data structures:** bounded queues, pools, weighted budgets, and invariant proofs connect counts to representation.
- **Distributed systems:** local semaphores do not survive partitions or coordinate replicas; leases and durable consensus-backed quotas address different failure models.
- **Cloud and platform engineering:** connection limits, worker pools, admission control, bulkheads, and load shedding use permit-like accounting.
- **Security and safety:** resource exhaustion is an availability risk, while safety-critical capacity requires domain hazard analysis beyond synchronization.

## References

1. Edsger W. Dijkstra, “Cooperating Sequential Processes,” EWD123, 1965, [E. W. Dijkstra Archive](https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html).
2. Edsger W. Dijkstra, *A Discipline of Programming*, Prentice-Hall, 1976.
3. IEEE and The Open Group, *POSIX.1-2024*, §4.20 “Semaphores,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html) (retrieved 2026-08-29).
4. IEEE and The Open Group, *POSIX.1-2024*, “sem_wait, sem_timedwait,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/sem_wait.html) (retrieved 2026-08-29).
5. IEEE and The Open Group, *POSIX.1-2024*, “sem_post,” [official specification](https://pubs.opengroup.org/onlinepubs/9799919799/functions/sem_post.html) (retrieved 2026-08-29).
6. Oracle, “Semaphore,” Java SE 26 API, [official API](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/Semaphore.html) (retrieved 2026-08-29).
7. The Go Authors, “The Go Memory Model,” version of 2022-06-06, [official specification](https://go.dev/ref/mem) (retrieved 2026-08-29).
8. Allen B. Downey, *The Little Book of Semaphores*, second edition, Green Tea Press, 2016, [author-hosted book](https://greenteapress.com/wp/semaphores/).
9. David R. Butenhof, *Programming with POSIX Threads*, Addison-Wesley, 1997.
10. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.

## Exercises

### Exercise 1

Define a permit and state the fixed-capacity invariant for a six-connection pool. Trace two successes, one failed try-acquire while four other permits are already owned, and one release.

### Exercise 2

Prove by induction that successful one-permit acquire and owned release preserve (S+U=K). Explain why unmatched release lies outside the legal transition system.

### Exercise 3

Diagnose a service that has eight permits, seven healthy resources, an unbounded request queue, and cleanup that posts after every acquisition attempt. Give a repair order.

### Exercise 4

Design admission for jobs requiring one, two, or four units from capacity eight. Compare atomic bulk permits, repeated acquisition, separate classes, and a mutex-protected weighted budget.

### Exercise 5

A medical infusion platform proposes a semaphore to limit simultaneous pump commands. State what this chapter's verification can establish and what requires named authorized human review.

## Answers to the Exercises

### Answer 1

One permit authorizes checkout and use of one healthy connection until that connection is returned or retired through the pool protocol. With (K=6), maintain (0<=S,U<=6) and (S+U=6). If four other permits are owned, the state is (2,4). Two successful acquires yield (1,5) then (0,6). A try-acquire now fails and leaves (0,6); it creates no cleanup obligation. One owned release yields (1,5). The trace says nothing about connection health unless pool inventory is reconciled separately.

### Answer 2

Base case: initialization gives (S,U)=(K,0), hence (S+U=K). Inductive acquire step assumes conservation and (S>0), then (S-1)+(U+1)=S+U=K. Inductive release assumes a real owned obligation (U>0), then (S+1)+(U-1)=K. Bounds follow from those preconditions. An unmatched release has no element to remove from (U); it invents capacity, so it is not a legal release transition. Capacity increase must instead be a separately authorized resize transition with its own invariant.

### Answer 3

First stop unconditional cleanup: release only a token produced by confirmed acquisition. Next reconcile logical and physical capacity, normally draining or retiring the eighth permit until eight healthy resources truly exist. Move acquisition before accepting or materializing expensive work, and independently bound the wait queue with rejection, backpressure, cancellation, and one monotonic deadline. Add scoped tokens, double-release detection, resource-health accounting, wait-age metrics, and shutdown reconciliation. Do not post merely to restore apparent throughput; find every leaked or inflated transition.

### Answer 4

Atomic bulk acquisition is safe and compact when the API offers all-or-none requests, but four-unit requests can block smaller ones under FIFO. Repeated acquisition is unacceptable without rollback because two jobs can hold partial units and deadlock. Separate one-, two-, and four-unit classes improve isolation but can strand capacity and require an allocation policy across classes. A weighted budget under one mutex and condition makes available units, queue order, cancellation, resizing, and aging explicit; it is more code but usually easiest to prove. Reject requests above eight, preserve one absolute deadline, grant atomically, and return the recorded weight exactly once.

### Answer 5

The chapter's checks can validate a finite permit-count model, front matter and structure, snippet output, citations, local links, exercise correspondence, and reasoning that every successful acquisition owns one release. They cannot establish pump independence, dosage limits, command timing, sensor validity, physical response, fail-safe behavior, clinical hazards, cybersecurity controls, regulatory compliance, or deployment suitability. Named authorized medical-device clinical, systems, controls, hardware, real-time, functional-safety, software verification, cybersecurity, human-factors, quality, and regulatory reviewers must approve those claims and the real implementation. This chapter claims no external review.
