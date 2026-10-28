---
module_id: DSE-012
program: Data Structures Engineering
level: 1
module_number: 12
title: Dynamic Arrays and Geometric Growth
status: complete
last_verified: 2026-09-04
---

# Dynamic Arrays and Geometric Growth

## One-Page Review

### Governing question

How can a dynamic array preserve contiguous sequence semantics while changing capacity, and which proof, invalidation, failure, memory, and latency obligations make geometric growth safe and honestly described?

### Essential definitions

- A **dynamic array** is a variable-length sequence represented by a contiguous backing allocation plus logical length and capacity metadata.
- **length/size** $n$ counts live elements; **capacity** $c$ counts element slots available before another allocation is required.
- **spare capacity** is the region of slots `[n,c)`; for nontrivial element types it is storage, not a sequence of live default elements.
- A **growth policy** selects a new capacity $c'\ge n+k$ when appending $k$ elements would exceed $c$.
- **geometric growth** chooses capacities that increase by a factor $\alpha>1$, up to rounding, minimum-capacity, required-size, and maximum-size rules.
- **reallocation** obtains different storage and transfers live elements; it can invalidate pointers, references, iterators, slices, and foreign views according to the API.
- **reserve** requests capacity for future elements without changing logical length; exactness and growth policy are contract-specific.
- **amortized cost** bounds total cost across every permitted operation sequence under a stated cost model; it does not cap each individual operation.
- **hysteresis** separates growth and shrink thresholds to prevent repeated grow/shrink oscillation near one boundary.
- **deamortization** spreads rebuilding work across operations using an explicit transitional representation so per-operation work can be bounded under stronger assumptions.

### Central model, mechanism, or theorem

State is $(B,n,c)$ with invariants

$$
0\le n\le c\le c_{max},
$$

live initialized sequence in slots `[0,n)`, and spare non-element storage in `[n,c)`. If `append(x)` finds $n<c$, it constructs at slot $n$ and increments length only after success. If $n=c$, it checks a new capacity, allocates, transfers exactly the $n$ live elements, constructs `x`, commits the new state, and releases the old storage under its failure guarantee.

For doubling from capacity 1, capacities copied before $N$ successful single-element appends form

$$
1+2+4+\cdots+2^{m-1}=2^m-1<N.
$$

Thus fewer than $N$ prior elements are copied and $N$ new elements are written: total unit element work is below $2N$, although a resize append can cost $\Theta(n)$. The potential $\Phi=2n-c+1$ gives amortized cost at most 3 under the chapter's explicit append/copy unit model.

### Critical invariants

1. `0 <= length <= capacity <= maximum`, and capacity byte size is representable and allocatable.
2. Slots below length contain exactly the logical sequence in order; spare slots are never read or destroyed as live elements.
3. Length changes only after successful construction of the new logical element.
4. A reallocation either commits one valid new representation or leaves the stated valid old representation; partial transfers are cleaned exactly once.
5. Every alias or view follows documented invalidation and lifetime rules across growth, insertion, erasure, reserve, shrink, move, and destruction.
6. Growth and shrink policies satisfy their claimed aggregate bounds under rounding and maximum-capacity rules.
7. Amortized, peak-latency, peak-memory, allocation, and element-transfer claims remain distinct.

### Common failures

- Treating capacity as logical length or spare bytes as initialized elements.
- Assuming every implementation doubles, exposes capacity, or honors an exact reserve request.
- Computing growth or byte size with overflowing arithmetic.
- Publishing new length before element construction succeeds.
- Moving elements, then failing, without a valid rollback or documented weaker guarantee.
- Holding pointers, iterators, slices, or FFI views across an operation that may reallocate.
- Forgetting that append can reuse storage, so old and returned views may still alias.
- Shrinking at the same utilization threshold used for growth and creating resize thrashing.
- Calling amortized constant time a worst-case latency guarantee.
- Benchmarking only pre-reserved appends while claiming default growth behavior.

### Compact example

Start with capacity 1 and append nine integers under doubling. Growth copies 1 element at capacity 1, then 2, 4, and 8: 15 copied elements total. Nine new-element writes produce 24 unit writes, capacity ends at 16, and the capacity trace after each append is `1,2,4,4,8,8,8,8,16`. The observed ratio `24/9` is not the asymptotic proof; the geometric-series argument establishes the bound for arbitrary $N$ in the stated model.

### Connections

[DSE-011](011-fixed-arrays.md) supplies the backing-array layout, initialization, and checked-index foundation. [DSE-003](003-operation-contracts.md) supplies failure guarantees, [DSE-004](004-time-space-and-allocation-cost.md) supplies amortized and peak resource models, [DSE-008](008-iterators-and-traversal-protocols.md) supplies invalidation semantics, [DSE-009](009-property-based-testing-of-data-structures.md) supplies stateful testing, and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supplies evidence discipline.

## Governing Question

What state machine, capacity rule, transfer protocol, amortized proof, and API contract allow a dynamic array to grow while preserving sequence values—and when do memory, latency, aliasing, concurrency, or failure requirements demand another design?

## Why This Matters

Dynamic arrays power vectors, lists, byte buffers, builders, column batches, and adjacency storage because they combine constant-time indexed access with variable logical length. Their convenience hides a representation transition: once capacity is exhausted, the implementation may allocate a larger fixed array, move or copy every live element, update metadata, and release old storage. The abstract append is simple; the concrete operation can fail, invalidate aliases, temporarily double memory, execute user code, and create a latency spike.

Geometric growth is the central solution to repeated-copy cost, but “it doubles and append is O(1)” is an incomplete explanation. Common production libraries deliberately leave the growth factor unspecified. Element transfer can throw or panic, allocation can fail, zero-sized types can have special capacity, and views can retain an old allocation. A defensible design separates required semantics from policy, proves total work for the actual rule, and exposes or contains invalidation and resource effects.

## Prerequisites and Retrieval

Before this module, retrieve:

- fixed-array extent, layout, initialization, one-past, views, and overflow from [DSE-011](011-fixed-arrays.md);
- representation state, abstraction functions, and transition invariants from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- strong/basic/no-effect failure guarantees and alias contracts from [DSE-003](003-operation-contracts.md);
- aggregate, accounting, potential, allocation, peak-memory, and tail-cost reasoning from [DSE-004](004-time-space-and-allocation-cost.md);
- element move/copy/drop constraints from [DSE-007](007-genericity-and-type-constraints.md);
- iterator/view invalidation and evidence methods from [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify a dynamic array's abstract sequence and `(buffer,length,capacity)` representation invariant;
2. implement append as a transactional state transition over initialized and spare storage;
3. derive aggregate and potential proofs for doubling and general geometric growth under explicit cost models;
4. distinguish amortized throughput from resize latency, peak memory, allocator calls, and element side effects;
5. design overflow-safe `reserve`, bulk append, maximum-size, and allocation-failure behavior;
6. explain reference, pointer, iterator, slice, and FFI invalidation across reallocation and in-place mutation;
7. analyze growth-factor, preallocation, shrinking, hysteresis, and memory-retention trade-offs;
8. compare C++ vector, Rust Vec, Java ArrayList, Go slices, Python lists, and .NET List without assuming their private growth factors;
9. design stateful, fault-injection, sanitizer, and benchmark evidence for growth boundaries;
10. determine when stable addresses, hard latency, bounded memory, concurrency, or high-stakes review require another representation.

## Core Exposition

**Separate abstract length from physical capacity.** The abstract value is a finite sequence $A=\langle a_0,\ldots,a_{n-1}\rangle$. The representation stores a backing allocation $B$, length $n$, and capacity $c$. Only slots `[0,n)` are live elements and observable through ordinary indexing/iteration. Slots `[n,c)` are reserve storage. For reference-based runtimes they may contain implementation values; for low-level generic storage they may be logically uninitialized. In neither case does capacity add elements to the abstract sequence.

The central invariant is `0 <= n <= c <= max_size`. The backing storage must support at least $c$ properly aligned slots under checked byte arithmetic. The abstraction function reads exactly the live prefix. Any debug interface that exposes spare storage creates additional initialization, aliasing, and information-leak obligations.

**Append is a commit protocol.** With spare capacity, append constructs or assigns the new element into slot $n$, then publishes $n+1$. If construction fails, length remains $n$, and cleanup follows the element/API guarantee. Publishing length first would make a failed or concurrent observer see uninitialized/nonexistent data.

When full, a strong conceptual protocol is:

1. compute `required = n + k` with checked arithmetic for the incoming count;
2. choose $c'\ge required$, respecting maximum element and byte limits;
3. acquire storage for $c'$ slots;
4. transfer live elements in order under copy/move/relocation rules, tracking the constructed prefix;
5. construct incoming elements, including self-alias cases defined by the API;
6. if a step fails, destroy newly constructed objects and release new storage, preserving the promised old state when possible;
7. atomically at the abstraction level commit `(B',n+k,c')`;
8. destroy old moved/copied elements as required and release old storage.

Real implementations can reorder steps for performance and type traits, but must prove equivalent ownership and failure behavior. A move that can fail after modifying its source may prevent a strong guarantee. Some specifications condition guarantees on whether a type is nothrow-movable or copyable. Do not advertise “append has no effect on failure” without accounting for allocator and element operations.

**Growth policy is policy, not essence.** A geometric rule can be written

$$
c'=\max(required,c_{min},\lceil\alpha c\rceil),\qquad \alpha>1,
$$

with special handling at zero and near `max_size`. Production rules may change factors by size, use allocator size classes, choose the smallest sufficient allocation for bulk append, or retain implementation freedom. Java `ArrayList`, Rust `Vec`, Go `append`, C++ `vector`, Python `list`, and .NET `List<T>` should be used through their documented guarantees, not reverse-engineered growth constants treated as API.

Before multiplying capacity by $\alpha$, check whether required size already exceeds the geometric candidate and whether either exceeds element/byte limits. Integer wrap can select a small capacity followed by out-of-bounds construction. APIs should distinguish arithmetic/capacity overflow from allocator exhaustion where their ecosystem supports it. Fallible reservation enables callers to recover without relying on process termination or unwinding.

**Aggregate proof for doubling.** Suppose capacity begins at 1; a successful append costs one unit to construct the new element, and growth additionally costs one per existing element copied. Immediately before the $(N+1)$-st slot would be needed, copied capacities are powers of two smaller than the final range. Their sum is less than $N$. Thus $N$ successful appends perform $N$ new writes plus fewer than $N$ copy writes: total below $2N$, so amortized element work is $O(1)$.

This is deterministic over every append sequence under this model; it is not an average over random inputs. It also excludes allocator internals, destructor effects, page faults, cache traffic, and failed operations unless added to the cost model. Rounding and a different factor change constants, not the geometric conclusion when the factor remains bounded away from one and capacity progress is guaranteed.

For general $\alpha>1$, old capacities form a geometric series whose sum is proportional to final capacity with factor roughly $1/(\alpha-1)$, subject to rounding. A factor close to one reduces immediate slack but increases allocation/copy frequency and constants. A large factor reduces copying but increases unused capacity and peak allocation. The “best” factor depends on allocator behavior, element size, workload lifetime, memory budget, and latency.

**Potential proof for doubling.** Under initial `(n=0,c=1)` and reachable nonempty invariant $n\le c\le2n$, choose $\Phi=2n-c+1$. It is nonnegative and initially zero. A no-growth append has actual cost 1 and increases potential by 2, for amortized cost 3. At a full state `n=c`, growth to `2n` and append has actual cost `n+1`; potential changes from `n+1` to 3, so $\Delta\Phi=2-n$ and amortized cost is 3. Telescoping bounds total actual cost by total amortized cost.

Potential is an analysis device, not stored runtime credit. The proof establishes a sequence bound for the defined state transitions. It does not make the expensive operation physically fast or reserve memory for future growth.

**Latency and peak space tell different stories.** At capacity $n$, a growth append can transfer $n$ elements and cost $\Theta(n)$. During allocate-copy-free growth, old and new buffers coexist, so peak element storage can approach $c+c'$, plus allocator metadata and temporaries. Virtual reservation, in-place expansion, relocation primitives, garbage collection, and reference sharing change observed peaks but require evidence.

Pre-reserving a known final size can remove intermediate reallocations and preserve addresses until that capacity is exceeded. It may also overallocate, retain memory, increase working set, or fail earlier. Benchmark both default growth and relevant reservation policy; do not pre-reserve only the preferred implementation while claiming ordinary append performance.

**Reallocation is an invalidation event.** For pointer-like contiguous containers, moving storage changes element addresses. C++ vector specifications define which operations reallocate and the resulting iterator/reference invalidation. Rust borrowing normally prevents safe simultaneous mutation through a borrowed slice, while unsafe raw pointers still require discipline. Java iterators have modification/fail-fast rules but references to element objects differ from references into contiguous slots. Each ecosystem needs its own exact table.

Go makes an especially useful aliasing lesson: a slice is a descriptor of an underlying array. `append` reuses the underlying array when capacity suffices and allocates a new one otherwise. The returned slice must be used. Old and new slices can alias after one append but not after another, depending on capacity. Correct code must not assume either outcome unless it controls capacity and contract.

An index often survives relocation as a numeric position, but insertion/erasure before it can change which element occupies that position. Stable IDs need a separate indirection/generation scheme. FFI consumers, device kernels, asynchronous I/O, and stored callbacks cannot retain a data pointer across possible growth unless ownership freezes capacity or an explicit pin/lease prevents mutation.

**Insertion and erasure add movement.** Appending affects the end; inserting at position $i$ shifts $n-i$ elements even without reallocation. Erasing shifts later elements left and destroys one logical element. Overlap-safe move direction, exception behavior, self-references, and invalidation must be specified. Bulk operations should reserve once when size is known, yet input ranges can alias the destination or be single-pass, and `required=n+k` still needs checking.

Removal does not imply capacity shrink. Retaining capacity makes refill cheap and avoids allocator churn but can hold large memory. `shrink_to_fit`, `trimToSize`, or equivalent is often a request with language/library-specific strength. It can reallocate and invalidate views. Security-sensitive code must not assume removed or freed capacity is overwritten; use a documented secure-erasure facility when required.

**Shrinking needs hysteresis.** If growth occurs at full capacity and shrink occurs immediately near the same boundary, alternating append/remove operations can trigger repeated $\Theta(n)$ transfers. A common analytical policy grows by two and shrinks only at utilization at most one quarter, perhaps to half capacity. Between a shrink and the next grow, sufficiently many net inserts are required to pay for rebuilding. The exact thresholds and potential need proof, rounding rules, minimum capacity, and workload analysis.

Automatic shrinking is not always desirable: oscillating workloads, allocator fragmentation, pointer stability, and cache warming can favor retention. Expose an explicit compaction operation or application lifecycle boundary when predictable reclamation is more valuable than automatic response.

**Deamortization is a different representation.** To bound per-operation transfer, an incremental design maintains old and new storage simultaneously plus migration progress and a rule locating every logical element. Appends during migration need a defined destination; reads and writes may consult/mutate one or both buffers; erasure and insertion interact with the frontier; iterators need a coherent order; failures and destruction need exactly-once ownership; and concurrency needs synchronization.

Copying a constant number of elements per operation can bound migration work, but allocation itself, zero-initialization, page commitment, element callbacks, and allocator pauses can still violate a hard latency bound. A real-time claim requires a suitable allocator/storage strategy and worst-case evidence or proof for every step. The simple instruction “allocate double and copy later” is not enough when the old buffer is already full.

**Testing must target transitions.** Stateful model tests compare the live prefix against a simple sequence across append, insert, erase, reserve, clear, shrink, and failure. Generate lengths exactly below/at/above capacity boundaries, bulk sizes, zero capacity, maximum arithmetic, aliasing inputs, throwing/move-only/resource-owning elements, and repeated grow/shrink cycles. Inject allocation and element-transfer failure at every step; check old/new value guarantees and leak/double-destroy counts. Sanitizers and unsafe interpreters address memory errors; they do not prove the growth policy or exception guarantee.

Benchmark capacity traces, allocation counts, bytes copied/moved, total work, individual resize latency, peak memory, and steady append separately. Record implementation/tool versions because private growth policy can change. Correctness and invalidation tests remain distinct from timing. A geometric curve observed over a few sizes does not replace the amortized proof.

**Concurrency requires external or owned synchronization.** A dynamic array mutation can change metadata, construct elements, and relocate the entire buffer. Concurrent readers or writers cannot safely use old state without a language-supported synchronization, ownership, copy-on-write, snapshot, read-copy-update, or specialized concurrent design. Spare capacity does not make unsynchronized `push` safe: threads race on length and slot ownership even without allocation.

For security and high-stakes systems, bound attacker-controlled reserve/append counts, account for peak old-plus-new memory, handle allocation failure, validate serialized lengths, avoid stale raw views, and control data remanence. An amortized bound is not a denial-of-service bound or deadline guarantee. Clinical or control-system use also requires domain, hazard, resource, operational, and regulatory review beyond the container proof.

The following standard-library-only model makes every growth and copy explicit under doubling. `None` represents spare educational storage; the values inserted here exclude `None`, so it is never ambiguous with a live value.

<!-- bijux-verify: {"id":"explicit-doubling-growth-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=(0, 1, 2, 3, 4, 5, 6, 7, 8)\nlength=9\ncapacity=16\ncapacity_trace=(1, 2, 4, 4, 8, 8, 8, 8, 16)\ncopied_elements=15\ntotal_unit_writes=24\ninvariant=True\nevidence=finite_growth_trace_not_complexity_proof\n","stderr":""}} -->
```python
class EducationalDynamicArray:
    def __init__(self):
        self.buffer = [None]
        self.length = 0
        self.copied = 0

    @property
    def capacity(self):
        return len(self.buffer)

    def append(self, value):
        if value is None:
            raise ValueError("None is reserved for spare storage")
        if self.length == self.capacity:
            new_buffer = [None] * (self.capacity * 2)
            for index in range(self.length):
                new_buffer[index] = self.buffer[index]
                self.copied += 1
            self.buffer = new_buffer
        self.buffer[self.length] = value
        self.length += 1

    def values(self):
        return tuple(self.buffer[: self.length])

    def invariant(self):
        return (
            0 <= self.length <= self.capacity
            and all(value is not None for value in self.buffer[: self.length])
            and all(value is None for value in self.buffer[self.length :])
        )


array = EducationalDynamicArray()
capacities = []
for number in range(9):
    array.append(number)
    capacities.append(array.capacity)

print(f"values={array.values()}")
print(f"length={array.length}")
print(f"capacity={array.capacity}")
print(f"capacity_trace={tuple(capacities)}")
print(f"copied_elements={array.copied}")
print(f"total_unit_writes={array.copied + array.length}")
print(f"invariant={array.invariant()}")
print("evidence=finite_growth_trace_not_complexity_proof")
```

This trace establishes the educational implementation's nine-element behavior and counters. It does not prove the general amortized theorem, validate a production allocator or generic element type, or measure runtime performance, invalidation, failure safety, concurrency, and peak resident memory.

## Definitions and Notation

Let $A\in T^n$ be the abstract sequence, $B$ the current backing storage, $n=len(A)$, $c$ capacity, and $c_{max}$ the maximum permitted element count after byte/layout constraints. The **utilization/load** is $u=n/c$ for positive $c$. A **capacity trace** records capacity after each operation.

Let actual operation cost be $a_i$, potential $\Phi(s)\ge0$, and amortized cost $\hat a_i=a_i+\Phi(s_i)-\Phi(s_{i-1})$. Telescoping relates their sums. This chapter's unit model charges one for a new-element construction and one per transferred element; real models add allocation, destruction, callbacks, bytes, or time.

A pointer/reference/view is **invalidated** when its later use is outside contract, even if the numerical address happens to remain readable. **Peak capacity** and **peak live memory** differ because allocators, old/new overlap, references, and garbage collection can retain additional storage.

## Mechanisms, Invariants, or Proof Structure

Representation preservation splits append into spare and full cases. The spare case maintains the live-prefix invariant by constructing at exactly $n$ before increment. The full case uses a temporary representation with a constructed-prefix counter; rollback destroys exactly that prefix, while commit swaps ownership only after the new live sequence is complete under the promised guarantee.

The doubling aggregate proof follows the finite geometric identity $\sum_{j=0}^{m-1}2^j=2^m-1$. The potential proof follows from nonnegative $\Phi=2n-c+1$ over reachable states and amortized cost 3 in both cases. Both quantify element-unit work; neither bounds one resize's actual cost.

For shrink/grow hysteresis, prove a minimum number of net operations between opposite resizes and charge the later transfer to those operations, or supply a piecewise potential covering sparse and dense regimes. Threshold equality, integer rounding, minimum capacity, failed operations, and bulk changes belong in the proof.

## Alternatives and Trade-Offs

- **Geometric growth** gives linear total transfer and spare memory; fixed increments reduce slack locally but can yield quadratic total copying.
- **Larger growth factors** reduce reallocations; smaller factors reduce immediate slack. Allocator size classes complicate both.
- **Reserve** can improve latency/address stability for known demand; it can increase early failure and retained memory.
- **Automatic retention** favors refill and stable capacity; explicit shrink favors reclamation but may reallocate and invalidate.
- **Copy transfer** can preserve the old value on failure; move/relocation can be cheaper but needs type and exception guarantees.
- **Contiguous dynamic arrays** favor indexing/traversal; segmented/deque/tree structures can offer stable addresses or bounded growth work.
- **Amortized resizing** keeps a simple representation; incremental migration adds metadata and access complexity for stronger latency goals.
- **Index handles** survive relocation but not positional insert/erase semantics; stable IDs add indirection and generations.
- **Copy-on-write/snapshots** support readers; writes, retention, identity, and concurrency become more complex.
- **Fallible reserve APIs** enable recovery; infallible/panicking APIs simplify callers but restrict failure control.

## Failure Modes and Misconceptions

1. **“Capacity elements already exist.”** Only the live prefix belongs to the sequence.
2. **“Every vector doubles.”** Growth factor is often an unspecified implementation detail.
3. **“Reserve exact means allocator bytes are exact.”** API and allocator may still provide more; inspect the contract.
4. **“Amortized O(1) means every append is fast.”** A resize can transfer all live elements.
5. **“Average case and amortized mean the same thing.”** Amortized analysis can be deterministic over every sequence.
6. **“Reallocation only changes capacity.”** It can invalidate every address-based observer and execute element operations.
7. **“An old slice always aliases after append.”** It depends on whether backing storage was reused.
8. **“Removing elements frees memory.”** Capacity commonly remains allocated until explicit shrink/destruction.
9. **“Shrink whenever utilization falls.”** Without hysteresis, alternating operations can thrash.
10. **“Move makes growth infallible.”** Allocation and element move/relocation rules still matter.
11. **“A pointer that still has the same bits is valid.”** Lifetime and invalidation are contractual, not accidental readability.
12. **“Preallocation proves normal append performance.”** It measures a different lifecycle configuration.
13. **“Incremental copying guarantees hard constant latency.”** Allocation, initialization, callbacks, pages, and coordination also need bounds.
14. **“Spare capacity makes concurrent append safe.”** Length publication and slot ownership still race.

## Worked Examples

### Example 1

Appending nine values under doubling copies 1+2+4+8=15 prior elements and writes nine new ones. The finite count illustrates the mechanism; the geometric-series proof establishes the sequence bound.

### Example 2

Growing by a fixed 100 slots copies approximately 100+200+...+N elements before size $N$, which is quadratic in the number of fixed-size growth steps. Fixed increments are appropriate only under a bounded demand or different cost model.

### Example 3

For $n=c=2^{63}$, computing `2*c` in an unsigned 64-bit type wraps. A correct policy first compares required and maximum capacities, uses checked arithmetic, and reports length overflow rather than attempting a small allocation.

### Example 4

A caller reserves 10,000 elements, obtains an FFI pointer, and appends within reported capacity. A contract like Rust Vec guarantees no reallocation for push while capacity suffices, but insertion, foreign asynchronous lifetime, custom allocator, and other APIs still require exact review.

### Example 5

Two Go slices share a backing array. Appending within capacity changes the returned slice over shared storage; appending beyond capacity allocates new storage. Assign the return and never infer aliasing solely from equal earlier contents.

### Example 6

A C++ vector transfer of resource-owning elements fails on element $k$. Exception safety depends on element copy/move traits and the operation's specified guarantee; cleanup must destroy exactly the successfully constructed new prefix without double-owning resources.

### Example 7

An interactive editor alternates between sizes 1,000,000 and 1,000,001. Automatic shrink/grow at the same threshold can repeatedly copy the whole sequence. Retention or separated thresholds eliminate that oscillation at the cost of spare memory.

### Example 8

A service receives a declared list length of four billion small records. It checks maximum count and total peak old-plus-new memory before reserve, rejects beyond policy, and avoids turning amortized efficiency into a memory-exhaustion attack.

### Example 9

A benchmark reports pre-reserved append throughput, default-growth total throughput, distribution of individual append latency, transfer count, allocation count, and peak memory separately. This exposes both aggregate advantage and resize spikes.

### Example 10

A dynamic medication-event buffer can be model-tested for order and loss, but capacity policy alone cannot establish clinical completeness, deadline safety, durable recovery, privacy, audit retention, or deployment capacity. Those need system and domain evidence.

## Cross-Program Connections

- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns allocation, relocation, destruction, unsafe spare capacity, and fallible reserve interfaces.
- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains failure guarantees, moves, ownership, aliases, exceptions, and undefined behavior.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops aggregate, accounting, potential, hysteresis, and deamortization proofs.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns publication, races, snapshots, copy-on-write, and migration synchronization.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains allocators, virtual reservation, page commitment, memory pressure, and resident peaks.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains transfer bandwidth, cache effects, NUMA placement, and false sharing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns integer overflow, exhaustion, stale pointer, remanence, and untrusted-length threat models.

## References

1. ISO C++ working draft, [`vector` Overview](https://eel.is/c++draft/vector.overview). Contiguous container representation surface, types, capacity, access, and modifiers.
2. ISO C++ working draft, [`vector` Capacity](https://eel.is/c++draft/vector.capacity). Size/capacity, reserve, shrink request, reallocation, invalidation, and complexity.
3. ISO C++ working draft, [`vector` Modifiers](https://eel.is/c++draft/vector.modifiers). Insert/append/erase effects, reallocation, invalidation, complexity, and exception guarantees.
4. Rust Project, [`std::vec::Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html). Pointer-length-capacity guarantees, live/spare layout, reserve, reallocation, shrink, zero-sized types, and unspecified growth policy.
5. Rust Project, [Rustonomicon: Implementing Vec](https://doc.rust-lang.org/nomicon/vec/vec.html). Unsafe allocation, growth, initialization, pointer, and destruction obligations in an educational implementation.
6. Oracle, [Java SE 25 `ArrayList`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/ArrayList.html). Capacity, ensure/trim operations, constant-amortized add, fail-fast iteration, synchronization, and unspecified growth detail.
7. Go Project, [Go Specification: `append`](https://go.dev/ref/spec#Appending_and_copying_slices). Reuse versus allocation, sufficient new backing array, overlapping append, and result semantics.
8. Go Project, [Go Slices: Usage and Internals](https://go.dev/blog/slices-intro). Array-backed slice descriptors, length/capacity, aliasing, reslicing, copying, and growth.
9. Python Software Foundation, [CPython `listobject.c`](https://github.com/python/cpython/blob/main/Objects/listobject.c). Current production source for list allocation, resizing, transfer, and implementation-specific overallocation.
10. Python Software Foundation, [Python/C API: List Objects](https://docs.python.org/3/c-api/list.html). Public list construction, item access, initialization, mutation, and stable-ABI boundaries.
11. Microsoft, [.NET `List<T>.Capacity`](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.capacity). Logical count/capacity distinction, reallocation, maximum capacity, and trim/ensure operations.

## Exercises

### Exercise 1

Specify and prove single-element append for a generic dynamic array, including spare and growth paths, overflow, failure, and destruction.

### Exercise 2

Derive aggregate and potential bounds for doubling from capacity 1, then explain exactly what neither proof establishes.

### Exercise 3

Design a grow-and-shrink policy with hysteresis. Give thresholds, rounding/minimum rules, an amortized argument, and adversarial tests.

### Exercise 4

Create an invalidation and alias matrix for append, reserve, insert, erase, clear, shrink, move, and destruction in one chosen ecosystem.

### Exercise 5

Prepare a verification and evidence plan for a latency-sensitive, security-sensitive dynamic buffer receiving untrusted records.

## Answers to the Exercises

### Answer 1

State `(B,n,c)` with checked `0<=n<=c<=max`, live initialized prefix `[0,n)`, and spare storage `[n,c)`. With spare capacity, construct `x` at `n`; on success increment length, on failure leave length and live prefix unchanged. When full, checked-add required size, select and validate `c'`, allocate, transfer in order while tracking constructed prefix, construct `x`, then commit new ownership/metadata; rollback destroys only new live objects and preserves the promised old state. Element copy/move traits determine achievable guarantee. On commit, destroy/release old representation exactly once. Prove abstraction is old sequence followed by `x` in both cases and include self-alias and allocator failure in the contract.

### Answer 2

For $N$ appends, copied full capacities are powers of two whose sum is below $N$; adding $N$ new writes gives total element work below $2N$. With $\Phi=2n-c+1$, reachable `c<=2n` states make potential nonnegative; a spare append has amortized 3, and a full append costing `n+1` changes potential by `2-n`, also 3. Telescoping bounds the sequence. Neither establishes worst-case append latency, allocator time, byte traffic for variable-size elements, exception/failure behavior, peak old-plus-new memory, address stability, concurrency, cache performance, or a production library's private factor.

### Answer 3

For an analytical policy, grow from full positive `c` to `2c`; after removal, shrink to `c/2` only when `n<=c/4`, never below minimum 1, with explicit floor/ceiling and checked arithmetic. After shrinking, utilization is at most one half; reaching full requires $\Theta(c)$ net appends, while reaching the next shrink requires $\Theta(c)$ net removals, so transfers can be charged to intervening operations. A rigorous solution supplies aggregate charging or a piecewise potential for append and pop. Test equality at thresholds, odd capacities, zero/one, bulk changes, failures, alternating boundary sequences, maximum size, capacity traces, total transfers, and abstraction equality. Production choice can prefer no automatic shrink.

### Answer 4

Use the selected ecosystem's normative/library documentation rather than a generic table. For each operation record whether reallocation can/must occur; which element addresses, iterators, indices, end positions, subviews, and foreign pointers remain valid; whether element identity/order shifts; and failure effects. Append may preserve addresses only without reallocation; reserve can invalidate if it reallocates; insert/erase can invalidate at/after a position even without allocation; clear destroys elements while perhaps retaining capacity; shrink may reallocate; move transfers or changes ownership under type rules; destruction invalidates all observers. Include Go-style conditional backing-array aliasing or Java object-reference semantics only when relevant.

### Answer 5

Define maximum records/bytes and peak old-plus-new budget; use checked required-size/capacity arithmetic and fallible allocation; validate record lengths before reserve; separate spare storage from live values; specify failure rollback, cleanup, cancellation, remanence, view leasing, and no stale FFI/asynchronous pointers. Model/property-test all growth boundaries and malicious sizes, inject allocation/transfer failures, run memory/race/undefined-behavior tools, verify leak/double-destroy counters, and retain deterministic regressions. Benchmark individual resize latency, tail distribution, allocation/page effects, peak resident memory, and default versus reserve on target systems. Hard deadlines require deamortized/bounded allocation design and worst-case evidence. Security, reliability, operations, privacy, domain, safety, quality, human-factors, and regulatory owners review their scopes; finite tests and amortized proofs do not establish deployment fitness.
