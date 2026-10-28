---
module_id: CONPAR-001
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 1
title: Concurrency, Parallelism, and Asynchrony
status: complete
last_verified: 2026-08-28
---

# Concurrency, Parallelism, and Asynchrony

## One-Page Review

### Governing question

Which kind of overlap does a program need: independently progressing activities, simultaneous computation, or delayed completion without blocking the initiator?

### Essential definitions

- **Concurrency** is the composition of multiple activities whose lifetimes overlap and whose events may be interleaved or partially ordered.
- **Parallelism** is the simultaneous physical execution of multiple computations on distinct execution resources.
- **Asynchrony** separates initiation from completion: an operation may complete later, and its result is observed through a callback, future, event, channel, or continuation.
- A **task** is a unit of work with a lifecycle and result or completion condition; it is not necessarily a thread.
- A **schedule** selects an order and placement for enabled events subject to program constraints.
- A **dependency** orders two events; independent events are candidates for reordering or parallel execution.
- **Overlap** is observable coincidence in lifetime; it does not by itself prove simultaneous execution or speedup.

### Central model, mechanism, or theorem

Represent a computation by events (E) and a strict partial order (\prec) containing program-order and communication dependencies. A legal sequential schedule is a linear extension of this order. Events incomparable under (\prec) are concurrent in the model; an implementation may interleave them on one processor or execute them simultaneously on several processors.

An asynchronous operation splits one conceptual action into at least an initiation event and a later completion event:

\[
start(op)\prec complete(op)\prec consume(result).
\]

Asynchrony changes control flow and waiting; parallelism additionally requires overlapping execution on distinct resources.

### Critical invariants

- Concurrency, parallelism, and asynchrony are related but not synonyms.
- Per-activity order and communication dependencies must hold in every legal schedule.
- A correct concurrent program must tolerate every schedule allowed by its model, not only one observed run.
- Parallel execution cannot remove true dependencies.
- Asynchronous APIs do not make CPU work nonblocking if that work still runs on the caller's execution resource.
- More workers do not guarantee lower latency or higher throughput; overhead, contention, and bottlenecks remain.
- Completion, failure, cancellation, and ownership must all have explicit observers.

### Common failures

Typical failures include equating async with multithreading, equating threads with parallel speedup, assuming one-core execution cannot be concurrent, blocking an event loop with CPU work, spawning unbounded work, measuring overlap without a correctness oracle, ignoring cancellation, and treating one successful schedule as evidence for all schedules.

### Compact example

Two activities contain ordered events (A_1\prec A_2) and (B_1\prec B_2), with no cross-dependency. There are (\binom{4}{2}=6) legal interleavings on one sequential processor. Two processors may also run an (A) event and a (B) event simultaneously. The same concurrent structure admits both interleaved and parallel implementations.

### Connections

Retrieve [PLS-001's outcome and trace model](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). [CONPAR-002](../ROADMAP.md) distinguishes processes, threads, tasks, and fibers. Scheduling connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), while distributed partial orders connect to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

When work overlaps, what structure is logical, what execution is physical, and what completion protocol does the caller observe?

Concurrency is principally a program-structure problem: several activities exist during the same period and must coordinate. Parallelism is principally an execution-resource property: computations literally run at the same time. Asynchrony is principally a control-flow property: starting an operation does not require the initiating flow to wait synchronously for completion.

These dimensions can combine in many ways. A single-thread event loop runs many concurrent asynchronous operations but executes one callback at a time. A data-parallel kernel performs many arithmetic operations simultaneously, often with a synchronous boundary before and after. Several blocking threads can be concurrent and parallel without using an async syntax. Clear vocabulary prevents an API spelling from substituting for an execution model.

## Why This Matters

Design choices follow the dimension that solves the actual problem. A server with many waiting connections needs concurrency and bounded asynchronous waiting. A matrix calculation needs parallel computation and careful partitioning. A user interface needs asynchronous completion so slow I/O does not block event processing. A workflow may need concurrency for independent requests but no speedup claim at all.

Incorrect classification leads to predictable failures. CPU-heavy work placed directly in an event loop delays every other task. Thousands of threads can exhaust memory or scheduling capacity. Parallelizing a dependency chain adds overhead without creating independent work. Unbounded fan-out overloads the downstream system that was supposed to become faster.

## Prerequisites and Retrieval

You should understand functions, program execution, elapsed time, sequences, sets, and directed acyclic graphs. Retrieve these facts:

1. A partial order can leave two elements incomparable.
2. A total order places every pair in one order.
3. Correctness and performance are separate claims.
4. Throughput measures completed work per interval; latency measures time for one operation under a stated population and percentile.
5. A dependency graph permits an event only after all predecessors complete.

No threading or async API is assumed.

## Learning Objectives

After completing this module, you should be able to:

- distinguish concurrency, parallelism, and asynchrony in precise language;
- model activities as partially ordered events;
- enumerate small legal interleavings;
- identify whether a workload is waiting, computing, coordinating, or combining these;
- explain why an async function can still block progress;
- separate logical task structure from threads and processors;
- state correctness, cancellation, resource, and performance obligations for overlapping work;
- reject mechanism choices based only on syntax, worker count, or one benchmark run.

## Core Exposition

A sequential program supplies one primary order of actions. A concurrent program admits several activities and therefore several possible global orders consistent with each activity's local rules. Concurrency can arise from independent requests, background work, callbacks, operating-system signals, actors, or threads. The defining issue is composition and coordination, not how many cores the machine has.

Parallelism uses simultaneous execution resources: CPU cores, vector lanes, GPU execution units, or nodes. It seeks performance, capacity, or deadline goals by exploiting independent work. A parallel program still needs a logical ordering model: inputs must exist before consumers use them, partial results must be combined correctly, and barriers or messages impose dependencies.

Asynchrony separates request from result. A synchronous call transfers control until it returns or fails. An asynchronous initiation returns before the operation is complete; another mechanism later reports success, failure, or cancellation. This can prevent an execution resource from sitting idle during I/O. It does not erase the work, guarantee another thread, or guarantee concurrent progress if the runtime cannot resume it.

An event partial order unifies the concepts. Each activity contributes program-order edges. Communication contributes a send-before-receive edge. Starting a task precedes its completion; completion precedes consuming its result. A legal schedule respects every edge but chooses among currently incomparable events. Nondeterminism comes from those choices and from environmental completion order.

A **single-core interleaving** executes one event at each instant yet supports concurrent activities by switching among them. This improves responsiveness and resource use when activities wait. It does not reduce the total CPU work and can increase it through scheduling overhead.

A **parallel schedule** maps independent events to different resources over overlapping time intervals. Parallel execution is possible only where dependencies leave work available. Even then, coordination, data movement, imbalance, and contention can dominate. Speedup is an empirical claim under a named workload and environment, backed by a correctness oracle.

Asynchronous runtimes often use cooperative scheduling: a task runs until it reaches a suspension point or completes. If it performs a long CPU loop without yielding or offloading, other tasks cannot progress on that worker. Preemptive threads move the scheduling boundary into the runtime or operating system, but shared state and blocking remain correctness concerns.

Mechanism selection begins with questions, not brand names:

1. Which activities must overlap, and why?
2. Where are the true data and control dependencies?
3. Is the scarce resource CPU, I/O capacity, memory, a remote quota, or human-visible latency?
4. What bounds admissions and in-flight work?
5. How do success, failure, timeout, and cancellation propagate?
6. What result and trace constitute correctness?
7. Which measurements would establish improvement?

## Definitions and Notation

Let (E) be events and (\prec\subset E\times E) a strict partial order: irreflexive and transitive. If neither (e_1\prec e_2) nor (e_2\prec e_1), write (e_1\parallel_c e_2) for logical concurrency. This symbol does not assert physical simultaneous execution.

A schedule (\sigma=(e_1,\ldots,e_n)) is legal when it contains each selected event once and respects the order:

\[
e_i\prec e_j\Longrightarrow i<j.
\]

For two chains of lengths (m) and (n) with no cross-dependencies, the number of interleavings is

\[
\binom{m+n}{m}=\frac{(m+n)!}{m!n!}.
\]

Physical parallelism can be modeled by start and finish times (s(e),f(e)) and resource assignment (r(e)). Two events execute in parallel when their intervals overlap and (r(e_1)\ne r(e_2)).

An asynchronous operation has a handle or continuation (h) linking initiation to a later outcome:

\[
init(op)\to h,
\qquad
resolve(h,Outcome),
\qquad
await(h)\to Outcome.
\]

This notation describes a protocol, not a promise that `await` blocks a thread or that work runs elsewhere.

## Mechanisms, Invariants, or Proof Structure

**Order preservation.** Every schedule must preserve program-order and communication edges. Reordering independent events is allowed; reversing a dependency is not.

**Interleaving count.** Choose the (m) positions occupied by activity A among (m+n) positions. A's local order then fixes its events in those slots, and B's order fixes the rest. Therefore there are (\binom{m+n}{m}) schedules for two independent chains. This counts schedules, not processor executions or distinct observations.

**Dependency lower bound.** If (e_1\prec e_2\prec\cdots\prec e_k), those events cannot execute simultaneously with one another in any valid implementation. Extra processors cannot shorten their combined dependency-path work below the path's own execution requirement.

**Completion ownership.** Every initiated operation must have a defined owner responsible for observing completion, failure, or cancellation. Detached work without such an owner can outlive requests, leak resources, or hide failures.

**Bounded concurrency.** Admission capacity must be finite or governed by backpressure. The fact that an API can create a task cheaply does not imply that downstream connections, memory, or rate limits are unbounded.

**Correctness before speed.** A performance comparison uses the same semantic oracle on sequential and overlapping implementations. Faster wrong output, dropped cancellation, or duplicated effects is not speedup.

## Alternatives and Trade-Offs

**Sequential versus concurrent structure.** Sequential code is easier to reason about when overlap provides no user or resource benefit. Concurrency improves responsiveness and utilization but enlarges the schedule space.

**Blocking threads versus asynchronous tasks.** Threads let blocking-style code overlap but consume thread and stack resources and expose shared-memory hazards. Async tasks can represent many waiting operations compactly, but require suspension-aware libraries and must not monopolize workers.

**Shared memory versus message passing.** Shared memory makes communication direct but requires synchronization and visibility rules. Message passing makes transfer points explicit but adds queues, serialization, ownership, and ordering policies.

**Task parallelism versus data parallelism.** Task parallelism runs different operations whose dependencies form a graph. Data parallelism applies related operations across partitions. Both require adequate granularity and a correct combine rule.

**Latency versus throughput.** More in-flight work may increase throughput while worsening tail latency through queues and contention. Optimize the metric and population the service actually promises.

**Deterministic versus adaptive scheduling.** A deterministic scheduler improves replay and analysis. Adaptive scheduling may balance real workloads better. Correctness should not depend on one favorable adaptive choice.

## Failure Modes and Misconceptions

1. **Concurrency means two CPU cores.** Concurrent activities can interleave on one core.
2. **Parallelism means async syntax.** Synchronous vector or fork-join work can be physically parallel.
3. **`await` always yields immediately.** Work before a suspension point can monopolize the current worker.
4. **Threads guarantee CPU speedup.** Runtime locks, dependencies, contention, and workload size may prevent it.
5. **More tasks always improve throughput.** They can overload queues, memory, connections, or remote services.
6. **One correct run proves concurrent correctness.** It exercises one schedule and environment.
7. **Independent source statements are independent work.** Aliases, effects, and hidden dependencies may connect them.
8. **Completion order is initiation order.** Async operations can complete in another order unless the protocol constrains them.
9. **Cancellation is just an error message.** It is a protocol affecting ownership, cleanup, children, and externally committed effects.
10. **Performance proves architecture.** Measurements support a bounded workload claim, not a universal mechanism rule.

## Worked Examples

### Example 1

**Question:** How many schedules can interleave two two-event activities?

**Reasoning:** Preserve (A1\prec A2) and (B1\prec B2). The executable enumerator checks all permutations and keeps those satisfying both constraints.

<!-- bijux-verify: {"id":"two-chain-interleavings","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"A1 A2 B1 B2\nA1 B1 A2 B2\nA1 B1 B2 A2\nB1 A1 A2 B2\nB1 A1 B2 A2\nB1 B2 A1 A2\ncount: 6\n","stderr":""}} -->
```python
from itertools import permutations

events = ("A1", "A2", "B1", "B2")
legal = []
for schedule in permutations(events):
    if schedule.index("A1") < schedule.index("A2") and schedule.index("B1") < schedule.index("B2"):
        legal.append(schedule)

for schedule in sorted(legal):
    print(" ".join(schedule))
print("count:", len(legal))
```

**Conclusion:** Six legal sequential interleavings realize concurrency without physical parallelism.

### Example 2

**Question:** Can a one-thread event loop serve several network requests concurrently?

**Reasoning:** Request A initiates I/O and suspends; the loop advances B while A waits, then resumes A on completion. Their lifetimes overlap, but callbacks execute one at a time on that thread. Blocking the thread prevents all progress.

**Conclusion:** Concurrent asynchronous waiting needs neither simultaneous callback execution nor several threads.

### Example 3

**Question:** Is a vector addition parallel but not necessarily concurrent at the application level?

**Reasoning:** One application task issues an operation whose independent element additions run simultaneously across vector lanes. The caller may synchronously wait for the instruction or kernel boundary. There need not be multiple application task lifecycles.

**Conclusion:** Physical data parallelism can occur inside a synchronously observed computation.

### Example 4

**Question:** Do four blocking worker threads use four cores while waiting for disk?

**Reasoning:** Their request lifetimes are concurrent, but blocked workers execute no application instructions. The operating system may run ready threads in parallel when CPU work exists. Whether four cores are used depends on runnable work and runtime constraints, not thread count.

**Conclusion:** Thread concurrency and CPU parallelism are separate observations.

### Example 5

**Question:** Why can an `async` image transform freeze a service?

**Reasoning:** If the function performs a long CPU transform before any suspension, it occupies the event-loop worker. Other ready tasks wait despite async syntax. The work must be partitioned with cooperative yield points or moved to an appropriate bounded compute executor, then measured.

**Conclusion:** Async declaration does not make synchronous CPU work nonblocking.

### Example 6

**Question:** Which parts of processing four independent image tiles can run in parallel?

**Reasoning:** Reading shared metadata precedes tile transforms. The four transforms are incomparable if they read immutable inputs and write disjoint outputs. Final assembly depends on all four. Thus only the middle antichain is parallel; setup and assembly remain ordered.

**Conclusion:** Dependency structure, not desired worker count, reveals exploitable parallelism.

### Example 7

**Question:** Can two concurrent operations race even on one processor?

**Reasoning:** Suppose each logical increment reads counter 0 and later writes read-value plus one. A schedule can perform both reads before either write, then write 1 twice. No instructions execute simultaneously, yet the non-atomic compound operations interleave incorrectly.

**Conclusion:** Races concern allowed ordering and shared state, not only simultaneous hardware execution.

### Example 8

**Question:** Why is unbounded request fan-out unsafe?

**Reasoning:** Launching 10,000 asynchronous calls may be cheap for the caller but exceed socket, memory, rate, or downstream database capacity. Queuing increases tail latency and failures trigger retry amplification. A semaphore, worker pool, or backpressure protocol must encode an admission bound.

**Conclusion:** Asynchrony changes waiting representation; it does not create infinite capacity.

### Example 9

**Question:** What happens when one child of a concurrent search fails?

**Reasoning:** A design must decide whether siblings continue, are cancelled, or produce partial results; who awaits cleanup; and whether emitted effects can be undone. Ignoring the failed future hides an error and may leak work. Structured ownership ties child lifetime to a parent policy.

**Conclusion:** Failure and cancellation semantics are part of concurrency correctness.

### Example 10

**Question:** A parallel report is twice as fast but occasionally omits rows. Is it successful?

**Reasoning:** The benchmark lacks a correctness oracle. Compare canonical row sets, duplicates, ordering requirements, totals, and failure behavior before latency. Only runs producing an allowed report belong in the performance population; environment, input, warm-up, and percentiles must then be recorded.

**Conclusion:** Performance evidence is meaningful only for semantically valid outcomes under a stated workload.

## Cross-Program Connections

- **Operating Systems:** schedulers map runnable threads and processes to processors; this program owns language-level structure rather than scheduler implementation.
- **Distributed Systems:** partial order and message completion persist when activities lack shared memory and clocks.
- **Systems Programming:** runtimes, system calls, memory ownership, and process boundaries implement concurrency mechanisms.
- **Functional Programming:** immutable inputs and explicit effects reduce interference and expose parallel dependencies.
- **Algorithm Engineering:** dependency graphs, partitioning, granularity, and combine laws determine parallel opportunity.
- **Software Reliability Engineering:** admission control, queues, cancellation, retries, and tail latency shape production behavior.
- **Testing & Quality Engineering:** systematic schedulers and trace oracles explore more than one fortunate execution.
- **Performance Engineering:** throughput, latency, utilization, speedup, and efficiency require distinct experiments.

## References

- Maurice Herlihy, Nir Shavit, Victor Luchangco, and Michael Spear. [*The Art of Multiprocessor Programming*, 2nd ed.](https://www.educate.elsevier.com/book/details/9780124159501). Morgan Kaufmann/Elsevier, 2020, ISBN 9780124159501. Publisher record checked 2026-08-28.
- Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea. [*Java Concurrency in Practice*](https://www.pearson.com/en-us/subject-catalog/p/java-concurrency-in-practice/P200000009374). Addison-Wesley Professional, 2006, ISBN 9780321349606. Publisher record checked 2026-08-28.
- Andrew Gerrand. [“Concurrency is not parallelism.”](https://go.dev/blog/waza-talk) *The Go Blog*, 2013, presenting Rob Pike's Waza talk and slides. Official language-project record checked 2026-08-28.
- Leslie Lamport. [“Time, Clocks, and the Ordering of Events in a Distributed System.”](https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/) *Communications of the ACM* 21(7), 1978, pp. 558–565, DOI 10.1145/359545.359563. Author publication record checked 2026-08-28.
- C. A. R. Hoare. [“Communicating Sequential Processes.”](https://www.cs.ox.ac.uk/publications/publication8253-abstract.html) *Communications of the ACM* 21(8), 1978, pp. 666–677, DOI 10.1145/359576.359585. Oxford and ACM DOI metadata checked 2026-08-28.

## Exercises

### Exercise 1

Classify each situation as concurrent, parallel, asynchronous, or a combination: a single-thread event loop with 500 open sockets; a synchronous GPU matrix multiplication; four blocking request threads on four cores; a callback scheduled after a timer; two coroutines that never overlap in lifetime.

### Exercise 2

Activities A and B contain three and two ordered events with no cross-dependencies. Derive the number of legal interleavings and list the reasoning, not all schedules. Then add dependency (A2\prec B2) and explain how you would count the remaining schedules.

### Exercise 3

A single-worker async service parses a request for 2 ms, performs 80 ms of CPU compression, awaits 20 ms of network I/O, and renders for 3 ms. Diagnose which segment blocks other tasks, propose a bounded design, and state correctness and performance evidence required before claiming improvement.

### Exercise 4

Compare a thread-per-request design, a single event loop, and a bounded task pool for 20,000 mostly waiting requests with occasional CPU-heavy validation. Discuss memory, scheduling, blocking compatibility, admission control, cancellation, and CPU placement without assuming one universally wins.

### Exercise 5

Design a concurrent price-aggregation request that queries five providers, requires any three valid replies, has a 150 ms deadline, and must not exceed 40 in-flight provider calls service-wide. Specify event dependencies, ownership, admission, timeout, cancellation, late replies, correctness oracle, and measurements.

## Answers to the Exercises

### Answer 1

The one-thread socket loop is concurrent and asynchronous but not executing callbacks in parallel. Synchronous GPU multiplication is physically parallel inside the operation but need not be asynchronous or expose several application tasks. Four blocking threads can be concurrent and parallel while runnable, though waiting threads are not computing. A timer callback is asynchronous because initiation and later completion are separated; it becomes concurrent with other work if lifetimes overlap. Coroutines whose lifetimes never overlap are sequential despite coroutine syntax.

### Answer 2

For independent chains of lengths 3 and 2, choose the three A positions among five, giving (\binom{5}{3}=10); local order fixes events within chosen positions. With (A2\prec B2), filter those ten linear extensions by requiring A2's position to precede B2's. A direct count can condition on B2's position or enumerate combinations of A positions; either method must still preserve A1 before A2 before A3 and B1 before B2. The added edge removes schedules in which B2 precedes A2 but does not impose an unnecessary total order on all events.

### Answer 3

On one cooperative worker, parsing and rendering occupy it briefly, while the 80 ms compression monopolizes it for the dominant interval; the network await releases it. Offload compression to a bounded compute pool or partition it only if the implementation supports safe yielding, keep an admission bound, and propagate cancellation across the handoff. Verify byte-for-byte or semantically canonical compressed output, errors, deadline behavior, cleanup, and no duplicate effects. Then measure request latency percentiles, throughput, queue delay, CPU utilization, and memory under a named workload; do not infer improvement from async syntax.

### Answer 4

Thread-per-request tolerates blocking libraries and simple control flow but risks large stacks, scheduling overhead, and shared-state hazards at 20,000 requests. A single event loop represents waiting compactly but any blocking call or CPU-heavy validation stalls all tasks unless offloaded. A bounded task pool controls concurrency and can isolate CPU work, but queued work needs deadlines and overload policy. All designs require finite admission, owned cancellation, result/error observation, and downstream limits. The selection depends on runtime costs, library behavior, CPU fraction, latency objectives, and measurements rather than a universal mechanism rule.

### Answer 5

The parent request starts after acquiring service-wide permits for at most the calls it can issue. Each provider has start, response/failure, validation, and completion events; validation follows response. The parent may return after any three valid results satisfy the aggregation rule, or fail at deadline or when three valid results become impossible. One owner tracks all children, releases permits exactly once, cancels or marks unnecessary calls, and safely discards late replies while still observing cleanup. The oracle checks provider identity, freshness, validation, aggregation rule, no permit excess, deadline classification, and no leaked children. Measurements include valid-result latency percentiles, provider and total in-flight counts, cancellation latency, late-reply rate, error mix, queue delay, and resource use under a declared provider-delay distribution.
