---
module_id: DSE-066
program: Data Structures Engineering
level: 2
module_number: 66
title: Michael-Scott Queues
status: complete
last_verified: 2026-08-30
---

# Michael-Scott Queues

## One-Page Review

### Governing question

How does the Michael–Scott linked queue turn two independently lagging atomic pointers into a linearizable lock-free FIFO, and what memory-order, reclamation, capacity, lifecycle, and verification obligations remain outside its compact pseudocode?

### Essential definitions

- A **FIFO queue** returns items in enqueue order, subject to a legal ordering of overlapping operations.
- A **dummy** or **sentinel node** is the node at `Head`; it carries no abstract queue item.
- `Head` identifies the current dummy. Its successor, if any, carries the oldest item.
- `Tail` is an optimization pointer on the live chain. In the original algorithm it is the last or second-to-last node and may lag after publication.
- **helping** means one operation performs an auxiliary pointer advance needed by another operation.
- A **linearization point** is the indivisible event where an operation takes abstract effect.
- **lock-free** means system-wide progress: in an infinite execution with active operations, operations keep completing; one participant may starve.
- **retirement** removes a node from the reachable representation; **reclamation** later permits its storage to be reused.
- **ABA** is an equality illusion caused when a compared representation changes away and back while an observer is delayed.

### Central model, mechanism, or theorem

The concrete queue is one singly linked chain beginning at the dummy. Enqueue initializes a private node, finds a live node whose `next` is null, and CAS-links the new node there. That link CAS—not the later `Tail` swing—linearizes enqueue. Dequeue takes a consistent `Head`, `Tail`, and `Head.next` observation. If `Head == Tail` and `next == null`, it returns empty at that observation. If `Head == Tail` but `next != null`, `Tail` lags; the dequeuer helps it forward and retries. Otherwise, successful CAS of `Head` to `next` linearizes dequeue; the successor becomes the new dummy and supplies the returned value.

Assuming atomic transitions, safe publication, a lifetime-safe dereference window, no harmful ABA, and correct reclamation, the link order is FIFO and each successful head swing removes exactly the oldest reachable item. A failed structural CAS or invalidated snapshot usually witnesses another successful transition. Repeated interference therefore implies system progress, not bounded per-operation latency.

### Critical invariants

1. `Head` and `Tail` always identify nodes in one finite acyclic live chain.
2. `Head` is the first live node and is always a dummy.
3. Abstract items are exactly the payloads strictly after `Head`, in link order.
4. Reachable `next` links change only once, from null to one successor.
5. An enqueue becomes visible only at its successful null-to-node link CAS.
6. A dequeue removes one item only at its successful `Head` CAS.
7. `Tail` never precedes `Head`; under the original algorithm it is last or second-to-last.
8. `Head == Tail` is empty only when the consistent `Head.next` observation is null.
9. Private initialization is published before consumers read payload or `next`.
10. No node is reclaimed or reused while any operation can still dereference an old observation.

### Common failures

- Treating `Tail` as the authoritative membership boundary.
- Declaring empty from `Head == Tail` without inspecting `Head.next`.
- Linearizing enqueue at the best-effort `Tail` swing.
- Mutating a reachable link or linking one node twice.
- Reading payload after a head swing when another dequeuer may reclaim the node.
- Freeing the old dummy immediately without a reclamation protocol.
- Assuming sequential consistency prevents ABA or use-after-free.
- Calling lock-free wait-free, fair, bounded, or fast under every workload.
- Adding exact `size`, capacity, close, waiting, or bulk operations without a composed proof.
- Benchmarking the CAS core while excluding allocation and retired-memory pressure.

### Compact example

Enqueuer E1 links A after dummy 0 and pauses before moving `Tail`. A dequeuer observes `Head == Tail == 0` but `0.next == A`, so it helps `Tail` to A instead of reporting empty. E2 links B after A and also leaves `Tail` behind. The dequeuer swings `Head` from 0 to A and returns A; a later dequeuer helps `Tail` to B, swings `Head` from A to B, and returns B. B is now the dummy. Two link CAS operations and two head CAS operations preserve FIFO despite both delayed tail swings.

### Connections

[DSE-017](017-queues.md) supplies the sequential FIFO contract. [DSE-062](062-fine-grained-locking.md) supplies linearization and lifetime framing. [DSE-065](065-lock-free-stack-structure-and-invariants.md) supplies CAS, publication, progress, and reclamation prerequisites. The [program roadmap](../ROADMAP.md) next develops ABA avoidance, hazard pointers, epochs, and reclamation testing.

## Governing Question

Can a dummy node, a monotone linked chain, and helping CAS loops implement a production-credible linearizable lock-free multi-producer/multi-consumer FIFO once memory visibility, ABA, reclamation, overload, lifecycle, and evidence boundaries are explicit?

## Why This Matters

Queues coordinate schedulers, runtimes, event loops, storage engines, telemetry paths, executors, and network stacks. A single mutex around a sequential queue is often the right baseline, but a preempted holder can block every participant. Michael and Scott's 1996 algorithm is a foundational nonblocking alternative: enqueuers and dequeuers can make progress through different ends of a linked chain, while helping repairs a deliberately weak tail invariant.

The algorithm is valuable because it separates abstract truth from navigation hints. Membership is established by a successful link CAS. `Tail` may be stale without making the abstract queue stale. This pattern recurs in nonblocking structures: allow bounded representation lag, make every observer recognize it, and make repair optional for the operation that created the lag but available to others.

The short algorithm is not a complete library queue. Its original presentation assumes counted pointers and a compatible allocator/reuse scheme. Modern implementations may rely on garbage collection, hazard pointers, epochs, tagged pointers, or specialized ownership. Each choice changes which pointers can be dereferenced, when old dummies can be reused, and whether the lock-free claim includes reclamation. Memory ordering must also publish node initialization through the link and make a consumer's observations coherent under the target language.

An unbounded lock-free queue can still fail operationally: producers can outrun consumers until memory exhaustion, a participant can starve, a stalled epoch can retain retired nodes, and one hot tail region can generate coherence traffic. Backpressure, waiting, close, cancellation, fairness, exact size, iteration, and destruction are separate protocols. Production engineering therefore couples the core safety proof with lifecycle design and workload evidence.

## Prerequisites and Retrieval

Retrieve [DSE-017](017-queues.md): abstract sequence `Q`, enqueue appending, dequeue removing the oldest item, and empty behavior. Retrieve singly linked lists, atomic compare-and-exchange, release/acquire publication, linearizability, lock-free versus wait-free progress, ABA, allocator lifetime, and finite history reasoning.

From [DSE-061](061-thread-safe-wrappers-and-coarse-grained-locks.md), retrieve the correct mutex baseline. From [DSE-062](062-fine-grained-locking.md), retrieve operation-specific linearization and logical-versus-physical deletion. From [DSE-065](065-lock-free-stack-structure-and-invariants.md), retrieve CAS retry, publication, ABA, and reclamation proof boundaries. The repository verifier deliberately excludes runtime threading primitives, so this chapter's executable artifact is a bounded transition model, not evidence about real atomics or scheduler interleavings.

## Learning Objectives

After completing this module, you can:

1. derive the Michael–Scott representation from a sequential FIFO specification;
2. explain why the permanent dummy removes empty/singleton special-case mutation;
3. locate enqueue, dequeue, and empty linearization points;
4. distinguish the authoritative link structure from a lagging `Tail` hint;
5. prove connectivity, FIFO order, head, tail, and ownership invariants;
6. explain helping and the scope of the lock-free progress argument;
7. derive publication and consumption requirements under a target memory model;
8. diagnose ABA, use-after-free, and unsafe payload-read schedules;
9. design capacity, waiting, shutdown, observation, and reclamation boundaries; and
10. construct layered functional, history, memory, progress, and performance evidence.

## Core Exposition

**Start from the sequential object.** Let abstract state be finite sequence `Q=<q_0,...,q_{n-1}>`. `enqueue(x)` changes it to `Q·<x>`. A successful `dequeue()` on nonempty `Q` returns `q_0` and changes state to the suffix; on empty it returns an absence result unchanged. Decide whether null is a value, whether dequeue waits, whether capacity is bounded, and what close means before selecting a representation.

**Keep one permanent structural node.** Initialize a node `d` with `d.next=null`, then set `Head=Tail=d`. `Head` denotes a dummy, never an abstract element. If `Head.next` is node A, A is the oldest item. When A is dequeued, `Head` advances to A; A's payload has been returned and A becomes the new dummy. Thus the implementation does not remove the item node itself during that dequeue—it removes the old dummy from the live prefix and changes the role of A.

This role transfer eliminates a delicate empty-to-nonempty split update. Enqueue always appends after an existing node. Dequeue always advances from an existing dummy. At least one node remains in the live chain until object destruction.

**Derive enqueue.** Allocate a private node `n`, initialize its payload, and set `n.next=null`. Repeatedly:

1. load `tail=Tail` and `next=tail.next`;
2. validate that `tail` still equals `Tail` before relying on the pair;
3. if `next` is null, CAS `tail.next` from null to `n`;
4. on successful link, enqueue has completed abstractly; best-effort CAS `Tail` from `tail` to `n` and return;
5. if `next` is nonnull, `Tail` lags, so help CAS `Tail` from `tail` to `next` and retry.

Only one contender can change a given terminal `next` from null. Its successful link CAS appends after all previously linked nodes and is enqueue's linearization point. The `Tail` swing is navigation maintenance. If the enqueuer pauses after linking, every other operation can discover the link and advance `Tail`; completed enqueue does not depend on its creator resuming.

**Derive dequeue.** Repeatedly load `head=Head`, `tail=Tail`, and `next=head.next`, then validate `head` still equals `Head`. If `head==tail`, inspect `next`. Null means no payload follows the dummy, so return empty at that consistent observation. Nonnull means an enqueue linked a node but `Tail` has not caught up; help `Tail` toward `next` and retry. If `head!=tail`, a successor should exist. Protect `next` under the reclamation protocol, read its payload at the safe point required by the implementation, and CAS `Head` from `head` to `next`. Success linearizes dequeue. Retire old `head`; do not reclaim it until no observer can dereference it.

Why read the successor value before the head CAS in the original pseudocode? After another dequeuer advances `Head` again, the node holding that value may become an old dummy eligible for reclamation. A late unprotected read can be use-after-free. Reading early is necessary in that memory-management setting but is not sufficient: `head`, `tail`, and `next` themselves also need lifetime protection compatible with concurrent removal and reuse.

**Prove FIFO order.** Every successful link CAS changes exactly one terminal null link to a private node. Because reachable nonnull links never change, these successes create a total chain order. Place each enqueue at its link CAS. A successful dequeue changes `Head` only to its immediate successor, so it removes the first payload after the prior dummy. Place it at the head CAS. It therefore returns enqueued nodes in link order. A qualifying empty observation sees a dummy with no successor and can be placed at that read. These points lie between invocation and response and preserve the order of nonoverlapping calls.

**Understand consistent observations.** Separate atomic loads are not one hardware snapshot. The validation reread prevents combining an old `head` with a successor observed after `Head` changed. Similarly, enqueue verifies `Tail` before acting on `tail.next`. On invalidation, discard the local reasoning and retry. Equality alone is meaningful only if ABA/lifetime rules guarantee that the representation denotes the same logical node incarnation.

**Treat `Tail` as a bounded hint.** In the original algorithm, `Tail` is the last or second-to-last live node. A link CAS can make it lag by one. Before another append can link farther, its traversal/help step advances `Tail`; hence the bound. Some production descendants use more relaxed self-linking or traversal schemes, so their invariants must be read from their own implementation rather than imported mechanically.

The state `Head==Tail && Head.next!=null` is not contradictory. It is the precise publication window after an enqueue's link CAS and before tail repair. Reporting empty from pointer equality would erase a completed enqueue. Helping closes the window without waiting for the paused enqueuer.

**Establish publication.** All fields of `n` are initialized while private. The successful link CAS must have release semantics, or participate in an equivalent synchronization chain. A dequeuer or helper that follows that link needs an acquire path before consuming payload and next. Head/tail maintenance orders may sometimes be weaker because they are hints, but the exact proof depends on which acquire observes which release and on the reclamation protocol. Use the target language's official atomic rules; sequential consistency is a conservative starting point, not a lifetime solution.

**Prove only the progress actually obtained.** In the abstract strong-CAS algorithm, a failed link CAS means another enqueuer appended there. A failed head CAS or invalidated head means another dequeuer advanced. Seeing nonnull `tail.next` means an enqueue linked; helping advances a finite lag unless another operation moved the target. Persistent interference therefore entails successful system transitions. If a participant runs alone from a current state, it completes after bounded local repair. This is lock-freedom, not wait-freedom or starvation freedom.

Weak CAS may fail spuriously; progress then depends on the primitive's guarantees and loop. Allocation may block, throw, or exhaust memory. Hazard scanning and epoch quiescence can delay reuse. Callbacks, destructors, scheduler suspension, and page faults are outside the small transition proof. State whether the claim covers only preallocated structural operations or the end-to-end API.

**Separate reclamation from removal.** After dequeue advances `Head`, the old dummy is unreachable from the new head but may remain in another thread's local `head` or `tail`. Immediate free enables use-after-free. Reuse can also create ABA: an old address-plus-counter representation may compare equal after several removals and allocations. The original algorithm used counted pointers and assumed appropriate memory management; a modern implementation needs a concrete scheme.

Hazard pointers announce protected nodes, validate after announcement, retire removed nodes, and reclaim only after a scan proves no hazard names them. Epoch schemes delay reclamation until every participant from a prior epoch has quiesced. Garbage collection preserves physical lifetime but the algorithm must still avoid harmful node reuse or mutation. Tagged pointers have width and wraparound assumptions. These are alternative proof systems, not interchangeable optimizations.

**Compose capacity and lifecycle explicitly.** The core queue is logically unbounded. Checking `size < capacity` before enqueue races. An exact bounded API needs reservation and rollback that compose with publication, or a bounded ring algorithm with different invariants. Backpressure and blocking dequeue require a notification protocol that cannot miss a transition between checking empty and sleeping. A semaphore/count can drift unless its update and queue operation have proved failure/cancellation rules.

Close must order admission against in-flight enqueues, define whether consumers drain existing items, and delay destruction until operations and reclamation quiesce. An enqueue that linearized before noticing cancellation cannot simply disappear. Retrying a timed-out call may duplicate an item unless the API provides identity/idempotency. Exact `size` and snapshots are not free: traversals race with head movement and need lifetime protection; a count linearized separately can describe another instant.

**Use a finite artifact honestly.** The model below makes CAS methods indivisible and deliberately leaves `Tail` behind twice. It demonstrates the lag state, helping branch, dummy-role transfer, FIFO result, and final structural invariants.

<!-- bijux-verify: {"id":"michael-scott-bounded-schedule","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"enqueued=A,B\ndequeued=A,B\nlink_successes=2\nhead_successes=2\ntail_advances=2\nhead=2\ntail=2\ndummy=2\nempty=True\nall_invariants=True\nevidence=finite_michael_scott_schedule_model\n","stderr":""}} -->
```python
class MichaelScottScheduleModel:
    def __init__(self):
        self.head = 0
        self.tail = 0
        self.next_of = {0: None}
        self.value_of = {0: None}
        self.link_successes = 0
        self.head_successes = 0
        self.tail_advances = 0

    def prepare(self, node, value):
        assert node not in self.next_of
        self.next_of[node] = None
        self.value_of[node] = value

    def link(self, predecessor, node):
        if self.next_of[predecessor] is not None:
            return False
        self.next_of[predecessor] = node
        self.link_successes += 1
        return True

    def help_tail(self, expected, desired):
        if self.tail != expected or self.next_of[expected] != desired:
            return False
        self.tail = desired
        self.tail_advances += 1
        return True

    def dequeue(self):
        while True:
            head = self.head
            tail = self.tail
            successor = self.next_of[head]
            assert head == self.head
            if head == tail:
                if successor is None:
                    return None
                assert self.help_tail(tail, successor)
                continue
            assert successor is not None
            value = self.value_of[successor]
            if self.head == head:
                self.head = successor
                self.head_successes += 1
                return value

    def reachable(self):
        nodes = []
        seen = set()
        node = self.head
        while node is not None and node not in seen:
            nodes.append(node)
            seen.add(node)
            node = self.next_of[node]
        return nodes, node is None


queue = MichaelScottScheduleModel()
queue.prepare(1, "A")
assert queue.link(0, 1)  # E1 pauses before its optional Tail swing.
assert queue.head == queue.tail and queue.next_of[queue.head] == 1
assert queue.help_tail(0, 1)  # Another operation repairs the lag.

queue.prepare(2, "B")
assert queue.link(1, 2)  # E2 also leaves Tail behind.
first = queue.dequeue()
second = queue.dequeue()  # Observes Head == Tail with a successor and helps.
nodes, acyclic = queue.reachable()
empty = queue.head == queue.tail and queue.next_of[queue.head] is None
all_invariants = (
    first == "A"
    and second == "B"
    and nodes == [2]
    and acyclic
    and queue.link_successes == 2
    and queue.head_successes == 2
    and queue.tail_advances == 2
    and empty
)

print("enqueued=A,B")
print(f"dequeued={first},{second}")
print(f"link_successes={queue.link_successes}")
print(f"head_successes={queue.head_successes}")
print(f"tail_advances={queue.tail_advances}")
print(f"head={queue.head}")
print(f"tail={queue.tail}")
print(f"dummy={nodes[0]}")
print(f"empty={empty}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_michael_scott_schedule_model")
```

The artifact uses unique integer node identities, never reclaims storage, and executes a chosen sequential schedule. It proves only its finite state assertions. It does not run threads, implement language atomics, explore arbitrary histories, establish memory ordering, ABA safety, reclamation safety, lock-freedom, or performance.

**Build an evidence ladder.** First test sequential empty/singleton/FIFO behavior and ownership. Then use deterministic schedules for delayed tail swing, two enqueuers at one terminal link, two dequeuers at one head, enqueue/dequeue overlap, empty observation, cancellation, and stalled observers. Record invocation/response histories and check bounded linearizability. Use target-language race, sanitizer, model-checking, and reclamation tools. Pause participants at every load/protect/CAS boundary; measure whether peers complete and whether retired memory remains bounded.

Benchmark against a correct mutex queue and mature platform alternatives with identical allocation, capacity, wakeup, and payload semantics. Vary producer/consumer ratio, empty rate, burst size, threads, CPU/NUMA placement, payload size, allocator, and reclamation. Report throughput, latency percentiles, CAS attempts/failures, help count, coherence traffic, allocations, retired bytes, quiescence delay, per-thread fairness, and overload behavior. A throughput win under one balanced microbenchmark is not a universal design result.

## Definitions and Notation

Let abstract queue be `Q=<q_0,...,q_{n-1}>`, oldest first. Concrete nodes form `Reach(H)=<d,x_0,...,x_{n-1}>`, where `H=Head`, `d` is the dummy, and payload projection of nodes after `d` equals `Q`. `next(x)` is null or a successor; while reachable in the basic algorithm, a nonnull link is immutable.

`T=Tail` is on `Reach(H)`. In the original algorithm, distance from `T` to the terminal node is zero or one. `CAS(A,e,n)` atomically writes `n` to atomic object `A` iff its current representation equals expected `e`. Equality is valid only under the stated identity/ABA model.

For enqueue `E(n)`, `lp(E)` is successful `CAS(tail.next,null,n)`. The later `CAS(Tail,tail,n)` is auxiliary. For nonempty dequeue `D`, `lp(D)` is successful `CAS(Head,head,next)`. For empty dequeue, `lp(D)` is the validated observation `head==tail && head.next==null`.

Node lifecycle states are private `P`, linked/live `L`, dummy `D`, retired `R`, and reclaimable `C`. A new node moves `P→L` at link CAS; its payload is removed and role becomes `D` at a later head CAS; the old dummy moves `D→R`; reclamation allows `R→C` only after all possible observers are excluded.

Let `A_l`, `F_l` be link attempts/failures, `A_h`, `F_h` head attempts/failures, `H_t` successful tail-help advances, `B_r` retired bytes, and `L_p` latency percentile. These are measured quantities under a named implementation and workload, not proof variables.

## Mechanisms, Invariants, or Proof Structure

### Representation and FIFO proof

1. Initialization creates one finite chain containing only the dummy.
2. A successful link CAS appends one private initialized node at the unique terminal null link.
3. Nonnull reachable links never change, so link order is permanent while nodes remain reachable.
4. A successful head CAS advances exactly one link, returning the immediate successor's payload.
5. Thus payloads are removed in successful-link order and the new head remains a dummy.

### Tail-lag and helping proof

1. Before append, `Tail` is terminal or one behind.
2. Linking after a terminal tail can introduce distance one.
3. Observers seeing nonnull `tail.next` help `Tail` to that successor before attempting another append.
4. Therefore original `Tail` remains on the chain, never behind `Head`, and at most one link from terminal.
5. `Head==Tail && next!=null` denotes lag, not emptiness.

### Linearization proof

Order operations by successful link CAS, successful head CAS, and qualifying empty reads. Each enqueue appends one item; each nonempty dequeue removes/returns the oldest linked item; each empty read observes no successor. Failed attempts and tail repair have no abstract effect. The selected point is inside each call, and nonoverlapping real-time order is preserved.

### Progress proof boundary

Mismatch or invalidation indicates a structural transition by another participant; lag repair advances a finite chain edge. Repeated interference implies system completions, while an operation running alone completes. This assumes scheduled steps, suitable atomics, bounded local work, safe lifetime access, and no harmful ABA. It excludes blocking/failing allocation, unbounded callbacks, reclamation quiescence, fairness, and weak-CAS spurious behavior unless separately proved.

### Evidence ladder

1. Sequential FIFO, empty, singleton, ownership, null, capacity, and close tests.
2. Reachability, acyclicity, dummy-role, link immutability, tail-bound, and single-return assertions.
3. Controlled schedules at every load, validation, link, head, and tail-help boundary.
4. Bounded linearizability/model checking over invocation-response histories.
5. Target memory-order, race, sanitizer, ABA, and reclamation evidence.
6. Stalled-participant, thread-exit, allocation failure, overload, cancellation, and shutdown faults.
7. Workload-shaped latency, throughput, retries, helping, coherence, fairness, and retained-memory measurement.

## Alternatives and Trade-Offs

| Design | Mechanism | Main advantage | Principal cost |
|---|---|---|---|
| Mutex queue | sequential queue under one lock | simplest proof, close, size, capacity | holder blocking and convoying |
| Two-lock linked queue | separate head/tail locks | enqueue/dequeue overlap | blocking, lifecycle lock ordering |
| Michael–Scott queue | link/head CAS plus helping | compact lock-free MPMC core | allocation, hot ends, reclamation |
| Hazard-pointer MS queue | per-thread announcements | safe native reuse; individual protection | scans, records, retry protocol |
| Epoch-protected MS queue | read-side participation | cheap common-path protection | stalled participants retain memory |
| GC-managed linked queue | collector preserves lifetime | simpler physical reclamation | GC cost and implementation-specific links |
| Bounded MPMC ring | per-slot sequence/state | fixed memory and locality | fixed capacity, wraparound proof |
| Segmented queue | linked fixed-size buffers | amortized allocation/cache benefit | segment retirement and boundary states |
| Flat combining | delegated batched queue ops | fewer hot-word transitions | combiner latency and blocking assumptions |
| Work-stealing deques | owner end plus stealing end | scheduler locality/scalability | different semantics, more complex races |

A correct mutex or two-lock queue is often preferable when blocking is acceptable and lifecycle features dominate. A bounded ring is usually stronger for fixed memory and cache locality, but it is not a drop-in linked-queue proof. Managed-runtime libraries may use Michael–Scott ideas while deliberately changing traversal, unlinking, or tail slack; verify the actual source and public contract.

## Failure Modes and Misconceptions

- **“`Tail` is the last item.”** It can legally lag; links define membership and order.
- **“Equal head and tail means empty.”** Only a consistent null successor establishes empty.
- **“Tail CAS publishes enqueue.”** The prior link CAS is the abstract effect.
- **“A helper completes another call.”** Tail helping repairs representation; the enqueue already linearized at linking.
- **“The dequeued node is freed.”** The old dummy becomes retired; the value node becomes the next dummy.
- **“Reading payload after winning is safer.”** Another dequeue may then retire/reclaim that successor; protection and read placement matter.
- **“Counted pointers solve ABA permanently.”** Finite counters can wrap and require atomic width/alignment assumptions.
- **“Acquire/release solves lifetime.”** Visibility ordering does not prevent reuse or use-after-free.
- **“Garbage collection proves the algorithm.”** It helps lifetime but does not prove ordering, progress, logical reuse, or lifecycle.
- **“Lock-free means no waiting.”** A caller can retry/starve indefinitely, and reclamation or allocation can block.
- **“Unbounded means no capacity policy.”** It means memory is the implicit capacity and exhaustion is the failure mode.
- **“A semaphore trivially adds blocking.”** Queue and permit transitions must compose across failure, timeout, and cancellation.
- **“`size()` can count links safely.”** Traversal needs lifetime safety and is not necessarily a single-instant snapshot.
- **“Weakly consistent iteration is a snapshot.”** It may reflect overlapping changes according to a documented weaker contract.
- **“Stress success proves linearizability.”** Tests sample executions; proof/model checking and memory evidence address different risks.

## Worked Examples

### Example 1

**Situation.** Queue starts with dummy D. E links A after D and pauses before moving `Tail`.

**Reasoning.** The link CAS linearized A. A dequeuer sees `Head==Tail==D` but `D.next=A`, helps `Tail=D→A`, and retries. Reporting empty would place the dequeue after a completed enqueue while returning absence.

**Conclusion.** Head/tail equality plus a nonnull successor is a repair state, not empty.

### Example 2

**Situation.** Enqueuers E and F both observe terminal T and prepare A and B.

**Reasoning.** Only one null-to-node CAS on `T.next` wins, say A. F's failure has no abstract effect. F observes/helps tail to A, then links B after A. Linearization order is E then F, regardless of response order.

**Conclusion.** Contending terminal link CAS operations serialize enqueue order.

### Example 3

**Situation.** Two dequeuers both observe dummy D and successor A.

**Reasoning.** Only one CAS `Head:D→A` wins absent ABA. Winner returns A. Loser must discard its value candidate, protect/reload the new successor, and retry; it cannot also return A.

**Conclusion.** Head-CAS winner uniqueness provides exactly one removal.

### Example 4

**Situation.** Dequeue reads empty, and an overlapping enqueue links A immediately afterward.

**Reasoning.** The empty operation linearizes at the consistent null-successor observation; enqueue linearizes later at link CAS. Overlap permits that sequential order.

**Conclusion.** A nonblocking empty result need not anticipate an overlapping producer.

### Example 5

**Situation.** E initializes payload A and uses a release link CAS; D follows the link through an acquire observation.

**Reasoning.** The synchronization edge publishes E's prior writes before D consumes A. If D has no acquire path, a data-race-free language proof may be absent even though pointer topology looks correct.

**Conclusion.** Link publication, not tail maintenance, carries payload visibility.

### Example 6

**Situation.** P loads old dummy D. Q advances head, retires D, and allocator reuses D's address before P validates.

**Reasoning.** P can compare equal bits belonging to a different incarnation, dereference changed storage, or perform a stale CAS. Hazard/epoch protection, sufficiently strong tags, or another scheme must forbid the schedule or detect identity change.

**Conclusion.** ABA and reclamation are coupled correctness obligations.

### Example 7

**Situation.** Capacity is 100; two producers read an exact counter of 99 and both link.

**Reasoning.** A separate precheck is not atomic with either publication. Reserve capacity atomically before linking with defined rollback, use a packed/composed state, serialize admission, or choose a bounded ring.

**Conclusion.** Exact capacity is a cross-object protocol, not a free queue property.

### Example 8

**Situation.** Consumer checks empty, then waits on a condition; producer links and signals between those actions.

**Reasoning.** Without a mutex/sequence/permit protocol that makes check-and-park atomic relative to notification, the consumer can miss the signal and sleep while data exists.

**Conclusion.** Lock-free storage does not automatically implement blocking channels.

### Example 9

**Situation.** Close observes an empty queue and frees its dummy while an admitted producer has initialized a private node but not linked it.

**Reasoning.** The producer can link through freed state or publish after destruction. Close must stop admission, account for entrants, wait for in-flight operations, apply drain/discard policy, and quiesce reclamation.

**Conclusion.** Destruction requires a lifecycle proof spanning unpublished operations.

### Example 10

**Situation.** An MS queue wins a 16-thread preallocated throughput test but production has bursty producers, slow consumers, and stalled epoch participants.

**Reasoning.** The benchmark omitted allocation, unbounded growth, retired retention, tail latency, topology, and backpressure. Measure those with equal semantics against mutex, ring, and platform queues; define overload limits before adoption.

**Conclusion.** End-to-end operational evidence can reverse a CAS-core benchmark result.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** CAS, release/acquire, progress classes, helping, ABA, hazard pointers, epochs, and history checking provide the language-level machinery.
- **Operating Systems:** preemption, allocator behavior, futex/parking protocols, cache coherence, NUMA, and teardown determine end-to-end behavior.
- **Database Engineering:** queues carry log, flush, compaction, and worker tasks; bounded admission and crash/retry semantics matter more than local FIFO alone.
- **Data Engineering:** ingestion buffers need explicit watermarks, backpressure, loss policy, and observability; an unbounded queue can convert lag into memory failure.
- **Security Engineering:** producer floods, retained memory, counter wrap, unsafe reuse, and teardown races create denial-of-service or memory-corruption surfaces.
- **Performance Engineering:** help rate, CAS failures, coherence, allocation, retired bytes, per-thread fairness, and percentile latency must be interpreted together.

## References

1. Maged M. Michael and Michael L. Scott, [“Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms”](https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf), PODC 1996, pp. 267–275. Primary algorithm, pseudocode, safety, linearization, and progress arguments.
2. Maged M. Michael and Michael L. Scott, [“Nonblocking Algorithms and Preemption-Safe Locking on Multiprogrammed Shared Memory Multiprocessors”](https://www.cs.rochester.edu/u/scott/papers/1998_JPDC_nonblocking.pdf), *Journal of Parallel and Distributed Computing* 51(1), 1998. Expanded queue design and experimental context.
3. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness framework and queue histories.
4. Maurice Herlihy, [“Wait-Free Synchronization”](https://cs.brown.edu/people/mph/Herlihy91/p124-herlihy.pdf), *ACM TOPLAS* 13(1), 1991. Primary progress and universality framework.
5. Maged M. Michael, [“Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects”](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/hazard_pointers.pdf), *IEEE TPDS* 15(6), 2004, pp. 491–504. Primary safe-reclamation and ABA treatment.
6. Oracle, [`ConcurrentLinkedQueue`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/util/concurrent/ConcurrentLinkedQueue.html), Java SE 26. Official current FIFO, weakly consistent traversal, size-cost, and memory-consistency contract, accessed 2026-08-30.
7. ISO C++ working draft, [Atomics clause](https://eel.is/c++draft/atomics), current draft accessed 2026-08-30. Primary atomic-object, compare-exchange, and memory-order specification.
8. Rust Project, [`std::sync::atomic`](https://doc.rust-lang.org/std/sync/atomic/), Rust 1.98 documentation, accessed 2026-08-30. Official atomic ordering, portability, and progress-scope guidance.

## Exercises

### Exercise 1

State the sequential FIFO specification and define dummy node, helping, linearization point, lock-free, ABA, retirement, and reclamation. List the original Michael–Scott representation invariants.

### Exercise 2

Trace from dummy D: E1 links A and pauses; E2 observes lag, helps tail, links B, and updates tail; D1 and D2 both observe D/A, D2 wins, then D1 retries. Give abstract order, returned values, and final head/tail chain.

### Exercise 3

Review an implementation that declares empty whenever `Head==Tail`, uses relaxed link CAS, reads successor payload after head CAS, and immediately frees the old dummy. Identify each defect and give a safe high-level correction.

### Exercise 4

Design a bounded, blocking, closeable API around an MS-style queue. Specify capacity reservation/rollback, notification without lost wakeup, successful and empty points, cancellation, close/drain, in-flight tracking, and destruction/reclamation.

### Exercise 5

A cross-socket telemetry service has bursty producers, occasional consumers, severe memory growth, and high tail-CAS traffic. Select among MS queue, bounded MPMC ring, mutex queue, and segmented queue; give a verification, benchmark, and rollout plan.

## Answers to the Exercises

### Answer 1

`enqueue(x)` appends x to abstract sequence `Q`; nonempty dequeue returns/removes its first element; empty returns absence unchanged. The dummy is the head node excluded from abstract payloads. Helping advances another operation's lagging structural hint. A linearization point is the atomic abstract-effect event. Lock-free guarantees system-wide, not per-call, progress. ABA hides intervening state behind equal bits. Retirement follows unlinking; reclamation permits reuse only after no observer remains.

The live representation is one finite acyclic chain; `Head` is its first node and dummy; payloads after it equal `Q`; reachable nonnull next links are immutable; `Tail` is on the chain, never before head, and originally last or second-to-last; link CAS alone appends; head CAS alone removes; equal head/tail is empty only with null successor; publication makes fields visible; observed nodes remain alive; harmful ABA is excluded.

### Answer 2

Initially `Head=Tail=D`. E1's CAS `D.next:null→A` linearizes enqueue A; its tail pause has no abstract effect. E2 sees `Tail=D`, `D.next=A`, helps `Tail:D→A`, then CAS-links `A.next:null→B`, linearizing enqueue B, and swings `Tail:A→B`. Both dequeuers observe `Head=D`, successor A. D2 wins `Head:D→A`, linearizes and returns A; D1's old CAS fails and it must discard the old candidate. D1 protects/reloads head A and successor B, then wins `Head:A→B`, linearizes and returns B.

Final live chain is only B as dummy, with `Head=Tail=B` and `B.next=null`. Abstract order is `enqueue(A), enqueue(B), dequeue()->A, dequeue()->B`; failed CAS and both tail moves are absent from the abstract history. Old D and then A are retired and require safe reclamation.

### Answer 3

`Head==Tail` can coexist with nonnull `Head.next` after enqueue publication, so the empty test loses a completed item; inspect a consistent successor and help tail when nonnull. Relaxed publication may fail to make private payload/next initialization visible; use a target-proved release link and acquire consumption path. Reading payload after head CAS can race with another dequeue that makes the successor reclaimable. Immediate free races with observers that loaded the old dummy and enables reuse/ABA.

Correct outline: enter the chosen reclamation protection; acquire/validate head, tail, and successor; on equal head/tail, return empty only for validated null successor, otherwise help/retry. Protect successor before dereference. Read its value at a lifetime-safe point, CAS head with target-valid ordering, retry on failure, and on success return the saved value. Retire the old dummy and reclaim only after hazards/epochs/other protocol excludes every observer. Derive exact memory orders and identity handling from the target language and reclamation implementation.

### Answer 4

Expose `tryEnqueue`, `enqueueUntil`, `tryDequeue`, `dequeueUntil`, `close`, and `awaitQuiescence`, with explicit full, empty, timeout, cancelled, and closed results. Before publication, atomically reserve one of N capacity permits; failure returns/waits. Allocation or cancellation before link releases the reservation. Successful link CAS linearizes enqueue and creates one data-available permit. Successful head CAS linearizes dequeue and releases capacity exactly once. Empty remains a validated null-successor observation.

Waiters need a sequence/condition/semaphore protocol in which registering to sleep and rechecking state prevents a transition-and-signal from being missed; spurious wakeups loop. Cancellation before a point rolls back reservation/registration; after a point the operation occurred and its result must be delivered or recovered idempotently. Close atomically blocks new admission, wakes waiters, defines drain versus discard, and accounts for producers already holding reservations. Destruction waits for entrants and callbacks, drains/disposes payloads, and reaches reclamation quiescence. The linked CAS core may remain lock-free, but waiting, exact admission, allocation, close, and reclamation need separate progress claims.

### Answer 5

Memory growth makes unbounded MS unsuitable without strict admission. If capacity and predictable locality dominate and payload slots fit a fixed ring, choose a proven bounded MPMC ring with per-slot sequence numbers. If resize/bursts require elastic chunks, a bounded segmented queue amortizes allocation but adds segment retirement. A mutex queue is the strongest simple baseline when blocking is acceptable. Retain MS only if its nonblocking progress is required and a bound/reclamation system is proven; high tail-CAS traffic alone may be reduced by batching/segments but is secondary to overload safety.

Verify sequential semantics, wrap/segment states, capacity permits, cancellation, close, ownership, histories, target memory order, races, reclamation, and stalled participants. Benchmark realistic producer/consumer imbalance and NUMA placement against all baselines, reporting throughput, per-thread/tail latency, occupancy, drops/waits, CAS/help, cache misses/coherence, allocations, and retained bytes. Canary behind one stable API with bounded queues and alerts for occupancy, age, memory, and latency; shadow/differential-check where possible. Roll back for any history, loss/duplication, memory, lifecycle, fairness, or tail regression, and expand only after sustained production-shaped evidence.
