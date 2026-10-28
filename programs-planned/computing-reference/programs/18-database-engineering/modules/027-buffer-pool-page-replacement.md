---
module_id: DBE-027
program: Database Engineering
level: 1
module_number: 27
title: Buffer-Pool Page Replacement
status: complete
last_verified: 2026-08-30
---

# Buffer-Pool Page Replacement

## One-Page Review

### Governing question

When a buffer pool needs a frame, which eligible resident page should it replace so future I/O and stalls are minimized without violating pin, dirty, I/O, recovery, or concurrency constraints?

### Essential definitions

A **replacement policy** ranks or searches frames for reuse; it does not override eligibility. **Recency** measures time/accesses since the last reference; **frequency** measures repeated reuse. **LRU** evicts the least recently used eligible page. **Clock** approximates recency with a circular hand and reference/usage state. **LRU-K** uses the time of the K-th most recent reference to distinguish established reuse. **2Q** separates first-touch pages from repeatedly referenced pages. **Admission** decides whether/how a new page enters protected cache. **Scan resistance** prevents one-pass traffic from displacing a reused working set. A **ghost/history entry** remembers an evicted identity without retaining its page bytes.

### Central model, mechanism, or theorem

Belady's offline policy evicts the page whose next use is farthest in the future, but online systems do not know future references. Practical policies estimate reuse from bounded history under strict operational constraints. Victim selection is two-stage: policy proposes a frame; the buffer manager atomically verifies zero pins, no conflicting latch/I/O, correct tag/state, and clean or safely flushed status. Workload-dependent evidence—not a universal ranking—decides whether exact LRU, clock, history queues, adaptive schemes, or workload-specific rings are best.

### Critical invariants

- Only frames proven eligible under DBE-026's lifecycle may be recycled.
- Policy metadata updates cannot expose stale frame identity or corrupt pin/state accounting.
- Hits/misses, admissions, promotions, demotions, and evictions have defined linearization/accounting points.
- A dirty victim is preserved until WAL-compliant writeback succeeds; selection may retry afterward.
- One-pass scans/prefetch do not automatically receive the same protection as demonstrated reuse.
- History/ghost identifiers are generation-aware and never treated as resident bytes.
- Shards/rings/classes have bounded capacity and an explicit borrowing/fallback rule.
- Evaluation replays representative traces with equal capacity, eligibility, warmup, and cost definitions.

### Common failures

Failures include calling unpinned pages evictable without checking dirty/I/O/latches; implementing exact global LRU with a lock on every hit; giving speculative prefetch full recency credit; allowing a scan to flush the hot set; treating sequential pages as universally cold; ignoring looping scans; comparing policies with different memory or warmup; optimizing hit count when miss costs differ; omitting dirty-write cost and free-buffer waits; retaining unbounded ghost history; applying cache-wide statistics to one tenant/page class; and tuning one benchmark trace as a permanent universal policy.

### Compact example

With capacity three and trace `A,B,C,A,D,A,B,E`, exact LRU records two hits and six misses, evicting B, C, then D and ending with A,B,E. A simple one-bit clock records one hit and seven misses on this trace because all initial frames receive a second chance before recently reused A is encountered again; it ends E,A,B. This is not proof that LRU is universally better: clock has cheaper concurrent metadata, while scans can destroy strict LRU unless admission/rings/history protect the hot set.

### Connections

[DBE-026](026-buffer-pools.md) defines frame safety. [DBE-028](../ROADMAP.md) handles dirty-victim writeback; [DBE-060](../ROADMAP.md) later profiles query pipelines whose access patterns drive replacement.

## Governing Question

Replacement is an online prediction problem under correctness constraints. The manager observes past references but pays future misses. It also operates in a concurrent database where frames can be pinned, dirty, loading, latched, or reserved, and where pages differ in read cost, write cost, fanout value, and access class.

The governing question is therefore not “what is the best cache algorithm?” It is how a policy estimates reuse cheaply, admits traffic safely, avoids pathological interference, cooperates with writeback and buffer lifecycle, and proves benefit on the actual workload without turning metadata contention into the new bottleneck.

## Why This Matters

Replacement controls cache reach and tail latency. A poor victim choice converts later logical reads into storage requests, may block foreground work on dirty writeback, and can evict upper index levels or catalogs whose reuse value exceeds their byte count. A large scan can replace an OLTP working set in seconds.

Policy overhead matters at hit rates near 100% because nearly every request updates metadata. Exact list movement under a global lock can cost more than avoided misses. Sharded or approximate policies trade precision for throughput. The correct objective includes CPU, synchronization, I/O service time, dirty cost, fairness, and recovery pressure.

Results are workload-specific. Uniform random access, Zipf hot sets, sequential scans, cyclic scans, nested-loop reuse, mixed page sizes, index/root pages, prefetch, checkpointing, and multi-tenant bursts favor different choices. Benchmark evidence must preserve those phases and costs.

## Prerequisites and Retrieval

Retrieve buffer frames/pins/latches/dirty state, caches, stacks/queues, hash tables, circular arrays, probability, reuse distance, working sets, asynchronous I/O, WAL, concurrency, and experimental design.

Distinguish selection from eligibility; recency from frequency; admission from promotion; resident page from ghost identity; hit count from saved cost; logical miss from device I/O; scan resistance from scan avoidance; dirty selection from durable eviction; exact LRU from LRU-like product names; and offline optimal from implementable online policy.

## Learning Objectives

After this module, you should be able to:

1. simulate LRU and clock on a finite trace;
2. explain their metadata and concurrency trade-offs;
3. identify sequential/cyclic scan pollution;
4. explain LRU-K, 2Q, ghost history, and adaptive admission;
5. separate victim ranking from atomic eligibility checks;
6. include dirty and heterogeneous miss costs in policy reasoning;
7. design workload-class rings or partitions without stranded capacity;
8. interpret replacement metrics and reuse-distance evidence;
9. construct fair trace/workload experiments; and
10. diagnose churn, hot-set eviction, and replacement contention.

## Core Exposition

If future references were known, evicting the page used farthest in the future minimizes misses for a fixed cache on a reference string. That offline result is a benchmark lower bound, not an algorithm a running database can execute. Online policies infer future value from past behavior, query hints, page type, or learned/adaptive state.

Replacement applies only after DBE-026 establishes eligibility. A pinned frame cannot be recycled. A dirty frame requires safe writeback. A loading or I/O-owned frame has another lifecycle owner. A content latch can conflict. Policy metadata may say “cold,” but the buffer manager must atomically recheck current descriptor state before retagging.

LRU maintains resident pages from most to least recently used. A hit moves its page to the front; a miss evicts the eligible tail. It captures temporal locality and is intuitive, but exact maintenance can require pointer writes and synchronization on every hit. Concurrent implementations shard, batch, approximate, or sample rather than maintain one perfect global list.

LRU suffers scan pollution. A one-pass scan longer than the cache touches each page once, continuously making it most recent and eventually evicting a smaller hot set. When the scan pages are never reused, this replaces high-value pages with zero-future-value pages. Admission and protected/probationary regions address the problem.

Clock arranges frames conceptually in a circle. A reference sets a bit or increments a small usage counter. A moving hand skips pinned frames, clears/decrements positive usage, and selects an eligible zero-usage frame. It approximates recency with low metadata cost and no list move per hit. Multiple sweeps under widespread pins/high counts can increase search work.

PostgreSQL's official buffer README documents a clock-sweep with a bounded usage counter and a small ring strategy for large one-pass operations. The ring reuses a bounded subset rather than displacing the whole shared cache. This is a concrete design with engine-specific sizes and dirty behavior, not a universal constant.

InnoDB documents a midpoint-insertion LRU variant: new pages enter an “old” portion, while a qualifying later access promotes them to the “young” portion. Pages read ahead but never used age out without full protection. The old/new split and delay controls aim to keep scans from displacing repeatedly used pages.

Frequency helps distinguish a truly hot page from a single recent touch. Pure LFU can retain formerly popular pages after phase change and needs counters/aging. Recency-frequency hybrids bound history and adapt. They must define how correlated accesses within one operation count; repeatedly reading one tuple on a pinned page should not necessarily imply long-term reuse.

LRU-K records reference history and uses the K-th previous access to estimate interarrival/reuse. Pages with fewer than K observations receive probationary treatment. It improves scan resistance but consumes history and timestamp/ordering work and requires choices about K, correlated-reference windows, and history retention.

2Q uses queues to separate pages seen once from those seen again. A first touch enters a probationary FIFO; eviction can leave a bounded history identity. Re-reference promotes into a main LRU-like queue. This approximates frequency/history with constant-time structures and protects the main set from one-time scans.

Adaptive policies such as ARC-style designs use resident and ghost lists to balance recency and frequency based on where misses occur. Ghost entries contain identities and metadata, not page bytes; they reveal that recently evicted pages were requested again. History must be bounded and generation-aware to avoid memory leaks and false associations after relation rewrite.

Admission is as important as eviction. “Always admit” forces every miss to displace something. A policy can bypass cache, insert into probation, use frequency sketches, or admit only if the candidate appears more valuable than a victim. Database query plans can label sequential, bulk, temporary, or prefetch traffic, but hints can be wrong and must not compromise correctness.

Scan rings dedicate or borrow a small cyclic set for one-pass operations. They cap pollution and improve repeated transfer through a small memory footprint. If the scan is cyclic and its working set slightly exceeds the ring, the ring can thrash; if many pages are concurrently pinned, it may be too small. Dirty scan pages also couple ring reuse to WAL/writeback.

Partitioning by workload/page class isolates interference: index roots, catalogs, undo, heap, temporary, bulk scan, or tenants can receive separate quotas. Hard partitions strand capacity when one class is idle and another overloaded. Soft quotas with borrowing preserve isolation intent while allowing global utilization, but complicate accounting and fairness.

Page value can be cost-aware. A remote/compressed page may cost more to reload than a local sequential page. An upper B-tree page can save many downstream I/Os. A dirty victim has writeback cost. Cost-aware policies estimate `reuse probability * miss cost - retention cost`, but estimates and classification overhead can be wrong or gamed. Correctness must not depend on them.

Dirty pages complicate replacement without changing basic eligibility. A policy can prefer clean victims to avoid foreground stalls, but permanently avoiding dirty pages lets them monopolize the pool. Background writeback can prepare likely victims; DBE-028 covers coordination. Metrics should count proposed dirty victims, writeback waits, retries, and eventual reuse.

Pins distort the candidate set. A policy may encounter many cold-but-pinned frames and sweep repeatedly. Long pins can arise from valid operators or leaks. Replacement cannot solve a pin leak; it exposes it through scan length, no-victim waits, and pin-age/owner evidence.

Prefetch pages need careful admission. Giving a speculative read the same recency credit as a demand hit lets unused prefetch pollute the cache. A first actual use can promote it. Conversely, bypassing all prefetch loses value for accurate sequential/index readahead. Measure useful versus unused prefetched eviction.

Replacement metadata has race semantics. A hit that sets a reference bit concurrently with a hand clearing it must result in a permitted state, and the descriptor tag must remain stable for that update. ABA after frame reuse requires generation/tag recheck. Approximate lost recency can be acceptable; lost pins or dirty state cannot.

Global policy locks are scalability risks. Per-frame atomic counters, partitioned hands/lists, deferred access logs, sampling, and batched promotion reduce contention. Approximation error must be measured alongside CPU cycles, cache-line bouncing, lock wait, and miss cost. A policy with fewer misses can lose overall throughput.

Multi-page-size or compressed caches need byte-aware accounting. Evicting one 64 KiB frame is not equivalent to one 4 KiB frame. Object-count hit rate can favor large low-value items. Policies can rank value per byte and ensure enough contiguous/appropriate frames, while preserving separate compressed/uncompressed image relationships.

Warmup and phase change challenge history. Persisted recency from yesterday may be harmful after schema/workload change. Adaptive history needs decay/reset. Evaluation should include cold start, steady state, bursts, scans, phase transitions, and restart—not only a stationary trace.

Reuse distance counts distinct intervening pages between references. A page hits under ideal LRU capacity `C` when its stack distance is less than `C` (subject to initial compulsory misses). A miss-ratio curve across capacities reveals working-set knees, but real policies, pins, dirty eligibility, sharding, and cost heterogeneity diverge from the ideal.

Policy evaluation must use equal effective bytes and metadata overhead, identical reference traces/admission inputs, warmup, page sizes, pin/dirty states, and storage-cost models. Report compulsory, capacity, pollution, conflict/shard, and eligibility-induced misses where possible. Include policy CPU and contention, not only miss count.

Production metrics include hits/misses by page/workload class, eviction/admission/promotion/demotion counts, clean/dirty/no-victim rejections, clock scans/usage distribution, list/queue sizes, ghost hits, ring reuse, prefetch useful/unused, churn (pages loaded then quickly evicted), reuse distance, free waits, policy locks/atomics CPU, storage latency/bytes, checkpoint/writeback, and tenant fairness.

Testing uses deterministic traces with known results, property/model checks for capacity and uniqueness, pinned/dirty/in-flight frames, concurrent hit/hand races, all-ineligible pools, scan and cyclic patterns, hot-set plus scans, phase changes, skew, prefetch error, sharding imbalance, resize, relation generation reuse, faulted writeback, and long runs proving bounded history/counters.

The executable model compares exact LRU and one-bit clock on the same trace, then demonstrates a two-frame scan ring that preserves a separate two-page hot cache. It assumes all modeled victims are clean and unpinned and therefore does not model eligibility, dirty I/O, concurrency, or vendor behavior.

<!-- bijux-verify: {"id":"replacement-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"trace=('A', 'B', 'C', 'A', 'D', 'A', 'B', 'E')\nlru=(2, 6, ('A', 'B', 'E'), ('B', 'C', 'D'))\nclock=(1, 7, ('E', 'A', 'B'), (('A', 'D'), ('B', 'A'), ('C', 'B'), ('D', 'E')))\nhot_before=('H1', 'H2')\nscan_ring=('S5', 'S6')\nhot_after=('H1', 'H2')\nscan_resistant=True\n","stderr":""}} -->
```python
from collections import deque


def lru(trace: tuple[str, ...], capacity: int) -> tuple:
    cache: list[str] = []
    hits = misses = 0
    evicted = []
    for page in trace:
        if page in cache:
            hits += 1
            for position, resident in enumerate(cache):
                if resident == page:
                    del cache[position]
                    break
        else:
            misses += 1
            if len(cache) == capacity:
                evicted.append(cache.pop(0))
        cache.append(page)
    return hits, misses, tuple(cache), tuple(evicted)


def clock(trace: tuple[str, ...], capacity: int) -> tuple:
    frames: list[str | None] = [None] * capacity
    referenced = [0] * capacity
    hand = hits = misses = 0
    evicted = []
    for page in trace:
        if page in frames:
            hits += 1
            referenced[frames.index(page)] = 1
            continue
        misses += 1
        while frames[hand] is not None and referenced[hand]:
            referenced[hand] = 0
            hand = (hand + 1) % capacity
        if frames[hand] is not None:
            evicted.append((frames[hand], page))
        frames[hand] = page
        referenced[hand] = 1
        hand = (hand + 1) % capacity
    return hits, misses, tuple(frames), tuple(evicted)


trace = ("A", "B", "C", "A", "D", "A", "B", "E")
lru_result = lru(trace, 3)
clock_result = clock(trace, 3)
hot = list(lru(("H1", "H2", "H1", "H2"), 2)[2])
hot_before = tuple(hot)
scan_ring: deque[str] = deque(maxlen=2)
for page in ("S1", "S2", "S3", "S4", "S5", "S6"):
    scan_ring.append(page)
hot_after = tuple(hot)

print(f"trace={trace}")
print(f"lru={lru_result}")
print(f"clock={clock_result}")
print(f"hot_before={hot_before}")
print(f"scan_ring={tuple(scan_ring)}")
print(f"hot_after={hot_after}")
print(f"scan_resistant={hot_before == hot_after}")
```

The trace proves no general winner. It exposes policy differences under equal capacity and a deliberately isolated scan class; real systems must include metadata bytes, eligibility, dirty cost, concurrency, page sizes, and workload phases.

## Definitions and Notation

For reference sequence `r_1...r_T` and cache capacity `C`, a hit occurs when requested page is valid/resident and eligible for access; replacement runs on a miss needing capacity. LRU recency order is a stack from least to most recently referenced. Reuse distance for a repeated page is the number of distinct page identities referenced between its two accesses.

For page `p`, an abstract cost-aware value may be `V(p)=Pr(reuse before eviction horizon)*miss_cost(p)-retention_cost(p)`. This is a decision model, not an observable truth. Metadata, history, dirty cost, and page bytes must count against the same budget.

## Mechanisms, Invariants, or Proof Structure

A defensible replacement workflow is:

1. Define capacity in bytes including policy metadata and cache partitions.
2. Classify access source—demand, prefetch, scan, bulk, temporary—and apply documented admission.
3. Update recency/frequency/history only while frame identity is stable.
4. On capacity demand, select from the correct shard/class/ring with bounded search.
5. Atomically revalidate pin, latch, I/O, tag/generation, dirty, and writeback state.
6. If ineligible, preserve correctness state, feed rejection metrics, and continue/fallback with progress.
7. For dirty candidates, coordinate safe writeback; never discard the page or WAL obligation.
8. Remove/retag through DBE-026's page-table protocol; retain only bounded generation-aware ghost state.
9. Adapt quotas/history using stable measurements and bounded parameters.
10. Validate against trace models and representative concurrent workloads including CPU, stalls, I/O, fairness, and phase changes.

LRU's stack property permits miss-ratio derivation from reuse distance. Clock lacks exact stack inclusion but reduces update overhead. Neither property overrides eligibility: an ideal ranked victim that becomes pinned must be rejected.

## Alternatives and Trade-Offs

Exact LRU offers clear recency semantics but high mutation contention. Clock reduces hit-path work but approximates order and may sweep. LRU-K and 2Q improve scan resistance/history discrimination at memory and tuning cost. Adaptive ghost policies respond to workload but add lists, identities, and complex concurrent state.

Hard partitions isolate workloads but strand memory; global pools maximize utilization but allow interference; soft quotas/rings split the difference. Bypass avoids pollution but sacrifices unexpected reuse. Dirty-aware preference reduces foreground stalls but can trap dirty pages unless writeback progresses.

Cost-aware/learned policies can value expensive pages but require reliable features, bounded inference cost, drift detection, explainable fallback, and safety separation. A simple approximate policy with low contention often wins end-to-end despite more misses.

## Failure Modes and Misconceptions

- “LRU is optimal.” Only offline future-aware replacement is optimal for the fixed trace model.
- “Clock is LRU.” It is a low-overhead approximation with different trace behavior.
- “The coldest page is evictable.” Pins, I/O, dirty state, and latches decide eligibility.
- “Every hit should promote.” Correlated accesses and speculative prefetch can inflate value.
- “Scans are always one-touch.” Looping scans can have meaningful cyclic reuse.
- “Separate pools solve interference.” Hard boundaries can strand capacity or starve a class.
- “Ghost entries are free.” They consume memory and need bounds/generation invalidation.
- “More hits means faster.” Miss/write costs and policy contention differ.
- “Dirty pages should never be victims.” Avoidance without writeback can exhaust the pool.
- “One trace proves production superiority.” Capacity, phases, pins, costs, concurrency, and warmup must match.

## Worked Examples

### Example 1

Capacity-three LRU loads A,B,C. The next A is a hit and moves A most recent. D evicts B; A hits; B evicts C; E evicts D. Final order A,B,E gives two hits and six misses.

### Example 2

One-bit clock gives every initial frame a second chance. When D arrives, the hand clears A,B,C then replaces A; the immediately following A misses. This finite counterexample shows approximation error, not a universal clock defect.

### Example 3

A hot set H1,H2 fits capacity two. A separate two-frame ring cycles S1 through S6 and ends S5,S6 while H1,H2 remain resident. A global LRU of capacity two would end with scan pages instead.

### Example 4

A page is least recent but pinned by a join. The policy proposes it; atomic eligibility rejects it and advances. Replacement accuracy cannot justify violating the pin.

### Example 5

Two clean pages have equal reuse prediction, but one local miss costs 100 microseconds and one remote decompression costs 8 milliseconds. A cost-aware policy may retain the latter, provided classification overhead and future-reuse estimates are validated.

### Example 6

A dirty cold page is repeatedly skipped, eventually leaving most of the pool dirty and ineligible. Background writeback of likely victims restores replacement progress; simply preferring clean pages hid the backlog.

### Example 7

LRU-K sees one scan touch for S but repeated separated references for H. With K=2, H receives established-reuse evidence while S remains probationary. Correlated repeated accesses within one operator need a window so they do not masquerade as independent reuse.

### Example 8

2Q evicts a first-touch page but retains its identity in bounded history. A later reference promotes it to the main queue, distinguishing recurrence from a never-reused scan page without retaining payload bytes.

### Example 9

Tenant A scans 1 TB while tenant B's 10 GB hot index shares a global pool. Per-class soft quotas/rings protect B but allow A to borrow idle frames. Fairness metrics must include miss service time, not only frame counts.

### Example 10

Policy X reduces misses 3% but adds a contended global-list update to every hit, lowering throughput 15%. Policy Y's approximate counter has more misses but higher end-to-end throughput. Evaluation includes policy CPU and lock wait, so Y wins this workload.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies lists, queues, circular arrays, histories, sketches, and invariants.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies online algorithms, adversaries, competitive baselines, and trace evaluation.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page replacement, working sets, reuse distance, and memory pressure.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies atomic counters, sharding, races, and progress.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies fairness, observability, capacity, and workload experimentation.

## References

1. PostgreSQL Global Development Group, [Buffer Manager README](https://github.com/postgres/postgres/blob/master/src/backend/storage/buffer/README), clock-sweep, scan ring, dirty-victim, and concurrency design notes.
2. Oracle, [InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/8.4/en/innodb-buffer-pool.html), MySQL 8.4 midpoint LRU and old/new sublist documentation.
3. Oracle, [Making the Buffer Pool Scan Resistant](https://dev.mysql.com/doc/refman/8.4/en/innodb-performance-midpoint_insertion.html), MySQL 8.4 admission/promotion controls.
4. Elizabeth J. O'Neil, Patrick E. O'Neil, and Gerhard Weikum, [The LRU-K Page Replacement Algorithm for Database Disk Buffering](https://doi.org/10.1145/170035.170081), ACM SIGMOD 1993.
5. Theodore Johnson and Dennis Shasha, [2Q: A Low Overhead High Performance Buffer Management Replacement Algorithm](https://www.vldb.org/conf/1994/P439.PDF), VLDB 1994.
6. Nimrod Megiddo and Dharmendra S. Modha, [ARC: A Self-Tuning, Low Overhead Replacement Cache](https://www.usenix.org/conference/fast-03/arc-self-tuning-low-overhead-replacement-cache), FAST 2003.
7. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, buffer replacement foundations.
8. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, buffer-management foundations.

## Exercises

### Exercise 1

Simulate capacity-three LRU and one-bit clock for `A,B,C,B,D,A,B,E`. Give hits, misses, evictions, final frames/order, and hand/reference bits for clock.

### Exercise 2

A capacity-four cache holds hot H1,H2 and then scans S1–S8 once. Compare global LRU with a two-frame hot main plus two-frame scan ring. State memory fairness and what changes for a repeated looping scan.

### Exercise 3

Design a concurrent clock victim loop that handles pinned, dirty, loading, retagged, and positive-usage frames without losing progress or correctness.

### Exercise 4

Compare LRU, clock, LRU-2, 2Q, and an adaptive ghost policy for OLTP hot pages mixed with nightly scans, prefetch, phase changes, and expensive remote pages. Give evaluation criteria rather than one universal winner.

### Exercise 5

Design a production replacement-policy experiment. Include capacity/metadata parity, workload phases, cache warmup, pins/dirty state, costs, concurrency, tenants, failure, rollout, rollback, and proof limitations.

## Answers to the Exercises

### Answer 1

For LRU: A,B,C are misses; B hits and becomes most recent; D evicts A; A evicts C; B hits; E evicts D. Hits are 2, misses 6, evictions A,C,D, and least-to-most order is A,B,E after A was reinserted. For the chapter's clock convention, the hand starts at frame 0 and advances after every insertion. B is the only hit. Inserting D clears all three initial reference bits and replaces A; then A replaces B, B replaces C, and E clears the three new reference bits before replacing D. Clock therefore has 1 hit, 7 misses, replacements A→D, B→A, C→B, D→E, final frames E,A,B, hand at frame 1, and reference bits 1,0,0. Neither simulation alters pins or eligibility, and this result does not make clock equivalent to LRU.

### Answer 2

Global capacity-four LRU eventually contains the last four scan pages S5–S8; H1,H2 are evicted despite prior reuse. The split design keeps H1,H2 in its two main frames and ends with S7,S8 in the ring, using the same total four frames but hard-reserving half. If the scan repeats cyclically, a two-frame ring cannot retain an eight-page loop and will miss continuously; admission/history or borrowing based on measured recurrence may outperform permanent isolation. Soft quotas avoid wasting the main frames when hot pages disappear.

### Answer 3

Advance a shared/partitioned hand atomically and inspect one descriptor under its header protocol. If pinned or loading/I/O-owned, skip without changing correctness state. If usage is positive, atomically decrement only if the tag/generation is unchanged and continue. If zero, attempt to claim/pin an unchanged eligible frame; recheck tag, pins, latches/I/O, and dirty. A dirty frame is queued/written under DBE-028 and retried only after successful write; a concurrently pinned/retagged frame is released and skipped. Bound a sweep, expose no-victim waits, allow free/writeback progress, avoid holding global locks across I/O, and preserve dirty/page-table state on every failure.

### Answer 4

LRU captures immediate locality but pollutes under scans and has high concurrent list traffic. Clock lowers hit overhead and can pair with scan rings but approximates order. LRU-2 and 2Q distinguish repeated reuse from first touch; LRU-2 needs timestamps/history/window tuning, while 2Q uses bounded queues. Adaptive ghost policies can shift recency/frequency balance across phases but add state and complexity. Evaluate equal effective bytes, policy CPU/locks, miss latency/bytes by local versus remote page, dirty stalls, prefetch usefulness, OLTP tails during scan, phase adaptation, history memory, pin-induced sweeps, and fairness. Choose the measured end-to-end winner with simple fallback.

### Answer 5

Run baseline and candidate with equal page-plus-metadata bytes, page sizes/shards, storage, and query plans. Include cold/warm startup, steady OLTP, full and looping scans, bulk writes, checkpoint, prefetch accuracy, tenant bursts, and phase changes; preserve realistic pins, dirty ratios, WAL/writeback, and failures. Record logical hits/misses by class, storage service time/bytes, admissions/promotions/evictions, churn, clock/list work, dirty/pin rejections, no-victim waits, policy CPU/cache-line/lock contention, p50/p99, throughput, replicas, and memory. Canary behind reversible configuration with thresholds and rollback; replay deterministic traces plus production-shaped concurrency. State that observed workloads and fault tests do not prove future traces or universal optimality.
