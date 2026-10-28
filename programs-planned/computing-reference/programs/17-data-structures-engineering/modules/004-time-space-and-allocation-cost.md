---
module_id: DSE-004
program: Data Structures Engineering
level: 1
module_number: 4
title: Time, Space, and Allocation Cost
status: complete
last_verified: 2026-08-29
---

# Time, Space, and Allocation Cost

## One-Page Review

### Governing question

How should an engineer specify and validate the time, space, and allocation costs of a data structure without confusing asymptotic proofs, implementation constants, allocator behavior, and measurements from one machine?

### Essential definitions

- A **cost model** assigns abstract costs to selected primitive operations; every complexity claim is relative to one.
- **worst-case cost** is the maximum cost over admitted inputs and valid states of a stated size.
- **average-case cost** is an expectation under an explicit probability distribution over inputs or states.
- **expected cost** is an expectation over declared randomness, which may come from the algorithm, inputs, or both.
- **amortized cost** bounds total cost across every allowed operation sequence, without assuming a probability distribution.
- **auxiliary space** is additional working storage beyond the representation of the input and required output.
- **live space** is storage reachable and semantically needed at an observation point; **peak live space** is its maximum during an operation or trace.
- **retained space** is storage still held by a runtime, allocator, cache, or pool even when not part of the abstract value.
- **allocation count** counts allocation events; **allocated bytes** counts requested or usable allocation volume; neither alone equals peak memory.
- **slack** is reserved capacity not currently occupied by live elements; **fragmentation** is unusable or poorly reusable space caused by layout and allocation history.

### Central model, mechanism, or theorem

For operation trace (sigma=o_1,ldots,o_m), define actual time cost (c_i), allocation events (a_i), requested bytes (b_i), and live-space function (L(t)). Report distinct quantities:

\[
C(\sigma)=\sum_{i=1}^{m}c_i,\qquad
A(\sigma)=\sum_{i=1}^{m}a_i,\qquad
B(\sigma)=\sum_{i=1}^{m}b_i,
\]

\[
L_{peak}(\sigma)=\max_t L(t).
\]

An amortized bound assigns charges (hat c_i) or potential (Phi_i\ge0) so that every prefix satisfies

\[
\sum_{i=1}^{j}c_i\le\sum_{i=1}^{j}hat c_i
\]

or (hat c_i=c_i+Phi_i-Phi_{i-1}). Mathematical bounds and empirical measurements answer different questions and must be reported separately.

### Critical invariants

- Every cost claim names the operation, input/state size, workload or sequence, cost model, and quantifier.
- Worst-case, expected, average-case, amortized, and high-probability guarantees are never used interchangeably.
- Time proofs count declared primitives; wall-clock measurements include implementation, runtime, operating system, and hardware effects.
- Space reports distinguish payload, metadata, slack, working memory, transient copies, allocator overhead, fragmentation, and retained caches where relevant.
- Allocation reports distinguish count, requested bytes, usable bytes, lifetime, peak coexistence, and deallocation behavior.
- An amortized proof covers every allowed sequence and does not claim a per-operation latency bound.
- Integer overflow, maximum capacity, address-space limits, and allocation failure remain part of the operation contract.
- Benchmarks pin implementation, toolchain, configuration, workload, machine, warm-up, repetitions, and statistical summary.
- Instrumentation overhead and observer scope are documented.
- Finite timings can refute a claimed implementation behavior but do not prove asymptotic complexity.

### Common failures

Common failures are writing “fast” or `O(1)` without a model; presenting amortized cost as worst-case latency; calling hash lookup constant without distribution or adversarial assumptions; counting elements but ignoring per-node metadata and allocator rounding; equating cumulative allocated bytes with peak memory; measuring resident memory and calling it object size; timing setup with the operation; reporting the fastest run only; extrapolating from tiny inputs; and treating a clean profiler trace as a proof that no allocation occurs.

### Compact example

A dynamic array that doubles capacity has worst-case (\Theta(n)) append when it copies (n) elements, but (\Theta(1)) amortized append across every sequence starting empty. At size just above (n/2), its reserved slots are below (n), yet a resize can temporarily coexist with the old and new buffers, raising peak storage. Exact bytes also include element representation, alignment, allocator metadata, and runtime policy. One label—“constant append”—cannot express all of this.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) separates abstract value from representation. [DSE-002](002-representation-invariants.md) supplies capacity/size invariants. [DSE-003](003-operation-contracts.md) makes resource guarantees observable contracts. DSE-005 and DSE-006 develop layout and locality; DSE-010 develops benchmarking in depth.

## Governing Question

When two structures implement the same abstract operations, how do we reason about which consumes less time and memory for a workload—and how do we keep proof, cost-model approximation, runtime allocation, and physical measurement from collapsing into one misleading number?

A linked list and dynamic array both represent sequences. A RAM-model table may say insertion at a known list node is constant while array insertion is linear. On real machines, finding the node, allocating it, following pointers, cache misses, branch prediction, and allocator synchronization can dominate. The asymptotic statement may be correct and still answer the wrong workload question.

## Why This Matters

Data structures turn workload shape into resource behavior. A representation with low steady-state bytes can require large transient copies. A design with low allocation count can retain large arenas. Expected constant-time hashing can fail under adversarial collisions. Amortized constant append can violate a hard latency deadline during resize.

Resource claims also affect reliability. Allocation failure, integer overflow, fragmentation, garbage-collector pressure, memory limits, and latency tails are correctness concerns when they cause rejection, eviction, missed deadlines, or process termination. A production-grade choice needs mathematical bounds plus measured evidence at the relevant abstraction boundary.

## Prerequisites and Retrieval

You should know functions, summations, logarithms, powers, basic probability, arrays, pointers/references, and DSE-001 through DSE-003. Retrieve:

1. Big-O is an asymptotic upper-bound relation, not an exact runtime.
2. A data-structure operation begins in a valid state and may change both state and capacity.
3. A representation invariant can relate size, capacity, nodes, and cached metadata.
4. A contract must say whether a cost is worst-case, amortized, or expected.
5. Measurement observes one implementation/configuration/environment, not a mathematical function directly.

## Learning Objectives

After completing this module, you should be able to:

- define an operation-specific cost function and choose an appropriate cost model;
- distinguish worst, best, average, expected, amortized, and high-probability costs;
- prove a simple amortized bound with aggregate, accounting, and potential reasoning;
- decompose representation space into payload, metadata, slack, and working storage;
- distinguish live, peak-live, retained, resident, virtual, and cumulative allocation measures;
- count allocation events and reason about allocation lifetime and peak coexistence;
- compare asymptotic predictions with reproducible measurements without overclaiming;
- detect workload, adversary, overflow, and resource-limit assumptions hidden in cost claims;
- write a multidimensional cost contract for an operation;
- review a data structure for both average efficiency and tail/resource safety.

## Core Exposition

**Choose the question before the notation.** Complexity is a property of a specified operation under a size measure and model. For lookup in a map, size may be number of entries (n), key length (ell), table capacity (m), or all three. Hash computation is not constant when keys have variable length. A precise bound might be (O(\ell+1)) expected probes under stated hashing assumptions, not simply `O(1)`.

For a graph adjacency structure, input size may be vertices (V) and edges (E). For range reporting, output size (k) matters. For a persistent update, path length and number of shared nodes matter. State the parameters rather than hiding them in one (n).

**Cost models.** The unit-cost RAM model counts word-sized reads, writes, arithmetic, comparisons, and control steps as constant, assuming words can address the represented memory. A comparison model counts key comparisons and is useful for ordered dictionaries. A pointer-machine model restricts navigation. External-memory models count block transfers. Cache-aware and cache-oblivious analyses introduce block/cache parameters. DSE-006 and DSE-071 onward develop machine and storage models further.

A model is useful when its primitives approximate the dominant scarce resource and support proof. It is not a literal processor. Multiplication, hashing, allocation, system calls, cache misses, and arbitrary-precision arithmetic are not universally unit cost. State deviations explicitly.

**Asymptotic bounds.** (T(n)\in O(f(n))) means there exist constants (c,n_0) such that (T(n)\le cf(n)) for all (n\ge n_0). (\Omega) gives a lower bound; (\Theta) gives both. The notation suppresses constants and lower-order terms, so it ranks growth rather than predicting a crossover on a particular machine.

Worst-case cost maximizes over valid states and inputs of the declared size. Best case rarely supports a client guarantee but can explain fast paths. Average case needs a probability distribution; “typical” is not a distribution. Expected cost must identify whether randomness belongs to inputs, hash seeds, randomized balancing, or scheduling. An adaptive adversary may observe prior behavior, invalidating independence assumptions.

High-probability bounds state a failure probability as a function of size, for example at most (n^{-c}). An expectation alone permits rare large costs. Latency-sensitive services need tail distributions or hard bounds in addition to mean/expected analysis.

**Amortized analysis.** Amortization is deterministic sequence analysis. It proves a total bound for every permitted operation sequence; it does not average over random inputs. A single operation can remain expensive.

The aggregate method totals a sequence then divides. For a stack with `multipop(k)`, every pushed element can be popped at most once, so (m) operations perform (O(m)) total pushes/pops and have (O(1)) amortized cost.

The accounting method overcharges cheap operations and stores credits. Every prefix must keep the bank nonnegative; borrowing from future operations would not prove a bound for a sequence that stops early. For a binary counter, charge a 0-to-1 flip enough to fund its later 1-to-0 flip.

The potential method defines nonnegative stored work (\Phi(state)). Amortized cost

\[
\hat c_i=c_i+\Phi(D_i)-\Phi(D_{i-1})
\]

telescopes. If (\Phi(D_0)=0) and (\Phi\ge0), actual total cost is at most total amortized cost. Potential belongs to the analysis, not necessarily a runtime field.

**Dynamic-array growth.** Suppose capacity starts at one and doubles when full. An append without growth writes one element. Growth from capacity (q) allocates (2q) slots, copies (q) elements, then writes the new element. Before reaching capacity (2^k), total copies are

\[
1+2+4+\cdots+2^{k-1}=2^k-1.
\]

Thus total copies across (n) appends are below a constant multiple of (n), giving constant amortized writes/copies. The growing append itself is still linear in current size.

Growth factor (g>1) trades slack against copying frequency. Factors near one reduce unused capacity but increase total copying; larger factors reduce reallocations but can reserve more space. Integer rounding, maximum capacity, allocator size classes, and in-place growth change constants. Shrinking at the same threshold as growth can oscillate; hysteresis separates thresholds.

**Space is multidimensional.** Abstract payload is the information clients intend to store. Representation space adds object headers, pointers, hashes, control bytes, lengths, capacity, alignment, padding, allocator metadata, and slack. A node storing one eight-byte value may consume several times that amount once pointers, header, alignment, and allocation rounding are included.

Logical size (n) does not determine exact bytes without element representation and runtime layout. Shallow-size functions generally exclude separately allocated referents. Recursive “deep size” risks double-counting shared objects and following caches or global interned values. State the ownership graph and counting policy.

Auxiliary space excludes input and required output under the selected algorithmic convention. In-place often means (O(1)) or sublinear auxiliary storage, not zero memory traffic. Recursion consumes stack frames. Iterators, temporary buffers, remembered sets, and runtime bookkeeping can matter even when source code declares no container.

**Live, peak, retained, resident, and virtual space.** Live space follows objects/references considered reachable and necessary under a defined ownership scope. Peak live space is the maximum during an operation/trace. A resize can require old and new buffers simultaneously, so transient peak exceeds both steady states.

Retained memory includes freed capacity held in pools, arenas, thread caches, or language runtimes for reuse. Resident set size counts physical pages attributed to a process under operating-system policy and includes code, stacks, shared pages, allocators, and unrelated objects. Virtual size includes mapped address ranges not necessarily resident. These measurements answer different questions.

Garbage collection adds allocation-rate and lifetime effects. Short-lived nodes can increase collection frequency even if peak live bytes stay low. Generational collectors, reference counting, tracing, compaction, and escape analysis change costs. Report runtime/version and collection controls when relevant.

**Allocation metrics.** Count allocation events, requested bytes, usable/rounded bytes, peak simultaneously live allocations, lifetimes, frees, and reallocations as needed. Cumulative allocated bytes can be enormous in a constant-memory loop because the same space is repeatedly allocated and freed. Conversely, one arena allocation can hide many logical object creations.

An allocation is not a constant-time mathematical primitive in all contexts. It may take locks, refill size classes, map pages, zero memory, trigger collection, invoke destructors, or fail. Pooling shifts cost to initialization, retention, and reclamation. Allocation elimination can improve latency while increasing retained memory.

Fragmentation has internal and external forms. Internal fragmentation is unused space within allocated units due to rounding or capacity. External fragmentation is free space split so it cannot satisfy requests efficiently. Precise definitions depend on allocator. Do not infer fragmentation by subtracting shallow object sizes from RSS.

**Peak coexistence and failure.** A copy-based resize may allocate the new buffer before releasing the old, so peak slots can approach old plus new capacity. If the allocation fails, DSE-003's failure contract decides whether the old structure remains intact. In-place reallocation may reduce copying but has allocator- and platform-specific behavior.

Capacity arithmetic must check overflow before multiplication/addition. Maximum-size APIs should account for addressable bytes, element size, allocator limits, and reserved metadata. A theoretical (O(n)) structure is not safe if `n * element_size` wraps.

**Workload-sensitive totals.** Operation mixtures matter. A structure with fast lookup and expensive rebuild may suit read-heavy workloads but fail bursty writes. Model traces including initial fill, steady state, churn, scans, deletion, clear, reuse, concurrency, and destruction. Report distribution and ordering, not only operation percentages.

For a workload (W), total cost can be a vector rather than one score:

\[
Cost(W)=(time,tail,peak\ bytes,allocations,bytes\ allocated,IO,contention).
\]

Weighting dimensions into one scalar is a product decision and can hide hard limits. Use feasibility constraints first, then compare Pareto trade-offs.

**Measurement as model checking.** Benchmarking asks how one implementation behaves under a controlled workload/environment. It can reveal incorrect scaling, excessive allocation, phase changes, or cost-model omissions. It cannot prove an asymptotic theorem because it samples finite sizes and conditions.

Record source/commit, compiler/interpreter and flags, dependencies, allocator/GC, CPU/memory/OS, frequency/power/container controls, input generation, setup exclusion, warm-up, sample count, statistic, uncertainty, and raw results. Use enough work per sample to exceed timer resolution and enough independent samples to characterize variability; fixed universal repetition counts are not scientifically meaningful.

Avoid dead-code elimination and constant folding in compiled benchmarks. Separate construction from the operation unless construction is the subject. Validate outputs so optimization cannot remove work. Randomize or balance order to reduce drift. Measure cold and warm behavior separately when both matter.

Median describes central tendency under skew; quantiles expose tails; confidence intervals require assumptions or appropriate resampling. Minimum time can approximate an uncontended lower envelope but must not be presented as typical. Outlier removal needs a prespecified, justified policy and raw-data retention.

Use allocation tracers, heap profilers, and runtime counters at the correct scope. Instrumentation can change allocation, scheduling, and caches; quantify or triangulate its effect. A profiler not observing native, child-process, device, or kernel memory cannot prove absence there.

The executable model below counts one abstract write per append, element copies during doubling, allocation events, capacity, and modeled peak slots. It does not measure Python list allocation or physical memory.

<!-- bijux-verify: {"id":"dynamic-array-cost-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"n=0 capacity=0 writes=0 copies=0 allocations=0 peak_slots=0\nn=1 capacity=1 writes=1 copies=0 allocations=1 peak_slots=1\nn=2 capacity=2 writes=2 copies=1 allocations=2 peak_slots=3\nn=3 capacity=4 writes=3 copies=3 allocations=3 peak_slots=6\nn=5 capacity=8 writes=5 copies=7 allocations=4 peak_slots=12\nn=9 capacity=16 writes=9 copies=15 allocations=5 peak_slots=24\nevidence=modeled_counts_not_memory_measurement\n","stderr":""}} -->
```python
class CostedArray:
    def __init__(self):
        self.size = 0
        self.capacity = 0
        self.writes = 0
        self.copies = 0
        self.allocations = 0
        self.peak_slots = 0

    def append(self):
        if self.size == self.capacity:
            old_capacity = self.capacity
            new_capacity = 1 if old_capacity == 0 else 2 * old_capacity
            self.allocations += 1
            self.copies += self.size
            self.peak_slots = max(self.peak_slots, old_capacity + new_capacity)
            self.capacity = new_capacity
        self.size += 1
        self.writes += 1
        self.peak_slots = max(self.peak_slots, self.capacity)


for target in (0, 1, 2, 3, 5, 9):
    model = CostedArray()
    for _ in range(target):
        model.append()
    print(
        f"n={model.size} capacity={model.capacity} writes={model.writes} "
        f"copies={model.copies} allocations={model.allocations} "
        f"peak_slots={model.peak_slots}"
    )
print("evidence=modeled_counts_not_memory_measurement")
```

## Definitions and Notation

Let (I_n) be admitted inputs/states of size (n), and (C(x)) actual primitive count in a declared model. Then

\[
C_{worst}(n)=\max_{x\in I_n}C(x),\qquad
C_{best}(n)=\min_{x\in I_n}C(x).
\]

For distribution (P_n), average cost is (E_{x\sim P_n}[C(x)]). For algorithmic random variable (R), expected cost can be (E_R[C(x,R)]) for fixed (x). Name both sources when both vary.

For representation (r), decompose modeled bytes as

\[
M(r)=payload+metadata+slack+allocator\ overhead,
\]

under a declared ownership/counting policy. Working memory (W(t)) and retained/runtime memory are reported separately. Allocation event (e) has requested size, usable size if observable, time, lifetime, and owner.

An amortized charge sequence is valid if every prefix dominates actual cost. Potential analysis additionally requires an initial bound and lower bound sufficient for telescoping.

## Mechanisms, Invariants, or Proof Structure

**Cost-claim audit.** Identify operation, parameters, valid-state family, workload/quantifier, primitive model, bound type, and hidden assumptions. Reject a claim missing any dimension needed by clients.

**Aggregate proof.** Sum actual work across a trace and bound repeated participation. In a doubling array, each completed capacity contributes once to copying, producing a geometric series.

**Accounting proof.** Assign credits to operations or objects; establish nonnegative balance after every prefix; show all actual work is paid. Credits are analytical, not runtime currency.

**Potential proof.** Choose (Phi(state)\ge0), calculate actual plus potential change in every operation case, and telescope. Show starting/ending potential terms rather than omitting them.

**Space accounting.** Draw the ownership graph, count each allocation once, separate shallow payload/metadata from referents, and model maximum simultaneously live states during updates.

**Measurement correspondence.** State which theoretical primitive a metric approximates, which layers it includes, and which it cannot observe. Compare slopes or normalized work only over justified regimes.

**Executable evidence boundary.** The snippet implements abstract counters for isolated arrays. It proves its printed arithmetic for six targets only; it is not a Python allocator, heap, cache, latency, or asymptotic experiment.

## Alternatives and Trade-Offs

**Exact counting versus asymptotics.** Exact counts expose constants and small-input behavior but depend tightly on implementation/model. Asymptotics transfer across sizes and implementations but suppress crossovers and machine costs. Use both at their appropriate layer.

**Worst-case versus amortized design.** Amortization often improves throughput and simplicity. Incremental resizing/deamortization can bound tails but adds state, branches, and invariant complexity.

**Compactness versus allocation churn.** Shrinking eagerly reduces slack but can reallocate repeatedly. Hysteresis or retention reduces churn while consuming more memory.

**Per-object allocation versus arenas.** Individual allocation simplifies lifetime and reclamation. Arenas reduce overhead/localize memory but retain space and couple object lifetimes.

**Cached metadata versus recomputation.** Cached size/hash/summary improves query time at added bytes and update obligations. Recalculation saves representation space but repeats work.

**Generic versus specialized representation.** Boxing and pointers support heterogeneous/generic values but add indirection and metadata. Unboxed specialization improves density at code-complexity and compatibility cost.

**Microbenchmark versus end-to-end workload.** Microbenchmarks isolate mechanisms and scaling. End-to-end tests include realistic interactions but make attribution harder. Neither alone answers both causality and product impact.

## Failure Modes and Misconceptions

1. **“Big-O is runtime.”** It is a relation on growth under a cost model, not seconds.
2. **“Average means amortized.”** Average requires probability; amortized covers sequences without probability.
3. **“Expected O(1) is worst-case O(1).”** Rare or adversarial inputs may be much slower.
4. **“Amortized constant gives constant latency.”** A resize can still be linear.
5. **“Space complexity is object size.”** Headers, referents, slack, working storage, allocator and runtime layers differ.
6. **“Cumulative allocated bytes is peak memory.”** Reused short-lived allocations inflate cumulative volume without simultaneous liveness.
7. **“RSS is data-structure memory.”** It includes unrelated and shared process pages under OS accounting.
8. **“No allocation in a profiler means none occurred.”** Scope, sampling, optimization, native layers, and instrumentation limits matter.
9. **“More repetitions always improve a benchmark.”** Correlated or biased measurements remain biased.
10. **“The fastest sample is performance.”** It is not typical or tail behavior.
11. **“Doubling wastes half the memory.”** Slack depends on size relative to capacity; transient copies and allocator rounding add different costs.
12. **“A lower asymptotic bound always wins.”** Constants, locality, size regime, and workload can dominate.
13. **“A benchmark proves complexity.”** Finite samples can support correspondence or refute implementation claims, not universal growth theorems.
14. **“Memory optimization is always safe.”** It may worsen latency, failure atomicity, concurrency, and implementation risk.

## Worked Examples

### Example 1

**Question:** What does worst-case `O(1)` stack push require?

**Reasoning:** A fixed-capacity stack can write/increment in constant RAM steps when not full; the precondition/capacity outcome is explicit. A growable array push is generally only amortized constant because reallocation copies elements.

**Conclusion:** Capacity and bound type belong in the claim.

### Example 2

**Question:** Why is hash lookup not simply constant?

**Reasoning:** Key hashing may cost (O(\ell)); probe count depends on load, hash distribution, collision strategy, and adversary. Expected constant probes needs assumptions; worst case can be linear.

**Conclusion:** State key-length and collision assumptions.

### Example 3

**Question:** How many copies occur before a doubling array reaches capacity 16?

**Reasoning:** Resizes copy 0, 1, 2, 4, and 8 existing elements; nonzero copies total 15. This is below the final capacity and linear in appended elements.

**Conclusion:** Geometric growth yields constant amortized copying.

### Example 4

**Question:** Can an (O(n))-space linked list use less memory than an (O(n))-space array?

**Reasoning:** Both have linear growth, but list nodes add pointers, per-allocation headers/rounding, and locality costs; arrays add slack and one header. Constants and element layout decide actual bytes.

**Conclusion:** Same asymptotic space does not imply comparable footprint.

### Example 5

**Question:** Why can freeing every node leave RSS high?

**Reasoning:** An allocator/runtime may retain arenas/pages for reuse, fragmentation may prevent page release, and RSS includes unrelated memory.

**Conclusion:** Abstract liveness, allocator retention, and process residency are different metrics.

### Example 6

**Question:** Does an arena eliminate allocations?

**Reasoning:** It replaces many external allocator calls with fewer arena allocations while retaining internal bump allocations and potentially longer lifetimes.

**Conclusion:** Report allocator events and logical object creation separately.

### Example 7

**Question:** How can a benchmark hide resize spikes?

**Reasoning:** Reporting total time divided by many appends shows amortized throughput; medians of batches can omit rare spikes. Per-operation latency or resize-aligned traces expose tails.

**Conclusion:** Measurement aggregation must match the contract.

### Example 8

**Question:** Why exclude setup from lookup timing?

**Reasoning:** Building and populating a structure measures construction plus lookup and can dominate. Include setup only when the workload actually reconstructs per query.

**Conclusion:** Benchmark scope follows the operational question.

### Example 9

**Question:** What does the snippet's `peak_slots=24` at (n=9) mean?

**Reasoning:** The model assumes old capacity 8 and new capacity 16 coexist during resize. It does not include element bytes, headers, allocator rounding, or reuse.

**Conclusion:** A modeled peak is not a heap measurement.

### Example 10

**Question:** A memory-bounded flight controller uses a dynamic structure. What exceeds asymptotic analysis?

**Reasoning:** Engineers need hard capacities, overflow and allocation-failure behavior, per-operation worst-case time, fragmentation/retention under the actual allocator, concurrency, startup and fault traces, hardware/toolchain identity, and independent timing/memory evidence. Domain, safety, security, quality, and regulatory reviewers validate the integrated control case. This chapter claims no such approval.

**Conclusion:** Asymptotic efficiency cannot establish real-time or safety fitness.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) owns asymptotic, amortized, randomized, and experimental analysis broadly.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies allocation, ownership, alignment, and failure mechanisms.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains virtual memory, pages, residency, and process accounting.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies caches, branches, bandwidth, and hardware-counter interpretation.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies benchmark design and evidence quality.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats adversarial complexity and resource exhaustion.

## References

1. Thomas H. Cormen et al., [*Introduction to Algorithms*, 4th ed.](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press. Asymptotic, probabilistic, amortized, and data-structure analysis.
2. Pat Morin, [*Open Data Structures*, Python edition](https://opendatastructures.org/ods-python.pdf). Geometric resizing, operation cost, amortized analysis, and space analysis.
3. Python Software Foundation, [`sys.getsizeof`](https://docs.python.org/3/library/sys.html#sys.getsizeof). Shallow object-size semantics and referent limitation.
4. Python Software Foundation, [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html). Allocation tracing, snapshots, peaks, domains, and limitations.
5. Python Software Foundation, [CPython Memory Management](https://docs.python.org/3/c-api/memory.html). Allocator domains, raw/memory/object interfaces, and runtime requirements.
6. Rust Project, [`std::alloc::Layout`](https://doc.rust-lang.org/std/alloc/struct.Layout.html). Allocation size, alignment, layout construction, and overflow constraints.
7. ISO C++ working draft, [Allocator requirements](https://eel.is/c++draft/allocator.requirements). Current allocation/deallocation interface and requirements.
8. Jason Evans et al., [`jemalloc` manual](https://jemalloc.net/jemalloc.3.html). Size classes, arenas, thread caches, statistics, profiling, and retention controls.
9. Google Benchmark Project, [User Guide](https://google.github.io/benchmark/user_guide.html). Benchmark setup, timing, repetitions, complexity fitting, counters, and reporting.
10. Valgrind Project, [Massif heap profiler manual](https://valgrind.org/docs/manual/ms-manual.html). Heap snapshots, peak analysis, stacks, allocation trees, and profiler scope.

## Exercises

### Exercise 1

For a dynamic array growing by factor two from capacity one, derive total copies and allocation count after (n) appends. Distinguish worst-case and amortized append cost.

### Exercise 2

Compare modeled space for 1,000 64-bit values in a contiguous array versus individually allocated doubly linked nodes. Define symbolic header, pointer, alignment, and allocator-rounding parameters rather than inventing platform constants.

### Exercise 3

Design an accounting or potential proof for a stack supporting `push`, `pop`, and `multipop(k)`. Prove the prefix/nonnegative condition.

### Exercise 4

Design a reproducible experiment that distinguishes dynamic-array amortized throughput from worst-case resize latency and allocation peaks. State what the experiment cannot prove.

### Exercise 5

Prepare a resource-assurance plan for a data structure used in a hard memory and latency budget. Include formal bounds, overflow, allocation failure, fragmentation, workload/adversary, measurement, tool identity, fault injection, and human review.

## Answers to the Exercises

### Answer 1

For (n=0), count is zero. For (n>0), capacities allocated are (1,2,4,\ldots,2^k), where (2^{k-1}<n\le2^k); allocation count is (k+1=\lceil\log_2 n\rceil+1) except exact powers require the same expression (and (n=1) gives one). Copies are (0+1+2+\cdots+2^{k-1}=2^k-1<2n). Each append writes once, so total modeled writes plus copies are (O(n)), yielding (O(1)) amortized cost. An append triggering growth from size (q) copies (q), so worst-case append is (\Theta(n)).

### Answer 2

Let array header be (H_a), per contiguous value eight bytes, capacity (c\ge1000), and total allocator rounding/metadata (R_a(c)). Modeled array bytes are (H_a+8c+R_a(c)), with slack (8(c-1000)). Let node object header be (H_n), two pointer fields of (p) bytes, value eight bytes, padding (P_n), and per-node allocation overhead/rounding (R_n). List plus container header (H_l) is (H_l+1000(H_n+2p+8+P_n+R_n)). This excludes separately allocated values and shared/runtime metadata unless the ownership policy includes them. Substitute measured platform-specific quantities only after pinning ABI, runtime, allocator, and measurement method.

### Answer 3

Charge `push` two units: one pays its insertion and one credit is stored on the pushed element. Charge `pop` and `multipop` zero beyond consuming stored credits: each removed element uses its one credit. At every prefix, credits equal the number of currently stored elements and are nonnegative because no element can be popped before it is pushed, and each is popped at most once. Hence total actual pushes plus removals is at most twice the number of pushes, which is at most twice the operation count; amortized cost is constant. Empty-pop checking adds constant actual/charged cost and does not affect the argument.

### Answer 4

Pin implementation, growth policy, element type, compiler/runtime, allocator, machine, OS, power/frequency policy, and source digest. Pre-reserve or start empty according to separate scenarios. Record per-append latency and mark capacity changes; report full distribution and resize-aligned maxima rather than only total/mean. Independently trace allocation events/requested/usable bytes and peak coexistence, validating profiler scope. Use sizes crossing several capacities, warm/cold variants, enough work for timer resolution, repeated independent trials, raw data, medians/quantiles and uncertainty. Confirm results and prevent optimization. The experiment can test this implementation/environment and expose scaling or contract violations; it cannot prove asymptotic bounds, all machines/workloads, absence of unobserved allocation, or real-time safety.

### Answer 5

Define exact maximum logical size, element/layout bounds, metadata/slack, transient copies, stack/auxiliary memory, retained allocator state, and concurrency multiplicity. Prove arithmetic cannot overflow and every operation respects worst-case time and space; amortized/expected arguments are insufficient for a hard per-call bound unless buffered by a proved schedule. Specify allocation-free steady state or failure outcomes, preallocation, fragmentation model, reclamation, and recovery. Model allowed and adversarial traces, then run implementation- and hardware-pinned timing/memory tests with allocation/fault injection, cold/warm/startup/shutdown, concurrency, long-duration churn, limits, and instrumentation cross-checks. Record compiler/linker/runtime/allocator/OS/configuration digests. Independent data-structure, real-time, systems, security, safety, quality, domain and regulatory reviewers approve their scopes; no benchmark or local proof alone establishes deployment fitness.
