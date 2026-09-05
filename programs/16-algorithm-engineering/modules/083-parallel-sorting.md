---
module_id: ALGE-083
program: Algorithm Engineering
level: 2
module_number: 83
title: Parallel Sorting
status: complete
last_verified: 2026-09-05
---

# Parallel Sorting

## One-Page Review

### Governing question

How should an engineer decompose sorting across finite processors so that the result is a permutation in total order, while work, span, movement, load balance, stability, numeric semantics, and failure behavior remain explicit?

### Essential definitions

- A parallel sort is correct when its output is both ordered by the declared comparator and a permutation of the exact input snapshot.
- **Work** counts total operations; **span** counts the longest dependency chain. Low span without work efficiency can waste processors.
- A **sorting network** is a data-independent sequence of compare-exchange layers. Disjoint comparators in one layer can execute concurrently.
- Parallel merge sort recursively sorts subranges and parallelizes merge; parallel quicksort partitions concurrently but needs defenses against skew.
- **Sample sort** locally sorts, samples keys, selects splitters, partitions into buckets, exchanges buckets, and locally merges or sorts them.
- **Oversampling** draws more splitter candidates to reduce bucket imbalance probability at additional sample and classification cost.
- A distributed sort must define global rank order, equal-key policy, ownership intervals, collective membership, and failure epoch.

### Central model, mechanism, or theorem

For $n$ keys, $P$ workers, total work $T_1$, and span $T_\infty$, any execution needs at least

$$
T_P\ge\max(T_1/P,T_\infty).
$$

A comparison sort also needs $\Omega(n\log n)$ comparisons in the decision-tree model. Parallelism can reduce elapsed comparison depth but not erase total information work. Practical algorithms therefore combine local sequential efficiency with balanced parallel partition, merge, or network layers. In sample sort, splitter quality controls the maximum receive bucket $b_{\max}$; the slowest worker and largest memory allocation scale with that maximum, not the average $n/P$.

### Critical invariants

- Comparator results form the promised ordering over every represented key, including exceptional values.
- Every input record belongs to exactly one partition and appears exactly once in output.
- Output partitions occupy nonoverlapping ordered key intervals; concatenating ranks yields global order.
- Equal-key records preserve original order if and only if stability is promised.
- Same-layer network operations touch disjoint locations, and recursive tasks do not race on overlapping ranges.
- Counts, offsets, buffer sizes, and messages agree before redistribution.
- Validation uses an input snapshot and contributor epoch consistent with the produced result.

### Common failures

Timing only local sorts; assuming equal input counts imply equal work; choosing splitters from biased samples; dropping or duplicating boundary-equal keys; reversing merge tie policy; comparing floating NaNs without a total policy; overflowing counts or displacements; creating too many tiny tasks; exhausting memory during all-to-all exchange; relying on an incidental collective barrier; accepting a failed-rank partial result; checking order without permutation; and reporting speedup against a weak or semantically different baseline.

### Compact example

Four workers receive 16 records. Local sorting costs are balanced, but deterministic regular samples choose splitters 4, 6, and 8. With a stable decorated order, receive bucket sizes become 8, 3, 3, and 2. The output is correct, yet the largest worker handles twice the average load. Correctness and load balance are separate obligations.

### Connections

[ALGE-081](./081-work-span-and-parallel-dependency.md) supplies work/span and scheduling bounds. [ALGE-082](./082-parallel-prefix-and-reduction.md) supplies prefix offsets and collective reasoning. [ALGE-013](./013-merge-sort.md), [ALGE-014](./014-quicksort-and-partitioning.md), and [ALGE-016](./016-counting-radix-and-bucket-sorting.md) supply sequential mechanisms. ALGE-085 and ALGE-086 next separate external-memory models and external sorting.

## Governing Question

Given records, comparator semantics, processor and memory topology, distribution, stability and reproducibility requirements, and a failure model, which parallel sorting design delivers a verified ordered permutation without hiding work inflation, imbalance, communication, or semantic changes?

## Why This Matters

Sorting is a systems primitive as much as an algorithm. It groups equal keys, establishes merge order, builds indexes, enables range partitioning, canonicalizes output, schedules events, and prepares joins. At scale, comparison cost may cease to dominate: reading keys, moving records, allocating buffers, synchronizing levels, sampling a skewed population, and exchanging buckets can decide performance.

The sequential phrase “sort this array” hides choices that parallel execution exposes. Is the order stable? Are keys unique? Can the comparator run concurrently? Is it a total order on NaNs and locale-dependent strings? May records move, or only indexes? Is output replicated or distributed? Can a worker fail? A fast kernel that answers a different one of those questions is not an optimization.

Parallel sorting is also an excellent exercise in separating models. A sorting network has deterministic comparison locations and depth. PRAM results show what is possible under ideal shared-memory assumptions. Task-parallel merge and partition expose real dependency graphs. Sample sort exposes probabilistic or deterministic load balance plus communication. GPUs and clusters expose bandwidth, topology, and finite buffers. Production design has to connect these levels without conflating them.

## Prerequisites and Retrieval

Retrieve comparison lower bounds and adversary arguments from [ALGE-008](./008-lower-bounds-and-adversary-arguments.md), merge invariants from [ALGE-013](./013-merge-sort.md), partition invariants from [ALGE-014](./014-quicksort-and-partitioning.md), stability and indirect sorting from [ALGE-018](./018-stable-sorting-and-indirect-sorting.md), distribution-aware selection from [ALGE-020](./020-engineering-a-sort-for-real-data-distributions.md), work/span from [ALGE-081](./081-work-span-and-parallel-dependency.md), and scans from [ALGE-082](./082-parallel-prefix-and-reduction.md). You should be able to prove ordered permutation, analyze recurrences, and distinguish abstract operations from bytes moved.

## Learning Objectives

After this module, you should be able to:

1. state ordered-permutation, stability, distribution, and reproducibility contracts precisely;
2. derive work and span for network, merge, partition, and sample-based designs;
3. prove comparator-network, recursive-range, bucket-interval, and exactly-once invariants;
4. distinguish average load from maximum bucket and quantify imbalance consequences;
5. design duplicate-safe splitters, offsets, redistribution, and final local ordering;
6. compare comparison, radix, shared-memory, GPU, and distributed approaches by the resources they consume;
7. diagnose comparator, synchronization, memory, count, communication, failure, and benchmark defects; and
8. validate output, stability, determinism, bounds, and performance under adversarial distributions.

## Core Exposition

### Begin with the semantic contract

Let input records be $R=(r_0,\ldots,r_{n-1})$ and key function $k$. A result $S$ is sorted when $k(S_i)\preceq k(S_{i+1})$ for every adjacent pair. It is a permutation when each input occurrence—not merely each distinct value—appears exactly once. For duplicate records, use identities or multisets to distinguish occurrences.

A stable result adds: whenever $i<j$ and $k(r_i)=k(r_j)$, $r_i$ precedes $r_j$ in output. Decorating each record with original position and ordering by $(k(r_i),i)$ converts stability into an ordinary total order, though it increases key and movement cost. An implementation can preserve stability more cheaply through stable local sorting, boundary rules, exchange order, and stable merging.

The comparator must satisfy the ordering contract used by the algorithm. Irreflexivity and transitivity are central for strict-weak-order interfaces; some domains need an explicit totalization. Floating NaNs, signed zeros, locale collation, version strings, and mixed encodings do not acquire policy merely because calls run concurrently. A comparator that reads mutable shared state can return inconsistent answers and invalidate every proof.

Output placement matters. A shared-memory sort may return one contiguous array. A distributed sort may promise that every local rank is sorted and every key on rank $i$ is no greater than every key on rank $i+1$. Replication, range balance, empty ranks, and preservation of the input partition are separate policies.

### Lower bounds and performance models

Any comparison sort must distinguish $n!$ permutations, giving worst-case decision-tree depth $\lceil\log_2(n!)\rceil=\Omega(n\log n)$ comparisons. Parallel comparisons reduce dependency depth only when many legal comparisons are independent. Total work still pays for comparisons, record movement, classification, prefix offsets, allocation, and merging.

The work/span lower bound from ALGE-081 is necessary, not predictive. Sorting time may be approximated by local work, synchronization, memory traffic, and communication terms, but each term needs measurement. For distributed sample sort, a useful decomposition is

$$
T\approx T_{local-sort}+T_{sample}+T_{partition}+T_{counts}+T_{exchange}+T_{final-sort/merge}.
$$

If rank $i$ receives $b_i$ records, the final stage is governed by $b_{\max}=\max_i b_i$. Average $n/P$ can conceal a catastrophic hot rank. Peak memory can include input, send buffer, receive buffer, samples, counts, and temporary merge state simultaneously.

### Sorting networks

A comparator maps $(a,b)$ to $(\min(a,b),\max(a,b))$ under a declared order. A sorting network fixes comparator pairs in advance; comparators in one layer are disjoint and parallel. Batcher's bitonic and odd-even merge networks established practical regular constructions with $O(\log^2 n)$ depth and $O(n\log^2 n)$ comparators [1]. Their data-independent control is useful when regular scheduling or limited data-dependent behavior matters.

The zero-one principle states that a comparator network sorts every totally ordered input if it sorts every binary input. The proof maps values below a failing threshold to zero and values at or above it to one; comparators commute with this monotone mapping. It provides exhaustive validation for small networks, not permission to ignore comparator or machine faults.

AKS established asymptotically $O(\log n)$-depth, $O(n\log n)$-size sorting networks, while large constants and construction complexity make asymptotic existence different from an automatic implementation choice. Cole's parallel merge-sort results likewise demonstrate logarithmic PRAM time under stated CREW and EREW models [2]. Model-qualified theorems do not include cache misses, finite bandwidth, allocation, or task overhead.

### Parallel merge sort

Recursively sort the left and right halves in parallel, then merge. If merge remains sequential, the root merge contributes $\Theta(n)$ span, so recursive parallelism alone cannot yield logarithmic span. A parallel merge partitions the output: choose a pivot from one input, binary-search its rank in the other, place it at its combined rank, and recursively merge the two disjoint output ranges.

Tie handling is part of the rank calculation. For a stable merge, a left-origin pivot must be placed relative to equal right records consistently with original range order. Using lower bound on one side and upper bound on the other without a coherent rule can duplicate output positions or reverse equals.

The merge proof establishes that each recursive call owns disjoint input slices and a disjoint output interval; the pivot's rank is final; child intervals exactly cover the remainder. Cut off to a tuned sequential merge when tasks become too small. The cutoff changes scheduling overhead, not the result contract.

### Parallel partition and quicksort

Parallel partition evaluates predicates independently, scans bucket counts to unique offsets, and scatters records. A two-way partition then recurses on disjoint ranges. With good pivots, the dependency tree is shallow; with repeated keys or adversarial pivots, one range can retain nearly all input. Three-way partition isolates keys less than, equal to, and greater than the pivot and is essential for duplicate-heavy data.

Randomized pivoting turns fixed adversarial order into a probabilistic balance statement conditional on the random model. Sampling several keys and choosing a median improves pivot quality at extra work. Introspective fallback limits bad recursion depth. Concurrent in-place partition is possible but much harder to verify than count-scan-scatter; cache traffic, temporary storage, and stability may dominate the choice.

### Sample sort step by step

Sample sort generalizes partitioning to $P$ or more buckets.

1. Assign each input occurrence to exactly one worker.
2. Sort each local run under the same total order.
3. Draw regular or randomized samples from every run.
4. Sort samples and choose ordered splitters $s_1\le\cdots\le s_{P-1}$.
5. Classify every record into one bucket under a defined boundary-equality rule.
6. Count destinations and prefix-scan counts into disjoint send offsets.
7. Redistribute buckets to their owner ranks.
8. Merge received sorted runs or sort the received bucket.
9. Validate local order, cross-rank boundaries, and global permutation.

Parallel sorting by regular sampling uses structured local samples to improve partition balance under its stated assumptions [3]. Oversampling makes splitter estimates more robust, especially with random sampling, but consumes sample sorting, broadcast, and classification resources. No sample can rescue an equality rule that sends all copies of one hot key to one rank. Duplicate-aware schemes split equal-key occurrences by secondary identity or assign equality quotas while preserving stability.

### Execute a stable sample-sort reference

This bounded reference simulates four workers sequentially. It decorates records by original position, locally sorts, regularly samples, chooses splitters, redistributes, and validates the exact stable permutation. Its uneven bucket sizes intentionally show that correctness does not prove balance.

<!-- bijux-verify: {"id":"stable-sample-sort-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sorted: [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 7, 8, 9, 9]\nlocal sizes: [4, 4, 4, 4]\nbucket sizes: [8, 3, 3, 2]\nsplitters: [(4, 2), (6, 8), (8, 6)]\nones retain positions: [1, 3]\n","stderr":""}} -->
```python
def stable_sample_sort(values, workers):
    decorated = [(value, position) for position, value in enumerate(values)]
    size = len(decorated)
    cuts = [(worker * size) // workers for worker in range(workers + 1)]
    runs = [
        sorted(decorated[cuts[worker]:cuts[worker + 1]])
        for worker in range(workers)
    ]

    samples = []
    for run in runs:
        for sample_number in range(1, workers):
            if run:
                index = min((sample_number * len(run)) // workers, len(run) - 1)
                samples.append(run[index])
    ordered_samples = sorted(samples)
    splitters = [
        ordered_samples[min((number * len(ordered_samples)) // workers,
                            len(ordered_samples) - 1)]
        for number in range(1, workers)
    ] if ordered_samples else []

    buckets = [[] for _ in range(workers)]
    for run in runs:
        for item in run:
            destination = 0
            while destination < len(splitters) and item > splitters[destination]:
                destination += 1
            buckets[destination].append(item)

    merged = [item for bucket in buckets for item in sorted(bucket)]
    assert merged == sorted(decorated)
    return merged, [len(run) for run in runs], [len(bucket) for bucket in buckets], splitters


values = [9, 1, 4, 1, 7, 3, 8, 2, 6, 5, 0, 4, 9, 2, 7, 3]
result, local_sizes, bucket_sizes, splitters = stable_sample_sort(values, 4)
print("sorted:", [value for value, _ in result])
print("local sizes:", local_sizes)
print("bucket sizes:", bucket_sizes)
print("splitters:", splitters)
print("ones retain positions:", [position for value, position in result if value == 1])
```

This is evidence for one deterministic sequential simulation on the recorded interpreter. It does not create threads, perform an MPI exchange, establish a general balance bound, or benchmark a machine. Exhaustive checks against a decorated sequential oracle are appropriate for short inputs; actual implementations additionally need race, collective, allocation, and topology evidence.

### Radix and distribution sorting

When keys have bounded digital representations, radix approaches avoid the comparison lower bound because they use more structure than binary comparisons. A parallel stable radix pass builds per-worker digit histograms, reduces or scans counts into global digit bases, scans per-worker counts into private offsets, and scatters each record stably. Multiple passes cover the key.

Digit width trades passes against histogram size, cache footprint, contention, and sparsity. Signed integers, variable-length strings, endianness, floating encodings, and descending order require explicit transforms. A correct bitwise order is not automatically the product's semantic order. GPU sorting research demonstrates how radix and merge designs depend on memory hierarchy and parallel primitives, not merely asymptotic comparison counts [5].

### Shared-memory engineering

Use coarse local sorts to exploit mature sequential kernels, then parallelize merging or redistribution. Task creation stops below a measured grain threshold. Allocate scratch space by ownership rather than from one contended allocator. Keep partitions NUMA-local when possible and avoid copying large records by sorting compact keys or indexes.

False sharing can arise in per-worker counts; pad or arrange metadata based on measured layout. Barriers, joins, futures, and task dependences must match the actual range graph. Never infer visibility solely from the fact that tasks “should have finished.” If the comparator is expensive, cache derived keys only when snapshot consistency and memory cost permit.

### Distributed-memory engineering

Distributed sample sort typically broadcasts splitters, computes a count matrix, and uses a variable-sized all-to-all exchange. MPI 4.1 specifies `MPI_Alltoallv` as pairwise matching variable-count blocks with explicit counts and displacements [8]. That is a communication contract, not a load-balance guarantee, an implicit sort, or a portable global barrier beyond the collective's specified completion semantics.

Counts may exceed narrow integer interfaces; use supported large-count operations or chunking under a proved plan. Validate every pair's send and receive agreement before allocating. Bound peak receive memory or exchange in rounds. Preserve record serialization, endian, and schema compatibility. After redistribution, a multiway merge can exploit already sorted sender runs; resorting is simpler but may repeat work.

Process failure invalidates ordinary collective membership assumptions. A fault-aware design establishes an epoch, reconstructs committed input ownership, and restarts or resumes with exactly-once semantics. Substituting an empty bucket for a failed rank yields a sorted sequence that is not a permutation of the intended input.

### Accelerator and heterogeneous concerns

Sorting networks offer regular control for small fixed tiles. Radix passes expose histogram, scan, and scatter kernels. Merge-path and partition techniques divide merge work. Yet device performance depends on coalescing, shared-memory capacity, bank conflicts, occupancy, launch cost, and host-device movement. Satish and colleagues' manycore GPU work analyzes algorithm choices against these machine resources [5].

In a heterogeneous pipeline, include transfers, format conversion, allocation, and synchronization in the measured interval. A device-only speedup can coexist with a slower end-to-end sort. Validate the same ordering and stability semantics on CPU and accelerator; different floating or collation policies are not harmless implementation detail.

### Validation and evidence

Correctness validation needs at least two independent predicates: adjacent order and exact permutation. For occurrence identity, compare decorated output against a trusted stable oracle, or use exact counting where the domain is bounded. Hashes are useful corruption detectors but collision-prone hashes alone are not a proof. Cross-rank validation checks each local run and the maximum/minimum boundary between consecutive nonempty ranks.

Exhaust small arrays across all permutations and duplicate multisets. Include already sorted, reverse, equal, organ-pipe, sawtooth, clustered, heavy-hitter, sparse-range, adversarial splitter, empty-worker, one-item, extreme-key, NaN-policy, and huge-record cases. For networks, exhaust binary inputs by the zero-one principle at bounded size. For concurrency, perturb schedules, vary workers and grain, use race tools, and validate every run.

Performance evidence records $n$, record/key bytes, distribution, entropy and duplicates, comparator, stability, algorithm, sample rate, bucket sizes, workers, affinity, topology, memory peak, bytes moved, collectives, compiler, runtime, warmup, repetitions, and validation result. Compare against a strong sequential implementation with the same semantics. Report throughput, latency distribution, speedup, efficiency, work inflation, and imbalance separately.

## Definitions and Notation

Input occurrence $r_i$ has key $k(r_i)$ and identity $i$. The order relation is $\preceq$. A stable totalized key may be $(k(r_i),i)$. $T_1$ is total work, $T_\infty$ span, $T_P$ time on $P$ workers, and parallelism $T_1/T_\infty$.

Worker $j$ initially owns $n_j$ items and receives bucket size $b_j$; $b_{\max}=\max_j b_j$. Splitters $s_1,\ldots,s_{P-1}$ define ordered bucket intervals under a declared equality rule. A sorting network has size $C$ comparators and depth $D$ parallel layers. For communication, $m_{ij}$ is the record count sent from rank $i$ to rank $j$.

The input snapshot is $R^e$ for membership epoch $e$. Correct distributed output is the ordered permutation of exactly $R^e$, not merely the contributions of ranks that happened to finish.

## Mechanisms, Invariants, or Proof Structure

### Ordered-permutation proof

Prove comparator assumptions. Prove every record is assigned to one local range, bucket, message, and final position. Prove bucket intervals are ordered and final local sorts are ordered; then concatenation is globally ordered. Prove equality boundaries and original-position order if stability is promised.

### Network and recursive proofs

For a network, show disjoint comparator locations per layer and use the zero-one principle plus exhaustive binary validation at bounded $n$. For parallel merge, prove pivot rank and disjoint child input/output intervals. For parallel partition, prove counts, scans, and scatter offsets cover each destination interval without collision.

### Balance and resource proof

State whether splitter balance is deterministic, probabilistic, empirical, or absent. Derive bounds only under the source theorem's sampling and distribution assumptions. Independently check count sums, displacement ranges, integer capacity, buffer peaks, message agreement, and $b_{\max}$.

### Implementation and failure proof

Map range dependencies to joins or barriers; prove scratch ownership and comparator thread safety. For distribution, prove rank ordering, serialization, communicator membership, and exactly-once input lineage. A recovery path must reproduce or explicitly abandon the epoch; sorted surviving data is not silent success.

## Alternatives and Trade-Offs

**Sorting networks** provide regular data-independent layers but often do more comparisons. **Parallel merge sort** offers predictable divide-and-conquer and stability with buffer movement. **Parallel quicksort** can be in-place and cache-friendly but needs skew and duplicate defenses. **Sample sort** scales through multiway partitioning but makes splitter quality and all-to-all exchange central.

**Comparison sorting** supports general comparators. **Radix sorting** exploits key representation and can reduce instruction count while increasing passes, histograms, and semantic conversion obligations. **Stable sorting** preserves equal-key lineage at a cost; **unstable sorting** may move equals freely only when callers permit it.

**Local resort after exchange** is simple; **multiway merge** reuses sorted runs. **Direct records** avoid indirection but move more bytes; **indirect indexes** reduce movement but add random access. **Fixed partitions and trees** improve reproducibility; **adaptive scheduling and splitters** may improve balance while changing order or timing.

## Failure Modes and Misconceptions

- **“Parallelizing recursive calls parallelizes merge.”** A sequential root merge still has linear span.
- **“Sorted output proves correctness.”** Records can be lost or duplicated while order remains valid.
- **“Every rank starts equal, so the sort is balanced.”** Splitters determine receive load.
- **“More samples always fix skew.”** A hot equal key needs an equality-distribution policy.
- **“Comparator equality is record equality.”** Distinct occurrences and payloads may share a key.
- **“A network is automatically fast.”** Comparator count, movement, vector width, and memory decide realized cost.
- **“Radix sort violates the lower bound.”** It uses key representation beyond the comparison model.
- **“A collective sorts data.”** It only moves blocks under its specified count and type semantics.
- **“Collectives are portable barriers.”** Depend only on specified completion and ordering guarantees.
- **“A failed rank is an empty bucket.”** That drops part of the input snapshot.
- **“GPU kernel time is end-to-end time.”** Transfers, conversion, allocation, and synchronization count.
- **“Speedup proves scalability.”** State baseline, semantics, workers, imbalance, work inflation, and machine limits.

## Worked Examples

### Example 1

**Situation.** Eight keys enter a three-layer candidate sorting network.

**Reasoning.** Independent comparators within each layer can run together, so layer count is span in the comparator model. But $3$ layers cannot realize enough comparisons for a general eight-input network; exhaust all $2^8$ binary inputs and find a counterexample. One failing binary input disproves universal sorting by the zero-one principle.

**Conclusion.** Network depth is useful only after functional validation.

### Example 2

**Situation.** Parallel merge sort sorts two halves concurrently but merges 16 million records with one thread.

**Reasoning.** The root merge alone has linear span and dominates after recursive sorts accelerate. Partition the merge by searched ranks into disjoint output intervals, or accept the bottleneck deliberately for a bounded size.

**Conclusion.** Parallel subproblems do not remove a sequential combine.

### Example 3

**Situation.** Stable merge combines left records `(5,L1),(5,L2)` and right `(5,R1)`.

**Reasoning.** Original left range precedes the right range, so stable output is `L1,L2,R1`. A tie rule that selects right first remains key-sorted but violates stability.

**Conclusion.** Tie policy belongs in both proof and tests.

### Example 4

**Situation.** Four equal initial chunks produce sample-sort receive sizes 8, 3, 3, and 2.

**Reasoning.** The average is 4, but the bottleneck ratio is $8/4=2$. Local input balance did not imply key-range balance; splitter and equality choices created the hot bucket.

**Conclusion.** Measure $b_{\max}$ and full distribution, not only average load.

### Example 5

**Situation.** Half the records have one identical key.

**Reasoning.** A boundary rule sending equality wholly left can place at least half the data on one rank regardless of oversampling. Secondary original identity or quota-based equal-key splitting distributes occurrences while a global stable order specifies their sequence.

**Conclusion.** Duplicate skew requires semantic partition design.

### Example 6

**Situation.** A radix pass has four workers and 256 digit buckets.

**Reasoning.** Each worker builds 256 counts. Reducing digit totals yields global bucket bases; scanning per-worker counts yields private nonoverlapping offsets. Stable traversal then scatters each record exactly once. Atomic increments into shared buckets are unnecessary.

**Conclusion.** Histogram plus scan converts classification into collision-free placement.

### Example 7

**Situation.** A floating-key comparator treats every comparison with NaN as false.

**Reasoning.** The resulting relation may not produce the intended total placement, and different algorithms can place NaNs differently. Define a total policy—such as all NaNs after numbers with a payload tie policy—and test it on CPU and accelerator.

**Conclusion.** Parallelism cannot repair an unspecified order domain.

### Example 8

**Situation.** Every distributed rank sends an agreed number of records, but 32-bit displacement addition wraps.

**Reasoning.** Pairwise counts can be correct while buffer addresses are not. Prove prefix totals fit the interface and allocation type, use large-count support or chunked rounds, and reject overflow before communication.

**Conclusion.** Count agreement and address capacity are separate invariants.

### Example 9

**Situation.** A GPU radix kernel is six times faster than CPU sorting, but transfers and allocation exceed saved time.

**Reasoning.** Kernel-only measurement excludes required pipeline stages. Compare equal semantic contracts across host-to-device conversion, sort, device-to-host output, synchronization, and validation.

**Conclusion.** Optimize and report the boundary the product actually pays.

### Example 10

**Situation.** Rank 3 fails after sending some buckets.

**Reasoning.** Survivors may concatenate a sorted result, but its occurrence set is uncertain and duplicates may exist after replay. Abort the epoch or recover from committed ownership and idempotent transfer metadata before publishing.

**Conclusion.** Global permutation requires explicit failure and replay semantics.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** tasks, barriers, futures, atomics, work stealing, and memory visibility realize sort dependency graphs.
- **Computer Architecture:** caches, vector units, NUMA, GPU memory, network topology, and bandwidth determine movement cost.
- **Distributed Systems:** membership epochs, exactly-once lineage, replay, and partial failure govern distributed ordered permutations.
- **Database Engineering:** external sorts, merge joins, index builds, collation, and stable row identity inherit ordering semantics.
- **Data Engineering:** range partitioning, shuffle skew, schema serialization, and deterministic output use sample-sort mechanisms.
- **Software Delivery and Reliability Engineering:** distribution suites, race detection, performance baselines, rollback, and telemetry govern deployment.

## References

1. Kenneth E. Batcher, “Sorting Networks and Their Applications,” *AFIPS Spring Joint Computer Conference* 32, 1968, 307–314. DOI: [10.1145/1468075.1468121](https://doi.org/10.1145/1468075.1468121). Primary source for bitonic and odd-even sorting networks; ACM-linked record checked 2026-09-05.
2. Richard Cole, “Parallel Merge Sort,” *SIAM Journal on Computing* 17(4), 1988, 770–785. DOI: [10.1137/0217049](https://doi.org/10.1137/0217049). Primary CREW/EREW PRAM merge-sort result; SIAM and author-hosted records checked 2026-09-05.
3. Hanmao Shi and Jonathan Schaeffer, “Parallel Sorting by Regular Sampling,” *Journal of Parallel and Distributed Computing* 14(4), 1992, 361–372. DOI: [10.1016/0743-7315(92)90075-X](https://doi.org/10.1016/0743-7315(92)90075-X). Primary regular-sampling algorithm and qualified balance result; publisher and DBLP records checked 2026-09-05.
4. Guy E. Blelloch, Charles E. Leiserson, Bruce M. Maggs, C. Greg Plaxton, Stephen J. Smith, and Marco Zagha, “A Comparison of Sorting Algorithms for the Connection Machine CM-2,” *Proceedings of SPAA*, 1991, 3–16. DOI: [10.1145/113379.113380](https://doi.org/10.1145/113379.113380). Primary comparative parallel-sorting study; ACM-linked record checked 2026-09-05.
5. Nadathur Satish, Mark Harris, and Michael Garland, “Designing Efficient Sorting Algorithms for Manycore GPUs,” *IEEE IPDPS*, 2009, 1–10. DOI: [10.1109/IPDPS.2009.5161005](https://doi.org/10.1109/IPDPS.2009.5161005). Primary GPU radix and merge sorting study; IEEE-linked record checked 2026-09-05.
6. Michael Axtmann, Timo Bingmann, Peter Sanders, and Christian Schulz, “Practical Massively Parallel Sorting,” *SPAA*, 2015, 13–23. DOI: [10.1145/2755573.2755595](https://doi.org/10.1145/2755573.2755595). Primary distributed-memory engineering and communication study; ACM-linked record checked 2026-09-05.
7. Michael Axtmann, Sascha Witt, Daniel Ferizovic, and Peter Sanders, “In-Place Parallel Super Scalar Samplesort,” *ESA*, 2017, Article 9. DOI: [10.4230/LIPIcs.ESA.2017.9](https://doi.org/10.4230/LIPIcs.ESA.2017.9). Primary shared-memory sample-sort design; Dagstuhl record checked 2026-09-05.
8. MPI Forum, *MPI: A Message-Passing Interface Standard*, Version 4.1, November 2, 2023, Section 6.7.6, “All-to-All Scatter/Gather.” Official current specification used for variable-count exchange semantics; PDF and HTML checked 2026-09-05.

## Exercises

### Exercise 1

Define ordered permutation, stability, work efficiency, sorting-network depth, splitter, oversampling, maximum bucket load, and membership epoch. Explain why checking adjacent order alone is insufficient.

### Exercise 2

Four workers receive 32 records and after sample partition receive bucket sizes `[5,7,16,4]`. Compute average, maximum-to-average imbalance, efficiency ceiling due only to this final-stage imbalance, and peak-record memory if each worker retains 8 input records while allocating its receive bucket. State the assumptions.

### Exercise 3

A stable distributed sample sort uses a mutable comparator, sends equal splitters wholly left, computes 32-bit displacements unchecked, invokes variable all-to-all with mismatched pair counts, resorts locally, validates only order, and publishes after one rank fails. Diagnose every defect and give a focused check or remedy.

### Exercise 4

Design a parallel stable sort for 400 million variable-size records with 64-bit keys on two NUMA CPU sockets and four GPUs. Specify semantic order, decomposition, local algorithm, partition or merge, offsets, movement, memory, synchronization, stability, failure, validation, observability, and performance evidence.

### Exercise 5

A privacy-sensitive service needs deterministic globally sorted audit events across changing cluster sizes, equal timestamps, replayed partitions, and adversarial tenants. Transfer the chapter's reasoning to define an order and algorithm, control skew and denial-of-service risk, and state what cannot be guaranteed during incomplete membership.

## Answers to the Exercises

### Answer 1

An ordered permutation contains every input occurrence exactly once and has nondecreasing adjacent keys. Stability preserves original relative order among equal keys. Work efficiency asymptotically matches the best sequential work. Sorting-network depth is the number of dependent comparator layers. A splitter defines a bucket boundary. Oversampling takes more candidate keys than final splitters to improve their estimates. Maximum bucket load is $b_{\max}$, the largest worker destination. A membership epoch fixes the exact distributed contributors. Adjacent order alone is insufficient because deleting every record, dropping a shard, or duplicating a key can still leave a sorted sequence; exact occurrence preservation must be checked independently.

### Answer 2

Total records are $32$, so average receive load is $32/4=8$. Maximum is $16$, giving imbalance $16/8=2$. If final processing is linear per record, all workers start together, and there are no other costs, the best efficiency relative to ideal equal division is at most $8/16=1/2$; this is a limited stage model, not total program efficiency. If each worker retains its 8-record input while allocating receive space, peak record slots are `[13,15,24,12]`, with global simultaneous total $64$ and per-worker maximum $24$. Metadata, serialization, scratch, samples, and allocator overhead are excluded and must be added in a real memory model.

### Answer 3

Mutable comparator state can violate consistent transitivity; freeze inputs and property-test the comparator concurrently. Sending equality left creates duplicate-key skew; distribute equal occurrences by stable secondary identity or quotas and test an all-equal input. Unchecked 32-bit prefix sums can wrap; use a proved capacity, large counts, or chunking and test boundary overflow. Mismatched pair counts violate exchange semantics; all ranks compare or derive one count matrix before communication. Local resort is not inherently wrong but repeats work; compare it fairly with merging sender runs. Order-only validation misses loss and duplication; verify occurrence permutation and rank boundaries. A failed rank invalidates the epoch; abort or reconstruct committed ownership and replay idempotently before publishing.

### Answer 4

Define a total key as `(uint64 key, original snapshot position)` so equality is stable; specify payload identity and byte encoding. Partition the snapshot into NUMA-local chunks, build compact key/index arrays, and use GPU radix sorting for sufficiently large resident chunks while CPU workers handle small or transfer-hostile chunks. Produce sorted runs, sample across every run with duplicate-aware secondary identities, select global splitters, count destinations, scan into offsets, and redistribute contiguous record references or packed payloads. Merge received runs stably rather than blindly resorting when merge metadata fits. Bound device, pinned-host, send, receive, and payload-arena memory; exchange in rounds if peak capacity would be exceeded. Synchronize kernel completion, transfers, count publication, and merge readiness through explicit events and task dependences. Abort the immutable snapshot on device or process failure unless durable ownership permits exact replay. Validate key order, occurrence IDs, stability, per-bucket boundaries, count sums, checksums, and a trusted sample or full oracle where feasible. Observe stage times, bytes, PCIe and NUMA traffic, bucket histogram, allocation peak, tasks, GPU occupancy, retries, and validation. Compare end-to-end with a strong CPU stable sort under identical semantics across distributions and record sizes.

### Answer 5

Define each event's total key as `(event timestamp under one declared time scale, tenant ID, durable partition ID, source sequence, event ID)`; never let arrival race decide equality. Use a fixed logical range-partition rule or a deterministic sample/splitter procedure derived from the input epoch, then stable local sorts and deterministic multiway merge. Deduplicate replays by durable event ID before or during the exact permutation protocol. Limit per-tenant records, key and comparator cost, sample influence, bucket bytes, and spill or exchange bandwidth; detect hot timestamps and split equals by the remaining total key rather than one timestamp bucket. Validate contributor manifests, occurrence IDs, boundaries, result digest, and reproducibility across worker counts. During incomplete membership, the service can publish an explicitly partial, watermarked view, block, or fail; it cannot honestly guarantee a complete global permutation of an epoch whose contributors or replay state are unknown.
