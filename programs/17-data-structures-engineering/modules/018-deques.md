---
module_id: DSE-018
program: Data Structures Engineering
level: 1
module_number: 18
title: Deques
status: complete
last_verified: 2026-08-29
---

# Deques

## One-Page Review

### Governing question

How can one sequence support insertion, removal, and observation at both ends while keeping orientation, capacity, growth, wraparound, block layout, eviction, iteration, and concurrency contracts precise?

### Essential definitions

- A **deque** (double-ended queue, pronounced “deck”) is a finite sequence supporting operations at both front and back.
- `push_front(x)` prepends; `push_back(x)` appends; `pop_front` removes first; `pop_back` removes last.
- **Orientation** defines front-to-back logical order independently of physical layout.
- A **bounded deque** has a maximum element/byte capacity and an explicit full policy.
- A **dropping deque/history** automatically evicts an opposite-end element when full; this differs from a capacity-bounded deque whose insertion can fail.
- A **circular-array deque** maps logical positions through modular indices in reusable storage.
- A **segmented deque** stores elements across fixed or variable blocks with metadata locating the ends.
- A **linked deque** uses bidirectional nodes and endpoint links; it has different allocation and locality costs.
- A **monotonic deque** is an algorithm-maintained deque whose stored candidate keys are ordered to answer sliding extrema.
- A **work-stealing deque** is a specialized concurrent structure with asymmetric owner and thief operations; it is not an ordinary thread-safe deque by default.

### Central model, mechanism, or theorem

Write the abstract deque front-to-back as `D=<d0,...,d(n-1)>`. The four endpoint transitions are:

\[
\begin{aligned}
push_front(x,D)&=\langle x\rangle\cdot D,\\
push_back(D,x)&=D\cdot\langle x\rangle,\\
pop_front(D)&=(d_0,\langle d_1,\ldots,d_{n-1}\rangle),\\
pop_back(D)&=(d_{n-1},\langle d_0,\ldots,d_{n-2}\rangle).
\end{aligned}
\]

For a circular array with capacity `c>0`, head index `h`, and size `n`, logical element i occupies `(h+i) mod c`. Back insertion uses `(h+n) mod c`; front insertion changes `h` to `(h-1) mod c`. Size distinguishes full (`n=c`) from empty (`n=0`). These equations preserve logical order across physical wrap.

### Critical invariants

1. The representation encodes exactly one front-to-back abstract sequence.
2. Empty/full and both endpoint observations agree with size and capacity.
3. Every live element occupies exactly one valid slot/node; every non-live slot follows lifetime rules.
4. Circular indexing is checked, normalizes wrap correctly, and never divides by zero.
5. Segmented metadata reaches blocks/elements in order without gaps, duplication, or stale map entries.
6. Successful endpoint operations publish/destroy exactly one element under their failure contract.
7. Bounded insertion and automatic eviction are never confused; callers observe rejection or loss explicitly.
8. Iterators, bulk spans, resizing, concurrent owners/thieves, and reclamation obey documented rules.

### Common failures

- Reversing logical orientation for one of the four endpoint methods.
- Using only equal head/tail indices to represent both full and empty without another bit/count/slot.
- Performing unsigned `head-1` without correct modular normalization.
- Reading wrapped storage as one contiguous span.
- Assuming every deque is a circular array; current CPython uses linked fixed-length blocks.
- Calling all endpoint operations worst-case constant while ignoring allocation or resizing.
- Treating bounded `maxlen` eviction as rejected insertion.
- Assuming efficient endpoints imply efficient arbitrary middle insertion or random access.
- Mutating a monotonic deque without preserving candidate-value and expiration invariants.
- Treating documented atomic endpoint methods as a multi-operation transaction.
- Copying a work-stealing algorithm without its owner/thief, memory-order, resize, and reclamation proof.

### Compact example

A capacity-five circular deque appends A,B,C; prepends Z; removes C from the back; appends D,E and becomes full; rejects Y at the front; removes Z and E; then prepends X. Logical order is `X,A,B,D`, physical head is slot four, and live elements wrap from slot four to slots zero through two. The trace verifies finite mapping and boundaries, not generic growth or concurrency.

### Connections

[DSE-016](016-stacks.md) and [DSE-017](017-queues.md) are restricted one-end/two-end views; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supplies resizing; [DSE-015](015-doubly-and-intrusive-linked-lists.md) supplies linked endpoints. The [program roadmap](../ROADMAP.md) next isolates ring-buffer invariants and then editor-oriented ropes/piece tables.

## Governing Question

What abstraction, end orientation, layout, capacity policy, and evidence make double-ended operations dependable—and when do monotonic-window or work-stealing uses require stronger invariants than an ordinary deque?

## Why This Matters

Stacks and queues restrict which end clients may use. A deque exposes both, allowing it to serve either abstraction, maintain windows, schedule work, store histories, and support algorithms that expire one end while adding or pruning at the other. This flexibility reduces the need to move elements through an unsuitable array front.

It also increases the contract surface. Four endpoint methods must agree on orientation. Array storage can wrap. Growth may relocate. Segmented implementations have block maps. Bounded variants can reject or automatically evict. Concurrent work stealing assigns different permissions to owner and thieves. “Deque operation is O(1)” is therefore only useful after naming the representation, operation, capacity state, and cost model.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction and representation proofs from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- failure, ownership, alias, and observer contracts from [DSE-003](003-operation-contracts.md);
- worst-case/amortized allocation, byte, and latency models from [DSE-004](004-time-space-and-allocation-cost.md);
- layout/locality and iterator tools from [DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-008](008-iterators-and-traversal-protocols.md);
- model tests and benchmarks from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- dynamic arrays, linked lists, stacks, and queues from [DSE-012](012-dynamic-arrays-and-geometric-growth.md), [DSE-014](014-singly-linked-lists.md), [DSE-015](015-doubly-and-intrusive-linked-lists.md), [DSE-016](016-stacks.md), and [DSE-017](017-queues.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify all four endpoint operations over one logical sequence orientation;
2. derive circular-array index equations and full/empty invariants;
3. compare circular, segmented, linked, and persistent representations;
4. distinguish endpoint guarantees from middle access/insertion and iterator guarantees;
5. design bounded rejection, dropping eviction, growth, and byte-capacity policies;
6. implement and prove a monotonic deque for sliding-window extrema;
7. explain why CPython, Rust, Java, C++, and Swift deque contracts/layouts differ;
8. test wrap, growth, exact-full, eviction, alias, failure, and iterator boundaries;
9. benchmark real endpoint/window workloads without importing legacy machine constants;
10. state the owner/thief, linearization, ordering, resizing, ABA, and reclamation obligations of work stealing.

## Core Exposition

**Fix logical orientation first.** Use front-to-back order D. `push_front` adds before index zero and `push_back` after the last element. Pops remove those respective positions. A deque used as a stack chooses one end consistently; used as FIFO, it inserts at one end and removes the other. The minimal deque does not require arbitrary indexing or middle mutation.

Java `Deque` names paired endpoint methods and provides exception and special-value variants. C++ `deque` is a full sequence container with random access and middle operations, so its public contract is richer than the minimal ADT. Rust `VecDeque` documents a growable ring buffer. Do not infer one library's layout or invalidation from the shared word “deque.”

**Circular arrays reuse both sides.** With `c>0`, size n, head h, logical index i maps to `(h+i) mod c`. Front is h; back is `(h+n-1) mod c` when nonempty. Push-back constructs at `(h+n) mod c`; push-front computes a preceding head and constructs there. Pops clear/destroy one live endpoint and adjust head/size.

Tracking size makes equal head/tail unambiguous. Other designs reserve one slot, store a full bit, or use monotonic counters whose difference is size. Each changes usable capacity and overflow reasoning. A zero-capacity deque cannot perform modulo c; handle it before index arithmetic.

For unsigned machine integers, `(h-1)%c` may underflow before modulo. Use `h==0 ? c-1 : h-1`, a language-defined wrapping operation with proved bounds, or wider/checked arithmetic. Likewise, `h+n` can overflow even if the final modulo would be small. Keeping normalized bounded indices or proving monotonic-counter wrap is essential.

**Wrapped data is at most two contiguous spans.** If h+n<=c, live storage is one span `[h,h+n)`. Otherwise it is `[h,c)` followed by `[0,(h+n)%c)`. Iteration yields them in that logical order. APIs requiring one contiguous slice may copy or rotate, changing time, invalidation, and failure behavior.

Cleared endpoint slots must no longer be live. Reference runtimes should release them; low-level generic storage must destroy exactly once. Debug markers cannot substitute for lifetime tracking. Serialization writes logical order, not physical slot order or spare capacity.

**Growth is a representation transition.** When a growable ring is full, allocate a larger buffer and place logical sequence contiguously or at a chosen new head, then commit. This can move every element, invalidate physical views, and temporarily retain old/new storage. Geometric policies give amortized bounds under DSE-012 assumptions, not worst-case latency.

Growth from both ends does not require reserved slack on both physical sides because circular mapping reuses any spare slot. Nevertheless, an implementation can choose block allocation or centered initial placement to reduce early transitions. Bulk prepend/append must define source order and self-alias handling.

**Segmented deques trade contiguity for stable endpoint growth.** A block-based representation stores elements in chunks and a map/index of blocks. Endpoint insertion consumes room in the end block or allocates another block/map entry. Random access can compute a block and offset, but exact constants, block size, map growth, iterator structure, and invalidation are implementation-specific.

ISO C++ does not require `std::deque` to match a particular private block layout. Its standard clauses define observable complexity and invalidation. CPython's current source explicitly stores deque elements in a doubly linked list of fixed-length blocks, contradicting the legacy archive's claim that it “uses ring buffer.” Swift Collections currently advertises its Deque family as ring-buffer implementations. Current implementation claims must stay tied to sources/versions.

**Linked deques reuse doubly linked invariants.** A circular sentinel or head/tail doubly linked list gives constant link work at both ends. Each element pays two links and usually allocation/indirection. Known-node middle erasure can be constant link work, but minimal deque semantics need only endpoints. Intrusive variants separate membership from object ownership.

Arrays/rings generally favor compact storage; linked nodes favor stable identities and splice. Segmented designs sit between. Choose with element size, capacity, iteration, random access, stable-reference, allocator, and latency requirements—not an abstract table alone.

**Full policy changes semantics.** A capacity-bounded deque can reject push at either end without changing D. A dropping deque with maximum length can accept and evict the opposite end. Python `deque(maxlen=k)` documents bounded behavior; callers must understand which old element is discarded when new elements arrive.

For histories, automatic oldest eviction can be intended. For a work queue, silent eviction may be data loss. APIs should return the evicted element/count or provide explicit metrics where loss matters. Count capacity may be insufficient for variable-size values; maintain checked byte/weight accounting.

Bulk insertion that exceeds capacity needs exact policy: reject all, accept prefix, retain last k, evict from opposite end, or error. Each affects source order and observable removed values. Do not extrapolate one-element semantics carelessly.

**Middle operations are not the deque's main promise.** Indexing can be constant in ring/segmented representations, linear in linked ones. Inserting near an end can move the shorter side in an array deque; middle insertion can still be linear. Searching is linear absent another index. Exposing a general sequence API creates more invalidation and failure rules than an endpoint adaptor.

Rotation can be a head-index change only in a full circular buffer or under carefully relocated live/spare interpretation; with spare capacity, arbitrary head change can make holes appear live. General rotation may move pointers/elements or perform endpoint operations. Use the exact library contract, not a ring intuition.

**Monotonic deques store candidates, not every answer.** For sliding maximum of array `a` and window width k, store indices whose values are strictly decreasing (or nonincreasing under a tie policy). Before processing index i, remove front indices outside `[i-k+1,i]`. Remove back indices whose values cannot beat `a[i]`, then append i. Front is the maximum candidate.

Every index is appended once and removed at most once from each end, so total deque operations are O(n), yielding O(n) time under constant endpoint work. The deque can hold at most k indices. Equal-value tie policy determines whether older or newer equal candidates survive and can affect reported index while leaving maximum value unchanged.

The legacy archive's monotonic-window insight is useful, but its reported machine timings and “zero allocations” claims do not transfer universally. Python deque may allocate blocks as it grows and interpreter/runtime costs vary. Preserve the aggregate proof; benchmark the target environment separately.

**Work-stealing deques are asymmetric concurrent algorithms.** A common scheduler lets an owner push/pop one end while thieves steal the other. This encourages local LIFO depth-first behavior and exposes older work to thieves, but the exact algorithm defines semantics. Chase-Lev-style dynamic circular deques coordinate top/bottom counters, the last-item race, resizing, publication, and stolen snapshots.

An ordinary library deque protected only for individual endpoint calls does not automatically implement work stealing. Compound empty-check/pop, task ownership, shutdown, and resizing still race. Lock-free progress is not wait freedom; thieves can retry or starve. Memory ordering, counter wrap, ABA, array lifetime after resize, and reclamation require formal/implementation-specific reasoning.

**Thread-safe methods do not compose automatically.** Python documents thread-safe appends/pops for deques, but a multi-step invariant such as “if nonempty, inspect then remove the same value” requires a lock or an atomic combined operation. Portability requires the documented language/runtime contract rather than legacy claims about the GIL or private locks.

Java concurrent deque classes, blocking deques, and work-stealing schedulers have different fairness, waiting, iterator, and consistency contracts. Select the needed abstraction instead of wrapping a general deque and assuming stronger behavior.

**Evidence targets both ends and every boundary.** A sequence model can use a simple list. Generate all four endpoint operations, peek both ends, clear, bulk operations, rotation if supported, growth, bounded rejection/eviction, and iterator creation/mutation. After each operation compare logical order, size, live slots/nodes, capacity, and retained references.

For circular implementations emphasize capacity zero/one, head zero, wrap at both ends, exact full, alternating operations, growth while wrapped, maximum arithmetic, self-aliasing input, allocation/element failure, and two-span export. For segmented layouts force block/map boundaries and map growth. For dropping deques verify exact evicted identities and metrics.

Benchmark endpoint mixes, iteration, random access if promised, bulk operations, growth, block transitions, wrap, memory/allocations, latency distributions, and realistic algorithms such as sliding windows. Concurrent/work-stealing validation needs histories, schedule exploration, memory/race tools, forced resize/reuse, last-item races, stalled thieves, overload, and shutdown.

The following Python trace verifies a bounded circular deque. `None` is an educational spare marker and prohibited as data.

<!-- bijux-verify: {"id":"bounded-circular-deque-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=X,A,B,D\nfront=X\nback=D\nsize=4\ncapacity=5\nhead_index=4\nwrapped=True\noverflow_rejected=True\ninvariant=True\nevidence=finite_circular_deque_trace\n","stderr":""}} -->
```python
class CircularDeque:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("negative capacity")
        self.storage = [None] * capacity
        self.head = 0
        self.size = 0

    def _physical(self, logical):
        if not 0 <= logical < self.size or not self.storage:
            raise IndexError(logical)
        return (self.head + logical) % len(self.storage)

    def push_back(self, value):
        if value is None or self.size == len(self.storage):
            return False
        index = (self.head + self.size) % len(self.storage)
        self.storage[index] = value
        self.size += 1
        return True

    def push_front(self, value):
        if value is None or self.size == len(self.storage):
            return False
        self.head = len(self.storage) - 1 if self.head == 0 else self.head - 1
        self.storage[self.head] = value
        self.size += 1
        return True

    def pop_front(self):
        if self.size == 0:
            raise LookupError("empty deque")
        value = self.storage[self.head]
        self.storage[self.head] = None
        self.head = (self.head + 1) % len(self.storage)
        self.size -= 1
        return value

    def pop_back(self):
        if self.size == 0:
            raise LookupError("empty deque")
        index = self._physical(self.size - 1)
        value = self.storage[index]
        self.storage[index] = None
        self.size -= 1
        return value

    def values(self):
        return [self.storage[self._physical(i)] for i in range(self.size)]

    def invariant(self):
        if not 0 <= self.size <= len(self.storage):
            return False
        if self.storage and not 0 <= self.head < len(self.storage):
            return False
        live = {self._physical(i) for i in range(self.size)}
        return all((value is not None) == (i in live) for i, value in enumerate(self.storage))


deque = CircularDeque(5)
for item in ("A", "B", "C"):
    assert deque.push_back(item)
assert deque.push_front("Z")
assert deque.pop_back() == "C"
assert deque.push_back("D") and deque.push_back("E")
overflow_rejected = not deque.push_front("Y")
assert deque.pop_front() == "Z"
assert deque.pop_back() == "E"
assert deque.push_front("X")

values = deque.values()
print(f"values={','.join(values)}")
print(f"front={values[0]}")
print(f"back={values[-1]}")
print(f"size={deque.size}")
print(f"capacity={len(deque.storage)}")
print(f"head_index={deque.head}")
print(f"wrapped={deque.head + deque.size > len(deque.storage)}")
print(f"overflow_rejected={overflow_rejected}")
print(f"invariant={deque.invariant()}")
print("evidence=finite_circular_deque_trace")
```

## Definitions and Notation

| Term or symbol | Meaning |
|---|---|
| `D` | Abstract front-to-back sequence. |
| front/back | Two designated logical endpoints. |
| `h` | Physical index of logical front in a circular representation. |
| `n`, `c` | Logical size and physical element capacity. |
| `phys(i)` | `(h+i) mod c` for valid logical i when c>0. |
| wrapped | Live logical order crosses the physical end of storage. |
| segmented deque | Deque whose elements occupy several blocks. |
| dropping deque | Bounded history that accepts by evicting according to policy. |
| monotonic deque | Candidate deque ordered by value plus expiration. |
| owner/thief | Asymmetric roles in a work-stealing deque. |
| endpoint work | Core manipulation at front/back, excluding other costs unless stated. |

## Mechanisms, Invariants, or Proof Structure

**ADT proof.** Each of four endpoint equations adds/removes exactly one correct sequence end; peek returns the corresponding value unchanged. Stack/queue specializations follow by restricting calls.

**Circular proof.** `0<=n<=c`, normalized h for c>0, and `phys(i)` maps n logical indices injectively into live slots. Each endpoint transition changes h/n and one slot so the new mapping yields the required sequence. Capacity zero is handled before modulo.

**Growth proof.** Allocate checked larger storage, transfer logical i in order using old mapping, establish one live destination per element, then commit new buffer/head/capacity or clean partial state under the failure guarantee.

**Monotonic proof.** Front indices are in-window; stored indices increase; candidate values follow the chosen monotonic/tie order. Removed-back candidates cannot become a future maximum before the new item expires. Each index enters once and leaves at most once, giving O(n) total endpoint work.

**Cost conclusion.** Circular fixed endpoint work is worst-case constant under bounded element operations; growth adds linear transfers and yields amortized bounds. Segmented endpoint operations may allocate at block/map boundaries. Linked endpoints use constant links with node allocation. Concurrent claims require separate algorithms.

## Alternatives and Trade-Offs

- **Circular array:** compact reuse and indexing; wrap, resize, and two-span rules.
- **Segmented blocks:** endpoint growth without moving all elements; block/map metadata and noncontiguity.
- **Doubly linked nodes:** stable nodes and splice; link/allocation overhead and poor locality.
- **Persistent functional deque:** immutable versions/sharing; balancing schedules and retention complexity.
- **Rejecting bounded deque:** preserves existing contents and reports full; producer handles refusal.
- **Dropping bounded history:** always accepts under element policy; explicit opposite-end data loss.
- **Growable deque:** avoids fixed full policy until resource limit; growth latency, peak memory, and invalidation.
- **Endpoint adaptor:** small stable API; full sequence container exposes indexing/middle operations and more contracts.
- **Strict deque versus monotonic deque:** ordinary deque stores requested sequence; monotonic structure deliberately discards dominated candidates.
- **Locked general deque versus work-stealing deque:** locking supplies broad mutual exclusion; specialized ownership can increase concurrency with far harder proof.

## Failure Modes and Misconceptions

1. **“Deque is another spelling of queue.”** It permits both-end insertion and removal.
2. **“All deques are ring buffers.”** Libraries use rings, blocks, links, or other representations.
3. **“Equal endpoints mean empty.”** They can also mean full unless state distinguishes them.
4. **“Modulo fixes every wrap.”** Zero capacity and pre-modulo integer overflow/underflow remain.
5. **“Wrapped storage is contiguous.”** Logical data can occupy two physical spans.
6. **“Push is worst-case constant.”** Growth or block/map allocation can add work.
7. **“Bounded insertion always rejects.”** Some deques evict an old element instead.
8. **“Efficient ends imply efficient middle edits.”** Middle work can remain linear.
9. **“Rotation is always one index change.”** Spare/live layout may require movement.
10. **“Python deque uses a circular array.”** Current CPython source uses linked fixed-length blocks.
11. **“A monotonic deque contains the whole window.”** It contains only undominated candidates.
12. **“Equal-value tie policy does not matter.”** It can change which index survives.
13. **“Atomic endpoint methods make compound logic atomic.”** Check-then-act still races.
14. **“Work stealing is just pop from the other end.”** Owner/thief races, resizing, ordering, and reclamation define the algorithm.
15. **“Lock-free means every thief succeeds quickly.”** Per-operation starvation/retry can remain.
16. **“Legacy timing proves current speed.”** Hardware, runtime, version, inputs, and allocation state must be reproduced.

## Worked Examples

### Example 1

From `<A,B>`, push-front X gives `<X,A,B>` and push-back Y gives `<X,A,B,Y>`. Pop-front returns X; pop-back returns Y; `<A,B>` remains. Conclusion: one orientation makes all four endpoints unambiguous.

### Example 2

Capacity five, h=4, n=4 maps logical indices to physical `4,0,1,2`. The elements are wrapped but iteration yields the logical order. Conclusion: physical sorting by slot would be wrong.

### Example 3

With c=0, computing `(h+n)%c` is invalid even though the deque is empty. Push must first reject or grow. Conclusion: zero capacity precedes modular arithmetic.

### Example 4

A full rejecting deque `<A,B,C>` refuses push-front X and remains unchanged. A max-length dropping deque accepts X and evicts C, becoming `<X,A,B>`. Conclusion: capacity policy changes observable semantics.

### Example 5

A growable wrapped ring transfers logical positions 0..n-1 into a larger contiguous destination. Copying physical storage order would rotate the sequence. Conclusion: growth follows the abstraction mapping.

### Example 6

CPython's deque crosses a block boundary and allocates/links another fixed-length block; Rust VecDeque wraps in a growable ring. Both support efficient endpoints through different mechanisms. Conclusion: contracts can align while layouts differ.

### Example 7

For values `4,2,2,5` with window three, a sliding-max deque can remove older equal 2 or retain it under a tie policy; maximum values remain `4,5`, but chosen argmax indices differ. Conclusion: tie semantics matter for identity outputs.

### Example 8

Each index in a monotonic maximum algorithm is appended once; after it is dominated or expires it is removed once and never returns. At most 2n removals/additions yield linear total deque work. Conclusion: aggregate analysis, not per-step pruning count, proves the bound.

### Example 9

Two individually thread-safe calls `if d: x=d[0]; d.popleft()` can observe another thread removing x between inspection and pop. Conclusion: method atomicity does not compose into a transaction.

### Example 10

A work-stealing scheduler passes endpoint tests but fails the one-item owner/thief race during resize. Ordinary deque correctness did not prove memory ordering, array lifetime, or linearization. Conclusion: specialized concurrency needs specialized evidence.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns work stealing, owner/thief permissions, atomics, linearizability, memory ordering, and reclamation.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns modular arithmetic, uninitialized slots, blocks, allocators, spans, and raw lifetime.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops monotonic windows, 0-1 BFS, palindrome methods, aggregate proofs, and benchmarks.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) connects worklists, schedulers, and traversal frontiers.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects run queues, per-core scheduling, stealing, caches, NUMA, and wakeup behavior.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns overload, bounded histories, dropping metrics, and capacity operations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns arithmetic corruption, stale slots, retention, exhaustion, and malicious window sizes.

## References

1. ISO C++ working draft, [`deque`](https://eel.is/c%2B%2Bdraft/deque). Observable random-access sequence, endpoint/middle operations, complexity, capacity, modifiers, invalidation, and exception behavior.
2. Rust Project, [`VecDeque`](https://doc.rust-lang.org/std/collections/struct.VecDeque.html). Current growable ring-buffer representation, endpoint operations, logical iteration, two slices, and `make_contiguous`.
3. Oracle, [Java SE 25 `Deque`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Deque.html). Double-ended interface, paired failure forms, capacity-restricted variants, stack/queue mappings, and iteration.
4. Oracle, [Java SE 25 `ArrayDeque`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/ArrayDeque.html). Current array-deque API, growth, null policy, endpoint operations, iteration, and fail-fast limitations.
5. Python Software Foundation, [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque). Endpoint methods, bounded max length, eviction, rotation, indexing, copying, and documented thread-safe appends/pops.
6. Python Software Foundation, [CPython `_collectionsmodule.c`](https://github.com/python/cpython/blob/main/Modules/_collectionsmodule.c). Current linked fixed-length-block implementation, block length, endpoint paths, rotation, clear, and reentrancy handling.
7. Apple, [Swift Collections](https://github.com/apple/swift-collections). Current DequeModule ring-buffer family, value/unique/rigid ownership variants, release status, and public API policy.
8. David Chase and Yossi Lev, [Dynamic Circular Work-Stealing Deque](https://www.cs.wm.edu/~dcschmidt/PDF/work-stealing-dequeue.pdf). Primary SPAA paper for a dynamically growing circular work-stealing algorithm and its owner/thief setting.
9. Python Software Foundation, [C API Stability](https://docs.python.org/3/c-api/stable.html). Public versus limited/stable ABI boundaries and why private CPython representation details are not portable extension contracts.
10. Oracle, [Java SE 25 `ConcurrentLinkedDeque`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ConcurrentLinkedDeque.html). Current concurrent deque contract, weakly consistent iteration, memory effects, null policy, and size complexity.

## Exercises

### Exercise 1

Specify the Deque ADT and show how stack and FIFO queue APIs arise by restricting endpoint operations.

### Exercise 2

Prove a fixed-capacity circular deque's mapping and all four endpoint transitions, including c=0, full/empty, wrap, and slot lifetime.

### Exercise 3

Design grow, bulk prepend/append, and max-length eviction semantics with checked sizes, aliasing, failure, invalidation, and returned eviction evidence.

### Exercise 4

Derive a monotonic deque for sliding maximum, including equal-value tie policy, invariant, correctness, and O(n) aggregate work.

### Exercise 5

Prepare an evidence plan for adopting a dynamic circular work-stealing deque in a production scheduler.

## Answers to the Exercises

### Answer 1

D is a finite front-to-back sequence. Push-front prepends, push-back appends, nonempty pop-front removes/returns first, nonempty pop-back removes/returns last, and peeks observe corresponding ends. Empty/full policies are explicit. A stack uses push/pop on the same selected end, yielding LIFO. A FIFO queue pushes at one end and pops the other, preserving admission order. Restricting the API does not change representation but removes operations clients may rely on, enabling future implementation changes.

### Answer 2

For c>0 maintain `0<=n<=c`, normalized `0<=h<c`, and live physical set `{(h+i)%c | 0<=i<n}` containing D[i] exactly once; all other slots non-live. Push-back constructs at `(h+n)%c`; push-front selects predecessor h then constructs; pop-front clears h then advances h and decrements; pop-back clears `(h+n-1)%c` then decrements. Prove injectivity because two logical indices differing by less than c cannot be congruent modulo c. Size distinguishes empty/full. For c=0, reject or grow before modulo. Check pre-modulo arithmetic/underflow, construct-before-publish, return-before-destroy, and reference clearing.

### Answer 3

Compute required elements/bytes with checked arithmetic and maximum policy. For growth, allocate c', traverse old logical order through its mapping, construct destinations, then atomically commit or clean partial state; physical observers invalidate. Bulk order equals repeated endpoint operations under a stated source order; snapshot or forbid self-aliasing; choose all-or-nothing or successful-prefix failure. For max length, define exact opposite-end eviction for each insertion and oversized bulk behavior, return evicted values/counts or durable metrics, clear/destroy them exactly once, and distinguish eviction from rejection. Count and byte capacities can both apply.

### Answer 4

Store indices in increasing order and values in decreasing order. For each i, remove front while index `<i-k+1`; remove back while value is less than `a[i]`, or less-than-or-equal if newer equal values should replace older; append i. Front is in-window and dominates every later stored candidate; removed expired indices are invalid, while a back candidate removed by a newer no-smaller value cannot become maximum before that newer index expires. Each i is appended once and removed at most once, so total endpoint operations and time are O(n), space O(k). State the tie policy when returning argmax identity.

### Answer 5

Specify owner push/pop end, thief end, empty/last-item race, linearization points, progress, task ownership, resize, shutdown, cancellation, and counter limits. Reproduce the exact algorithm and memory model; prove publication, snapshot array lifetime, top/bottom ordering, compare-and-swap race, counter wrap, ABA, and reclamation with stalled thieves. Keep a locked scheduler as model. Use schedule/linearizability exploration, forced one-item races, resize at wrap, address reuse, memory/race tools, stress, stalled owners/thieves, overload, cancellation, and shutdown. Measure steal success/retries, locality, CPU, memory, throughput, and latency tails. Require named concurrency, runtime, allocator, reliability, security, operations, and independent review; the paper and endpoint tests do not certify the implementation.
