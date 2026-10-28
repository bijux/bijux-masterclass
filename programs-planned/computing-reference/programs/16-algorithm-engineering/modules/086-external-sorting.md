---
module_id: ALGE-086
program: Algorithm Engineering
level: 2
module_number: 86
title: External Sorting
status: complete
last_verified: 2026-09-05
---

# External Sorting

## One-Page Review

### Governing question

How do we produce a verified total order when the input, intermediate runs, and output exceed fast memory, while minimizing full-data passes, bounding temporary storage, and preserving stability, durability, and recovery semantics?

### Essential definitions

- A **run** is a sequence already sorted under the final comparator.
- **Run generation** reads a memory-sized chunk, sorts it internally, and writes a run; replacement selection can create longer runs under qualified input assumptions.
- A **$k$-way merge** keeps one input buffer per run and one output buffer, repeatedly emitting the least current record.
- With fast memory $M$ items and blocks of $B$ items, feasible fan-in is at most roughly $M/B-1$ before heap, metadata, and safety reserves.
- A **merge pass** reads every participating run and writes their merged successors. Fewer passes often matter more than fewer comparisons.
- **Stable external sorting** preserves original occurrence order among equal keys across run formation and every merge.
- A recoverable sort records immutable inputs, completed runs, checksums, comparator identity, and publication state.

### Central model, mechanism, or theorem

Chunk sorting creates $R_0=\lceil N/M_r\rceil$ initial runs when $M_r$ items are usable for records. With effective fan-in $k\ge2$, merge-pass count is

$$
p=\lceil\log_k R_0\rceil.
$$

If every stage reads and writes all $N$ items once, a simple logical transfer account is $2N(1+p)$ items: one run-generation stage and $p$ merge stages. In block I/Os this yields the standard external comparison-sort form $\Theta((N/B)\log_{M/B}(N/B))$ under the model and regime of Aggarwal and Vitter [1]. Ceilings, partial runs, already resident data, compression, and final placement refine the engineering count.

### Critical invariants

- Every input occurrence belongs to exactly one initial run and appears exactly once after every pass.
- Each run is sorted under one immutable comparator and encoding contract.
- Merge input positions advance once; output is the stable minimum among current heads.
- Buffer, heap, decoder, allocator, and concurrent-worker memory remain within usable $M$.
- Temporary-space planning includes old and new runs until safe deletion or atomic publication.
- Checkpoints name complete immutable runs; partial outputs are never mistaken for committed runs.
- The published output is ordered, a permutation of the input snapshot, and durable to the promised boundary.

### Common failures

Using nominal rather than usable memory; allocating one block per run without reserving output and heap state; choosing excessive fan-in; losing stability at equal-key merge boundaries; overflowing counts or offsets; opening too many files; allowing locale or comparator changes between passes; deleting source runs before successor durability; resuming from truncated output; checking order without permutation; ignoring variable record size and compression expansion; and benchmarking warm cache while claiming storage performance.

### Compact example

Seventeen items with four-item run memory create five runs. Fan-in three merges them as $5\to2\to1$, so there are two merge passes and three read/write stages including run generation. The simple logical traffic is $2\cdot17\cdot3=102$ item transfers. Raising fan-in to five removes one full merge pass only if five input buffers, output, heap, and metadata genuinely fit.

### Connections

[ALGE-013](./013-merge-sort.md) supplies merge invariants, [ALGE-018](./018-stable-sorting-and-indirect-sorting.md) supplies stability, [ALGE-020](./020-engineering-a-sort-for-real-data-distributions.md) supplies comparator and benchmark design, [ALGE-083](./083-parallel-sorting.md) supplies partitioning, and [ALGE-085](./085-external-memory-cost-models.md) supplies the I/O model. ALGE-087 next generalizes blocking; ALGE-089 covers external indexes.

## Governing Question

Given an input snapshot larger than memory, record representation, comparator, stability and durability requirements, storage topology, usable memory, temporary-space budget, and failure model, which run-generation and merge plan produces an ordered permutation with reproducible evidence and acceptable data movement?

## Why This Matters

External sorting underlies database operators, index construction, log compaction, analytics shuffles, deduplication, search indexing, canonical archives, and large scientific pipelines. When data exceeds memory, the design objective changes: comparisons matter, but passes over bytes, request patterns, spill amplification, and temporary capacity can dominate.

The textbook mechanism—sort chunks, then merge—is only the beginning. Real records vary in size. Keys may be smaller than payloads. Compression changes physical bytes and CPU work. Multiple workers multiply buffers. Equal keys require a stability policy. Storage errors and process crashes can leave partial runs. The final rename may be atomic on one filesystem but not across services. A production sort must connect an ordering proof to a storage protocol.

External sorting also shows why “more fan-in” is not automatically better. Large $k$ reduces passes but consumes buffers, grows selection structures, scatters reads, raises file-descriptor pressure, and may reduce sequential request sizes. The optimum belongs to a specific hierarchy and workload, not to asymptotic notation alone.

## Prerequisites and Retrieval

Retrieve merge correctness from [ALGE-013](./013-merge-sort.md), comparator and stability contracts from [ALGE-018](./018-stable-sorting-and-indirect-sorting.md), adaptive sorting from [ALGE-019](./019-adaptive-and-hybrid-sorting.md), measurement from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), parallel partitioning from [ALGE-083](./083-parallel-sorting.md), and $N,M,B$, scan, and sorting I/O bounds from [ALGE-085](./085-external-memory-cost-models.md). You should be able to prove a two-way merge and calculate ceilings and logarithms.

## Learning Objectives

After this module, you should be able to:

1. specify the input snapshot, total order, stability, representation, and publication contract;
2. derive initial-run counts, legal fan-in, merge passes, logical traffic, and peak temporary space;
3. implement and prove stable multiway merging;
4. compare chunk sorting, replacement selection, natural runs, merge sorting, and distribution sorting;
5. design buffer allocation, asynchronous reads, parallel run generation, and merge scheduling without exceeding memory;
6. diagnose comparator drift, skew, variable records, corruption, descriptor, durability, and recovery defects;
7. validate sortedness, exact occurrence preservation, stability, checksums, pass lineage, and restart behavior; and
8. measure logical and physical bytes, requests, CPU, overlap, amplification, and end-to-end time.

## Core Exposition

### Freeze semantics before spilling

Let the immutable input snapshot contain occurrences $r_0,\ldots,r_{N-1}$. Define a key function and total comparison policy, including nulls, NaNs, collation, encodings, descending components, and tie breakers. A stable sort orders equal keys by original position. If the source is partitioned, original position needs a durable global form such as `(partition, sequence)`.

Comparator identity belongs in run metadata. Locale changes, library upgrades, or inconsistent normalization between run generation and merge can make individually sorted runs incompatible. Store a comparator/schema version and reject mixed runs rather than producing a plausible but invalid order.

Decide whether output contains full records, key-pointer pairs, or reordered references. Indirect sorting reduces temporary payload movement but adds later random access and requires referenced data to remain immutable. Variable-size records require byte budgets; “one million records fit” is not a capacity invariant.

### Generate initial runs

The basic method fills usable memory with records, sorts them using a strong internal algorithm, and writes one immutable run. If usable record memory is $M_r$, it creates $R_0=\lceil N/M_r\rceil$ runs for fixed-size items. Run writes should be sequential and include record count, byte length, key bounds, comparator version, and checksum.

Usable $M_r$ excludes input/output buffers, sort scratch, parsed keys, decompression state, runtime overhead, concurrent workers, and a reserve. Measure peak resident bytes. An internal stable sort does not by itself guarantee global stability: the merge must also choose earlier-run occurrences first on equality, and run order must correspond to original occurrence order.

Natural-run generation exploits already ordered stretches. It can sharply reduce $R_0$ on favorable inputs but needs a minimum-run policy and worst-case fallback. Reverse runs may be reversible only when equal-key stability is preserved.

### Replacement selection

Replacement selection maintains a heap of active records. Emit the minimum. A newly read record stays active in the current run if it is no smaller than the last emitted key; otherwise freeze it for the next run. Under independent random-order assumptions, expected runs can approach twice memory length, but adversarial descending input yields runs near $M_r$ [2].

The method trades longer runs against heap comparisons, random memory access, and more complex state. It must carry stable occurrence IDs and distinguish active from frozen records. Do not quote the expected run length without the input model. Modern fast internal sorts and large sequential writes can make chunk sorting preferable despite shorter runs.

### Multiway merge

Open up to $k$ sorted runs. Maintain a buffer for each, an output buffer, and a selection structure over nonempty heads. Repeatedly choose the least head, append it, advance exactly that input, and refill its buffer when empty. A binary heap costs $O(\log k)$ comparisons per record; loser trees and specialized selection structures improve constants and update locality [4].

For stability, compare `(key, original occurrence order)`, or on equal keys prefer the earlier logical run and preserve position within each run. Filename lexicography is not a safe proxy unless it encodes the original order by contract.

The merge invariant is: the output prefix is the stable sorted sequence of all consumed occurrences, and every unconsumed occurrence is at least the last emitted item. Each current head is the minimum remaining item of its run; therefore the minimum head is the global minimum remaining item. Induction proves ordered permutation.

### Execute a pass-planning reference

This reference creates four-item sorted runs, performs stable three-way merges, and records the run-count geometry. The linear head selection is deliberately simple; production selection structures change comparison cost, not merge semantics.

<!-- bijux-verify: {"id":"external-merge-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"run counts: [5, 2, 1]\nsorted: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 21, 23]\nstages: 3\nlogical item transfers: 102\n","stderr":""}} -->
```python
def merge_sorted_runs(runs):
    positions = [0] * len(runs)
    output = []
    while True:
        winner = None
        for run_number, run in enumerate(runs):
            position = positions[run_number]
            if position < len(run):
                candidate = (run[position], run_number)
                if winner is None or candidate < winner:
                    winner = candidate
        if winner is None:
            return output
        value, run_number = winner
        output.append(value)
        positions[run_number] += 1


def external_merge_reference(values, memory_items, fan_in):
    runs = [sorted(values[start:start + memory_items])
            for start in range(0, len(values), memory_items)]
    run_counts = [len(runs)]
    while len(runs) > 1:
        runs = [merge_sorted_runs(runs[start:start + fan_in])
                for start in range(0, len(runs), fan_in)]
        run_counts.append(len(runs))
    stages = len(run_counts)
    return runs[0], run_counts, stages, 2 * len(values) * stages


values = [13, 7, 2, 19, 5, 17, 11, 3, 23, 1, 9, 21, 15, 4, 8, 6, 10]
ordered, run_counts, stages, transfers = external_merge_reference(values, 4, 3)
print("run counts:", run_counts)
print("sorted:", ordered)
print("stages:", stages)
print("logical item transfers:", transfers)
```

Execution validates one in-memory simulation on the recorded interpreter. It does not perform storage I/O, enforce byte capacity, survive crashes, or establish device performance. Those claims require separate evidence.

### Plan fan-in and passes

If each input buffer is $b_i$ bytes and the output buffer is $b_o$, require

$$
\sum_{i=1}^{k}b_i+b_o+H+X\le M_{usable},
$$

where $H$ is selection/metadata state and $X$ covers decoding, allocation, and reserves. Equal block-sized buffers give a theoretical $k\approx M/B-1$, but larger buffers may be needed for efficient actual requests.

Starting from $R_0$ runs, balanced passes produce $R_{j+1}=\lceil R_j/k\rceil$. Uneven final groups are harmless. If a final pass would contain only one small group, allocate resources accordingly; do not pad with fake runs unless empty-run handling is explicit.

Polyphase schedules historically reduce rewinds or device requirements under constrained tape-like media. On modern storage, balanced multiway merge and explicit run placement are often simpler, but scheduling still matters when temporary devices, request quotas, or capacity differ. Device-era history should inform, not dictate, current design.

### Temporary-space accounting

During a safe pass, predecessor runs may coexist with successor runs until the successor is complete, verified, and durably registered. Peak temporary bytes can approach input-run bytes plus output-run bytes, along with buffers and metadata. In-place assumptions are dangerous across failure boundaries.

Delete inputs only after their successor's count, length, checksum, and ordering metadata are committed. Use unique immutable run IDs and a manifest that atomically advances lineage. Orphan partial files can be garbage-collected only after proving no committed manifest references them.

Compression changes both capacity and traffic. Bound decoded buffer expansion and pathological records. Checksums should cover the representation needed for replay; an encrypted run also needs key-version and authentication metadata.

### Parallel run generation and merging

Run generation is naturally parallel over disjoint chunks, but workers multiply memory and output bandwidth. Assign explicit per-worker budgets and cap concurrency. Parallel internal sorting helps only if storage supply and memory bandwidth do not dominate.

Independent merge groups can execute concurrently. A scheduler should balance input bytes, not merely run counts, because replacement selection and variable records create uneven runs. Avoid multiple groups contending on the same storage path. A final single merge may expose less parallelism; parallel partitioned merge requires sampled boundaries and exact nonoverlapping output ownership.

AlphaSort demonstrated that cache behavior, parallel processors, and striped storage jointly affect external-sort engineering [5]. Its 1995 measurements are historical evidence on its machine, not current universal ratios. The durable lesson is to design across the whole hierarchy and measure each bottleneck.

### Distribution sorting alternative

External distribution sort samples splitters, partitions records into bucket files, then recursively or internally sorts buckets. Good splitters can create mostly sequential partition writes and parallel independent buckets. Bad splitters create oversized buckets, extra passes, and capacity failures.

Equality policy is crucial under duplicate skew. Hashing equal-key occurrences across buckets may break global stability unless secondary occurrence identity defines contiguous ranges. Sampling bounds require their distribution and randomness assumptions. Merge sort offers more predictable pass structure; distribution sort can exploit keys and parallelism.

### Variable records and key normalization

Buffer and run planning uses bytes. A single record larger than a buffer needs a streaming representation, separate payload storage, or rejection. Store compact normalized keys or prefixes carefully: a prefix comparison needs fallback to full keys when equal. Collation keys can expand and their version must remain fixed.

Indirect sorting stores `(key, reference, occurrence)` records, sorts them externally, then gathers payloads. This reduces sort traffic but can transform final output into random reads. A later batched gather or rewriting payloads into run order may restore locality. Evaluate the complete pipeline.

### Failure and recovery protocol

Treat each run as immutable. Write to a new run ID, close and flush to the required boundary, verify length/count/checksum, then publish it in a durable manifest. A checkpoint records completed run generation or merge groups plus comparator and input snapshot identities.

On restart, trust only committed runs. Recompute an incomplete group from its immutable predecessors. Idempotent naming prevents duplicate publication. If input can change, pin a version or retain source offsets; otherwise replay may sort different data.

The final output becomes visible through an atomic local rename, transactional metadata change, or versioned object pointer appropriate to the storage system. “Rename” is not universally atomic across filesystems or object stores; use the platform's documented primitive and test failure points.

### Validation and evidence

Validate every run's adjacent order, count, byte length, checksum, key bounds, schema, and comparator version. During merge, verify output count equals the sum of inputs and optionally check stable occurrence monotonicity among equal keys. At the end, check orderedness and exact permutation using occurrence IDs or an independent multiset method; hashes alone have collision limitations.

Test empty input, one item, one run, partial final block, exact memory boundary, all equal, sorted, reverse, duplicate-heavy, giant record, invalid encoding, comparator exception, truncated run, corrupt checksum, short read/write, full temporary space, descriptor exhaustion, worker death, and crash before/after manifest publication.

Measure records and bytes, run counts/sizes, fan-in, passes, buffer sizes, read/write requests and bytes, cache state, compression, CPU comparisons, merge-structure operations, queue depth, stalls, concurrency, temporary peak, retries, checksum time, durability latency, and total time. Graefe surveys practical database sorting techniques and their resource adaptation [4]; use such sources to form hypotheses, then reproduce locally.

## Definitions and Notation

$N$ is total fixed-size items unless bytes are stated; $M$ is usable fast-memory capacity, $B$ transfer block size, $M_r$ run-generation record capacity, $R_j$ run count after stage $j$, $k$ effective merge fan-in, and $p$ merge-pass count. Run $Q_i$ is an immutable sorted sequence with count $n_i$.

A stable occurrence key is $(key(r_i),i)$. `Scan(N)=Θ(N/B)` and `Sort(N)=Θ((N/B)log_{M/B}(N/B))` retain the model-qualified meanings from ALGE-085. Logical traffic counts algorithm-visible items or bytes; physical traffic includes filesystem, device, replication, and amplification effects.

## Mechanisms, Invariants, or Proof Structure

### Run-generation proof

Show chunks are disjoint and cover the snapshot exactly. Prove the internal sort returns a stable ordered permutation. Bind each immutable run to count, checksum, comparator version, and input range.

### Multiway-merge proof

Maintain one position per run. The least current head is the least remaining occurrence globally because each run is sorted. Emit it with the stable tie rule and advance only that run. Induction establishes ordered permutation of consumed prefixes and terminates after the sum of input counts.

### Resource and pass proof

Derive $R_0$, legal $k$ from complete usable-memory accounting, recurrence $R_{j+1}=\lceil R_j/k\rceil$, and $p$. Sum reads/writes per stage, partial blocks, temporary coexistence, descriptors, and concurrent groups.

### Recovery proof

Every committed run is complete and immutable. A manifest transition references only verified successors. Restart discards uncommitted partial outputs and deterministically recomputes from committed predecessors. Final publication references exactly one verified terminal run.

## Alternatives and Trade-Offs

**Chunk sorting** is simple and robust; **replacement selection** can lengthen runs but adds heap/state cost and input-dependent guarantees. **Natural runs** exploit presortedness but need worst-case fallback.

**Higher fan-in** reduces passes but shrinks buffers and raises selection, descriptor, and request pressure. **Loser trees** improve repeated head selection; **heaps** are simpler. **Merge sorting** gives predictable passes; **distribution sorting** can parallelize buckets but risks skew.

**Full-record sorting** gives sequential final output at high traffic. **Indirect sorting** moves compact references but may defer random payload access. **Compression** reduces physical bytes while adding CPU and expansion risk. **Aggressive deletion** lowers temporary space; conservative immutable lineage strengthens recovery.

## Failure Modes and Misconceptions

- **“The data does not fit, so use virtual memory.”** unmanaged paging can create opaque random movement and weak recovery.
- **“Fan-in equals $M/B$.”** output, heap, decoder, metadata, workers, and reserve consume memory.
- **“Longer replacement-selection runs are guaranteed.”** run length depends on input order and assumptions.
- **“Stable local runs imply stable final output.”** every merge tie must preserve occurrence order.
- **“One merge pass is one read.”** a durable successor is also written.
- **“More workers reduce passes.”** they may only divide work while multiplying buffers and contention.
- **“Sorted output proves success.”** missing and duplicated records remain sorted.
- **“Checksums prove ordering.”** they detect corruption under stated limits, not comparator correctness.
- **“A closed file is durable.”** persistence requires the promised flush/replication boundary.
- **“Partial successor runs can resume anywhere.”** heap and buffer state make unsafe continuation subtle; recompute a group unless checkpoint semantics are complete.
- **“Historical disk ratios are current facts.”** retain mechanisms and remeasure the hierarchy.
- **“Temporary files are disposable immediately.”** predecessor deletion must follow verified committed lineage.

## Worked Examples

### Example 1

**Situation.** $N=17$ and usable run memory holds four records.

**Reasoning.** $R_0=\lceil17/4\rceil=5$. Run sizes are 4, 4, 4, 4, and 1; their disjoint ranges cover all occurrences.

**Conclusion.** Capacity uses ceilings and an explicit partial final run.

### Example 2

**Situation.** Five runs merge with fan-in three.

**Reasoning.** Counts evolve $5\to\lceil5/3\rceil=2\to1$, so two merge passes are required. Including generation gives three read/write stages.

**Conclusion.** Pass count follows run geometry, not record comparisons.

### Example 3

**Situation.** The preceding 17-item plan reads and writes every item each stage.

**Reasoning.** Logical transfers are $2\cdot17\cdot3=102$. Partial blocks and metadata refine physical I/O but do not change this declared item model.

**Conclusion.** State what traffic unit and stages include.

### Example 4

**Situation.** Two run heads have key 9, one from an earlier input range.

**Reasoning.** A stable merge emits the earlier occurrence first. Comparing only key and arbitrary heap position can reverse them while preserving key order.

**Conclusion.** Stability needs a durable tie key.

### Example 5

**Situation.** Replacement selection receives descending keys.

**Reasoning.** Every new key is smaller than the last emitted key and freezes for the next run. The hoped-for near-$2M$ average behavior disappears.

**Conclusion.** Expected run length is not a worst-case guarantee.

### Example 6

**Situation.** A 1 GiB budget launches four merges, each allocating 300 MiB.

**Reasoning.** Concurrent buffers alone need 1.2 GiB before heap and runtime state. Reduce concurrency or per-merge fan-in/buffers.

**Conclusion.** Global memory, not isolated operator memory, is invariant.

### Example 7

**Situation.** A single bucket receives 80% of records in distribution sort.

**Reasoning.** It exceeds internal capacity and needs extra partition passes, while other workers idle. Duplicate-aware splitters or merge sorting may be safer.

**Conclusion.** Sampling and equality policy govern distribution-sort depth.

### Example 8

**Situation.** A successor run is complete in page cache when the process deletes predecessors and crashes.

**Reasoning.** If the successor was not durable, all lineage may be lost. Flush, verify, and commit its manifest before predecessor deletion.

**Conclusion.** Safe cleanup follows durable publication.

### Example 9

**Situation.** Indirect sorting cuts temporary bytes tenfold but output consumers need payload order.

**Reasoning.** Random payload gathers can erase the saving. Batch gathers by source block or rewrite payloads sequentially, then measure the full pipeline.

**Conclusion.** Optimize through the required output boundary.

### Example 10

**Situation.** Restart sees a valid predecessor manifest and a truncated uncommitted successor.

**Reasoning.** Ignore and replace the partial successor under a unique attempt ID, remerge immutable predecessors, verify, then atomically advance the manifest.

**Conclusion.** Immutable runs make recovery a lineage decision.

## Cross-Program Connections

- **Database Engineering:** sort operators, merge joins, index builds, buffer managers, collations, and transactions operationalize external sorting.
- **Data Engineering:** shuffles, range partitions, spills, object storage, compaction, and skew use the same run and lineage mechanisms.
- **Operating Systems:** page cache, asynchronous I/O, filesystems, descriptors, writeback, and atomic rename shape implementation.
- **Platform Engineering:** temporary quotas, storage classes, worker budgets, monitoring, retries, and cleanup govern production execution.
- **Distributed Systems:** immutable artifacts, manifests, epochs, checksums, idempotence, and publication define recovery.
- **Software Delivery and Reliability Engineering:** fault injection, performance baselines, format compatibility, and rollback validate changes.

## References

1. Alok Aggarwal and Jeffrey Scott Vitter, “The Input/Output Complexity of Sorting and Related Problems,” *Communications of the ACM* 31(9), 1988, 1116–1127. DOI: [10.1145/48529.48535](https://doi.org/10.1145/48529.48535). Primary external sorting upper/lower bounds; ACM-linked and author records checked 2026-09-05.
2. Donald E. Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*, 2nd ed., Addison-Wesley, 1998. Authoritative treatment of external sorting, replacement selection, multiway merging, and historical storage constraints.
3. Jeffrey Scott Vitter, *Algorithms and Data Structures for External Memory*, Foundations and Trends in Theoretical Computer Science 2(4), 2008, 305–474. DOI: [10.1561/0400000014](https://doi.org/10.1561/0400000014). Authoritative external-memory monograph.
4. Goetz Graefe, “Implementing Sorting in Database Systems,” *ACM Computing Surveys* 38(3), 2006, Article 10. DOI: [10.1145/1132960.1132964](https://doi.org/10.1145/1132960.1132964). Survey of practical run generation, merging, memory adaptation, and database concerns; ACM-linked record checked 2026-09-05.
5. Chris Nyberg, Tom Barclay, Zarka Cvetanovic, Jim Gray, and David B. Lomet, “AlphaSort: A Cache-Sensitive Parallel External Sort,” *The VLDB Journal* 4(4), 1995, 603–627. Official VLDB paper and bibliographic record checked 2026-09-05; historical evidence for whole-hierarchy engineering.
6. Roman Dementiev, Lutz Kettner, and Peter Sanders, “STXXL: Standard Template Library for XXL Data Sets,” *Software: Practice and Experience* 38(6), 2008, 589–637. DOI: [10.1002/spe.844](https://doi.org/10.1002/spe.844). Primary external-memory library design and asynchronous I/O evidence.
7. Andreas Beckmann, Roman Dementiev, and Johannes Singler, “Building a Parallel Pipelines Framework for Multi-Core Programming,” *IPDPS Workshops*, 2010. DOI: [10.1109/IPDPSW.2010.5470837](https://doi.org/10.1109/IPDPSW.2010.5470837). Primary pipelined external-processing engineering; IEEE-linked record checked 2026-09-05.
8. Peter Sanders, Kurt Mehlhorn, Martin Dietzfelbinger, and Roman Dementiev, *Sequential and Parallel Algorithms and Data Structures: The Basic Toolbox*, Springer, 2019. DOI: [10.1007/978-3-030-25209-0](https://doi.org/10.1007/978-3-030-25209-0). Authoritative algorithm-engineering treatment of sorting and memory hierarchies.

## Exercises

### Exercise 1

Define run, run generation, replacement selection, stable $k$-way merge, fan-in, merge pass, logical traffic, committed run, and publication boundary. Explain why a sorted output need not be a correct external-sort result.

### Exercise 2

A fixed-record input has $N=10{,}000{,}000$, usable run capacity $M_r=625{,}000$, and effective fan-in $k=5$. Derive initial runs, run counts after every pass, merge-pass count, total read/write stages, and logical item traffic under the simple full-read/full-write model.

### Exercise 3

An implementation uses nominal RAM, assumes replacement selection always doubles run length, compares equal keys by heap slot, opens every run, omits output writes from traffic, deletes predecessors before flush, resumes truncated output, and validates only adjacent order. Diagnose each defect and prescribe a focused check.

### Exercise 4

Design a stable external sort for 20 TiB of variable-size records using local SSD scratch and versioned object storage. Specify comparator, run format, byte budgets, run generation, fan-in, scheduling, compression, temporary capacity, checksums, recovery, publication, validation, observability, and performance evidence.

### Exercise 5

A regulated archive must canonicalize events under a collation that may be upgraded, preserve duplicate order, accept late partitions, and prove which input snapshot produced each output. Transfer the chapter's reasoning into a versioned sorting and migration design, including what happens during partial failure.

## Answers to the Exercises

### Answer 1

A run is a sequence sorted by the final comparator. Run generation creates runs from memory-bounded input portions. Replacement selection uses active/frozen heap records to extend runs when input order permits. Stable $k$-way merge emits the least of up to $k$ heads and preserves original order on equal keys. Fan-in is simultaneous input-run count; a merge pass transforms one run set into fewer successors. Logical traffic counts algorithm-visible transferred items/bytes. A committed run is complete, verified, immutable, and referenced by durable lineage. Publication makes one verified terminal run the visible result. Adjacent order alone misses dropped/duplicated occurrences, wrong snapshot, instability, corruption, or undurable publication.

### Answer 2

$R_0=\lceil10{,}000{,}000/625{,}000\rceil=16$. With $k=5$, $R_1=\lceil16/5\rceil=4$ and $R_2=\lceil4/5\rceil=1$. Thus two merge passes follow run generation, for three read/write stages. Under the declared model, traffic is $2N(1+p)=2\cdot10{,}000{,}000\cdot3=60{,}000{,}000$ item transfers. Block rounding, metadata, compression, and final placement are excluded and must be added when mapping to storage.

### Answer 3

Nominal RAM omits buffers/runtime/concurrency; measure usable peak. Replacement-selection length is distribution-dependent; test descending and duplicate-heavy inputs. Heap-slot ties violate stability; compare durable occurrence order. Opening every run may exceed memory and descriptors; derive legal fan-in. Output writes are half of a full pass in the simple model; count them. Deleting before durable successor commit can lose lineage; flush, verify, manifest, then delete. A truncated merge lacks trustworthy selection/buffer state; recompute its group from immutable inputs unless a complete checkpoint exists. Order-only validation misses permutation and snapshot errors; verify counts, occurrence IDs or independent multiset evidence, stability, checksums, and lineage.

### Answer 4

Freeze an object-version input manifest and total key including durable occurrence identity. Encode self-describing immutable runs with schema/comparator versions, counts, byte lengths, key bounds, checksums, compression, and source lineage. Allocate memory by bytes across input/output buffers, internal stable-sort scratch, keys, decoders, and worker reserve. Generate SSD runs in bounded parallel chunks; upload or retain them according to scratch capacity. Choose fan-in from measured sequential request size, memory, descriptors, SSD bandwidth, and object multipart limits; balance groups by bytes and merge stably with a loser tree or heap. Bound coexistence of predecessors/successors, schedule cleanup after durable manifest transitions, and handle giant records. Authenticate/checksum every run, retry idempotently, and reconstruct incomplete groups. Publish a versioned terminal manifest only after validation and required replication. Check order, exact occurrence set, stability, byte/count sums, checksums, and replay after injected failures. Observe run histogram, passes, logical/physical bytes, requests, compression, CPU, memory and scratch peaks, queue depth, stalls, retries, durability, and end-to-end time.

### Answer 5

Treat collation rules and normalization tables as versioned comparator artifacts. Give each event a stable `(partition, sequence, event ID)` occurrence identity and sort by `(collation key, occurrence identity)` so duplicates are reproducible. Freeze an input manifest; late partitions create a new snapshot, not silent mutation of an old result. Preserve old comparator runs or rebuild every run under the new version—never merge mixed comparator versions. A migration writes new immutable runs and a terminal manifest alongside the old output, validates order/permutation/stability and source lineage, then atomically changes the archive's version pointer. On partial failure, keep the old published version, discard or resume only fully checkpointed new groups, and report the new snapshot unavailable until every referenced partition and verified successor is present.
