---
module_id: CONPAR-053
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 53
title: Lock-Free Queues
status: complete
last_verified: 2026-08-29
---

# Lock-Free Queues

## One-Page Review

### Governing question

How can a multi-producer, multi-consumer FIFO queue use a linked moving sentinel, separate head and tail atomics, and helping to remain linearizable and logically lock-free while preserving publication, payload ownership, reclamation, bounded resources, and shutdown?

### Essential definitions

- A **Michael–Scott queue** is a linked nonblocking FIFO with atomic head and tail references and an initial dummy/sentinel node.
- The **sentinel** is the node referenced by head; its successor, if any, contains the next logical queue value.
- **Enqueue linearizes** when CAS changes the observed last node's `next` from null to the new node.
- The **tail reference is advisory**: it may lag behind the actual last linked node without changing the abstract queue.
- **Helping** advances a lagging tail so a paused enqueuer is not required for system progress.
- **Dequeue linearizes** when CAS advances head from the old sentinel to its successor; the old sentinel becomes retired.
- **Empty observation** requires a validated state in which head equals tail and the observed head successor is null.
- A **moving sentinel** means the successfully dequeued value's node becomes the new head/sentinel representation.
- **Protection** prevents head, tail, and successor nodes from being reclaimed while an operation reads or compares them.
- **Logical FIFO order** follows successful link CAS events, not producer invocation, tail swing, allocation, or response order.

### Central model, mechanism, or theorem

Enqueue initializes private node `n` with null next, protects/validates tail `t`, and reads `t.next`. If next is null, successful `CAS(t.next,null,n)` links and linearizes the enqueue; advancing tail to `n` is optional helping. If next is non-null, tail lags and any caller may advance it. Dequeue protects/validates head `h`, tail `t`, and `next=h.next`. If `h=t` with null next, it returns empty; if `h=t` with non-null next, it helps tail. Otherwise successful `CAS(head,h,next)` linearizes dequeue of `next`'s payload and retires old sentinel `h`. Correct lifetime, value extraction, ordering, and reclamation remain language-specific proof obligations.

### Critical invariants

Head and tail reference nodes on one finite acyclic initialized chain; tail never precedes head and may lag the last node. Exactly one reachable null-next node is the physical last node. The abstract queue is the payload sequence after head. Published next links never change. One link CAS admits one value at the FIFO rear; one head CAS removes one front value. Failed CAS commits nothing and refreshes every derivative. Every dereferenced node is protected and revalidated. Each old sentinel retires once; no node/payload is reclaimed, reused, moved, or destroyed while a stale observer can access it. Close, empty, cancellation, allocation failure, and capacity exhaustion remain distinct. Shutdown waits for operation/reclaimer quiescence.

### Common failures

Code linearizes enqueue at tail advancement; declares empty merely because head equals tail while head.next is non-null; waits for the original producer instead of helping; reads next/value before protecting nodes; frees the old sentinel immediately; moves the successor payload while other dequeuers can still inspect it; retries using stale head/tail/next; lets tail move backward; publishes an uninitialized node with relaxed ordering; ignores ABA and address reuse; calls a blocking allocator/reclaimer lock-free; adds a separate count/close flag without an atomic state protocol; or treats a nonblocking FIFO as a bounded backpressure channel.

### Compact example

Enqueue A links A and advances tail. Enqueue B links B, which already completes the abstract enqueue. A helper advances tail before the original B producer's advisory tail CAS, so that CAS fails harmlessly. Dequeue removes A; enqueue C links/advances; dequeue removes B, leaving C. FIFO results are A then B; one failed tail CAS changes no abstract state; all A/B/C values remain accounted.

### Connections

[Thread-Safe Queues](017-thread-safe-queues.md) supplies FIFO/lifecycle semantics. [Compare-and-Swap Loops](026-compare-and-swap-loops.md) supplies retry rules. [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md) supplies reclamation foundations. Later modules isolate ABA, hazard pointers, epochs, proof, and contention management.

## Governing Question

How should engineers derive, implement, verify, and operate a linked lock-free FIFO so its two-root helping protocol remains correct under real language memory, allocation, payload, reclamation, close, and failure behavior?

The queue is not a stack with a tail added: its moving-sentinel and lagging-tail states are essential parts of both safety and progress.

## Why This Matters

Concurrent queues connect producers and consumers in schedulers, runtimes, storage engines, telemetry paths, and message systems. A blocked lock owner can halt all participants, motivating nonblocking designs. FIFO also creates more shared structure than a Treiber stack: enqueue modifies the last node's next while dequeue advances head, and tail is permitted to lag so a producer can pause after linking without blocking later operations.

That design demonstrates helping. The abstract value becomes queued before the advisory tail catches up. Any thread seeing the intermediate state completes the pointer housekeeping. This tolerance is subtle: treating head-equals-tail as empty without inspecting next loses a linked value; treating tail swing as enqueue commitment can make a completed value invisible in the proof.

The compact pseudocode assumes garbage collection or safe reclamation. In a manual-memory implementation, operations can observe head, tail, and successor while competitors retire nodes. Protecting one pointer may not be enough. The value stored in the successor becomes the new sentinel after dequeue, so copying, moving, and destruction need an explicit representation protocol.

## Prerequisites and Retrieval

Retrieve:

- FIFO capacity, ownership, close, and wake semantics from [Thread-Safe Queues](017-thread-safe-queues.md);
- CAS witness refresh from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- publication ordering from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- weak-memory audit from [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- backpressure from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md);
- progress quantifiers from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md); and
- lifetime/ABA foundations from [Implementing a Lock-Free Stack](052-implementing-a-lock-free-stack.md).

Retrieval prompt: draw `head=tail=A`, `A.next=B`, identify why B is already enqueued, and give the correct action for a dequeuer before it may decide empty.

## Learning Objectives

After completing this module, a learner can:

1. specify linked FIFO and moving-sentinel representation invariants;
2. distinguish enqueue link linearization from advisory tail advancement;
3. derive dequeue, empty, and lagging-tail cases from a validated snapshot;
4. explain how helping preserves progress after a producer pauses;
5. place protection and revalidation before every pointer dereference;
6. specify payload extraction and old-sentinel retirement without races;
7. audit ABA, reclamation, allocation, and target atomics in the progress claim;
8. design boundedness, close, cancellation, wakeup, drain, and shutdown as separate protocols;
9. verify FIFO histories, memory lifetime, helping, and weak-memory behavior; and
10. compare linked MPMC queues with mutex queues, bounded rings, channels, batching, and mature libraries.

## Core Exposition

### Abstract FIFO and linked representation

The abstract queue stores finite sequence `Q`. `enqueue(v)` changes `Q` to `Q·v`; `dequeue()` changes nonempty `v·R` to `R` and returns `v`; dequeue on empty returns empty. Concurrent results must correspond to one legal sequential order respecting nonoverlapping real-time precedence.

The physical chain starts at atomic head and ends at the unique reachable node whose atomic next is null. Atomic tail references some reachable node between head and the last node, possibly the last itself. Initially one dummy node D has null next, and head=tail=D. The abstract values are stored in nodes strictly after head.

After a successful dequeue, head advances to its successor. That successor becomes the new sentinel even though its payload represents the dequeued value. Implementations must make that payload logically consumed exactly once while keeping the node structurally usable until a later dequeue retires it. Managed implementations can read/copy an immutable item; manual ownership implementations often need a carefully designed slot/state or defer destruction.

### Enqueue preparation and link

Allocate a private node N, initialize its payload, and set N.next=null. Read/protect tail T and observe next=T.next; then revalidate that T remains the relevant tail snapshot. If next is null, T appears physically last. Attempt `CAS(T.next,null,N)`.

Success on that link CAS linearizes enqueue. N is now reachable after every previously linked value, so FIFO order is determined. Release semantics on publication makes initialization visible to acquiring consumers. The enqueuer then attempts `CAS(tail,T,N)`, but this tail swing is optimization/cleanup: failure does not undo or fail the enqueue.

If the link CAS fails, another producer linked a node. Refresh T and next. N remains private and can be retried because it has never been shared. Avoid allocating a new node, logging a new logical operation, or repeating external effects on each retry.

### Lagging tail and helping

If an observer sees `T.next=N` non-null, T is not the physical last node. Some enqueue already linked N and therefore completed abstractly, even if its producer paused before swinging tail. The observer attempts to advance tail from T to N and retries. Any producer or consumer can help.

Tail may lag more than one node under repeated paused swings. Helpers advance it stepwise using validated next links. It must never be moved to an unrelated or preceding node. A failed tail CAS means someone else changed tail; it does not imply abstract failure.

Helping removes dependence on the linker resuming and is central to lock-free progress. It also means operation ownership differs from pointer-maintenance ownership: another thread can finish housekeeping for a completed enqueue.

### Dequeue snapshot and cases

Dequeue protects/reads H=head, T=tail, and N=H.next, then validates the snapshot according to the reclamation protocol. Three logical cases follow.

If H=T and N=null, no linked value follows the sentinel, so an appropriate validated observation linearizes empty dequeue. A concurrent enqueue may occur immediately later; empty is an instantaneous result.

If H=T and N is non-null, tail lags. The queue is not empty. Help `tail` toward N and retry. This intermediate state is the most important correction to naive double-ended reasoning.

If H differs from T, a successor should exist under the invariant. Protect N and obtain its payload under the representation's ownership rules. Attempt `CAS(head,H,N)`. Success linearizes dequeue of N's logical payload and makes old H retired. Failure changes no abstract state; release/refresh protections and recompute.

### Why head and tail need validation

Reading head, then tail, then next does not create one atomic multiword snapshot. CAS loops use validation to establish that the relationships used for a proposal still hold. If head changes, the successor/payload may no longer be the front. If tail changes, helping target may be stale. If a node is reclaimed, any validation after unprotected dereference is too late.

Hazard pointers might require multiple hazard slots for head, tail, and next plus read-publish-reread sequences. The exact minimal set depends on which pointers are dereferenced and the algorithm/reclaimer proof. Epoch protection can cover the whole operation, at the cost of delayed reclamation. Garbage collection preserves referenced objects but not ordering or algorithmic invariants.

Do not translate managed pseudocode to raw pointers mechanically. Memory lifetime is a refinement layer with new states and progress dependencies.

### Linearizability proof

Initially the sentinel chain represents empty. Successful link CAS changes exactly one null next into N, appending N after all previously linked nodes; it preserves a finite acyclic chain and linearizes enqueue. Tail changes preserve the chain and abstract sequence, so they have no abstract effect.

Successful head CAS moves the sentinel to its immediate successor and removes exactly the first abstract payload. Old head retirement occurs after linearization and does not change remaining FIFO order. A validated H=T/N=null observation corresponds to no node after head and linearizes empty. H=T/N non-null only helps and makes no abstract change.

Failed CAS events make no shared transition. Ordering successful link CAS and head CAS events plus empty observations gives a sequential FIFO history. A dequeue cannot remove N before N's link; among nodes, link order defines reachability order. Real-time order of nonoverlapping operations follows event times.

This proof assumes payload extraction agrees with moving-sentinel representation and every read is memory-safe. It is separate from liveness.

### Payload ownership is subtle

In a garbage-collected queue of immutable references, dequeue can read `N.item` before head CAS and return it only on success. Competing dequeuers may read the same immutable reference, but only the head-CAS winner returns it. The new head node remains reachable as sentinel until a later dequeue retires it.

In a language with move-only values, two contenders cannot both unsafely move from N before knowing the winner. Options include storing shared/immutable payload, placing payload in an atomic one-time-take slot after winning, designing node/value indirection, or using another established implementation technique. That technique requires its own linearization/destruction proof.

The old sentinel H, not N, becomes unlinked after head advances. Reclaiming H is safe only after stale head/tail observers are excluded. N cannot be freed merely because its payload was consumed; it is the new structural head.

### Lock-free progress

For enqueue, successful link CAS completes an operation; failed link CAS due to changed null next witnesses another enqueue link. Non-null next triggers bounded helping toward an already completed enqueue. For dequeue, successful head CAS completes; a failed head CAS witnesses another dequeue or relevant change; lagging-tail help advances physical state toward the last linked node.

With strong CAS or bounded-spurious assumptions and safe nonblocking protection, an infinite active retry history implies infinitely many successful links/head advances or bounded help progress leading to attempts—system-wide lock-free logical progress. One caller can starve, so the queue is not wait-free.

Allocation, target atomic fallback, hazard/epoch registration/scanning, garbage collector, value destruction, and backoff can weaken end-to-end progress. State “logical enqueue/dequeue kernel is lock-free after allocation under reclaimer R on targets X,” not an unsupported universal claim.

### Reclamation and ABA

Dequeuers retire old sentinels, while producers/consumers may still hold them as observed head/tail or follow their next. Immediate free is use-after-free. Reclamation must cover every observer and helper, not just dequeuers.

Address reuse can create ABA on head, tail, or next comparisons. Tags help only with atomic pair support and wrap bounds. Hazard pointers delay reuse of specifically protected nodes; epochs delay reuse until prior readers quiesce. Each must integrate with thread exit and shutdown.

A stalled epoch participant may let operations progress while retired sentinels accumulate without bound. Operational availability therefore needs a memory-retention policy in addition to logical lock-freedom. A blocking scan allocator can make the combined operation blocking.

### Memory ordering

The successful link CAS must release prior node payload/next initialization. Consumers/helpers that acquire the link can then read initialized fields. Head/tail observations and CAS orders must preserve the validation and structural transitions required by the language model. Failure orders are legal load orders and must support refreshed witnesses; they cannot be release-only.

Tail is advisory but its next dereference still needs safe publication and lifetime. Relaxed tail updates may be possible in a proven implementation; guessing relaxed everywhere because tail “does not matter” is unsafe. Sequential consistency does not repair reclamation, ABA, or payload ownership.

Validate source-language happens-before and pointer/provenance rules. Hardware coherence diagrams do not override undefined behavior. Target atomics must support pointer width/alignment and the promised progress.

### Boundedness and backpressure

The linked queue is generally unbounded until allocation fails. It offers no backpressure. A semaphore/count added outside enqueue can leak or overcommit when a thread pauses after reservation or link; head and count are not one transaction. Cancellation and close make that composition harder.

A bounded MPMC ring uses per-slot sequence/generation state and different proofs. A mutex plus bounded condition-variable queue may best provide blocking producer backpressure, wakeups, fairness, and simple shutdown. “Lock-free” should not override required capacity semantics.

If a product keeps linked MPMC, enforce a total node/byte budget using an integrated reservation protocol with exact release and failure recovery. Qualify its progress and ensure control/cancellation traffic cannot be starved behind data.

### Close, cancellation, and shutdown

The base algorithm has no close. A separate closed flag creates races: a producer may read open, then link after close. Decide whether such already-admitted sends are allowed. If close must exclude all later links, combine entry/close generations or use an operation registry/protocol whose linearization is provable.

Dequeue on closed-empty should differ from temporarily empty. Wait/wakeup is also not inherent; parking needs a lost-wakeup-safe sequence tied to state generations. A polling lock-free queue can waste energy.

Cancellation before link/head CAS can release private/protection state. After enqueue link, the value is queued even if tail swing did not happen; cancellation cannot report no effect. After dequeue head CAS, the value is owned by that operation and needs delivery/cleanup despite caller cancellation.

Shutdown closes admission, stops/wakes waiters, waits for operation entry quiescence, drains or destroys according to policy, reclaims all old sentinels/retired nodes, deregisters protectors, and releases the final sentinel. Head=tail alone is not quiescence.

### Performance and topology

Separate head and tail often reduce producer-consumer contention compared with one-root stack, but producers still contend on last.next/tail and consumers on head. Cache coherence, NUMA, allocation, reclaimer scanning, payload size, and lag/help rates matter. False sharing between head/tail metadata can couple paths.

Batch enqueue/dequeue can amortize atomics but changes latency, cancellation, and linearization. Segmented/ring queues reduce allocation. Relaxed FIFO variants can scale by allowing bounded reordering. Each changes semantics.

Measure throughput and latency distributions, CAS attempts/failures, tail-lag distance, help attempts/success, allocation, retired high-water, cache misses/coherence, fairness/starvation, energy, and close/drain time. Compare a mature lock-free library, optimized mutex queue, and bounded ring with identical product behavior.

### Verification strategy

Use a sequential FIFO oracle and a history checker. Enumerate empty/one/many values, concurrent producer order, two consumers on one node, last-node enqueue/dequeue, paused producer after link, multiple-node tail lag, and failed tail/head/link CAS. Linearization events—not response order—must yield the reference sequence.

Model protection/reclamation: pause observers at head/tail/next, retire old sentinel, force address reuse and tag wrap-adjacent states, and reject dereference after reclaim or duplicate payload take. Inject cancellation before/after both linearization points, allocation failure, close races, stalled participants, and shutdown.

Weak-memory tools inspect publication/validation. Sanitizers find some data races/use-after-free. Target checks verify atomic mappings. Stress with affinity, preemption, oversubscription, NUMA, producer/consumer ratios, skewed pauses, and long duration. Finite testing does not prove linearizability or lock-free progress universally; record model bounds and proof assumptions.

## Definitions and Notation

Let atomic references be `H` and `T`. `next(n)` is atomic and immutable after its null-to-node link. `Chain(H)` is the finite acyclic nodes reachable from H; `last(H)` has null next. Invariant: `T` is in `Chain(H)` and is H, last, or a predecessor of last. Abstract `Q` is payloads of nodes strictly after H in chain order.

Enqueue proposal is `CAS(next(t),null,n)`; success linearizes value admission. `CAS(T,t,n_or_next)` is advisory help. Dequeue proposal is `CAS(H,h,next(h))`; success linearizes removal. Validated `h=t` and `next(h)=null` linearizes empty.

Node states are private, reachable, sentinel, retired, protected, reclaimable, and reclaimed; sentinel is reachable. Let `L`, `D`, and `K` count successful links, dequeue head commits, and tail-help commits. Abstract queue length under completed structural events is `L-D`, subject to initial/close specification.

ABA is equality of a reused representation across an intervening chain history. Tagged `(pointer,generation)` comparisons require atomicity and no wrap while stale observations live.

## Mechanisms, Invariants, or Proof Structure

Audit a lock-free queue in this order:

1. define FIFO, empty, close, capacity, wait, cancellation, and terminal outcomes;
2. prove chain finiteness/acyclicity, unique null-next last, and tail reachability/lag bounds;
3. define sentinel and payload ownership, including move/copy/destructor behavior;
4. linearize enqueue at link CAS, dequeue at head CAS, and empty at validated null successor;
5. treat tail swings/help as representation-only transitions that cannot fail an admitted enqueue;
6. protect and revalidate every head, tail, successor, payload, and help dereference;
7. refresh all derived references after failed CAS or validation;
8. prove publication, ABA prevention, retirement, reclamation, and target atomic semantics;
9. scope lock-free progress through allocation, reclaimer, backoff, runtime, and cleanup;
10. integrate reservation, close, parking/wakeup, cancellation, drain, and shutdown without hidden races;
11. model-check FIFO histories plus lifetime/reuse under weak memory, then stress targets; and
12. benchmark against mutex, ring, channel, batch, and mature-library alternatives with identical semantics.

The executable model separates link commitment from advisory tail advancement and records FIFO/accounting.

<!-- bijux-verify: {"id":"michael-scott-abstract-history","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=['enqueue A links', 'tail advances to A', 'enqueue B links', 'helper advances tail to B', 'B enqueuer tail CAS fails harmlessly', 'dequeue A commits', 'enqueue C links', 'tail advances to C', 'dequeue B commits']\ndequeue_results=['A', 'B']\nfinal_queue=['C']\nlink_commits=3\nhead_commits=2\ntail_advances=3\ntail_cas_failures=1\nfifo_preserved=True\nall_values_accounted=True\n","stderr":""}} -->
```python
queue = []
events = []
dequeue_results = []
link_commits = 0
head_commits = 0
tail_advances = 0
tail_cas_failures = 0
tail = "sentinel"

def link(value):
    global link_commits
    queue.append(value)
    link_commits += 1
    events.append(f"enqueue {value} links")

def advance_tail(value, actor="tail"):
    global tail, tail_advances
    tail = value
    tail_advances += 1
    if actor == "helper":
        events.append(f"helper advances tail to {value}")
    else:
        events.append(f"tail advances to {value}")

def dequeue():
    global head_commits
    value = queue.pop(0)
    head_commits += 1
    dequeue_results.append(value)
    events.append(f"dequeue {value} commits")

link("A")
advance_tail("A")
link("B")
advance_tail("B", actor="helper")
tail_cas_failures += 1
events.append("B enqueuer tail CAS fails harmlessly")
dequeue()
link("C")
advance_tail("C")
dequeue()

print(f"events={events}")
print(f"dequeue_results={dequeue_results}")
print(f"final_queue={queue}")
print(f"link_commits={link_commits}")
print(f"head_commits={head_commits}")
print(f"tail_advances={tail_advances}")
print(f"tail_cas_failures={tail_cas_failures}")
print(f"fifo_preserved={dequeue_results == ['A', 'B']}")
print(f"all_values_accounted={dequeue_results + queue == ['A', 'B', 'C']}")
```

Limitations: this sequential list model stipulates links/head/tail events. It has no nodes, sentinel storage, atomics, threads, weak memory, protection, ABA, reclamation, allocation, payload moves, close, cancellation, backpressure, shutdown, or progress proof. It illustrates abstract commitment/helping only.

## Alternatives and Trade-Offs

- **Mutex/condition queue:** clear bounded capacity, fairness, close, and blocking wakeups; paused lock owner can block peers.
- **Michael–Scott linked MPMC:** independent ends and helping; allocation/reclamation/payload proofs are substantial.
- **Managed-runtime linked queue:** GC simplifies lifetime; collector/runtime and payload semantics still qualify progress.
- **Bounded MPMC ring:** no node allocation and hard capacity; per-slot generations, wrap, full/empty, and false-sharing proof.
- **SPSC ring:** smallest fast proof for one producer/consumer; invalid for cloneable MPMC roles.
- **Segmented queue:** amortizes allocation and reduces pointer chasing; segment lifecycle and indexing are more complex.
- **Elimination/combining queue:** reduces central contention; can change fairness/order or add helper descriptors.
- **Relaxed FIFO:** higher scalability through allowed reordering; unsuitable when strict global FIFO is semantic.
- **Batch operations:** amortize atomics; increase latency, retained ownership, and cancellation/failure scope.
- **Channel abstraction:** provides lifecycle/backpressure semantics; implementation progress and wakeups remain API-specific.
- **Never reclaim until shutdown:** simple finite-batch lifetime; memory grows with dequeues.
- **Mature library:** concentrates expert review; target, capacity, close, reclamation, and guarantees still require audit.

## Failure Modes and Misconceptions

1. **“Tail is the last node.”** It is permitted to lag; follow/help its next.
2. **“Enqueue commits when tail moves.”** The successful null-next link is the abstract admission.
3. **“Head equals tail means empty.”** Non-null head.next means tail lags and a value exists.
4. **“The dequeued successor can be freed.”** It becomes the new sentinel; old head is retired.
5. **“One protected pointer is enough.”** every dereferenced head/tail/next needs exact reclaimer coverage.
6. **“GC solves the queue.”** It addresses reclamation but not linearization, ordering, progress, close, or performance.
7. **“A linked queue provides backpressure.”** It is unbounded until allocation/budget failure unless capacity is integrated.
8. **“A count can be bolted on.”** count, link, cancellation, and recovery must form a coherent state protocol.
9. **“Lock-free means each producer is fair.”** an individual CAS loop can starve.
10. **“Stress proves MPMC correctness.”** weak memory, rare reuse, infinite progress, and lifecycle require stronger evidence.

## Worked Examples

### Example 1

Producer P links N after tail T with release CAS, then is descheduled. N is already FIFO-visible. Consumer observes head=tail=T and T.next=N, helps tail to N, retries, and dequeues N. No progress depends on P resuming.

### Example 2

P1 links A, P2 reads old tail and sees next A, helps tail, then links B after A. Although P2 may respond before P1, successful link order is A then B, so FIFO requires dequeues A then B. Invocation/response overlap permits that order.

### Example 3

C1 and C2 both protect head H and successor N/read its immutable payload. C1 advances head H-to-N and returns payload. C2's CAS fails and it returns nothing; it refreshes. A move-only representation cannot let both destructively move the payload before the winner is known.

### Example 4

Naive C reads H, P advances head and reclaims H, then C reads H.next. Protection must precede dereference and be validated against current head. Retirement of H waits until all head/tail observers exclude it; protecting N alone would not repair the H read.

### Example 5

An epoch participant pauses while holding a queue guard. Producers and consumers remain logically lock-free, but millions of old sentinels accumulate. The service adds memory admission, participant monitoring, controlled deregistration, and explicit reclamation-progress alerts instead of claiming bounded availability.

### Example 6

Producer cancellation arrives after link but before tail swing. The enqueue is committed and must return/record success or an outcome discoverable by stable operation ID. Freeing N or reporting “not queued” corrupts ownership. A helper may already have advanced tail.

### Example 7

A separate closed flag permits P to observe open, pause, close to return, then P links. If contract forbids this, operation entry and close need a generation/registry gate; if admitted-before-close pushes may finish, document that linearization and make drain wait for them.

### Example 8

A product needs capacity 1,000 and producers that sleep when full. A raw linked lock-free queue fails the requirement. A bounded channel with conserved slots and lost-wakeup-safe condition waiting can be more correct, efficient, and auditable even though it uses a mutex.

### Example 9

A bounded model explores two producers/consumers, paused linkers, tail lag of two, empty races, reuse, cancellation, and close. Histories record link/head CAS events for FIFO checking; lifetime monitors cover H/T/N; weak-memory tooling checks publication. Target stress then measures retries/help/reclamation.

### Example 10

A lock-free queue carries commands in an autonomous rail-signalling subsystem. Production requires named railway signalling/interlocking, control, embedded/atomic, real-time, functional-safety, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; hazard/requirements traceability; formal FIFO/lifetime/progress and target mapping review; worst-case time/memory/reclamation analysis; hardware-in-the-loop, contention, fault-injection, failover, recovery, environmental, and operational evidence; independent fail-safe interlocks; and signed residual-risk acceptance. This chapter supplies no deployment authorization.

## Cross-Program Connections

- **Algorithms:** FIFO histories, linked invariants, helping ranks, and relaxed alternatives define semantics.
- **Programming languages:** atomics, memory models, move/copy/destruct, GC, pointer provenance, and unsafe code shape proofs.
- **Operating systems:** scheduling, preemption, parking/wakeup, allocation, priorities, and thread exit affect service.
- **Computer architecture:** coherence on head/tail/next, NUMA, cache layout, and atomic widths affect cost/support.
- **Formal methods:** linearizability refinement, temporal progress, separation/lifetime logic, and model checking validate designs.
- **Memory management:** hazard, epoch, reference, GC, and quiescence protocols govern node reuse.
- **Distributed systems:** FIFO scope, close, duplication, and process failure differ fundamentally across address spaces.
- **Reliability/security:** cancellation, close, memory exhaustion, contention attacks, and cleanup govern availability.
- **Performance:** producer/consumer ratios, help, lag, retries, allocation, and retained memory decide value.
- **Safety engineering:** bounded time/space and independent physical safeguards exceed queue correctness.

## References

1. M. M. Michael and M. L. Scott. “Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms.” PODC, 1996. <https://doi.org/10.1145/248052.248106>.
2. University of Rochester Synchronization Group. “Pseudocode for Linked Non-Blocking Queue.” <https://www.cs.rochester.edu/research/synchronization/pseudocode/queues.html>.
3. M. P. Herlihy and J. M. Wing. “Linearizability: A Correctness Condition for Concurrent Objects.” ACM TOPLAS 12(3), 1990. <https://doi.org/10.1145/78969.78972>.
4. M. M. Michael. “Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects.” IEEE TPDS 15(6), 2004. <https://doi.org/10.1109/TPDS.2004.8>.
5. T. Brown. “Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way.” PODC, 2015. <https://doi.org/10.1145/2767386.2767436>.
6. A. Morrison and Y. Afek. “Fast Concurrent Queues for x86 Processors.” PPoPP, 2013. <https://doi.org/10.1145/2442516.2442527>.
7. ISO C++ Working Draft. “Atomic Operations Library.” <https://eel.is/c++draft/atomics>.
8. Oracle. “Java Platform API: ConcurrentLinkedQueue.” <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentLinkedQueue.html>.
9. Crossbeam Project. “SegQueue.” <https://docs.rs/crossbeam-queue/latest/crossbeam_queue/struct.SegQueue.html>.
10. Rust Project. “Atomic Types.” <https://doc.rust-lang.org/stable/core/sync/atomic/index.html>.

## Exercises

### Exercise 1

Prove the chain/tail invariants and linearization points for enqueue, dequeue, and empty; explain why every tail-only CAS is abstractly silent.

### Exercise 2

Give a complete head-equals-tail trace for truly empty and lagging-tail states. Specify protection, validation, helping, and retry for each.

### Exercise 3

Design safe payload extraction and reclamation for move-only values using either hazard pointers or epochs. Account for two competing consumers and the moving sentinel.

### Exercise 4

Add bounded capacity, close, blocking wait/wakeup, cancellation, and shutdown. Explain whether a Michael–Scott core remains the right product architecture and qualify progress.

### Exercise 5

A medical-device queue is FIFO-linearizable and meets average throughput. Explain why this is insufficient and enumerate required human evidence.

## Answers to the Exercises

### Answer 1

Initially H=T=D and D.next=null: one finite acyclic chain, T reachable, one null last, abstract empty. A successful `CAS(T.next,null,N)` replaces the unique observed last null link with initialized N/null, appending exactly one value and linearizing enqueue; failed link changes nothing. Tail CAS moves T forward along an existing chain, preserving chain and abstract payload sequence, hence is silent. Successful `CAS(H,H,N)` with N=old H.next moves sentinel one edge, removes exactly first abstract payload and linearizes dequeue; old H retires. Validated H=T and H.next=null has no post-head payload and linearizes empty. H=T with non-null next is lag only. Event order yields FIFO because links append and head advances one edge.

### Answer 2

Protect/read H, protect/read T as required, read/protect N=H.next, and revalidate H/current relationships before using them. True empty is stable H=T and N=null; return empty at the validated observation. Lag is H=T and N non-null: N's link already linearized enqueue, so attempt `CAS(T,T,N)` as help, release/refresh protection, and retry; never return empty. If validation fails at any point, clear/replace hazards or restart within epoch. Tail help failure is harmless because another helper/operation changed it. Exact number/order of hazard slots must cover every dereference.

### Answer 3

Represent each successor payload with a one-time extraction state that only the successful head-CAS dequeuer may claim, or an immutable/shared payload copied before CAS under the chosen language semantics. Both consumers protect H and N and may inspect non-destructively; only head-CAS winner marks/takes N's logical payload once. N remains structural new sentinel and is not reclaimed; old H is retired once. Hazards keep H/N alive through validation/CAS and scan before old-H free; epochs keep the operation pinned and reclaim H after grace. Prove memory publication, one-take transition, losers' no-move behavior, destructor context, ABA/reuse, thread exit, and reclaimer progress/space.

### Answer 4

Define permit/byte reservation before allocation/link, with one owner and exact return after dequeue/cancel; a paused reservation cannot permanently lose capacity, so helping/rollback or a lock may be needed. Define close admission: already registered enqueues either may finish or are excluded by one generation/registry protocol. Waiters use state generation plus predicate loop to avoid lost wakeups; dequeue distinguishes open-empty from closed-empty. Cancellation before linearization releases resources; after link/head CAS reports committed ownership. Shutdown closes, wakes, waits for admitted/in-flight operations, drains/discards, quiesces reclaimer, destroys final sentinel, and joins waiters. These blocking/lifecycle requirements often make a bounded mutex/channel or proven bounded ring preferable. Qualify the MS logical kernel separately from blocking admission/wakeup/reclamation.

### Answer 5

FIFO and mean throughput omit memory lifetime under rare schedules, target atomic fallback, reclaimer/space progress, worst-case latency, scheduler/preemption, overload, cancellation, faults, cybersecurity, safe downstream action, and alarm/operator behavior. Require named clinical/device-domain, embedded/hardware, real-time, functional-safety, software, cybersecurity, human-factors, quality, independent verification, operations, and regulatory reviewers; requirements/hazard traceability; formal memory/FIFO/progress and target/compiler review; worst-case time/resource/reclamation analysis; hardware-in-the-loop, saturation, delayed-reader/reuse, fault-injection, failover, recovery, environmental, usability, and clinical evidence; independent safe-state controls; and signed residual-risk acceptance. This answer is not medical authorization.
