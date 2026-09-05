---
module_id: ALGE-085
program: Algorithm Engineering
level: 2
module_number: 85
title: External-Memory Cost Models
status: complete
last_verified: 2026-09-05
---

# External-Memory Cost Models

## One-Page Review

### Governing question

When data movement dominates computation, how should an engineer model, derive, and validate an algorithm's transfers without confusing an ideal I/O bound with operating-system, device, or end-to-end behavior?

### Essential definitions

- The two-level external-memory model has fast memory capacity $M$ items and transfers contiguous blocks of $B$ items; computation on resident items is free in the basic I/O count [1].
- `Scan(N) = Θ(N/B)` denotes the block transfers needed for a contiguous pass over $N$ items, up to boundary and cache-state terms.
- Comparison sorting requires `Sort(N) = Θ((N/B) log_{M/B}(N/B))` I/Os in the standard eligible regime [1].
- A **cache-aware** algorithm uses $M$ and $B$ explicitly. A **cache-oblivious** algorithm does not, but its analysis still assumes an ideal-cache model and often a tall-cache condition [3].
- **Spatial locality** reuses items in one transferred block; **temporal locality** reuses a resident block before eviction.
- The red-blue pebble game models communication needed to evaluate a computation DAG with limited fast storage [2].
- I/O complexity, bytes transferred, IOPS, latency, bandwidth, CPU work, write amplification, and elapsed time are different evidence dimensions.

### Central model, mechanism, or theorem

For $N$ contiguous items, at least $\lceil N/B\rceil$ aligned-block equivalents must enter fast memory when none are resident, and a sequential scan meets that bound up to alignment. A divide-and-conquer or blocked algorithm wins when it completes substantial reuse while a working set remains within $M$. For comparison sorting, multiway external merge sort creates runs of size about $M$, then merges about $M/B$ runs per pass, producing the standard sorting bound under model assumptions [1].

### Critical invariants

- Units for $N$, $M$, and $B$ match; block rounding and initial cache state are declared.
- Transfers are charged at the stated memory boundary, with replacement, associativity, prefetch, and write policy explicit.
- Every input item required by the computation is fetched and every durable output required by the contract is written.
- A claimed reuse occurs before eviction and within actual capacity after metadata, buffers, and concurrency.
- Lower-bound hypotheses match the algorithm class, data representation, and allowed recomputation.
- Measurements isolate logical requests, physical bytes, cache hits, writeback, synchronization, and end-to-end time.

### Common failures

Counting records instead of blocks; treating $M/B$ as $M$; ignoring alignment and partial blocks; assuming random access always means one physical I/O; assuming the operating-system cache is empty; using a cache-oblivious theorem without its ideal replacement or tall-cache hypothesis; double-counting nested cache layers; excluding output writes; overlooking concurrent buffer multiplication; equating fewer I/Os with faster runtime; benchmarking warm cache while claiming cold; and applying a disk-era latency story unchanged to SSD, remote, or persistent memory.

### Compact example

Sixteen items occupy four blocks of four. With room for two blocks, row-major scanning incurs four compulsory block misses. Column-major access to a row-major $4\times4$ matrix cycles through four blocks while only two fit, causing sixteen misses under LRU. Both execute sixteen logical item reads; their data-movement costs differ fourfold in the declared model.

### Connections

[ALGE-005](./005-asymptotic-time-and-space.md) supplies asymptotic notation, [ALGE-013](./013-merge-sort.md) supplies merge structure, [ALGE-020](./020-engineering-a-sort-for-real-data-distributions.md) supplies distribution-aware measurement, and [ALGE-081](./081-work-span-and-parallel-dependency.md) separates work from span. [ALGE-083](./083-parallel-sorting.md) supplies parallel partitioning. ALGE-086 next derives external sorting; ALGE-087 and ALGE-088 apply blocking and cache-oblivious design.

## Governing Question

Given a computation, representation, hierarchy boundary, transfer granularity, capacity, replacement behavior, concurrency, durability contract, and device, which data-movement model is justified, what bound follows, and which measurements could falsify the engineering prediction?

## Why This Matters

Arithmetic has become cheap relative to moving data across many boundaries: registers and caches, NUMA domains, accelerator memory, local storage, remote storage, and networks. An algorithm with fewer comparisons can lose because it scatters accesses; a blocked algorithm can win despite extra arithmetic because each fetched byte performs more useful work.

External-memory theory gives a vocabulary for this effect. It makes block transfers first-class and reveals why scanning, multiway merging, B-trees, blocked matrices, and batched queries work. It also provides lower bounds: some movement is inherent, not a compiler accident. The model's abstraction is its strength and its limit. It does not automatically capture queue depth, prefetch, cache associativity, SSD erase behavior, compression, remote retries, or durability barriers.

The engineering discipline is therefore two-stage. First derive a model-qualified I/O result. Then map its transfers to the actual hierarchy and measure the omitted mechanisms. Neither stage replaces the other.

## Prerequisites and Retrieval

Retrieve asymptotic quantifiers from [ALGE-005](./005-asymptotic-time-and-space.md), lower bounds from [ALGE-008](./008-lower-bounds-and-adversary-arguments.md), machine-model discipline from [ALGE-009](./009-machine-models-and-hidden-constants.md), proof-and-measurement design from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), merge sort from [ALGE-013](./013-merge-sort.md), work/span from [ALGE-081](./081-work-span-and-parallel-dependency.md), and parallel sorting from [ALGE-083](./083-parallel-sorting.md). You should manipulate logarithms, ceiling terms, and working-set sizes.

## Learning Objectives

After this module, you should be able to:

1. define the two-level I/O and ideal-cache models with units and assumptions;
2. derive scan, search, merge-pass, and comparison-sort transfer counts;
3. explain spatial/temporal locality, compulsory/capacity/conflict misses, and writeback;
4. distinguish cache-aware blocking from cache-oblivious recursion;
5. apply red-blue pebbling intuition and recognize lower-bound hypotheses;
6. map an abstract block transfer cautiously to caches, storage, accelerators, and networks;
7. diagnose alignment, buffer, cache-state, concurrency, durability, and measurement defects; and
8. validate I/O claims with traces, counters, controlled cache state, and end-to-end evidence.

## Core Exposition

### State the boundary and units

Choose one boundary. Fast memory holds $M$ items; slow memory is unbounded for the analysis; one I/O transfers a contiguous block of $B$ items. Usually $1\le B\le M\le N$, and $M/B$ is the number of resident blocks. The model counts transfers, not instructions executed on resident data.

“Item” must be concrete. If records vary in size, item-count formulas do not map directly to bytes. Use fixed-size keys, packed bytes, pages, or another declared unit. Metadata and buffers consume capacity. If $M$ is 1 GiB but four concurrent workers each allocate 300 MiB, the promised resident working set does not fit.

Declare initial and final state. A cold-cache read starts with none of the needed blocks resident. A warm-cache analysis may credit residency but must identify it. If output must be durable, dirty data must cross the durability boundary; merely reaching a page cache is not necessarily completion.

### Derive scanning

An aligned array of $N$ items occupies $\lceil N/B\rceil$ blocks. A cold sequential pass reads each block once, so

$$
Scan(N)=\Theta(N/B).
$$

If the first item begins at offset $a$ within a block, the exact occupied block count is $\lceil(a+N)/B\rceil$. A read-modify-write pass may also cause allocation reads and dirty writebacks, depending on overwrite and write policy. Big-Theta intentionally hides these terms; an engineering capacity plan cannot.

Sequentiality helps actual systems through prefetch and request coalescing, but those are outside the basic count. Conversely, a remote object store may require requests larger than a theoretical cache block to amortize latency. Preserve the locality principle while recalibrating the boundary.

### Random access and caching

One logical random lookup does not always equal one I/O. Its block may be resident; adjacent lookups may share a block; prefetch may fetch it; a cache conflict may evict it; a translation or index lookup may add more transfers. Expected I/O needs a request distribution and cache policy.

Compulsory misses fetch blocks never seen in the epoch. Capacity misses occur because the working set exceeds available blocks. Conflict misses occur in limited-associativity caches even when total capacity would suffice. The fully associative ideal-cache model omits conflicts. LRU is an implementable policy useful for trace experiments, not identical to every device or theorem's optimal replacement assumption.

### Execute a block-trace model

This reference simulates a fully associative LRU cache with block size four and capacity two blocks. It compares contiguous and column-major access over the same sixteen row-major items.

<!-- bijux-verify: {"id":"lru-block-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scan misses: 4 hits: 12\ncolumn misses: 16 hits: 0\nscan lower bound: 4\n","stderr":""}} -->
```python
def lru_block_misses(addresses, capacity_items, block_items):
    capacity_blocks = capacity_items // block_items
    resident = []
    misses = 0
    for address in addresses:
        block = address // block_items
        if block in resident:
            resident = [item for item in resident if item != block]
        else:
            misses += 1
            if len(resident) == capacity_blocks:
                resident.pop(0)
        resident.append(block)
    return misses, len(addresses) - misses


sequential = list(range(16))
column_major = [row * 4 + column for column in range(4) for row in range(4)]
scan_misses, scan_hits = lru_block_misses(sequential, 8, 4)
column_misses, column_hits = lru_block_misses(column_major, 8, 4)
print("scan misses:", scan_misses, "hits:", scan_hits)
print("column misses:", column_misses, "hits:", column_hits)
print("scan lower bound:", (len(sequential) + 4 - 1) // 4)
```

The simulation validates one trace and one replacement policy. It omits writeback, associativity, prefetch, multiple levels, translation, queueing, concurrency, and device latency. That limitation is part of the evidence.

### Searching and trees

Binary search makes $O(\log N)$ comparisons but may touch $O(\log N)$ blocks when levels occupy unrelated locations. A B-tree increases fanout to $\Theta(B)$ keys per node and yields $O(\log_B N)$ node transfers, with root caching reducing practical cost. Node split, fill factor, variable keys, concurrency, and write durability affect constants and updates.

The comparison illustrates model-aware design: minimize hierarchy transfers, not just comparison depth. A flat sorted array can outperform a tree for batched or in-memory reads due to contiguous access; the model does not dictate one data structure without workload assumptions.

### External merge sorting

Read up to $M$ items, sort them internally, and write a run. This creates about $\lceil N/M\rceil$ runs. Reserve one block buffer per input run and one output buffer, permitting fan-in about $M/B-1$. Each merge pass reads and writes $\Theta(N/B)$ blocks. The number of passes is logarithmic in $M/B$, leading to

$$
Sort(N)=\Theta\left(\frac NB\log_{M/B}\frac NB\right)
$$

in the standard comparison external-memory regime [1]. Precise formulas handle the initial run size, ceilings, output write, already sorted runs, and memory reserved for heaps or loser trees. ALGE-086 develops these mechanisms fully.

The logarithm base is a capacity ratio, not an arbitrary constant when engineering passes. Doubling RAM or increasing effective fan-in can remove an entire full-data read/write pass. But too many runs can turn sequential streams into random or poorly queued requests.

### Distribution, permutation, and lower bounds

Aggarwal and Vitter give tight I/O bounds for sorting and related permutation problems in their parallel-disk model [1]. Apply them only when comparison/permutation assumptions, block transfers, memory size, and eligible parameter regime match. Compression, restricted keys, approximate output, preexisting order, or allowed recomputation can define a different problem.

Hong and Kung's red-blue pebble game places values in slow or fast storage and charges movement needed to fire computation-DAG vertices [2]. It makes reuse constraints explicit and supports communication lower bounds. A lower bound for one DAG or no-recomputation rule may not transfer to algorithms allowed to restructure or recompute.

Lower bounds are diagnostic. If measured movement appears below one, check units, hidden cache residency, compression, omitted writes, a different output, or an inapplicable theorem before declaring a breakthrough.

### Cache-aware blocking

A cache-aware algorithm chooses tiles from known $M$ and $B$. For matrix multiplication, blocks aim to keep input and output tiles resident across many arithmetic operations. For graph and database work, batches group requests by block or key range. For merging, buffer counts and sizes are explicit.

Choose usable $M$, not nominal capacity. Code, stack, metadata, concurrent tasks, allocator fragmentation, cache sharing, and other processes reduce it. A tile exactly equal to advertised cache capacity is brittle. Multi-level hierarchies may need nested blocking.

Cache awareness enables tuning but couples performance to parameters. Record where parameters came from and benchmark neighboring values. Treat automatic tuning output as empirical evidence for a platform/input class, not a theorem.

### Cache-oblivious recursion

Cache-oblivious algorithms recursively divide until subproblems implicitly fit, without taking $M$ or $B$ as parameters. Frigo, Leiserson, Prokop, and Ramachandran analyze such algorithms in an ideal-cache model and show how two-level optimality can extend through a hierarchy under stated assumptions [3].

“Oblivious” does not mean caches are irrelevant or performance is automatic. The analysis assumes a block cache, often optimal replacement, and for some results a tall-cache condition such as $M=\Omega(B^2)$. Base-case overhead, recursion layout, associativity, translation, prefetch, and parallel scheduling can defeat constants.

Recursive layouts can improve locality across unknown levels, while explicit blocking can exploit known vector widths, devices, or direct-I/O constraints. Hybrid designs are normal: recursive decomposition plus tuned leaves.

### Parallel disks, workers, and hierarchy composition

The parallel-disk model can transfer blocks from multiple disks per I/O step [1]. Modern analogues include channels, devices, shards, or ranks, but independence and bandwidth must be demonstrated. Requests may share controllers or network links. Replace “$D$ disks gives $D$ speedup” with a topology and concurrency model.

Parallel workers multiply buffers and can destroy the capacity premise. They also reorder requests, create contention, and change cache sharing. A good sequential I/O bound plus low computational span does not imply scalable combined execution. Track maximum per-worker transfers, shared bandwidth, queue depth, and synchronization.

When composing levels, avoid charging one physical byte independently at every theoretical boundary as though times add without overlap. Report each boundary's counters, then measure end-to-end critical time. Transfers can overlap computation or one another, but overlap has resource and dependency limits.

### Writes, persistence, and amplification

Read and write costs may be asymmetric. Dirty cache blocks can coalesce multiple updates; random small writes may trigger device- or storage-engine amplification; copy-on-write and logging add bytes; durability barriers impose ordering. The basic symmetric block count does not model these effects.

Define completion: CPU store, cache coherence, kernel acceptance, device persistence, remote quorum, or application checkpoint. Measure logical bytes, issued bytes, device bytes where observable, and durable latency. An algorithm that writes fewer logical blocks can still amplify more internally.

Batching and buffering trade latency and loss window for fewer transfers. Correctness must cover crashes between data and metadata writes. External-memory complexity is not a crash-consistency proof.

### Measurement and model calibration

Construct synthetic traces whose theoretical counts are exact: aligned scans, strided arrays, repeated working sets just below and above capacity, blocked and unblocked matrix access. Validate the tracing tool before applying it to a complex algorithm.

Control cache state deliberately. Cold tests can use files larger than cache, direct-I/O-like mechanisms where appropriate, or documented eviction—not an unverified belief that a prior command cleared everything. Warm tests should report priming. Avoid destructive system-wide cache operations.

Record logical records, bytes, block size, alignment, usable memory, page/cache policy, prefetch, read/write mix, queue depth, workers, storage and filesystem, compression, durability, cache state, repetitions, counters, CPU time, and wall time. Reconcile model-predicted transfers with observed misses/bytes and explain gaps.

## Definitions and Notation

$N$ is problem size in declared items, $M$ fast-memory capacity in those items, $B$ contiguous items per transfer, and $m=M/B$ resident blocks. $D$ denotes independent transfer channels only when the model supplies them. $Scan(N)=\Theta(N/B)$ and $Sort(N)=\Theta((N/B)\log_{M/B}(N/B))$ name standard asymptotic bounds under their regimes.

An access trace is $a_0,\ldots,a_{q-1}$; block identity is $\lfloor a_i/B\rfloor$ for aligned fixed-size items. A cache state is an ordered or unordered resident-block set under a declared replacement policy. Working set is the distinct data needed during an interval, including metadata and buffers.

## Mechanisms, Invariants, or Proof Structure

### Scan and layout proof

Count distinct occupied blocks, including initial offset. Prove each is fetched at least once from cold state and that sequential order fetches it at most once before last use. Add output and writeback terms required by the contract.

### Blocking proof

Identify a subproblem's complete resident state and prove it fits usable $M$. Show every loaded block performs the claimed reuse before eviction. Sum blocks across tiles, including boundaries and overlap, then account for concurrency.

### Sorting and lower-bound proof

Count initial runs, legal merge fan-in, full-data transfers per pass, and pass count. State comparison/permutation model, $M$, $B$, initial/final state, and parameter regime before invoking the sorting lower bound.

### Empirical correspondence

Map theoretical items and blocks to actual bytes/pages/requests. Validate instrumentation on exact traces. Compare cold and warm results, isolate reads/writes, and retain end-to-end timing. A mismatch is a finding about assumptions or implementation, not automatically noise.

## Alternatives and Trade-Offs

**RAM analysis** counts operations and may miss movement. **External-memory analysis** exposes one transfer boundary but abstracts device details. **Red-blue pebbling** reasons from computation DAGs and reuse. **Roofline-style models** connect operations and bytes but answer a different performance question.

**Cache-aware blocking** exploits known parameters and direct-I/O constraints. **Cache-oblivious recursion** targets multiple unknown levels but relies on ideal-cache hypotheses. **Sequential scans** maximize locality; **batched sorting** pays reordering to convert future random access into sequential groups.

**Buffered writes** reduce transfers but delay visibility/durability. **Direct access** lowers software buffering ambiguity but imposes alignment and operational constraints. **More parallel I/O** can raise throughput or merely contend on a shared bottleneck.

## Failure Modes and Misconceptions

- **“One item access is one I/O.”** Blocks, residency, and prefetch intervene.
- **“$O(N)$ time means optimal movement.”** Access order can cause radically different misses.
- **“A scan costs exactly $N/B$.”** Alignment, ceilings, initial state, and writes affect exact counts.
- **“Cache-oblivious means assumption-free.”** Ideal replacement and tall-cache hypotheses still exist.
- **“Nominal cache size is usable $M$.”** metadata, sharing, and concurrency consume it.
- **“Random means slow and sequential means fast.”** Device, cache, batch, and queue behavior must be measured.
- **“Fewer transfers guarantees lower time.”** transfer sizes, latency, overlap, CPU work, and contention differ.
- **“Warm cache is realistic by default.”** workload and service lifetime determine state.
- **“An I/O lower bound covers compression.”** the representation and permitted operations may have changed.
- **“Parallel channels multiply bandwidth.”** topology may share controllers or links.
- **“Written means durable.”** persistence boundary and ordering must be explicit.
- **“A trace proves production performance.”** it supports one model mapping and environment.

## Worked Examples

### Example 1

**Situation.** An aligned 1,000-item array uses blocks of 64 items.

**Reasoning.** A cold scan touches $\lceil1000/64\rceil=16$ blocks. Starting 40 items into a block touches $\lceil(40+1000)/64\rceil=17$ blocks.

**Conclusion.** Alignment disappears asymptotically but matters in exact evidence.

### Example 2

**Situation.** Two loops read the same 16 row-major matrix cells with $M=8$, $B=4$.

**Reasoning.** Row order consumes four blocks once. Column order cycles among four row blocks while two fit and incurs sixteen LRU misses.

**Conclusion.** Equal operation counts can hide fourfold modeled movement.

### Example 3

**Situation.** Binary search reads 30 nodes from unrelated blocks.

**Reasoning.** It uses only 30 comparisons but up to 30 cold transfers. A high-fanout search node uses the block to choose among many children and reduces transfer depth.

**Conclusion.** Comparison depth and I/O depth optimize different resources.

### Example 4

**Situation.** Fast memory holds 1,024 blocks and an external merge reserves one output block.

**Reasoning.** At most 1,023 one-block input buffers fit before heap and metadata allowances. Engineering fan-in must be lower if those structures share $M$.

**Conclusion.** Merge fan-in uses blocks of capacity, not raw item capacity.

### Example 5

**Situation.** Four workers each choose a 300 MiB tile on a machine with 1 GiB usable memory.

**Reasoning.** Concurrent demand is 1.2 GiB before metadata, so the per-task locality proof fails. Limit concurrency or shrink tiles.

**Conclusion.** Parallelism is part of the working-set invariant.

### Example 6

**Situation.** A cache-oblivious transpose is analyzed under $M=\Omega(B^2)$, but measured cache has $M<B^2$ in chosen units.

**Reasoning.** The theorem's tall-cache hypothesis does not apply. The implementation may still work, but optimality needs other evidence.

**Conclusion.** Verify theorem hypotheses before quoting the bound.

### Example 7

**Situation.** A benchmark reports zero storage reads after a previous run.

**Reasoning.** The operating-system page cache retained the file. This is valid warm-cache evidence, not cold-device evidence; label and test both relevant states.

**Conclusion.** Cache state is an experimental variable.

### Example 8

**Situation.** Compression halves physical bytes but adds decompression work.

**Reasoning.** The fixed-item block model changed. Report logical and physical bytes, compression ratio, CPU work, memory, and wall time rather than forcing both runs into one $B$.

**Conclusion.** Representation changes require a revised cost mapping.

### Example 9

**Situation.** An update reaches the kernel page cache and the process reports durable success.

**Reasoning.** Power loss may still lose dirty pages. The completion boundary must include required flush and device or replicated acknowledgment semantics.

**Conclusion.** I/O count alone is not persistence evidence.

### Example 10

**Situation.** Eight storage shards deliver only three times one-shard throughput.

**Reasoning.** Shared network, coordinator, uneven partitions, or queue limits can dominate. The parallel-disk independence assumption is empirically false for this mapping.

**Conclusion.** Calibrate model channels against topology and measurements.

## Cross-Program Connections

- **Computer Architecture:** cache lines, associativity, prefetch, TLBs, NUMA, memory controllers, and persistent memory refine the boundary.
- **Operating Systems:** page cache, filesystems, direct I/O, writeback, scheduling, and durability determine observed transfers.
- **Database Engineering:** B-trees, buffer pools, external joins, sorting, logging, and page layouts operationalize I/O models.
- **Data Engineering:** partitioning, shuffles, columnar layout, compression, spills, and remote object reads trade computation for movement.
- **Platform Engineering:** storage classes, quotas, telemetry, caching, and topology turn parameters into governed resources.
- **Software Delivery and Reliability Engineering:** cold/warm benchmarks, crash tests, counters, regression budgets, and rollback validate changes.

## References

1. Alok Aggarwal and Jeffrey Scott Vitter, “The Input/Output Complexity of Sorting and Related Problems,” *Communications of the ACM* 31(9), 1988, 1116–1127. DOI: [10.1145/48529.48535](https://doi.org/10.1145/48529.48535). Primary source for the external-memory/parallel-disk model and tight sorting-related bounds; ACM-linked and author records checked 2026-09-05.
2. Jia-Wei Hong and H. T. Kung, “I/O Complexity: The Red-Blue Pebble Game,” *STOC*, 1981, 326–333. DOI: [10.1145/800076.802486](https://doi.org/10.1145/800076.802486). Primary computation-DAG communication model and lower bounds; ACM and DBLP records checked 2026-09-05.
3. Matteo Frigo, Charles E. Leiserson, Harald Prokop, and Sridhar Ramachandran, “Cache-Oblivious Algorithms,” *ACM Transactions on Algorithms* 8(1), 2012, Article 4. DOI: [10.1145/2071379.2071383](https://doi.org/10.1145/2071379.2071383). Journal version of the ideal-cache and cache-oblivious results; ACM-linked and author-hosted records checked 2026-09-05.
4. Jeffrey Scott Vitter, *Algorithms and Data Structures for External Memory*, Foundations and Trends in Theoretical Computer Science 2(4), 2008, 305–474. DOI: [10.1561/0400000014](https://doi.org/10.1561/0400000014). Authoritative monograph for external-memory paradigms, algorithms, and data structures.
5. Lars Arge, “The Buffer Tree: A Technique for Designing Batched External Data Structures,” *Algorithmica* 37, 2003, 1–24. DOI: [10.1007/s00453-003-1021-x](https://doi.org/10.1007/s00453-003-1021-x). Primary buffered external-data-structure technique; Springer-linked record checked 2026-09-05.
6. Erik D. Demaine, “Cache-Oblivious Algorithms and Data Structures,” in *Lecture Notes from the EEF Summer School on Massive Data Sets*, 2002. Author-hosted survey checked 2026-09-05; used for model exposition and hierarchy interpretation.
7. Michael A. Bender, Erik D. Demaine, and Martin Farach-Colton, “Cache-Oblivious B-Trees,” *SIAM Journal on Computing* 35(2), 2005, 341–358. DOI: [10.1137/S0097539701389956](https://doi.org/10.1137/S0097539701389956). Primary cache-oblivious search-structure result; SIAM-linked record checked 2026-09-05.
8. Peter Sanders, Kurt Mehlhorn, Martin Dietzfelbinger, and Roman Dementiev, *Sequential and Parallel Algorithms and Data Structures: The Basic Toolbox*, Springer, 2019. DOI: [10.1007/978-3-030-25209-0](https://doi.org/10.1007/978-3-030-25209-0). Authoritative algorithm-engineering treatment of memory hierarchies, sorting, and measurement.

## Exercises

### Exercise 1

Define $N$, $M$, $B$, block transfer, `Scan(N)`, spatial and temporal locality, cache-aware, cache-oblivious, tall-cache, and durability boundary. Distinguish I/O complexity from elapsed time.

### Exercise 2

An array of 10,000 fixed-size items starts 17 items into a block; $B=128$ and usable $M=16,384$ items. Compute occupied blocks, resident block capacity, cold read-only scan transfers, and read-plus-durable-rewrite transfers under an explicit simple policy.

### Exercise 3

An external algorithm treats nominal RAM as $M$, launches eight full-size buffers, assumes every random lookup is one I/O, quotes a cache-oblivious bound without tall-cache checks, benchmarks only warm cache, omits output writes, and treats page-cache completion as durability. Diagnose each defect and prescribe evidence.

### Exercise 4

Design an I/O study comparing row-major, blocked, and recursive cache-oblivious matrix traversal across cache and local-storage boundaries. Specify units, hypotheses, traces, cache state, parameters, correctness, counters, timing, confounders, and falsification criteria.

### Exercise 5

A cloud pipeline reads compressed columnar objects, joins by key, spills intermediate data, and writes a replicated durable result. Transfer the model to derive a useful multi-boundary cost account and explain which classic assumptions must be replaced by measurements.

## Answers to the Exercises

### Answer 1

$N$ is problem size in declared items, $M$ fast-memory capacity, and $B$ contiguous items per transfer. A block transfer moves one such unit across the chosen boundary. `Scan(N)=Θ(N/B)` is the contiguous-pass bound with stated rounding/state. Spatial locality uses nearby items in one block; temporal locality reuses a resident block. Cache-aware algorithms take hierarchy parameters explicitly; cache-oblivious algorithms do not but are analyzed under a cache model. A tall-cache hypothesis relates capacity and block size, commonly $M=\Omega(B^2)$ for particular results. A durability boundary is the state transition after which required failures cannot erase acknowledged output. I/O complexity counts abstract transfers; elapsed time also includes latency, bandwidth, overlap, computation, contention, software, and device behavior.

### Answer 2

Occupied blocks are $\lceil(17+10000)/128\rceil=\lceil10017/128\rceil=79$. Fast memory holds $16384/128=128$ blocks. From a cold state, a sequential read-only scan needs 79 block reads. Under the simple policy “read each partial or full block, dirty every occupied block, then write every dirty block durably once,” cost is 79 reads plus 79 writes, or 158 transfers. A full-block overwrite interface could avoid some reads; logging, replication, and flushes could add costs. Those alternatives require a different declared policy.

### Answer 3

Nominal RAM ignores metadata and competing use; measure usable capacity. Eight buffers multiply working set; include concurrency or limit it. Random logical lookups can hit, share blocks, prefetch, or add index transfers; trace block identities. Cache-oblivious results retain model and tall-cache hypotheses; verify them and replacement assumptions. Warm-only timing cannot support cold claims; run and label controlled warm and cold states. Omitting output writes changes the contract; count dirty writeback and required metadata. Page-cache acceptance is not durable completion; include specified flush/device/replica acknowledgments and crash tests. Reconcile predicted blocks with observed bytes, cache misses, requests, CPU, and end-to-end time.

### Answer 4

Use fixed-size matrix elements and define cache-line and storage-page boundaries separately. Hypotheses: row-major traversal is scan-optimal for rows but poor for columns; tiles fitting usable cache reduce reloads; recursive subdivision approaches good locality across multiple sizes. Generate exact address traces for small matrices and compare with an independently implemented LRU/ideal simulator. Sweep dimensions, leading-dimension padding, alignment, tile sizes around capacity, recursion cutoffs, and cold/warm state. Keep arithmetic and output identical; checksum all results. Record hardware counters for cache/TLB misses, logical and physical storage bytes where available, CPU instructions, bandwidth, and end-to-end time. Control prefetch, compiler, affinity, page cache, filesystem, storage, repetitions, and concurrent load. Falsify a model mapping when observed transfer scaling or capacity knees systematically contradict predictions; investigate associativity, prefetch, translation, buffering, or measurement errors rather than deleting the result.

### Answer 5

At object storage, count requests, compressed bytes, ranges, latency, retries, and cache hits; classic fixed $B$ becomes chosen range/object granularity. At decompression, count CPU, expanded bytes, and resident column working set. For the join, model partition/hash/sort movement, skewed maximum partition, network shuffle bytes/messages, and memory; spills add local reads and writes by pass. At output, count encoded bytes, multipart requests, replication traffic, metadata commits, and durability acknowledgments. Preserve logical row counts and exact join semantics across every representation. Replace free computation, symmetric reads/writes, one ideal cache, independent disks, fixed-size items, and simple completion with measured codec cost, layered caches, topology, queueing, variable records, failures, and durability. Still use scan, sorting, and working-set lower bounds as hypotheses, but report each boundary plus end-to-end critical time without double-counting overlapped transfers.
