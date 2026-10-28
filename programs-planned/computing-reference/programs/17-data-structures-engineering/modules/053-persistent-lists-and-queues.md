---
module_id: DSE-053
program: Data Structures Engineering
level: 2
module_number: 53
title: Persistent Lists and Queues
status: complete
last_verified: 2026-08-30
---

# Persistent Lists and Queues

## One-Page Review

### Governing question

How should immutable lists and FIFO queues preserve every version while providing correct order, honest amortized or worst-case bounds under branching histories, safe lazy evaluation, bounded retention, and production-grade evidence?

### Essential definitions

- A **persistent list** is an immutable sequence whose `cons`, `head`, and `tail` operations preserve old roots by sharing suffixes.
- A **queue** is a first-in, first-out abstract data type with enqueue at the rear and peek/dequeue at the front.
- A **two-list queue** stores a front list in dequeue order and a rear list in reverse enqueue order.
- A **rotation** reverses the rear and appends it to the front, either eagerly, incrementally, or lazily.
- **Amortized time** bounds total work over an allowed operation trace; it is not a bound on each operation.
- A **persistent execution trace** is a version DAG in which several later operations may use the same earlier queue.
- A **suspension** is delayed computation; **memoization** records its result so all forcing paths share the work.
- A **schedule** exposes a bounded portion of an incremental rotation on every operation.
- A **real-time queue** guarantees a worst-case bound per operation, not merely a low average over one history.
- **Confluent persistence** permits an operation such as concatenation to combine two previous versions.

### Central model, mechanism, or theorem

A cons list node `(value,next)` is already persistent when both fields and every reachable payload are immutable. `cons(x,L)` allocates one node pointing to `L`; `tail(L)` returns an existing suffix. Each root denotes an independent logical sequence even though physical suffixes have multiple incoming edges.

A simple functional FIFO queue represents sequence `F ++ reverse(R)`. Enqueue conses onto `R`; dequeue removes from `F`; when `F` becomes empty, normalization reverses `R`. The representation invariant is `len(F)+len(R)=size`, and every nonempty normalized queue has nonempty `F`. This implementation is semantically persistent, but an eager rotation gives only a linear-history amortized claim. Branch repeatedly from a version immediately before rotation and the same conceptual credits pay for many reversals.

Persistence-compatible amortization makes delayed work part of the immutable value and memoizes it, so different branches force the same suspension at most once. A real-time design additionally schedules a bounded amount of rotation work per operation and proves the rotation finishes before the front is exhausted. Strict languages can encode the suspended process as an explicit state machine. API choice, evaluation strategy, scheduler invariant, and cost model are therefore one contract.

### Critical invariants

1. Every published list/queue node and transitively reachable value is immutable, or value ownership is explicitly weaker.
2. A list root is acyclic and finite unless the API explicitly supports coinductive streams.
3. Queue abstraction is exactly `F ++ reverse(R)` or the documented equivalent during rotation.
4. Stored lengths equal reachable logical lengths and empty/nonempty states agree with the abstract sequence.
5. Every dequeue returns the oldest retained element and a new queue containing the remaining sequence; old roots remain unchanged.
6. Delayed work is deterministic, exception semantics are specified, and memoized results are safely published once.
7. The rotation/schedule invariant ensures required front cells exist before consumers demand them.
8. Complexity claims quantify the permitted version DAG, forcing model, allocation, and reclamation—not only source-level calls.
9. Roots, iterators, thunks, schedules, caches, and in-flight readers participate in retention and lifetime accounting.

### Common failures

- Calling a mutable linked list persistent because operations return a new wrapper.
- Storing mutable payloads and promising deep snapshot isolation.
- Reversing the rear all at once and claiming worst-case constant-time dequeue.
- Applying linear-sequence amortization unchanged to a branching persistent trace.
- Using call-by-name suspensions without memoization, so every force repeats work.
- Memoizing unsafely under concurrency or caching a partially initialized result.
- Checking only stored lengths while order, rotation state, or schedule is corrupt.
- Conflating FIFO queues, priority queues, deques, streams, and durable message queues.
- Retaining a tiny root or iterator that pins a long suffix or suspended rotation.
- Measuring throughput without tail latency, branch shape, forcing, allocation, and live roots.

### Compact example

Starting from empty, enqueue `alpha`, `beta`, `gamma`. The two-list representation is front `[alpha]`, rear `[gamma,beta]`, denoting `[alpha,beta,gamma]`. Dequeue returns `alpha` and reverses the rear into front `[beta,gamma]`. Enqueue `delta` shares that front. Independently enqueue `xray` from the earlier `[alpha,beta]` root, yielding `[alpha,beta,xray]`; neither branch changes the original. The finite executable reproduces these values and identities, but does not establish an asymptotic bound.

### Connections

[DSE-051](051-path-copying.md) defines version and lifetime semantics, while [DSE-052](052-structural-sharing.md) supplies physical-DAG accounting. [DSE-014](014-singly-linked-lists.md), [DSE-017](017-queues.md), and [DSE-019](019-ring-buffers.md) provide the Level I linked-list, FIFO, and bounded-buffer baseline. [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supply cost and evidence discipline. The [program roadmap](../ROADMAP.md) proceeds to persistent trees, tries, vectors, versioned storage, concurrency, and verification.

## Governing Question

Which logical sequence, persistence level, evaluation strategy, rotation protocol, cost model, ownership policy, and evidence make a persistent list or FIFO queue correct for both linear and branching use—not merely elegant source code?

## Why This Matters

Immutable lists are the smallest useful example of persistence. A new head can share an arbitrarily long suffix with an old list while preserving both values. The same idea underlies environment chains, paths, undo logs, syntax traversals, worklists, and functional language runtimes. Lists also reveal the central engineering risk: one mutable element or one unbounded retained root can invalidate the apparent simplicity.

FIFO queues expose a deeper issue. The familiar two-list representation is short, practical, and semantically persistent. Its conventional amortized argument, however, assumes one future: each rear element is charged once for a later reversal. Full persistence creates a version DAG. Many branches can return to the same pre-rotation version and request the same expensive step. A proof over a linear call sequence no longer proves the advertised bound.

Lazy evaluation with memoization can repair the accounting by sharing the result of delayed work across branches. Real-time scheduling can strengthen the guarantee to a bounded amount of work per operation. Those mechanisms introduce new obligations: when a thunk runs, whether it runs once, how exceptions are cached, how concurrent forces synchronize, which roots retain it, and whether latency measurements include forcing and garbage collection.

Production engineers also use “persistent queue” to mean a durable broker or disk-backed message log. That is a different abstraction. An immutable in-memory FIFO provides versions and snapshot values; it does not provide process-crash recovery, acknowledgements, delivery guarantees, consumer groups, or exactly-once effects. Precise vocabulary prevents an algorithmic data structure from being mistaken for a distributed system.

## Prerequisites and Retrieval

Retrieve singly linked representation, sentinels, cycles, and iteration from [DSE-014](014-singly-linked-lists.md); FIFO contracts from [DSE-017](017-queues.md); and bounded circular-storage contrast from [DSE-019](019-ring-buffers.md). Retrieve persistence levels, version roots, failure publication, and reclamation from [DSE-051](051-path-copying.md), and logical occurrences versus physical DAG nodes from [DSE-052](052-structural-sharing.md).

You should be able to prove a representation invariant by induction, distinguish worst-case from amortized cost, trace a version DAG, reason about reachability-based memory, and separate abstract values from object identity. Review [DSE-002](002-representation-invariants.md), [DSE-004](004-time-space-and-allocation-cost.md), [DSE-006](006-memory-locality-and-cache-behavior.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) as needed.

## Learning Objectives

After completing this module, you can:

1. specify immutable list and FIFO queue semantics independently from representation;
2. prove suffix sharing and explain its identity, lifetime, and retention consequences;
3. derive the two-list queue abstraction and its normalization invariant;
4. distinguish worst-case, ephemeral amortized, persistent amortized, and real-time guarantees;
5. construct a branching trace that invalidates a naïve linear-history credit proof;
6. explain how laziness, memoization, schedules, and explicit rotation state repair different obligations;
7. design total empty/error, iterator, concurrency, serialization, and failure contracts;
8. compare strict, lazy, banker's, physicist's, Hood–Melville, and finger-tree-like representations;
9. validate every retained version, representation state, and sharing promise; and
10. benchmark work, forcing, allocation, retention, and tail latency under adversarial version DAGs.

## Core Exposition

**Start with the abstract values.** A finite list over elements `A` is either `Nil` or `Cons(x,xs)`. Its operations are `empty`, `cons`, `is_empty`, `head`, and `tail`; traversal, map, fold, reverse, and append derive from them. A FIFO queue is a finite sequence with `empty`, `enqueue(q,x)`, `peek(q)`, and `dequeue(q)`. Enqueue adds at the logical rear; dequeue returns/removes the logical front.

Define empty behavior. A total API can return an option/result containing either `(value,new_queue)` or empty. An exception-based API names its exception. A sentinel is unsafe if the element domain can contain it. `peek` returns an element without changing the abstract sequence, although a lazy implementation may internally force and memoize work; whether such hidden mutation is observable under concurrency or failures belongs to the runtime contract.

Persistence means an update returns a new root and leaves all earlier roots queryable. It does not require retaining all roots forever; application references determine retention. Partial/full persistence is mostly natural for immutable values because any root can be passed to enqueue/dequeue. Concatenation combines two versions and is therefore confluent persistence, which needs separate representation and complexity arguments.

List equality normally compares element sequences, not node identities or construction history. Queue equality should likewise compare FIFO order unless the API intentionally uses identity. Values need transitive immutability, copying, ownership, or a documented shallow-snapshot contract. A persistent spine containing a mutable byte buffer does not preserve the buffer's historical content.

**A cons list obtains persistence by construction.** Represent a nonempty node as immutable `(head,tail)`. `cons(x,L)` creates one node whose tail references `L`; it cannot affect `L`. `tail(cons(x,L))=L` by identity. Inductively, every node reachable from an old root remains unchanged after future `cons` or `tail` operations. Several roots may share the same suffix.

For `L=[a,b,c]`, `cons(z,L)` physically adds one node and shares all three old nodes. Taking two tails returns the node for `c`. Building `cons(x,tail(L))` creates `[x,b,c]` and shares `[b,c]`. Logical occurrences across roots can exceed unique physical nodes; use the union of root reachability for live-space accounting.

Prepend, head, and tail take constant pointer-machine work and one/zero spine allocation. Lookup at index `i` takes `O(i)`. Reverse copies `n` spine nodes. `append(X,Y)` copies the entire spine of `X` so its last pointer can lead to `Y`, while sharing `Y`; its work/allocation are `Theta(|X|)`. A recursive implementation also risks call-stack overflow unless the language optimizes tail calls or the algorithm is iterative.

An iterator pins its root and visits a stable suffix under immutability. That makes snapshot iteration simple, but a one-element iterator can retain all remaining nodes and payloads. A cursor represented as a suffix root is itself a persistent list. Expose ownership/close semantics where readers are long-lived or external resources sit in payloads.

**Derive the two-list FIFO queue.** Store `Q=(F,R,n_f,n_r)`, where `F` is in front-to-rear order and `R` is in rear-to-front order. The abstract sequence is

`seq(Q) = list(F) ++ reverse(list(R))`.

Enqueue `x` creates `R'=Cons(x,R)`, so `reverse(R')=reverse(R)++[x]`. It therefore appends logically in constant cons work. If `F` is nonempty, dequeue returns `head(F)` and uses `tail(F)`. When `F` is empty and `R` nonempty, reverse `R` to become the new front and clear the rear. A normalized nonempty queue always has a front cell.

Lengths make size constant-time and make corruption visible. Require `n_f=|F|`, `n_r=|R|`, `size=n_f+n_r`, nonnegative bounded integers, and `(n_f+n_r=0)` exactly when both lists are empty. If using the minimal normalize-only-when-empty scheme, require `n_f>0` for every nonempty published queue. Stronger scheduled algorithms use different balance constraints.

The representation proof is algebraic. Enqueue preserves sequence because reversing the new rear moves `x` to its end. A normal dequeue with `F=Cons(y,F')` yields `y` and sequence `F'++reverse(R)`. A rotation when `F'` is empty replaces `([],R)` by `(reverse(R),[])`, whose sequence is unchanged. Old queue roots are untouched because all list nodes and queue records are immutable.

**The simple cost proof has a persistence boundary.** In one linear history, each element is consed once onto `R`, copied at most once by reversal, and removed once from `F`. The aggregate work for `m` operations is `O(m)`, so operations are amortized `O(1)`, although the dequeue triggering a reversal costs `Theta(n)`. A potential such as `Phi(Q)=|R|` pays for future reverse work under an appropriate constant accounting.

That proof assumes the state whose rear contains the credits has one future. Retain `Q` with one front item and `n` rear items. From `Q`, dequeue forces a reversal costing `Theta(n)`. Discard the result, return to the same `Q`, and repeat on `k` branches. The version DAG performs `Theta(kn)` reversal work after only `O(n+k)` updates, while the same stored potential is spent `k` times. Semantic persistence survives; the claimed persistent amortized bound does not.

This is not merely a hostile API user. Parsers, search, speculative execution, backtracking, symbolic evaluation, and undo trees naturally branch. State the allowable trace. “Amortized `O(1)` on a linear ephemeral history” may be a useful guarantee, but it is weaker than “amortized `O(1)` over a fully persistent execution DAG.”

**Laziness can share deferred work.** Instead of eagerly reversing, represent the new front as a lazy stream whose cells are produced incrementally. A suspension encapsulates deterministic computation plus a state initially unevaluated, then evaluating, then value or failure. Memoization stores the result. If many versions share that suspension, its computation is charged once physically; later forces reuse the cell.

Call-by-name without memoization is insufficient because every branch repeats evaluation. Memoization without immutability can also fail: if the thunk reads changing state, the first forcing branch changes the value observed by others. Require pure/deterministic delayed computation or explicitly snapshot every dependency. Specify whether exceptions are memoized, retried, wrapped, or poison the structure.

Okasaki's persistence-aware debit methods attach debt to unevaluated suspensions and require each operation to discharge enough debt before it can demand the result. The proof reasons over execution traces rather than pretending old versions have disjoint credits. A suspension that has already been forced has no remaining work, even if many roots reference it.

Memoization commonly mutates a private thunk cell, so “purely functional interface” and “no mutation anywhere” are different. The mutation is observationally benign only when all forces yield the same value/failure, publication is safe, and identity/timing/resource effects are outside or explicitly inside the contract. In a concurrent runtime, use a once-cell, lock, atomic state machine, or runtime-provided thread-safe lazy value. Never expose a partially built stream node.

**Scheduling strengthens latency guarantees.** A real-time queue spreads rotation across operations. One family stores a front stream, a strict reversed rear, and a schedule that is a suffix of pending front/rotation work. Maintain a balance condition such as `|R| <= |F|`; when enqueue would violate it, start a rotation that produces a new front incrementally and clear the rear. Each public operation forces a bounded number of schedule cells.

The central deadline proof is: when rotation starts, enough old front elements remain to serve dequeues while the new front is produced; every operation advances the schedule; therefore the new front is ready before the old front is exhausted. Exact constants depend on the rotation algorithm. Do not quote `O(1)` from a different invariant or evaluation semantics.

A strict language can reify incremental reversal as a state machine: idle, reversing front/rear with accumulators, appending, and done. Each enqueue/dequeue executes a fixed number of state transitions. Hood–Melville-style real-time queues demonstrate this route. The state machine is more verbose but makes scheduling explicit and avoids relying on implicit language laziness. Every intermediate state requires a representation invariant and abstraction function.

Worst-case source-level step count is not necessarily worst-case wall-clock latency. Allocation, reference counting, cache misses, thunk synchronization, garbage collection, and destructor cascades can pause. Use “real-time” in the data-structural asymptotic sense unless a runtime deadline has actually been established.

**Lists, queues, deques, and concatenation have different design spaces.** A FIFO queue needs access at one end and insertion at the other. A deque also inserts/removes at both ends. A catenable sequence combines two whole values. A priority queue orders by priority, not arrival. A durable message queue adds storage and delivery semantics. One representation does not inherit another abstraction's guarantees.

Cons lists give constant front operations but linear append. Difference lists represent a list as a function and make composition cheap, but materialization and persistence/closure retention matter; naïve repeated application can create deep call chains. Catenable lists can use lazy linking, trees, or bootstrapped deques. Concatenation is confluent because output depends on two roots; sharing and ancestry can become complex.

Finger trees represent persistent sequences with small digits at the ends and recursively measured internal nodes. They support end access amortized constant time and concatenation/splitting logarithmic in a relevant size, while cached monoidal measures enable indexing or search. They are powerful but have larger constants, more node forms, and richer invariants than a simple FIFO.

Kaplan–Tarjan catenable deques and later verified implementations show that stronger worst-case and concatenation bounds are possible, but their machinery should not be casually reconstructed from a sketch. Choose the weakest structure meeting the actual API. A queue that never concatenates should not pay for a general catenable sequence without evidence.

**Failure and resource behavior complete the contract.** With immutable construction, enqueue allocates privately and publishes a new queue last. If element retention, node allocation, reversal, thunk creation, or metadata computation fails, release partial work and preserve old roots. A lazy failure may occur later during peek/dequeue; specify which operation reports it and whether future forces repeat it.

Reference counting gives prompt reclamation for acyclic spines but adds updates on every shared tail/root and can recursively destroy long unique chains. Use iterative/deferred destruction or tracing where stack depth matters. Cycles can enter through payloads, memo cells, parent pointers, callbacks, or caches. Tracing collectors handle unreachable cycles but introduce heap and pause policy.

Arenas improve allocation locality but suffix sharing crosses version/generation boundaries. One surviving node can retain an arena containing many dead peers. Epoch reclamation fits readers of published roots, but an epoch only says when retired objects may be reclaimed; it does not determine which shared nodes remain reachable from newer roots.

Bound queue size, root/version count, branch factor, reader age, thunk depth/work, retained/live bytes, element bytes, operation time, and serialized output. Overflow-check stored lengths. Recursive comparison, hashing, serialization, or destruction of an adversarial list may exhaust the stack or CPU. Do not log full queue contents when elements may be sensitive.

**Concurrency separates values from a shared service.** An immutable queue value can be read by many threads after safe publication and lifetime protection. Two threads can independently enqueue onto the same root and receive two valid branches. That is full persistence, not a concurrent multi-producer queue.

A shared latest-queue variable needs synchronization. A compare-and-swap loop loads a root, constructs a new root, and publishes if unchanged. A loser retries or records a branch. Linearizability concerns the atomic root update; FIFO ordering between concurrent enqueues follows successful publication order, not start time. Allocation and lazy forcing may still lock.

Forcing a shared suspension concurrently must establish exactly one fully initialized memoized outcome or a specified equivalent. Blocking waiters, cancellation, reentrancy, recursive self-force, and exception publication need definitions. A dead thread must not leave the lazy cell permanently “evaluating” without recovery policy.

Do not use this structure as a lock-free MPMC channel merely because its roots are immutable. Channels require atomic coordination, blocking/wakeup or polling semantics, closure, cancellation, backpressure, and memory-order proofs. Immutable values are useful components, not the whole concurrent object.

**Serialization should preserve values before identities.** The simplest list/queue format stores elements in logical order plus schema/version and rebuilds the representation. This discards physical sharing and suspended work, which is usually desirable. Never serialize raw pointers, locks, thunks, closures, or process-local memo state.

If many versions must preserve shared suffixes, graph serialization assigns node IDs/content hashes and root records. Validate reference ranges, acyclicity, element bounds, root reachability, stored lengths, queue abstraction, node/type tags, and quotas. A cyclic or extremely deep input is hostile even if its byte length is modest.

On disk, immutable records do not by themselves give durability. Write children/elements, checksums, and metadata before atomically publishing roots; define flush and recovery. Garbage collection traces retained root manifests. Encryption and integrity do not replace authorization to individual histories.

Representation changes—strict to lazy, length width, encoding, comparator/equality, element schema—need migration or logical rebuild. A versioned logical format is more durable than exposing current node shapes.

**Evidence must exercise values, branches, states, and costs.** Maintain a simple array/deque model for each retained root. Generate enqueue, peek, dequeue, empty, and branch-from-any-version operations. Compare every version after every operation; do not let the reference model share the implementation's lists or thunks.

Validate representation states: exact lengths, abstraction sequence, acyclicity, schedule/debt/rotation invariants, thunk states, and allowed sharing. Exhaust tiny histories, including empty operations, one element, rotation boundaries, alternating operations, long rear, long front, repeated branches at every boundary, and equal-content independently built queues.

Metamorphic properties include enqueue then eventual dequeue order, peek/dequeue agreement, old-root immutability, branch isolation, `dequeue(enqueue(empty,x))=(x,empty)`, size change, serialization round trip, and normalization preserving sequence. Sharing tests are white-box promises; logical correctness does not require maximum sharing.

For persistent amortized evidence, generate version DAGs—not only linear traces. Repeatedly branch from pre-rotation states and count actual list-cell/thunk/state transitions. Verify memoized work runs once per suspension. For real-time claims, instrument the maximum work per public operation and test adversarial sequences. An average cannot establish a worst-case bound.

Fault-inject allocations, element retention, thunk creation/force, memo publication, state transitions, length overflow, root CAS, serialization writes, and cancellation. Concurrent tests race force, enqueue/dequeue publication, release, and retry under sanitizers or model checking where available.

Benchmarks vary size, enqueue/dequeue mix, branch factor/depth, pre-rotation branching, strict/lazy runtime, forcing policy, retained roots/readers, element size, allocator/collector/refcount, threads, and serialization. Report latency quantiles and maximum observed steps, allocation/copies, forced/memoized cells, CAS retries, live/retained/reclaimed bytes, oldest root/reader, GC pauses, and correctness checks. Keep asymptotic proof, finite test, and production measurement distinct.

The executable below uses immutable Python tuples as cons cells and queue records. It checks a finite two-list queue, old-version preservation, branching, FIFO order, normalization, and selected identity sharing. Python tuples copy queue records and the eager rotation has no persistent amortized or real-time proof; the snippet is semantic and structural evidence only.

<!-- bijux-verify: {"id":"persistent-two-list-queue-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"linear_q=alpha,beta,gamma\npopped=alpha\nafter_pop=beta,gamma\nafter_enqueue=beta,gamma,delta\nbranch=alpha,beta,xray\nq2_unchanged=alpha,beta\nq3_unchanged=True\nbranch_isolated=True\nq5_shares_q4_front=True\nq7_front_equals_but_not_identical=True\nall_fifo=True\nall_invariants=True\nevidence=finite_persistent_two_list_queue_trace\n","stderr":""}} -->
```python
EMPTY = None


def cons(value, tail):
    return (value, tail)


def list_length(node):
    total = 0
    while node is not EMPTY:
        total += 1
        node = node[1]
    return total


def reverse_list(node):
    result = EMPTY
    while node is not EMPTY:
        result = cons(node[0], result)
        node = node[1]
    return result


def list_values(node):
    values = []
    while node is not EMPTY:
        values.append(node[0])
        node = node[1]
    return tuple(values)


def normalize(queue):
    front, rear, front_length, rear_length = queue
    if front is EMPTY and rear is not EMPTY:
        return (reverse_list(rear), EMPTY, rear_length, 0)
    return queue


def empty_queue():
    return (EMPTY, EMPTY, 0, 0)


def enqueue(queue, value):
    front, rear, front_length, rear_length = queue
    return normalize((front, cons(value, rear), front_length, rear_length + 1))


def dequeue(queue):
    front, rear, front_length, rear_length = normalize(queue)
    if front is EMPTY:
        raise ValueError("empty queue")
    value = front[0]
    remainder = normalize((front[1], rear, front_length - 1, rear_length))
    return value, remainder


def queue_values(queue):
    front, rear, _, _ = queue
    return list_values(front) + tuple(reversed(list_values(rear)))


def valid(queue):
    front, rear, front_length, rear_length = queue
    lengths_match = (
        front_length == list_length(front)
        and rear_length == list_length(rear)
    )
    normalized = (front_length + rear_length == 0) or front is not EMPTY
    return lengths_match and normalized


q0 = empty_queue()
q1 = enqueue(q0, "alpha")
q2 = enqueue(q1, "beta")
q3 = enqueue(q2, "gamma")
popped, q4 = dequeue(q3)
q5 = enqueue(q4, "delta")
q6 = enqueue(q2, "xray")
_, q7 = dequeue(q2)

versions = (q0, q1, q2, q3, q4, q5, q6, q7)
expected = (
    (),
    ("alpha",),
    ("alpha", "beta"),
    ("alpha", "beta", "gamma"),
    ("beta", "gamma"),
    ("beta", "gamma", "delta"),
    ("alpha", "beta", "xray"),
    ("beta",),
)
all_fifo = tuple(queue_values(queue) for queue in versions) == expected
all_invariants = all(valid(queue) for queue in versions)

print("linear_q=" + ",".join(queue_values(q3)))
print("popped=" + popped)
print("after_pop=" + ",".join(queue_values(q4)))
print("after_enqueue=" + ",".join(queue_values(q5)))
print("branch=" + ",".join(queue_values(q6)))
print("q2_unchanged=" + ",".join(queue_values(q2)))
print("q3_unchanged=" + str(queue_values(q3) == expected[3]))
print("branch_isolated=" + str(queue_values(q5) != queue_values(q6)))
print("q5_shares_q4_front=" + str(q5[0] is q4[0]))
print(
    "q7_front_equals_but_not_identical="
    + str(q7[0] == q2[1] and q7[0] is not q2[1])
)
print("all_fifo=" + str(all_fifo))
print("all_invariants=" + str(all_invariants))
print("evidence=finite_persistent_two_list_queue_trace")
```

## Definitions and Notation

- `Nil` is the empty finite list; `Cons(x,xs)` is an immutable node with head `x` and tail `xs`.
- `list(L)` is the logical element sequence reachable from list root `L`.
- `Q=(F,R,n_f,n_r)` is the basic two-list queue state.
- `seq(Q)=list(F) ++ reverse(list(R))` is its abstraction function; `++` denotes sequence concatenation.
- `size(Q)=n_f+n_r`; stored lengths must equal reachable spine lengths.
- `enqueue(Q,x)` appends `x` to the abstract rear; `dequeue(Q)` returns `(oldest,Q')`.
- A **root** names one immutable list/queue version; retained roots form a set `Roots`.
- A **version DAG** has an edge from operation/result version `u` to each prior version it consumes.
- A **linear trace** is a version path; a **branching trace** reuses an earlier version in multiple future operations.
- `W(op)` is actual representation work, such as cons allocations, reverse steps, forces, or rotation transitions.
- `Phi(Q)` is a potential assigned to a state for amortized analysis; amortized cost is `W + Phi(after) - Phi(before)` in a linear trace.
- A **suspension** delays computation; `force(s)` requests its value; a memoized suspension records a completed value/failure.
- A **schedule** is persistent state describing incremental work that public operations must advance.
- **Real-time** here means worst-case asymptotic data-structure steps per operation, not a certified wall-clock deadline.
- **Shallow persistence** preserves the spine but not mutations inside element payloads; **deep persistence** preserves the intended reachable value graph.
- `Reach(r)` is the set of physical nodes reachable from root `r`; live physical nodes are `union_{r in Roots} Reach(r)` plus runtime roots such as thunks and iterators.

## Mechanisms, Invariants, or Proof Structure

**List proof.** Base root `Nil` is valid. If `L` is a valid immutable acyclic list, `Cons(x,L)` is valid when `x` satisfies the element ownership policy: its tail is valid, its logical sequence is `[x]++list(L)`, and no existing node changes. Head/tail equations follow by construction. Induction over operations proves every retained root's sequence.

**Queue abstraction proof.** Maintain `I(Q)`: stored lengths match the spines, size is their sum, published nonempty minimal queues have a front, and `seq(Q)=F++reverse(R)`. Enqueue establishes the rear equation `reverse(Cons(x,R))=reverse(R)++[x]`. Dequeue removes `head(F)`. Normalization uses `reverse(R)++[]` in place of `[]++reverse(R)`, preserving sequence and size. Immutability preserves all old roots.

**Linear amortized proof.** Charge each enqueue enough constant credits to allocate its rear cell and later copy that element during one reversal. Along one result-following path, every rear cell enters one rotation before removal, so total reverse work is linear in enqueues. The triggering operation can still be linear worst-case.

**Counterproof under branching.** Choose a root with one front cell and `n` rear cells. Create `k` children, each by dequeuing that same root. Every child independently performs the eager `n`-cell reverse, giving `Omega(kn)` actual work. The root contains only one set of credits. Thus the original potential proof is not valid for arbitrary version DAGs.

**Memoized repair.** Put delayed rotation cells in shared immutable queue state and ensure each suspension computes at most once. Assign debit to unevaluated work. A branch that forces work changes the shared suspension state to evaluated, so sibling branches observe the paid result. Prove deterministic value, safe one-time publication, and that every operation discharges debt before demanding the cell.

**Real-time repair.** Define rotation states and a progress measure `remaining`. Prove each public operation performs at most constant state transitions; enqueue/dequeue preserve the abstraction across intermediate states; `remaining` decreases on scheduled steps; and the consumer deadline cannot reach an unavailable front cell before `remaining=0`. Include startup and finalization constants.

**Lifetime invariant.** A node/thunk/state may be reclaimed only when unreachable from all list/queue roots, iterators, schedules, memo cells, readers, registries, and external handles. Refcounts or tracing must model those edges. Physical live space is a reachability union, not the sum of logical version sizes.

**Concurrency invariant.** Published nodes are fully initialized. A shared root update has a stated linearization point. A memo cell transitions atomically among allowed states and publishes one complete outcome. Readers acquire lifetime before traversal. No lock-free guarantee is inferred merely from immutable nodes.

**Evidence ladder.** Algebra proves representation and asymptotic claims under assumptions. Exhaustive/property tests compare finite histories and branches. Instrumentation checks actual bounded transitions/forces for implementations. Benchmarks characterize a runtime/workload. Fault, concurrency, retention, and serialization tests address different obligations. Passing one rung does not imply the others.

## Alternatives and Trade-Offs

| Representation | Core benefit | Bound caveat | Engineering cost |
|---|---|---|---|
| Immutable cons list | Constant prepend/head/tail and suffix sharing | Append/index are linear | Minimal; retention/locality can surprise |
| One-list FIFO | Simplest representation | Either enqueue or dequeue is linear | Useful only for small/skewed workloads |
| Strict two-list queue | Small, fast, semantically persistent | Eager rotation is linear worst-case; simple amortization is linear-history | Low |
| Lazy banker's queue | Persistence-aware amortization through shared memoized work | Depends on lazy/memo semantics and debit proof | Moderate |
| Physicist's queue | Different lazy scheduling/accounting organization | Same need to prove forcing and persistence assumptions | Moderate |
| Real-time lazy queue | Worst-case bounded abstract steps | Runtime pauses and force synchronization remain | Higher |
| Hood–Melville strict queue | Explicit incremental state in strict languages | More intermediate states/invariants | Higher |
| Finger tree / measured sequence | Deque, split, concatenation, search versatility | Larger constants and richer invariants | High |
| Catenable deque/list | Efficient confluent combination | Complex proof, sharing, and retention | Very high |
| Mutable ring buffer | Locality, bounded capacity, predictable storage | Ephemeral unless copied/logged; shared updates synchronize | Different abstraction |

Prefer a cons list for stack-like histories and front operations. Prefer a strict two-list queue when traces are linear, occasional reversal latency is acceptable, and the contract says so. Use a verified lazy or explicit real-time design when branching or tail guarantees matter. Use finger trees/catenable structures only when split/concatenate/deque operations justify them. For bounded concurrent channels, use a purpose-built synchronization structure.

## Failure Modes and Misconceptions

1. **“Functional syntax guarantees persistence.”** Hidden mutable tails, arrays, payloads, caches, or unsafe references can couple versions.
2. **“Two lists mean every operation is constant time.”** The rotation-triggering operation is linear unless work is scheduled.
3. **“Amortized proof automatically survives persistence.”** A branching version DAG can spend one state's credits repeatedly.
4. **“Lazy means work disappears.”** Work is delayed; without memoization it repeats, and with memoization it consumes state, synchronization, and memory.
5. **“Memoization is observationally irrelevant.”** Timing, exceptions, allocation, locks, and side channels may reveal first force.
6. **“Real-time means a wall-clock SLA.”** The theorem counts model steps; runtime GC, allocation, scheduling, and page faults can pause.
7. **“Queue immutability makes a concurrent queue.”** A shared service still needs atomic publication, FIFO linearization, blocking, close, and backpressure.
8. **“A tail pointer is a harmless iterator.”** It can retain the entire suffix and its payload graph.
9. **“Logical size is memory.”** Multiple roots share nodes, while thunks, schedules, headers, allocators, and dead-but-uncollected nodes add overhead.
10. **“Serialize the node graph exactly.”** Internal thunk/lock/state shapes are unstable and unsafe; logical-order formats are usually preferable.
11. **“Concatenation is just append.”** Efficient concatenation combines roots and requires confluent persistence plus a new bound.
12. **“One passing FIFO test proves the queue.”** Rotation boundaries, every old root, branches, state invariants, failures, and resource behavior remain.

## Worked Examples

### Example 1

**Sharing a list suffix.**

Question: `L=[b,c,d]`; build `A=cons(a,L)` and `X=cons(x,L)`. How many logical occurrences and unique spine nodes exist across `A` and `X`?

Reasoning: each root unfolds to four occurrences, so the sum is eight. Physically `L` contributes three shared nodes, while `a` and `x` add one each: five unique nodes. Mutating the `c` node would corrupt both values, so it must be immutable.

Conclusion: logical size across versions is eight occurrences, but live physical spine size is five nodes with one shared three-node suffix.

### Example 2

**Append cost and identity.**

Question: append `X=[1,2,3]` to `Y=[4,5]` with cons lists.

Reasoning: the last pointer of immutable `X` cannot change. Rebuild `3 -> Y`, then `2 -> rebuilt`, then `1 -> rebuilt`: three new nodes. Both `Y` nodes are shared. The output equals `[1,2,3,4,5]`; no original `X` node is on its first three-node prefix.

Conclusion: list append takes and allocates `Theta(|X|)` spine work while sharing `Y`.

### Example 3

**Two-list FIFO trace.**

Question: enqueue `a,b,c` from empty, then dequeue once in the minimal normalized two-list queue.

Reasoning: after `a`, normalize to `F=[a],R=[]`. Enqueue `b,c` gives `F=[a],R=[c,b]`, denoting `[a]++reverse([c,b])=[a,b,c]`. Dequeue returns `a`; empty front triggers reverse, producing `F=[b,c],R=[]`.

Conclusion: the abstract FIFO order is preserved, but that dequeue copies two rear spine nodes.

### Example 4

**Empty boundary contract.**

Question: what should `dequeue(empty)` do?

Reasoning: returning `None` is ambiguous if `None` is a valid element. A total API returns a tagged empty result; another valid contract raises a named exception and leaves the empty root unchanged. Stored lengths must be zero and both spines empty.

Conclusion: empty behavior is an explicit type/API decision, not an implementation accident or magic payload.

### Example 5

**Breaking naïve amortization with persistence.**

Question: a retained root has front `[a]` and a rear of 1,000 elements. Ten branches each dequeue that root. What work can eager rotation perform?

Reasoning: every branch removes `a`, finds the front empty, and independently reverses the same 1,000 logical rear nodes. Actual reverse steps are 10,000. A linear-history proof had deposited only enough credit for one reversal.

Conclusion: the strict two-list queue remains semantically correct, but `O(1)` amortized over arbitrary persistent branching is false.

### Example 6

**Why memoization changes the trace cost.**

Question: suppose all ten branches share a delayed, memoized rotation rather than separately calling reverse.

Reasoning: the first branch forces stream cells and publishes their results. Sibling branches force the same suspension identities and reuse evaluated cells. Under deterministic computation and safe once-publication, physical rotation work occurs once, though every branch still performs its own dequeue bookkeeping.

Conclusion: shared memoized computation can support persistence-aware amortization; mere deferred call-by-name computation cannot.

### Example 7

**Rotation deadline.**

Question: a scheduled queue begins rotation with enough front cells to serve upcoming dequeues and advances two rotation transitions per public operation. What must the proof show?

Reasoning: establish a progress measure, a lower bound on consumable old-front cells, an upper bound on transitions required, and invariant preservation for enqueue and dequeue. Then show the transitions reach done before a dequeue needs a cell not yet constructed.

Conclusion: “incremental” is not enough; a deadline inequality connects balance, work rate, and consumer demand.

### Example 8

**Shallow snapshot failure.**

Question: queue `Q1` contains mutable list `payload=[1]`; `Q2=enqueue(Q1,x)`; then code appends `2` to `payload`.

Reasoning: neither queue spine changed, but reading the first element through both roots now yields `[1,2]`. The historical value `[1]` was not preserved. Copying only the cons spine provided shallow, not deep, persistence.

Conclusion: element ownership/immutability is part of the queue snapshot contract.

### Example 9

**Competing concurrent enqueues.**

Question: writers load root `[a]`; one constructs `[a,b]`, another `[a,c]`, and both try to publish a latest root.

Reasoning: both branch values are valid. With unconditional stores, the last store loses the other update. With compare-and-swap, one succeeds and defines the next latest order; the loser retries from that root or preserves an explicit branch. Retry-side effects must not duplicate.

Conclusion: immutable versions prevent structural races but do not define multiwriter service semantics.

### Example 10

**Selecting a representation.**

Question: a parser keeps many checkpoints, branches heavily, needs FIFO worklists, and has a strict 99.9th-percentile latency target; it never concatenates queues.

Reasoning: a strict eager two-list queue exposes repeated rotation spikes under checkpoints. A general finger tree adds unused operations and constants. A tested persistence-aware lazy queue may fit if memo forcing is safe; an explicit real-time state machine gives clearer strict-runtime bounds. Benchmark both with the parser's branch DAG and collector.

Conclusion: choose the simplest verified scheduled FIFO meeting branch and tail requirements, not the most general sequence.

## Cross-Program Connections

- Programming-languages semantics: laziness, memoization, observational equivalence, exceptions, and cost semantics determine whether the proof matches execution.
- Concurrent and parallel programming: immutable roots simplify snapshots, while once-cells, CAS publication, epochs, and channels require memory-order and progress proofs.
- Software engineering: persistent queues support undo, event-sourced projections, parser checkpoints, and immutable application state, but retention ownership must be explicit.
- Database engineering: version roots resemble snapshot readers and copy-on-write pages; root publication and garbage collection echo MVCC lifecycle concerns.
- Distributed systems: algorithmic FIFO order is much weaker than durable broker delivery, acknowledgement, replication, and exactly-once effect semantics.
- Security engineering: hostile depths, branch/root pinning, thunk bombs, serialization graphs, timing of first force, and sensitive history require quotas and isolation.
- Formal methods: inductive list/queue abstraction, execution-trace amortization, and machine-checked Hood–Melville/catenable deque developments show distinct proof layers.
- Performance engineering: allocation, cache locality, GC/refcount, forcing, branch shape, and tail latency can dominate asymptotic source-level operations.

## References

1. Chris Okasaki, *Purely Functional Data Structures*, PhD thesis, Carnegie Mellon University, 1996. https://www.cs.cmu.edu/~rwh/students/okasaki.pdf
2. Chris Okasaki, “Simple and Efficient Purely Functional Queues and Deques,” *Journal of Functional Programming* 5(4), 1995. https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7B3036772616B39E87BF7FBD119015AB/S0956796800001489a.pdf/simple-and-efficient-purely-functional-queues-and-deques.pdf
3. Chris Okasaki, “Amortization and Persistence via Lazy Evaluation,” in *Purely Functional Data Structures*, Cambridge University Press. https://www.cambridge.org/core/books/purely-functional-data-structures/amortization-and-persistence-via-lazy-evaluation/95B424557EF683F5EB579544A645EF6A
4. Alejandro Gómez-Londoño, “Hood–Melville Queue,” Archive of Formal Proofs, 2021. https://isa-afp.org/entries/Hood_Melville_Queue.html
5. Ralf Hinze and Ross Paterson, “Finger Trees: A Simple General-Purpose Data Structure,” *Journal of Functional Programming* 16(2), 2006. https://www.cs.ox.ac.uk/ralf.hinze/publications/FingerTrees.pdf
6. Haim Kaplan and Robert E. Tarjan, “Strictly Functional, Real-Time Deques with Catenation,” Princeton technical report TR-584-98, 1998. https://www.cs.princeton.edu/research/techreps/283
7. Jules Viennot, Arthur Wendling, Armaël Guéneau, and François Pottier, “Verified Purely Functional Catenable Real-Time Deques,” 2025. https://cambium.inria.fr/~fpottier/publis/viennot-wendling-gueneau-pottier-verified-catenable-deques.pdf
8. Clojure, `PersistentQueue.java`, current implementation source, retrieved 2026-08-30. https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentQueue.java

## Exercises

### Exercise 1

**Retrieve the abstraction.**

For `F=[p,q]`, `R=[t,s,r]`, `n_f=2`, and `n_r=3`, compute the logical queue. State the result of one dequeue and the representation before any optional stronger balancing.

### Exercise 2

**Derive the persistent counterexample.**

Construct a family of version DAGs showing why eager two-list queue amortization over a linear history does not yield `O(1)` amortized cost per operation under full persistence. Give update count and reversal work asymptotically.

### Exercise 3

**Design and validate a strict state machine.**

Sketch durable states for an incremental strict rotation, the abstraction information each state must carry, and a validator/test strategy. You need not reproduce a published algorithm, but must avoid claiming a bound you have not proved.

### Exercise 4

**Choose between three designs.**

Compare a strict two-list queue, a persistence-aware memoized queue, and a finger tree for: (a) a single-thread batch pipeline; (b) a branching theorem prover; and (c) an editor sequence needing split and concatenation. Include proof, runtime, and retention trade-offs.

### Exercise 5

**Transfer to a durable service boundary.**

A team proposes serializing an in-memory lazy persistent queue, including thunk objects and node pointers, as its durable job broker. Diagnose the category error and design a safe boundary between immutable scheduling snapshots and a crash-recoverable queue service.

## Answers to the Exercises

### Answer 1

**Retrieve the abstraction.**

`reverse(R)=reverse([t,s,r])=[r,s,t]`; therefore `seq(Q)=[p,q,r,s,t]`. One dequeue returns `p`. The remaining minimal representation can be `F=[q]`, `R=[t,s,r]`, `n_f=1`, `n_r=3`, denoting `[q,r,s,t]`. No normalization is required because the front remains nonempty. A scheduled implementation might rebalance earlier under its own stronger invariant, but must preserve the same logical sequence.

### Answer 2

**Derive the persistent counterexample.**

Build a root `Q_n` using `n+1` enqueues so it has one front element and `n` rear elements under minimal normalization. Retain `Q_n`. For each of `k` children, perform `dequeue(Q_n)` and discard or retain the result. Every child independently reverses `n` rear nodes, so reversal work is `Theta(kn)`. The trace used `O(n+k)` public operations/edges but can choose `k=n`, producing `Theta(n^2)` reverse work. The old potential `|R|=n` was counted once yet spent on every outgoing edge. This refutes the arbitrary-version-DAG amortized claim, not FIFO correctness.

### Answer 3

**Design and validate a strict state machine.**

Use states such as `Idle(front,rear,lengths)`, `Reversing(old_front,old_rear,new_front,new_rear,done_count)`, `Appending(remaining,accumulator,done_count)`, and `Done(new_front)`. The exact transitions depend on the selected algorithm, so this is architecture rather than a worst-case proof. Each state needs an abstraction relation to the same logical queue, exact lengths/progress, acyclicity, ownership, and a statement of which front elements are immediately consumable. Public operations execute a fixed transition budget.

Validation should compare logical order against an independent deque for every intermediate published state, check progress decreases and lengths match, exhaust small rotation boundaries, branch from every state, and inject failure at every allocation/transition. Instrument maximum transitions per operation. A real-time claim additionally needs a formal deadline argument proving the rotation finishes before front demand, plus runtime measurements that separately characterize allocation and collection pauses.

### Answer 4

**Choose between three designs.**

For the single-thread batch pipeline, a strict two-list queue is preferred when linear-history amortization and occasional rotation latency are acceptable; it minimizes machinery and memo retention. For a branching theorem prover, use a persistence-aware memoized or explicitly real-time queue whose proof covers version DAGs. Memoization shares forced work but requires deterministic thread-safe lazy cells and can retain suspensions; explicit scheduling adds state complexity.

For the editor, a finger tree or another measured persistent sequence fits split, concatenation, and access at both ends; a FIFO-only queue makes middle operations linear. Its richer node/measure invariants, allocation constants, and retention require testing. In every case, choose using the actual operation distribution and branch shape, state the guarantee, compare every retained version, and benchmark latency/allocation/live bytes under the target runtime.

### Answer 5

**Transfer to a durable service boundary.**

Thunk objects contain process-local evaluation state, closures, locks, pointers, runtime code assumptions, and possibly partial failures. Raw pointers are meaningless after restart. An immutable FIFO version also lacks acknowledgements, leases, replication, fsync/root publication, redelivery, idempotency, authorization, and backpressure. Calling it a durable broker is therefore a category error.

Define a logical wire/storage record containing schema version, stable job IDs, canonical bounded payloads, ordering/partition metadata, and integrity/authentication fields—not node layout. A durable append/claim/ack state machine writes and flushes records before publishing offsets/roots, recovers from checksummed logs, and defines at-least-once or another delivery contract. Rebuild an in-memory persistent queue as a disposable scheduling snapshot from committed records. Snapshot roots may optimize readers, but the durable log/state machine is authoritative. Test crash points, duplicate delivery, corrupt/truncated records, authorization, quotas, replay, schema migration, and garbage collection independently from the in-memory FIFO proof.
